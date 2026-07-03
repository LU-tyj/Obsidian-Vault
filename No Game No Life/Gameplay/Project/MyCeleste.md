[MyCeleste 项目地址](https://github.com/LU-tyj/MyCeleste)
用来记录复刻蔚蓝过程中遇到的问题与相关解决方案。

## 0330
### 1 Jump Buffer 实现过程中出现大跳然后小跳一下
此时的实现跳跃思路：
转换从Locomotive到jump的条件：启动jumpTimer或者从空中落下

Press "K" -> jumpBufferTimer.Start() & TryJump() -> TryJump 会判断如果土狼时间或者IsGrounded -> 开启 jumpTimer
当检测到到达地面 -> 判断jumpBufferTimer是否启动 -> 启动 jumpTimer
当检测到离开地面 -> 开启coyoteTimer

通过jumpTimer是否正在运行 -> 判断是否持续每帧施加力，改变jumpVelocity -> 当持续时间结束或者在坠落时，增加重力 -> 同步rb.linearVelocityY 与 jumpVelocity

**实现了**coyote time，以及能持续按键来升高
**但是**，跳跃存在最低高度，因为刚开始给了一个jumpForce是恒定的；Jump Buffer存在bug，刚好落地的瞬间按下，会启动jumpBufferTimer和TryJump，JumpTimer就会重复Start，然后产生很大的初始速度以及后期再跳了一下，猜测原因是因为jumpVelocity分散，会出现重叠控制。

### 2 关于跳跃的改进
新版本的代码使用了新的跳跃机制，是一个做减法的跳跃系统。
1. 相比原本的按下按键持续施加jumpForce相比，现在使用如果在上升过程中没有按下按键就会施加一个重力，来阻碍上升，从而实现超级小跳。这样也避免了分散的jumpVelocity被重复地添加速度。
2. 改变了buffer jump实现的思路，为了正确实现buffer jump，我们在fixedUpdate中进行逐帧的检测，如果`jumpBufferTimer.IsRuning && isGround` 那么我们就会调用`ExcuteJump()`，统一管理Timers，开启`jumpTimer`，使状态机切换至jump
3. 普通情况按下，我们会在按下“K”时使用`TryJump()`，来判断土狼时间或者普通跳跃是否能够进行，然后调用`ExcuteJump()`
4. 引入了一个`endedJumpEarly`的bool变量，标识是否在到达最高点前停止按键。
>其实思路就是：判断 *普通跳跃*、*buffer jump*、*coyote time*，然后进行`ExcuteJump()` 进入Jump状态，然后使用HandleJump函数来处理跳跃的具体逻辑。

## 0401 
在3.31实现了ScriptableObject的添加，以及实现了自制的重力效果。

**现在有一个问题**：我的Jump虽然可以使用，但是判断分散，实行流程多，每帧的jumpBuffer的检查其实可以在状态切换中进行，刚开始速度的赋值可以在JumpState中进行，这样会将PlayerController中的代码分散到JumpState中。但带来的坏处是：Timer控制分散，需要将很多变量的值调整为public等。

## 0407
因为有些迷茫，要不要实现自定义物理，但被朋友指出这是在钻牛角尖，所以觉定能做出一个playable的游戏就完事。

现在完成了MoveX MoveY的逐像素移动，以及新增了jumpCorrection。本来有个问题是角色看起来不在地面上，也撞不了天花板，是因为PPU设置的太小，导致出现精度问题，现在将其修复为32，这样看起来正常多了。之后要把HitCeil和HitGround集中在 MoveX和MoveY中。

下午修复了jumpBuffer没有用（发现其实一直都是土狼时间在作用）以及连续按角色无法跳跃的问题。解决办法是从airState直接切换至jumpState，而不是从airState切换到locomotionState再判断jumpBuffer
```csharp
private bool ReturnToLocomotionState() => 
	isGrounded && !jumpTimer.IsRunning && !jumpBufferTimer.IsRunning;
```
>具体错误原因：我的PlayerState一直在AirState，因为我点按时jumpBufferTimer一直启动，结果就一直回不到locomotionState，也就无法进行跳跃。因此个AirState添加一个这样的状态就好了。
>如果直接移除 `!jumpBufferTimer.IsRunning`，由于jumpTimer受到jumpBufferTimer控制，其实就是会锁住，所以只能从AirState直接到跳跃，才能实现jumpBuffer

现在有个想法，这个项目就不要追求极致的完美，而是当一个学习项目，想到什么就加什么，这样然后与此同时做出正经的项目，这样挺好的

完成了冲刺的实现，虽然有点简陋，因为冲刺的消耗比较分散，但还是可以的。
