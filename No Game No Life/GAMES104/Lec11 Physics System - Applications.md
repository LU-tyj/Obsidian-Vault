## 1 Character Controller
角色控制是一种反物理的，是为了让游戏的行为符合自己的认知
要处理很多的问题

---

## 2 Ragdoll
处理角色与环境互动。在悬崖上处决敌人，敌人会自然掉下去，而不是播放完动画倒地在悬崖边缘

这里就又提到了 Human Joint Constrains，防止出现不自然的动作。可以先动画驱动Kinematic，然后再物理运算 Dynamic（动画和物理仿真边界在哪里？）动画播放+物理模拟

---

## 3 Clothing
最早的方法是直接用骨骼驱动的动画（Kinematic）来驱动衣料变化
然后就是用动力学骨骼（Dynamic）来驱动衣料变化

最主要的是 **Mesh-based Cloth Simulation**
- 先添加Physics Mesh，一般Physical Mesh的密度会远小于Render Mesh
- 给每个Mesh添加Constraints
- Set Cloth Physical Material（这里就可以细分了）

把cloth physical material模拟成弹簧质点模型。
受到 Spring force 以及 Spring damping force（弹簧阻力 F=-kv，因为cloth毕竟不质点）
对于一个布料上的质点，会受到：
- 重力
- 风力
- 空气阻力
- Spring force & Spring damping force（弹簧内部摩擦）
![[Cloth Solver - Mass-spring System.png]]
![[Verlet Integration.png]]

布料一个严重的问题是自穿插，解决方法可以给布料的物理模型加厚，或者把布料的物理仿真做的更细，还可以在布料里加一个立场，当穿过去的时候往回顶

---

## 4 Destruction
Chunk Hierarchy 把一个物体分成一个层次型的碎片
Connectivity Graph & Value 把碎片连在一起，并规定最大能承受的冲击，通过计算Damage来破坏

使用Voronoi算法生成chunk，随机生成一些种子，然后不断扩大半径只到全部覆盖
![[Destruction System.png]]

---

