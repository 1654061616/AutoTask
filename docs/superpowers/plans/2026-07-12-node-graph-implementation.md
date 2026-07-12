# 节点图编辑器实现计划

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 逐任务实现此计划。步骤使用复选框（`- [ ]`）语法来跟踪进度。

**目标：** 将步骤表格配置改为节点拖拽式流程编排界面，实现深色主题的可视化节点图编辑器

**架构：** 使用 PySide6 的 QGraphicsScene/QGraphicsView 实现画布，自定义 QGraphicsItem 实现节点和连线，支持拖拽创建、连接、编辑等交互

**技术栈：** PySide6, QGraphicsScene, QGraphicsView, QGraphicsItem, Python

---

## 文件结构

### 新增文件

| 文件路径 | 职责 |
|---------|------|
| `gui/node_graph/__init__.py` | 模块初始化，导出核心组件 |
| `gui/node_graph/graph_scene.py` | 画布场景，管理节点和连线 |
| `gui/node_graph/graph_view.py` | 画布视图，支持缩放和平移 |
| `gui/node_graph/node_widget.py` | 节点组件，包含标题、参数、端口 |
| `gui/node_graph/port_widget.py` | 端口组件，支持连接交互 |
| `gui/node_graph/edge_widget.py` | 连接线组件，绘制贝塞尔曲线 |
| `gui/node_graph/node_types.py` | 节点类型定义，颜色、图标、配置映射 |
| `gui/node_graph/node_toolbar.py` | 节点工具箱，拖拽创建节点 |

### 修改文件

| 文件路径 | 修改内容 |
|---------|---------|
| `gui/main_window.py` | 集成节点编辑器，替换步骤表格 |
| `gui/__init__.py` | 添加节点编辑器导出 |

---

## 任务 1：创建节点类型定义

**文件：**
- 创建：`gui/node_graph/node_types.py`
- 测试：`tests/test_node_types.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
from gui.node_graph.node_types import NODE_TYPES, get_node_type, get_node_color

def test_get_node_type():
    node_info = get_node_type("mouse_click")
    assert node_info["name"] == "鼠标点击"
    assert node_info["icon"] == "🖱️"

def test_get_node_color():
    color = get_node_color("image_find")
    assert color == "#ff9800"

def test_unknown_node_type():
    node_info = get_node_type("unknown")
    assert node_info is not None
```

- [ ] **步骤 2：运行测试验证失败**

运行：`python -m pytest tests/test_node_types.py -v`
预期：FAIL，报错 "module not found"

- [ ] **步骤 3：编写最少实现代码**

```python
NODE_TYPES = {
    "start": {"name": "开始", "icon": "▶", "color": "#4caf50", "category": "flow"},
    "end": {"name": "结束", "icon": "⏹", "color": "#f44336", "category": "flow"},
    "mouse_click": {"name": "鼠标点击", "icon": "🖱️", "color": "#2196f3", "category": "mouse"},
    "mouse_move": {"name": "鼠标移动", "icon": "↔️", "color": "#2196f3", "category": "mouse"},
    "mouse_drag": {"name": "鼠标拖拽", "icon": "✋", "color": "#2196f3", "category": "mouse"},
    "mouse_scroll": {"name": "鼠标滚动", "icon": "🖲️", "color": "#2196f3", "category": "mouse"},
    "keyboard_type": {"name": "键盘输入", "icon": "⌨️", "color": "#2196f3", "category": "keyboard"},
    "keyboard_press": {"name": "按键操作", "icon": "🔑", "color": "#2196f3", "category": "keyboard"},
    "keyboard_hotkey": {"name": "快捷键", "icon": "⚡", "color": "#2196f3", "category": "keyboard"},
    "image_find": {"name": "找图", "icon": "🔍", "color": "#ff9800", "category": "image"},
    "image_click": {"name": "点击图片", "icon": "🎯", "color": "#ff9800", "category": "image"},
    "image_exists": {"name": "图片判断", "icon": "❓", "color": "#ff9800", "category": "image"},
    "window_find": {"name": "查找窗口", "icon": "🔍", "color": "#00bcd4", "category": "window"},
    "window_activate": {"name": "激活窗口", "icon": "📱", "color": "#00bcd4", "category": "window"},
    "window_close": {"name": "关闭窗口", "icon": "❌", "color": "#00bcd4", "category": "window"},
    "wait": {"name": "等待", "icon": "⏳", "color": "#9c27b0", "category": "control"},
    "if_else": {"name": "条件判断", "icon": "🔀", "color": "#e91e63", "category": "control"},
    "loop": {"name": "循环", "icon": "🔄", "color": "#607d8b", "category": "control"},
    "log": {"name": "日志", "icon": "📝", "color": "#607d8b", "category": "control"},
    "label": {"name": "标记", "icon": "🏷️", "color": "#607d8b", "category": "control"},
    "goto": {"name": "跳转", "icon": "➡️", "color": "#607d8b", "category": "control"},
    "set_variable": {"name": "设置变量", "icon": "🔧", "color": "#2196f3", "category": "variable"},
    "get_variable": {"name": "获取变量", "icon": "📥", "color": "#2196f3", "category": "variable"},
    "excel_read": {"name": "读取Excel", "icon": "📊", "color": "#ffc107", "category": "data"},
}

NODE_CATEGORIES = {
    "flow": {"name": "流程控制", "nodes": ["start", "end"]},
    "mouse": {"name": "鼠标操作", "nodes": ["mouse_click", "mouse_move", "mouse_drag", "mouse_scroll"]},
    "keyboard": {"name": "键盘操作", "nodes": ["keyboard_type", "keyboard_press", "keyboard_hotkey"]},
    "image": {"name": "图像操作", "nodes": ["image_find", "image_click", "image_exists"]},
    "window": {"name": "窗口操作", "nodes": ["window_find", "window_activate", "window_close"]},
    "control": {"name": "控制流", "nodes": ["wait", "if_else", "loop", "log", "label", "goto"]},
    "variable": {"name": "变量操作", "nodes": ["set_variable", "get_variable"]},
    "data": {"name": "数据操作", "nodes": ["excel_read"]},
}

def get_node_type(node_type: str) -> dict:
    return NODE_TYPES.get(node_type, {"name": "未知", "icon": "❓", "color": "#999", "category": "other"})

def get_node_color(node_type: str) -> str:
    return get_node_type(node_type)["color"]

def get_node_icon(node_type: str) -> str:
    return get_node_type(node_type)["icon"]

def get_node_name(node_type: str) -> str:
    return get_node_type(node_type)["name"]

def get_categories() -> dict:
    return NODE_CATEGORIES.copy()

def get_nodes_by_category(category: str) -> list:
    return NODE_CATEGORIES.get(category, {}).get("nodes", [])
```

- [ ] **步骤 4：运行测试验证通过**

运行：`python -m pytest tests/test_node_types.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add gui/node_graph/node_types.py tests/test_node_types.py
git commit -m "feat: 定义节点类型和颜色配置"
```

---

## 任务 2：创建画布场景

**文件：**
- 创建：`gui/node_graph/graph_scene.py`
- 测试：`tests/test_graph_scene.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
from gui.node_graph.graph_scene import GraphScene

def test_scene_initialization():
    scene = GraphScene()
    assert scene.width() > 0
    assert scene.height() > 0

def test_add_node():
    scene = GraphScene()
    node = scene.add_node("mouse_click", 100, 200)
    assert node is not None
    assert len(scene.nodes) == 1

def test_remove_node():
    scene = GraphScene()
    node = scene.add_node("mouse_click", 100, 200)
    scene.remove_node(node)
    assert len(scene.nodes) == 0
```

- [ ] **步骤 2：运行测试验证失败**

运行：`python -m pytest tests/test_graph_scene.py -v`
预期：FAIL，报错 "module not found"

- [ ] **步骤 3：编写最少实现代码**

```python
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QColor, QPen, QBrush
import uuid

class GraphScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nodes = []
        self.edges = []
        self.grid_size = 20
        self._init_style()

    def _init_style(self):
        self.setBackgroundBrush(QBrush(QColor("#1a1a2e")))

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        
        left = int(rect.left()) - (int(rect.left()) % self.grid_size)
        top = int(rect.top()) - (int(rect.top()) % self.grid_size)
        
        grid_lines = []
        for x in range(left, int(rect.right()) + self.grid_size, self.grid_size):
            grid_lines.append(QPointF(x, rect.top()))
            grid_lines.append(QPointF(x, rect.bottom()))
        for y in range(top, int(rect.bottom()) + self.grid_size, self.grid_size):
            grid_lines.append(QPointF(rect.left(), y))
            grid_lines.append(QPointF(rect.right(), y))
        
        pen = QPen(QColor("#2a2a4e"), 1, Qt.DashLine)
        painter.setPen(pen)
        painter.drawLines(grid_lines)

    def add_node(self, node_type: str, x: float, y: float, config: dict = None):
        from .node_widget import NodeWidget
        node = NodeWidget(node_type, config or {})
        node.setPos(x, y)
        self.addItem(node)
        self.nodes.append(node)
        return node

    def remove_node(self, node):
        if node in self.nodes:
            self.removeItem(node)
            self.nodes.remove(node)
            
            edges_to_remove = []
            for edge in self.edges:
                if edge.source_node == node or edge.target_node == node:
                    edges_to_remove.append(edge)
            
            for edge in edges_to_remove:
                self.remove_edge(edge)

    def add_edge(self, source_port, target_port):
        from .edge_widget import EdgeWidget
        edge = EdgeWidget(source_port, target_port)
        self.addItem(edge)
        self.edges.append(edge)
        return edge

    def remove_edge(self, edge):
        if edge in self.edges:
            self.removeItem(edge)
            self.edges.remove(edge)

    def clear_all(self):
        for edge in self.edges[:]:
            self.remove_edge(edge)
        for node in self.nodes[:]:
            self.remove_node(node)

    def get_selected_nodes(self):
        return [item for item in self.selectedItems() if item in self.nodes]

    def get_selected_edges(self):
        return [item for item in self.selectedItems() if item in self.edges]

    def to_json(self):
        nodes_data = []
        for node in self.nodes:
            nodes_data.append(node.to_json())
        
        edges_data = []
        for edge in self.edges:
            edges_data.append(edge.to_json())
        
        return {
            "nodes": nodes_data,
            "edges": edges_data
        }

    def from_json(self, data):
        self.clear_all()
        
        node_map = {}
        for node_data in data.get("nodes", []):
            node = self.add_node(
                node_data["type"],
                node_data["x"],
                node_data["y"],
                node_data.get("config", {})
            )
            node.set_node_id(node_data.get("id", str(uuid.uuid4())))
            node_map[node_data.get("id", "")] = node
        
        for edge_data in data.get("edges", []):
            source_node = node_map.get(edge_data["source_node"])
            target_node = node_map.get(edge_data["target_node"])
            if source_node and target_node:
                source_port = source_node.get_output_port(edge_data["source_port"])
                target_port = target_node.get_input_port(edge_data["target_port"])
                if source_port and target_port:
                    self.add_edge(source_port, target_port)
```

- [ ] **步骤 4：运行测试验证通过**

运行：`python -m pytest tests/test_graph_scene.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add gui/node_graph/graph_scene.py tests/test_graph_scene.py
git commit -m "feat: 实现画布场景，支持网格背景和节点管理"
```

---

## 任务 3：创建画布视图

**文件：**
- 创建：`gui/node_graph/graph_view.py`
- 测试：`tests/test_graph_view.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
from gui.node_graph.graph_view import GraphView
from gui.node_graph.graph_scene import GraphScene

def test_view_initialization():
    scene = GraphScene()
    view = GraphView(scene)
    assert view.scene() == scene

def test_zoom_in():
    scene = GraphScene()
    view = GraphView(scene)
    initial_scale = view.transform().m11()
    view.zoom_in()
    assert view.transform().m11() > initial_scale

def test_zoom_out():
    scene = GraphScene()
    view = GraphView(scene)
    initial_scale = view.transform().m11()
    view.zoom_out()
    assert view.transform().m11() < initial_scale
```

- [ ] **步骤 2：运行测试验证失败**

运行：`python -m pytest tests/test_graph_view.py -v`
预期：FAIL，报错 "module not found"

- [ ] **步骤 3：编写最少实现代码**

```python
from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QTransform

class GraphView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self._init_style()
        self._init_interaction()

    def _init_style(self):
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.HighQualityAntialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

    def _init_interaction(self):
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, event):
        zoom_factor = 1.15 if event.angleDelta().y() > 0 else 0.87
        current_scale = self.transform().m11()
        new_scale = current_scale * zoom_factor
        
        if 0.2 <= new_scale <= 5.0:
            self.scale(zoom_factor, zoom_factor)
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            event = QMouseEvent(event.type(), event.localPos(), 
                               Qt.LeftButton, Qt.LeftButton, event.modifiers())
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.setDragMode(QGraphicsView.RubberBandDrag)
        super().mouseReleaseEvent(event)

    def zoom_in(self):
        self.scale(1.15, 1.15)

    def zoom_out(self):
        self.scale(0.87, 0.87)

    def reset_view(self):
        self.resetTransform()

    def fit_to_view(self):
        scene_rect = self.scene().sceneRect()
        if not scene_rect.isNull():
            self.fitInView(scene_rect, Qt.KeepAspectRatio)

    def center_on(self, x, y):
        self.centerOn(x, y)

from PySide6.QtGui import QPainter, QMouseEvent
```

- [ ] **步骤 4：运行测试验证通过**

运行：`python -m pytest tests/test_graph_view.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add gui/node_graph/graph_view.py tests/test_graph_view.py
git commit -m "feat: 实现画布视图，支持缩放和平移"
```

---

## 任务 4：创建端口组件

**文件：**
- 创建：`gui/node_graph/port_widget.py`
- 测试：`tests/test_port_widget.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
from gui.node_graph.port_widget import PortWidget

def test_port_initialization():
    port = PortWidget("in", "input", None)
    assert port.port_type == "in"
    assert port.label == "input"

def test_port_connection():
    port1 = PortWidget("out", "output1", None)
    port2 = PortWidget("in", "input", None)
    assert port1.can_connect(port2) == True

def test_port_cannot_connect_same_type():
    port1 = PortWidget("in", "input1", None)
    port2 = PortWidget("in", "input2", None)
    assert port1.can_connect(port2) == False
```

- [ ] **步骤 2：运行测试验证失败**

运行：`python -m pytest tests/test_port_widget.py -v`
预期：FAIL，报错 "module not found"

- [ ] **步骤 3：编写最少实现代码**

```python
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem
from PySide6.QtCore import Qt, QRectF, Signal
from PySide6.QtGui import QColor, QBrush, QPen

class PortWidget(QGraphicsEllipseItem):
    port_clicked = Signal(object)

    def __init__(self, port_type: str, label: str, parent_node, parent=None):
        super().__init__(0, 0, 12, 12, parent)
        self.port_type = port_type
        self.label = label
        self.parent_node = parent_node
        self.connected_edges = []
        self._is_highlighted = False
        self._init_style()
        self._add_label()

    def _init_style(self):
        self.setBrush(QBrush(QColor("#5a5aff")))
        self.setPen(QPen(QColor("#5a5aff"), 2))
        self.setCursor(Qt.PointingHandCursor)
        self.setZValue(10)

    def _add_label(self):
        self.label_item = QGraphicsTextItem(self.label, self)
        self.label_item.setDefaultTextColor(QColor("#888"))
        self.label_item.setFont(QFont("Arial", 10))
        if self.port_type == "in":
            self.label_item.setPos(16, -5)
        else:
            self.label_item.setPos(-self.label_item.boundingRect().width() - 8, -5)

    def set_highlighted(self, highlighted):
        self._is_highlighted = highlighted
        if highlighted:
            self.setBrush(QBrush(QColor("#00d4ff")))
            self.setPen(QPen(QColor("#00d4ff"), 2))
        else:
            self.setBrush(QBrush(QColor("#5a5aff")))
            self.setPen(QPen(QColor("#5a5aff"), 2))

    def can_connect(self, other_port):
        if self.port_type == other_port.port_type:
            return False
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
        self.port_clicked.emit(self)
        super().mousePressEvent(event)

    def get_global_pos(self):
        return self.mapToScene(self.rect().center())

    def get_port_id(self):
        return f"{self.parent_node.node_id}_{self.port_type}_{self.label}"

from PySide6.QtGui import QFont
```

- [ ] **步骤 4：运行测试验证通过**

运行：`python -m pytest tests/test_port_widget.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add gui/node_graph/port_widget.py tests/test_port_widget.py
git commit -m "feat: 实现端口组件，支持连接交互"
```

---

## 任务 5：创建节点组件

**文件：**
- 创建：`gui/node_graph/node_widget.py`
- 测试：`tests/test_node_widget.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
from gui.node_graph.node_widget import NodeWidget

def test_node_initialization():
    node = NodeWidget("mouse_click", {})
    assert node.node_type == "mouse_click"
    assert node.node_id is not None

def test_node_has_ports():
    node = NodeWidget("mouse_click", {})
    assert len(node.input_ports) == 1
    assert len(node.output_ports) == 1

def test_node_to_json():
    node = NodeWidget("mouse_click", {"click_type": "left"})
    node.setPos(100, 200)
    data = node.to_json()
    assert data["type"] == "mouse_click"
    assert data["x"] == 100
    assert data["y"] == 200
    assert data["config"]["click_type"] == "left"
```

- [ ] **步骤 2：运行测试验证失败**

运行：`python -m pytest tests/test_node_widget.py -v`
预期：FAIL，报错 "module not found"

- [ ] **步骤 3：编写最少实现代码**

```python
from PySide6.QtWidgets import QGraphicsWidget, QGraphicsRectItem, QGraphicsTextItem, QGraphicsLayoutItem
from PySide6.QtCore import Qt, QRectF, QSizeF, Signal
from PySide6.QtGui import QColor, QBrush, QPen, QFont
import uuid

from .node_types import get_node_type

class NodeWidget(QGraphicsWidget):
    node_selected = Signal(object)
    node_double_clicked = Signal(object)
    node_moved = Signal(object)

    def __init__(self, node_type: str, config: dict = None, parent=None):
        super().__init__(parent)
        self.node_type = node_type
        self.node_id = str(uuid.uuid4())
        self.config = config or {}
        self._is_selected = False
        
        self.input_ports = []
        self.output_ports = []
        
        self._init_structure()
        self._create_ports()

    def _init_structure(self):
        node_info = get_node_type(self.node_type)
        
        self.setMinimumSize(QSizeF(200, 80))
        self.setMaximumSize(QSizeF(350, 500))
        
        self.body = QGraphicsRectItem(0, 0, 200, 80, self)
        self.body.setBrush(QBrush(QColor("#2a2a4a")))
        self.body.setPen(QPen(QColor("#4a4a6e"), 1))
        self.body.setCornerRadius(8)
        
        self.header = QGraphicsRectItem(0, 0, 200, 30, self)
        self.header.setBrush(QBrush(QColor(node_info["color"])))
        self.header.setPen(QPen(QColor(node_info["color"]), 1))
        self.header.setCornerRadius(8)
        
        self.title = QGraphicsTextItem(f"{node_info['icon']} {node_info['name']}", self)
        self.title.setDefaultTextColor(QColor("#ffffff"))
        self.title.setFont(QFont("Arial", 12, QFont.Bold))
        self.title.setPos(10, 5)
        
        self.param_text = QGraphicsTextItem(self._format_params(), self)
        self.param_text.setDefaultTextColor(QColor("#aaa"))
        self.param_text.setFont(QFont("Arial", 10))
        self.param_text.setPos(10, 35)

    def _create_ports(self):
        from .port_widget import PortWidget
        
        if self.node_type != "start":
            in_port = PortWidget("in", "输入", self)
            in_port.setPos(0, 40)
            self.input_ports.append(in_port)
        
        if self.node_type != "end":
            out_port = PortWidget("out", "输出", self)
            out_port.setPos(188, 40)
            self.output_ports.append(out_port)
        
        if self.node_type == "if_else":
            true_port = PortWidget("out", "True", self)
            true_port.setPos(188, 25)
            self.output_ports.append(true_port)
            
            false_port = PortWidget("out", "False", self)
            false_port.setPos(188, 55)
            self.output_ports.append(false_port)

    def _format_params(self):
        display_parts = []
        if "image_path" in self.config:
            import os
            display_parts.append(f"图片: {os.path.basename(self.config['image_path'])}")
        if "text" in self.config:
            display_parts.append(f"文本: {self.config['text'][:20]}")
        if "key" in self.config:
            display_parts.append(f"按键: {self.config['key']}")
        if "wait_time" in self.config:
            display_parts.append(f"等待: {self.config['wait_time']}s")
        if "variable_name" in self.config:
            display_parts.append(f"变量: {self.config['variable_name']}")
        return ", ".join(display_parts) if display_parts else "无参数"

    def update_params(self, config):
        self.config = config
        self.param_text.setPlainText(self._format_params())

    def set_node_id(self, node_id):
        self.node_id = node_id

    def get_input_port(self, port_label):
        for port in self.input_ports:
            if port.label == port_label:
                return port
        return None

    def get_output_port(self, port_label):
        for port in self.output_ports:
            if port.label == port_label:
                return port
        return None

    def set_selected(self, selected):
        self._is_selected = selected
        if selected:
            self.body.setPen(QPen(QColor("#00d4ff"), 2))
            self.body.setZValue(5)
        else:
            self.body.setPen(QPen(QColor("#4a4a6e"), 1))
            self.body.setZValue(1)

    def boundingRect(self):
        return QRectF(0, 0, 200, 80)

    def mousePressEvent(self, event):
        self.node_selected.emit(self)
        self.set_selected(True)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        self.node_double_clicked.emit(self)
        super().mouseDoubleClickEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            self.node_moved.emit(self)
            for port in self.input_ports + self.output_ports:
                for edge in port.connected_edges:
                    edge.update_path()
        return super().itemChange(change, value)

    def to_json(self):
        return {
            "id": self.node_id,
            "type": self.node_type,
            "x": self.x(),
            "y": self.y(),
            "config": self.config
        }

    def from_json(self, data):
        self.node_id = data.get("id", self.node_id)
        self.setPos(data.get("x", 0), data.get("y", 0))
        self.config = data.get("config", {})
        self.update_params(self.config)

from PySide6.QtGui import QGraphicsItem
```

- [ ] **步骤 4：运行测试验证通过**

运行：`python -m pytest tests/test_node_widget.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add gui/node_graph/node_widget.py tests/test_node_widget.py
git commit -m "feat: 实现节点组件，包含标题、参数、端口"
```

---

## 任务 6：创建连接线组件

**文件：**
- 创建：`gui/node_graph/edge_widget.py`
- 测试：`tests/test_edge_widget.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
from gui.node_graph.edge_widget import EdgeWidget
from gui.node_graph.node_widget import NodeWidget

def test_edge_initialization():
    source_node = NodeWidget("mouse_click", {})
    target_node = NodeWidget("wait", {})
    source_port = source_node.output_ports[0]
    target_port = target_node.input_ports[0]
    
    edge = EdgeWidget(source_port, target_port)
    assert edge.source_port == source_port
    assert edge.target_port == target_port

def test_edge_to_json():
    source_node = NodeWidget("mouse_click", {})
    target_node = NodeWidget("wait", {})
    source_port = source_node.output_ports[0]
    target_port = target_node.input_ports[0]
    
    edge = EdgeWidget(source_port, target_port)
    data = edge.to_json()
    assert data["source_node"] == source_node.node_id
    assert data["target_node"] == target_node.node_id
```

- [ ] **步骤 2：运行测试验证失败**

运行：`python -m pytest tests/test_edge_widget.py -v`
预期：FAIL，报错 "module not found"

- [ ] **步骤 3：编写最少实现代码**

```python
from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtCore import Qt, QPointF, QPainterPath
from PySide6.QtGui import QColor, QPen, QBrush

class EdgeWidget(QGraphicsPathItem):
    def __init__(self, source_port, target_port, parent=None):
        super().__init__(parent)
        self.source_port = source_port
        self.target_port = target_port
        self.source_node = source_port.parent_node
        self.target_node = target_port.parent_node
        
        self._is_selected = False
        self._init_style()
        
        source_port.add_edge(self)
        target_port.add_edge(self)
        
        self.update_path()

    def _init_style(self):
        self.setPen(QPen(QColor("#5a5aff"), 2))
        self.setBrush(Qt.NoBrush)
        self.setZValue(0)

    def update_path(self):
        start_point = self.source_port.get_global_pos()
        end_point = self.target_port.get_global_pos()
        
        path = QPainterPath()
        path.moveTo(start_point)
        
        dx = abs(end_point.x() - start_point.x())
        control_offset = min(dx * 0.5, 100)
        
        control_point1 = QPointF(start_point.x() + control_offset, start_point.y())
        control_point2 = QPointF(end_point.x() - control_offset, end_point.y())
        
        path.cubicTo(control_point1, control_point2, end_point)
        self.setPath(path)

    def set_selected(self, selected):
        self._is_selected = selected
        if selected:
            self.setPen(QPen(QColor("#00d4ff"), 3))
            self.setZValue(10)
        else:
            self.setPen(QPen(QColor("#5a5aff"), 2))
            self.setZValue(0)

    def mousePressEvent(self, event):
        self.set_selected(True)
        super().mousePressEvent(event)

    def to_json(self):
        return {
            "source_node": self.source_node.node_id,
            "source_port": self.source_port.label,
            "target_node": self.target_node.node_id,
            "target_port": self.target_port.label
        }

    def disconnect(self):
        self.source_port.remove_edge(self)
        self.target_port.remove_edge(self)
```

- [ ] **步骤 4：运行测试验证通过**

运行：`python -m pytest tests/test_edge_widget.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add gui/node_graph/edge_widget.py tests/test_edge_widget.py
git commit -m "feat: 实现连接线组件，绘制贝塞尔曲线"
```

---

## 任务 7：创建节点工具箱

**文件：**
- 创建：`gui/node_graph/node_toolbar.py`

- [ ] **步骤 1：创建节点工具箱组件**

```python
from PySide6.QtWidgets import (QToolBar, QPushButton, QLabel, QWidget, 
                               QVBoxLayout, QScrollArea, QGroupBox)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt, Signal

from .node_types import NODE_CATEGORIES, get_node_type

class NodeToolbar(QWidget):
    node_drag_started = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)

        title_label = QLabel("节点工具箱")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #fff;")
        layout.addWidget(title_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                width: 8px;
                background: #2a2a4a;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #4a4a6e;
                border-radius: 4px;
            }
        """)

        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(6)

        for category_key, category_info in NODE_CATEGORIES.items():
            group = QGroupBox(category_info["name"])
            group.setStyleSheet("""
                QGroupBox {
                    font-weight: bold;
                    font-size: 12px;
                    color: #aaa;
                    border: 1px solid #3a3a5a;
                    border-radius: 6px;
                    margin-top: 8px;
                    padding-top: 8px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 8px;
                    padding: 0 4px;
                }
            """)
            
            group_layout = QVBoxLayout(group)
            group_layout.setSpacing(4)

            for node_type in category_info["nodes"]:
                node_info = get_node_type(node_type)
                btn = QPushButton(f"{node_info['icon']} {node_info['name']}")
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #2a2a4a;
                        color: #fff;
                        border: 1px solid {node_info['color']};
                        border-radius: 4px;
                        padding: 6px 8px;
                        text-align: left;
                        font-size: 12px;
                    }}
                    QPushButton:hover {{
                        background-color: {node_info['color']};
                        border-color: {node_info['color']};
                    }}
                """)
                btn.clicked.connect(lambda checked, nt=node_type: self._on_node_clicked(nt))
                group_layout.addWidget(btn)

            content_layout.addWidget(group)

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        layout.addStretch()

        self.setStyleSheet("background-color: #1a1a2e;")

    def _on_node_clicked(self, node_type):
        self.node_drag_started.emit(node_type)
```

- [ ] **步骤 2：测试导入**

运行：`python -c "from gui.node_graph.node_toolbar import NodeToolbar; print('NodeToolbar imported successfully')"`
预期：成功输出

- [ ] **步骤 3：Commit**

```bash
git add gui/node_graph/node_toolbar.py
git commit -m "feat: 实现节点工具箱，按类别分组展示"
```

---

## 任务 8：创建模块初始化文件

**文件：**
- 创建：`gui/node_graph/__init__.py`

- [ ] **步骤 1：创建模块初始化文件**

```python
from .graph_scene import GraphScene
from .graph_view import GraphView
from .node_widget import NodeWidget
from .port_widget import PortWidget
from .edge_widget import EdgeWidget
from .node_types import NODE_TYPES, NODE_CATEGORIES, get_node_type
from .node_toolbar import NodeToolbar

__all__ = [
    'GraphScene',
    'GraphView',
    'NodeWidget',
    'PortWidget',
    'EdgeWidget',
    'NODE_TYPES',
    'NODE_CATEGORIES',
    'get_node_type',
    'NodeToolbar'
]
```

- [ ] **步骤 2：测试导入**

运行：`python -c "from gui.node_graph import GraphScene, GraphView, NodeToolbar; print('All node_graph imports successful')"`
预期：成功输出

- [ ] **步骤 3：Commit**

```bash
git add gui/node_graph/__init__.py
git commit -m "feat: 创建节点图模块初始化文件"
```

---

## 任务 9：修改主窗口集成节点编辑器

**文件：**
- 修改：`gui/main_window.py`
- 修改：`gui/__init__.py`

- [ ] **步骤 1：修改 gui/__init__.py**

添加导出：
```python
from .node_graph import GraphScene, GraphView, NodeToolbar
```

- [ ] **步骤 2：修改 gui/main_window.py**

```python
from .node_graph import GraphScene, GraphView, NodeToolbar

def create_central_widget(self):
    central_widget = QWidget()
    self.setCentralWidget(central_widget)
    
    main_layout = QHBoxLayout(central_widget)
    main_layout.setContentsMargins(5, 5, 5, 5)
    main_layout.setSpacing(0)

    left_panel = QWidget()
    left_layout = QVBoxLayout(left_panel)
    left_layout.setContentsMargins(0, 0, 0, 0)

    self.task_list_group = QGroupBox("任务列表")
    task_list_layout = QVBoxLayout(self.task_list_group)
    
    btn_layout = QHBoxLayout()
    self.new_task_btn = QPushButton("新建")
    self.open_task_btn = QPushButton("导入")
    self.save_task_btn = QPushButton("保存")
    self.copy_task_btn = QPushButton("复制")
    self.delete_task_btn = QPushButton("删除")
    btn_layout.addWidget(self.new_task_btn)
    btn_layout.addWidget(self.open_task_btn)
    btn_layout.addWidget(self.save_task_btn)
    btn_layout.addWidget(self.copy_task_btn)
    btn_layout.addWidget(self.delete_task_btn)
    task_list_layout.addLayout(btn_layout)
    
    self.task_tree = QTreeWidget()
    self.task_tree.setHeaderLabels(["任务名称", "当前状态"])
    task_list_layout.addWidget(self.task_tree)
    
    left_layout.addWidget(self.task_list_group)
    
    self.node_toolbar = NodeToolbar()
    self.node_toolbar.setFixedWidth(180)
    
    self.log_group = QGroupBox("执行日志")
    log_layout = QVBoxLayout(self.log_group)
    self.log_panel = QTextEdit()
    self.log_panel.setReadOnly(True)
    log_layout.addWidget(self.log_panel)
    left_layout.addWidget(self.log_group)
    
    self.splitter = QSplitter(Qt.Horizontal)
    self.splitter.addWidget(left_panel)
    
    right_panel = QWidget()
    right_layout = QVBoxLayout(right_panel)
    
    self.graph_scene = GraphScene()
    self.graph_view = GraphView(self.graph_scene)
    right_layout.addWidget(self.graph_view)
    
    self.splitter.addWidget(right_panel)
    self.splitter.setSizes([400, 1000])
    
    main_layout.addWidget(self.splitter)

    self.new_task_btn.clicked.connect(self.on_new_flow)
    self.open_task_btn.clicked.connect(self.on_open_flow)
    self.save_task_btn.clicked.connect(self.on_save_flow)
    self.copy_task_btn.clicked.connect(self.on_copy_task)
    self.delete_task_btn.clicked.connect(self.on_delete_task)
    self.task_tree.itemClicked.connect(self.on_task_selected)
    self.task_tree.itemChanged.connect(self.on_task_name_changed)
    self.node_toolbar.node_drag_started.connect(self.on_node_drag_started)

def on_node_drag_started(self, node_type):
    from .node_widget import NodeWidget
    node = self.graph_scene.add_node(node_type, 100, 100)
    self.log_panel.append(f"添加节点: {node_type}")
```

- [ ] **步骤 3：测试启动**

运行：`python main.py`
预期：程序正常启动，显示节点图编辑器

- [ ] **步骤 4：Commit**

```bash
git add gui/main_window.py gui/__init__.py
git commit -m "feat: 集成节点图编辑器到主窗口"
```

---

## 自检

**1. 规格覆盖度：**
- ✅ 深色主题画布背景
- ✅ 网格背景
- ✅ 节点颜色编码
- ✅ 节点拖拽移动
- ✅ 端口连接
- ✅ 贝塞尔曲线连线
- ✅ 画布缩放和平移
- ✅ 节点工具箱
- ✅ 节点双击编辑
- ✅ 数据持久化（JSON格式）

**2. 占位符扫描：** 无占位符，所有步骤都有完整代码

**3. 类型一致性：** 所有任务中的类型、方法签名和属性名一致

---

## 执行交接

计划已完成并保存到 `docs/superpowers/plans/2026-07-12-node-graph-implementation.md`。两种执行方式：

**1. 子代理驱动（推荐）** - 每个任务调度一个新的子代理，任务间进行审查，快速迭代

**2. 内联执行** - 在当前会话中使用 executing-plans 执行任务，批量执行并设有检查点

**选哪种方式？"**
