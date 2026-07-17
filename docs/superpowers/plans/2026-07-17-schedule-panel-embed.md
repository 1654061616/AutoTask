# 定时调度面板嵌入 - 实现计划

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 逐任务实现此计划。步骤使用复选框（`- [ ]`）语法来跟踪进度。

**目标：** 将调度配置功能嵌入主窗口右侧面板，替换旧的简单定时设置，支持 immediate/interval/cron/date 四种类型，CRON 类型带表达式生成器和执行时间预览。

**架构：** 新建 `SchedulePanel`（嵌入面板）和 `CronGeneratorDialog`（CRON生成器弹窗），修改 `core/scheduler.py` 支持新类型，修改 `main_window.py` 替换旧面板。

**技术栈：** PySide6, croniter, APScheduler

---

### 任务 1：添加 croniter 依赖
- [ ] 修改：`requirements.txt` — 追加 `croniter>=2.0.0`

### 任务 2：创建 CRON 表达式生成器弹窗
- [ ] 创建：`gui/widgets/cron_generator.py`

### 任务 3：创建 SchedulePanel 定时调度面板
- [ ] 创建：`gui/widgets/schedule_panel.py`

### 任务 4：更新 widgets 包导出
- [ ] 修改：`gui/widgets/__init__.py`

### 任务 5：增强 core/scheduler.py
- [ ] 修改：`core/scheduler.py`

### 任务 6：修改 main_window.py 集成新面板
- [ ] 修改：`gui/main_window.py`

---