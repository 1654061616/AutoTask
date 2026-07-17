# 样式表集中管理 - 设计文档

**日期**: 2026-07-17
**状态**: 设计中

## 1. 背景

项目中存在 100+ 处 `setStyleSheet` 内联样式调用，分布在 10+ 个文件中。已有 `gui/styles_bak.py` 文件包含 `Colors` 和 `Styles` 类，但被重命名为 `_bak` 表示被搁置，且 `ui_builder.py` 中的导入 `from gui.styles import Styles, Colors` 会因文件不存在而失败。

## 2. 目标

- 所有样式集中管理，消除内联样式
- 支持亮色/暗色主题切换
- 使用 QSS 外部样式表 + 动态工厂方法双层架构

## 3. 文件结构

```
gui/
├── styles/                          # 新：样式管理模块
│   ├── __init__.py                  # 统一导出
│   ├── colors.py                    # 颜色常量
│   ├── widget_styles.py             # 动态样式工厂
│   └── theme_manager.py             # 主题管理器
│
resources/
└── themes/
    ├── light.qss                    # 亮色主题
    └── dark.qss                     # 暗色主题
```

## 4. 职责划分

| 放在 `.qss` 文件中（静态） | 留在 `widget_styles.py` 中（动态） |
|---|---|
| 全局控件默认样式（QLineEdit, QComboBox, QSpinBox...） | 需要传参的按钮（`btn_success("8px 20px")`） |
| QMainWindow 背景 | 运行时状态切换（如按钮变红/蓝） |
| QTreeWidget / QHeaderView 样式 | 颜色随参数变化的组件 |
| QGroupBox 全局默认 | — |
| QTextEdit 代码编辑器样式 | — |
| 通用 hover/focus/pressed 状态 | — |

## 5. ThemeManager 设计

```python
class ThemeManager:
    _instance = None
    _current_theme = "light"
    _watched_widgets: list[QWidget] = []

    @classmethod
    def instance(cls) -> "ThemeManager": ...

    def load_qss(self, theme="light") -> str: ...

    def apply_to(self, widget: QWidget, theme="light"): ...

    def switch_theme(self, theme: str): ...

    def watch(self, widget: QWidget): ...

    def current_theme(self) -> str: ...
```

## 6. 三层调用架构

```
调用层（各面板）           中间层（工厂方法）          底层（QSS + 颜色常量）
─────────────────    ─────────────────────    ────────────────────────
widget.setStyleSheet  →  Styles.input_field()  →  light.qss 中的 QLineEdit
widget.setStyleSheet  →  Styles.btn_primary()  →  colors.py 中的 PRIMARY
widget.setStyleSheet  →  Styles.spin_box()     →  light.qss 中的 QSpinBox
QMainWindow           →  ThemeManager.apply()  →  light.qss / dark.qss
```

## 7. 迁移映射

### 7.1 改造前（内联样式示例）

```python
spinbox.setStyleSheet("""
    QSpinBox { padding: 5px; border: 1px solid #ddd; border-radius: 4px; min-width: 100px; }
    QSpinBox:focus { border-color: #3498db; }
""")
```

### 7.2 改造后（引用工厂）

```python
spinbox.setStyleSheet(Styles.spin_box())
```

### 7.3 改造范围

| 文件 | 改造方式 |
|------|---------|
| `gui/styles_bak.py` | 删除，逻辑迁移到 `gui/styles/` |
| `gui/step_panels/__init__.py` | 所有内联样式 → `Styles.xxx()` 工厂方法 |
| `gui/step_panels/*.py`（6 个子面板） | 同上 |
| `gui/widgets/node_editor_dialog.py` | 同上 |
| `gui/widgets/cron_generator.py` | 同上 |
| `gui/main_window/ui_builder.py` | 用 `ThemeManager.apply_to()` 替换 |
| `gui/main_window/schedule_handler.py` | 动态状态切换保留在 `widget_styles.py` |
| `gui/main_window/schedule_panel.py` | 按钮样式引用工厂 |
| `gui/node_graph/node_toolbar.py` | 同上 |

### 7.4 新增工厂方法

- `small_input()` — 小号输入框
- `small_line_edit()` — 小号 QLineEdit
- `browse_btn()` — 浏览按钮
- `select_btn()` — 坐标选择按钮
- `slider()` — 滑块样式
- `schedule_btn_start()` / `schedule_btn_stop()` — 调度按钮（蓝/红）
- `ok_btn()` / `cancel_btn()` — 对话框按钮
- `small_spin_box()` — 小号 SpinBox
- `section_label()` — 区域标签

## 8. 实施步骤

1. 创建 `gui/styles/` 包，迁移 `styles_bak.py` 内容
2. 创建 `resources/themes/light.qss`，提取全局静态样式
3. 实现 `ThemeManager`
4. 逐个改造各面板，删除内联样式
5. 删除 `gui/styles_bak.py`