[[GAMES104_Lecture04_Rendering on Game Engine.pdf]]

## 1 Challenges
- 复杂：成千上万的 GO 需要不同的视觉效果
- 算力：基于现在的硬件基础上
- 帧率：图形学中希望帧率越高越好，但是游戏中所有的帧率需要相同
- 资源利用率：不只有渲染系统对cpu进行占用

---

## 2 Building Blocks of Rendering
这些就是 GAMES101 中基础的图形学知识。
![[Rendering_Pipeline.png]]

projection（正交、透视）-> shading -> Texture
>这些都是需要大算力的

---

## 3 GPU : Understand the Hardware
### 3.1 SIMD and SIMT
SIMD (Single Instruction Multiple Data)
SIMT (Single Instruction Multiple Threads)
![[SIMD_SIMT.png]]

### 3.2 GPU Architecture
![[GPU_Architecture.png]]
费米架构

>Core -> SM -> GPC
>SM 会进行计算以及数据交换

==数据与计算分离，但这也带来了数据传输速度慢的问题；以及增多 Cache hit，避免查找数据造成Cache miss==

---

## 4 Renderable
**Building Block of Renderable** : Mesh + Material + Shader

### 4.1 Mesh Primitive
渲染时一般使用 Vertex Data and Index Data 来存储物体，只存储顶点和对顶点所标的index
>尽可能把模型变为Triangle Strip（顶点连续，内存友好）
>记得要对每个 Vertex 都要计算法向量
![[Mesh_Primitive .png]]

### 4.2 Material
==Material == BRDF== 反映了物体表面如何与光进行互作
Determine the appearance of objects, and how objects interact with light.
还有Texture

---

## 5 Render Objects in Engine
一个 GO 上有多种不同的 Material，不能简单地表示。为了整理这些，根据材质的不同把 mesh 切割成多个**Submesh**，每个 Submesh 有自己的材质、纹理，但Vertex存储在同一个 buffer 中，因此每个 Submesh 只要多存储 offset 和 count（从 buffer 中截取）就行了。

==Instance : Use Handle to Reuse Resources.==

为了节约空间，现代游戏引擎会建立一个 **Resource Pool**，这样只需要存储 index 就好了，绘制时只需要使用 index（合并同类项）
![[Resource_Pool.png]]

优化方法：
- Sort by Material
- GPU Batch Rendering

---

## 6 Visibility Culling
只渲染视线锥里的物体，用 Bounding Box 进行判断Culling
![[Bounding_Box.png]]
使用BVH Culling(Bounding Volume Hierarchy Culling) 进行优化

>PVS (Potential Visibility Set) 算法：从门口看，看到有多少房间
![[PVS.png]]

---

## 7 Texture Compression
核心思想：**Block Based** (切成例如 4 * 4 的小块)
DXT优化算法：从 4 * 4 的色块中选择最亮和最暗的点，然后对其他像素进行插值。

---

## 8 Cluster-Based Mesh Pipeline
现代游戏引擎的渲染管线。
核心思想：对一个精细的模型进行分组，用GPU自行生成（看不到的就不渲染）

[[Lec5 Lighting, Materials and Shaders]] 中详细介绍了 Light Materials 以及 shaders的渲染