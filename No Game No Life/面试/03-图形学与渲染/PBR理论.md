---
title: "PBR理论"
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
  - "[[法线贴图]]"
  - "[[阴影技术]]"
---

## 🎯 一句话结论（自测用）
> PBR（基于物理的渲染）的核心思想是通过 BRDF 模拟光与材质的物理交互。Blinn-Phong 是经验模型（快速但不物理准确），Cook-Torrance 是 PBR 的微面元 BRDF，由法线分布(D)、几何遮蔽(G) 和菲涅尔(F) 三项组成。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）

**光照模型的演进**：

1. **Phong 光照模型**：
   - Diffuse: `Kd * lightColor * max(dot(N, L), 0)`
   - Specular: `Ks * lightColor * pow(max(dot(R, V), 0), shininess)`
   - R 是反射方向，shininess 控制高光集中度

2. **Blinn-Phong 光照模型**：
   - 将反射向量 R 替换为**半程向量 H** = normalize(L + V)
   - Specular: `Ks * pow(max(dot(N, H), 0), shininess)`
   - **优势**：H 比 R 计算更简单，且当光源在物体背面时不会出现 Phong 的镜面高光断裂

3. **Cook-Torrance BRDF（PBR核心）**：
   由三项相乘组成：
   - **D（Normal Distribution Function）**：法线分布函数，微面元中有多少法线方向等于半程向量 H。常用 GGX（Trowbridge-Reitz）
   - **G（Geometry Function）**：几何遮蔽函数，微面元间相互遮挡的比例。常用 Smith's method
   - **F（Fresnel Equation）**：菲涅尔方程，反射率随入射角增大而增大。常用 Schlick 近似
   
   `BRDF = (D * G * F) / (4 * (N·L) * (N·V))`

4. **PBR 核心参数**：Base Color（基础色）、Metallic（金属度）、Roughness（粗糙度）、Normal Map（法线贴图）、AO（环境光遮蔽）

## 🔍 详细解析

**为什么 Blinn-Phong 比 Phong 更好？**
- 半程向量 H 在背面时仍有意义，而反射向量 R 在光源位于物体背面时会背离 V 方向，导致 specular 计算错误
- 实际测试中 Blinn-Phong 更接近真实材质表现

**Cook-Torrance D/F/G 通俗理解**：
- D：在我看的方向上，有多少微面元恰好在"能反射光"的角度上（决定了高光形状）
- G：有多少微面元没被"邻居"挡住（决定了暗角/粗糙度上升时的暗度）
- F：入射角越大，反射率越大（为什么扫视水面/桌面能看到反射，正上方看却看不到）

**能量守恒**：PBR 严格要求 Diffuse + Specular <= 1，这保证了材质在不同光照条件下都看起来真实

## 💬 面试官常见追问
- "半程向量解决了 Phong 的什么问题？" -> 解决了光源在背面时的 specular 计算断裂，且计算更高效（H 只需加法归一化，R 需要反射向量计算）
- "BRDF 的 D、F、G 分别用哪些算法？" -> 常用：D=GGX，F=Schlick，G=Smith
- "为什么 Cook-Torrance 要考虑 G（几何遮蔽）？" -> 粗糙表面上的微面元会互相遮挡入射光和反射光，不考虑 G 会边缘过亮

## ⚠️ 我曾经的误区 / 网上常见错答
- 误区：Blinn-Phong 是 Phong 的升级版，可以完全替代。实际上 Blinn-Phong 在某些角度 specular 会比 Phong 更集中（shininess 相同时），需要调整参数
- 误区：PBR 就是 Cook-Torrance。Cook-Torrance 只是 PBR 中一种常用的微面元 BRDF，PBR 还包括能量守恒、金属/非金属区分、迪士尼原则等一整套方法论

## 🔗 关联知识点
- [[法线贴图]]
- [[渲染管线]]
- [[延迟渲染vs前向渲染]]

## 📎 原始出处
- GitHub Q9/Q15: unitykit/unityClientInterviewGuide
- 牛客网009 Q9: 冯/布林-冯光照模型; Q10: Cook-Torrance BRDF
- 牛客网013 Q2: Phong光照实现; Q4: PBR原理
- 牛客网015 Q7: 冯氏光照 vs 布林-冯; Q8: Cook-Torrance D/F/G
- 博客园/牛客网 Q2: Blinn-Phong光照模型
- BOSS直聘: Blinn-Phong光照模型
