# 定时调度面板嵌入 - 设计文档

**日期**: 2026-07-17  
**状态**: 设计中

---

## 1. 概述

将调度配置功能嵌入到 `main_window.py` 右侧面板，替换现有的简单"定时设置" QGroupBox。
支持四种触发类型，其中 CRON 类型支持表达式生成器和执行时间预览。

## 2. 架构
main_window.py 右侧面板 (right_layout) ├── 任务信息 (QGroupBox) ← 不变 ├── 定时设置 (QGroupBox) ← 替换：嵌入 SchedulePanel │ └── SchedulePanel (QWidget) ← 新增 gui/widgets/schedule_panel.py │ └── [cron类型] 点击按钮弹出 │ └── CronGeneratorDialog ← 新增 gui/widgets/cron_generator.py ├── 执行步骤查看 (QGroupBox) ← 不变 └── 操作按钮组 ← 不变


Plain Text


## 3. 新增依赖

`requirements.txt` 新增：
croniter>=2.0.0


Plain Text


## 4. SchedulePanel 组件设计

### 4.1 文件位置
`gui/widgets/schedule_panel.py`

### 4.2 类签名

```python
class SchedulePanel(QWidget):
    """嵌入右侧面板的定时调度配置组件"""
    
    def __init__(self, parent=None): ...
    def get_config(self) -> dict: ...
    def load_config(self, config: dict): ...
    def _on_trigger_changed(self, trigger_type: str): ...
    def _on_cron_expression_changed(self, text: str): ...
    def _update_cron_preview(self): ...
    def _open_cron_generator(self): ...
```

### 4.3 触发类型与控件

| 中文显示 | 内部值 | 控件 |
|---------|--------|------|
| 立即执行1次 | `immediate` | 提示标签："任务启动后立即执行一次" |
| 间隔执行 | `interval` | QSpinBox(1-86400) + 单位标签"秒" |
| CRON定时 | `cron` | QLineEdit(CRON表达式) + "生成器"按钮 + 下次执行时间预览 |
| 指定时间 | `date` | QDateTimeEdit(日期时间选择器) |

### 4.4 CRON 类型子布局
┌─────────────────────────────────────────┐ │ CRON表达式: [* * * * * ] [生成器]│ │ │ │ 最近执行时间: │ │ 1. 2026-07-17 14:00:00 │ │ 2. 2026-07-17 14:30:00 │ │ 3. 2026-07-17 15:00:00 │ │ 4. 2026-07-17 15:30:00 │ │ 5. 2026-07-17 16:00:00 │ └─────────────────────────────────────────┘


Plain Text


CRON 表达式输入框默认值：`0 9 * * *`（每天9点）
输入框内容变化时实时更新执行时间预览。

### 4.5 配置数据格式

```python
config = {
    "trigger_type": "immediate",  # immediate | interval | cron | date
    "params": {
        # interval 类型
        "interval": 3600,         # 秒数
        
        # cron 类型
        "cron_expression": "0 9 * * *",  # 标准5字段CRON表达式
        
        # date 类型
        "run_date": "2026-07-17T14:00:00"  # ISO格式日期时间
    }
}
```

## 5. CronGeneratorDialog 组件设计

### 5.1 文件位置
`gui/widgets/cron_generator.py`

### 5.2 类签名

```python
class CronGeneratorDialog(QDialog):
    """CRON表达式生成器弹窗"""
    
    cron_generated = Signal(str)  # 发送生成的CRON表达式
    
    def __init__(self, current_expression="0 9 * * *", parent=None): ...
    def _on_field_changed(self): ...
    def _on_preset_selected(self, preset: str): ...
    def _build_expression(self) -> str: ...
```

### 5.3 界面布局
┌──────────────────────────────────────────┐ │ CRON 表达式生成器 │ │ │ │ 常用预设: [每天9点执行 ▼] │ │ │ │ 分钟: [0 ] (0-59, 逗号分隔多项) │ │ 小时: [9 ] (0-23) │ │ 日: [* ] (1-31) │ │ 月: [* ] (1-12) │ │ 星期: [* ] (0-6, 0=周日) │ │ │ │ 当前表达式: 0 9 * * * │ │ │ │ 预览: │ │ 2026-07-17 09:00:00 │ │ 2026-07-18 09:00:00 │ │ 2026-07-19 09:00:00 │ │ │ │ [确定] [取消] │ └──────────────────────────────────────────┘


Plain Text


### 5.4 常用预设

| 预设名称 | CRON 表达式 |
|---------|------------|
| 每分钟 | `* * * * *` |
| 每5分钟 | `*/5 * * * *` |
| 每小时 | `0 * * * *` |
| 每天9点 | `0 9 * * *` |
| 每天9点和18点 | `0 9,18 * * *` |
| 工作日9点 | `0 9 * * 1-5` |
| 每周一9点 | `0 9 * * 1` |
| 每月1号9点 | `0 9 1 * *` |

选择预设后自动填充各字段输入框，并更新表达式预览。

## 6. 数据流

### 6.1 保存（on_save_flow）
SchedulePanel.get_config() → save_data["schedule"] → JSON 文件


Plain Text


移除旧字段 `execute_mode`、`execute_time`、`delay`，替换为 `schedule`。当前 JSON 结构（`resources/测试.json`）中，定时相关字段在**顶层**：

```JSON
{
  "id": "e8d59afc",
  "name": "测试",
  "version": "1.0",
  "status": "已停止",
  "nodes": [...],
  "edges": [...],
  "execute_mode": "手动执行",   ← 删除
  "execute_time": "13:14:00",  ← 删除
  "delay": 1440                ← 删除
}
```

改造后，三个旧字段替换为一个 `schedule` 节点，**同样在顶层**：

```JSON
{
  "id": "e8d59afc",
  "name": "测试",
  "version": "1.0",
  "status": "已停止",
  "nodes": [...],
  "edges": [...],
  "schedule": {
    "trigger_type": "cron",
    "params": {
      "cron_expression": "0 9 * * *"
    }
  }
}
```

对应代码中 `on_save_flow` 的 `save_data` 字典变化：

```Python
save_data = {
    ...
    # "execute_mode": self.execute_mode_combo.currentText(),  ← 删除
    # "execute_time": self.execute_time_edit.text(),          ← 删除
    # "delay": self.delay_spin.value()                        ← 删除
    "schedule": self.schedule_panel.get_config(),             ← 新增
}
```

四种类型的 JSON 示例：

| 类型      | `schedule` 值                                                |
| :-------- | :----------------------------------------------------------- |
| immediate | `{"trigger_type": "immediate", "params": {}}`                |
| interval  | `{"trigger_type": "interval", "params": {"interval": 3600}}` |
| cron      | `{"trigger_type": "cron", "params": {"cron_expression": "0 9 * * *"}}` |
| date      | `{"trigger_type": "date", "params": {"run_date": "2026-07-17T14:00:00"}}` |

------

需要我把这个 JSON 结构说明也补充到设计文档中吗？


### 6.2 加载（load_schedule_settings）
task["schedule"] → SchedulePanel.load_config(config) → 恢复面板状态


Plain Text


不兼容旧格式：无 `schedule` 字段时默认 `immediate`。

### 6.3 CRON生成器交互
用户点击"生成器"按钮 → 打开 CronGeneratorDialog(current_expression) → 用户选择预设/填写字段 → 点击"确定" → 发射 cron_generated 信号 → SchedulePanel 更新 CRON 表达式输入框 → 触发执行时间预览更新


Plain Text


## 7. main_window.py 修改点

| 位置 | 操作 | 说明 |
|------|------|------|
| 导入区 | 新增 | `from gui.widgets.schedule_panel import SchedulePanel` |
| `create_central_widget` | 替换 | 移除旧 schedule_group，改为 `self.schedule_panel = SchedulePanel()` |
| `load_schedule_settings` | 修改 | 调用 `self.schedule_panel.load_config()` |
| `on_save_flow` | 修改 | 调用 `self.schedule_panel.get_config()` 替换旧字段 |
| `on_new_flow` | 修改 | 重置 `self.schedule_panel` |

## 8. 新增文件清单

| 文件 | 说明 |
|------|------|
| `gui/widgets/schedule_panel.py` | 定时调度面板组件 |
| `gui/widgets/cron_generator.py` | CRON表达式生成器弹窗 |

## 9. 移除的代码

`main_window.py` 中：
- `self.schedule_group`、`self.execute_mode_combo`、`self.execute_time_edit`
- `self.delay_spin`、`self.next_execute_label` 及所有相关布局代码
- core/scheduler.py 修改 — 新增 immediate 分支 + 增强 cron 支持完整 5 字段表达式
## 10. 不做的事

- `gui/scheduler_dialog.py` 保留不动
- 不改变其他面板组件

## 11. 测试要点

1. 四种触发类型切换正常，控件正确显示/隐藏
2. CRON表达式输入后，执行时间预览实时更新
3. CRON生成器：选择预设后各字段正确填充，表达式正确
4. CRON生成器确定后，表达式回填到主面板
5. 保存/加载任务后调度配置正确恢复
规格自检
✅ 占位符扫描 — 无 TODO、待定
✅ 内部一致性 — CRON 5 字段格式在 SchedulePanel、CronGeneratorDialog、配置数据三处一致
✅ 范围检查 — 聚焦面板嵌入 + CRON增强，不涉及其他模块
✅ 模糊性检查 — 预设列表、字段含义、信号传递均已明确