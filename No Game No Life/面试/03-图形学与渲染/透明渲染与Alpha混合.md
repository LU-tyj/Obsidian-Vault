---
title: "透明渲染与Alpha混合"
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
  - "[[Early-Z与深度测试]]"
  - "[[Overdraw与GPU优化]]"
---

## 🎯 一句话结论（自测用）
> 透明物体必须从后往前排序渲染，因为颜色混合依赖目标缓冲区已有的颜色。不透明物体应该从前往后渲染以最大化 Early-Z 效益。Alpha Test 是"全透或全不透"的二元判断，Alpha Blend 可实现半透明渐变效果。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）

**1. 不透明物体的渲染顺序：从前往后**
- 先渲染离摄像机近的物体，将较近的深度写入 Z-Buffer
- 后续远处物体的片元在 [[Early-Z与深度测试|Early-Z]] 阶段被丢弃，连片元着色器都不用跑
- 最大化渲染效率

**2. 透明物体的渲染顺序：从后往前**
- 透明物体的颜色要与已渲染颜色做混合（blending）
- 混合公式：`最终颜色 = 源颜色 * SrcFactor + 目标颜色 * DstFactor`
- 最常用：`Blend SrcAlpha OneMinusSrcAlpha` = 源颜色 * α + 目标颜色 * (1-α)
- 如果从前往后渲染，后面的透明物体会被深度测试丢弃，无法参与混合

**3. Alpha Test vs Alpha Blend**：
- **Alpha Test**：片元透明度 < 阈值直接丢弃（全透或全不透），不写入深度——会破坏 [[Early-Z与深度测试|Early-Z]]
- **Alpha Blend**：片元颜色与目标缓冲区已存颜色按 α 值混合，产生半透明效果。透明物体通常不写入深度（或写但不可靠）

**4. 半透明物体的深度写入问题**：
- 通常透明渲染不写入深度（`ZWrite Off`），因为后面的透明物体需要和前一个透明物体的颜色混合
- 如果透明物体写入深度，后面的透明物体会被深度测试丢弃
- 不透明物体先渲染并写入深度，透明物体后渲染且不写入深度

## 🔍 详细解析

**渲染队列（Queue）**：
Unity 中通过 `Queue` 标签控制渲染顺序：
- Background (1000) -> Geometry (2000) -> AlphaTest (2450) -> Transparent (3000) -> Overlay (4000)

**Unity 的混合因子设置**：
```
Blend SrcAlpha OneMinusSrcAlpha  // 标准半透明
Blend One One                     // 叠加/发光效果
Blend DstColor Zero               // 正片叠底
Blend One OneMinusDstColor       // 柔光
```

**多个透明物体重叠时的 Overdraw 问题**：
- 每一层半透明都会对同一像素做一次混合计算
- 多层半透明 UI 重叠会导致严重的 [[Overdraw与GPU优化|Overdraw]]，是移动端性能杀手
- 解决：减少透明层数、合并透明元素、使用不透明替代方案

## 💬 面试官常见追问
- "如果有半透明和全透明物体混在一起怎么渲染？" -> 全透明（Alpha=0）的直接丢弃。半透明按从后往前的顺序逐个渲染，每个做一次 Blend
- "Alpha Test 为什么和 Early-Z 冲突？" -> 因为 Early-Z 在着色器之前执行，无法预知 clip/discard 的结果
- "Shader 中的渲染队列是怎么配置的？" -> `Tags { "Queue" = "Transparent" }`，还可以用 `"Queue" = "Transparent+500"` 做微调

## ⚠️ 我曾经的误区 / 网上常见错答
- 误区：透明物体也可以从前往后渲染，只是颜色不对。实际上如果透明物体能通过深度测试（后面的被前面遮挡），从前往后渲染的混合结果是完全错误的
- 误区：所有透明物体都是同一批次渲染的。实际上透明渲染仍然是逐物体 DrawCall，只是渲染顺序被重组

## 🔗 关联知识点
- [[Early-Z与深度测试]]
- [[渲染管线]]
- [[Overdraw与GPU优化]]

## 📎 原始出处
- GitHub Q7: Alpha Test vs Alpha Blend; Q8: Blending公式
- 牛客网001 Q17: 不透明几何体重叠渲染几次; Q18: 非透明物体从前往后; Q19: 透明物体从后往前
- 牛客网013 Q6: 半透明物体绘制怎么处理
