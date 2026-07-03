---
source_platform: GitHub
source_url:
  - https://github.com/unitykit/unityClientInterviewGuide
  - https://github.com/Lafree317/Unity-InterviewQuestion
crawl_date: 2026-07-03
crawl_agent: agent-github
company_mentioned: [通用, 网易互娱]
position: Unity客户端开发
raw: true
---

# 图形学与渲染面试题

## 一、渲染管线

### Q1: 渲染管线的主要阶段？

| 阶段 | 说明 |
|------|------|
| **应用阶段** | CPU 准备数据（网格、纹理、摄像机、灯光），设置渲染状态，调用 DrawCall |
| **几何阶段** | 顶点着色 -> 曲面细分 -> 几何着色器 -> 投影 -> 裁剪 -> 屏幕映射 |
| **光栅化阶段** | 三角形设置 -> 遍历 -> 片元生成 |
| **片元/像素处理** | 纹理采样 -> 颜色计算 -> 模板测试 -> 深度测试 -> 混合 -> 输出到帧缓冲区 |

简化流程：本地坐标 -> 视图坐标 -> 背面裁剪 -> 光照 -> 裁剪 -> 投影 -> 视图变换 -> 光栅化

### Q2: MVP 变换是什么？
- **M (Model)**: 模型矩阵，将物体从局部坐标转换到世界坐标
- **V (View)**: 视图矩阵，将世界坐标转换到相机坐标
- **P (Projection)**: 投影矩阵，将相机坐标转换到裁剪空间

---

## 二、DrawCall

### Q3: 什么是 DrawCall？如何降低？

**定义**：CPU 准备好渲染数据后，对底层图形 API（OpenGL/DirectX/Vulkan）发出的渲染命令。

**过高的影响**：手机帧率下降（卡顿）、发热严重、CPU 瓶颈

**降低 DrawCall 的方法**：

| 手段 | 说明 |
|------|------|
| 静态合批 | 将相同材质的静态物体合并为一个网格 |
| 动态合批 | 自动合并使用相同材质的动态物体（顶点数 <= 300） |
| GPU Instancing | 一次 DrawCall 渲染多个相同网格的不同实例 |
| SRP Batcher | URP/HDRP 下缓存 Shader 属性，减少 CPU 状态切换 |
| 图集合并 | 将零散贴图合并为大图 |
| 遮挡剔除 | 剔除被遮挡的不可见物体 |
| LOD | 远处物体使用低模 |

### Q4: 静态合批 vs 动态合批？

| 对比维度 | 静态合批 | 动态合批 |
|---------|---------|---------|
| 是否自动 | 需手动标记 Static | 自动进行 |
| 物体能否移动 | 否 | 是 |
| 内存开销 | 较大 | 较小 |
| 限制 | 需相同材质，顶点数 <= 64k | 需相同材质，顶点数 <= 300 |

---

## 三、Shader

### Q5: Unity Shader 的种类？

| 类型 | 特点 |
|------|------|
| 表面着色器（Surface Shader） | 抽象层次高，易用，支持前向/延迟渲染 |
| 顶点/片元着色器（VF Shader） | 灵活度高，需更多代码 |
| 固定功能管线着色器 | 备选方案，用于低端硬件 |

### Q6: Shader 中的渲染队列（Queue）？
通过 `Queue` 标签控制渲染顺序：
- Background (1000) -> Geometry (2000) -> AlphaTest (2450) -> Transparent (3000) -> Overlay (4000)

### Q7: Alpha Test vs Alpha Blend？
- **Alpha Test**: 片元透明度低于阈值直接丢弃，全透/全不透，无半透明
- **Alpha Blend**: 与已渲染颜色混合，可实现半透明效果

### Q8: Blending 公式？
```
最终颜色 = 源颜色 * SrcFactor + 目标颜色 * DstFactor
Blend SrcAlpha OneMinusSrcAlpha: 最终颜色 = 源颜色 × 源Alpha + 目标颜色 × (1-源Alpha)
```

### Q9: 漫反射公式？
```
diffuse = Kd * lightColor * max(dot(N, L), 0)
```
N: 表面法线, L: 光源方向, Kd: 漫反射系数

---

## 四、URP 与 HDRP

### Q10: URP / HDRP / Built-in 的区别？

| 管线 | 灵活性 | 性能 | 画质 | 适用平台 |
|------|--------|------|------|----------|
| Built-in RP | 低 | 中等 | 中等 | 所有（旧项目） |
| URP | 中 | 高 | 好 | 移动端/跨平台 |
| HDRP | 高 | 低帧率 | 极致 | PC/主机/高端 |
| SRP（自定义） | 最高 | 取决实现 | 取决实现 | 特定需求 |

### Q11: URP 的 Forward vs Deferred 渲染？
- **Forward**: 逐像素光源，单 Pass
- **Deferred**: 分离几何与光照阶段，支持多光源

### Q12: SRP Batcher 的作用？
- URP/HDRP 中的特殊优化
- 缓存 Shader 属性，减少 CPU 设置渲染状态的开销
- 不减少 DrawCall 次数，但提高 CPU->GPU 传输速率

---

## 五、光照与贴图

### Q13: 实时光照 vs 烘焙光照？
- 实时光照：运行时计算，支持动态物体，开销大
- 烘焙光照：预先计算光照结果到 Lightmap，节省运行时开销，但只适用于静态物体

### Q14: MipMap 是什么？优缺点？
- 纹理的 LOD，预先生成多级分辨率副本
- 优点：优化显存带宽，减少锯齿
- 缺点：多占用约 33% 内存
- UI 不适用 MipMap

### Q15: PBR 的核心参数？
- Base Color（基础色）
- Metallic（金属度）
- Roughness / Smoothness（粗糙度/光滑度）
- Normal Map（法线贴图）
- Ambient Occlusion（环境光遮蔽）

---

## 六、其他渲染相关

### Q16: LOD 是什么？优缺点？
- **定义**: 根据物体与摄像机的距离，动态切换不同精度模型
- **优点**: 减少 GPU 渲染开销
- **缺点**: 增加美术工作量和内存消耗（多套模型）

### Q17: Overdraw 是什么？如何减少？
- 同一像素被多次绘制（如多层半透明 UI 重叠）
- 减少方法：减少半透明重叠区域、合理渲染顺序、使用遮挡剔除

### Q18: GPU 优化技巧？
- Shader 中用 half/fixed 代替 float（非必要不用高精度）
- 避免分支、循环、复杂数学运算（sin/tan/pow）
- 控制实时阴影分辨率与距离
- 减少 Overdraw
- 合理使用 LOD

### Q19: 为什么游戏用前向渲染更多？
- 支持 MSAA（延迟渲染不支持硬件 MSAA）
- 移动端不支持延迟渲染
- Shader 编写更自由

---

> 来源: unitykit/unityClientInterviewGuide, Lafree317/Unity-InterviewQuestion
