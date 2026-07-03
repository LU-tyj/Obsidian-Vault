---
title: "UGUI 性能优化"
category: Unity引擎原理
tags: [Unity, Csharp, 网易互娱, UGUI, 性能优化, UI]
frequency: ⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[DrawCall 优化]]"
  - "[[对象池]]"
  - "[[Canvas 渲染模式]]"
---

## 一句话结论（自测用）
> UGUI 优化核心六条：Canvas 动静分离、图集化、RectMask2D 替代 Mask、关闭不必要的 Raycast Target、用 TMP 替代 Text、ScrollView 使用对象池。每个 Canvas 的 Rebuild 是最贵的操作。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **Canvas 动静分离**：将频繁变化的 UI（血条、计时器）和静态 UI 放到**不同 Canvas** 下。因为 Canvas 中任意一个元素变化，都会导致整个 Canvas 的网格重建。
2. **图集化**：同一界面的散图整合为一张 Atlas，共享 Material，满足合批条件，减少 DrawCall。
3. **Mask vs RectMask2D**：
   - Mask：使用模板缓冲（Stencil），额外 2 个 DrawCall，不支持合批
   - RectMask2D：通过 `IClipper` 裁剪顶点，无额外 DC，只能矩形遮罩，性能远优于 Mask
4. **关闭不必要的 Raycast Target**：不需要交互的 UI（纯装饰图片、背景）关闭 `Raycast Target`，减少 EventSystem 的射线检测开销。
5. **TMP 替代 Text**：TextMeshPro 顶点数更少，支持 SDF 渲染，缩放清晰，性能更好。
6. **ScrollView 对象池**：只实例化可见区域的条目，滚动时复用。避免一次性生成数百个 item。
7. **Canvas 渲染模式**：
   - Screen Space - Overlay：UI 永远在最上层，适合 HUD
   - Screen Space - Camera：绑定相机，受相机后处理影响
   - World Space：UI 在世界空间中如 3D 物体

## 详细解析

### Canvas.Rebuild 的触发链
```
SetActive / 修改 RectTransform / 修改 Text 内容
  -> 标记为 Dirty（Layout Dirty / Graphic Dirty）
  -> CanvasUpdateRegistry 在下一帧执行 Rebuild
  -> Layout Rebuild（重新计算布局）
  -> Graphic Rebuild（重新生成网格顶点）
  -> 所有子节点的重建
```
**优化要点**：避免在 Update 中高频修改 UI 属性（如每帧改 Text 文本显示倒计时），改用事件驱动或降低更新频率（如 0.2s 更新一次）。

### 合批条件
1. 同一 Canvas
2. 相同 Material（通常来自同一 Atlas）
3. 相同纹理（同一图集）
4. 渲染层级相邻（中间不插入不同 Material 的元素）

### Raycast Target 的性能影响
每个开启 `Raycast Target` 的 Graphic 都会被 EventSystem 遍历做射线检测。关闭不需要交互的 UI 元素可以大幅减少检测次数。用 `CanvasRenderer` 的 `cull` 功能可以自动关闭不可见 UI 的 Raycast Target。

### TMP vs Text
| | Text | TextMeshPro |
|--|------|-------------|
| 顶点数（每字符） | 4 | 4（SDF 模式） |
| 缩放清晰度 | 模糊（位图） | 清晰（SDF） |
| 动态字体 | 需要 | 不需要（提前烘焙 SDF Atlas）|
| 富文本支持 | 有限 | 丰富（颜色、大小、Sprite） |

## 面试官常见追问
- 为什么 Canvas 的动静分离很重要？（任意一个元素 dirty 都会重建整个 Canvas）
- RectMask2D 有什么限制？（只能矩形裁剪，不能圆形/异形）
- UGUI 的事件系统怎么工作？（EventSystem 每帧检测输入，通过 GraphicRaycaster 做射线检测，走 IPointerXXXHandler 接口派发）
- 为什么 ScrollView 会卡？（每个 item 都参与 Layout Rebuild + Graphic Rebuild + 实例化开销）

## 我曾经的误区 / 网上常见错答
- **错**："UI 优化就是减少 DrawCall" —— 对 UGUI 来说 Canvas 重建的开销往往大于 DrawCall
- **错**："给每个 UI 加 Canvas 可以隔离变化" —— Canvas 越多，每个 Canvas 都有重建开销，需要平衡
- **错**："TMP 只是 Text 的替代，功能一样" —— TMP 的 SDF 渲染和 Sprite Asset 等特性超出 Text 很多

## 关联知识点
- [[DrawCall 优化]]
- [[对象池]]
- [[Canvas 渲染模式]]
- [[CPU与GPU优化]]

## 原始出处
- GitHub面经_Unity引擎 Q12-Q15
- GitHub面经_性能优化 Q11
- 博客园 多论坛面经汇总 3.2 节
