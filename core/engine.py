from typing import Dict, Any, Optional
import threading
import time
from .parser import FlowParser
from .variables import VariableManager
from .logger import Logger

class FlowEngine:
    def __init__(self):
        self.flow: Optional[Dict[str, Any]] = None
        self.variable_manager = VariableManager()
        self.logger = Logger()
        self.is_running = False
        self.current_step = None
        self.thread: Optional[threading.Thread] = None
        self.parser = FlowParser()
    
    def load_flow(self, flow: Dict[str, Any]):
        self.flow = self.parser.parse(flow)
    
    def load_flow_from_file(self, file_path: str):
        self.flow = self.parser.load_from_file(file_path)
    
    def set_excel_data(self, excel_path: str):
        self.variable_manager.load_excel(excel_path)
    
    def run(self):
        if not self.flow or self.is_running:
            return
        self.is_running = True
        self.thread = threading.Thread(target=self._execute_flow)
        self.thread.start()
    
    def _execute_flow(self):
        try:
            self.logger.info("开始执行流程: {}".format(self.flow.get("name", "Unknown")))
            steps = self.flow.get("steps", [])
            if not steps:
                self.logger.warning("流程中没有步骤")
                return
            
            current_index = 0
            while current_index < len(steps) and self.is_running:
                step = steps[current_index]
                self.current_step = step
                self.logger.info(f"执行步骤: {step.get('name', step.get('id'))}")
                
                try:
                    self._execute_step(step)
                except Exception as e:
                    self.logger.error(f"步骤执行失败: {str(e)}")
                
                next_step_id = step.get("next_step")
                if next_step_id:
                    current_index = self._find_step_index(next_step_id)
                else:
                    current_index += 1
            
            self.logger.info("流程执行完成")
        finally:
            self.is_running = False
            self.current_step = None
    
    def _execute_step(self, step: Dict[str, Any]):
        step_type = step["type"]
        config = step.get("config", {})
        
        wait_before = step.get("wait_before")
        if wait_before:
            self._execute_wait(wait_before)
        
        self.logger.debug(f"执行操作类型: {step_type}")
        
        wait_after = step.get("wait_after")
        if wait_after:
            self._execute_wait(wait_after)
    
    def _execute_wait(self, wait_config):
        if isinstance(wait_config, dict):
            wait_type = wait_config.get("type", "fixed")
            if wait_type == "random":
                min_wait = wait_config.get("min", 1)
                max_wait = wait_config.get("max", 3)
                import random
                wait_time = random.uniform(min_wait, max_wait)
            else:
                wait_time = wait_config.get("value", 1)
        else:
            wait_time = wait_config
        time.sleep(wait_time)
    
    def _find_step_index(self, step_id: str) -> int:
        steps = self.flow.get("steps", [])
        for i, step in enumerate(steps):
            if step["id"] == step_id:
                return i
        return -1
    
    def stop(self):
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "is_running": self.is_running,
            "current_step": self.current_step,
            "flow_name": self.flow.get("name") if self.flow else None
        }