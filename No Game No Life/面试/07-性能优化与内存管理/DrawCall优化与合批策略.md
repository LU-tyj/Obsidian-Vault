---
title: "DrawCall优化与合批策略"
category: 性能优化与内存管理
tags: [性能优化, DrawCall, 合批, SRP Batcher, GPU Instancing, 网易互娱]
frequency: ⭐⭐⭐
difficulty: 中等
companies: [网易互娱]
status: new
last_reviewed:
next_review:
related:
  - "[[UI优化策略]]"
  - "[[GPU性能优化与Overdraw]]"
  - "[[CPU性能优化]]"
---

## 🎯 一句话结论（自测用）
> 减少 DrawCall 的核心思路是**合并渲染批次**，让 CPU 尽可能少地向 GPU 发送渲染指令。10 种主流方法：静态合批、动态合批、GPU Instancing、SRP Batcher、图集合并、减少 Shader Pass、遮挡剔除、LOD、合理排序减少状态切换、UI 画布合理划分。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **DrawCall 是什么**：CPU 每次向 GPU 发送的一次"绘制"指令，包含网格数据、材质、Shader 等信息。DrawCall 过多会导致 CPU 成为瓶颈（准备渲染状态的开销）。
2. **减少 DrawCall 的十大方法**：
   - 静态合批 (Static Batching)：将不移动的、共用同一材质的物体在打包时合并为一个 Mesh，运行时一次性绘制。
   - 动态合批 (Dynamic Batching)：运行时将符合条件的动态小物体合并。限制：顶点属性不超过 900，缩放必须一致、使用相同材质。
   - GPU Instancing：同一 Mesh + 同一材质的大量物体，通过传递实例矩阵数组一次 DrawCall 绘制多个。
   - SRP Batcher（URP/HDRP）：不合并 Mesh，而是缓存材质属性到 GPU，减少 SetPass Call。对 Shader 有兼容要求。
   - 图集合并（Texture Atlas）：同一界面的小图合并为一张大图，同一材质即可合批。
   - 减少 Shader Pass 数量：每个 Pass 增加一个 DrawCall，减少多 Pass Shader。
   - 遮挡剔除（Occlusion Culling）：不渲染被遮挡的物体。
   - LOD：远处物体降模，减少顶点数。
   - 合理渲染排序：减少材质/Shader/贴图切换。
   - UI 优化：Canvas 合理划分、动静分离。
3. **移动端目标值**：低端机 <= 100-150 Batches，中端机 <= 200-300，高端机 <= 400-500；SetPass Calls 控制在 20-30 以内。

## 🔍 详细解析

### 静态合批 vs 动态合批

| 对比维度 | 静态合批 | 动态合批 |
|---------|---------|---------|
| 触发条件 | 物体标记为 Static | 运行时自动判断 |
| 合并时机 | 打包/构建时 | 每帧运行时 |
| 内存开销 | 合并后会增加内存（多份顶点数据） | 少量 CPU 计算开销 |
| 适用场景 | 场景中不动的建筑、地形 | 小物体、数量不多时 |
| 顶点限制 | 无特别限制 | 顶点属性 < 900 |

### GPU Instancing 使用条件
- 同一 Mesh、同一 Material
- Shader 需支持 Instancing（`#pragma multi_compile_instancing`）
- 适用：大量相同物体（树木、子弹、敌人模型），不适合每个物体颜色/材质不同的场景

### SRP Batcher 原理
- 前提：使用 SRP（URP 或 HDRP）
- 机制：将 "材质属性" 缓存在 GPU 一侧的持续内存，每次渲染只需更新 Transform 等少数数据，大幅减少 SetPass Call
- Shader 要求：必须兼容 SRP Batcher（Unity 的 Lit Shader 默认兼容）

## 💬 面试官常见追问
- **静态合批和动态合批有什么区别？各自内存开销如何？** → 静态合批合并为一个大 Mesh 占用额外内存；动态合批每帧运行时计算，有顶点数限制
- **GPU Instancing 和 SRP Batcher 能同时用吗？** → 可以结合，但 SRP Batcher 优先级更高；Instancing 是"一次画多个"，SRP Batcher 是"减少状态设置"
- **为什么 UI 的 DrawCall 优化不一样？** → UI 使用 Canvas，每个 Canvas 重建时需合并网格；关键是动静分离和减少 Canvas 数量
- **SetPass Call 和 Batches 的区别？** → Batches 是总渲染批次，SetPass Call 是 Shader Pass 切换次数（实际影响更大）

## ⚠️ 我曾经的误区 / 网上常见错答
- 误区：动态合批零开销。实际上动态合批每帧都有 CPU 合并开销，顶点数超限反而增加 DrawCall
- 误区：合批越多越好。SRP Batcher 不追求合批数量，而是减少 SetPass Call
- 误区：所有物体都能静态合批。需同一材质、同一 Shader，且物体标记为 Static Batching

## 🔗 关联知识点
- [[UI优化策略]]
- [[GPU性能优化与Overdraw]]
- [[CPU性能优化]]

## 📎 原始出处
- GitHub面经_性能优化 Q4/Q6：减少 DrawCall 的 10 种方法与合理目标值
- 牛客网 009 Q7：剔除/LOD/合批
- 牛客网 013 Q5：DrawCall 太多怎么优化
- 牛客网 015 Q3/Q5：剔除方式 + 合批
- 博客园多论坛汇总：DrawCall/合批/引擎优化为必考点
