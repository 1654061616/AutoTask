import pytest
import sys
sys.path.insert(0, '..')
from core.scheduler import TaskScheduler

def test_scheduler_initialization():
    scheduler = TaskScheduler()
    assert scheduler is not None

def test_add_task():
    scheduler = TaskScheduler()
    def test_func():
        pass
    scheduler.add_task("test_task", "interval", interval=60, func=test_func)
    assert "test_task" in scheduler.tasks

def test_remove_task():
    scheduler = TaskScheduler()
    def test_func():
        pass
    scheduler.add_task("test_task", "interval", interval=60, func=test_func)
    scheduler.remove_task("test_task")
    assert "test_task" not in scheduler.tasks

def test_start_stop():
    scheduler = TaskScheduler()
    scheduler.start()
    assert scheduler.is_running
    scheduler.stop()
    assert not scheduler.is_running