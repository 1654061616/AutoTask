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