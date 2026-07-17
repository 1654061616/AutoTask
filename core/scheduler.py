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
        
        if trigger_type == "immediate":
            if func:
                func()
            return True
        elif trigger_type == "interval":
            seconds = kwargs.get('interval', 60)
            trigger = IntervalTrigger(seconds=seconds)
        elif trigger_type == "cron":
            cron_expression = kwargs.get('cron_expression', '0 9 * * *')
            parts = cron_expression.split()
            if len(parts) == 5:
                trigger = CronTrigger(
                    minute=parts[0], hour=parts[1], day=parts[2],
                    month=parts[3], day_of_week=parts[4]
                )
            elif len(parts) == 7:
                trigger = CronTrigger(
                    second=parts[0], minute=parts[1], hour=parts[2],
                    day=parts[3], month=parts[4], day_of_week=parts[5],
                    year=parts[6]
                )
            else:
                return False
        elif trigger_type == "date":
            run_date = kwargs.get('run_date')
            if isinstance(run_date, str):
                run_date = datetime.datetime.fromisoformat(run_date)
            if run_date is None:
                run_date = datetime.datetime.now()
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