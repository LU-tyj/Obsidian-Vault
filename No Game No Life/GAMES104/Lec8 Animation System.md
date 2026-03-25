## 1 Challenges in Game Animation
- **Interactive and dynamic animation** 既要接收用户的输入，又要响应环境的变化
- **Real Time** 大量的数据读取写入
- **Realism** 要求更加真实

![[Outline of Animation System.png]]

---

## 2 2D Animation Techniques in Games
**Sprite animation**：把贴图循环播放

**Live2D**：一堆小图原进行拼接，分别进行变换。定义每个图原深度，给每个图原生成控制网格（Art Mesh）。

---

## 3 3D Animation Techniques in Games
### 3.1 DoF (Degrees of Freedom)
自由度：一个物体能在多少维度变化
6D：平移3个，旋转3个

### 3.2 Approachs
- **Rigid Hierarchical Animation**
	最早的角色动画，把动画和骨骼绑定，像皮影戏
- **Per-vertex Animation**
- **Morph Target Animation**
- **3D Skinned Animation** 最主要的
- **Physics-based Animation**
- **Animation Content Creation**

### 3.3 Skinned Animation Implementation
#### 3.3.1 How to Animate a Mesh
1. Create mesh for a binding pose 
2. Create a binding skeleton for the mesh 
3. “Paint” per-vertices skinning weights to related skeleton 
4. Animate skeleton to desired pose 
5. Animate skinned vertices by skeleton and skinning weights
![[Animate a mesh.png]]

每个角色有三个坐标系：Local, Model, World
![[Different Spaces.png]]

#### 3.3.2 Skeleton for Creatures
骨骼由Joints（关节，刚体片段）的层级结构组成，其中有一个joint被选为root；每个joint都有一个父joint
>Joint 是关节，用来直接控制动画动作，用来存储
>Bone为骨骼，是两个关节之间的部分

一般来说正常的游戏人类骨骼有 50～100个joints，细节一点有300+ joints（斗篷、人脸、武器）

#### 3.3.3 Root Joint
一般表示人类的 Root Joint 在角色两脚中间，这样可以非常好的表示是否接触地面，以及角色的速度

#### 3.3.4 Bind Animation for Objects
如何实现人骑马？有一个Bind Point，两者的position和rotation都相同。
![[Bind Animation for Objects.png]]

#### 3.3.5 Bind Pose -- T-pose & A-pose
mesh的pose
![[Bind Pose.png]]

**Skeleton Pose**：骨骼运动时的一个状态，把pose连在一起就是动画。这时是由9 DoFs组成（还有3个方向的Scale）

### 3.4 Math of 3D Rotation
笛卡尔坐标系中，可以很好的表示2D-Rotation，表示成矩阵乘法。但是3D-Rotation会非常复杂。

#### 3.4.1 Euler Angle
这里就用了 Euler Angle，欧拉角，由三个角组成：
- **Yaw angle** : $\psi$ 
	绕Y轴的旋转，通常表示对象的左右转向
- **Pitch angle** : $\theta$
	绕X轴的旋转，通常表示对象的上下倾斜
- **Roll angle** : $\phi$
	绕Z轴的旋转，通常表示对象的侧倾
>旋转顺序不同，结果不同
>一般xyz顺序

**欧拉角的问题——万向锁**：当沿着y轴转了90度后，由于规定了旋转顺序为xyz，沿y轴旋转不会对x轴产生影响，但会对z轴产生影响，导致z轴与x轴重合，即减少了一个自由度（可以数学计算理解）

这里就是欧拉角的缺点了：
1. 万向锁
2. 难以插值
3. 难以进行旋转的叠加
4. 难以旋转到空间中的任意角度（只方便沿着xyz轴转）

#### 3.4.2 Quaternion
复数一个非常好的性质是可以通过正则化复数的乘法来表示角度相加。
![[Quaternion.png]]
四元数定义了ijk三个旋转参数
最有意思的是 $i^2 = j^2 = k^2 = ijk = -1$
这样可以左右同乘=> $ik = j$，其他同理

向量可以转换为四元数 $v_q = (0,v) = bi +cj + dk$

### 3.5 Joint Pose
Joint Pose 主要的变化：
- Orientation 旋转
- Position 位置
- Scale 缩放
这些变换都可以用矩阵表示（具体见GAMES101），形成变换矩阵 Affine Matrix
$$ M = R_{HM} T_{HM} S_{HM} $$
这样子节点Joint Pose的变换可以表示为其父节点的累乘。
>我们一般在 Local Space 进行插值，防止骨骼伸长，对角度进行插值，控制两个 Joint 的相对位置保持不变（关系满足Skinning Matrix）![[Interpolation Local Space vs Model Space.png]]

骨骼的存储就是把上面的joint的内容和变换进行存储

### 3.6 Simple Animation Runtime Pipeline
![[Simple Animation Runtime Pipeline.png]]

---

## 4 Animation Compression
### 4.1 Simplest Compression - DoF Reduction
舍弃存储一些没有用的维度，比如scale、Translate等（主要是Rotation）。

对旋转进行 Keyframe 关键帧插值，如果原始的数值和插值出来的数值超过一定阈值时，把那个点作为其关键帧。
>但线性插值可能不太符合旋转

使用 Catmull-Rom Spline 进行插值，更容易接近真实的 Rotation，也会少很多 Key Frame

### 4.2 Float Quantization
可以看 [Tiny ML](https://hanlab.mit.edu/courses/2024-fall-65940)中的浮点数量化章节，通过映射到 \[0, 1\]这个区间，来对浮点数进行量化

### 4.3 Quaternion Quantization
1. 可以通过只存储3个数，最后一个通过平方和为1算出；
2. 通过性质，去除最大的四元数，剩下的三个会处于$[-\frac{1}{\sqrt 2}, \frac{1}{\sqrt 2}]$ 这个区间内，这样我们只需要用 2 bit 标出哪个是最大值，然后剩下的3个数之用 15 bits 去存储。

### 4.4 Error Propagation
压缩带来的误差会随着 joint 进行累加，放大错误
分类分为：Data Error；Visual Error（最主要）

---

## 5 Animation DCC Process
动画是怎么做的
- Mesh 
- Skeleton binding
- Skinning
- Animation creation
- Exporting
