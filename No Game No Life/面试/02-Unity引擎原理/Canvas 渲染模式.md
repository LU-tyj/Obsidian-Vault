---
title: "Canvas 渲染模式"
category: Unity引擎原理
tags: [Unity, Csharp, 网易互娱, UGUI, Canvas]
frequency: ⭐
difficulty: 简单
companies: [网易互娱]
status: new
last_reviewed:
next_review:
related:
  - "[[UGUI 性能优化]]"
  - "[[坐标系统与向量运算]]"
---

## 一句话结论（自测用）
> Canvas 三种渲染模式：Screen Space - Overlay（永远最上层的 HUD）、Screen Space - Camera（绑定相机，受后处理影响）、World Space（世界中 3D UI）。选择依据：是否需要透视效果、是否受光照影响、是否固定在屏幕。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **Screen Space - Overlay**：
   - UI 始终渲染在屏幕最上层，不受任何相机影响
   - 不需要指定相机
   - **自动适配屏幕分辨率**
   - 适用：HUD、血条、状态栏
2. **Screen Space - Camera**：
   - UI 绑定到指定相机，渲染位置相对于该相机
   - 受相机的后处理、裁剪面等影响
   - 可以和其他 3D 物体有正确的深度关系
   - 适用：需要后处理效果的 UI、和 3D 场景混合的 UI
3. **World Space**：
   - UI 作为世界中的 3D 物体存在
   - 可以被遮挡、可以有透视效果
   - 适用：游戏中的漂浮文字、NPC 头顶标识、场景中的交互提示

## 详细解析

### 如何选择渲染模式
| 需求 | 推荐模式 |
|------|---------|
| 标准 HUD 界面 | Overlay |
| UI 需要 Bloom/模糊等后处理 | Camera |
| 需要 3D UI 在世界中 | World Space |
| UI 和 3D 物体有明显遮挡关系 | Camera 或 World Space |
| 固定屏幕位置不随相机移动 | Overlay |

### Screen Space - Camera 的关键设置
- `Render Camera`：指定渲染 UI 的相机
- `Plane Distance`：UI 平面距离相机的距离，影响 UI 和 3D 物体的遮挡关系
- `Sorting Layer`：控制 UI 和其他渲染物体的层级

## 面试官常见追问
- Overlay 和 Camera 在性能上有差异吗？（Overlay 略快，因为少一次相机裁剪计算；实际差异很小）
- World Space UI 能合批吗？（能，同 Canvas + 同材质 + 同纹理仍然可以合批）
- 多个 Canvas 的渲染顺序怎么控制？（Sort Order 或 Sorting Layer）

## 关联知识点
- [[UGUI 性能优化]]
- [[坐标系统与向量运算]]

## 原始出处
- GitHub面经_Unity引擎 Q12
