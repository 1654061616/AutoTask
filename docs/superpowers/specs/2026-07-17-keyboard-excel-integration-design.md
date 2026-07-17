# 键盘输入 × Excel 读取整合设计

## 1. 概述

将 `keyboard_type`（键盘输入）和 `excel_read`（读取Excel）整合为一个节点，支持三种数据来源：手动输入、从Excel读取、从变量读取。Excel 读取支持顺序读取（逐行）和随机读取（随机行）两种模式。

## 2. 面板设计

### 2.1 键盘输入面板（改造后）

在现有 `KeyboardTypePanel` 顶部增加"数据来源"选择：

```
┌──────────────────────────────────────┐
│ 数据来源: [从Excel读取         ▼]    │
│   · 手动输入                         │
│   · 从Excel读取                      │
│   · 从变量读取                       │
├──────────────────────────────────────┤
│ [当选择"手动输入"时]                  │
│   输入内容: [QTextEdit]              │
├──────────────────────────────────────┤
│ [当选择"从Excel读取"时]              │
│   文件路径: [___________] [浏览]      │
│   工作表:   [Sheet1________]         │
│   读取模式: [顺序读取         ▼]     │
│     · 顺序读取（逐行）                │
│     · 随机读取（随机行）              │
│   读取范围: ● 单元格 ○ 行 ○ 列 ○ 区域│
│   [根据读取范围显示对应输入框]         │
│   输出格式: [字符串            ▼]    │
│     · 字符串 · 数字 · 列表            │
├──────────────────────────────────────┤
│ [当选择"从变量读取"时]                │
│   变量名: [___________]              │
├──────────────────────────────────────┤
│ 输入方式: [逐字输入            ▼]    │
│ 输入间隔: [0.05]                     │
│ □ 随机间隔   □ 模拟人类输入           │
│ 执行前延迟: [0.0] 秒                 │
└──────────────────────────────────────┘
```

### 2.2 动态显示规则

| 数据来源 | 显示区域 |
|---------|---------|
| 手动输入 | 文本输入框 (QTextEdit) |
| 从Excel读取 | 文件路径、工作表、读取模式、读取范围、输出格式 |
| 从变量读取 | 变量名输入框 |

### 2.3 读取模式行为

| 模式 | 行为 | 循环 |
|------|------|------|
| 顺序读取 | 第1次执行读第1行，第2次读第2行... | 到末尾后从头循环 |
| 随机读取 | 每次执行随机选一行 | 无 |

## 3. 配置数据结构

### 3.1 新 config 格式

```python
{
    "data_source": "manual",        # "manual" | "excel" | "variable"
    
    # 手动输入
    "input_text": "hello world",
    
    # Excel 读取
    "excel": {
        "file_path": "C:/data.xlsx",
        "sheet": "Sheet1",
        "read_mode": "sequential",   # "sequential" | "random"
        "read_range": "row",         # "cell" | "row" | "column" | "range"
        # 单元格
        "cell_address": "A1",
        # 行
        "row_number": 1,             # 顺序时作为起始行，随机时忽略
        # 列
        "column_number": 1,
        # 区域
        "start_cell": "A1",
        "end_cell": "A100",
        # 输出
        "var_format": "string",      # "string" | "number" | "list"
    },
    
    # 变量读取
    "variable_name": "my_var",
    
    # 键盘输入设置
    "input_method": "typing",        # "typing" | "clipboard"
    "interval": 0.05,
    "random_interval": False,
    "random_min_interval": 0.02,
    "random_max_interval": 0.15,
    "human_input": False,
    "delay": 0.0
}
```

### 3.2 向后兼容

引擎读取 config 时，若 `data_source` 字段不存在，默认 `"manual"`，使用 `input_text` 字段，保证旧任务文件正常运行。

## 4. 引擎改动

### 4.1 引擎级光标追踪

在 `FlowEngine` 中新增 `_excel_cursors` 字典，维护每个文件的顺序读取位置：

```python
class FlowEngine:
    def __init__(self):
        # ...
        self._excel_cursors = {}  # {file_path: current_row}
    
    def _read_excel_for_keyboard(self, excel_config):
        """从 Excel 读取数据，支持顺序/随机模式"""
        file_path = excel_config["file_path"]
        sheet = excel_config.get("sheet", "Sheet1")
        read_mode = excel_config.get("read_mode", "sequential")
        read_range = excel_config.get("read_range", "cell")
        var_format = excel_config.get("var_format", "string")
        
        import openpyxl
        wb = openpyxl.load_workbook(file_path, data_only=True)
        ws = wb[sheet]
        
        if read_mode == "sequential":
            cursor_key = f"{file_path}:{sheet}"
            current_row = self._excel_cursors.get(cursor_key, 1)
            # 读取当前行
            value = self._read_row_value(ws, current_row, read_range, excel_config)
            # 推进光标
            self._excel_cursors[cursor_key] = current_row + 1
            # 到末尾循环
            if current_row > ws.max_row:
                self._excel_cursors[cursor_key] = 1
        else:  # random
            import random
            current_row = random.randint(1, ws.max_row)
            value = self._read_row_value(ws, current_row, read_range, excel_config)
        
        wb.close()
        return self._format_value(value, var_format)
    
    def _read_row_value(self, ws, row_num, read_range, config):
        """根据读取范围从指定行读取数据"""
        if read_range == "cell":
            addr = config.get("cell_address", "A1")
            col_letter = ''.join(c for c in addr if c.isalpha())
            addr = f"{col_letter}{row_num}"
            return ws[addr].value
        elif read_range == "row":
            return [ws.cell(row=row_num, column=c).value 
                    for c in range(1, ws.max_column + 1)]
        elif read_range == "column":
            col_num = config.get("column_number", 1)
            return ws.cell(row=row_num, column=col_num).value
        elif read_range == "range":
            # 区域模式下，行号决定在区域内的偏移
            start_cell = config.get("start_cell", "A1")
            end_cell = config.get("end_cell", "A1")
            start_col = openpyxl.utils.column_index_from_string(
                ''.join(c for c in start_cell if c.isalpha()))
            start_row = int(''.join(c for c in start_cell if c.isdigit()))
            end_col = openpyxl.utils.column_index_from_string(
                ''.join(c for c in end_cell if c.isalpha()))
            end_row = int(''.join(c for c in end_cell if c.isdigit()))
            total_rows = end_row - start_row + 1
            offset = (row_num - 1) % total_rows
            actual_row = start_row + offset
            return [ws.cell(row=actual_row, column=c).value 
                    for c in range(start_col, end_col + 1)]
    
    def _format_value(self, value, var_format):
        if var_format == "number":
            return str(value) if value is not None else "0"
        elif var_format == "list":
            return ", ".join(str(v) for v in value) if value else ""
        else:
            return str(value) if value is not None else ""
```

### 4.2 改造 `_execute_keyboard_type`

```python
def _execute_keyboard_type(self, config):
    if not self.keyboard:
        self.logger.error("键盘操作模块未加载")
        return
    
    data_source = config.get("data_source", "manual")
    
    if data_source == "excel":
        text = self._read_excel_for_keyboard(config["excel"])
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

## 5. 文件变更清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `gui/step_panels/keyboard_panel.py` | 修改 | 增加数据来源选择、Excel 读取配置区、变量名输入 |
| `core/engine.py` | 修改 | 增加 `_excel_cursors`、`_read_excel_for_keyboard`、改造 `_execute_keyboard_type` |
| `gui/node_graph/node_types.py` | 修改 | `keyboard_type` 节点描述更新 |
| `gui/step_panels/excel_panel.py` | 保留 | 独立 Excel 读取节点仍可用 |

## 6. 测试要点

- [ ] 手动输入模式：与现有行为一致
- [ ] Excel 顺序读取：多次执行逐行读取，到末尾循环
- [ ] Excel 随机读取：每次执行读取不同行
- [ ] 变量读取：从已有变量读取文本
- [ ] 向后兼容：旧任务文件（无 data_source 字段）正常执行
- [ ] 单元格/行/列/区域四种读取范围均正常
- [ ] 字符串/数字/列表三种输出格式均正常