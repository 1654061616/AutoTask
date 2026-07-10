# AutoFlow 自动化操作软件 - 设计文档

## 1. 项目概述

### 1.1 项目名称
AutoFlow - 可视化桌面自动化引擎

### 1.2 项目定位
一款基于 Python + PySide6 开发的零代码可视化桌面自动化工具，通过拖拽式步骤编排实现鼠标控制、键盘输入、图片识别、分支判断等自动化操作。

### 1.3 设计理念
- **零代码**：无需编程基础，通过可视化界面编排自动化流程
- **数据驱动**：支持 Excel 数据读取作为步骤输入参数
- **插件化架构**：核心引擎与操作模块解耦，支持自定义扩展
- **防检测**：内置随机延时、智能操作间隔，模拟人类行为模式

### 1.4 参考项目
- **Qflow**：节点拖拽式流程编排、特征识图、一键打包
- **AutoTask-UI-**：PySide6 界面、多任务管理、定时调度

---

## 2. 功能需求

### 2.1 核心操作类型

| 类别 | 操作类型 | 说明 |
|------|---------|------|
| **鼠标操作** | 移动、单击、双击、右键、拖拽、滚轮 | 支持绝对/相对坐标、偏移点击 |
| **键盘操作** | 文本输入、按键、组合键、热键 | 支持随机输入间隔、防乱码模式 |
| **延时等待** | 固定等待、随机等待(1-20000毫秒) | 模拟人类操作间隔 |
| **图片识别** | 查找图片、判断是否存在、点击图片 | 支持区域搜索、置信度设置、模板/特征匹配 |
| **文字识别** | OCR识别、查找文字、读取文字 | 支持中英文 |
| **分支判断** | IF-ELSE、IF-ELIF-ELSE | 基于图片/文字/变量判断 |
| **循环控制** | FOR循环、WHILE循环 | 支持次数控制和条件循环 |
| **数据操作** | 读取Excel、设置变量、获取变量 | 支持参数化输入 |
| **文件操作** | 截图保存、文件读写、目录操作 | 支持日志记录 |

### 2.2 关键特性

#### 2.2.1 Excel数据驱动
- 步骤可读取 Excel 单元格作为输入参数
- 支持 `${EXCEL:Sheet1!A1}` 格式引用
- 支持批量数据循环处理

#### 2.2.2 后台执行支持
- 支持在后台窗口执行鼠标点击和键盘输入
- 基于 `pydirectinput` 实现游戏级操作
- 支持窗口句柄绑定

#### 2.2.3 随机等待时间
- 每个步骤可配置 1-20000毫秒 随机等待
- 支持最小/最大等待时间设置
- 支持全局随机系数配置

#### 2.2.4 变量参数传递
- 步骤间可设置和传递变量
- 支持变量类型：字符串、数字、布尔值、列表
- 支持变量表达式计算

#### 2.2.5 定时调度
- 单次执行
- 每日定时执行
- 循环间隔执行

---

## 3. 架构设计

### 3.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        PySide6 GUI 界面层                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ 步骤编辑器    │  │ 流程管理面板  │  │ 执行监控与日志面板    │   │
│  │ (StepEditor) │  │ (FlowManager)│  │ (MonitorPanel)       │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ 属性配置面板  │  │ 工具箱面板    │  │ 定时调度面板         │   │
│  │ (Property    │  │ (Toolbox)    │  │ (SchedulerPanel)     │   │
│  │  Panel)      │  │              │  │                      │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                       核心引擎层 CoreEngine                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ 流程解析器    │  │ 步骤执行器    │  │ 变量管理器           │   │
│  │ (FlowParser) │  │ (StepRunner) │  │ (VariableManager)    │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│  ┌──────────────┐  ┌──────────────┐                             │
│  │ 定时调度器    │  │ 日志记录器    │                             │
│  │ (Scheduler)  │  │ (Logger)     │                             │
│  └──────────────┘  └──────────────┘                             │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                        操作层 Operations                         │
│  ┌────────┐ ┌────────┐ ┌──────────┐ ┌──────┐ ┌───────┐ ┌─────┐ │
│  │ Mouse  │ │ Keybo  │ │ Image   │ │ OCR  │ │ Excel │ │ File│ │
│  │ Ctrl   │ │ ard    │ │ Match   │ │ Eng  │ │ Reader│ │ Ops │ │
│  └────────┘ └────────┘ └──────────┘ └──────┘ └───────┘ └─────┘ │
│  ┌────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │ Window │ │ Condition│ │ LoopCtrl │ │ Clipboard│             │
│  │ Ctrl   │ │  (判断)  │ │ (循环)   │ │ (剪贴板) │             │
│  └────────┘ └──────────┘ └──────────┘ └──────────┘             │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    底层依赖 (pyautogui/opencv/openpyxl)          │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 模块职责

| 模块 | 职责 |
|------|------|
| **GUI层** | 用户交互、流程可视化编辑、执行监控 |
| **FlowParser** | JSON流程文件解析、步骤校验、变量解析 |
| **StepRunner** | 步骤执行引擎、流程控制、异常处理 |
| **VariableManager** | 全局变量管理、Excel数据读取、表达式计算 |
| **Scheduler** | 定时任务调度、执行计划管理 |
| **MouseCtrl** | 鼠标移动、点击、拖拽、滚轮操作 |
| **KeyboardCtrl** | 键盘输入、按键、组合键操作 |
| **ImageMatch** | 图片识别、模板匹配、特征匹配 |
| **OCREngine** | OCR文字识别、文字定位 |
| **ExcelReader** | Excel文件读取、数据提取 |
| **WindowCtrl** | 窗口管理、后台执行、句柄操作 |

---

## 4. 数据结构设计

### 4.1 流程文件格式 (JSON)

```json
{
  "name": "示例流程",
  "version": "1.0",
  "description": "登录系统并提交表单",
  "global_config": {
    "random_wait_min": 1,
    "random_wait_max": 3,
    "default_confidence": 0.85,
    "fail_safe_enabled": true
  },
  "variables": {
    "username": "${EXCEL:Sheet1!A1}",
    "password": "${EXCEL:Sheet1!B1}",
    "url": "https://example.com/login"
  },
  "steps": [
    {
      "id": "step_1",
      "type": "mouse_click",
      "name": "点击登录按钮",
      "config": {
        "click_type": "left",
        "target_type": "image",
        "image_path": "resources/login_btn.png",
        "confidence": 0.85,
        "region": [0, 0, 1920, 1080],
        "offset_x": 0,
        "offset_y": 0
      },
      "wait_before": {
        "type": "random",
        "min": 1,
        "max": 3
      },
      "wait_after": 1,
      "next_step": "step_2"
    },
    {
      "id": "step_2",
      "type": "keyboard_type",
      "name": "输入用户名",
      "config": {
        "text": "${username}",
        "interval": 0.1,
        "anti_detection": true
      },
      "next_step": "step_3"
    },
    {
      "id": "step_3",
      "type": "if_else",
      "name": "判断登录成功",
      "config": {
        "condition": {
          "type": "image_exists",
          "image_path": "resources/success.png",
          "confidence": 0.9,
          "timeout": 10
        },
        "if_true": "step_4",
        "if_false": "step_5"
      }
    },
    {
      "id": "step_4",
      "type": "log",
      "name": "登录成功",
      "config": {
        "message": "登录成功，继续执行后续操作",
        "level": "info"
      },
      "next_step": null
    },
    {
      "id": "step_5",
      "type": "log",
      "name": "登录失败",
      "config": {
        "message": "登录失败，退出流程",
        "level": "error"
      },
      "next_step": null
    }
  ]
}
```

### 4.2 步骤类型配置

#### 4.2.1 鼠标操作 (mouse_click)
```json
{
  "type": "mouse_click",
  "config": {
    "click_type": "left",
    "target_type": "coordinate",
    "x": 500,
    "y": 300,
    "offset_x": 10,
    "offset_y": 10
  }
}
```

#### 4.2.2 键盘输入 (keyboard_type)
```json
{
  "type": "keyboard_type",
  "config": {
    "text": "Hello World",
    "interval": 0.1,
    "anti_detection": true,
    "use_paste": false
  }
}
```

#### 4.2.3 图片识别 (image_find)
```json
{
  "type": "image_find",
  "config": {
    "image_path": "target.png",
    "confidence": 0.85,
    "region": [0, 0, 1920, 1080],
    "match_method": "template",
    "timeout": 10,
    "scroll_if_not_found": true
  }
}
```

#### 4.2.4 分支判断 (if_else)
```json
{
  "type": "if_else",
  "config": {
    "condition": {
      "type": "image_exists",
      "image_path": "success.png",
      "confidence": 0.9
    },
    "if_true": "step_success",
    "if_false": "step_fail"
  }
}
```

#### 4.2.5 循环控制 (loop)
```json
{
  "type": "loop",
  "config": {
    "loop_type": "for",
    "count": 5,
    "steps": ["step_a", "step_b"],
    "break_condition": {
      "type": "image_exists",
      "image_path": "exit.png"
    }
  }
}
```

---

## 5. 界面设计

### 5.1 主界面布局

```
┌─────────────────────────────────────────────────────────────────┐
│  菜单栏  │  工具栏(新建/打开/保存/运行/停止)  │  状态栏           │
├──────────┼──────────────────────────────────────┼────────────────┤
│          │                                      │                │
│  工具箱  │                                      │                │
│  (步骤   │                                      │                │
│   类型)  │        步骤编辑区域                   │   属性面板      │
│          │   (表格/节点列表)                     │   (配置参数)    │
│          │                                      │                │
│          │                                      │                │
├──────────┼──────────────────────────────────────┼────────────────┤
│          │              日志输出区域                            │
└──────────┴──────────────────────────────────────────────────────┘
```

### 5.2 工具箱面板

| 分组 | 步骤类型 | 图标 |
|------|---------|------|
| **基础操作** | 鼠标点击、键盘输入、延时等待、截图 | 🖱️ ⌨️ ⏱️ 📸 |
| **视觉识别** | 图片查找、文字识别、颜色检测 | 🔍 📝 🎨 |
| **流程控制** | IF判断、循环、跳转、日志 | 🔀 🔄 ➡️ 📋 |
| **数据操作** | 读取Excel、设置变量、获取变量 | 📊 💾 📥 |
| **窗口操作** | 窗口查找、窗口激活、后台执行 | 🪟 ✅ 🔙 |

### 5.3 步骤编辑区域

采用表格形式展示步骤列表：

| 列名 | 说明 |
|------|------|
| 序号 | 步骤顺序编号 |
| 类型 | 步骤类型图标 |
| 名称 | 步骤名称 |
| 配置 | 简要配置信息 |
| 等待前 | 执行前等待时间 |
| 等待后 | 执行后等待时间 |
| 操作 | 编辑/删除/上移/下移 |

---

## 6. 核心引擎设计

### 6.1 流程执行引擎

```python
class FlowEngine:
    def __init__(self):
        self.variable_manager = VariableManager()
        self.logger = Logger()
        self.is_running = False
        self.current_step = None
    
    def load_flow(self, file_path):
        """加载流程文件"""
    
    def set_excel_data(self, excel_path):
        """设置Excel数据源"""
    
    def run(self):
        """执行流程"""
    
    def stop(self):
        """停止流程"""
    
    def execute_step(self, step):
        """执行单个步骤"""
    
    def resolve_variables(self, text):
        """解析变量表达式"""
```

### 6.2 步骤执行器

```python
class StepRunner:
    def __init__(self, engine):
        self.engine = engine
    
    def run_mouse_click(self, config):
        """执行鼠标点击"""
    
    def run_keyboard_type(self, config):
        """执行键盘输入"""
    
    def run_image_find(self, config):
        """执行图片查找"""
    
    def run_if_else(self, config):
        """执行分支判断"""
    
    def run_loop(self, config):
        """执行循环"""
    
    def run_wait(self, config):
        """执行等待"""
```

### 6.3 变量管理器

```python
class VariableManager:
    def __init__(self):
        self.variables = {}
        self.excel_data = {}
    
    def load_excel(self, file_path):
        """加载Excel数据"""
    
    def get_variable(self, name):
        """获取变量值"""
    
    def set_variable(self, name, value):
        """设置变量值"""
    
    def resolve_expression(self, expr):
        """解析表达式"""
    
    def parse_excel_reference(self, ref):
        """解析Excel引用"""
```

---

## 7. 操作模块设计

### 7.1 鼠标操作模块

```python
class MouseController:
    def click(self, x, y, click_type="left", offset_x=0, offset_y=0):
        """点击指定坐标"""
    
    def move(self, x, y, duration=0.5):
        """移动鼠标到指定坐标"""
    
    def drag(self, start_x, start_y, end_x, end_y, duration=0.5):
        """拖拽操作"""
    
    def scroll(self, clicks, x=None, y=None):
        """滚轮滚动"""
    
    def right_click(self, x, y):
        """右键点击"""
    
    def double_click(self, x, y):
        """双击"""
    
    def get_position(self):
        """获取当前鼠标位置"""
```

### 7.2 图片识别模块

```python
class ImageMatcher:
    def __init__(self):
        self.method = "template"
        self.default_confidence = 0.85
    
    def find_image(self, template_path, region=None, confidence=None):
        """在屏幕上查找图片"""
    
    def image_exists(self, template_path, region=None, confidence=None):
        """判断图片是否存在"""
    
    def find_all_images(self, template_path, region=None, confidence=None):
        """查找所有匹配的图片"""
    
    def click_image(self, template_path, region=None, confidence=None):
        """查找并点击图片"""
    
    def get_image_position(self, template_path, region=None, confidence=None):
        """获取图片位置"""
    
    def match_template(self, screenshot, template, confidence):
        """模板匹配"""
    
    def match_feature(self, screenshot, template, confidence):
        """特征匹配(AKAZE)"""
```

### 7.3 键盘操作模块

```python
class KeyboardController:
    def type_text(self, text, interval=0.1, anti_detection=False):
        """输入文本"""
    
    def press_key(self, key):
        """按下单个按键"""
    
    def hotkey(self, *keys):
        """按下组合键"""
    
    def key_down(self, key):
        """按住按键"""
    
    def key_up(self, key):
        """释放按键"""
    
    def type_safe(self, text):
        """安全输入模式(防乱码)"""
    
    def paste_text(self, text):
        """通过剪贴板粘贴文本"""
```

### 7.4 Excel读取模块

```python
class ExcelReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.workbook = None
    
    def open(self):
        """打开Excel文件"""
    
    def close(self):
        """关闭Excel文件"""
    
    def get_sheet_names(self):
        """获取所有工作表名称"""
    
    def read_cell(self, sheet_name, cell_ref):
        """读取单元格值"""
    
    def read_range(self, sheet_name, start_cell, end_cell):
        """读取单元格范围"""
    
    def read_row(self, sheet_name, row_num):
        """读取整行"""
    
    def read_column(self, sheet_name, column_num):
        """读取整列"""
    
    def get_row_count(self, sheet_name):
        """获取行数"""
    
    def get_column_count(self, sheet_name):
        """获取列数"""
```

---

## 8. 项目结构

```
autoflow/
├── main.py                    # 入口文件
├── core/                      # 核心引擎
│   ├── __init__.py
│   ├── engine.py              # 流程引擎
│   ├── parser.py              # JSON解析器
│   ├── variables.py           # 变量管理
│   ├── scheduler.py           # 定时调度
│   └── logger.py              # 日志记录
├── operations/                # 操作模块
│   ├── __init__.py
│   ├── mouse.py               # 鼠标操作
│   ├── keyboard.py            # 键盘操作
│   ├── image_match.py         # 图片识别
│   ├── ocr_engine.py          # OCR识别
│   ├── excel_reader.py        # Excel读取
│   ├── file_ops.py            # 文件操作
│   ├── window_ctrl.py         # 窗口控制
│   ├── clipboard.py           # 剪贴板操作
│   └── conditions.py          # 条件判断
├── gui/                       # PySide6界面
│   ├── __init__.py
│   ├── main_window.py         # 主窗口
│   ├── step_editor.py         # 步骤编辑器
│   ├── property_panel.py      # 属性配置面板
│   ├── toolbox.py             # 工具箱
│   ├── monitor_panel.py       # 监控面板
│   ├── flow_manager.py        # 流程管理
│   ├── scheduler_dialog.py    # 定时调度对话框
│   └── widgets/               # 自定义控件
│       ├── __init__.py
│       ├── step_table.py      # 步骤表格
│       ├── image_picker.py    # 图片选择器
│       └── variable_editor.py # 变量编辑器
├── plugins/                   # 插件目录
│   ├── __init__.py
│   └── example_plugin.py      # 示例插件
├── resources/                 # 资源文件
│   ├── icons/                 # 图标资源
│   └── templates/             # 模板文件
├── tests/                     # 测试代码
│   ├── __init__.py
│   ├── test_engine.py         # 引擎测试
│   ├── test_image_match.py    # 图片识别测试
│   ├── test_mouse.py          # 鼠标操作测试
│   └── test_excel.py          # Excel读取测试
├── docs/                      # 文档
├── requirements.txt           # 依赖清单
└── setup.py                   # 打包配置
```

---

## 9. 依赖清单

| 依赖 | 版本 | 用途 |
|------|------|------|
| `PySide6` | >=6.5.0 | GUI界面 |
| `pyautogui` | >=0.9.54 | 前台鼠标键盘操作 |
| `pydirectinput` | >=1.0.4 | 游戏/后台操作 |
| `opencv-python` | >=4.8.0 | 图片识别匹配 |
| `easyocr` | >=1.7.0 | OCR文字识别 |
| `openpyxl` | >=3.1.0 | Excel读写 |
| `numpy` | >=1.24.0 | 图像处理 |
| `Pillow` | >=10.0.0 | 截图处理 |
| `mss` | >=10.0.0 | 高性能截图 |
| `APScheduler` | >=3.10.0 | 定时调度 |
| `pyperclip` | >=1.8.2 | 剪贴板操作 |

---

## 10. 关键设计决策

### 10.1 图片识别策略
- **默认模板匹配**：OpenCV `matchTemplate`，速度快，适合简单场景
- **特征匹配降级**：AKAZE 特征点匹配，抗形变能力强，作为备用方案
- **灰度匹配优化**：提高 30% 匹配速度

### 10.2 防检测机制
- **随机输入间隔**：每个字符输入间隔随机化
- **随机等待时间**：步骤间等待时间随机化(1-10秒)
- **缓动鼠标移动**：模拟人类鼠标移动轨迹
- **剪贴板粘贴**：支持通过剪贴板粘贴文本，避免输入法问题

### 10.3 错误处理策略
- **图片未找到**：支持超时重试、滚动查找、默认坐标
- **步骤失败**：支持跳过、重试、终止流程
- **异常捕获**：全局异常捕获，记录详细日志

### 10.4 性能优化
- **截图缓存**：复用截图，避免重复截取
- **区域限制**：支持限定搜索区域，减少计算量
- **异步执行**：IO操作异步化，不阻塞UI

---

## 11. 开发路线图

| 阶段 | 功能 | 时间 |
|------|------|------|
| **Phase 1** | 基础框架搭建、GUI界面、核心引擎 | 2周 |
| **Phase 2** | 鼠标操作、键盘操作、延时等待 | 2周 |
| **Phase 3** | 图片识别、OCR识别、条件判断 | 3周 |
| **Phase 4** | 循环控制、变量管理、Excel读取 | 2周 |
| **Phase 5** | 定时调度、后台执行、打包发布 | 2周 |
| **Phase 6** | 插件系统、性能优化、文档完善 | 2周 |

---

## 12. 测试计划

### 12.1 单元测试
- 鼠标操作测试：点击、移动、拖拽
- 键盘操作测试：文本输入、组合键
- 图片识别测试：模板匹配、特征匹配
- Excel读取测试：单元格读取、范围读取
- 变量解析测试：表达式计算、Excel引用

### 12.2 集成测试
- 完整流程执行测试
- 条件分支测试
- 循环控制测试
- Excel数据驱动测试

### 12.3 性能测试
- 图片识别速度测试
- 流程执行效率测试
- 内存占用测试

---

## 13. 打包与部署

### 13.1 打包命令
```bash
pyinstaller -F -w -i resources/icons/app.ico --add-data "resources;resources" --name AutoFlow main.py
```

### 13.2 发布格式
- Windows：`AutoFlow.exe`
- 绿色便携：无需安装，解压即用

---

## 14. 代码规范

- **命名规范**：类名使用 PascalCase，函数名使用 snake_case
- **代码风格**：遵循 PEP8 规范
- **类型提示**：使用 Python 类型注解
- **文档注释**：每个函数/类添加 docstring
- **错误处理**：统一异常处理，记录详细日志

---

## 15. 安全考虑

- **防多开保护**：同一流程只允许运行一个实例
- **紧急退出**：鼠标移动到屏幕角落或按快捷键终止
- **日志脱敏**：敏感信息（密码等）不记录到日志
- **依赖校验**：启动时校验所有依赖是否安装

---

## 16. 扩展计划

### 16.1 插件系统
- 支持自定义步骤类型
- 支持第三方操作模块集成
- 插件市场与共享机制

### 16.2 AI 增强
- AI 智能找图（基于大模型）
- 自然语言生成流程
- AI 错误诊断与修复

### 16.3 远程控制
- Web 远程管理界面
- 手机端控制
- 多设备协同
