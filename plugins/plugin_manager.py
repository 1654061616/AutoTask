"""
插件管理器 — 动态加载和管理插件模块
"""
import os
import sys
import importlib
import pkgutil
from typing import Dict, Any, List

class PluginManager:
    """插件管理器，支持动态加载、卸载和按分类获取插件"""

    def __init__(self):
        self.plugins: Dict[str, Any] = {}
        self.plugin_dirs = ["plugins"]

    def load_plugins(self):
        """扫描插件目录并加载所有包含 register 函数的插件包"""
        for plugin_dir in self.plugin_dirs:
            if not os.path.isdir(plugin_dir):
                continue

            sys.path.insert(0, plugin_dir)

            for _, name, is_pkg in pkgutil.iter_modules([plugin_dir]):
                if is_pkg:
                    try:
                        module = importlib.import_module(name)
                        if hasattr(module, 'register'):
                            plugin_info = module.register()
                            self.plugins[name] = plugin_info
                    except Exception as e:
                        print(f"加载插件 {name} 失败: {e}")

            sys.path.pop(0)

    def get_plugin(self, name: str) -> Any:
        """获取指定插件"""
        return self.plugins.get(name)

    def get_all_plugins(self) -> List[Dict[str, Any]]:
        """获取所有已加载插件"""
        return list(self.plugins.values())

    def get_plugins_by_category(self, category: str) -> List[Dict[str, Any]]:
        """按分类获取插件"""
        return [p for p in self.plugins.values() if p.get("category") == category]

    def unload_plugin(self, name: str):
        """卸载指定插件"""
        if name in self.plugins:
            del self.plugins[name]

    def reload_plugins(self):
        """重新加载所有插件"""
        self.plugins.clear()
        self.load_plugins()