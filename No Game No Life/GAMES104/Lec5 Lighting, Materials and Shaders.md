[[GAMES104_Lecture05_Rendering on Game Engine_Lighting, Materials and Shaders.pdf]]

## 1 The Rendering Equation
![[The_Rendering_Equation.png]]

但Rendering非常困难：
1. 物体对光源是否可见，以及光源本身的复杂性；
2. 积分运算难以在硬件上计算；
3. 光会反射，导致任何物质都是光源。

---

## 2 Starting from Simple
### 2.1 Simple Light Solution
只有一个主光源，环境自身的光源取平均称为 `ambient light`，对高反射率物体使用了环境贴图 `environment map`

### 2.2 Blinn-Phong Materials
![[Blinn-Phong_Materials.png]]
算出 **BRDF**
但这个会带来问题，导致能量不守恒，在光线追踪过程中，会无限放大震动；而且对于复杂的材质，Blinn-Phong 模型难以表示。

### 2.3 Shadow
游戏引擎行业使用了 **shadow map**，从光的视角渲染整个场景。但也出现了自遮挡的问题，光源和摄像机采样频率不同。
![[Shadow_Map.png]]

### 2.4 Basic Shading Solution
Simple Light + Ambient, Blinn-Phong Materials and Shadow Map.

---

## 3 Pre-computed Global Illumination
假设场景中每个物体是不动的，所以进行提前计算，实现很好的效果。
预计算即是用空间换时间。
把三维空间展开在一个2D纹理上。
全局光照对于真实感的刻画非常重要。
![[Global_Light.png]]

如何计算全局光照？
目标问题：在 PBR / IBL 中，漫反射项本质是一个球面积分

$$  
E(\mathbf{n}) = \int_{\Omega} L(\omega) , \max(0, \mathbf{n}\cdot\omega), d\omega  
$$

- $L(\omega)$：环境光贴图（HDRI）
    
- $\mathbf{n}$：表面法线
    
- $\max(0, \mathbf{n}\cdot\omega)$：Lambert BRDF

直接数值积分：**慢，不适合实时**
即寻找绕过数值积分计算的方法。

### 3.1 Spherical Harmonics
球谐函数，通过这样来表示全局光照。
![[Spherical_Harmonics_Encoding.png]]
只需要存储 12 （4 * 3RGB）个参数，就可以表示全局光照。
==利用这个方法可以对全局光照进行压缩表示==
接下来以9个SH参数（二阶段）为例子进行讲解：
1. SH 参数是什么
	类似傅立叶系数，是一段信号在正弦/余弦基上的投影；SH 系数是一张“方向光分布”在球谐基上的投影
	**每个系数表示环境光在某一种“球面模式（pattern）”上的强度权重。**
2. SH的核心思路
	把环境光$L(\omega)$ 投影到 SH 基： $L(\omega) \approx \sum_{l=0}^{2}\sum_{m=-l}^{l} c_{lm} Y_l^m(\omega)$
	Lambert 卷积核 $\max(0, n\cdot\omega)$也能解析地投影到 SH → 得到一组**固定常数核系数** $k_l$
	运行时直接点积：$E(\mathbf{n}) \approx \sum_{l,m} k_l  c_{lm} Y_l^m(\mathbf{n})$
	把「球面积分」变成「9 项点积」，**每像素 O(1)**
3. 渲染时的伪代码
```cpp
vec3 EvalDiffuseSH(vec3 n)
{
    float x = n.x, y = n.y, z = n.z;

    float sh[9];
    sh[0] = 0.282095;
    sh[1] = 0.488603 * y;
    sh[2] = 0.488603 * z;
    sh[3] = 0.488603 * x;
    sh[4] = 1.092548 * x * y;
    sh[5] = 1.092548 * y * z;
    sh[6] = 0.315392 * (3.0 * z * z - 1.0);
    sh[7] = 1.092548 * x * z;
    sh[8] = 0.546274 * (x * x - y * y);

    vec3 color = vec3(0);
    for (int i = 0; i < 9; ++i)
        color += shCoeff[i] * sh[i];  // shCoeff[i] 是预计算的 RGB

    return color;
}
```

### 3.2 SH Lightmap
把全局光照画在一张图上，这张图称为 atlas。
Precomputed GI -> UV Atlas ->Lighting + Direct Lighting -> Final Shading with Materials

Pros：
- 运行时效率高
- Gl 细节多效果好
Cons：
- 计算时间长
- 只能处理静态物体和静态的光
- 存储空间占用大

### 3.3 Light Probe
在空间上撒一堆采样点 Probes，对每个Probe进行光场采样。对其中的物体使用插值来获得自己的光照。

Pros：
- 运行时效率高
- 可以处理动态物体和静态物体
Cons：
- Gl 细节一般

---

## 4 Physical-Based Material
没看懂

---

## 5 Summary of Popular AAA Rendering
- Lightmap + Light probe 
- PBR + IBL 
- Cascade shadow + VSSM 