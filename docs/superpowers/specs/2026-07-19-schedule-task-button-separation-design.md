# 定时按钮与任务执行按钮拆分设计

## 目标
将定时任务按钮与手动任务执行按钮完全解耦。
单向影响：定时执行时禁用手动开始按钮（防止重复执行），手动执行不影响定时按钮。

## 当前问题
1. 定时按钮是同一个按钮切换文字和信号，使用 disconnect/reconnect，逻辑脆弱
2. _on_start_scheduled() 直接调用 self.on_run_flow()，影响 start/stop 按钮状态
3. 立即执行1次触发类型等同于点击开始当前任务
4. task_status_label 状态管理混乱

## 设计方案

### 一、SchedulePanel 按钮改造
**文件**：gui/main_window/schedule_panel.py
- 新增 stop_scheduled_btn（默认隐藏），新增 stop_scheduled 信号
- 新增 set_schedule_running() / set_schedule_stopped() 方法
- start_scheduled_btn 始终绑定 start_scheduled 信号，不再 disconnect/reconnect
- 两个按钮并列互斥显示

### 二、ScheduleHandlerMixin 改造
**文件**：gui/main_window/schedule_handler.py
- _on_start_scheduled()：调用 set_schedule_running()；立即执行1次不再调用 on_run_flow()；定时回调改为 _execute_scheduled_task()
- _on_stop_scheduled()：调用 set_schedule_stopped()
- 新增 _execute_scheduled_task()：复用核心执行逻辑，执行前禁用 start_task_btn（防止重复启动），执行完成后恢复 start_task_btn 状态
- 新增 _update_task_status_label()：根据两个标志位组合显示

### 三、TaskExecutorMixin 改造
**文件**：gui/main_window/task_executor.py
- on_run_flow() / on_stop_flow() 中 status_label 改为 _update_task_status_label()
- 手动执行时：禁用 start_task_btn，启用 stop_task_btn（不变）
- 手动执行完成后：恢复 start_task_btn（不变）
- 手动执行不影响定时按钮

### 四、ui_builder.py 信号连接
**文件**：gui/main_window/ui_builder.py
- 新增 self.schedule_panel.stop_scheduled.connect(self._on_stop_scheduled)

### 五、task_status_label 状态
| 手动执行中 | 定时中 | 定时正执行 | 显示        |
|-----------|--------|-----------|-----------|
| 否 | 否 | 否 | 已停止       |
| 是 | 否 | 否 | 执行中       |
| 否 | 是 | 否 | 定时中       |
| 否 | 是 | 是 | 定时任务执行中   |
| 是 | 是 | / | 定时中；手动执行中 |

### 六、按钮互斥规则
- 定时执行中 → 禁用 start_task_btn（不可重复启动），启用 stop_task_btn（可手动停止）
- 手动执行中 → 不影响定时按钮
- 定时执行完成后 → 恢复 start_task_btn 为定时执行前的状态

## 涉及文件
- gui/main_window/schedule_panel.py
- gui/main_window/schedule_handler.py
- gui/main_window/task_executor.py
- gui/main_window/ui_builder.py
