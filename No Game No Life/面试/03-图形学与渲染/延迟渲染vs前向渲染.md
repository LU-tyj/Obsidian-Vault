---
title: "延迟渲染vs前向渲染"
category: 图形学与渲染
tags: [图形学, 渲染, 网易互娱]
frequency: ⭐⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[渲染管线]]"
  - "[[URP-HDRP对比]]"
  - "[[抗锯齿技术]]"
---

## 🎯 一句话结论（自测用）
> 前向渲染逐物体逐光源计算光照（O(mesh * light)），延迟渲染先写G-Buffer再屏幕空间逐光源计算（O(screen * light)）。多光源场景用延迟渲染性能更好，但移动端和需要MSAA时用前向渲染。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **前向渲染**：每个物体在同一个 Pass 中，对每个影响它的光源执行一次光照计算。
2. **延迟渲染**：分为两个阶段：
   - Geometry Pass：将几何信息（Albedo、Normal、Depth、Roughness 等）写入多张 G-Buffer
   - Lighting Pass：在屏幕空间中，对每个像素从 G-Buffer 重建材质参数，遍历光源计算光照
3. **核心优劣**：
   - 前向渲染：支持 MSAA、Shader 编写自由，但多光源时复杂度爆炸（O(n_objects * n_lights)）
   - 延迟渲染：多光源情况下效率极高（O(n_pixels * n_lights)），但不支持硬件 MSAA、G-Buffer 带宽压力大、移动端 Tile-based GPU 不太适合传统延迟渲染
4. **Forward+**：在 Forward 基础上加了一个 Light Culling Pass（用 compute shader 做 tile-based light selection），兼顾两者优点

## 🔍 详细解析

**各方案对比表**（网易面试高频）：

| 方案 | Pass数 | 多光源 | MSAA | 移动端 | 透明物体 |
|------|--------|--------|------|--------|----------|
| Forward | 1/n_lights | 差 | 支持 | 好 | 好 |
| Deferred | 2 | 极好 | 不支持(硬件) | 差 | 需额外Pass |
| Forward+ | 2 | 好 | 支持 | 可 | 好 |
| Tiled Forward | 2 | 好 | 支持 | 好 | 好 |

**为什么前向渲染支持 MSAA 而延迟渲染不支持？**
MSAA 在同一三角形内的多个采样点共享一次片元着色器计算。延迟渲染的 G-Buffer 存储的是每个像素的几何信息，MSAA 需要在 G-Buffer 写入时按采样点存储（大幅增加 G-Buffer 大小），并在光照阶段对每个采样点做光照计算，开销不可接受。

**TBR（Tile-Based Rendering）与移动端延迟渲染**：
- 移动端 GPU 多用 TBR 架构，将屏幕分成小块 tile，在片上 SRAM 中完成渲染
- 传统延迟渲染的 G-Buffer 太大可能放不进 tile memory
- Unity 在移动端不推荐延迟渲染，优先使用 Forward 或 Forward+

## 💬 面试官常见追问
- "场景复杂且有很多光源，如何优化？" -> 使用延迟渲染，或 Forward+ 的 tile-based light culling
- "为什么游戏引擎更多用前向渲染？" -> 支持 MSAA、移动端友好、透明物体处理更简单、Shader 更自由
- "延迟渲染如何处理透明物体？" -> 透明物体不写入 G-Buffer，在延迟渲染结束后再用前向渲染单独绘制
- "Forward+ 是如何做光照剔除的？" -> 将屏幕划分为 tile，用 compute shader 计算每个 tile 受哪些灯光影响，Forward pass 只计算被影响的光源

## ⚠️ 我曾经的误区 / 网上常见错答
- 误区：延迟渲染一定比前向渲染好。实际上两者各有适用场景，移动端或光源少的场景前向渲染更优
- 误区：延迟渲染不消耗带宽。实际上 G-Buffer 写入和读取消耗大量带宽，尤其在移动端

## 🔗 关联知识点
- [[渲染管线]]
- [[URP-HDRP对比]]
- [[抗锯齿技术]]
- [[PBR理论]]

## 📎 原始出处
- GitHub Q11 Q19: unitykit/unityClientInterviewGuide
- 牛客网001 Q22: 网易互娱2面 - 延迟渲染优化多光源
- 牛客网009 Q13: 延迟渲染
- 牛客网013 Q8/Q15/Q16: Forward+ vs Deferred、移动端TBR
- 牛客网015 Q13: 延迟渲染 vs 正向渲染
- 博客园: 高频考点汇总
