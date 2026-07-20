# 连线控制点可拖动调整 实现计划

> 面向 AI 代理的工作者：使用 superpowers:executing-plans 逐任务实现此计划。步骤使用复选框（`- [ ]`）语法来跟踪进度。

**目标：** 连线贝塞尔曲线的两个控制点可通过拖动手柄自由调整，控制点位置持久化到 JSON 保存/加载。

**架构：** 在 `edge_widget.py` 中新增 `ControlPointHandle` 类（`QGraphicsObject`，作为 `EdgeWidget` 的子项），选中连线时显示手柄，拖动手柄更新控制点偏移比例，`update_path()` 根据偏移量 + 端口位置计算实际控制点坐标。

**技术栈：** PySide6 QGraphicsObject, QPainterPath cubicTo

---

### 任务 1：新增 ControlPointHandle 类 + 集成到 EdgeWidget

**文件：**
- 修改：`gui/node_graph/edge_widget.py`

- [ ] **步骤 1：在 edge_widget.py 顶部新增 ControlPointHandle 类**

```python
class ControlPointHandle(QGraphicsObject):
    """贝塞尔曲线控制点手柄，选中边时显示，可拖动调整曲线形状"""
    SIZE = 10
    COLOR = QColor("#ffaa00")
    COLOR_HOVER = QColor("#ffcc44")

    def __init__(self, edge, parent=None):
        super().__init__(parent)
        self._edge = edge
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsObject.ItemIsMovable, True)
        self.setFlag(QGraphicsObject.ItemSendsGeometryChanges, True)
        self.setCursor(Qt.CursorShape.SizeAllCursor)
        self.setZValue(10)
        self.setVisible(False)

    def boundingRect(self):
        return QRectF(-self.SIZE, -self.SIZE, self.SIZE * 2, self.SIZE * 2)

    def shape(self):
        path = QPainterPath()
        path.addEllipse(self.boundingRect())
        return path

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor("#cc8800"), 1.5))
        painter.setBrush(QBrush(self.COLOR))
        painter.drawEllipse(QPointF(0, 0), self.SIZE, self.SIZE)

    def hoverEnterEvent(self, event):
        self.update()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.update()
        super().hoverLeaveEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsObject.ItemPositionHasChanged:
            self._edge._on_handle_moved()
        return super().itemChange(change, value)
```

- [ ] **步骤 2：修改 EdgeWidget.__init__，创建两个 ControlPointHandle**

在 `self.update_path()` 之前添加：

```python
self._cp1_offset = (0.25, 0.0)
self._cp2_offset = (0.75, 0.0)

self._cp1_handle = ControlPointHandle(self, self)
self._cp2_handle = ControlPointHandle(self, self)
```

- [ ] **步骤 3：修改 EdgeWidget.itemChange，选中时显示/隐藏手柄**

在 `ItemSelectedChange` 分支中，`value` 为 True 时显示手柄，False 时隐藏：

```python
def itemChange(self, change, value):
    if change == QGraphicsPathItem.ItemSelectedChange:
        if value:
            self.setPen(QPen(QColor("#00d4ff"), 3))
            self.setZValue(5)
            self._cp1_handle.setVisible(True)
            self._cp2_handle.setVisible(True)
        else:
            self.setPen(QPen(QColor("#5a5aff"), 2))
            self.setZValue(-1)
            self._cp1_handle.setVisible(False)
            self._cp2_handle.setVisible(False)
    return super().itemChange(change, value)
```

- [ ] **步骤 4：修改 EdgeWidget.update_path，使用 (u,v) 坐标系计算控制点**

偏移量 `(u, v)` 含义：`u` = 沿向量方向的比例，`v` = 垂直方向的比例。
控制点 = start + vector * u + perpendicular * v，其中 perpendicular = (vector.y, -vector.x)。

```python
def update_path(self):
    try:
        if not hasattr(self, 'source_port') or not hasattr(self, 'target_port'):
            return
        start_point = self.source_port.get_global_pos()
        end_point = self.target_port.get_global_pos()

        dx = end_point.x() - start_point.x()
        dy = end_point.y() - start_point.y()

        cp1 = QPointF(
            start_point.x() + dx * self._cp1_offset[0] + dy * self._cp1_offset[1],
            start_point.y() + dy * self._cp1_offset[0] - dx * self._cp1_offset[1]
        )
        cp2 = QPointF(
            start_point.x() + dx * self._cp2_offset[0] + dy * self._cp2_offset[1],
            start_point.y() + dy * self._cp2_offset[0] - dx * self._cp2_offset[1]
        )

        path = QPainterPath()
        path.moveTo(start_point)
        path.cubicTo(cp1, cp2, end_point)
        self.setPath(path)

        self._update_handles()
    except Exception:
        pass
```

- [ ] **步骤 5：新增 _update_handles 和 _on_handle_moved 方法**

```python
def _update_handles(self):
    """根据 (u,v) 偏移量 + 端口位置更新手柄场景坐标"""
    try:
        start_point = self.source_port.get_global_pos()
        end_point = self.target_port.get_global_pos()
        dx = end_point.x() - start_point.x()
        dy = end_point.y() - start_point.y()

        cp1_pos = QPointF(
            start_point.x() + dx * self._cp1_offset[0] + dy * self._cp1_offset[1],
            start_point.y() + dy * self._cp1_offset[0] - dx * self._cp1_offset[1]
        )
        cp2_pos = QPointF(
            start_point.x() + dx * self._cp2_offset[0] + dy * self._cp2_offset[1],
            start_point.y() + dy * self._cp2_offset[0] - dx * self._cp2_offset[1]
        )
        self._cp1_handle.setPos(cp1_pos)
        self._cp2_handle.setPos(cp2_pos)
    except Exception:
        pass

def _on_handle_moved(self):
    """手柄被拖动后，反算 (u,v) 偏移量并更新曲线"""
    try:
        start_point = self.source_port.get_global_pos()
        end_point = self.target_port.get_global_pos()
        dx = end_point.x() - start_point.x()
        dy = end_point.y() - start_point.y()

        denom = dx * dx + dy * dy
        if denom < 0.001:
            return

        cp1_pos = self._cp1_handle.pos()
        delta1_x = cp1_pos.x() - start_point.x()
        delta1_y = cp1_pos.y() - start_point.y()
        self._cp1_offset = (
            (dx * delta1_x + dy * delta1_y) / denom,
            (dy * delta1_x - dx * delta1_y) / denom
        )

        cp2_pos = self._cp2_handle.pos()
        delta2_x = cp2_pos.x() - start_point.x()
        delta2_y = cp2_pos.y() - start_point.y()
        self._cp2_offset = (
            (dx * delta2_x + dy * delta2_y) / denom,
            (dy * delta2_x - dx * delta2_y) / denom
        )

        self.update_path()
    except Exception:
        pass
```

- [ ] **步骤 6：运行现有测试，确保不破坏已有功能**

```bash
python -m pytest tests/test_edge_widget.py -v --tb=short
```

预期：现有测试 PASS

- [ ] **步骤 7：Commit**

```bash
git add gui/node_graph/edge_widget.py
git commit -m "feat: 新增 ControlPointHandle，选中连线时显示可拖动控制点手柄（任务 1/4）"
```

---

### 任务 2：控制点位置持久化（to_json / from_json）

**文件：**
- 修改：`gui/node_graph/edge_widget.py`

- [ ] **步骤 1：修改 EdgeWidget.to_json，增加 cp1/cp2 偏移量**

```python
def to_json(self):
    return {
        "source_node": self.source_node.node_id,
        "source_port": self.source_port.label,
        "target_node": self.target_node.node_id,
        "target_port": self.target_port.label,
        "cp1": {"x": self._cp1_offset[0], "y": self._cp1_offset[1]},
        "cp2": {"x": self._cp2_offset[0], "y": self._cp2_offset[1]}
    }
```

- [ ] **步骤 2：新增 EdgeWidget.from_json 方法**

```python
def from_json(self, data):
    cp1 = data.get("cp1", {"x": 0.25, "y": 0.0})
    cp2 = data.get("cp2", {"x": 0.75, "y": 0.0})
    self._cp1_offset = (cp1.get("x", 0.25), cp1.get("y", 0.0))
    self._cp2_offset = (cp2.get("x", 0.75), cp2.get("y", 0.0))
    self.update_path()
```

- [ ] **步骤 3：在 GraphScene.from_json 中调用 edge.from_json**

修改 `gui/node_graph/graph_scene.py` 的 `from_json` 方法，在 `add_edge` 之后调用 `edge.from_json(edge_data)`：

```python
for edge_data in data.get("edges", []):
    source_node = node_map.get(edge_data["source_node"])
    target_node = node_map.get(edge_data["target_node"])
    if source_node and target_node:
        source_port = source_node.get_output_port(edge_data["source_port"])
        target_port = target_node.get_input_port(edge_data["target_port"])
        if source_port and target_port:
            edge = self.add_edge(source_port, target_port)
            edge.from_json(edge_data)
```

- [ ] **步骤 4：在 node_handler.load_nodes_from_flow 中调用 edge.from_json**

修改 `gui/main_window/node_handler.py` 的 `load_nodes_from_flow` 方法：

```python
for edge_data in edges:
    try:
        source_node = node_map.get(edge_data["source_node"])
        target_node = node_map.get(edge_data["target_node"])
        if source_node and target_node:
            source_port = source_node.get_output_port(edge_data["source_port"])
            target_port = target_node.get_input_port(edge_data["target_port"])
            if source_port and target_port:
                edge = self.graph_scene.add_edge(source_port, target_port)
                edge.from_json(edge_data)
    except Exception as e:
        print(f"加载连线失败: {e}")
```

- [ ] **步骤 5：在 NodeEditorDialog._load_data 中调用 edge.from_json**

修改 `gui/widgets/node_editor_dialog.py` 的 `_load_data` 方法：

```python
for edge_data in edges:
    source_node = node_map.get(edge_data.get("source_node"))
    target_node = node_map.get(edge_data.get("target_node"))
    if source_node and target_node:
        source_port = source_node.get_output_port(edge_data.get("source_port", "输出"))
        target_port = target_node.get_input_port(edge_data.get("target_port", "输入"))
        if source_port and target_port:
            edge = self.graph_scene.add_edge(source_port, target_port)
            edge.from_json(edge_data)
```

- [ ] **步骤 6：运行现有测试，确保不破坏已有功能**

```bash
python -m pytest tests/ -v --tb=short
```

预期：所有测试 PASS

- [ ] **步骤 7：Commit**

```bash
git add gui/node_graph/edge_widget.py gui/node_graph/graph_scene.py gui/main_window/node_handler.py gui/widgets/node_editor_dialog.py
git commit -m "feat: 控制点偏移量持久化，to_json/from_json 保存和恢复 cp1/cp2（任务 2/4）"
```

---

### 任务 3：编写单元测试

**文件：**
- 修改：`tests/test_edge_widget.py`

- [ ] **步骤 1：添加测试 — 控制点手柄创建且初始隐藏**

```python
def test_control_point_handles_created():
    """EdgeWidget 创建时包含两个 ControlPointHandle，初始隐藏"""
    scene = GraphScene()
    node1 = scene.add_node("mouse_click", 100, 100)
    node2 = scene.add_node("mouse_click", 400, 100)
    source_port = node1.get_output_port("输出")
    target_port = node2.get_input_port("输入")
    edge = scene.add_edge(source_port, target_port)

    assert hasattr(edge, '_cp1_handle')
    assert hasattr(edge, '_cp2_handle')
    assert not edge._cp1_handle.isVisible()
    assert not edge._cp2_handle.isVisible()
```

- [ ] **步骤 2：添加测试 — 选中时手柄可见**

```python
def test_handles_visible_on_selected():
    """选中边时控制点手柄可见"""
    scene = GraphScene()
    node1 = scene.add_node("mouse_click", 100, 100)
    node2 = scene.add_node("mouse_click", 400, 100)
    edge = scene.add_edge(node1.get_output_port("输出"), node2.get_input_port("输入"))

    edge.setSelected(True)
    assert edge._cp1_handle.isVisible()
    assert edge._cp2_handle.isVisible()

    edge.setSelected(False)
    assert not edge._cp1_handle.isVisible()
    assert not edge._cp2_handle.isVisible()
```

- [ ] **步骤 3：添加测试 — 控制点持久化**

```python
def test_control_points_persisted():
    """to_json/from_json 包含控制点偏移量"""
    scene = GraphScene()
    node1 = scene.add_node("mouse_click", 100, 100)
    node2 = scene.add_node("mouse_click", 400, 100)
    edge = scene.add_edge(node1.get_output_port("输出"), node2.get_input_port("输入"))

    edge._cp1_offset = (0.3, 0.1)
    edge._cp2_offset = (0.7, -0.1)

    data = edge.to_json()
    assert data["cp1"]["x"] == 0.3
    assert data["cp1"]["y"] == 0.1
    assert data["cp2"]["x"] == 0.7
    assert data["cp2"]["y"] == -0.1

    edge._cp1_offset = (0.25, 0.0)
    edge._cp2_offset = (0.75, 0.0)
    edge.from_json(data)
    assert edge._cp1_offset == (0.3, 0.1)
    assert edge._cp2_offset == (0.7, -0.1)
```

- [ ] **步骤 4：添加测试 — 默认偏移量**

```python
def test_control_points_default_offsets():
    """EdgeWidget 创建时控制点偏移量为默认值"""
    scene = GraphScene()
    node1 = scene.add_node("mouse_click", 100, 100)
    node2 = scene.add_node("mouse_click", 400, 100)
    edge = scene.add_edge(node1.get_output_port("输出"), node2.get_input_port("输入"))

    assert edge._cp1_offset == (0.25, 0.0)
    assert edge._cp2_offset == (0.75, 0.0)
```

- [ ] **步骤 5：运行测试验证失败**

```bash
python -m pytest tests/test_edge_widget.py -v --tb=short
```

预期：新增 4 个测试 PASS

- [ ] **步骤 6：Commit**

```bash
git add tests/test_edge_widget.py
git commit -m "test: 新增控制点手柄创建、可见性、持久化测试（任务 3/4）"
```

---

### 任务 4：集成测试与验证

**文件：**
- 无新文件

- [ ] **步骤 1：运行完整测试套件**

```bash
python -m pytest tests/ -v --tb=short
```

预期：所有测试 PASS

- [ ] **步骤 2：检查 JSON 文件格式**

确认 `resources/测试.json` 中连线数据包含 `cp1`/`cp2` 字段。

- [ ] **步骤 3：手动验证清单**

- [ ] 选中连线，控制点手柄出现在连线上
- [ ] 拖动手柄到任意位置，曲线形状实时更新
- [ ] 取消选中连线，手柄隐藏
- [ ] 重新选中连线，手柄出现在上次调整的位置
- [ ] 拖动节点，手柄跟随移动，曲线形状保持
- [ ] 保存后 JSON 包含 cp1/cp2 偏移量
- [ ] 重新加载后曲线形状恢复

- [ ] **步骤 4：Commit**

```bash
git commit -m "chore: 集成测试与验证通过（任务 4/4）"
```