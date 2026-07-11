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
        self.setSceneRect(0, 0, 2000, 2000)

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