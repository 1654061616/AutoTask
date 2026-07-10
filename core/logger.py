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