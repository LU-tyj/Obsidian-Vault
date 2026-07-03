---
title: "Gamma矫正"
category: 图形学与渲染
tags: [图形学, 渲染, 网易互娱]
frequency: ⭐
difficulty: 简单
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[渲染管线]]"
  - "[[PBR理论]]"
---

## 🎯 一句话结论（自测用）
> Gamma 矫正是因为显示器对输入电压的非线性响应（Gamma ≈ 2.2）——输入信号加倍，亮度不是加倍而是增大约 2.2 次方。渲染管线必须在输出前做 Gamma 矫正（power 1/2.2），否则画面会偏暗。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **为什么需要 Gamma 矫正**：
   - 人眼对暗部亮度变化更敏感（非线性感知）
   - 历史原因：CRT 显示器输入电压与输出亮度呈 `output = input^2.2` 的非线性关系
   - 现代显示器继承了这个 Gamma 曲线
2. **渲染管线中的 Gamma 矫正**：
   - 纹理通常以 sRGB 空间存储（经过 Gamma 编码），进入 Shader 计算前需要先解码到线性空间
   - 所有光照计算必须在**线性空间**中进行（因为光能的加减是在物理线性空间中的）
   - 最终输出到显示器前，需要再做一次 Gamma 编码：`output = input^(1/2.2)`
3. **Unity 中的设置**：
   - `Player Settings > Color Space` 选择 Linear
   - Linear 空间：Unity 自动做输入纹理的 sRGB 解码和输出帧缓冲的 Gamma 编码
   - Gamma 空间：不做矫正（兼容旧项目，但光照效果不物理准确）

## 🔍 详细解析

**线性空间 vs Gamma 空间的视觉效果**：
- Gamma 空间：暗部细节丢失（暗部被压缩），亮部过曝（亮部被拉伸）
- Linear 空间：光照计算物理准确，暗部有层次，高光自然

**流程总结**：
```
纹理(sRGB空间) --[去Gamma: power 2.2]--> 线性空间光照计算 --[加Gamma: power 1/2.2]--> 显示器
```

## 💬 面试官常见追问
- "Blinn-Phong 计算在线性空间和 Gamma 空间有什么不同？" -> Gamma 空间的高光看起来更集中但偏暗，暗部细节丢失。线性空间的 diffuse/specular 混合更接近真实材质表现

## 🔗 关联知识点
- [[PBR理论]]
- [[渲染管线]]

## 📎 原始出处
- 牛客网013 Q3: Gamma矫正
