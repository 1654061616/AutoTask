"""
流程执行引擎 — 负责解析、调度和执行自动化流程任务
"""
from typing import Dict, Any, Optional, List, Callable
import threading
import time
from .parser import FlowParser
from .variables import VariableManager
from .logger import Logger


class FlowEngine:
    """流程执行引擎，负责加载流程定义并按节点图顺序执行各步骤"""

    def __init__(self):
        self.flow: Optional[Dict[str, Any]] = None          # 当前加载的流程定义
        self.variable_manager = VariableManager()            # 变量管理器
        self.logger = Logger()                               # 日志记录器
        self.is_running = False                              # 是否正在执行
        self.current_step = None                             # 当前执行的步骤
        self.thread: Optional[threading.Thread] = None       # 执行线程
        self.parser = FlowParser()                           # 流程解析器
        self.step_executor = None                            # 步骤执行器
        self._init_operations()                              # 初始化操作模块
        self.completed_callbacks: List[Callable[[bool, str], None]] = []  # 完成回调列表
        self._excel_cursors: Dict[str, int] = {}             # Excel 读取游标

    def add_completed_callback(self, callback: Callable[[bool, str], None]):
        """添加流程完成回调函数"""
        if callback not in self.completed_callbacks:
            self.completed_callbacks.append(callback)

    def remove_completed_callback(self, callback: Callable[[bool, str], None]):
        """移除流程完成回调函数"""
        if callback in self.completed_callbacks:
            self.completed_callbacks.remove(callback)

    def _init_operations(self):
        """初始化操作模块，创建 StepExecutor 实例"""
        try:
            from core.step_executor import create_step_executor
            self.step_executor = create_step_executor(self.variable_manager, self.logger)
        except ImportError as e:
            self.logger.error(f"加载操作模块失败: {str(e)}")
            self.step_executor = None

    def load_flow(self, flow: Dict[str, Any]):
        """加载流程字典"""
        self.flow = self.parser.parse(flow)

    def load_flow_from_file(self, file_path: str):
        """从 JSON 文件加载流程"""
        self.flow = self.parser.load_from_file(file_path)

    def set_excel_data(self, excel_path: str):
        """加载 Excel 数据文件"""
        self.variable_manager.load_excel(excel_path)

    def run(self):
        """在新线程中启动流程执行"""
        if not self.flow or self.is_running:
            return
        self.is_running = True
        self.thread = threading.Thread(target=self._execute_flow)
        self.thread.start()

    def _execute_flow(self):
        """执行流程的核心方法，按节点图顺序遍历执行"""
        success = True
        error_message = ""
        try:
            self.logger.info("开始执行流程: {}".format(self.flow.get("name", "Unknown")))
            nodes = self.flow.get("nodes", [])
            edges = self.flow.get("edges", [])
            node_map = {n["id"]: n for n in nodes}

            current_node_id = self._follow_edge_from_start(edges, node_map)
            if not current_node_id:
                self.logger.warning("流程中没有可执行的节点")
                return

            while current_node_id and self.is_running:
                node = node_map.get(current_node_id)
                if not node or node.get("type") == "end":
                    break

                self.current_step = node
                self.logger.info(f"执行节点: {node.get('type', node.get('id'))}")

                step_result = None
                try:
                    step_result = self._execute_step(node)
                except Exception as e:
                    self.logger.error(f"节点执行失败: {str(e)}")
                    success = False
                    error_message = str(e)
                    break

                if self.step_executor and self.step_executor.flow_control.goto_target is not None:
                    current_node_id = self.step_executor.flow_control.goto_target
                    self.step_executor.flow_control.clear_goto()
                    continue

                if step_result is True:
                    step_result = "True"
                elif step_result is False:
                    step_result = "False"
                current_node_id = self._follow_edge(current_node_id, step_result, edges, node_map)

            self.logger.info("流程执行完成")
        except Exception as e:
            self.logger.error(f"流程执行异常: {str(e)}")
            success = False
            error_message = str(e)
        finally:
            self.is_running = False
            self.current_step = None
            for callback in self.completed_callbacks:
                try:
                    callback(success, error_message)
                except Exception:
                    pass

    def _follow_edge_from_start(self, edges, node_map):
        """从 start 节点出发，找到第一条边指向的下一个节点 ID"""
        start_node = next((n for n in node_map.values() if n["type"] == "start"), None)
        if not start_node:
            return None
        return self._follow_edge(start_node["id"], None, edges, node_map)

    def _follow_edge(self, source_id, source_port, edges, node_map):
        """根据源节点和端口，查找下一条边指向的目标节点 ID"""
        for edge in edges:
            if edge["source_node"] != source_id:
                continue
            if source_port is None:
                if edge["source_port"] not in ("True", "False"):
                    target_id = edge["target_node"]
                    target = node_map.get(target_id, {})
                    return target_id if target.get("type") != "end" else None
            else:
                if edge["source_port"] == source_port:
                    target_id = edge["target_node"]
                    target = node_map.get(target_id, {})
                    return target_id if target.get("type") != "end" else None
        return None

    def _execute_step(self, step: Dict[str, Any]):
        """执行单个步骤，处理 wait_before 和 wait_after"""
        if not self.step_executor:
            self.logger.error("步骤执行器未加载")
            return None

        wait_before = step.get("wait_before")
        if wait_before:
            self._execute_wait(wait_before)

        step_result = self.step_executor.execute(
            step,
            is_running_func=lambda: self.is_running,
            excel_cursors=self._excel_cursors,
            flow_nodes=self.flow.get("nodes", []),
        )

        wait_after = step.get("wait_after")
        if wait_after:
            self._execute_wait(wait_after)

        return step_result

    def _execute_wait(self, wait_config):
        """执行等待操作，支持固定时长和随机时长"""
        import random
        if isinstance(wait_config, dict):
            wait_type = wait_config.get("type", "fixed")
            if wait_type == "random":
                min_wait = wait_config.get("min", 1)
                max_wait = wait_config.get("max", 3)
                wait_time = random.uniform(min_wait, max_wait)
            else:
                wait_time = wait_config.get("value", 1)
        else:
            wait_time = wait_config
        time.sleep(wait_time)

    def stop(self):
        """停止流程执行并等待线程结束"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)

    def get_status(self) -> Dict[str, Any]:
        """获取当前引擎运行状态"""
        return {
            "is_running": self.is_running,
            "current_step": self.current_step,
            "flow_name": self.flow.get("name") if self.flow else None
        }