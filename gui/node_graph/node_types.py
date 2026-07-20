"""
节点类型定义 — 定义所有可用的节点类型及其分类
"""

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