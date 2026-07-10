import os
import sys
import importlib
import pkgutil
from typing import Dict, Any, List

class PluginManager:
    def __init__(self):
        self.plugins: Dict[str, Any] = {}
        self.plugin_dirs = ["plugins"]
    
    def load_plugins(self):
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
        return self.plugins.get(name)
    
    def get_all_plugins(self) -> List[Dict[str, Any]]:
        return list(self.plugins.values())
    
    def get_plugins_by_category(self, category: str) -> List[Dict[str, Any]]:
        return [p for p in self.plugins.values() if p.get("category") == category]
    
    def unload_plugin(self, name: str):
        if name in self.plugins:
            del self.plugins[name]
    
    def reload_plugins(self):
        self.plugins.clear()
        self.load_plugins()