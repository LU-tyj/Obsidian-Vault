---
title: "Overdraw与GPU优化"
category: 图形学与渲染
tags: [图形学, 渲染, 网易互娱, Unity]
frequency: ⭐
difficulty: 简单
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[DrawCall与合批]]"
  - "[[透明渲染与Alpha混合]]"
  - "[[LOD与剔除]]"
  - "[[渲染管线]]"
---

## 🎯 一句话结论（自测用）
> Overdraw 是同一像素被多次绘制导致的 GPU 浪费。主要来源是透明物体叠加和不必要 UI 重叠。优化方向包括合理的渲染顺序、减少半透明重叠、以及 Shader 层面的精度和计算简化。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **Overdraw 的定义**：同一屏幕像素被多次着色——例如多层半透明 UI 重叠时，GPU 对底层像素的计算白做了
2. **Overdraw 的主要来源**：
   - 多层半透明物体叠加
   - UI 元素大面积重叠
   - 粒子特效大量覆盖屏幕
3. **减少 Overdraw 的方法**：
   - 合理排序：不透明物体从前往后（利用 Early-Z 避免 Overdraw），透明物体从后往前（必须画但最小化混合层数）
   - 遮挡剔除：被遮挡的物体完全不提交渲染
   - 减少半透明 UI 重叠：将 UI 合并、避免大面积全透明区域
4. **GPU 优化技巧**：
   - Shader 中使用 `half`/`fixed` 代替 `float`（移动端精度够用且更快）
   - 避免 Shader 中的分支（`if-else`）和复杂数学（`sin/tan/pow`）
   - 控制实时阴影分辨率与距离
   - 合理使用 [[LOD与剔除|LOD]] 降低远处物体的面数

## 🔍 详细解析

**Overdraw 的衡量**：Unity Scene View 中切换 Shaded -> Overdraw 模式，白色/亮色区域表示 Overdraw 严重的区域

**移动端 Overdraw 特别重要**：
- 移动端 GPU 是 TBR 架构，带宽敏感
- Overdraw 意味着每个像素可能被多次从显存读取和写入
- 移动端优化中，控制 Overdraw 和降低分辨率是最有效的两种 GPU 优化

**Shader 精度对比**：
| 类型 | 精度 | 速度 | 适用 |
|------|------|------|------|
| float | 32bit | 慢 | 世界坐标、UV大纹理 |
| half | 16bit | 中 | 颜色、单位向量、HDR |
| fixed | 11bit | 快 | 简单颜色、0-1 范围值 |

## 💬 面试官常见追问
- "如何用 Profiler 定位 Overdraw 问题？" -> Frame Debugger 查看每个 DrawCall 的渲染结果 + Scene Overdraw 视图
- "透明物体排序是怎么保证的？" -> Unity 按渲染队列 (Queue) 和物体到摄像机的距离对透明物体排序。同 Queue 内按距离排序

## ⚠️ 我曾经的误区 / 网上常见错答
- 误区：Overdraw 不重要，GPU 性能够强。移动端 Overdraw 是帧率杀手，一两个全屏半透明叠加就能让帧率暴跌
- 误区：Shader 中写 if-else 没问题。GPU 是 SIMD 架构，if-else 导致所有分支都被执行然后选择结果，实际上没有节省计算

## 🔗 关联知识点
- [[DrawCall与合批]]
- [[透明渲染与Alpha混合]]
- [[LOD与剔除]]
- [[渲染管线]]

## 📎 原始出处
- GitHub Q17: Overdraw; Q18: GPU优化技巧
- GitHub性能优化Q5/Q7: GPU优化、Overdraw优化
