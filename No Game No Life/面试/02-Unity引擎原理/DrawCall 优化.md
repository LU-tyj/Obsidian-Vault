---
title: "DrawCall 优化"
category: Unity引擎原理
tags: [Unity, Csharp, 网易互娱, DrawCall, 性能优化, 渲染]
frequency: ⭐⭐⭐
difficulty: 困难
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[UGUI 性能优化]]"
  - "[[CPU与GPU优化]]"
  - "[[AssetBundle 机制]]"
---

## 一句话结论（自测用）
> DrawCall = CPU 向 GPU 发送的一次绘制指令。减少 DC 的十大方法：静态/动态合批、GPU Instancing、SRP Batcher、图集、减少 Shader Pass、遮挡剔除、LOD、合理渲染排序、UI Canvas 动静分离。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **什么是 DrawCall**：CPU 准备数据（材质、纹理、Shader、变换矩阵等），通过图形 API（DirectX/Metal/Vulkan）向 GPU 发送"Render this"指令。每次 DC 有 CPU 开销，DC 多了 CPU 成为瓶颈。
2. **减少 DrawCall 的 10 种方法**：
   1. **静态合批（Static Batching）**：标记为 Batching Static 的不动物体合并为一个 Mesh，运行时一次绘制（增加内存）
   2. **动态合批（Dynamic Batching）**：Unity 自动对小 Mesh（顶点数 < 300）做合批（有额外 CPU 开销）
   3. **GPU Instancing**：用同一 Mesh + Material 渲染大量相同物体，一次 DC 画多个（限制：同 Mesh 同材质）
   4. **SRP Batcher（URP/HDRP）**：减少材质属性设置开销，批量提交 DrawCall（不减少 DC 数量但大幅降低 CPU 开销）
   5. **图集合并**：多张散图合成一张 Atlas，共享 Material，满足合批条件
   6. **减少 Shader Pass 数量**：每个 Pass 增加一个 DC，精简 Shader
   7. **遮挡剔除（Occlusion Culling）**：摄像机看不到的物体直接不提交 DC
   8. **LOD**：远处物体用低面数 Mesh / 简化 Shader
   9. **合理渲染排序**：减少状态切换（同材质、同 Shader 的物体连续渲染）
   10. **UI 优化**：Canvas 动静分离，图集化，关闭不必要的 Raycast Target
3. **移动端 DrawCall 合理目标**：
   - 低端机 <= 100-150 Batches
   - 中端机 <= 200-300 Batches
   - 高端机 <= 400-500 Batches
   - SetPass Calls 尽量 <= 20-30

## 详细解析

### 静态合批 vs 动态合批 vs GPU Instancing vs SRP Batcher

| 技术 | 条件 | 原理 | 优点 | 缺点 |
|------|------|------|------|------|
| **Static Batching** | 标记 Batching Static，同材质 | 预合并 Mesh 到超大 Mesh | 运行时零消耗 | 额外内存（存合并 Mesh） |
| **Dynamic Batching** | 小 Mesh（<300 顶点），同材质 | 运行时每帧合并顶点 | 自动无标记 | CPU 开销（合并计算） |
| **GPU Instancing** | 同 Mesh + 同材质 | GPU 端实例化绘制 | 一次 DC 画多个 | 不能使用 MaterialPropertyBlock 变体属性（需特殊 Shader） |
| **SRP Batcher** | 同 Shader 变体 | 缓存材质属性到 GPU | 不合并 Mesh，大量减少 SetPass Call | 需要 URP/HDRP |

### 为什么这么多合批技术？
因为 SRP Batcher 解决的是 **SetPass Call**（切换 Shader/材质的开销），而传统 Batching / Instancing 解决的是 **DrawCall 数量**。两者目标不同，实际项目中叠加使用。

### Frame Debugger 定位 DC 问题
`Window -> Analysis -> Frame Debugger` 可以看到每一帧的每个 DrawCall 绘制了什么。检查：
- 是否有大量相同材质的物体没有合批（可能是 Shader 不兼容）
- 是否有未被遮挡的物体在绘制（开启 Occlusion Culling）
- UI Canvas 是否频繁重建（Canvas.BuildBatch 耗时高）

## 面试官常见追问
- 静态合批为什么会增加内存？（Unity 在内存中生成一份合并后的大 Mesh，原 Mesh 仍保留，相当于双份存储）
- GPU Instancing 和 SRP Batcher 的区别？（Instancing 减少 DC 数量，SRP Batcher 减少 DC 间的 CPU 准备开销；两者可以共存）
- 动态合批的 300 顶点限制怎么来的？（顶点属性越多则单顶点字节数越大，Unity 根据顶点缓冲区大小动态限制，300 是典型值）
- 什么情况下动态合批会失败？（Mesh 太大、材质不同、Shader 不兼容、使用 Multi-pass Shader、有 SkinnedMeshRenderer）
- 为什么不透明和透明物体合不到一起？（渲染顺序不同：不透明从前到后，透明从后到前，打断合批）

## 我曾经的误区 / 网上常见错答
- **错**："合批就是减少 DrawCall" —— SRP Batcher 不减少 DrawCall 数量，但大幅减少 CPU 准备开销，效果类似
- **错**："Batches 和 DrawCall 是一个东西" —— Unity Stats 面板的 Batches = DrawCall + SetPass Call 的总称
- **错**："标记 Static 就能合批" —— 还要满足同材质、同 Shader、不移动等条件
- **错**："DrawCall 越少越好" —— GPU Instancing 一次画大量物体可能让单个 DC 成为 GPU 瓶颈，需要平衡

## 关联知识点
- [[UGUI 性能优化]]
- [[CPU与GPU优化]]
- [[AssetBundle 机制]]
- [[动画系统]]
- [[ECS架构]]

## 原始出处
- GitHub面经_性能优化 Q2-Q7
- 牛客网 009_互娱上岸面经 Q7
- 牛客网 013_游戏引擎面经 Q5
- 牛客网 015_图形学专题 Q5
- 博客园 多论坛面经汇总 3.2 节
