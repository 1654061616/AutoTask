# CLAUDE.md

## 项目概述

AutoFlow 是一个基于 Python 的桌面自动化操作软件，使用 PySide6 (Qt for Python) 构建 GUI，支持通过可视化节点图编排自动化流程。核心功能包括：鼠标键盘模拟、图像识别点击、Excel 数据驱动、条件/循环控制、定时任务调度等。

## 技术栈

- **语言**: Python 3.8+
- **GUI 框架**: PySide6 (Qt)
- **自动化**: pyautogui, pydirectinput, keyboard
- **图像识别**: opencv-python, easyocr
- **数据处理**: openpyxl, numpy, Pillow
- **调度**: APScheduler
- **构建**: setuptools (pyproject.toml)
- **测试**: pytest

## 项目结构

```
AutoTask/
├── main.py                  # 程序入口，Qt 应用初始化
├── setup.py                 # 打包配置
├── pyproject.toml           # 项目元数据与依赖
├── requirements.txt         # pip 依赖列表
├── core/                    # 核心引擎层
│   ├── engine.py            # FlowEngine — 流程执行引擎
│   ├── step_executor.py     # StepExecutor — 步骤执行器 + create_step_executor 工厂函数
│   ├── parser.py            # FlowParser — JSON 流程文件解析/验证
│   ├── flow_manager.py      # FlowManager — 流程 CRUD 管理
│   ├── variables.py         # VariableManager — 变量管理（支持 ${var} 表达式解析）
│   ├── scheduler.py         # TaskScheduler — 定时任务调度（cron/interval/date）
│   └── logger.py            # Logger — 日志记录
├── operations/              # 操作模块层（被 step_executor 调用）
│   ├── mouse.py             # 鼠标操作（点击、移动、拖拽、滚动）
│   ├── keyboard.py          # 键盘操作（输入、按键、快捷键）
│   ├── image_recognition.py # 图像识别（模板匹配、存在判断）
│   ├── window.py            # 窗口操作（查找、激活、关闭）
│   ├── condition.py         # 条件判断（if/else）
│   ├── loop.py              # 循环控制
│   ├── excel.py             # Excel 读写
│   ├── control.py           # 流程控制（goto/label）
│   ├── clipboard.py         # 剪贴板操作
│   ├── file_operations.py   # 文件操作
│   └── ocr.py               # OCR 文字识别
├── gui/                     # GUI 界面层
│   ├── main_window/         # 主窗口（Mixin 模式拆分）
│   │   ├── __init__.py      # MainWindow 类（继承 QMainWindow + 5个 Mixin）
│   │   ├── ui_builder.py    # UIBuilderMixin — 界面构建
│   │   ├── task_manager.py  # TaskManagerMixin — 任务管理
│   │   ├── task_executor.py # TaskExecutorMixin — 任务执行
│   │   ├── schedule_handler.py # ScheduleHandlerMixin — 定时处理
│   │   ├── schedule_panel.py   # SchedulePanel — 定时面板
│   │   └── node_handler.py  # NodeHandlerMixin — 节点图处理
│   ├── node_graph/          # 节点图编辑器
│   │   ├── graph_scene.py   # GraphScene — QGraphicsScene 子类
│   │   ├── graph_view.py    # GraphView — QGraphicsView 子类
│   │   ├── node_widget.py   # NodeWidget — 节点控件
│   │   ├── port_widget.py   # PortWidget — 端口控件
│   │   ├── edge_widget.py   # EdgeWidget — 连线控件（贝塞尔曲线）
│   │   ├── node_types.py    # 节点类型定义
│   │   └── node_toolbar.py  # NodeToolbar — 节点工具栏
│   ├── step_panels/         # 步骤编辑面板（每种步骤类型一个面板）
│   │   ├── mouse_panel.py
│   │   ├── keyboard_panel.py
│   │   ├── image_panel.py
│   │   ├── window_panel.py
│   │   ├── excel_panel.py
│   │   ├── variable_panel.py
│   │   └── control_panel.py
│   ├── widgets/             # 通用组件
│   │   ├── cron_generator.py
│   │   └── node_editor_dialog.py
│   └── styles/              # 样式系统
│       ├── colors.py        # 颜色常量
│       ├── widget_styles.py # 组件样式
│       ├── theme_manager.py # 主题管理（亮/暗）
│       └── resources/       # 图标、QSS 主题文件
├── plugins/                 # 插件系统
│   ├── plugin_manager.py
│   └── example_plugin.py
├── utils/                   # 工具函数
│   └── resource_path.py     # 资源路径处理
├── tests/                   # 测试文件
├── resources/               # 测试用 JSON 流程文件
└── docs/                    # 设计文档与实现计划
```

## 架构设计

### 分层架构

```
GUI 层 (gui/)        — PySide6 界面，节点图编辑器，Mixin 模式
    ↓ 依赖
引擎层 (core/)        — 流程解析、执行、调度、变量管理
    ↓ 依赖
操作层 (operations/)  — 具体操作实现（鼠标、键盘、图像识别等）
```

### 关键设计模式

1. **Mixin 模式**: `MainWindow` 继承 5 个 Mixin 类，将功能拆分为独立模块
2. **工厂函数**: `create_step_executor()` 在 `core/step_executor.py` 中，组装所有操作模块注入 `StepExecutor`
3. **信号驱动**: 使用 Qt Signal 在 GUI 组件间通信（`flow_loaded`, `step_selected`, `flow_started`, `flow_stopped`, `log_received`, `task_completed`）
4. **节点图**: 基于 QGraphicsScene/QGraphicsView 的可视化流程编辑器

## 常用命令

```bash
# 安装依赖
pip install -r requirements.txt

# 运行程序
python main.py

# 运行所有测试
pytest tests/

# 运行单个测试
pytest tests/test_engine.py -v

# 构建分发包
python setup.py sdist bdist_wheel
```

## 代码规范

- Python 文件使用 UTF-8 编码
- 注释和文档字符串使用中文
- 类名使用 PascalCase，函数/变量使用 snake_case
- 每个模块文件顶部包含中文文档字符串说明功能
- 使用 type hints 标注类型
- 导入顺序：标准库 → 第三方库 → 项目内部模块
- 相对导入用于同包内模块（`from .xxx import`），绝对导入用于跨包（`from core.xxx import`）

## 注意事项

- `operations/__init__.py` 目前为空，操作模块通过 `core/step_executor.py` 中的 `create_step_executor()` 工厂函数组装
- 日志文件输出到 `autoflow_error.log`
- 测试流程 JSON 文件位于 `resources/` 目录
- 图标资源位于 `gui/styles/resources/icons/`
- 主题 QSS 文件位于 `gui/styles/resources/themes/`
- Windows 平台特殊处理：DPI 感知设置（`main.py`）
- 所有函数和类都必须有中文注释
- 所有变量都必须有中文注释
- 提交代码前，不用对比resources/下的所有文件
- 不允许自动提交代码
- 注意PowerShell引号问题，用标准引号
- Git提交时，注意不能使用&& 例如：git -C "E:\A_PycharmProjects\AutoTask" add -A && git -C "E:\A_PycharmProjects\AutoTask" commit -m "feat: 全局等待配置 — 工具栏设置弹窗，engine 回退到 global_config 默认值"
