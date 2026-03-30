[MyCeleste 项目地址](https://github.com/LU-tyj/MyCeleste)
用来记录复刻蔚蓝过程中遇到的问题与相关解决方案。

## 3.30
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
