---
title: "DrawCall与合批"
category: 图形学与渲染
tags: [图形学, 渲染, 网易互娱, Unity]
frequency: ⭐⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[渲染管线]]"
  - "[[LOD与剔除]]"
  - "[[URP-HDRP对比]]"
  - "[[Overdraw与GPU优化]]"
---

## 🎯 一句话结论（自测用）
> DrawCall 是 CPU 向 GPU 发起的渲染命令，过多的 DrawCall 会导致 CPU 瓶颈。降低 DrawCall 的核心手段包括静态合批、动态合批、GPU Instancing、SRP Batcher，以及图集合并和遮挡剔除。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **DrawCall 的定义**：CPU 准备好网格、材质、纹理等渲染状态后，调用底层图形 API（OpenGL/DX/Vulkan）向 GPU 提交一次渲染命令。状态切换开销是 DrawCall 性能瓶颈的本质原因。
2. **降低 DrawCall 的 4 种核心合批手段**：
   - **静态合批**：标记为 Static 的物体，同材质下 Unity 会自动合并为一个大网格（前提：顶点数 <= 64k），内存开销大—每个物体在内存中保留副本
   - **动态合批**：自动对相同材质、顶点数 <= 300 的可移动物体进行合并，每帧重建网格（CPU 开销）
   - **GPU Instancing**：一次 DrawCall 渲染多个相同网格的不同实例（通过 instance buffer 传递每个实例的差异化数据，如位置、颜色）
   - **SRP Batcher**：URP/HDRP 特有，不减少 DrawCall 次数但大幅减少状态切换开销—缓存 Shader 属性和材质参数在 GPU 常量缓冲区中
3. **非合批手段**：图集合并（减少纹理切换）、遮挡剔除（减少不需要绘制的物体）、[[LOD与剔除|LOD]]（远处降模减少顶点数）、合理渲染排序（减少 Shader/材质切换）

## 🔍 详细解析

**静态合批 vs 动态合批 vs GPU Instancing vs SRP Batcher**：

| 维度 | 静态合批 | 动态合批 | GPU Instancing | SRP Batcher |
|------|---------|---------|---------------|-------------|
| 物体是否可移动 | 否 | 是 | 是 | 是 |
| 内存开销 | 大（每物体保留副本） | 小 | 小 | 小 |
| 顶点限制 | 64k | 300 | 无 | 无 |
| 条件 | 手动标记 Static | 自动 | 同Mesh同材质 | URP/HDRP |
| 减少DC? | 是 | 是 | 是 | 不减少，减少切换耗时 |

**Minecraft 类游戏的 DrawCall 优化**（网易引擎面真题）：
- 使用体素世界的 Chunk 网格合并（类似静态合批）
- GPU Instancing 渲染大量相同方块
- 面剔除（相邻方块的面不渲染）

**移动端 DrawCall 目标值**：
- 低端机 <= 100-150 Batches
- 中端机 <= 200-300 Batches
- 高端机 <= 400-500 Batches
- SetPass Calls 控制在 20-30 以内

## 💬 面试官常见追问
- "静态合批为什么内存大？" -> 合批后合并为一个大网格，但原始网格的数据仍保留在内存中，相当于多存储了一份合并后的网格
- "GPU Instancing 和 SRP Batcher 的区别？" -> GPU Instancing 减少 DrawCall，适合大量相同物体；SRP Batcher 不减少 DrawCall 但降低每个 DrawCall 的 CPU 开销，适合不同材质的物体
- "动态合批的 300 顶点限制是怎么算的？" -> 动态合批每帧要在 CPU 端重新构建合并网格，限制是为了控制 CPU 开销；超过 300 顶点的物体不参与动态合批

## ⚠️ 我曾经的误区 / 网上常见错答
- 误区：DrawCall 越少越好。实际上 SRP Batcher 虽然不减少 DrawCall，但整体性能可以更好。关键是 CPU->GPU 的通信瓶颈，不是 DrawCall 数量本身
- 误区：合批就是免费的。静态合批代价是内存翻倍，动态合批有 CPU 合并开销

## 🔗 关联知识点
- [[URP-HDRP对比]]
- [[LOD与剔除]]
- [[Overdraw与GPU优化]]
- [[渲染管线]]

## 📎 原始出处
- GitHub Q3/Q4: unitykit/unityClientInterviewGuide
- GitHub性能优化Q2/Q4: unitykit/unityClientInterviewGuide
- 牛客网009 Q7: 剔除/LOD/合批
- 牛客网013 Q5: DrawCall优化; Q18: Minecraft DC优化
- 牛客网015 Q5: 合批(Batching)
- 博客园: 多论坛面经汇总
