## 1 Introduction
这是一片记录平台跳跃类型游戏手感如何提升的笔记。参考：
1. [Ultimate 2D Controller](https://github.com/Matthew-J-Spencer/Ultimate-2D-Controller/tree/main) 学习角色基本跳跃手感优化
2. [Celeste](https://www.mattmakesgames.com) 学习蔚蓝的角色控制技巧
3. [Git-amend 3D Platformer](https://github.com/adammyhre/3D-Platformer) 学习角色状态机的实现

---

## 2 How to improve your jump
### 2.1 自建Col
只使用 Unity Collider 中的 bound，而不使用其他因素。

当头部检测到天花板时，将速度设置为 `Mathf.Min(0, _frameVelocity.y)`

`CheckCollision()` 大致思路：
1. `Physics2D.queriesStartInColliders = false;` 将能否检测发射体自身设为false，因为我们是通过发射Capsule来判断碰撞，防止检测到自己
2. 发射Capsule来判断 `groundHit` & `ceilingHit`
3. `if else` 分类判断，比如检测到天花板将速度降为0
4. 复原`Physics2D.queriesStartInColliders

通过自定义Collision规则，来防止出现一些奇怪的手感和bug（我的老项目如果角色跳跃撞到顶会出现一些奇妙的动画播放bug）

### 2.2 Jumping
实现跳跃手感优化主要有：
- Jump Buffering（预输入），当角色还没落地时输入落地会跳起来
- Coyote Time（土狼时间），当角色离开平台短时间内依旧可以跳跃
- Jump Corner Correction（边缘修正），当你跳跃一点点碰到头时自动修正x
- 跳跃曲线，包含按的时间，重力变化，等等
>所有的这些都是通过Timer来进行控制，而不是简单的按下space然后就给一个冲量然后放着不管了。

处理跳跃的实现其实比较简单，判断是否能跳跃 -> 处理跳跃，然后接下来就交给Jump函数了。

### 2.3 Gravity
区别空中和地面的重力作用

