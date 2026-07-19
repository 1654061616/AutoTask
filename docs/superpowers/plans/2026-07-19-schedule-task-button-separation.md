# 定时按钮与任务执行按钮拆分 实现计划

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 逐任务实现此计划。步骤使用复选框（`- [ ]`）语法来跟踪进度。

**目标：** 将定时任务按钮与手动任务执行按钮完全解耦，单向影响（定时执行时禁用手动开始按钮，手动执行不影响定时按钮）

**架构：** 在 SchedulePanel 中新增独立的 stop_scheduled_btn 和 stop_scheduled 信号，消除 disconnect/reconnect 模式；在 ScheduleHandlerMixin 中拆分定时回调逻辑；在 TaskExecutorMixin 中引入状态标志位，统一通过 _update_task_status_label() 管理状态显示。

**技术栈：** PySide6, Python 3

---

### 任务 1：SchedulePanel 按钮改造

**文件：**
- 修改：`gui/main_window/schedule_panel.py`

- [ ] **步骤 1：新增 stop_scheduled 信号和 stop_scheduled_btn**

在 `SchedulePanel` 类定义中，在 `start_scheduled` 信号下方新增 `stop_scheduled` 信号：

```python
class SchedulePanel(QWidget):
    schedule_changed = Signal()
    start_scheduled = Signal()
    stop_scheduled = Signal()
```

- [ ] **步骤 2：在 _init_ui 中新增 stop_scheduled_btn 并隐藏**

在 `_init_ui` 方法中，`start_scheduled_btn` 之后新增 `stop_scheduled_btn`：

```python
        self.start_scheduled_btn = QPushButton("▶ 开始定时")
        self.start_scheduled_btn.setStyleSheet(Styles.schedule_btn_start())
        self.start_scheduled_btn.clicked.connect(lambda: self.start_scheduled.emit())
        trigger_layout.addWidget(self.start_scheduled_btn)
        self.stop_scheduled_btn = QPushButton("■ 停止定时")
        self.stop_scheduled_btn.setStyleSheet(Styles.schedule_btn_stop())
        self.stop_scheduled_btn.clicked.connect(lambda: self.stop_scheduled.emit())
        self.stop_scheduled_btn.hide()
        trigger_layout.addWidget(self.stop_scheduled_btn)
        trigger_layout.addStretch()
```

- [ ] **步骤 3：新增 set_schedule_running() 方法**

在 `SchedulePanel` 类中添加：

```python
    def set_schedule_running(self):
        self.start_scheduled_btn.hide()
        self.stop_scheduled_btn.show()

    def set_schedule_stopped(self):
        self.stop_scheduled_btn.hide()
        self.start_scheduled_btn.show()
```

- [ ] **步骤 4：Commit**

```bash
git add gui/main_window/schedule_panel.py
git commit -m "feat: SchedulePanel 新增 stop_scheduled_btn 和互斥显示方法"
```

---

### 任务 2：ScheduleHandlerMixin 改造

**文件：**
- 修改：`gui/main_window/schedule_handler.py`

- [ ] **步骤 1：重写 _on_start_scheduled() — 消除 disconnect/reconnect，拆分立即执行逻辑**

替换 `_on_start_scheduled` 方法（第 16-50 行）：

```python
    @Slot()
    def _on_start_scheduled(self):
        from core.scheduler import TaskScheduler

        if self.current_flow is None:
            QMessageBox.warning(self, "启动失败", "请先选择一个任务")
            return

        config = self.schedule_panel.get_config()
        if config is None:
            return

        trigger_type = config["trigger_type"]
        params = config["params"]

        if trigger_type == "immediate":
            QMessageBox.information(self, "定时任务", "立即执行任务已启动")
            self.on_run_flow()
            return

        self.scheduler = TaskScheduler()
        self.scheduler.add_task(
            task_id=self.current_flow.get("id", "scheduled"),
            name=self.current_flow.get("name", "定时任务"),
            trigger_type=trigger_type,
            func=lambda: self._execute_scheduled_task(),
            **params
        )
        self.scheduler.start()
        self.log_panel.append(f"定时任务已启动: {trigger_type}")
        self._update_task_status_label()

        self.schedule_panel.set_schedule_running()
```

- [ ] **步骤 2：新增 _execute_scheduled_task() 方法**

在 `_on_start_scheduled` 之后添加：

```python
    def _execute_scheduled_task(self):
        """定时回调：执行任务，执行前禁用start_task_btn，执行后恢复"""
        self._is_scheduled_executing = True
        self._update_task_status_label()

        self.start_task_btn.setEnabled(False)
        self.stop_task_btn.setEnabled(True)

        self.on_run_flow()

    def _on_scheduled_task_completed(self):
        """定时任务执行完成后的回调：恢复 start_task_btn 状态"""
        self._is_scheduled_executing = False
        self._update_task_status_label()

        if not self._is_manual_executing:
            self.start_task_btn.setEnabled(True)
```

- [ ] **步骤 3：重写 _on_stop_scheduled() — 消除 disconnect/reconnect**

替换 `_on_stop_scheduled` 方法（第 52-63 行）：

```python
    def _on_stop_scheduled(self):
        if hasattr(self, 'scheduler') and self.scheduler:
            self.scheduler.stop()
            self.scheduler = None
        self.log_panel.append("定时任务已停止")
        self._update_task_status_label()

        self.schedule_panel.set_schedule_stopped()
```

- [ ] **步骤 4：新增 _update_task_status_label() 方法**

在 `_on_stop_scheduled` 之后添加：

```python
    def _update_task_status_label(self):
        is_scheduled = hasattr(self, 'scheduler') and self.scheduler is not None
        is_scheduled_executing = getattr(self, '_is_scheduled_executing', False)
        is_manual_executing = getattr(self, '_is_manual_executing', False)

        if is_manual_executing and is_scheduled:
            text = "定时中；手动执行中"
        elif is_scheduled_executing:
            text = "定时任务执行中"
        elif is_manual_executing:
            text = "执行中"
        elif is_scheduled:
            text = "定时中"
        else:
            text = "已停止"

        self.task_status_label.setText(text)
```

- [ ] **步骤 5：Commit**

```bash
git add gui/main_window/schedule_handler.py
git commit -m "feat: ScheduleHandlerMixin 消除 disconnect/reconnect，拆分定时执行逻辑"
```

---

### 任务 3：TaskExecutorMixin 改造

**文件：**
- 修改：`gui/main_window/task_executor.py`

- [ ] **步骤 1：_start_task() 中替换 status_label 为 _update_task_status_label()，新增标志位**

修改 `_start_task` 方法（第 33-35 行），将 `self.task_status_label.setText("执行中")` 替换为 `self._update_task_status_label()`，并在开头设置 `_is_manual_executing` 标志：

```python
    def _start_task(self, task, item=None):
        if item is None:
            item = self.task_tree.currentItem()
            if not item:
                return

        task["status"] = "执行中"
        self.current_flow = task
        item.setData(0, Qt.UserRole, task)
        self._update_status_widget(item, "执行中")

        self._is_manual_executing = True
        self._update_task_status_label()
        self.task_status_label.setStyleSheet(Styles.status_label(Colors.SUCCESS))
        self.status_label.setText("运行中...")
        self.log_panel.append(f"开始执行任务: {task['name']}")

        self.start_task_btn.setEnabled(False)
        self.stop_task_btn.setEnabled(True)
        # ... 剩余代码不变
```

- [ ] **步骤 2：_on_task_completed_slot() 中替换 status_label 为 _update_task_status_label()，清除标志位**

修改 `_on_task_completed_slot` 方法（第 72-96 行），将 `self.task_status_label.setText("已停止")` 替换为 `self._update_task_status_label()`，在方法开头清除 `_is_manual_executing`：

```python
    @Slot(bool, str)
    def _on_task_completed_slot(self, success: bool, error_message: str):
        self._is_manual_executing = False

        if self.current_flow:
            current_item = None
            for i in range(self.task_tree.topLevelItemCount()):
                item = self.task_tree.topLevelItem(i)
                if item.data(0, Qt.UserRole) == self.current_flow:
                    current_item = item
                    break

            if current_item:
                self.current_flow["status"] = "已停止"
                current_item.setData(0, Qt.UserRole, self.current_flow)
                self._update_status_widget(current_item, "已停止")
                self._update_task_status_label()
                self.task_status_label.setStyleSheet(Styles.status_label("#e74c3c"))

        if success:
            self.status_label.setText("任务执行完成")
            self.log_panel.append("任务执行完成")
        else:
            self.status_label.setText("任务执行异常")
            self.log_panel.append(f"任务执行异常: {error_message}")

        if not getattr(self, '_is_scheduled_executing', False):
            self.start_task_btn.setEnabled(True)
        self.stop_task_btn.setEnabled(False)
        self.flow_stopped.emit()

        if getattr(self, '_is_scheduled_executing', False):
            self._on_scheduled_task_completed()
```

- [ ] **步骤 3：_stop_task() 中替换 status_label 为 _update_task_status_label()，清除标志位**

修改 `_stop_task` 方法（第 107-121 行），将 `self.task_status_label.setText("已停止")` 替换为 `self._update_task_status_label()`，清除 `_is_manual_executing`：

```python
    def _stop_task(self, task, item=None):
        if item is None:
            item = self.task_tree.currentItem()
            if not item:
                return

        self._is_manual_executing = False
        self.engine.stop()
        task["status"] = "已停止"
        item.setData(0, Qt.UserRole, task)
        self._update_status_widget(item, "已停止")

        self._update_task_status_label()
        self.task_status_label.setStyleSheet(Styles.status_label("#e74c3c"))
        self.status_label.setText("已停止")
        self.log_panel.append(f"停止任务: {task['name']}")

        if not getattr(self, '_is_scheduled_executing', False):
            self.start_task_btn.setEnabled(True)
        self.stop_task_btn.setEnabled(False)
        self.flow_stopped.emit()
```

- [ ] **步骤 4：Commit**

```bash
git add gui/main_window/task_executor.py
git commit -m "feat: TaskExecutorMixin 使用 _update_task_status_label 统一状态管理"
```

---

### 任务 4：ui_builder.py 信号连接

**文件：**
- 修改：`gui/main_window/ui_builder.py`

- [ ] **步骤 1：新增 stop_scheduled 信号连接**

在 `create_central_widget` 方法中（约第 180 行），紧接 `self.schedule_panel.start_scheduled.connect(self._on_start_scheduled)` 之后添加：

```python
        self.schedule_panel = SchedulePanel()
        self.schedule_panel.start_scheduled.connect(self._on_start_scheduled)
        self.schedule_panel.stop_scheduled.connect(self._on_stop_scheduled)
```

- [ ] **步骤 2：Commit**

```bash
git add gui/main_window/ui_builder.py
git commit -m "feat: ui_builder 连接 stop_scheduled 信号"
```

---

### 任务 5：验证与测试

**文件：**
- 无新建文件

- [ ] **步骤 1：运行应用，手动测试以下场景**

启动应用并测试：

1. **手动执行**：点击"开始当前任务" → 确认 `task_status_label` 显示"执行中"，定时按钮不变
2. **手动停止**：点击"停止当前任务" → 确认 `task_status_label` 显示"已停止"
3. **启动定时**：点击"▶ 开始定时" → 确认按钮切换为"■ 停止定时"，`task_status_label` 显示"定时中"
4. **停止定时**：点击"■ 停止定时" → 确认按钮切换回"▶ 开始定时"，`task_status_label` 显示"已停止"
5. **定时执行中**：定时触发时 → 确认 `start_task_btn` 被禁用，`stop_task_btn` 可用
6. **定时执行完成后**：确认 `start_task_btn` 恢复为启用状态
7. **手动执行不影响定时**：手动执行时，定时按钮保持原状态

- [ ] **步骤 2：运行现有测试确保无回归**

```bash
python -m pytest tests/ -v
```

---

## 自检

### 1. 规格覆盖度

| 规格章节 | 对应任务 |
|---------|---------|
| 一、SchedulePanel 按钮改造（新增 stop_scheduled_btn，set_schedule_running/stopped） | 任务 1 |
| 二、ScheduleHandlerMixin 改造（_on_start_scheduled 不调 on_run_flow，_execute_scheduled_task，_on_stop_scheduled，_update_task_status_label） | 任务 2 |
| 三、TaskExecutorMixin 改造（on_run_flow/on_stop_flow 用 _update_task_status_label，手动执行不影响定时） | 任务 3 |
| 四、ui_builder.py 信号连接 | 任务 4 |
| 五、task_status_label 状态表 | 任务 2（_update_task_status_label） |
| 六、按钮互斥规则 | 任务 2 + 任务 3 |

### 2. 占位符扫描

- 无 "待定"、"TODO"、"后续实现"
- 所有代码步骤都有实际代码块
- 所有方法签名和属性名在任务间一致

### 3. 类型一致性

- `_is_scheduled_executing`：在 `ScheduleHandlerMixin._execute_scheduled_task()` 中设置，在 `TaskExecutorMixin._on_task_completed_slot()` 中读取 → 一致（Mixin 共享同一实例）
- `_is_manual_executing`：在 `TaskExecutorMixin._start_task()` 中设置，在 `_on_task_completed_slot()` 和 `_stop_task()` 中清除 → 一致
- `_on_scheduled_task_completed()`：在 `ScheduleHandlerMixin` 中定义，在 `TaskExecutorMixin._on_task_completed_slot()` 中调用 → 一致
- `_update_task_status_label()`：在 `ScheduleHandlerMixin` 中定义，在 `TaskExecutorMixin` 中调用 → 一致
- `self.schedule_panel.set_schedule_running()` / `set_schedule_stopped()`：在 `ScheduleHandlerMixin` 中调用，在 `SchedulePanel` 中定义 → 一致