---
title: "Early-Z与深度测试"
category: 图形学与渲染
tags: [图形学, 渲染, 网易互娱]
frequency: ⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[渲染管线]]"
  - "[[透明渲染与Alpha混合]]"
  - "[[阴影技术]]"
---

## 🎯 一句话结论（自测用）
> Early-Z 是在片元着色器执行前做深度测试，提前丢弃被遮挡的片元以避免昂贵的着色计算。但它不能与 Alpha Test 或手动修改深度值的 Shader 同时使用，因为这会破坏深度判断的正确性。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **深度测试（Z-Test）**：比较当前片元的深度值与深度缓冲区中已存储的深度值，决定是否通过并写入帧缓冲。通常深度测试在片元着色器之后进行。
2. **Early-Z（Early Depth Test）**：将深度测试提前到片元着色器执行之前。如果一个片元在 Early-Z 阶段就被判定为被遮挡，GPU 直接跳过该片元的着色器计算，节省大量性能。
3. **Early-Z 的启动条件**：
   - 不透明物体，且按从前往后的顺序渲染（最大化 Early-Z 效益）
   - Shader 中没有 `clip()` / `discard` 操作（即 Alpha Test）
   - Shader 中没有手动写入深度值（即没有修改 `SV_Depth` / `gl_FragDepth`）
   - 没有开启 Alpha to Coverage
4. **Alpha Test 与 Early-Z 冲突的原因**：Alpha Test 可能丢弃片元，但 Early-Z 发生在片元着色器之前，无法预知片元是否会被丢弃。如果 Early-Z 提前更新了深度缓冲区，而被 Alpha Test 丢弃的片元本不应写入深度，这会导致后续物体被错误遮挡。

## 🔍 详细解析

**渲染管线中的深度测试位置**（按阶段）：

```
片元着色器执行之前（Early-Z 可选）
       |
  片元着色器执行
       |
Alpha Test（clip/discard）-- 如果开启，Early-Z 自动禁用
       |
模板测试（Stencil Test）
       |
深度测试（Z-Test）
       |
混合（Blending）
       |
写入帧缓冲
```

**Early-Z 为什么要求不透明物体从前往后渲染？**
如果先渲染远处的物体，它的深度值会写入 Z-Buffer。然后渲染近处物体时，Early-Z 发现 Z-Buffer 中已有更近的深度值，可以直接跳过近处物体后面的片元着色。如果反过来（从后往前），近处物体先写入了更近的深度，远处物体的片元被 Early-Z 全部丢弃——但这是正确结果，只是没有着色省略的收益。

## 💬 面试官常见追问
- "Early-Z 有使用限制吗？和 Alpha Test 为什么冲突？" -> 见上，核心原因是 Early-Z 无法预知 clip/discard 的结果
- "为什么不透明物体从前往后渲染？" -> 最大化 Early-Z 的片元着色省略效果：先渲染近处物体，远处被遮挡物体的片元在 Early-Z 阶段直接被丢弃，连片元着色器都不用跑
- "模板测试（Stencil Test）在渲染管线中的位置？" -> 通常在 Early-Z 之后/并行，在颜色混合之前。常用于实现遮罩、镜面反射、范围裁剪等

## ⚠️ 我曾经的误区 / 网上常见错答
- 误区：深度测试永远在着色器之后。实际上现代 GPU 普遍支持 Early-Z 将深度测试提前到着色器之前
- 误区：Early-Z = Early-Z Rejection。Rejection 是一种优化策略，指优先渲染不透明遮挡物来让后续物体的 Early-Z 更有效

## 🔗 关联知识点
- [[渲染管线]]
- [[透明渲染与Alpha混合]]
- [[阴影技术]]

## 📎 原始出处
- 牛客网001 Q14: 深度测试有办法提前吗(Early-Z); Q15: Early-Z与AlphaTest冲突
- 牛客网005 Q40: 深度测试
- 博客园: 高频考点汇总
