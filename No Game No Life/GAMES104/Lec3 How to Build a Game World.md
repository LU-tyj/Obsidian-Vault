[[GAMES104_Lecture03_How to Build a Game World.pdf]]

根据 [[Lec2 Layered Architecture of Game Engine]] ，我们知道了 Game Engine 的基本架构，现在要来学习如何构造一个游戏世界。

游戏世界主要组成有：Static Game Objects, Environments, Other Game Objects (Air Wall, Trigger Area)。我们把这些统称为 **Game Object (GO)**

## 1 How to Describe a Game Object
描述物体时，可以分为两类：`Property` 以及 `Behavior`。这样就可以用一个简单的类来定义一个 GO，以一个面向对象的逻辑构建这个世界。
> 虽然这种方式非常简单，但是随着 GO 的增多，难以合适表达子类关系。

所以现在最常用的的模式为 **Component Base**。下图就是以无人机为例子。
![[Component_of_Drone.png]]
![[Components_in_Commercial_Engines.png]]

**总结**：游戏世界中所有物体由 GO 组成，而每个 GO 又是 Component-Base 的。

---

## 2 How to Make the World Alive
### 2.1 Make Alive
- **Object-based Tick**: 依次调用每个 GO 内部所有 component 中的 `tick()` 函数，就可以实现 GO 的改变移动
- **Component-based Tick**: 依次调用所有 GO 的 component，不管 GO。就像做饭一样，要照顾流水线。

### 2.2 GO Interaction
除了 GO 自己的运动逻辑，还要考虑 GO 之间的交互。这里就引入了 `Events` 。
以炸弹爆炸为例子：
![[Bomb_Explode_Event.png]]

---

## 3 How to Manage Game Objects
知道GO如何活动以及交互，还需要管理和通知所有的 GO。
GO 被管理在场景 scene 中，每个 GO 都有自己的 ID 以及 Position。通过分割世界成小格子来进行管理、查找目标 GO。
![[Scene_Management.png]]


现在最主流的是 **BVH (Bounding Volume Hierarchies)** ，给每一个物体一个 Bounding Box（参考 GAMES101 Ray Tracing 部分）。

设计的难题在于：`tick()` 的执行顺序；`event` 的传递混乱性......
