"""节点图处理 Mixin：编辑步骤、加载节点图"""

import uuid

from PySide6.QtWidgets import QMessageBox, QDialog
from PySide6.QtCore import Qt, Slot

from ..widgets.node_editor_dialog import NodeEditorDialog


class NodeHandlerMixin:
    """节点图处理 Mixin：编辑执行步骤、加载节点到场景"""

    @Slot()
    def on_edit_steps(self):
        if not self.current_flow:
            QMessageBox.warning(self, "编辑失败", "请先选择一个任务")
            return

        dialog = NodeEditorDialog(self.current_flow, parent=self)

        try:
            if dialog.exec() == QDialog.Accepted:
                graph_data = dialog.get_graph_data()
                self.current_flow["nodes"] = graph_data.get("nodes", [])
                self.current_flow["edges"] = graph_data.get("edges", [])

                current_item = self.task_tree.currentItem()
                if current_item:
                    current_item.setData(0, Qt.UserRole, self.current_flow)

                self.load_nodes_from_flow(self.current_flow)
                self.log_panel.append(f"已更新执行步骤: {self.current_flow['name']}")
        finally:
            try:
                dialog.cleanup()
            except Exception:
                pass

    def load_nodes_from_flow(self, flow_data):
        try:
            self.graph_scene.clear_all()

            nodes = flow_data.get("nodes", [])
            edges = flow_data.get("edges", [])

            node_map = {}

            for node_data in nodes:
                try:
                    node = self.graph_scene.add_node(
                        node_data.get("type", "wait"),
                        node_data.get("x", 0),
                        node_data.get("y", 0),
                        node_data.get("config", {})
                    )
                    node.set_node_id(node_data.get("id", str(uuid.uuid4())))
                    node.restore_ports_from_data(node_data)
                    node_map[node_data.get("id", "")] = node
                except Exception as e:
                    print(f"加载节点失败: {e}")

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
        except Exception as e:
            print(f"加载节点图失败: {e}")