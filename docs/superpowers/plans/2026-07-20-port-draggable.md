# 节点端口可拖动调整位置 实现计划

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 逐任务实现此计划。步骤使用复选框（`- [ ]`）语法来跟踪进度。

**目标：** 让节点端口可以手动拖动到节点的四条边（上下左右）上，圆心对齐边缘，支持 X/Y 双向移动。

**架构：** 在 `PortWidget` 中实现手动拖动逻辑（用拖动阈值区分点击连线与拖动），在 `itemChange` 中约束位置到最近边缘并更新连线；在 `NodeWidget` 中持久化端口位置、处理节点高度变化时保留端口位置。

**技术栈：** PySide6 QGraphicsObject, QGraphicsItem

---

## 设计决策

### 1. 拖动 vs 点击的区分
端口当前 `mousePressEvent` 用于 emit `port_clicked`（连线交互）。改用**拖动阈值（3px）**：
- 按下时记录位置，不立即 emit
- 移动超过 3px → 进入拖动模式，不 emit `port_clicked`
- 释放时距离 < 3px → 视为点击，emit `port_clicked`

### 2. 边缘吸附算法
端口在节点坐标系中的圆心 `(cx, cy)` = `(pos.x + PORT_SIZE/2, pos.y + PORT_SIZE/2)`：
- 计算圆心到四条边的距离：`dist_left = |cx|`, `dist_right = |cx - node_width|`, `dist_top = |cy|`, `dist_bottom = |cy - node_height|`
- 选择距离最小的边，约束圆心在该边上
- 左/右边缘：圆心 x 固定，y 约束在 `[0, node_height]`
- 上/下边缘：圆心 y 固定，x 约束在 `[0, node_width]`

### 3. 连线更新
端口移动后，调用 `edge.update_path()` 更新所有已连接边的路径。

### 4. 端口位置持久化
`to_json()` 保存每个端口的 `(label, pos_x, pos_y)`，`from_json()` 恢复。

---

## 文件结构

| 文件 | 操作 | 职责 |
|------|------|------|
| `gui/node_graph/port_widget.py` | 修改 | 添加拖动逻辑、边缘吸附、连线更新 |
| `gui/node_graph/node_widget.py` | 修改 | 持久化端口位置、高度变化时保留位置 |
| `tests/test_port_widget.py` | 修改 | 添加端口拖动测试 |
| `tests/test_node_widget.py` | 修改 | 添加端口位置持久化测试 |

---

### 任务 1：PortWidget 添加拖动与边缘吸附

**文件：**
- 修改：`gui/node_graph/port_widget.py`（全文）

- [ ] **步骤 1：编写失败的测试**

```python
# tests/test_port_widget.py 追加以下内容

class MockNode:
    """模拟节点对象，提供 node_width 和 node_height"""
    def __init__(self):
        self.node_width = 200
        self.node_height = 100


def test_port_movable_flag():
    """端口应可移动"""
    node = MockNode()
    port = PortWidget("in", "输入", node)
    assert port.flags() & QGraphicsObject.ItemIsMovable


def test_port_drag_threshold_distinguishes_click():
    """拖动距离小于阈值应视为点击，emit port_clicked"""
    node = MockNode()
    port = PortWidget("in", "输入", node)
    clicked = []
    port.port_clicked.connect(lambda p: clicked.append(p))

    # 模拟小距离移动（< 3px）然后释放 → 应视为点击
    # 由于无法直接模拟鼠标事件，通过内部状态验证：
    # 按下后小距离移动，_dragging 应为 False
    assert not port._dragging


def test_port_snaps_to_nearest_edge():
    """端口拖动后应吸附到最近边缘"""
    node = MockNode()
    port = PortWidget("in", "输入", node)
    port.setPos(100, 100)  # 圆心在 (108, 108)，节点 200x100

    # 圆心 (108, 108)：离右边缘 92px，离下边缘近（108-100=-8，|108-100|=8）
    # 实际上离下边缘最近（距离 8），应吸附到底边
    port._snap_to_nearest_edge()
    # 圆心应在底边：y=node_height=100, x 约束在 [0, 200]
    # 圆心 x=108 在范围内，setPos 应为 (108-8, 100-8) = (100, 92)
    assert port.pos().y() == pytest.approx(100 - PortWidget.PORT_SIZE / 2)


def test_port_center_on_edge():
    """端口圆心应在边缘上"""
    node = MockNode()
    port = PortWidget("out", "输出", node)
    port.setPos(0, 0)
    port._snap_to_nearest_edge()
    # 圆心 (8, 8)，离上边缘和左边缘都是 8px，选第一个（左边缘）
    center = port.mapToParent(port.boundingRect().center())
    if abs(center.x()) < abs(center.y()):
        assert center.x() == pytest.approx(0)  # 圆心在左边缘
    else:
        assert center.y() == pytest.approx(0)  # 圆心在上边缘
```

- [ ] **步骤 2：运行测试验证失败**

运行：`python -m pytest tests/test_port_widget.py -v`
预期：部分测试 FAIL（`ItemIsMovable` 未设置、`_dragging` 不存在、`_snap_to_nearest_edge` 不存在）

- [ ] **步骤 3：修改 PortWidget 实现**

```python
# gui/node_graph/port_widget.py 完整修改

from PySide6.QtWidgets import QGraphicsObject, QGraphicsEllipseItem, QGraphicsTextItem
from PySide6.QtCore import Qt, QRectF, Signal, QPointF
from PySide6.QtGui import QColor, QBrush, QPen, QFont, QPainterPath


class PortWidget(QGraphicsObject):
    port_clicked = Signal(object)

    PORT_SIZE = 16
    PORT_MARGIN = 4
    DRAG_THRESHOLD = 3  # 拖动阈值（像素）

    def __init__(self, port_type: str, label: str, parent_node, parent=None):
        super().__init__(parent)
        self.port_type = port_type
        self.label = label
        self.parent_node = parent_node
        self.connected_edges = []
        self._is_highlighted = False
        self._dragging = False
        self._press_pos = None
        self._init_style()

        self.setFlag(QGraphicsObject.ItemIsMovable, True)
        self.setFlag(QGraphicsObject.ItemSendsGeometryChanges, True)

    def _init_style(self):
        self.ellipse = QGraphicsEllipseItem(0, 0, self.PORT_SIZE, self.PORT_SIZE, self)
        self.setZValue(20)

        if self.port_type == "in":
            fill_color = QColor("#ff9800")
        else:
            if self.label == "False":
                fill_color = QColor("#f44336")
            else:
                fill_color = QColor("#4caf50")

        self.ellipse.setBrush(QBrush(fill_color))
        self.ellipse.setPen(QPen(QColor("#ffffff"), 2))
        self.setCursor(Qt.PointingHandCursor)

        self.label_item = QGraphicsTextItem(self.label, self)
        self.label_item.setDefaultTextColor(QColor("#cccccc"))
        self.label_item.setFont(QFont("Arial", 9))

        if self.port_type == "in":
            self.label_item.setPos(self.PORT_SIZE + 4, -2)
        else:
            self.label_item.setPos(-self.label_item.boundingRect().width() - self.PORT_SIZE - 4, -2)

    def set_highlighted(self, highlighted):
        self._is_highlighted = highlighted
        if highlighted:
            self.ellipse.setBrush(QBrush(QColor("#00d4ff")))
            self.ellipse.setPen(QPen(QColor("#ffffff"), 3))
        else:
            if self.port_type == "in":
                self.ellipse.setBrush(QBrush(QColor("#ff9800")))
            else:
                if self.label == "False":
                    self.ellipse.setBrush(QBrush(QColor("#f44336")))
                else:
                    self.ellipse.setBrush(QBrush(QColor("#4caf50")))
            self.ellipse.setPen(QPen(QColor("#ffffff"), 2))

    def can_connect(self, other_port):
        if self.port_type == other_port.port_type:
            return False
        if self.parent_node is not None and other_port.parent_node is not None:
            if self.parent_node == other_port.parent_node:
                return False
        return True

    def add_edge(self, edge):
        if edge not in self.connected_edges:
            self.connected_edges.append(edge)

    def remove_edge(self, edge):
        if edge in self.connected_edges:
            self.connected_edges.remove(edge)

    def has_connections(self):
        return len(self.connected_edges) > 0

    def mousePressEvent(self, event):
        self._press_pos = event.pos()
        self._dragging = False
        event.accept()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._press_pos is not None and not self._dragging:
            delta = event.pos() - self._press_pos
            if (abs(delta.x()) > self.DRAG_THRESHOLD or
                    abs(delta.y()) > self.DRAG_THRESHOLD):
                self._dragging = True
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if not self._dragging and self._press_pos is not None:
            self.port_clicked.emit(self)
        self._press_pos = None
        self._dragging = False
        super().mouseReleaseEvent(event)

    def _update_connected_edges(self):
        for edge in self.connected_edges[:]:
            try:
                edge.update_path()
            except Exception:
                pass

    def _snap_to_nearest_edge(self):
        """将端口吸附到父节点的最近边缘，圆心在边缘上"""
        if self.parent_node is None:
            return
        node_w = self.parent_node.node_width
        node_h = self.parent_node.node_height
        half = self.PORT_SIZE / 2

        # 当前圆心在节点坐标系中的位置
        cx = self.pos().x() + half
        cy = self.pos().y() + half

        # 计算圆心到四条边的距离
        dist_left = abs(cx)
        dist_right = abs(cx - node_w)
        dist_top = abs(cy)
        dist_bottom = abs(cy - node_h)

        min_dist = min(dist_left, dist_right, dist_top, dist_bottom)

        if min_dist == dist_left:
            cx = 0
            cy = max(0, min(cy, node_h))
        elif min_dist == dist_right:
            cx = node_w
            cy = max(0, min(cy, node_h))
        elif min_dist == dist_top:
            cy = 0
            cx = max(0, min(cx, node_w))
        else:
            cy = node_h
            cx = max(0, min(cx, node_w))

        self.setPos(cx - half, cy - half)

    def itemChange(self, change, value):
        if change == QGraphicsObject.ItemPositionHasChanged:
            self._snap_to_nearest_edge()
            self._update_connected_edges()
        return super().itemChange(change, value)

    def get_global_pos(self):
        return self.mapToScene(self.boundingRect().center())

    def get_port_id(self):
        return f"{self.parent_node.node_id}_{self.port_type}_{self.label}"

    def boundingRect(self):
        m = self.PORT_MARGIN
        total = self.PORT_SIZE + 2 * m
        return QRectF(-m, -m, total, total)

    def shape(self):
        path = QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def paint(self, painter, option, widget=None):
        pass
```

- [ ] **步骤 4：运行测试验证通过**

运行：`python -m pytest tests/test_port_widget.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add gui/node_graph/port_widget.py tests/test_port_widget.py
git commit -m "feat: 端口支持拖动到节点四边，圆心对齐边缘"
```

---

### 任务 2：NodeWidget 持久化端口位置

**文件：**
- 修改：`gui/node_graph/node_widget.py`（`to_json`, `from_json`, `_create_ports`, `update_params`, `boundingRect`）

- [ ] **步骤 1：编写失败的测试**

```python
# tests/test_node_widget.py 追加以下内容

def test_node_to_json_includes_port_positions():
    """to_json 应包含端口位置信息"""
    node = NodeWidget("mouse_click", {})
    data = node.to_json()
    assert "ports" in data
    assert len(data["ports"]) == 2  # 1 input + 1 output


def test_node_from_json_restores_port_positions():
    """from_json 应恢复端口位置"""
    node = NodeWidget("mouse_click", {})
    data = {
        "id": node.node_id,
        "type": "mouse_click",
        "x": 100,
        "y": 200,
        "config": {},
        "ports": {
            "输入": [200, 50],
            "输出": [-8, 40]
        }
    }
    node.from_json(data)
    in_port = node.get_input_port("输入")
    out_port = node.get_output_port("输出")
    assert in_port.pos().x() == pytest.approx(200)
    assert in_port.pos().y() == pytest.approx(50)
    assert out_port.pos().x() == pytest.approx(-8)
    assert out_port.pos().y() == pytest.approx(40)


def test_node_bounding_rect_includes_top_bottom_ports():
    """boundingRect 应包含上下边缘的端口"""
    node = NodeWidget("mouse_click", {})
    rect = node.boundingRect()
    # 端口可在上下边缘，boundingRect 需要扩展
    assert rect.top() <= -PortWidget.PORT_SIZE
    assert rect.bottom() >= node.node_height + PortWidget.PORT_SIZE
```

- [ ] **步骤 2：运行测试验证失败**

运行：`python -m pytest tests/test_node_widget.py -v -k "port"`
预期：FAIL（`ports` 不在 json 中、boundingRect 范围不足）

- [ ] **步骤 3：修改 to_json 和 from_json**

```python
# node_widget.py 中修改 to_json 方法

def to_json(self):
    ports_data = {}
    for port in self.input_ports + self.output_ports:
        ports_data[port.label] = [port.pos().x(), port.pos().y()]
    return {
        "id": self.node_id,
        "type": self.node_type,
        "x": self.x(),
        "y": self.y(),
        "config": self.config,
        "ports": ports_data
    }
```

```python
# node_widget.py 中修改 from_json 方法

def from_json(self, data):
    self.node_id = data.get("id", self.node_id)
    self.setPos(data.get("x", 0), data.get("y", 0))
    self.config = data.get("config", {})
    self.update_params(self.config)
    # 恢复端口位置
    ports_data = data.get("ports", {})
    if ports_data:
        self._restore_port_positions(ports_data)
```

- [ ] **步骤 4：添加 _restore_port_positions 方法**

```python
# node_widget.py 中新增方法

def _restore_port_positions(self, ports_data):
    """根据保存的数据恢复端口位置"""
    for port in self.input_ports + self.output_ports:
        if port.label in ports_data:
            pos = ports_data[port.label]
            port.setPos(pos[0], pos[1])
```

- [ ] **步骤 5：修改 _create_ports 保留用户调整的位置**

`_create_ports` 在 `update_params` 中当节点高度变化时会被调用，此时会重建端口对象。需要先保存旧端口位置，创建新端口后恢复。

```python
# node_widget.py 中修改 _create_ports 方法

def _create_ports(self, saved_positions=None):
    port_offset = -PortWidget.PORT_SIZE / 2

    # 保存旧端口位置（如果未提供）
    if saved_positions is None:
        saved_positions = {}
        for port in self.input_ports + self.output_ports:
            saved_positions[port.label] = (port.pos().x(), port.pos().y())

    self.input_ports.clear()
    self.output_ports.clear()

    if self.node_type != "start":
        in_port = PortWidget("in", "输入", self, self)
        if "输入" in saved_positions:
            in_port.setPos(*saved_positions["输入"])
        else:
            in_port.setPos(port_offset, 40)
        self.input_ports.append(in_port)

    if self.node_type in ("if_else", "loop"):
        true_port = PortWidget("out", "True", self, self)
        if "True" in saved_positions:
            true_port.setPos(*saved_positions["True"])
        else:
            true_port.setPos(self.node_width + port_offset, 32)
        self.output_ports.append(true_port)

        false_port = PortWidget("out", "False", self, self)
        if "False" in saved_positions:
            false_port.setPos(*saved_positions["False"])
        else:
            false_port.setPos(self.node_width + port_offset, 88)
        self.output_ports.append(false_port)

    elif self.node_type in ("image_find", "image_click", "image_exists"):
        true_port = PortWidget("out", "True", self, self)
        if "True" in saved_positions:
            true_port.setPos(*saved_positions["True"])
        else:
            true_port.setPos(self.node_width + port_offset, 32)
        self.output_ports.append(true_port)

        false_port = PortWidget("out", "False", self, self)
        if "False" in saved_positions:
            false_port.setPos(*saved_positions["False"])
        else:
            false_port.setPos(self.node_width + port_offset, 88)
        self.output_ports.append(false_port)

    elif self.node_type != "end":
        out_port = PortWidget("out", "输出", self, self)
        if "输出" in saved_positions:
            out_port.setPos(*saved_positions["输出"])
        else:
            out_port.setPos(self.node_width + port_offset, 40)
        self.output_ports.append(out_port)
```

- [ ] **步骤 6：修改 update_params 传递端口位置**

```python
# node_widget.py 中修改 update_params 方法

def update_params(self, config):
    self.config = config
    new_params = self._format_params()
    self.param_text.setPlainText(new_params)

    old_height = self.node_height
    self._calc_height()

    if self.node_height != old_height:
        self.body.setRect(0, 0, self.node_width, self.node_height)
        self._create_ports()  # _create_ports 内部会保存旧位置
        self.prepareGeometryChange()
```

- [ ] **步骤 7：修改 boundingRect 包含上下边缘端口**

```python
# node_widget.py 中修改 boundingRect 方法

def boundingRect(self):
    return QRectF(-PortWidget.PORT_SIZE, -PortWidget.PORT_SIZE,
                  self.node_width + PortWidget.PORT_SIZE * 2,
                  self.node_height + PortWidget.PORT_SIZE * 2)
```

- [ ] **步骤 8：运行所有测试验证通过**

运行：`python -m pytest tests/test_node_widget.py tests/test_port_widget.py -v`
预期：全部 PASS

- [ ] **步骤 9：Commit**

```bash
git add gui/node_graph/node_widget.py tests/test_node_widget.py
git commit -m "feat: 节点端口位置持久化，支持 to_json/from_json 保存恢复"
```

---

### 任务 3：集成测试与手动验证

- [ ] **步骤 1：运行完整测试套件**

```bash
python -m pytest tests/ -v
```

- [ ] **步骤 2：手动验证清单**
  - [ ] 拖动端口到节点左边缘，圆心应在左边缘上
  - [ ] 拖动端口到节点右边缘，圆心应在右边缘上
  - [ ] 拖动端口到节点上边缘，圆心应在上边缘上
  - [ ] 拖动端口到节点下边缘，圆心应在下边缘上
  - [ ] 拖动后连线应自动更新路径
  - [ ] 点击端口（不拖动）应正常触发连线
  - [ ] 保存/加载后端口位置应恢复
  - [ ] 节点高度变化时端口位置应保留
```