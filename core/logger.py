"""
日志记录器 — 负责日志的存储、输出和回调通知
"""
import logging
import time
from typing import List, Callable

class Logger:
    """日志管理器，支持多级别日志记录和回调通知"""

    def __init__(self):
        self.logs: List[str] = []                       # 日志列表
        self.log_format = "%Y-%m-%d %H:%M:%S"           # 时间戳格式
        self.callbacks: List[Callable[[str], None]] = [] # 日志回调函数列表

    def add_callback(self, callback: Callable[[str], None]):
        """添加日志回调函数，当有新日志时会调用"""
        if callback not in self.callbacks:
            self.callbacks.append(callback)

    def remove_callback(self, callback: Callable[[str], None]):
        """移除日志回调函数"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def _add_log(self, level: str, message: str):
        """内部方法：添加一条日志并通知所有回调"""
        timestamp = time.strftime(self.log_format)
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_entry)
        print(log_entry)
        for callback in self.callbacks:
            try:
                callback(log_entry)
            except Exception:
                pass

    def info(self, message: str):
        """记录 INFO 级别日志"""
        self._add_log("INFO", message)

    def error(self, message: str):
        """记录 ERROR 级别日志"""
        self._add_log("ERROR", message)

    def warning(self, message: str):
        """记录 WARNING 级别日志"""
        self._add_log("WARNING", message)

    def debug(self, message: str):
        """记录 DEBUG 级别日志"""
        self._add_log("DEBUG", message)

    def get_logs(self) -> List[str]:
        """获取所有日志"""
        return self.logs

    def clear(self):
        """清空日志"""
        self.logs.clear()

    def get_last_log(self) -> str:
        """获取最后一条日志"""
        return self.logs[-1] if self.logs else ""