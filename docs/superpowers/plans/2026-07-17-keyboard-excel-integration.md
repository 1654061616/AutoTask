# 键盘输入×Excel读取整合 实现计划

> **面向 AI 代理的工作者：** 必需子技能：使用 superpowers:subagent-driven-development（推荐）或 superpowers:executing-plans 逐任务实现此计划。步骤使用复选框（`- [ ]`）语法来跟踪进度。

**目标：** 在 keyboard_type 节点中增加"从Excel读取"和"从变量读取"两种数据来源，Excel 支持顺序读取和随机读取

**架构：** 改造 KeyboardTypePanel 增加数据来源切换，改造 FlowEngine._execute_keyboard_type 根据 data_source 字段决定文本来源，引擎级维护 Excel 读取光标

**技术栈：** PySide6, openpyxl, Python 3.13

---

## 文件结构

| 文件 | 职责 |
|------|------|
| `gui/step_panels/keyboard_panel.py` | KeyboardTypePanel：增加数据来源选择、Excel 配置区、变量名输入 |
| `core/engine.py` | FlowEngine：增加 `_excel_cursors`、`_read_excel_for_keyboard`、改造 `_execute_keyboard_type` |
| `gui/node_graph/node_types.py` | `keyboard_type` 节点描述更新 |
| `tests/test_engine.py` | 新增 Excel 数据源和变量数据源的测试用例 |

---

### 任务 1：改造 KeyboardTypePanel 面板 UI

**文件：**
- 修改：`gui/step_panels/keyboard_panel.py`（KeyboardTypePanel 类）

- [ ] **步骤 1：在 init_ui 开头增加数据来源选择器**

在 `self.input_text_edit = QTextEdit()` 之前插入数据来源下拉框和 Excel 配置区域：

```python
def init_ui(self):
    # 数据来源选择
    self.data_source_combo = self.add_combobox("数据来源", ["手动输入", "从Excel读取", "从变量读取"])

    # --- Excel 配置区域 ---
    self.excel_group = QGroupBox("Excel 读取配置")
    excel_layout = QVBoxLayout(self.excel_group)
    excel_layout.setContentsMargins(8, 8, 8, 8)
    excel_layout.setSpacing(6)

    self.file_path_edit = self.add_file_browser("文件路径", "Excel Files (*.xlsx *.xls)")
    excel_layout.addWidget(self.file_path_edit)
    # 注意：add_file_browser 返回的是 QWidget，需要从布局中取出已添加的控件重新放入 excel_group
    # 实际上应直接在 excel_layout 中构建

    self.sheet_edit = QLineEdit()
    self.sheet_edit.setText("Sheet1")
    self.sheet_edit.setPlaceholderText("默认 Sheet1")
    self.sheet_edit.setStyleSheet("""
        QLineEdit { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; font-size: 13px; }
        QLineEdit:focus { border-color: #3498db; }
    """)
    row = QHBoxLayout()
    row.addWidget(QLabel("工作表:"))
    row.addWidget(self.sheet_edit, 1)
    excel_layout.addLayout(row)

    self.read_mode_combo = QComboBox()
    self.read_mode_combo.addItems(["顺序读取", "随机读取"])
    self.read_mode_combo.setStyleSheet("""
        QComboBox { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; font-size: 13px; }
        QComboBox:focus { border-color: #3498db; }
    """)
    row = QHBoxLayout()
    row.addWidget(QLabel("读取模式:"))
    row.addWidget(self.read_mode_combo, 1)
    excel_layout.addLayout(row)

    # 读取范围单选
    self.read_range_group = QGroupBox("读取范围")
    range_layout = QVBoxLayout(self.read_range_group)
    self.read_range_radios = []
    range_options = ["单元格", "行", "列", "区域"]
    for i, option in enumerate(range_options):
        radio = QRadioButton(option)
        if i == 0:
            radio.setChecked(True)
        self.read_range_radios.append(radio)
        range_layout.addWidget(radio)
    excel_layout.addWidget(self.read_range_group)

    # 单元格地址
    self.cell_group = QGroupBox("单元格地址")
    cell_layout = QFormLayout(self.cell_group)
    self.cell_address_edit = QLineEdit()
    self.cell_address_edit.setPlaceholderText("例如: A1")
    self.cell_address_edit.setStyleSheet("""
        QLineEdit { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; }
        QLineEdit:focus { border-color: #3498db; }
    """)
    cell_layout.addRow("单元格:", self.cell_address_edit)
    excel_layout.addWidget(self.cell_group)

    # 行号
    self.row_group = QGroupBox("行号")
    row_layout = QFormLayout(self.row_group)
    self.row_number_spin = QSpinBox()
    self.row_number_spin.setRange(1, 1048576)
    self.row_number_spin.setValue(1)
    self.row_number_spin.setStyleSheet("""
        QSpinBox { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; }
        QSpinBox:focus { border-color: #3498db; }
    """)
    row_layout.addRow("起始行:", self.row_number_spin)
    excel_layout.addWidget(self.row_group)

    # 列号
    self.column_group = QGroupBox("列号")
    column_layout = QFormLayout(self.column_group)
    self.column_number_spin = QSpinBox()
    self.column_number_spin.setRange(1, 16384)
    self.column_number_spin.setValue(1)
    self.column_number_spin.setStyleSheet("""
        QSpinBox { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; }
        QSpinBox:focus { border-color: #3498db; }
    """)
    column_layout.addRow("列号:", self.column_number_spin)
    excel_layout.addWidget(self.column_group)

    # 区域
    self.range_group = QGroupBox("区域范围")
    range_form = QFormLayout(self.range_group)
    self.start_cell_edit = QLineEdit()
    self.start_cell_edit.setPlaceholderText("起始: A1")
    self.start_cell_edit.setStyleSheet("""
        QLineEdit { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; }
        QLineEdit:focus { border-color: #3498db; }
    """)
    self.end_cell_edit = QLineEdit()
    self.end_cell_edit.setPlaceholderText("结束: B5")
    self.end_cell_edit.setStyleSheet("""
        QLineEdit { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; }
        QLineEdit:focus { border-color: #3498db; }
    """)
    range_form.addRow("起始:", self.start_cell_edit)
    range_form.addRow("结束:", self.end_cell_edit)
    excel_layout.addWidget(self.range_group)

    # 输出格式
    self.var_format_combo = QComboBox()
    self.var_format_combo.addItems(["字符串", "数字", "列表"])
    self.var_format_combo.setStyleSheet("""
        QComboBox { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; font-size: 13px; }
        QComboBox:focus { border-color: #3498db; }
    """)
    row = QHBoxLayout()
    row.addWidget(QLabel("输出格式:"))
    row.addWidget(self.var_format_combo, 1)
    excel_layout.addLayout(row)

    self.main_layout.addWidget(self.excel_group)

    # --- 变量读取区域 ---
    self.variable_group = QGroupBox("变量读取")
    var_layout = QVBoxLayout(self.variable_group)
    self.variable_name_edit = QLineEdit()
    self.variable_name_edit.setPlaceholderText("输入变量名")
    self.variable_name_edit.setStyleSheet("""
        QLineEdit { padding: 4px 6px; border: 1px solid #d0d0d0; border-radius: 3px; font-size: 13px; }
        QLineEdit:focus { border-color: #3498db; }
    """)
    var_layout.addWidget(self.variable_name_edit)
    self.main_layout.addWidget(self.variable_group)

    # --- 手动输入区域（现有）---
    self.input_text_edit = QTextEdit()
    # ... 保持现有代码不变 ...
```

- [ ] **步骤 2：修改 init_ui 末尾——连接数据来源切换信号，设置初始可见性**

在 `self._connect_signals()` 调用前增加：

```python
    # 数据来源切换信号
    self.data_source_combo.currentIndexChanged.connect(self._update_data_source_visibility)
    for radio in self.read_range_radios:
        radio.toggled.connect(self._update_read_range_visibility)

    self._connect_signals()
    self._update_random_interval_visibility()
    self._update_data_source_visibility()
    self._update_read_range_visibility()
```

- [ ] **步骤 3：增加可见性控制方法**

```python
def _update_data_source_visibility(self):
    source = self.data_source_combo.currentIndex()  # 0=手动, 1=Excel, 2=变量
    self.input_text_edit.setVisible(source == 0)
    self.excel_group.setVisible(source == 1)
    self.variable_group.setVisible(source == 2)

def _update_read_range_visibility(self):
    selected = -1
    for i, radio in enumerate(self.read_range_radios):
        if radio.isChecked():
            selected = i
            break
    self.cell_group.setVisible(selected == 0)
    self.row_group.setVisible(selected == 1)
    self.column_group.setVisible(selected == 2)
    self.range_group.setVisible(selected == 3)
```

- [ ] **步骤 4：修改 get_config 和 set_config**

```python
def get_config(self):
    source_map = {0: "manual", 1: "excel", 2: "variable"}
    read_range_types = ["cell", "row", "column", "range"]
    read_range_type = self.read_range_radios.index([r for r in self.read_range_radios if r.isChecked()][0])

    config = {
        "data_source": source_map[self.data_source_combo.currentIndex()],
        "input_method": "typing" if self.input_method_combo.currentIndex() == 0 else "clipboard",
        "interval": self.interval_spin.value(),
        "random_interval": self.random_interval_check.isChecked(),
        "random_min_interval": self.random_min_spin.value(),
        "random_max_interval": self.random_max_spin.value(),
        "human_input": self.human_input_check.isChecked(),
        "delay": self.delay_spin.value(),
    }

    # 手动输入
    if config["data_source"] == "manual":
        config["input_text"] = self.input_text_edit.toPlainText()

    # Excel 读取
    if config["data_source"] == "excel":
        config["excel"] = {
            "file_path": self.file_path_edit.text(),
            "sheet": self.sheet_edit.text(),
            "read_mode": "sequential" if self.read_mode_combo.currentIndex() == 0 else "random",
            "read_range": read_range_types[read_range_type],
            "cell_address": self.cell_address_edit.text(),
            "row_number": self.row_number_spin.value(),
            "column_number": self.column_number_spin.value(),
            "start_cell": self.start_cell_edit.text(),
            "end_cell": self.end_cell_edit.text(),
            "var_format": ["string", "number", "list"][self.var_format_combo.currentIndex()],
        }

    # 变量读取
    if config["data_source"] == "variable":
        config["variable_name"] = self.variable_name_edit.text()

    return config


def set_config(self, config):
    source_map = {"manual": 0, "excel": 1, "variable": 2}
    self.data_source_combo.setCurrentIndex(source_map.get(config.get("data_source", "manual"), 0))

    # 手动输入
    self.input_text_edit.setPlainText(config.get("input_text", ""))

    # Excel 读取
    excel = config.get("excel", {})
    self.file_path_edit.setText(excel.get("file_path", ""))
    self.sheet_edit.setText(excel.get("sheet", "Sheet1"))
    self.read_mode_combo.setCurrentIndex(0 if excel.get("read_mode", "sequential") == "sequential" else 1)
    read_range_map = {"cell": 0, "row": 1, "column": 2, "range": 3}
    self.read_range_radios[read_range_map.get(excel.get("read_range", "cell"), 0)].setChecked(True)
    self.cell_address_edit.setText(excel.get("cell_address", ""))
    self.row_number_spin.setValue(excel.get("row_number", 1))
    self.column_number_spin.setValue(excel.get("column_number", 1))
    self.start_cell_edit.setText(excel.get("start_cell", ""))
    self.end_cell_edit.setText(excel.get("end_cell", ""))
    var_format_map = {"string": 0, "number": 1, "list": 2}
    self.var_format_combo.setCurrentIndex(var_format_map.get(excel.get("var_format", "string"), 0))

    # 变量读取
    self.variable_name_edit.setText(config.get("variable_name", ""))

    # 键盘设置
    input_method_map = {"typing": 0, "clipboard": 1}
    self.input_method_combo.setCurrentIndex(input_method_map.get(config.get("input_method", "typing"), 0))
    self.interval_spin.setValue(config.get("interval", 0.05))
    self.random_interval_check.setChecked(config.get("random_interval", False))
    self.random_min_spin.setValue(config.get("random_min_interval", 0.02))
    self.random_max_spin.setValue(config.get("random_max_interval", 0.15))
    self.human_input_check.setChecked(config.get("human_input", False))
    self.delay_spin.setValue(config.get("delay", 0))

    self._update_random_interval_visibility()
    self._update_data_source_visibility()
    self._update_read_range_visibility()
```

- [ ] **步骤 5：更新导入**

在文件顶部增加缺失的导入：

```python
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLabel, QSpinBox, QDoubleSpinBox, QComboBox,
                               QCheckBox, QGroupBox, QTextEdit, QListView,
                               QLineEdit, QRadioButton, QPushButton, QFileDialog)
```

- [ ] **步骤 6：运行应用验证面板显示正常**

运行：`python main.py`
预期：打开节点编辑器，选择键盘输入节点，看到数据来源下拉框，切换三个选项时显示对应区域

- [ ] **步骤 7：Commit**

```bash
git add gui/step_panels/keyboard_panel.py
git commit -m "feat(keyboard_panel): 增加数据来源选择（手动/Excel/变量），Excel支持顺序和随机读取"
```

---

### 任务 2：改造引擎执行逻辑

**文件：**
- 修改：`core/engine.py`

- [ ] **步骤 1：在 FlowEngine.__init__ 中增加 Excel 光标追踪字典**

```python
def __init__(self):
    # ... 现有代码 ...
    self._excel_cursors = {}  # {"file_path:sheet": current_row}
```

- [ ] **步骤 2：增加 _read_excel_for_keyboard 方法**

```python
def _read_excel_for_keyboard(self, excel_config):
    import openpyxl
    import random

    file_path = excel_config.get("file_path", "")
    sheet = excel_config.get("sheet", "Sheet1")
    read_mode = excel_config.get("read_mode", "sequential")
    read_range = excel_config.get("read_range", "cell")
    var_format = excel_config.get("var_format", "string")

    wb = openpyxl.load_workbook(file_path, data_only=True)
    ws = wb[sheet]

    if read_mode == "sequential":
        cursor_key = f"{file_path}:{sheet}"
        current_row = self._excel_cursors.get(cursor_key, 1)
        if current_row > ws.max_row:
            current_row = 1
        value = self._read_excel_row_value(ws, current_row, read_range, excel_config)
        self._excel_cursors[cursor_key] = current_row + 1
    else:
        current_row = random.randint(1, ws.max_row)
        value = self._read_excel_row_value(ws, current_row, read_range, excel_config)

    wb.close()
    return self._format_excel_value(value, var_format)

def _read_excel_row_value(self, ws, row_num, read_range, config):
    if read_range == "cell":
        addr = config.get("cell_address", "A1")
        col_letter = ''.join(c for c in addr if c.isalpha())
        return ws[f"{col_letter}{row_num}"].value
    elif read_range == "row":
        return [ws.cell(row=row_num, column=c).value for c in range(1, ws.max_column + 1)]
    elif read_range == "column":
        col_num = config.get("column_number", 1)
        return ws.cell(row=row_num, column=col_num).value
    elif read_range == "range":
        import openpyxl.utils
        start_cell = config.get("start_cell", "A1")
        end_cell = config.get("end_cell", "A1")
        start_col = openpyxl.utils.column_index_from_string(''.join(c for c in start_cell if c.isalpha()))
        start_row = int(''.join(c for c in start_cell if c.isdigit()))
        end_col = openpyxl.utils.column_index_from_string(''.join(c for c in end_cell if c.isalpha()))
        end_row = int(''.join(c for c in end_cell if c.isdigit()))
        total_rows = end_row - start_row + 1
        offset = (row_num - 1) % total_rows
        actual_row = start_row + offset
        return [ws.cell(row=actual_row, column=c).value for c in range(start_col, end_col + 1)]
    return None

def _format_excel_value(self, value, var_format):
    if var_format == "number":
        return str(value) if value is not None else "0"
    elif var_format == "list":
        if isinstance(value, list):
            return ", ".join(str(v) if v is not None else "" for v in value)
        return str(value) if value is not None else ""
    else:
        return str(value) if value is not None else ""
```

- [ ] **步骤 3：改造 _execute_keyboard_type 方法**

```python
def _execute_keyboard_type(self, config):
    if not self.keyboard:
        self.logger.error("键盘操作模块未加载")
        return

    data_source = config.get("data_source", "manual")

    if data_source == "excel":
        text = self._read_excel_for_keyboard(config.get("excel", {}))
    elif data_source == "variable":
        var_name = config.get("variable_name", "")
        text = str(self.variable_manager.get_variable(var_name) or "")
    else:
        text = config.get("input_text", "")

    text = self.variable_manager.resolve_expression(text)
    interval = config.get("interval", 0.05)

    self.logger.info(f"键盘输入: {text}")
    self.keyboard.type(text, interval=interval)
```

- [ ] **步骤 4：运行现有测试确保不破坏原有功能**

```bash
python -m pytest tests/test_engine.py -v --tb=short
```
预期：PASS

- [ ] **步骤 5：Commit**

```bash
git add core/engine.py
git commit -m "feat(engine): 键盘输入支持Excel顺序/随机读取和变量读取"
```

---

### 任务 3：编写引擎测试

**文件：**
- 修改：`tests/test_engine.py`

- [ ] **步骤 1：增加 Excel 顺序读取测试**

在文件末尾增加：

```python
import tempfile
import os
import openpyxl

def test_keyboard_type_excel_sequential():
    """测试键盘输入从Excel顺序读取数据"""
    # 创建测试 Excel 文件
    tmp = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
    tmp_path = tmp.name
    tmp.close()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws['A1'] = "第一行"
    ws['A2'] = "第二行"
    ws['A3'] = "第三行"
    wb.save(tmp_path)
    wb.close()

    try:
        engine = FlowEngine()
        # 模拟键盘模块
        typed_texts = []
        class FakeKeyboard:
            def type(self, text, interval=0):
                typed_texts.append(text)
        engine.keyboard = FakeKeyboard()

        excel_config = {
            "file_path": tmp_path,
            "sheet": "Sheet1",
            "read_mode": "sequential",
            "read_range": "cell",
            "cell_address": "A1",
            "var_format": "string",
        }
        config = {
            "data_source": "excel",
            "excel": excel_config,
            "interval": 0.05,
        }

        # 第一次执行
        engine._execute_keyboard_type(config)
        assert typed_texts[0] == "第一行"

        # 第二次执行
        engine._execute_keyboard_type(config)
        assert typed_texts[1] == "第二行"

        # 第三次执行
        engine._execute_keyboard_type(config)
        assert typed_texts[2] == "第三行"

        # 第四次执行——循环回第一行
        engine._execute_keyboard_type(config)
        assert typed_texts[3] == "第一行"
    finally:
        os.unlink(tmp_path)


def test_keyboard_type_excel_random():
    """测试键盘输入从Excel随机读取"""
    tmp = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
    tmp_path = tmp.name
    tmp.close()

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    for i in range(1, 11):
        ws.cell(row=i, column=1, value=f"行{i}")
    wb.save(tmp_path)
    wb.close()

    try:
        engine = FlowEngine()
        typed_texts = []
        class FakeKeyboard:
            def type(self, text, interval=0):
                typed_texts.append(text)
        engine.keyboard = FakeKeyboard()

        excel_config = {
            "file_path": tmp_path,
            "sheet": "Sheet1",
            "read_mode": "random",
            "read_range": "cell",
            "cell_address": "A1",
            "var_format": "string",
        }
        config = {
            "data_source": "excel",
            "excel": excel_config,
            "interval": 0.05,
        }

        engine._execute_keyboard_type(config)
        # 随机读取应返回10行中的某一行
        assert typed_texts[0] in [f"行{i}" for i in range(1, 11)]
    finally:
        os.unlink(tmp_path)


def test_keyboard_type_variable():
    """测试键盘输入从变量读取"""
    engine = FlowEngine()
    typed_texts = []
    class FakeKeyboard:
        def type(self, text, interval=0):
            typed_texts.append(text)
    engine.keyboard = FakeKeyboard()
    engine.variable_manager.set_variable("my_var", "变量内容")

    config = {
        "data_source": "variable",
        "variable_name": "my_var",
        "interval": 0.05,
    }

    engine._execute_keyboard_type(config)
    assert typed_texts[0] == "变量内容"


def test_keyboard_type_manual_backward_compat():
    """测试手动输入模式向后兼容"""
    engine = FlowEngine()
    typed_texts = []
    class FakeKeyboard:
        def type(self, text, interval=0):
            typed_texts.append(text)
    engine.keyboard = FakeKeyboard()

    # 旧格式（无 data_source 字段）
    config = {
        "input_text": "旧格式文本",
        "interval": 0.05,
    }

    engine._execute_keyboard_type(config)
    assert typed_texts[0] == "旧格式文本"
```

- [ ] **步骤 2：运行测试**

```bash
python -m pytest tests/test_engine.py -v --tb=short
```
预期：4 个新测试 PASS

- [ ] **步骤 3：Commit**

```bash
git add tests/test_engine.py
git commit -m "test(engine): 增加键盘输入Excel读取和变量读取的测试"
```

---

### 任务 4：更新节点类型描述

**文件：**
- 修改：`gui/node_graph/node_types.py`

- [ ] **步骤 1：更新 keyboard_type 的 name**

```python
"keyboard_type": {"name": "键盘输入", "icon": "⌨️", "color": "#2196f3", "category": "keyboard"},
# 改为
"keyboard_type": {"name": "键盘输入（支持Excel/变量）", "icon": "⌨️", "color": "#2196f3", "category": "keyboard"},
```

- [ ] **步骤 2：Commit**

```bash
git add gui/node_graph/node_types.py
git commit -m "docs(node_types): 更新 keyboard_type 节点描述"
```

---

### 任务 5：最终验证

- [ ] **步骤 1：运行全部测试**

```bash
python -m pytest tests/test_engine.py tests/test_variables.py -v --tb=short
```
预期：全部 PASS

- [ ] **步骤 2：启动应用手工验证**

```bash
python main.py
```
验证：
1. 新建任务 → 添加键盘输入节点 → 数据来源选择"手动输入" → 正常
2. 数据来源选择"从Excel读取" → 显示 Excel 配置区域 → 浏览选择一个 xlsx 文件
3. 数据来源选择"从变量读取" → 显示变量名输入框
4. 保存任务后再打开，配置正确回显

- [ ] **步骤 3：Push**

```bash
git push
```