# Bug修复历史记录

## 概述

本文档记录了AutoFlow项目中最近的问题修复和功能改进，特别是涉及屏幕坐标选择和截图功能的相关问题。

---

## 问题列表

### 1. 坐标选择向左偏移问题

**问题描述**：选择屏幕坐标时，返回的坐标向左偏移约20px

**问题原因**：
- `GetCursorPos` 返回物理像素坐标
- Qt 的 `setGeometry` 在高 DPI 环境下使用逻辑坐标
- 两者不一致导致坐标偏移（125% DPI 缩放时约偏移20px）

**解决方案**：
1. 使用 `SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)` 设置进程级 DPI 感知（非弃用方法）
2. 使用 `pyautogui.position()` 获取坐标，与执行引擎使用同一套坐标系统
3. 使用 `QApplication.screens()` 获取屏幕尺寸，支持多显示器环境

**修改文件**：
- `main.py` - 添加进程级 DPI 感知设置
- `gui/step_panels/__init__.py` - 使用 pyautogui 获取坐标

**提交哈希**：`018560c`

---

### 2. 截图区域与选择区域坐标偏移问题

**问题描述**：截图区域与用户选择的区域坐标不一致

**问题原因**：DPI 缩放导致坐标系统不一致

**解决方案**：分离坐标系统，使用窗口局部坐标进行覆盖层绘制，使用 Windows API 屏幕坐标进行实际图像捕获

**修改文件**：`gui/step_panels/__init__.py`

**提交哈希**：`d1f5ffd`

---

### 3. 覆盖层框选区域与鼠标拖拽偏移问题

**问题描述**：覆盖层上出现的框选区域与鼠标拖拽位置有偏移

**问题原因**：坐标转换逻辑不一致

**解决方案**：统一坐标系统，确保框选区域和鼠标位置使用相同的坐标基准

**修改文件**：`gui/step_panels/__init__.py`

**提交哈希**：`312a2af`

---

### 4. 拖拽截图功能失效问题

**问题描述**：无法通过拖拽截图

**问题原因**：覆盖层点击事件处理逻辑错误

**解决方案**：修复鼠标事件处理，确保拖拽操作能够正常识别和处理

**修改文件**：`gui/step_panels/__init__.py`

**提交哈希**：`7f58d06`

---

### 5. 截图区域坐标偏移问题

**问题描述**：截图区域坐标与实际选择区域不一致

**问题原因**：DPI 缩放导致的坐标映射错误

**解决方案**：使用 Windows API 获取物理像素坐标进行截图

**修改文件**：`gui/step_panels/__init__.py`

**提交哈希**：`2e9344d`

---

### 6. 覆盖层未盖满屏幕问题

**问题描述**：全屏半透明覆盖层未覆盖整个屏幕

**问题原因**：屏幕尺寸计算错误

**解决方案**：使用 `QApplication.screens()` 获取所有屏幕的几何信息，确保覆盖层覆盖整个虚拟屏幕

**修改文件**：`gui/step_panels/__init__.py`

---

### 7. 删除mouse_panel中图片位置相关功能

**问题描述**：mouse_panel.py中包含不需要的图片位置选择功能

**解决方案**：删除图片位置相关代码，包括图片路径、相似度滑块、查找范围等控件

**修改文件**：`gui/step_panels/mouse_panel.py`

**提交哈希**：`4f92802`

---

### 8. QCheckBox样式表解析错误

**问题描述**：节点编辑器点击找图节点时，终端打印 "Could not parse stylesheet of object QCheckBox" 错误

**问题原因**：代码中使用了 `QCheckBox { spacing: 8px; }`，但 `spacing` 不是 Qt Style Sheet 支持的属性，导致样式表解析失败

**解决方案**：移除所有文件中无效的 QCheckBox 样式表设置

**修改文件**：
- `gui/step_panels/image_panel.py`
- `gui/step_panels/window_panel.py`
- `gui/step_panels/keyboard_panel.py`
- `gui/step_panels/control_panel.py`
- `gui/step_panels/mouse_panel.py`

**提交哈希**：`914cf82`

---

## 技术要点

### DPI感知设置

在 `main.py` 中添加进程级 DPI 感知设置：

```python
if platform.system() == "Windows":
    try:
        DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = 0x00000022
        ctypes.windll.user32.SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)
    except:
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except:
                pass
```

### 坐标获取方式

使用 `pyautogui.position()` 获取坐标，与执行引擎使用同一套坐标系统：

```python
def mousePressEvent(self, event):
    if event.button() == Qt.LeftButton:
        x, y = pyautogui.position()
        self.coordinate_selected.emit(x, y)
        self._cleanup()
```

### 屏幕尺寸获取

使用 `QApplication.screens()` 获取屏幕尺寸，支持多显示器环境：

```python
def showEvent(self, event):
    screens = QApplication.screens()
    min_x = min(s.geometry().left() for s in screens)
    min_y = min(s.geometry().top() for s in screens)
    max_x = max(s.geometry().right() for s in screens)
    max_y = max(s.geometry().bottom() for s in screens)
    self.setGeometry(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)
```

---

## 跨平台支持

- **Windows**：使用 `SetProcessDpiAwarenessContext` 设置 DPI 感知，使用 `pyautogui` 获取坐标
- **Linux**：无需额外设置 DPI 感知，`pyautogui` 和 Qt 自动处理

---

## 总结

这些问题主要集中在高 DPI 环境下的坐标系统一致性问题。核心解决方案是：
1. 设置进程级 DPI 感知
2. 使用同一套工具获取和使用坐标（`pyautogui`）
3. 确保覆盖层尺寸和坐标获取使用相同的坐标系统
