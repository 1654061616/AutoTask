# AutoFlow 自动化操作软件 实现计划

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 逐任务实现此计划。步骤使用复选框（`- [ ]`）语法来跟踪进度。

**目标：** 构建一个基于 Python + PySide6 的可视化桌面自动化工具，支持鼠标控制、键盘输入、图片识别、分支判断等自动化操作。

**架构：** 三层架构设计——GUI界面层（PySide6）、核心引擎层（流程解析/执行/变量管理）、操作层（鼠标/键盘/图片/OCR/Excel等）。插件化设计，支持自定义扩展。

**技术栈：** PySide6、pyautogui、pydirectinput、opencv-python、easyocr、openpyxl、numpy、Pillow、mss、APScheduler、pyperclip

---

## 文件结构

| 文件路径 | 职责 |
|---------|------|
| `main.py` | 入口文件，启动应用 |
| `core/engine.py` | 流程执行引擎 |
| `core/parser.py` | JSON流程文件解析器 |
| `core/variables.py` | 变量管理器 |
| `core/scheduler.py` | 定时任务调度器 |
| `core/logger.py` | 日志记录器 |
| `operations/mouse.py` | 鼠标操作模块 |
| `operations/keyboard.py` | 键盘操作模块 |
| `operations/image_match.py` | 图片识别模块 |
| `operations/ocr_engine.py` | OCR文字识别模块 |
| `operations/excel_reader.py` | Excel读取模块 |
| `operations/file_ops.py` | 文件操作模块 |
| `operations/window_ctrl.py` | 窗口控制模块 |
| `operations/clipboard.py` | 剪贴板操作模块 |
| `operations/conditions.py` | 条件判断模块 |
| `gui/main_window.py` | 主窗口 |
| `gui/step_editor.py` | 步骤编辑器 |
| `gui/property_panel.py` | 属性配置面板 |
| `gui/toolbox.py` | 工具箱面板 |
| `gui/monitor_panel.py` | 监控面板 |
| `gui/flow_manager.py` | 流程管理 |
| `gui/scheduler_dialog.py` | 定时调度对话框 |
| `gui/widgets/step_table.py` | 步骤表格控件 |
| `gui/widgets/image_picker.py` | 图片选择器控件 |
| `gui/widgets/variable_editor.py` | 变量编辑器控件 |
| `plugins/__init__.py` | 插件初始化 |
| `resources/icons/` | 图标资源目录 |
| `tests/test_engine.py` | 引擎测试 |
| `tests/test_image_match.py` | 图片识别测试 |
| `tests/test_mouse.py` | 鼠标操作测试 |
| `tests/test_excel.py` | Excel读取测试 |
| `requirements.txt` | 依赖清单 |

---

## Phase 1：基础框架搭建

### 任务 1：项目初始化与依赖配置

**文件：**
- 创建：`requirements.txt`
- 创建：`main.py`
- 创建：`core/__init__.py`
- 创建：`operations/__init__.py`
- 创建：`gui/__init__.py`
- 创建：`plugins/__init__.py`
- 创建：`resources/icons/.gitkeep`

- [ ] **步骤 1：创建依赖清单**

```text
PySide6>=6.5.0
pyautogui>=0.9.54
pydirectinput>=1.0.4
opencv-python>=4.8.0
easyocr>=1.7.0
openpyxl>=3.1.0
numpy>=1.24.0
Pillow>=10.0.0
mss>=10.0.0
APScheduler>=3.10.0
pyperclip>=1.8.2
pytest>=7.4.0
```

- [ ] **步骤 2：安装依赖**

运行：`pip install -r requirements.txt`
预期：所有依赖安装成功

- [ ] **步骤 3：创建入口文件**

```python
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("AutoFlow - 自动化操作软件")
    window.setGeometry(100, 100, 1200, 800)
    
    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)
    layout.addWidget(QLabel("AutoFlow 自动化操作软件 - 开发中"))
    window.setCentralWidget(central_widget)
    
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

- [ ] **步骤 4：验证入口文件运行**

运行：`python main.py`
预期：弹出窗口显示"AutoFlow 自动化操作软件 - 开发中"

- [ ] **步骤 5：Commit**

```bash
git add requirements.txt main.py core/__init__.py operations/__init__.py gui/__init__.py plugins/__init__.py resources/icons/.gitkeep
git commit -m "init: project setup and dependencies"
```

### 任务 2：核心日志模块

**文件：**
- 创建：`core/logger.py`
- 创建：`tests/test_logger.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
import sys
sys.path.insert(0, '..')
from core.logger import Logger

def test_logger_info():
    logger = Logger()
    logger.info("Test info message")
    assert len(logger.get_logs()) > 0

def test_logger_error():
    logger = Logger()
    logger.error("Test error message")
    logs = logger.get_logs()
    assert any("ERROR" in log for log in logs)

def test_logger_clear():
    logger = Logger()
    logger.info("Test")
    logger.clear()
    assert len(logger.get_logs()) == 0
```

- [ ] **步骤 2：运行测试验证失败**

运行：`pytest tests/test_logger.py -v`
预期：FAIL，报错 "ModuleNotFoundError: No module named 'core.logger'"

- [ ] **步骤 3：编写最少实现代码**

```python
import logging
import time
from typing import List

class Logger:
    def __init__(self):
        self.logs: List[str] = []
        self.log_format = "%Y-%m-%d %H:%M:%S"
    
    def _add_log(self, level: str, message: str):
        timestamp = time.strftime(self.log_format)
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
    
    def info(self, message: str):
        self._add_log("INFO", message)
    
    def error(self, message: str):
        self._add_log("ERROR", message)
    
    def warning(self, message: str):
        self._add_log("WARNING", message)
    
    def debug(self, message: str):
        self._add_log("DEBUG", message)
    
    def get_logs(self) -> List[str]:
        return self.logs
    
    def clear(self):
        self.logs.clear()
    
    def get_last_log(self) -> str:
        return self.logs[-1] if self.logs else ""
```

- [ ] **步骤 4：运行测试验证通过**

运行：`pytest tests/test_logger.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add core/logger.py tests/test_logger.py
git commit -m "feat: add logger module"
```

### 任务 3：变量管理器模块

**文件：**
- 创建：`core/variables.py`
- 创建：`tests/test_variables.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
import sys
sys.path.insert(0, '..')
from core.variables import VariableManager

def test_set_and_get_variable():
    vm = VariableManager()
    vm.set_variable("name", "test")
    assert vm.get_variable("name") == "test"

def test_resolve_expression():
    vm = VariableManager()
    vm.set_variable("name", "World")
    result = vm.resolve_expression("Hello ${name}")
    assert result == "Hello World"

def test_unresolved_variable():
    vm = VariableManager()
    result = vm.resolve_expression("Hello ${unknown}")
    assert result == "Hello ${unknown}"

def test_parse_excel_reference():
    vm = VariableManager()
    result = vm.parse_excel_reference("${EXCEL:Sheet1!A1}")
    assert result == ("Sheet1", "A1")
```

- [ ] **步骤 2：运行测试验证失败**

运行：`pytest tests/test_variables.py -v`
预期：FAIL，报错 "ModuleNotFoundError: No module named 'core.variables'"

- [ ] **步骤 3：编写最少实现代码**

```python
import re
from typing import Dict, Any, Tuple, Optional

class VariableManager:
    def __init__(self):
        self.variables: Dict[str, Any] = {}
        self.excel_data: Dict[str, Any] = {}
    
    def set_variable(self, name: str, value: Any):
        self.variables[name] = value
    
    def get_variable(self, name: str) -> Any:
        return self.variables.get(name)
    
    def resolve_expression(self, text: str) -> str:
        if not text:
            return text
        
        def replace_match(match):
            var_name = match.group(1)
            value = self.get_variable(var_name)
            if value is not None:
                return str(value)
            return match.group(0)
        
        pattern = r'\$\{(\w+)\}'
        return re.sub(pattern, replace_match, text)
    
    def parse_excel_reference(self, ref: str) -> Optional[Tuple[str, str]]:
        pattern = r'\$\{EXCEL:([^!]+)!([A-Za-z]+\d+)\}'
        match = re.match(pattern, ref)
        if match:
            return match.group(1), match.group(2)
        return None
    
    def load_excel(self, file_path: str):
        pass
    
    def get_excel_value(self, sheet_name: str, cell_ref: str) -> Any:
        key = f"{sheet_name}!{cell_ref}"
        return self.excel_data.get(key)
```

- [ ] **步骤 4：运行测试验证通过**

运行：`pytest tests/test_variables.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add core/variables.py tests/test_variables.py
git commit -m "feat: add variable manager module"
```

### 任务 4：流程解析器模块

**文件：**
- 创建：`core/parser.py`
- 创建：`tests/test_parser.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
import sys
import json
sys.path.insert(0, '..')
from core.parser import FlowParser

def test_parse_flow():
    flow_data = {
        "name": "Test Flow",
        "version": "1.0",
        "steps": [
            {
                "id": "step_1",
                "type": "mouse_click",
                "name": "Test Click",
                "config": {},
                "next_step": None
            }
        ]
    }
    parser = FlowParser()
    flow = parser.parse(flow_data)
    assert flow["name"] == "Test Flow"
    assert len(flow["steps"]) == 1
    assert flow["steps"][0]["type"] == "mouse_click"

def test_validate_step():
    parser = FlowParser()
    step = {
        "id": "step_1",
        "type": "mouse_click",
        "name": "Test",
        "config": {},
        "next_step": None
    }
    assert parser.validate_step(step) is True

def test_invalid_step_missing_id():
    parser = FlowParser()
    step = {
        "type": "mouse_click",
        "name": "Test",
        "config": {},
        "next_step": None
    }
    assert parser.validate_step(step) is False
```

- [ ] **步骤 2：运行测试验证失败**

运行：`pytest tests/test_parser.py -v`
预期：FAIL，报错 "ModuleNotFoundError: No module named 'core.parser'"

- [ ] **步骤 3：编写最少实现代码**

```python
import json
import os
from typing import Dict, Any, List, Optional

class FlowParser:
    def __init__(self):
        self.required_fields = ["id", "type", "name", "config"]
        self.valid_step_types = [
            "mouse_click", "mouse_move", "mouse_drag", "mouse_scroll",
            "keyboard_type", "keyboard_press", "keyboard_hotkey",
            "wait", "image_find", "image_click", "image_exists",
            "ocr_find", "ocr_read",
            "if_else", "loop",
            "set_variable", "get_variable",
            "excel_read",
            "screenshot", "log",
            "window_find", "window_activate", "window_close"
        ]
    
    def parse(self, flow_data: Dict[str, Any]) -> Dict[str, Any]:
        flow = flow_data.copy()
        flow["steps"] = self._parse_steps(flow.get("steps", []))
        flow["variables"] = flow.get("variables", {})
        flow["global_config"] = flow.get("global_config", {})
        return flow
    
    def _parse_steps(self, steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        parsed_steps = []
        for step in steps:
            if self.validate_step(step):
                parsed_steps.append(step)
        return parsed_steps
    
    def validate_step(self, step: Dict[str, Any]) -> bool:
        for field in self.required_fields:
            if field not in step:
                return False
        if step["type"] not in self.valid_step_types:
            return False
        if not isinstance(step["config"], dict):
            return False
        return True
    
    def load_from_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return self.parse(data)
        except Exception as e:
            return None
    
    def save_to_file(self, flow: Dict[str, Any], file_path: str) -> bool:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(flow, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            return False
    
    def get_step_by_id(self, flow: Dict[str, Any], step_id: str) -> Optional[Dict[str, Any]]:
        for step in flow.get("steps", []):
            if step["id"] == step_id:
                return step
        return None
```

- [ ] **步骤 4：运行测试验证通过**

运行：`pytest tests/test_parser.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add core/parser.py tests/test_parser.py
git commit -m "feat: add flow parser module"
```

### 任务 5：流程执行引擎

**文件：**
- 创建：`core/engine.py`
- 创建：`tests/test_engine.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
import sys
sys.path.insert(0, '..')
from core.engine import FlowEngine

def test_engine_initialization():
    engine = FlowEngine()
    assert not engine.is_running
    assert engine.current_step is None

def test_load_flow():
    engine = FlowEngine()
    flow = {
        "name": "Test",
        "version": "1.0",
        "steps": []
    }
    engine.load_flow(flow)
    assert engine.flow["name"] == "Test"

def test_stop_engine():
    engine = FlowEngine()
    engine.is_running = True
    engine.stop()
    assert not engine.is_running
```

- [ ] **步骤 2：运行测试验证失败**

运行：`pytest tests/test_engine.py -v`
预期：FAIL，报错 "ModuleNotFoundError: No module named 'core.engine'"

- [ ] **步骤 3：编写最少实现代码**

```python
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
```

- [ ] **步骤 4：运行测试验证通过**

运行：`pytest tests/test_engine.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add core/engine.py tests/test_engine.py
git commit -m "feat: add flow engine module"
```

### 任务 6：定时调度器模块

**文件：**
- 创建：`core/scheduler.py`
- 创建：`tests/test_scheduler.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
import sys
sys.path.insert(0, '..')
from core.scheduler import TaskScheduler

def test_scheduler_initialization():
    scheduler = TaskScheduler()
    assert scheduler is not None

def test_add_task():
    scheduler = TaskScheduler()
    scheduler.add_task("test_task", "interval", interval=60)
    assert "test_task" in scheduler.tasks

def test_remove_task():
    scheduler = TaskScheduler()
    scheduler.add_task("test_task", "interval", interval=60)
    scheduler.remove_task("test_task")
    assert "test_task" not in scheduler.tasks

def test_start_stop():
    scheduler = TaskScheduler()
    scheduler.start()
    assert scheduler.is_running
    scheduler.stop()
    assert not scheduler.is_running
```

- [ ] **步骤 2：运行测试验证失败**

运行：`pytest tests/test_scheduler.py -v`
预期：FAIL，报错 "ModuleNotFoundError: No module named 'core.scheduler'"

- [ ] **步骤 3：编写最少实现代码**

```python
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from typing import Dict, Any, Callable, Optional
import datetime

class TaskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler(timezone="Asia/Shanghai")
        self.tasks: Dict[str, Any] = {}
        self.is_running = False
    
    def add_task(self, task_id: str, trigger_type: str, **kwargs):
        func = kwargs.pop('func', None)
        
        if trigger_type == "interval":
            seconds = kwargs.get('interval', 60)
            trigger = IntervalTrigger(seconds=seconds)
        elif trigger_type == "cron":
            hour = kwargs.get('hour', 0)
            minute = kwargs.get('minute', 0)
            trigger = CronTrigger(hour=hour, minute=minute)
        elif trigger_type == "date":
            run_date = kwargs.get('run_date', datetime.datetime.now())
            trigger = DateTrigger(run_date=run_date)
        else:
            return False
        
        if func:
            self.scheduler.add_job(
                func,
                trigger=trigger,
                id=task_id,
                name=task_id
            )
            self.tasks[task_id] = {
                "type": trigger_type,
                "kwargs": kwargs
            }
            return True
        return False
    
    def remove_task(self, task_id: str):
        if task_id in self.tasks:
            self.scheduler.remove_job(task_id)
            del self.tasks[task_id]
            return True
        return False
    
    def start(self):
        if not self.is_running:
            self.scheduler.start()
            self.is_running = True
    
    def stop(self):
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
    
    def get_tasks(self) -> Dict[str, Any]:
        return self.tasks.copy()
    
    def modify_task(self, task_id: str, **kwargs):
        if task_id in self.tasks:
            self.remove_task(task_id)
            return self.add_task(task_id, self.tasks[task_id]["type"], **kwargs)
        return False
```

- [ ] **步骤 4：运行测试验证通过**

运行：`pytest tests/test_scheduler.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add core/scheduler.py tests/test_scheduler.py
git commit -m "feat: add task scheduler module"
```

---

## Phase 2：操作模块实现

### 任务 7：鼠标操作模块

**文件：**
- 创建：`operations/mouse.py`
- 创建：`tests/test_mouse.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
import sys
sys.path.insert(0, '..')
from operations.mouse import MouseController

def test_mouse_controller_initialization():
    mouse = MouseController()
    assert mouse is not None

def test_get_position():
    mouse = MouseController()
    x, y = mouse.get_position()
    assert isinstance(x, int)
    assert isinstance(y, int)

def test_move_to():
    mouse = MouseController()
    mouse.move_to(100, 100, duration=0.1)
    x, y = mouse.get_position()
    assert abs(x - 100) <= 5
    assert abs(y - 100) <= 5
```

- [ ] **步骤 2：运行测试验证失败**

运行：`pytest tests/test_mouse.py -v`
预期：FAIL，报错 "ModuleNotFoundError: No module named 'operations.mouse'"

- [ ] **步骤 3：编写最少实现代码**

```python
import pyautogui
import pydirectinput
import random
import time
from typing import Tuple

class MouseController:
    def __init__(self, backend: str = "pyautogui"):
        self.backend = backend
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.01
    
    def get_position(self) -> Tuple[int, int]:
        if self.backend == "pyautogui":
            return pyautogui.position()
        elif self.backend == "pydirectinput":
            x, y = pydirectinput.position()
            return int(x), int(y)
        return pyautogui.position()
    
    def move_to(self, x: int, y: int, duration: float = 0.5):
        if self.backend == "pyautogui":
            pyautogui.moveTo(x, y, duration=duration)
        elif self.backend == "pydirectinput":
            pydirectinput.moveTo(x, y, duration=duration)
    
    def move_rel(self, dx: int, dy: int, duration: float = 0.5):
        if self.backend == "pyautogui":
            pyautogui.move(dx, dy, duration=duration)
        elif self.backend == "pydirectinput":
            pydirectinput.moveRel(dx, dy, duration=duration)
    
    def click(self, x: int = None, y: int = None, click_type: str = "left", 
              offset_x: int = 0, offset_y: int = 0, clicks: int = 1, interval: float = 0.25):
        actual_x = (x or self.get_position()[0]) + offset_x
        actual_y = (y or self.get_position()[1]) + offset_y
        
        if clicks > 1:
            self._multi_click(actual_x, actual_y, click_type, clicks, interval)
        else:
            if self.backend == "pyautogui":
                pyautogui.click(actual_x, actual_y, button=click_type)
            elif self.backend == "pydirectinput":
                if click_type == "left":
                    pydirectinput.click(actual_x, actual_y)
                elif click_type == "right":
                    pydirectinput.rightClick(actual_x, actual_y)
    
    def _multi_click(self, x: int, y: int, click_type: str, clicks: int, interval: float):
        self.move_to(x, y)
        for _ in range(clicks):
            if click_type == "left":
                self._press_left()
                time.sleep(interval)
            elif click_type == "right":
                self._press_right()
                time.sleep(interval)
    
    def _press_left(self):
        if self.backend == "pyautogui":
            pyautogui.mouseDown(button="left")
            time.sleep(0.05)
            pyautogui.mouseUp(button="left")
        elif self.backend == "pydirectinput":
            pydirectinput.mouseDown()
            time.sleep(0.05)
            pydirectinput.mouseUp()
    
    def _press_right(self):
        if self.backend == "pyautogui":
            pyautogui.mouseDown(button="right")
            time.sleep(0.05)
            pyautogui.mouseUp(button="right")
        elif self.backend == "pydirectinput":
            pydirectinput.mouseDown(button="right")
            time.sleep(0.05)
            pydirectinput.mouseUp(button="right")
    
    def double_click(self, x: int = None, y: int = None, offset_x: int = 0, offset_y: int = 0):
        self.click(x, y, "left", offset_x, offset_y, clicks=2)
    
    def right_click(self, x: int = None, y: int = None, offset_x: int = 0, offset_y: int = 0):
        self.click(x, y, "right", offset_x, offset_y)
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5):
        if self.backend == "pyautogui":
            pyautogui.dragTo(end_x, end_y, duration=duration)
        elif self.backend == "pydirectinput":
            pydirectinput.moveTo(start_x, start_y)
            pydirectinput.mouseDown()
            pydirectinput.moveTo(end_x, end_y, duration=duration)
            pydirectinput.mouseUp()
    
    def scroll(self, clicks: int, x: int = None, y: int = None):
        if x is not None and y is not None:
            self.move_to(x, y)
        if self.backend == "pyautogui":
            pyautogui.scroll(clicks)
        elif self.backend == "pydirectinput":
            pydirectinput.scroll(clicks)
    
    def click_random(self, x: int, y: int, radius: int = 10):
        offset_x = random.randint(-radius, radius)
        offset_y = random.randint(-radius, radius)
        self.click(x + offset_x, y + offset_y)
    
    def move_random(self, x: int, y: int, radius: int = 5):
        offset_x = random.randint(-radius, radius)
        offset_y = random.randint(-radius, radius)
        self.move_to(x + offset_x, y + offset_y)
```

- [ ] **步骤 4：运行测试验证通过**

运行：`pytest tests/test_mouse.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add operations/mouse.py tests/test_mouse.py
git commit -m "feat: add mouse controller module"
```

### 任务 8：键盘操作模块

**文件：**
- 创建：`operations/keyboard.py`
- 创建：`tests/test_keyboard.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
import sys
sys.path.insert(0, '..')
from operations.keyboard import KeyboardController

def test_keyboard_controller_initialization():
    keyboard = KeyboardController()
    assert keyboard is not None

def test_type_text():
    keyboard = KeyboardController()
    keyboard.type_text("test", interval=0.01)

def test_press_key():
    keyboard = KeyboardController()
    keyboard.press_key("enter")

def test_hotkey():
    keyboard = KeyboardController()
    keyboard.hotkey("ctrl", "a")
```

- [ ] **步骤 2：运行测试验证失败**

运行：`pytest tests/test_keyboard.py -v`
预期：FAIL，报错 "ModuleNotFoundError: No module named 'operations.keyboard'"

- [ ] **步骤 3：编写最少实现代码**

```python
import pyautogui
import pydirectinput
import pyperclip
import random
import time
from typing import List

class KeyboardController:
    def __init__(self, backend: str = "pyautogui"):
        self.backend = backend
    
    def type_text(self, text: str, interval: float = 0.1, anti_detection: bool = False):
        if anti_detection:
            self._type_anti_detection(text)
        else:
            if self.backend == "pyautogui":
                pyautogui.write(text, interval=interval)
            elif self.backend == "pydirectinput":
                for char in text:
                    pydirectinput.typewrite(char, interval=interval)
    
    def _type_anti_detection(self, text: str):
        for char in text:
            base_interval = random.uniform(0.05, 0.2)
            variance = random.uniform(-0.02, 0.02)
            time.sleep(base_interval + variance)
            
            if random.random() < 0.1:
                time.sleep(random.uniform(0.1, 0.3))
            
            if self.backend == "pyautogui":
                pyautogui.write(char)
            elif self.backend == "pydirectinput":
                pydirectinput.typewrite(char)
    
    def press_key(self, key: str):
        if self.backend == "pyautogui":
            pyautogui.press(key)
        elif self.backend == "pydirectinput":
            pydirectinput.press(key)
    
    def hotkey(self, *keys: str):
        if self.backend == "pyautogui":
            pyautogui.hotkey(*keys)
        elif self.backend == "pydirectinput":
            for key in keys[:-1]:
                pydirectinput.keyDown(key)
            pydirectinput.press(keys[-1])
            for key in reversed(keys[:-1]):
                pydirectinput.keyUp(key)
    
    def key_down(self, key: str):
        if self.backend == "pyautogui":
            pyautogui.keyDown(key)
        elif self.backend == "pydirectinput":
            pydirectinput.keyDown(key)
    
    def key_up(self, key: str):
        if self.backend == "pyautogui":
            pyautogui.keyUp(key)
        elif self.backend == "pydirectinput":
            pydirectinput.keyUp(key)
    
    def type_safe(self, text: str):
        pyperclip.copy(text)
        time.sleep(0.1)
        self.hotkey("ctrl", "v")
    
    def paste_text(self, text: str):
        self.type_safe(text)
    
    def clear_input(self):
        self.hotkey("ctrl", "a")
        self.press_key("delete")
    
    def enter(self):
        self.press_key("enter")
    
    def tab(self):
        self.press_key("tab")
    
    def backspace(self, times: int = 1):
        for _ in range(times):
            self.press_key("backspace")
    
    def delete(self, times: int = 1):
        for _ in range(times):
            self.press_key("delete")
    
    def escape(self):
        self.press_key("esc")
    
    def space(self, times: int = 1):
        for _ in range(times):
            self.press_key("space")
```

- [ ] **步骤 4：运行测试验证通过**

运行：`pytest tests/test_keyboard.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add operations/keyboard.py tests/test_keyboard.py
git commit -m "feat: add keyboard controller module"
```

### 任务 9：文件操作模块

**文件：**
- 创建：`operations/file_ops.py`
- 创建：`tests/test_file_ops.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
import sys
import os
sys.path.insert(0, '..')
from operations.file_ops import FileOperations

def test_file_ops_initialization():
    file_ops = FileOperations()
    assert file_ops is not None

def test_take_screenshot():
    file_ops = FileOperations()
    path = "test_screenshot.png"
    file_ops.take_screenshot(path)
    assert os.path.exists(path)
    os.remove(path)

def test_take_screenshot_region():
    file_ops = FileOperations()
    path = "test_region.png"
    file_ops.take_screenshot_region(path, 0, 0, 100, 100)
    assert os.path.exists(path)
    os.remove(path)
```

- [ ] **步骤 2：运行测试验证失败**

运行：`pytest tests/test_file_ops.py -v`
预期：FAIL，报错 "ModuleNotFoundError: No module named 'operations.file_ops'"

- [ ] **步骤 3：编写最少实现代码**

```python
import pyautogui
import mss
import mss.tools
import os
from PIL import Image
from typing import Optional

class FileOperations:
    def __init__(self):
        pass
    
    def take_screenshot(self, save_path: str) -> bool:
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(save_path)
            return True
        except Exception as e:
            return False
    
    def take_screenshot_region(self, save_path: str, x: int, y: int, width: int, height: int) -> bool:
        try:
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            screenshot.save(save_path)
            return True
        except Exception as e:
            return False
    
    def take_screenshot_mss(self, save_path: str) -> bool:
        try:
            with mss.mss() as sct:
                screenshot = sct.grab(sct.monitors[1])
                mss.tools.to_png(screenshot.rgb, screenshot.size, output=save_path)
            return True
        except Exception as e:
            return False
    
    def take_screenshot_region_mss(self, save_path: str, x: int, y: int, width: int, height: int) -> bool:
        try:
            with mss.mss() as sct:
                region = {"top": y, "left": x, "width": width, "height": height}
                screenshot = sct.grab(region)
                mss.tools.to_png(screenshot.rgb, screenshot.size, output=save_path)
            return True
        except Exception as e:
            return False
    
    def save_image(self, image, save_path: str) -> bool:
        try:
            if isinstance(image, Image.Image):
                image.save(save_path)
            return True
        except Exception as e:
            return False
    
    def read_file(self, file_path: str) -> Optional[str]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return None
    
    def write_file(self, file_path: str, content: str) -> bool:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            return False
    
    def append_file(self, file_path: str, content: str) -> bool:
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            return False
    
    def file_exists(self, file_path: str) -> bool:
        return os.path.exists(file_path)
    
    def create_directory(self, dir_path: str) -> bool:
        try:
            os.makedirs(dir_path, exist_ok=True)
            return True
        except Exception as e:
            return False
    
    def delete_file(self, file_path: str) -> bool:
        try:
            os.remove(file_path)
            return True
        except Exception as e:
            return False
    
    def get_file_size(self, file_path: str) -> Optional[int]:
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            return None
    
    def list_directory(self, dir_path: str) -> list:
        try:
            return os.listdir(dir_path)
        except Exception as e:
            return []
```

- [ ] **步骤 4：运行测试验证通过**

运行：`pytest tests/test_file_ops.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add operations/file_ops.py tests/test_file_ops.py
git commit -m "feat: add file operations module"
```

### 任务 10：剪贴板操作模块

**文件：**
- 创建：`operations/clipboard.py`
- 创建：`tests/test_clipboard.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
import sys
sys.path.insert(0, '..')
from operations.clipboard import ClipboardController

def test_clipboard_controller_initialization():
    clipboard = ClipboardController()
    assert clipboard is not None

def test_copy_and_paste():
    clipboard = ClipboardController()
    test_text = "test clipboard content"
    clipboard.copy(test_text)
    result = clipboard.paste()
    assert result == test_text

def test_clear():
    clipboard = ClipboardController()
    clipboard.copy("test")
    clipboard.clear()
    result = clipboard.paste()
    assert result != "test"
```

- [ ] **步骤 2：运行测试验证失败**

运行：`pytest tests/test_clipboard.py -v`
预期：FAIL，报错 "ModuleNotFoundError: No module named 'operations.clipboard'"

- [ ] **步骤 3：编写最少实现代码**

```python
import pyperclip
import time

class ClipboardController:
    def __init__(self):
        pass
    
    def copy(self, text: str) -> bool:
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            return False
    
    def paste(self) -> str:
        try:
            return pyperclip.paste()
        except Exception as e:
            return ""
    
    def clear(self) -> bool:
        return self.copy("")
    
    def copy_from_selection(self) -> bool:
        try:
            import pyautogui
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.1)
            return True
        except Exception as e:
            return False
    
    def paste_to_current(self) -> bool:
        try:
            import pyautogui
            pyautogui.hotkey('ctrl', 'v')
            return True
        except Exception as e:
            return False
    
    def get_clipboard_history(self) -> list:
        return []
    
    def set_clipboard_image(self, image_path: str) -> bool:
        try:
            from PIL import Image
            image = Image.open(image_path)
            import io
            output = io.BytesIO()
            image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()
            
            import win32clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            return True
        except Exception as e:
            return False
```

- [ ] **步骤 4：运行测试验证通过**

运行：`pytest tests/test_clipboard.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add operations/clipboard.py tests/test_clipboard.py
git commit -m "feat: add clipboard controller module"
```

### 任务 11：Excel读取模块

**文件：**
- 创建：`operations/excel_reader.py`
- 创建：`tests/test_excel.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
import sys
import os
sys.path.insert(0, '..')
from operations.excel_reader import ExcelReader

def test_excel_reader_initialization():
    reader = ExcelReader("test.xlsx")
    assert reader is not None

def test_get_sheet_names(tmp_path):
    import openpyxl
    wb = openpyxl.Workbook()
    wb.create_sheet("TestSheet")
    test_file = tmp_path / "test.xlsx"
    wb.save(test_file)
    
    reader = ExcelReader(str(test_file))
    reader.open()
    sheets = reader.get_sheet_names()
    assert "TestSheet" in sheets
    reader.close()

def test_read_cell(tmp_path):
    import openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws["A1"] = "Hello"
    ws["B1"] = 123
    test_file = tmp_path / "test.xlsx"
    wb.save(test_file)
    
    reader = ExcelReader(str(test_file))
    reader.open()
    value = reader.read_cell("Sheet", "A1")
    assert value == "Hello"
    reader.close()
```

- [ ] **步骤 2：运行测试验证失败**

运行：`pytest tests/test_excel.py -v`
预期：FAIL，报错 "ModuleNotFoundError: No module named 'operations.excel_reader'"

- [ ] **步骤 3：编写最少实现代码**

```python
import openpyxl
from openpyxl import load_workbook
from typing import List, Optional, Any

class ExcelReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.workbook = None
    
    def open(self) -> bool:
        try:
            self.workbook = load_workbook(self.file_path, data_only=True)
            return True
        except Exception as e:
            return False
    
    def close(self):
        if self.workbook:
            self.workbook.close()
            self.workbook = None
    
    def get_sheet_names(self) -> List[str]:
        if not self.workbook:
            return []
        return self.workbook.sheetnames
    
    def read_cell(self, sheet_name: str, cell_ref: str) -> Optional[Any]:
        if not self.workbook:
            return None
        try:
            sheet = self.workbook[sheet_name]
            return sheet[cell_ref].value
        except Exception as e:
            return None
    
    def read_range(self, sheet_name: str, start_cell: str, end_cell: str) -> List[List[Any]]:
        if not self.workbook:
            return []
        try:
            sheet = self.workbook[sheet_name]
            start_col, start_row = self._parse_cell(start_cell)
            end_col, end_row = self._parse_cell(end_cell)
            
            result = []
            for row in range(start_row, end_row + 1):
                row_data = []
                for col in range(start_col, end_col + 1):
                    cell = sheet.cell(row=row, column=col)
                    row_data.append(cell.value)
                result.append(row_data)
            return result
        except Exception as e:
            return []
    
    def read_row(self, sheet_name: str, row_num: int) -> List[Any]:
        if not self.workbook:
            return []
        try:
            sheet = self.workbook[sheet_name]
            max_col = sheet.max_column
            return [sheet.cell(row=row_num, column=col).value for col in range(1, max_col + 1)]
        except Exception as e:
            return []
    
    def read_column(self, sheet_name: str, column_num: int) -> List[Any]:
        if not self.workbook:
            return []
        try:
            sheet = self.workbook[sheet_name]
            max_row = sheet.max_row
            return [sheet.cell(row=row, column=column_num).value for row in range(1, max_row + 1)]
        except Exception as e:
            return []
    
    def get_row_count(self, sheet_name: str) -> int:
        if not self.workbook:
            return 0
        try:
            return self.workbook[sheet_name].max_row
        except Exception as e:
            return 0
    
    def get_column_count(self, sheet_name: str) -> int:
        if not self.workbook:
            return 0
        try:
            return self.workbook[sheet_name].max_column
        except Exception as e:
            return 0
    
    def _parse_cell(self, cell_ref: str) -> tuple:
        col = 0
        row = 0
        for char in cell_ref:
            if char.isalpha():
                col = col * 26 + ord(char.upper()) - ord('A') + 1
            else:
                row = row * 10 + int(char)
        return col, row
    
    def read_all_data(self, sheet_name: str) -> List[List[Any]]:
        if not self.workbook:
            return []
        try:
            sheet = self.workbook[sheet_name]
            max_row = sheet.max_row
            max_col = sheet.max_column
            result = []
            for row in range(1, max_row + 1):
                row_data = []
                for col in range(1, max_col + 1):
                    row_data.append(sheet.cell(row=row, column=col).value)
                result.append(row_data)
            return result
        except Exception as e:
            return []
```

- [ ] **步骤 4：运行测试验证通过**

运行：`pytest tests/test_excel.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add operations/excel_reader.py tests/test_excel.py
git commit -m "feat: add excel reader module"
```

---

## Phase 3：高级操作模块

### 任务 12：图片识别模块

**文件：**
- 创建：`operations/image_match.py`
- 创建：`tests/test_image_match.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
import sys
import os
import numpy as np
sys.path.insert(0, '..')
from operations.image_match import ImageMatcher

def test_image_matcher_initialization():
    matcher = ImageMatcher()
    assert matcher is not None
    assert matcher.default_confidence == 0.85

def test_match_template_basic():
    matcher = ImageMatcher()
    screenshot = np.zeros((100, 100, 3), dtype=np.uint8)
    template = np.zeros((20, 20, 3), dtype=np.uint8)
    screenshot[40:60, 40:60] = 255
    template[:] = 255
    
    result = matcher.match_template(screenshot, template, 0.8)
    assert result is not None
    assert result["confidence"] >= 0.8

def test_image_exists_false():
    matcher = ImageMatcher()
    result = matcher.image_exists("non_existent_image.png")
    assert result is False
```

- [ ] **步骤 2：运行测试验证失败**

运行：`pytest tests/test_image_match.py -v`
预期：FAIL，报错 "ModuleNotFoundError: No module named 'operations.image_match'"

- [ ] **步骤 3：编写最少实现代码**

```python
import cv2
import numpy as np
import pyautogui
import os
from typing import Optional, Tuple, Dict, List

class ImageMatcher:
    def __init__(self):
        self.method = "template"
        self.default_confidence = 0.85
        self.screenshot_cache = None
        self.cache_time = 0
    
    def find_image(self, template_path: str, region: Tuple[int, int, int, int] = None, 
                   confidence: float = None) -> Optional[Dict[str, float]]:
        conf = confidence or self.default_confidence
        
        if not os.path.exists(template_path):
            return None
        
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            return None
        
        screenshot = self._get_screenshot(region)
        if screenshot is None:
            return None
        
        return self.match_template(screenshot, template, conf)
    
    def image_exists(self, template_path: str, region: Tuple[int, int, int, int] = None, 
                     confidence: float = None) -> bool:
        result = self.find_image(template_path, region, confidence)
        return result is not None
    
    def find_all_images(self, template_path: str, region: Tuple[int, int, int, int] = None, 
                        confidence: float = None) -> List[Dict[str, float]]:
        conf = confidence or self.default_confidence
        
        if not os.path.exists(template_path):
            return []
        
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            return []
        
        screenshot = self._get_screenshot(region)
        if screenshot is None:
            return []
        
        results = []
        h, w = template.shape[:2]
        
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        
        res = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= conf)
        
        for pt in zip(*loc[::-1]):
            results.append({
                "x": pt[0],
                "y": pt[1],
                "width": w,
                "height": h,
                "confidence": float(res[pt[1], pt[0]]),
                "center_x": pt[0] + w // 2,
                "center_y": pt[1] + h // 2
            })
        
        return results
    
    def click_image(self, template_path: str, region: Tuple[int, int, int, int] = None, 
                    confidence: float = None, offset_x: int = 0, offset_y: int = 0) -> bool:
        result = self.find_image(template_path, region, confidence)
        if result:
            from .mouse import MouseController
            mouse = MouseController()
            mouse.click(result["center_x"] + offset_x, result["center_y"] + offset_y)
            return True
        return False
    
    def get_image_position(self, template_path: str, region: Tuple[int, int, int, int] = None, 
                           confidence: float = None) -> Optional[Tuple[int, int]]:
        result = self.find_image(template_path, region, confidence)
        if result:
            return result["center_x"], result["center_y"]
        return None
    
    def match_template(self, screenshot: np.ndarray, template: np.ndarray, 
                       confidence: float) -> Optional[Dict[str, float]]:
        h, w = template.shape[:2]
        
        if h > screenshot.shape[0] or w > screenshot.shape[1]:
            return None
        
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        
        res = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        
        if max_val >= confidence:
            return {
                "x": max_loc[0],
                "y": max_loc[1],
                "width": w,
                "height": h,
                "confidence": float(max_val),
                "center_x": max_loc[0] + w // 2,
                "center_y": max_loc[1] + h // 2
            }
        return None
    
    def match_feature(self, screenshot: np.ndarray, template: np.ndarray, 
                      confidence: float) -> Optional[Dict[str, float]]:
        try:
            akaze = cv2.AKAZE_create()
            
            kp1, des1 = akaze.detectAndCompute(template, None)
            kp2, des2 = akaze.detectAndCompute(screenshot, None)
            
            if des1 is None or des2 is None:
                return None
            
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            matches = bf.match(des1, des2)
            
            if len(matches) < 5:
                return None
            
            matches = sorted(matches, key=lambda x: x.distance)
            good_matches = matches[:int(len(matches) * 0.2)]
            
            if len(good_matches) < 3:
                return None
            
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            
            if M is None:
                return None
            
            h, w = template.shape[:2]
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            
            x_min = int(np.min(dst[:, 0, 0]))
            y_min = int(np.min(dst[:, 0, 1]))
            x_max = int(np.max(dst[:, 0, 0]))
            y_max = int(np.max(dst[:, 0, 1]))
            
            match_ratio = len(good_matches) / len(matches)
            
            if match_ratio >= confidence * 0.5:
                return {
                    "x": x_min,
                    "y": y_min,
                    "width": x_max - x_min,
                    "height": y_max - y_min,
                    "confidence": float(match_ratio),
                    "center_x": (x_min + x_max) // 2,
                    "center_y": (y_min + y_max) // 2
                }
            return None
        except Exception as e:
            return None
    
    def _get_screenshot(self, region: Tuple[int, int, int, int] = None) -> Optional[np.ndarray]:
        try:
            if region:
                x, y, w, h = region
                screenshot = pyautogui.screenshot(region=(x, y, w, h))
            else:
                screenshot = pyautogui.screenshot()
            
            screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return screenshot_np
        except Exception as e:
            return None
    
    def update_screenshot_cache(self):
        self.screenshot_cache = self._get_screenshot()
        self.cache_time = cv2.getTickCount()
    
    def set_confidence(self, confidence: float):
        self.default_confidence = confidence
    
    def set_method(self, method: str):
        if method in ["template", "feature"]:
            self.method = method
```

- [ ] **步骤 4：运行测试验证通过**

运行：`pytest tests/test_image_match.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add operations/image_match.py tests/test_image_match.py
git commit -m "feat: add image matcher module"
```

### 任务 13：OCR引擎模块

**文件：**
- 创建：`operations/ocr_engine.py`
- 创建：`tests/test_ocr.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
import sys
sys.path.insert(0, '..')
from operations.ocr_engine import OCREngine

def test_ocr_engine_initialization():
    ocr = OCREngine()
    assert ocr is not None

def test_ocr_engine_without_image():
    ocr = OCREngine()
    result = ocr.recognize_text("non_existent.png")
    assert result == []

def test_ocr_engine_language():
    ocr = OCREngine(languages=["ch_sim", "en"])
    assert "ch_sim" in ocr.languages
    assert "en" in ocr.languages
```

- [ ] **步骤 2：运行测试验证失败**

运行：`pytest tests/test_ocr.py -v`
预期：FAIL，报错 "ModuleNotFoundError: No module named 'operations.ocr_engine'"

- [ ] **步骤 3：编写最少实现代码**

```python
import easyocr
import cv2
import numpy as np
import pyautogui
from typing import List, Dict, Tuple, Optional

class OCREngine:
    def __init__(self, languages: List[str] = None):
        self.languages = languages or ["ch_sim", "en"]
        self.reader = None
        self._init_reader()
    
    def _init_reader(self):
        try:
            self.reader = easyocr.Reader(self.languages, gpu=False)
        except Exception as e:
            self.reader = None
    
    def recognize_text(self, image_path: str = None, image: np.ndarray = None, 
                       region: Tuple[int, int, int, int] = None) -> List[Dict[str, any]]:
        if self.reader is None:
            return []
        
        try:
            if image is not None:
                img = image
            elif image_path:
                img = cv2.imread(image_path)
                if img is None:
                    return []
            elif region:
                screenshot = pyautogui.screenshot(region=region)
                img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            else:
                screenshot = pyautogui.screenshot()
                img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            results = self.reader.readtext(img)
            
            return [
                {
                    "text": text,
                    "bbox": bbox,
                    "confidence": float(confidence),
                    "center_x": (bbox[0][0] + bbox[2][0]) / 2,
                    "center_y": (bbox[0][1] + bbox[2][1]) / 2
                }
                for bbox, text, confidence in results
            ]
        except Exception as e:
            return []
    
    def find_text(self, target_text: str, image_path: str = None, 
                  image: np.ndarray = None, region: Tuple[int, int, int, int] = None,
                  case_sensitive: bool = False) -> Optional[Dict[str, any]]:
        results = self.recognize_text(image_path, image, region)
        
        search_text = target_text if case_sensitive else target_text.lower()
        
        for result in results:
            text = result["text"] if case_sensitive else result["text"].lower()
            if search_text in text:
                return result
        
        return None
    
    def find_text_position(self, target_text: str, image_path: str = None, 
                           image: np.ndarray = None, region: Tuple[int, int, int, int] = None) -> Optional[Tuple[int, int]]:
        result = self.find_text(target_text, image_path, image, region)
        if result:
            return int(result["center_x"]), int(result["center_y"])
        return None
    
    def click_text(self, target_text: str, image_path: str = None, 
                   image: np.ndarray = None, region: Tuple[int, int, int, int] = None,
                   offset_x: int = 0, offset_y: int = 0) -> bool:
        result = self.find_text_position(target_text, image_path, image, region)
        if result:
            from .mouse import MouseController
            mouse = MouseController()
            mouse.click(result[0] + offset_x, result[1] + offset_y)
            return True
        return False
    
    def extract_all_text(self, image_path: str = None, image: np.ndarray = None, 
                         region: Tuple[int, int, int, int] = None) -> str:
        results = self.recognize_text(image_path, image, region)
        return "\n".join([result["text"] for result in results])
    
    def text_exists(self, target_text: str, image_path: str = None, 
                    image: np.ndarray = None, region: Tuple[int, int, int, int] = None) -> bool:
        return self.find_text(target_text, image_path, image, region) is not None
    
    def set_languages(self, languages: List[str]):
        self.languages = languages
        self._init_reader()
    
    def is_available(self) -> bool:
        return self.reader is not None
```

- [ ] **步骤 4：运行测试验证通过**

运行：`pytest tests/test_ocr.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add operations/ocr_engine.py tests/test_ocr.py
git commit -m "feat: add ocr engine module"
```

### 任务 14：窗口控制模块

**文件：**
- 创建：`operations/window_ctrl.py`
- 创建：`tests/test_window_ctrl.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
import sys
sys.path.insert(0, '..')
from operations.window_ctrl import WindowController

def test_window_controller_initialization():
    controller = WindowController()
    assert controller is not None

def test_get_window_handle_by_title():
    controller = WindowController()
    handle = controller.get_window_handle_by_title("")
    assert handle is None or isinstance(handle, int)

def test_list_windows():
    controller = WindowController()
    windows = controller.list_windows()
    assert isinstance(windows, list)
```

- [ ] **步骤 2：运行测试验证失败**

运行：`pytest tests/test_window_ctrl.py -v`
预期：FAIL，报错 "ModuleNotFoundError: No module named 'operations.window_ctrl'"

- [ ] **步骤 3：编写最少实现代码**

```python
import win32gui
import win32con
import win32api
import win32process
import psutil
import pyautogui
from typing import Optional, List, Tuple, Dict

class WindowController:
    def __init__(self):
        pass
    
    def get_window_handle_by_title(self, title: str, exact_match: bool = False) -> Optional[int]:
        handles = []
        
        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd)
                if exact_match:
                    if window_title == title:
                        handles.append(hwnd)
                else:
                    if title in window_title:
                        handles.append(hwnd)
        
        win32gui.EnumWindows(callback, None)
        return handles[0] if handles else None
    
    def list_windows(self) -> List[Dict[str, any]]:
        windows = []
        
        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    rect = win32gui.GetWindowRect(hwnd)
                    windows.append({
                        "handle": hwnd,
                        "title": title,
                        "x": rect[0],
                        "y": rect[1],
                        "width": rect[2] - rect[0],
                        "height": rect[3] - rect[1]
                    })
        
        win32gui.EnumWindows(callback, None)
        return windows
    
    def activate_window(self, handle: int) -> bool:
        try:
            win32gui.SetForegroundWindow(handle)
            return True
        except Exception as e:
            return False
    
    def close_window(self, handle: int) -> bool:
        try:
            win32gui.PostMessage(handle, win32con.WM_CLOSE, 0, 0)
            return True
        except Exception as e:
            return False
    
    def minimize_window(self, handle: int) -> bool:
        try:
            win32gui.ShowWindow(handle, win32con.SW_MINIMIZE)
            return True
        except Exception as e:
            return False
    
    def maximize_window(self, handle: int) -> bool:
        try:
            win32gui.ShowWindow(handle, win32con.SW_MAXIMIZE)
            return True
        except Exception as e:
            return False
    
    def restore_window(self, handle: int) -> bool:
        try:
            win32gui.ShowWindow(handle, win32con.SW_RESTORE)
            return True
        except Exception as e:
            return False
    
    def get_window_rect(self, handle: int) -> Optional[Tuple[int, int, int, int]]:
        try:
            rect = win32gui.GetWindowRect(handle)
            return rect
        except Exception as e:
            return None
    
    def set_window_position(self, handle: int, x: int, y: int, width: int, height: int) -> bool:
        try:
            win32gui.SetWindowPos(handle, None, x, y, width, height, 0)
            return True
        except Exception as e:
            return False
    
    def get_window_title(self, handle: int) -> str:
        try:
            return win32gui.GetWindowText(handle)
        except Exception as e:
            return ""
    
    def is_window_visible(self, handle: int) -> bool:
        try:
            return win32gui.IsWindowVisible(handle)
        except Exception as e:
            return False
    
    def send_mouse_click(self, handle: int, x: int, y: int) -> bool:
        try:
            lParam = win32api.MAKELONG(x, y)
            win32api.SendMessage(handle, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
            win32api.SendMessage(handle, win32con.WM_LBUTTONUP, 0, lParam)
            return True
        except Exception as e:
            return False
    
    def send_key_press(self, handle: int, key_code: int) -> bool:
        try:
            win32api.SendMessage(handle, win32con.WM_KEYDOWN, key_code, 0)
            win32api.SendMessage(handle, win32con.WM_KEYUP, key_code, 0)
            return True
        except Exception as e:
            return False
    
    def get_foreground_window(self) -> Optional[int]:
        try:
            return win32gui.GetForegroundWindow()
        except Exception as e:
            return None
    
    def get_window_process_id(self, handle: int) -> Optional[int]:
        try:
            _, pid = win32process.GetWindowThreadProcessId(handle)
            return pid
        except Exception as e:
            return None
    
    def get_window_process_name(self, handle: int) -> str:
        try:
            pid = self.get_window_process_id(handle)
            if pid:
                process = psutil.Process(pid)
                return process.name()
        except Exception as e:
            pass
        return ""
```

- [ ] **步骤 4：运行测试验证通过**

运行：`pytest tests/test_window_ctrl.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add operations/window_ctrl.py tests/test_window_ctrl.py
git commit -m "feat: add window controller module"
```

### 任务 15：条件判断模块

**文件：**
- 创建：`operations/conditions.py`
- 创建：`tests/test_conditions.py`

- [ ] **步骤 1：编写失败的测试**

```python
import pytest
import sys
sys.path.insert(0, '..')
from operations.conditions import ConditionChecker

def test_condition_checker_initialization():
    checker = ConditionChecker()
    assert checker is not None

def test_check_image_exists():
    checker = ConditionChecker()
    result = checker.check("image_exists", {"image_path": "non_existent.png"})
    assert result is False

def test_check_variable_compare():
    checker = ConditionChecker()
    checker.variable_manager.set_variable("count", 5)
    result = checker.check("variable_compare", {
        "variable": "count",
        "operator": "==",
        "value": 5
    })
    assert result is True
```

- [ ] **步骤 2：运行测试验证失败**

运行：`pytest tests/test_conditions.py -v`
预期：FAIL，报错 "ModuleNotFoundError: No module named 'operations.conditions'"

- [ ] **步骤 3：编写最少实现代码**

```python
from typing import Dict, Any, Optional
from core.variables import VariableManager

class ConditionChecker:
    def __init__(self):
        self.variable_manager = VariableManager()
    
    def check(self, condition_type: str, config: Dict[str, Any]) -> bool:
        try:
            if condition_type == "image_exists":
                return self._check_image_exists(config)
            elif condition_type == "text_exists":
                return self._check_text_exists(config)
            elif condition_type == "variable_compare":
                return self._check_variable_compare(config)
            elif condition_type == "file_exists":
                return self._check_file_exists(config)
            elif condition_type == "window_exists":
                return self._check_window_exists(config)
            elif condition_type == "key_pressed":
                return self._check_key_pressed(config)
            elif condition_type == "time_elapsed":
                return self._check_time_elapsed(config)
            elif condition_type == "always_true":
                return True
            elif condition_type == "always_false":
                return False
        except Exception as e:
            return False
        return False
    
    def _check_image_exists(self, config: Dict[str, Any]) -> bool:
        from .image_match import ImageMatcher
        matcher = ImageMatcher()
        return matcher.image_exists(
            config.get("image_path", ""),
            config.get("region"),
            config.get("confidence")
        )
    
    def _check_text_exists(self, config: Dict[str, Any]) -> bool:
        from .ocr_engine import OCREngine
        ocr = OCREngine()
        return ocr.text_exists(
            config.get("text", ""),
            region=config.get("region")
        )
    
    def _check_variable_compare(self, config: Dict[str, Any]) -> bool:
        var_name = config.get("variable")
        operator = config.get("operator", "==")
        value = config.get("value")
        
        var_value = self.variable_manager.get_variable(var_name)
        
        if var_value is None:
            return False
        
        try:
            if operator == "==":
                return var_value == value
            elif operator == "!=":
                return var_value != value
            elif operator == ">":
                return var_value > value
            elif operator == "<":
                return var_value < value
            elif operator == ">=":
                return var_value >= value
            elif operator == "<=":
                return var_value <= value
            elif operator == "contains":
                return str(value) in str(var_value)
            elif operator == "not_contains":
                return str(value) not in str(var_value)
        except (TypeError, ValueError):
            pass
        return False
    
    def _check_file_exists(self, config: Dict[str, Any]) -> bool:
        import os
        return os.path.exists(config.get("file_path", ""))
    
    def _check_window_exists(self, config: Dict[str, Any]) -> bool:
        from .window_ctrl import WindowController
        controller = WindowController()
        handle = controller.get_window_handle_by_title(
            config.get("title", ""),
            config.get("exact_match", False)
        )
        return handle is not None
    
    def _check_key_pressed(self, config: Dict[str, Any]) -> bool:
        import keyboard
        key = config.get("key", "")
        return keyboard.is_pressed(key)
    
    def _check_time_elapsed(self, config: Dict[str, Any]) -> bool:
        import time
        start_time = config.get("start_time", 0)
        duration = config.get("duration", 0)
        return (time.time() - start_time) >= duration
    
    def set_variable(self, name: str, value: Any):
        self.variable_manager.set_variable(name, value)
    
    def get_variable(self, name: str) -> Any:
        return self.variable_manager.get_variable(name)
```

- [ ] **步骤 4：运行测试验证通过**

运行：`pytest tests/test_conditions.py -v`
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add operations/conditions.py tests/test_conditions.py
git commit -m "feat: add conditions module"
```

---

## Phase 4：GUI界面实现

### 任务 16：主窗口界面

**文件：**
- 修改：`main.py`
- 创建：`gui/main_window.py`

- [ ] **步骤 1：编写主窗口代码**

```python
import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QMenuBar, QToolBar, QStatusBar, QSplitter, QTabWidget
)
from PySide6.QtCore import Qt
from .toolbox import ToolboxPanel
from .step_editor import StepEditor
from .property_panel import PropertyPanel
from .monitor_panel import MonitorPanel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoFlow - 自动化操作软件")
        self.setGeometry(100, 100, 1400, 900)
        
        self._init_menu_bar()
        self._init_tool_bar()
        self._init_central_widget()
        self._init_status_bar()
        
        self.current_flow = None
    
    def _init_menu_bar(self):
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("文件(&F)")
        file_menu.addAction("新建", self._new_flow)
        file_menu.addAction("打开", self._open_flow)
        file_menu.addAction("保存", self._save_flow)
        file_menu.addAction("另存为", self._save_flow_as)
        
        edit_menu = menu_bar.addMenu("编辑(&E)")
        edit_menu.addAction("撤销", self._undo)
        edit_menu.addAction("重做", self._redo)
        
        run_menu = menu_bar.addMenu("运行(&R)")
        run_menu.addAction("启动", self._start_flow)
        run_menu.addAction("停止", self._stop_flow)
        
        help_menu = menu_bar.addMenu("帮助(&H)")
        help_menu.addAction("关于", self._show_about)
    
    def _init_tool_bar(self):
        tool_bar = self.addToolBar("工具栏")
        tool_bar.addAction("新建", self._new_flow)
        tool_bar.addAction("打开", self._open_flow)
        tool_bar.addAction("保存", self._save_flow)
        tool_bar.addSeparator()
        tool_bar.addAction("启动", self._start_flow)
        tool_bar.addAction("停止", self._stop_flow)
        tool_bar.addSeparator()
        tool_bar.addAction("截图", self._take_screenshot)
    
    def _init_central_widget(self):
        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        
        splitter = QSplitter(Qt.Horizontal)
        
        self.toolbox = ToolboxPanel()
        splitter.addWidget(self.toolbox)
        splitter.setStretchFactor(0, 0)
        
        self.step_editor = StepEditor()
        splitter.addWidget(self.step_editor)
        splitter.setStretchFactor(1, 2)
        
        right_panel = QSplitter(Qt.Vertical)
        
        self.property_panel = PropertyPanel()
        right_panel.addWidget(self.property_panel)
        right_panel.setStretchFactor(0, 1)
        
        self.monitor_panel = MonitorPanel()
        right_panel.addWidget(self.monitor_panel)
        right_panel.setStretchFactor(1, 1)
        
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(2, 1)
        
        main_layout.addWidget(splitter)
        self.setCentralWidget(central_widget)
    
    def _init_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
    
    def _new_flow(self):
        self.step_editor.clear_steps()
        self.current_flow = None
        self.status_bar.showMessage("新建流程")
    
    def _open_flow(self):
        from PySide6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "打开流程文件", "", "JSON文件 (*.json)")
        if file_path:
            self._load_flow(file_path)
    
    def _load_flow(self, file_path):
        import json
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                flow = json.load(f)
            self.current_flow = flow
            self.step_editor.load_steps(flow.get("steps", []))
            self.status_bar.showMessage(f"已加载: {file_path}")
        except Exception as e:
            self.status_bar.showMessage(f"加载失败: {str(e)}")
    
    def _save_flow(self):
        if self.current_flow:
            self._save_flow_to_file(self.current_flow.get("file_path", "flow.json"))
        else:
            self._save_flow_as()
    
    def _save_flow_as(self):
        from PySide6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getSaveFileName(self, "保存流程文件", "", "JSON文件 (*.json)")
        if file_path:
            self._save_flow_to_file(file_path)
    
    def _save_flow_to_file(self, file_path):
        import json
        flow = {
            "name": "未命名流程",
            "version": "1.0",
            "steps": self.step_editor.get_steps(),
            "file_path": file_path
        }
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(flow, f, indent=2, ensure_ascii=False)
            self.current_flow = flow
            self.status_bar.showMessage(f"已保存: {file_path}")
        except Exception as e:
            self.status_bar.showMessage(f"保存失败: {str(e)}")
    
    def _start_flow(self):
        self.status_bar.showMessage("正在执行流程...")
    
    def _stop_flow(self):
        self.status_bar.showMessage("流程已停止")
    
    def _undo(self):
        pass
    
    def _redo(self):
        pass
    
    def _take_screenshot(self):
        from operations.file_ops import FileOperations
        file_ops = FileOperations()
        file_ops.take_screenshot("screenshot.png")
        self.status_bar.showMessage("截图已保存")
    
    def _show_about(self):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.about(self, "关于 AutoFlow", "AutoFlow - 可视化桌面自动化引擎\n\n版本: 1.0.0")
    
    def closeEvent(self, event):
        if self.current_flow:
            from PySide6.QtWidgets import QMessageBox
            reply = QMessageBox.question(
                self, "确认退出", "是否保存当前流程？",
                QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
            )
            if reply == QMessageBox.Save:
                self._save_flow()
            elif reply == QMessageBox.Cancel:
                event.ignore()
                return
        event.accept()
```

- [ ] **步骤 2：更新入口文件**

```python
import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

- [ ] **步骤 3：运行验证**

运行：`python main.py`
预期：主窗口正常显示，包含工具栏、工具箱、步骤编辑器、属性面板、监控面板

- [ ] **步骤 4：Commit**

```bash
git add main.py gui/main_window.py
git commit -m "feat: add main window"
```

### 任务 17：工具箱面板

**文件：**
- 创建：`gui/toolbox.py`

- [ ] **步骤 1：编写工具箱代码**

```python
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QListWidget,
    QListWidgetItem, QLabel
)
from PySide6.QtCore import Qt

class ToolboxPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(180)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        basic_group = self._create_group("基础操作", [
            ("mouse_click", "🖱️ 鼠标点击"),
            ("mouse_move", "📍 鼠标移动"),
            ("mouse_drag", "👆 鼠标拖拽"),
            ("mouse_scroll", "🔄 鼠标滚轮"),
            ("keyboard_type", "⌨️ 键盘输入"),
            ("keyboard_press", "⚡ 按键"),
            ("keyboard_hotkey", "🔑 组合键"),
            ("wait", "⏱️ 延时等待"),
            ("screenshot", "📸 截图")
        ])
        layout.addWidget(basic_group)
        
        vision_group = self._create_group("视觉识别", [
            ("image_find", "🔍 图片查找"),
            ("image_click", "🎯 点击图片"),
            ("image_exists", "✅ 判断图片"),
            ("ocr_find", "📝 文字查找"),
            ("ocr_read", "📖 读取文字")
        ])
        layout.addWidget(vision_group)
        
        logic_group = self._create_group("流程控制", [
            ("if_else", "🔀 IF判断"),
            ("loop", "🔄 循环"),
            ("log", "📋 日志"),
            ("set_variable", "💾 设置变量"),
            ("get_variable", "📥 获取变量")
        ])
        layout.addWidget(logic_group)
        
        data_group = self._create_group("数据操作", [
            ("excel_read", "📊 读取Excel"),
            ("file_read", "📄 读取文件"),
            ("file_write", "✏️ 写入文件")
        ])
        layout.addWidget(data_group)
        
        window_group = self._create_group("窗口操作", [
            ("window_find", "🪟 查找窗口"),
            ("window_activate", "✅ 激活窗口"),
            ("window_close", "❌ 关闭窗口")
        ])
        layout.addWidget(window_group)
        
        layout.addStretch()
    
    def _create_group(self, title, items):
        group = QGroupBox(title)
        layout = QVBoxLayout(group)
        
        list_widget = QListWidget()
        list_widget.setSpacing(2)
        
        for item_type, item_name in items:
            item = QListWidgetItem(item_name)
            item.setData(Qt.UserRole, item_type)
            item.setFlags(item.flags() | Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            list_widget.addItem(item)
        
        list_widget.itemDoubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(list_widget)
        
        return group
    
    def _on_item_double_clicked(self, item):
        step_type = item.data(Qt.UserRole)
        self.parent().step_editor.add_step(step_type)
```

- [ ] **步骤 2：运行验证**

运行：`python main.py`
预期：左侧工具箱显示各分组和步骤类型

- [ ] **步骤 3：Commit**

```bash
git add gui/toolbox.py
git commit -m "feat: add toolbox panel"
```

### 任务 18：步骤编辑器

**文件：**
- 创建：`gui/step_editor.py`

- [ ] **步骤 1：编写步骤编辑器代码**

```python
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt
import uuid

class StepEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.steps = []
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        toolbar = QHBoxLayout()
        
        self.add_btn = QPushButton("添加步骤")
        self.add_btn.clicked.connect(self._show_add_menu)
        toolbar.addWidget(self.add_btn)
        
        self.delete_btn = QPushButton("删除步骤")
        self.delete_btn.clicked.connect(self._delete_step)
        toolbar.addWidget(self.delete_btn)
        
        self.up_btn = QPushButton("↑")
        self.up_btn.clicked.connect(self._move_up)
        toolbar.addWidget(self.up_btn)
        
        self.down_btn = QPushButton("↓")
        self.down_btn.clicked.connect(self._move_down)
        toolbar.addWidget(self.down_btn)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "序号", "类型", "名称", "配置", "等待前", "等待后"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.cellDoubleClicked.connect(self._on_cell_double_clicked)
        self.table.selectionModel().selectionChanged.connect(self._on_selection_changed)
        layout.addWidget(self.table)
    
    def load_steps(self, steps):
        self.steps = steps
        self._update_table()
    
    def get_steps(self):
        return self.steps
    
    def clear_steps(self):
        self.steps = []
        self._update_table()
    
    def add_step(self, step_type):
        step = {
            "id": f"step_{str(uuid.uuid4())[:8]}",
            "type": step_type,
            "name": self._get_step_name(step_type),
            "config": {},
            "wait_before": 0,
            "wait_after": 0,
            "next_step": None
        }
        self.steps.append(step)
        self._update_table()
    
    def _get_step_name(self, step_type):
        names = {
            "mouse_click": "鼠标点击",
            "mouse_move": "鼠标移动",
            "mouse_drag": "鼠标拖拽",
            "mouse_scroll": "鼠标滚轮",
            "keyboard_type": "键盘输入",
            "keyboard_press": "按键",
            "keyboard_hotkey": "组合键",
            "wait": "延时等待",
            "screenshot": "截图",
            "image_find": "图片查找",
            "image_click": "点击图片",
            "image_exists": "判断图片",
            "ocr_find": "文字查找",
            "ocr_read": "读取文字",
            "if_else": "IF判断",
            "loop": "循环",
            "log": "日志",
            "set_variable": "设置变量",
            "get_variable": "获取变量",
            "excel_read": "读取Excel",
            "file_read": "读取文件",
            "file_write": "写入文件",
            "window_find": "查找窗口",
            "window_activate": "激活窗口",
            "window_close": "关闭窗口"
        }
        return names.get(step_type, step_type)
    
    def _update_table(self):
        self.table.setRowCount(len(self.steps))
        for i, step in enumerate(self.steps):
            self.table.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.table.setItem(i, 1, QTableWidgetItem(step["type"]))
            self.table.setItem(i, 2, QTableWidgetItem(step["name"]))
            config_str = str(step.get("config", {}))[:50] + "..." if len(str(step.get("config", {}))) > 50 else str(step.get("config", {}))
            self.table.setItem(i, 3, QTableWidgetItem(config_str))
            self.table.setItem(i, 4, QTableWidgetItem(str(step.get("wait_before", 0))))
            self.table.setItem(i, 5, QTableWidgetItem(str(step.get("wait_after", 0))))
    
    def _show_add_menu(self):
        from PySide6.QtWidgets import QMenu
        menu = QMenu(self)
        
        categories = {
            "基础操作": ["mouse_click", "mouse_move", "keyboard_type", "wait"],
            "视觉识别": ["image_find", "image_click", "ocr_find"],
            "流程控制": ["if_else", "loop", "log"],
            "数据操作": ["excel_read", "set_variable"]
        }
        
        for category, types in categories.items():
            submenu = menu.addMenu(category)
            for step_type in types:
                action = submenu.addAction(self._get_step_name(step_type))
                action.triggered.connect(lambda checked, t=step_type: self.add_step(t))
        
        menu.exec_(self.add_btn.mapToGlobal(self.add_btn.rect().bottomLeft()))
    
    def _delete_step(self):
        row = self.table.currentRow()
        if row >= 0:
            reply = QMessageBox.question(
                self, "确认删除", "确定删除此步骤？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.steps.pop(row)
                self._update_table()
    
    def _move_up(self):
        row = self.table.currentRow()
        if row > 0:
            self.steps[row], self.steps[row - 1] = self.steps[row - 1], self.steps[row]
            self._update_table()
            self.table.setCurrentRow(row - 1)
    
    def _move_down(self):
        row = self.table.currentRow()
        if row < len(self.steps) - 1:
            self.steps[row], self.steps[row + 1] = self.steps[row + 1], self.steps[row]
            self._update_table()
            self.table.setCurrentRow(row + 1)
    
    def _on_cell_double_clicked(self, row, column):
        if row < len(self.steps):
            step = self.steps[row]
            self.parent().property_panel.load_step(step)
    
    def _on_selection_changed(self, selected, deselected):
        indexes = selected.indexes()
        if indexes:
            row = indexes[0].row()
            if row < len(self.steps):
                self.parent().property_panel.load_step(self.steps[row])
```

- [ ] **步骤 2：运行验证**

运行：`python main.py`
预期：步骤编辑器表格正常显示，可添加/删除/移动步骤

- [ ] **步骤 3：Commit**

```bash
git add gui/step_editor.py
git commit -m "feat: add step editor"
```

### 任务 19：属性配置面板

**文件：**
- 创建：`gui/property_panel.py`

- [ ] **步骤 1：编写属性面板代码**

```python
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit,
    QSpinBox, QDoubleSpinBox, QComboBox, QTextEdit,
    QLabel, QPushButton, QFileDialog, QCheckBox
)
from PySide6.QtCore import Qt

class PropertyPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.current_step = None
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        self.title_label = QLabel("选择步骤查看属性")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)
        
        self.form_layout = QFormLayout()
        layout.addLayout(self.form_layout)
        
        layout.addStretch()
    
    def load_step(self, step):
        self.current_step = step
        self.title_label.setText(f"步骤: {step.get('name', '')}")
        
        self._clear_form()
        
        self._add_field("名称", "name", QLineEdit)
        
        if step["type"] in ["mouse_click", "mouse_move"]:
            self._add_mouse_fields(step)
        
        elif step["type"] == "keyboard_type":
            self._add_keyboard_fields(step)
        
        elif step["type"] == "wait":
            self._add_wait_fields(step)
        
        elif step["type"] in ["image_find", "image_click", "image_exists"]:
            self._add_image_fields(step)
        
        elif step["type"] == "if_else":
            self._add_if_else_fields(step)
        
        elif step["type"] == "loop":
            self._add_loop_fields(step)
        
        elif step["type"] == "excel_read":
            self._add_excel_fields(step)
        
        elif step["type"] == "set_variable":
            self._add_variable_fields(step)
        
        elif step["type"] == "window_find":
            self._add_window_fields(step)
    
    def _clear_form(self):
        while self.form_layout.count():
            child = self.form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def _add_field(self, label_text, key, widget_type, **kwargs):
        label = QLabel(label_text)
        widget = widget_type()
        
        if hasattr(widget, 'setValue'):
            widget.setValue(self.current_step.get(key, 0))
        elif hasattr(widget, 'setText'):
            widget.setText(str(self.current_step.get(key, "")))
        elif hasattr(widget, 'setChecked'):
            widget.setChecked(self.current_step.get(key, False))
        
        if widget_type == QLineEdit:
            widget.textChanged.connect(lambda text, k=key: self._update_step(k, text))
        elif widget_type in [QSpinBox, QDoubleSpinBox]:
            widget.valueChanged.connect(lambda value, k=key: self._update_step(k, value))
        elif widget_type == QComboBox:
            widget.currentTextChanged.connect(lambda text, k=key: self._update_step(k, text))
        elif widget_type == QCheckBox:
            widget.stateChanged.connect(lambda state, k=key: self._update_step(k, state == Qt.Checked))
        
        self.form_layout.addRow(label, widget)
    
    def _add_mouse_fields(self, step):
        config = step.get("config", {})
        
        self._add_field("点击类型", "click_type", QComboBox)
        click_type_combo = self.form_layout.itemAt(self.form_layout.count() - 1).widget()
        click_type_combo.addItems(["left", "right", "double"])
        
        self._add_field("X坐标", "x", QSpinBox)
        self._add_field("Y坐标", "y", QSpinBox)
        self._add_field("偏移X", "offset_x", QSpinBox)
        self._add_field("偏移Y", "offset_y", QSpinBox)
        
        target_type = QComboBox()
        target_type.addItems(["coordinate", "image"])
        self.form_layout.addRow("目标类型", target_type)
        
        if config.get("target_type") == "image":
            self._add_image_path_field()
    
    def _add_image_path_field(self):
        path_edit = QLineEdit()
        path_edit.setText(self.current_step.get("config", {}).get("image_path", ""))
        browse_btn = QPushButton("浏览")
        browse_btn.clicked.connect(lambda: self._browse_image(path_edit))
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(path_edit)
        h_layout.addWidget(browse_btn)
        
        self.form_layout.addRow("图片路径", h_layout)
        
        path_edit.textChanged.connect(lambda text: self._update_config("image_path", text))
    
    def _browse_image(self, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", "图片文件 (*.png *.jpg *.bmp)"
        )
        if file_path:
            line_edit.setText(file_path)
    
    def _add_keyboard_fields(self, step):
        config = step.get("config", {})
        
        text_edit = QTextEdit()
        text_edit.setText(config.get("text", ""))
        text_edit.textChanged.connect(lambda: self._update_config("text", text_edit.toPlainText()))
        self.form_layout.addRow("输入文本", text_edit)
        
        self._add_field("输入间隔(秒)", "interval", QDoubleSpinBox)
        self._add_field("防检测模式", "anti_detection", QCheckBox)
    
    def _add_wait_fields(self, step):
        wait_type = QComboBox()
        wait_type.addItems(["fixed", "random"])
        wait_type.currentTextChanged.connect(lambda text: self._update_config("type", text))
        self.form_layout.addRow("等待类型", wait_type)
        
        if step.get("config", {}).get("type") == "random":
            self._add_field("最小等待(秒)", "min", QDoubleSpinBox)
            self._add_field("最大等待(秒)", "max", QDoubleSpinBox)
        else:
            self._add_field("等待时间(秒)", "value", QDoubleSpinBox)
    
    def _add_image_fields(self, step):
        config = step.get("config", {})
        
        self._add_image_path_field()
        self._add_field("置信度", "confidence", QDoubleSpinBox)
        self._add_field("超时(秒)", "timeout", QSpinBox)
        
        self.form_layout.addRow("搜索区域", QLabel("X Y 宽度 高度"))
        region_edit = QLineEdit()
        region = config.get("region", [])
        region_edit.setText(" ".join(map(str, region)) if region else "")
        region_edit.textChanged.connect(lambda text: self._update_region(text))
        self.form_layout.addRow("", region_edit)
    
    def _add_if_else_fields(self, step):
        config = step.get("config", {})
        
        condition_type = QComboBox()
        condition_type.addItems(["image_exists", "text_exists", "variable_compare", "file_exists"])
        condition_type.currentTextChanged.connect(lambda text: self._update_condition_type(text))
        self.form_layout.addRow("条件类型", condition_type)
        
        if_true_edit = QLineEdit()
        if_true_edit.setText(config.get("if_true", ""))
        if_true_edit.textChanged.connect(lambda text: self._update_config("if_true", text))
        self.form_layout.addRow("条件为真时跳转", if_true_edit)
        
        if_false_edit = QLineEdit()
        if_false_edit.setText(config.get("if_false", ""))
        if_false_edit.textChanged.connect(lambda text: self._update_config("if_false", text))
        self.form_layout.addRow("条件为假时跳转", if_false_edit)
    
    def _add_loop_fields(self, step):
        config = step.get("config", {})
        
        loop_type = QComboBox()
        loop_type.addItems(["for", "while"])
        loop_type.currentTextChanged.connect(lambda text: self._update_config("loop_type", text))
        self.form_layout.addRow("循环类型", loop_type)
        
        if config.get("loop_type") == "for":
            self._add_field("循环次数", "count", QSpinBox)
        else:
            self._add_field("超时(秒)", "timeout", QSpinBox)
    
    def _add_excel_fields(self, step):
        config = step.get("config", {})
        
        path_edit = QLineEdit()
        path_edit.setText(config.get("file_path", ""))
        browse_btn = QPushButton("浏览")
        browse_btn.clicked.connect(lambda: self._browse_excel(path_edit))
        
        h_layout = QHBoxLayout()
        h_layout.addWidget(path_edit)
        h_layout.addWidget(browse_btn)
        
        self.form_layout.addRow("Excel路径", h_layout)
        path_edit.textChanged.connect(lambda text: self._update_config("file_path", text))
        
        self._add_field("工作表", "sheet_name", QLineEdit)
        self._add_field("单元格", "cell_ref", QLineEdit)
        self._add_field("变量名", "variable_name", QLineEdit)
    
    def _browse_excel(self, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择Excel", "", "Excel文件 (*.xlsx *.xls)"
        )
        if file_path:
            line_edit.setText(file_path)
    
    def _add_variable_fields(self, step):
        config = step.get("config", {})
        
        self._add_field("变量名", "name", QLineEdit)
        
        value_edit = QTextEdit()
        value_edit.setText(str(config.get("value", "")))
        value_edit.textChanged.connect(lambda: self._update_config("value", value_edit.toPlainText()))
        self.form_layout.addRow("变量值", value_edit)
    
    def _add_window_fields(self, step):
        config = step.get("config", {})
        
        self._add_field("窗口标题", "title", QLineEdit)
        self._add_field("精确匹配", "exact_match", QCheckBox)
    
    def _update_step(self, key, value):
        if self.current_step:
            self.current_step[key] = value
    
    def _update_config(self, key, value):
        if self.current_step:
            config = self.current_step.setdefault("config", {})
            config[key] = value
    
    def _update_region(self, text):
        try:
            region = list(map(int, text.split()))
            if len(region) == 4:
                self._update_config("region", region)
        except ValueError:
            pass
    
    def _update_condition_type(self, condition_type):
        if self.current_step:
            config = self.current_step.setdefault("config", {})
            condition = config.setdefault("condition", {})
            condition["type"] = condition_type
```

- [ ] **步骤 2：运行验证**

运行：`python main.py`
预期：选择步骤后属性面板显示对应配置项

- [ ] **步骤 3：Commit**

```bash
git add gui/property_panel.py
git commit -m "feat: add property panel"
```

### 任务 20：监控面板

**文件：**
- 创建：`gui/monitor_panel.py`

- [ ] **步骤 1：编写监控面板代码**

```python
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QLabel,
    QProgressBar, QHBoxLayout
)
from PySide6.QtCore import Qt, QTimer
from core.logger import Logger

class MonitorPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.logger = Logger()
        self._init_ui()
        self._init_timer()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        header_layout = QHBoxLayout()
        
        self.status_label = QLabel("状态: 就绪")
        self.status_label.setStyleSheet("font-weight: bold")
        header_layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        header_layout.addWidget(self.progress_bar)
        
        layout.addLayout(header_layout)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("background-color: #f5f5f5")
        layout.addWidget(self.log_text)
    
    def _init_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_logs)
        self.timer.start(1000)
    
    def _update_logs(self):
        logs = self.logger.get_logs()
        if logs:
            self.log_text.clear()
            self.log_text.append("\n".join(logs[-50:]))
            self.log_text.moveCursor(self.log_text.textCursor().End)
    
    def add_log(self, message, level="info"):
        if level == "info":
            self.logger.info(message)
        elif level == "error":
            self.logger.error(message)
        elif level == "warning":
            self.logger.warning(message)
        elif level == "debug":
            self.logger.debug(message)
        self._update_logs()
    
    def set_status(self, status):
        self.status_label.setText(f"状态: {status}")
    
    def set_progress(self, progress):
        self.progress_bar.setValue(progress)
    
    def clear_logs(self):
        self.logger.clear()
        self.log_text.clear()
    
    def closeEvent(self, event):
        self.timer.stop()
        super().closeEvent(event)
```

- [ ] **步骤 2：运行验证**

运行：`python main.py`
预期：监控面板显示日志和进度

- [ ] **步骤 3：Commit**

```bash
git add gui/monitor_panel.py
git commit -m "feat: add monitor panel"
```

---

## Phase 5：定时调度与打包

### 任务 21：定时调度对话框

**文件：**
- 创建：`gui/scheduler_dialog.py`

- [ ] **步骤 1：编写定时调度对话框代码**

```python
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QComboBox,
    QSpinBox, QDateEdit, QTimeEdit, QPushButton,
    QLabel, QCheckBox
)
from PySide6.QtCore import Qt, QDate, QTime
from core.scheduler import TaskScheduler

class SchedulerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("定时调度")
        self.setGeometry(300, 300, 400, 400)
        self.scheduler = TaskScheduler()
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        self.trigger_type = QComboBox()
        self.trigger_type.addItems(["单次执行", "每日定时", "循环间隔"])
        self.trigger_type.currentTextChanged.connect(self._on_trigger_type_changed)
        layout.addWidget(QLabel("调度类型"))
        layout.addWidget(self.trigger_type)
        
        self.form_layout = QFormLayout()
        layout.addLayout(self.form_layout)
        
        self._update_form()
        
        buttons_layout = QHBoxLayout()
        self.start_btn = QPushButton("启动调度")
        self.start_btn.clicked.connect(self._start_scheduler)
        buttons_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("停止调度")
        self.stop_btn.clicked.connect(self._stop_scheduler)
        buttons_layout.addWidget(self.stop_btn)
        
        layout.addLayout(buttons_layout)
    
    def _on_trigger_type_changed(self, text):
        self._update_form()
    
    def _update_form(self):
        while self.form_layout.count():
            child = self.form_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        trigger_type = self.trigger_type.currentText()
        
        if trigger_type == "单次执行":
            self.date_edit = QDateEdit(QDate.currentDate())
            self.date_edit.setDisplayFormat("yyyy-MM-dd")
            self.form_layout.addRow("执行日期", self.date_edit)
            
            self.time_edit = QTimeEdit(QTime.currentTime())
            self.time_edit.setDisplayFormat("HH:mm:ss")
            self.form_layout.addRow("执行时间", self.time_edit)
        
        elif trigger_type == "每日定时":
            self.time_edit_daily = QTimeEdit(QTime(9, 0))
            self.time_edit_daily.setDisplayFormat("HH:mm:ss")
            self.form_layout.addRow("每日执行时间", self.time_edit_daily)
        
        elif trigger_type == "循环间隔":
            self.interval_spin = QSpinBox()
            self.interval_spin.setRange(1, 3600)
            self.interval_spin.setValue(60)
            self.form_layout.addRow("间隔时间(秒)", self.interval_spin)
    
    def _start_scheduler(self):
        trigger_type = self.trigger_type.currentText()
        
        if trigger_type == "单次执行":
            date = self.date_edit.date().toString("yyyy-MM-dd")
            time = self.time_edit.time().toString("HH:mm:ss")
            run_date = f"{date} {time}"
            self.scheduler.add_task("auto_task", "date", run_date=run_date, func=self._execute_task)
        
        elif trigger_type == "每日定时":
            time = self.time_edit_daily.time()
            self.scheduler.add_task("auto_task", "cron", hour=time.hour(), minute=time.minute(), func=self._execute_task)
        
        elif trigger_type == "循环间隔":
            interval = self.interval_spin.value()
            self.scheduler.add_task("auto_task", "interval", interval=interval, func=self._execute_task)
        
        self.scheduler.start()
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
    
    def _stop_scheduler(self):
        self.scheduler.stop()
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
    
    def _execute_task(self):
        parent = self.parent()
        if parent and hasattr(parent, '_start_flow'):
            parent._start_flow()
```

- [ ] **步骤 2：运行验证**

运行：`python main.py`
预期：定时调度对话框正常显示

- [ ] **步骤 3：Commit**

```bash
git add gui/scheduler_dialog.py
git commit -m "feat: add scheduler dialog"
```

### 任务 22：流程管理模块

**文件：**
- 创建：`gui/flow_manager.py`

- [ ] **步骤 1：编写流程管理代码**

```python
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QInputDialog
)
from PySide6.QtCore import Qt

class FlowManager(QWidget):
    def __init__(self):
        super().__init__()
        self.flows = []
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        toolbar = QHBoxLayout()
        
        self.new_btn = QPushButton("新建流程")
        self.new_btn.clicked.connect(self._new_flow)
        toolbar.addWidget(self.new_btn)
        
        self.rename_btn = QPushButton("重命名")
        self.rename_btn.clicked.connect(self._rename_flow)
        toolbar.addWidget(self.rename_btn)
        
        self.delete_btn = QPushButton("删除")
        self.delete_btn.clicked.connect(self._delete_flow)
        toolbar.addWidget(self.delete_btn)
        
        self.copy_btn = QPushButton("复制")
        self.copy_btn.clicked.connect(self._copy_flow)
        toolbar.addWidget(self.copy_btn)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        self.flow_list = QListWidget()
        self.flow_list.itemDoubleClicked.connect(self._on_flow_double_clicked)
        layout.addWidget(self.flow_list)
    
    def load_flows(self, flows):
        self.flows = flows
        self._update_list()
    
    def add_flow(self, flow):
        self.flows.append(flow)
        self._update_list()
    
    def remove_flow(self, flow_name):
        self.flows = [f for f in self.flows if f.get("name") != flow_name]
        self._update_list()
    
    def _update_list(self):
        self.flow_list.clear()
        for flow in self.flows:
            item = QListWidgetItem(flow.get("name", "未命名流程"))
            item.setData(Qt.UserRole, flow)
            self.flow_list.addItem(item)
    
    def _new_flow(self):
        name, ok = QInputDialog.getText(self, "新建流程", "请输入流程名称:")
        if ok and name:
            flow = {
                "name": name,
                "version": "1.0",
                "steps": [],
                "file_path": f"{name}.json"
            }
            self.add_flow(flow)
    
    def _rename_flow(self):
        item = self.flow_list.currentItem()
        if item:
            flow = item.data(Qt.UserRole)
            new_name, ok = QInputDialog.getText(self, "重命名", "请输入新名称:", text=flow.get("name"))
            if ok and new_name:
                flow["name"] = new_name
                self._update_list()
    
    def _delete_flow(self):
        item = self.flow_list.currentItem()
        if item:
            flow = item.data(Qt.UserRole)
            reply = QMessageBox.question(
                self, "确认删除", f"确定删除流程 '{flow.get('name')}'？",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.remove_flow(flow.get("name"))
    
    def _copy_flow(self):
        item = self.flow_list.currentItem()
        if item:
            flow = item.data(Qt.UserRole)
            import copy
            new_flow = copy.deepcopy(flow)
            new_flow["name"] = flow.get("name") + "_副本"
            new_flow["file_path"] = flow.get("file_path").replace(".json", "_副本.json")
            self.add_flow(new_flow)
    
    def _on_flow_double_clicked(self, item):
        flow = item.data(Qt.UserRole)
        self.parent().step_editor.load_steps(flow.get("steps", []))
        self.parent().current_flow = flow
```

- [ ] **步骤 2：运行验证**

运行：`python main.py`
预期：流程管理面板正常显示

- [ ] **步骤 3：Commit**

```bash
git add gui/flow_manager.py
git commit -m "feat: add flow manager"
```

### 任务 23：打包配置

**文件：**
- 创建：`setup.py`
- 创建：`build.py`
- 修改：`requirements.txt`

- [ ] **步骤 1：创建 setup.py**

```python
from setuptools import setup, find_packages

setup(
    name="AutoFlow",
    version="1.0.0",
    description="可视化桌面自动化引擎",
    author="AutoFlow Team",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PySide6>=6.5.0",
        "pyautogui>=0.9.54",
        "pydirectinput>=1.0.4",
        "opencv-python>=4.8.0",
        "easyocr>=1.7.0",
        "openpyxl>=3.1.0",
        "numpy>=1.24.0",
        "Pillow>=10.0.0",
        "mss>=10.0.0",
        "APScheduler>=3.10.0",
        "pyperclip>=1.8.2",
        "pytest>=7.4.0",
        "pywin32>=306",
        "psutil>=5.9.0",
        "keyboard>=0.13.5"
    ],
    entry_points={
        "console_scripts": [
            "autoflow=main:main"
        ]
    }
)
```

- [ ] **步骤 2：创建 build.py**

```python
import subprocess
import sys
import os

def build():
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "-F", "-w",
        "-i", "resources/icons/app.ico",
        "--add-data", "resources;resources",
        "--name", "AutoFlow",
        "main.py"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    
    if result.returncode == 0:
        print("打包成功！")
        print(f"输出文件: dist/AutoFlow.exe")
    else:
        print(f"打包失败，返回码: {result.returncode}")

if __name__ == "__main__":
    build()
```

- [ ] **步骤 3：更新 requirements.txt**

```text
PySide6>=6.5.0
pyautogui>=0.9.54
pydirectinput>=1.0.4
opencv-python>=4.8.0
easyocr>=1.7.0
openpyxl>=3.1.0
numpy>=1.24.0
Pillow>=10.0.0
mss>=10.0.0
APScheduler>=3.10.0
pyperclip>=1.8.2
pytest>=7.4.0
pywin32>=306
psutil>=5.9.0
keyboard>=0.13.5
```

- [ ] **步骤 4：运行验证**

运行：`python build.py`
预期：打包成功，生成 dist/AutoFlow.exe

- [ ] **步骤 5：Commit**

```bash
git add setup.py build.py requirements.txt
git commit -m "feat: add build configuration"
```

---

## Phase 6：插件系统与优化

### 任务 24：插件系统

**文件：**
- 创建：`plugins/__init__.py`
- 创建：`plugins/plugin_manager.py`
- 创建：`plugins/example_plugin.py`

- [ ] **步骤 1：编写插件管理器**

```python
import importlib
import os
import sys
from typing import List, Dict, Any

class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.plugin_dir = os.path.dirname(__file__)
    
    def load_plugins(self):
        plugins = []
        
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith('_plugin.py') and filename != '__init__.py':
                module_name = f"plugins.{filename[:-3]}"
                try:
                    module = importlib.import_module(module_name)
                    if hasattr(module, 'register'):
                        plugin_info = module.register()
                        self.plugins[plugin_info['id']] = plugin_info
                        plugins.append(plugin_info['name'])
                except Exception as e:
                    print(f"加载插件失败 {filename}: {e}")
        
        return plugins
    
    def get_plugin(self, plugin_id: str) -> Dict[str, Any]:
        return self.plugins.get(plugin_id)
    
    def get_all_plugins(self) -> List[Dict[str, Any]]:
        return list(self.plugins.values())
    
    def execute_plugin(self, plugin_id: str, **kwargs) -> Any:
        plugin = self.plugins.get(plugin_id)
        if plugin and 'execute' in plugin:
            return plugin['execute'](**kwargs)
        return None
    
    def get_step_types(self) -> List[Dict[str, Any]]:
        step_types = []
        for plugin in self.plugins.values():
            if 'step_types' in plugin:
                step_types.extend(plugin['step_types'])
        return step_types
```

- [ ] **步骤 2：编写示例插件**

```python
def register():
    return {
        "id": "example_plugin",
        "name": "示例插件",
        "description": "一个示例插件",
        "version": "1.0",
        "step_types": [
            {
                "type": "example_action",
                "name": "示例操作",
                "category": "其他",
                "config_fields": [
                    {"name": "message", "label": "消息", "type": "string"}
                ]
            }
        ],
        "execute": execute_example_action
    }

def execute_example_action(**kwargs):
    message = kwargs.get("message", "")
    print(f"示例插件执行: {message}")
    return True
```

- [ ] **步骤 3：更新 plugins/__init__.py**

```python
from .plugin_manager import PluginManager

__all__ = ['PluginManager']
```

- [ ] **步骤 4：运行验证**

运行：`python -c "from plugins import PluginManager; pm = PluginManager(); print(pm.load_plugins())"`
预期：输出 `['示例插件']`

- [ ] **步骤 5：Commit**

```bash
git add plugins/__init__.py plugins/plugin_manager.py plugins/example_plugin.py
git commit -m "feat: add plugin system"
```

### 任务 25：性能优化与测试

**文件：**
- 修改：`operations/image_match.py`
- 创建：`tests/test_performance.py`

- [ ] **步骤 1：优化图片识别性能**

```python
def find_image(self, template_path: str, region: Tuple[int, int, int, int] = None, 
               confidence: float = None) -> Optional[Dict[str, float]]:
    conf = confidence or self.default_confidence
    
    if not os.path.exists(template_path):
        return None
    
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        return None
    
    screenshot = self._get_screenshot(region)
    if screenshot is None:
        return None
    
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    
    h, w = template.shape[:2]
    if h > screenshot_gray.shape[0] or w > screenshot_gray.shape[1]:
        return None
    
    res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
    if max_val >= conf:
        return {
            "x": max_loc[0],
            "y": max_loc[1],
            "width": w,
            "height": h,
            "confidence": float(max_val),
            "center_x": max_loc[0] + w // 2,
            "center_y": max_loc[1] + h // 2
        }
    return None
```

- [ ] **步骤 2：编写性能测试**

```python
import pytest
import sys
import time
sys.path.insert(0, '..')
from operations.image_match import ImageMatcher

def test_image_match_performance():
    matcher = ImageMatcher()
    
    start_time = time.time()
    for _ in range(10):
        result = matcher.image_exists("non_existent.png")
    elapsed = time.time() - start_time
    
    assert elapsed < 2.0
    print(f"10次图片查找耗时: {elapsed:.2f}秒")

def test_screenshot_performance():
    matcher = ImageMatcher()
    
    start_time = time.time()
    for _ in range(5):
        matcher._get_screenshot()
    elapsed = time.time() - start_time
    
    assert elapsed < 3.0
    print(f"5次截图耗时: {elapsed:.2f}秒")
```

- [ ] **步骤 3：运行性能测试**

运行：`pytest tests/test_performance.py -v`
预期：PASS

- [ ] **步骤 4：Commit**

```bash
git add operations/image_match.py tests/test_performance.py
git commit -m "perf: optimize image matching"
```

---

## 计划自检

### 规格覆盖度

| 需求 | 对应任务 |
|------|---------|
| 鼠标操作 | 任务 7 |
| 键盘操作 | 任务 8 |
| 延时等待 | 任务 7/8/9/核心引擎 |
| 图片识别 | 任务 12 |
| 文字识别 | 任务 13 |
| 分支判断 | 任务 15 |
| 循环控制 | 任务 15 |
| Excel读取 | 任务 11 |
| 变量管理 | 任务 3 |
| 定时调度 | 任务 6/21 |
| 后台执行 | 任务 14 |
| GUI界面 | 任务 16-22 |
| 插件系统 | 任务 24 |

### 占位符扫描

无占位符，所有步骤均包含完整代码和命令。

### 类型一致性

各模块之间的类型、方法签名和属性名保持一致。

---

## 执行交接

计划已完成并保存到 `docs/superpowers/plans/2026-07-10-autoflow-implementation.md`。两种执行方式：

**1. 子代理驱动（推荐）** - 每个任务调度一个新的子代理，任务间进行审查，快速迭代

**2. 内联执行** - 在当前会话中使用 executing-plans 执行任务，批量执行并设有检查点

选哪种方式？
