[[GAMES104_Lecture07_Rendering on Game Engine_Render Pipeline, Post-process and Everything.pdf]]

## 1 Ambient Occlusion
**Ambient Occlusion（AO，环境光遮蔽）** 是计算机图形学中的一种**近似全局光照技术**，用于模拟**环境光被几何体遮挡时产生的阴影效果**。它的核心思想是：
**一个点周围被几何体遮挡得越多，它能接收到的环境光就越少，因此看起来越暗。**

- **Precomputed AO**
	早期的AO是在 Original model 上加上一个 AO map
- **SSAO (Screen Space Ambient Occlusion)**
	在屏幕上对世界进行局部采样。SSAO+的改进是只采一个半球
	![[SSAO.png]]
- **HBAO (Horizon-based Ambient Occlusion)**
	求仰角，计算半球面有多少是可以透光的。其问题是没有涉及不同角度的光照射的漫反射不同。
	![[HBAO.png]]
- **GTAO (Ground Truth-based Ambient Occlusion)**
	现在用的最多的 AO 算法，考虑了光与表面法向的夹角，以及光来回bounce后的效果

---

## 2 Fog Everything
最经典的是：
- Linear fog, Exp fog, Exp Square fog
- Height Fog
	假设Fog有个最大值，高度高于时强度递减，低于时强度递增
- Voxel-based Volumetric Fog
	实现丁达尔效应
	![[Voxel-based Volumetric Fog .png]]

---

## 3 Anti-aliasing
信号频率与采样频率不匹配产生 Aliasing
基本的解决方法（AA）是多采样几次然后平均

- **Super-sample AA (SSAA) and Multi-sample AA (MSAA)**
	SSAA是把一个采样区域平分为四个或更多，即对空间四倍采样
	MSAA也是对空间四倍采样，但在shading时会判断，如果四个subsample都落在同一个几何形体中，就只shading一次，否则加权平均
	这两个方法的缺陷都是现代游戏三角形太多了
- **FXAA (Fast Approximate Anti-aliasing)**
	先提取出edge（十字形滤波），再在edge处做插值
- **TAA (Temporal Anti-aliasing)**
	把当前帧与历史帧的信息结合起来，累计采样，从而得到更平滑的结果。（每一帧稍微一动采样的位置）

---

## 4 Post-process
目的：物理上做正确，比如正确被曝光；风格化的表达

Bloom, Tone Mapping, Color Grading
光晕，曝光，调色

### 4.1 Bloom Effect
光晕是因为聚焦不准确产生
先找到高光（亮度超过最大值），然后进行高斯模糊，然后与原图混合，最后得到 Bloom
![[Pyramid Guassian Blur.png]]

### 4.2 Tone Mapping
解决 HDR 渲染中亮部很亮、暗部暗的问题（超过最大亮度进行截断会产生色偏），实现 HDR -> LDR
![[Tone Mapping Curve.png]]

电影中常用 ACES Curve

### 4.3 Color Grading
**Lookup Table (LUT)**
把给的颜色映射到另一种颜色，使用的时候查表就好了

---

## 5 Rendering Pipeline
==One Equation for Everything: Rendering Function==

Rendering objects with meshes, texture and shaders. Culling

Lighting, Shadow and Global Illumination, PBR Materials

Terrain, Sky and Cloud

AO, Fog, Anti-aliasing, bloom, tone mapping, color grading

这些的按顺序进行就是 Rendering Pipeline

### 5.1 Forward Rendering
最简单的pipeline就是 ShadowPass -> Shading -> Post-process
```
for n meshes 
	for m lights 
		color += shading(mesh, light) 
```
但现在光照非常多，所以这个方法现在不适用

### 5.2 Deferred Rendering
把所有材质等放入 `G-Buffer` 中，然后渲染的时候只用计算光就好了。
```
for each object
	write G-Buffer
```

```
for each pixel
	gbuffer = readGBuffer(G-Buffer)
	for each light
		computeShading(gbuffer, light)
```
但比较消耗存储，读写比较消耗时间

### 5.3 Tile-based Rendering
一小块一小块渲染，这样不需要对每个光都计算所有的像素
![[Light Culling by Tiles.png]]

### 5.4 Cluster-based Rendering
不用算z- buffer，而是对每个tile计算其visibility

### 5.5 Visibility Buffer
![[VBuffer.png]]

---

## 6 Real Rendering Pipeline
Frame Graph 渲染pipeline，让系统自动优化内存分配、渲染顺序

---

## 7 Render to Monitor
如何把渲染显示在电脑屏幕
V-Sync