---
title: "UI优化策略"
category: 性能优化与内存管理
tags: [性能优化, UI优化, UGUI, Canvas, Overdraw, 网易互娱]
frequency: ⭐⭐
difficulty: 中等
companies: [网易互娱]
status: new
last_reviewed:
next_review:
related:
  - "[[DrawCall优化与合批策略]]"
  - "[[GPU性能优化与Overdraw]]"
---

## 🎯 一句话结论（自测用）
> UI 优化的七大策略：动静分离（不同 Canvas）、图集化、RectMask2D 替代 Mask、关闭不必要的 Raycast Target、TMP 替代 Text、ScrollView 对象池、控制 Canvas 数量。核心原则：减少 Canvas 重建频率（Rebuild）和降低 UI 的 Overdraw。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **动静分离**：将频繁变化的 UI（如血条、计时器）和静态 UI（如背景、边框）放在不同 Canvas 下。动态 Canvas 变化时只重建自己的网格，不影响静态部分。
2. **图集化**：同一界面的 UI 元素整合为一张图集（Sprite Atlas），同一材质即可合批。
3. **Mask 优化**：使用 RectMask2D 替代 Mask。Mask 使用模板测试（Stencil），会产生额外的 DrawCall；RectMask2D 只裁剪矩形区域，不增加 DrawCall。
4. **关闭不必要的 Raycast Target**：不需要点击交互的 UI 元素（纯装饰图片、文字）关闭 Raycast Target，减少事件系统的射线检测开销。
5. **TMP 替代 Text**：TextMeshPro 生成的顶点数更少（比原生 Text 少约 50%），且支持更丰富的文字效果。
6. **ScrollView 对象池**：滚动列表只实例化可见区域的 Cell，滚动时复用。避免几千个 Item 同时存在。
7. **控制 Canvas 数量**：每个 Canvas 更新时都会重建整个 Canvas 的网格。一个 Canvas 内任意元素变化会触发整个 Canvas 的重建。

## 🔍 详细解析

### Canvas 重建触发条件
- Canvas 内任意元素的 Transform 发生变化
- Material/Color 变化
- 文本内容变化
- 父级 CanvasGroup Alpha 变化
- 子元素增删

### Mask vs RectMask2D
| 对比 | Mask | RectMask2D |
|------|------|-----------|
| 实现原理 | Stencil Buffer | 顶点裁剪 |
| DrawCall | 额外增加 | 不增加 |
| 裁剪形状 | 任意形状（依赖 Image） | 仅矩形 |
| 性能 | 较差 | 较好 |

### UGUI Canvas 的三种渲染模式
| 模式 | 说明 | 适用场景 |
|------|------|---------|
| Screen Space - Overlay | 直接贴在屏幕上，无需摄像机 | 常规 HUD |
| Screen Space - Camera | 3D 场景中的 UI | 需要受摄像机影响 |
| World Space | 放在 3D 世界中的 UI | 血条、头顶文字 |

### NGUI vs UGUI
- UGUI 通过 Hierarchy 顺序控制渲染层级（越下面越上层）
- NGUI 通过 Widget Depth 控制
- UGUI 使用 Sprite Atlas 替代 NGUI 的图集概念
- UGUI 是 Unity 原生支持，不需要额外的 Collider 来响应事件

## 💬 面试官常见追问
- **一个 Canvas 内 Text 变了，会影响整个 Canvas 吗？** → 会。Canvas 内任意元素变化触发整个 Canvas 的重建（Rebuild），这是必须动静分离的原因
- **为什么 RectMask2D 比 Mask 好？** → Mask 使用 Stencil Buffer 多一个 DrawCall，RectMask2D 使用顶点裁剪不增加 DrawCall；但 RectMask2D 只能裁剪矩形
- **ScrollView 对象池怎么实现？** → 监听滚动位置，计算可见区域，显示/隐藏对应 Cell，Cell 数量固定为可见数量 + 缓冲数量

## ⚠️ 我曾经的误区 / 网上常见错答
- 误区：把所有 UI 放一个 Canvas 方便管理。一个元素变化导致全部重建，浪费性能
- 误区：用很多 Canvas 来分别控制。Canvas 数量过多也有元数据开销，需要在动静分离和 Canvas 数量间取平衡
- 误区：TMP 和 Text 差不多。TMP 顶点数少约 50%，且不依赖动态字体贴图

## 🔗 关联知识点
- [[DrawCall优化与合批策略]]
- [[GPU性能优化与Overdraw]]
- [[对象池设计]]

## 📎 原始出处
- GitHub面经_性能优化 Q11：UI 优化核心策略
- 优化.md：UI 模块优化 — UWA 性能优化系列
- UnityEngine.md：UGUI 底层、Canvas 渲染模式
