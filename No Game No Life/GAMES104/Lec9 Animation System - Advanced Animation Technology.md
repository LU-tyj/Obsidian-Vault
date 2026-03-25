
==如何让动画活灵活现==

## 1 Animation Blending
比如实现从走到跑，基本的原理就是线性插值
所有的动画的插值都是在clip之间进行

### 1.1 Calculate Blend Weight
如果是因为速度变化，可以通过速度来计算weight，保证weight求和为1（一个很简单的线性插值）

### 1.2 Align Blend Timeline
保证跑步和走路的clip都是整个的周期，可以更容易找到用来插值的keyframe

---

## 2 Blend Space
我们可以blend 往左走，往右走，原地走。三者在一条线上，称为 1D Blend Space
在此基础上加上前后，就形成了 2D Blend Space（但实际上左前走很快就会切换到左前跑）

**Skeleton Masked Blending**：但动画角色鼓掌时，可以蹲下和站起来鼓掌，只要用 mask 来只分开作用在 joint 上，然后进行混合。

**Additive Blending**：不仅只作用在局部skeleton，而且只存储其变化量（比如一个旋转），可以实现对着镜头点头。

---

## 3 Animation State Machine (ASM)
类似 FSM，isGround

### 3.1 ASM Definition
核心元素：nodes 以及 transitions

node的组成：Blend Space以及Clip

transition的分类：Smooth（用weight）；Frozen（直接改变）

### 3.2 ASM Methods
Layered Methods 层状状态机，详情参考[[2.6 State Pattern]]
但最主要的方法时 Animation Tree (Blend Tree)
![[BlendTree.png]]

使用 Blend Tree Control Parameters 来改变动画的组装

---

## 4 Inverse Kinematics (IK) 反向动力学
人的动作会被环境约束，我们前面所提及的内容都是 Forward Kinematics，通过一个个joints算过来；而IK就是受到外力影响，有约束的动力学。

### 4.1 Two Bones IK
比如人物在不平的路上走，我们知道了踩的位置，以及几个Joint的位置，还有腿长（两个球求交点），我们就可以确定一个三角形，知道大腿要迈多少度，小腿要迈多少度然后把动画做出来。
![[Two Bones IK.png]]
但问题是两个球求交点求出的解在一个圆环上，就会出现一些奇怪的动作。
一个很简单的解法是在做动画时标出大腿朝向的位置，这样就好了。

当你去够一个东西时要判断是否能够到
==不能忘记骨骼自身也有Constraints==
如何去解决这个问题？

### 4.2 CCD (Cyclic Coordinate Decent)
将最上面的Joint向目标点翻转，然后继续翻转第二个joint，最后再重复展开，这样反复的旋转和展开，知道到达或接近目标点。但由于可能一次就翻到尾，导致看起来很怪，可以进行Optimize。

优化常用方法：
- 设置每个Joints的翻转角度上限，或者旋转后与目标点的距离要高于一个下限
- 越靠近根节点旋转的幅度越小

### 4.3 FABRIK (Forward And Backward Reaching IK)
直接从端点开始强行把Joint放在目标点，然后把skeleton放过来，再把下一个Joint放在经过位移的skeleton的尾部，重复这个过程。这样根节点动了，所以再从根节点开始拉回原点，再拉到端头。经过Forward & Backward，端点会逐渐接近目标点。

FABRIK也可以很好的解决约束问题，只需要保证每次端点都在约束角度内
![[FABRIK with constraints.png]]

但这两个都有需要迭代很多次的问题。
而且在游戏中的约束有非常多，上述的两种简单算法就无法实现这样的目的。

### 4.4 Jacobian Matrix
这个是解决多约束问题的解决方法。
具体在物理系统中展开。
是一个逐渐逼近的过程。

有了Animation Blending 以及 IK，我们就可以更新[[Lec8 Animation System]]中的Animation Pipeline
![[Animation Pipeline witch Blending & IK.png]]

