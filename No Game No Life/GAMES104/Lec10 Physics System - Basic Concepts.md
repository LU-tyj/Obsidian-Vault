## 1 Actor & Shapes
### 1.1 Actor
Actor 分为3种，在unity rigidbody组件中可以看到，分别为static、dynamic、kinematic（游戏设计师设计的动作，动画驱动的感觉），除此之外都可以变为Trigger

### 1.2 Actor Shapes
![[Actor Shapes.png]]
>多用简单的形状

**Shape Properties** : Mass, Density, Center of Mass, Friction & Restitution (physics material 摩擦系数 & 弹性系数)

---

## 2 Force & Movement
### 2.1 Force
让游戏世界的物体能动起来
在游戏世界中经常使用 Impulse，冲量

### 2.2 Movement
物理学是这样的
很多地方都需要进行积分（比如加速度积到速度，速度积到位移），游戏中按每个tick更新物体位置。
- 可以用显式欧拉积分来化简（用当前速度和力预估未来的速度和位移），但容易出现能量不守恒的问题。
- 还有隐式欧拉法，假设能知道未来的状态，用未来的状态反推现在的状态。此时会出现能量的衰减，更加真实了。但缺点也是不知道未来的状态。
- 半隐式欧拉法，最主要的方法。用当前力算出未来的速度，在用未来的速度算出未来的位移。

---

## 3 Rigidbody Dynamic
现在考虑上物体的旋转
![[Angular Values vs. Linear Values.png]]

---

## 4 Collision Detection
- Broad Phase : 先用AABB判断是否会碰撞
- Narrow Phase : 再具体判断是哪个部位以及力的碰撞

### 4.1 Broad Phase
方法1：BVH（树状结构）
方法2：Sort and Sweep 根据坐标轴判断AABB是否有交集（将所有物体的AABB的左右边界的x坐标投影到坐标轴上，如果顺序乱了，那么就可能有交集，再沿着y轴排序一次，核心想法是在移动一两个物体后排序效率很高）

### 4.2 Narrow Phase - Objectives
碰撞的信息：
![[Narrow Phase.png]]

三种算法：
- Basic Shape Intersection Test : 比如两个球之间求交点，判断球心距离与半径
- Minkowski Difference-based Methods : 两个形体有交点，Minkowski Difference一定过原点。使用GJK算法来找到
- Separating Axis Theorem (SAT) : 一定能找到一个轴（以边为轴），如果不相交，所有顶点的投影都会不想交，3D中为面

### 4.3 Collision Resolution
当检测到碰撞后，要想办法把他们分开来。
最简单的方法是加一个相反的力（但容易出现一堆东西叠一起时炸开来）
把力学问题变成一个数学的约束问题（拉格朗日力学，把力学变成一个反向约束的问题）来回小冲量跌代，到多少误差或者上限次数后停止

Raycast : Multiple hits, Closest hit, Any hit
Sweep
Overlap

---

## 5 Efficiency, Accuracy and Determinism
Simulation Optimization - Sleeping 当一个rb不动一段时间停止对其计算，当受到力后再叫醒

Continuous Collision Detection 移动速度过快导致卡进模型里或穿墙
- 简单粗暴的方法 —— 增大墙厚度
- CCD 对物体运动进行保守的估计，怎么移动是安全的

Determinism Simulation 相同输入相同输出
- 步长一致
- 算法具体的选择要一致
- 浮点数的一致性
