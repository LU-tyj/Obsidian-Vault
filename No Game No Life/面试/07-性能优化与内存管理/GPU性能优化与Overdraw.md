---
title: "GPU性能优化与Overdraw"
category: 性能优化与内存管理
tags: [性能优化, GPU, Overdraw, LOD, 分辨率缩放, 阴影优化, Shader优化, 网易互娱]
frequency: ⭐⭐
difficulty: 中等
companies: [网易互娱]
status: new
last_reviewed:
next_review:
related:
  - "[[DrawCall优化与合批策略]]"
  - "[[LOD与细节层次]]"
  - "[[内存优化策略]]"
---

## 🎯 一句话结论（自测用）
> GPU 优化的六大方向：分辨率缩放（移动端最有效）、LOD 降模、减少后处理、减少 Overdraw、Shader 优化（用 half 替代 float）、控制实时阴影。Overdraw 优化通过合理渲染顺序（不透明从前往后、透明从后往前）和遮挡剔除实现。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **分辨率缩放**：移动端最有效的 GPU 优化手段，动态调整渲染分辨率。
2. **LOD**：远处物体使用低面数模型，减少顶点和片元处理量。
3. **后处理轻量化**：关闭不必要的后处理效果，或降低 Bloom/DOF 的分辨率和 Pass 次数。
4. **减少 Overdraw**：避免大量半透明物体重叠绘制。
   - 不透明物体从前往后渲染（利用 Early-Z 剔除）
   - 透明物体从后往前渲染（确保混合正确）
   - 使用遮挡剔除减少不可见物体绘制
   - UI 减少重叠、关闭不必要的 Raycast Target
5. **Shader 优化**：用 half/fixed 代替 float（移动端），减少纹理采样次数、避免复杂数学运算。
6. **实时阴影控制**：降低阴影分辨率、减少投射距离和投射物体数量、用静态烘焙替代实时阴影。

## 🔍 详细解析

### 不透明渲染顺序：从前往后
- 先渲染近处物体，后渲染远处物体
- 近处物体会写入深度缓冲，远处物体被深度测试剔除，节省片元着色器执行
- 这就是 Early-Z 的作用

### 透明渲染顺序：从后往前
- 透明物体不能写入深度缓冲（否则会挡住后面的透明物体）
- 必须从远处到近处逐个绘制，才能正确混合半透明颜色
- 这也是透明物体渲染的主要性能瓶颈

### Overdraw 量化
- 移动端 GPU（Tile-Based Rendering）对 Overdraw 特别敏感
- 可以通过 Unity Frame Debugger 或 RenderDoc 查看每个像素被绘制了几次
- 目标：半透明区域平均 Overdraw <= 2-3 层

### Shader 精度优化
| 类型 | 精度 | 适用场景 |
|------|------|---------|
| float | 32位 | 世界坐标、UV（桌面端） |
| half | 16位 | 颜色、方向向量（移动端优先） |
| fixed | 11位 | 简单颜色（已不常用） |

### 阴影优化策略
- Shadow Distance：控制阴影投射的最远距离
- Shadow Cascades：控制级联数量（移动端 0-2 级）
- Shadow Resolution：降低 ShadowMap 分辨率
- 静态物体使用烘焙 Lightmap 代替实时阴影

## 💬 面试官常见追问
- **移动端为什么不用全屏后处理？** → Tile-Based GPU 架构下全屏 Pass 会产生大量带宽开销
- **Overdraw 怎么看？** → Frame Debugger 或 RenderDoc 抓帧，看半透明区域渲染了几层
- **Alpha Test 为什么影响 Early-Z？** → Alpha Test 在片元着色器中 discard 片元，而 Early-Z 发生在片元着色器之前；如果 discard 了片元，Early-Z 写入了错误的深度值，GPU 会关闭 Early-Z 优化
- **半透明物体怎么处理才好？** → 尽量减少半透明面积、使用 Alpha-to-Coverage

## ⚠️ 我曾经的误区 / 网上常见错答
- 误区：降低分辨率 = 画面质量大幅下降。实际上合理的动态分辨率 + 锐化后处理可以在视觉损失很小的情况下大幅降低 GPU 负载。
- 误区：关闭阴影即可。很多游戏的阴影是核心视觉元素，优先降分辨率而不是完全关闭。

## 🔗 关联知识点
- [[DrawCall优化与合批策略]]
- [[LOD与细节层次]]
- [[内存优化策略]]

## 📎 原始出处
- GitHub面经_性能优化 Q5/Q7：GPU 优化方向 + Overdraw 优化
- 牛客网 013 Q5/Q6：半透明物体绘制处理 + DrawCall 优化
- 牛客网 015 Q3 剔除方式
- 优化.md：Overdraw / 后处理 / 阴影优化要点
