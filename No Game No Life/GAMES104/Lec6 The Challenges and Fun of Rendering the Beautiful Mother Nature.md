[[GAMES104_Lecture06_The Challenges and Fun of Rendering the Beautiful Mother Nature.pdf]]

## 1 Simple Idea - Heightfield
每隔 1m 画一个网格 Mesh Grids，根据高程图来绘制每一个顶点并附上材质。
这个方法很简单，但是对于开放世界的大地图来说，就比如远近的地形渲染的精度就不相同，因此采用了 **Adaptive Mesh Tessellation** 的方法，关注fov内部的三角形。
![[Adaptive_Mesh_Tessellation.png]]

### Two Golden Rules of Optimization
1. 如上图所示，视角越小越密，越宽越稀疏
2. error bound：采样点变少了，但是误差（屏幕上像素差）不能超过一定值

切分方法：
1. Triangle-Based Subdivision 等腰直角三角形最长边的中点对半切
	Subdivision and T-Junctions 如下图所示，当三角形T被进一步细分，但$T_B$却没有相应的点时，T新产生的点就会落在右侧三角形的一条“未分裂的边上”，当两者光栅化后，就会出现图中的情况。
	解决方法是大三角形跟着进行分裂。
	![[Subdivision_and_T-Junctions.png]]

2. 现在更多是基于四叉树Quad Tree的地形表达
	既优化了资源的管理，也可以很好的解决 T-junctions 的问题，使用 stitching 方法，如图所示，将分裂点进行合并。
	![[Stitching.png]]
3. Triangulated Irregular Network (TIN)
	使用不规则三角形进行表示
	优点是画的三角形数量少，而且运行速度快；缺点是需要pre-processing，很难进行修改
4. Hardware Tessellation
	基于GPU的分块以及Mesh shader pipeline
	![[Mesh_Shader_Pipeline.png]]

## 2 Non-Heightfield Terrain
挖洞例子：把挖掘处顶点输出NaN（无效数），这时GPU就会把这个点相关的所有三角形全部挖掉，再做一个隧道模型插进去就好了。

Marching Cubes：用三角形切分正方体来表示不规则图形

## 3 Terrain Materials and Texture Splatting
地形就是各种各样的材质按比例混合在一起，图中就展示了 PBR Materials以及笔刷进行混合。

其中可以高度图来对权重进行调整，来帮助blending。
当你height高，权重下降的慢一些，height低，权重下降的快一点；以及添加depth扰动来对权重进行修改，当平均高度差小于depth时，就混合。这样称为 Texture Splatting
![[Terrain_Materials_Blending.png]]

现实中会有 Texture Array进行渲染

Virtual Texture

---

## 4 Atmosphere
### 4.1 Analytic Atmosphere Appearance Modeling
最简单的表示大气的方法就是拟合（类似Blin-Phong），这里只要知道 $\theta$ （向上看的角度）和 $\gamma$（与太阳的夹角） ，就可以算出颜色。
![[Analytic_Atmosphere_Appearance_Modeling.png]]
Pros：简单
Cons：只能做地表，而且所有的参数都是固定写死的

### 4.2 Participating Media
气溶胶、空气中小分子称为Participating Media，形成了介质，形成光线的复杂现象。
其与光的相互作用效果有：
- 吸收一部分
- Out-scattering 四处散射
- Emission 自发光
- In-scattering 周边气体分子对你的辐射
四者相加，就为 **Radiative Transfer Equation (RTE)** 辐射传递方程。
由这些组成了 **Volume Rendering Equation (VRE)**，即为 RTF关于路径的积分。
从一个点出发，经过空气介质，到眼睛又多少的能量
![[RTE_VRE.png]]
这里有两个重要的影响：Transmittance 通透度；Scattering 散射度

### 4.3 Real Physics in Atmosphere
**Scattering Types**
- Rayleigh Scattering 
	当空气中介质的尺寸远小于光的波长时光会均匀散射，越短的波长散射的越厉害。下面为拟合的方程，其中参数 `h` 指的是海拔高度
	![[Rayleigh_Scattering_Equation.png]]
- Mie Scattering 
	当空气中介质的尺寸远接近或大于光的波长时，散射会有方向性，但与波长无关
	![[Mie_Scattering_Equation.png]]
现在的问题还是 Single Scattering，但实际上是有很多很多的散射 Multi Scattering

### 4.4 Ray Marching
为了解决Multi Scattering 的计算问题，可以沿着射线把效果积分下去。
![[Ray_Marching.png]]

可以使用 Precomputed Atmospheric Scattering，在运行前将所有可能方向的值存储在一个表上（四维），然后运行时读取表中的数据即可。只需要存储3个角度的信息以及高度，就可以知道任何远处的散射值
![[Precomputed_Atmospheric_Scattering.png]]

### 4.5 Production Friendly Quick Sky and Atmosphere Rendering
#### Simplify Multi-scattering Assumption 
假设对一个小分子散射的各向分布均匀，均匀光照射时，这样反射就是一个百分比衰减的过程，只要算一两个点就可以知道百分比，然后就可以用等比数列计算，可以算出无限次散射后的光的颜色的贡献度

对思维表，把高度和太阳位置均固定，然后就可以变为2维

## 5 Cloud
表示方法：
- Mesh-Based Cloud Modeling
- Billboard Cloud
- Volumetric Cloud Modeling（主流方法）缺点是复杂

