import pytest
import sys

def test_core_modules():
    from core.logger import Logger
    from core.variables import VariableManager
    from core.parser import FlowParser
    from core.engine import FlowEngine
    from core.scheduler import TaskScheduler
    from core.flow_manager import FlowManager
    
    logger = Logger()
    vm = VariableManager()
    parser = FlowParser()
    engine = FlowEngine()
    scheduler = TaskScheduler()
    fm = FlowManager()
    
    assert logger is not None
    assert vm is not None
    assert parser is not None
    assert engine is not None
    assert scheduler is not None
    assert fm is not None

def test_operations_modules():
    from operations.mouse import MouseOperations
    from operations.keyboard import KeyboardOperations
    from operations.file_operations import FileOperations
    from operations.clipboard import ClipboardOperations
    from operations.excel import ExcelOperations
    from operations.image_recognition import ImageRecognition
    from operations.condition import ConditionEvaluator
    
    mouse = MouseOperations()
    keyboard = KeyboardOperations()
    file_ops = FileOperations()
    clipboard = ClipboardOperations()
    excel = ExcelOperations()
    image_rec = ImageRecognition()
    condition = ConditionEvaluator()
    
    assert mouse is not None
    assert keyboard is not None
    assert file_ops is not None
    assert clipboard is not None
    assert excel is not None
    assert image_rec is not None
    assert condition is not None

def test_gui_modules():
    from gui.toolbox_panel import ToolboxPanel
    from gui.step_editor import StepEditor
    from gui.properties_panel import PropertiesPanel
    from gui.monitor_panel import MonitorPanel
    
    toolbox = ToolboxPanel()
    step_editor = StepEditor()
    properties = PropertiesPanel()
    monitor = MonitorPanel()
    
    assert toolbox is not None
    assert step_editor is not None
    assert properties is not None
    assert monitor is not None

def test_plugin_system():
    from plugins.plugin_manager import PluginManager
    
    pm = PluginManager()
    assert pm is not None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])