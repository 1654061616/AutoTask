# 连线控制点可拖动调整 — 设计文档

**日期：** 2026-07-20
**状态：** 已批准

## 1. 需求

- 连线（贝塞尔曲线）的两个控制点可以手动拖动调整位置（X/Y 自由移动）
- 调整后曲线弧度柔和，避免突兀回折
- 交叉回流连线可分别调整控制点，让交叉点落在网格空白处，避免线条重叠粘连
- 控制点位置持久化到 JSON，加载后恢复

## 2. 方案选型

选用 **方案 A：控制点手柄作为 EdgeWidget 的子项**。

| 方案 | 描述 | 选择 |
|------|------|------|
| A | ControlPointHandle 作为 EdgeWidget 的子图形项，偏移量存储 | ✅ 选用 |
| B | 场景级别的控制点代理，独立生命周期 | ❌ 太复杂 |
| C | 在边路径上直接拖拽"捏"曲线 | ❌ 不够精确 |

选用理由：与现有 PortWidget 作为 NodeWidget 子项的模式一致，改动集中在 EdgeWidget 一个文件。

## 3. 架构

### 3.1 新增 ControlPointHandle 类

位于 `edge_widget.py`，作为 EdgeWidget 的内部类或独立类。

```
ControlPointHandle(QGraphicsObject)
├── 直径 10px 圆形，填充 #ffaa00，半透明
├── 选中边时 setVisible(True)，取消选中时 setVisible(False)
├── ItemIsMovable + ItemSendsGeometryChanges
├── itemChange(ItemPositionHasChanged) → 更新偏移量 + 调用 edge.update_path()
└── 手柄位置以场景坐标存储
```

### 3.2 EdgeWidget 修改

| 新增属性 | 类型 | 说明 |
|----------|------|------|
| `_cp1_handle` | ControlPointHandle | 控制点 1 手柄 |
| `_cp2_handle` | ControlPointHandle | 控制点 2 手柄 |
| `_cp1_offset` | tuple(float, float) | 控制点 1 偏移比例，默认 (0.25, 0) |
| `_cp2_offset` | tuple(float, float) | 控制点 2 偏移比例，默认 (0.75, 0) |

| 修改方法 | 改动 |
|----------|------|
| `__init__` | 创建两个 ControlPointHandle，初始隐藏 |
| `update_path()` | 从偏移量计算实际控制点坐标，传给 cubicTo |
| `itemChange(ItemSelectedChange)` | 选中时显示手柄，取消选中时隐藏 |
| `to_json()` | 增加 cp1/cp2 偏移量 |
| 新增 `from_json()` | 恢复 cp1/cp2 偏移量 |
| 新增 `_update_handles()` | 根据偏移量 + 端口位置重新计算手柄场景坐标 |

**手柄位置计算公式：**
```
vector = end_port_global - start_port_global
handle_global = start_port_global + vector * (offset_x, offset_y)
```

其中默认偏移量 `cp1=(0.25, 0)`, `cp2=(0.75, 0)`，与当前自动计算的控制点行为一致。

## 4. 数据流

### 4.1 保存
```
EdgeWidget.to_json()
  → {
      source_node, source_port, target_node, target_port,
      cp1: { x: 0.25, y: 0.0 },
      cp2: { x: 0.75, y: 0.0 }
    }
  → GraphScene.to_json()
  → task_manager 写入 JSON 文件
```

### 4.2 加载
```
JSON 文件 → task_manager → GraphScene.from_json() / load_nodes_from_flow()
  → add_edge() → EdgeWidget.__init__()
  → edge.from_json(data) 恢复 cp1/cp2 偏移量
  → update_path() + _update_handles()
```

### 4.3 节点移动
```
NodeWidget.itemChange(ItemPositionChange)
  → port.itemChange → edge.update_path()
  → update_path() 根据偏移量 + 新端口位置重新计算控制点
  → _update_handles() 同步手柄位置
```

### 4.4 手柄拖动
```
ControlPointHandle.itemChange(ItemPositionHasChanged)
  → 从手柄场景坐标反算偏移比例
  → 更新 _cp1_offset / _cp2_offset
  → edge.update_path()
```

## 5. 边界情况

| 场景 | 处理 |
|------|------|
| 手柄拖到很远 | 不限制，偏移比例可超出 0~1 范围 |
| 删除连线 | 手柄随 EdgeWidget 一起销毁 |
| 删除节点 | GraphScene 先删边再删节点，手柄自然销毁 |
| 缩放画布 | 偏移量以比例存储，缩放不变形 |
| 连线未选中 | 手柄隐藏，不可交互 |
| 手柄被其他图形覆盖 | 设置 ZValue 确保在最上层 |

## 6. 测试策略

| 测试 | 验证点 |
|------|--------|
| ControlPointHandle 创建 | EdgeWidget 创建时包含两个手柄，初始隐藏 |
| 选中可见性 | 选中边时手柄可见，取消选中时隐藏 |
| 手柄拖动 | 拖动手柄后曲线路径更新 |
| 持久化 | to_json/from_json 包含控制点偏移量 |
| 节点跟随 | 移动节点后手柄位置更新 |

## 7. 修改文件清单

| 文件 | 改动 |
|------|------|
| `gui/node_graph/edge_widget.py` | 新增 ControlPointHandle 类，修改 EdgeWidget |
| `tests/test_edge_widget.py` | 新增控制点相关测试 |