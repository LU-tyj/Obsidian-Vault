---
title: "URP-HDRP对比"
category: 图形学与渲染
tags: [图形学, 渲染, 网易互娱, Unity]
frequency: ⭐
difficulty: 简单
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[渲染管线]]"
  - "[[延迟渲染vs前向渲染]]"
  - "[[DrawCall与合批]]"
---

## 🎯 一句话结论（自测用）
> Built-in RP 是传统固定管线（灵活低、全平台兼容），URP 是轻量级可编程管线（移动优先、性能好），HDRP 是高端可编程管线（画质极限、仅 PC/主机）。SRP Batcher 是 URP/HDRP 的 CPU 性能加速器——不减少 DrawCall 但大幅减少状态切换开销。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **三种渲染管线对比**：

| 管线 | 灵活性 | 性能 | 画质 | 目标平台 |
|------|--------|------|------|----------|
| Built-in RP | 低 | 中等 | 中等 | 所有（旧项目兼容） |
| URP | 中 | 高 | 好 | 移动端/跨平台 |
| HDRP | 高 | 低帧率 | 极致 | PC/主机/高端 |
| 自定义 SRP | 最高 | 取决实现 | 取决实现 | 特定需求 |

2. **URP 的关键特性**：
   - 单 Pass 前向渲染（简化版 Forward+）
   - SRP Batcher 加速 CPU 渲染状态提交
   - 内置 Shader Graph 可视化编辑
   - 支持移动端（但不支持延迟渲染的完整 G-Buffer）

3. **SRP Batcher 原理**：
   - 传统管线每个 DrawCall 需重新设置大量渲染状态
   - SRP Batcher 将 Shader 属性缓存在 GPU 常量缓冲区（CBUFFER）中
   - 当材质和 Shader 不变时，状态切换次数大幅减少
   - 不减少 DrawCall 数量，但每个 DrawCall 的 CPU 成本大幅降低

## 🔍 详细解析

**SRP Batcher 的兼容条件**：
- 必须使用 URP 或 HDRP
- Shader 必须兼容 SRP Batcher（使用 `CBUFFER_START(UnityPerMaterial)` 包裹材质属性）
- 不适用于使用 MaterialPropertyBlock 的 GPU Instancing 物体

**项目选型建议**：
- 移动端休闲/中度游戏 -> URP
- 3A/高画质 PC 游戏 -> HDRP
- 已有大型 Built-in 项目 -> 评估迁移成本后再决定
- 有特殊渲染需求 -> 自定义 SRP

## 💬 面试官常见追问
- "为什么要从 Built-in 迁移到 URP？" -> 性能更好（SRP Batcher）、支持 Shader Graph、Shader 变体管理更优、未来 Unity 主推方向
- "SRP Batcher 和 GPU Instancing 冲突吗？" -> 不冲突，但一个物体会优先使用一种方案。通常相同 Mesh 大量实例用 GPU Instancing，不同材质用 SRP Batcher

## 🔗 关联知识点
- [[延迟渲染vs前向渲染]]
- [[DrawCall与合批]]
- [[渲染管线]]

## 📎 原始出处
- GitHub Q10: URP/HDRP/Built-in区别; Q12: SRP Batcher
