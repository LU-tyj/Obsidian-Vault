## 1 Event Mechanism
使用事件系统，让GO之间相互交流。
Publish-subscirbe Pattern有3个关键：Event Definition、Callback Registration、Event Despatching。

### 1.1 Event Definition
最简单的方法是定义一个Event基类，然后派生出一系列Event。
但这样写死代码的话，我们每写一个新的Event 就要重编译一遍引擎代码。

有很多方法，比如UE是注入，Unity用Csharp等等。

### 1.2 Callback Registration
当我们对事件使用 `invoke` 时，我们就会调用注册的函数。但问题是生命周期，如果给敌人注册了一个函数，敌人死了，这个还注册在这里，要如何解决？
- Strong Reference：你不准死，因为你注册了这个函数（但这个肉眼可见的问题大）
- Weak Reference：触发函数时检验一下这个函数是否有效（`?`语法糖）

### 1.3 Event Dispatch
消息来了马上call，但是会出现单线程函数中断执行，先去执行事件方法的问题，比如炸弹引爆其他炸弹，那么你就动不了了，要等所有炸弹炸完。

现代方法使用 `Event Queue`，再用序列化和反序列化进行存储和加载。最后使用Ring Buffer 进行循环调用，这样就不用引用更多内存。再对不同的系统事件进行batching，就可以很大的提高效率

Event Queue也有问题，包括事件执行的顺序。而且事件太多可能会超出这一帧的运行。

---

## 2 Game Logic
使用脚本语言（lua），可以方便热更新，也简单易懂，不会crash本体。
脚本语言工作可以参考[[4.1 Bytecode]]模式。
热更新可以直接改变函数指针指向的地址，这样就可以不用编译

但脚本语言的问题就是：没有面向对象、运行慢

---

## 3 3C
==Character, Control & Camera==

### 3.1 Character
包括角色的动作、控制，以及交互等等。
一般使用状态机来进行控制。

### 3.2 Control
处理各种各样的输入设备。
使用Event系统
Feedback，也就是control的核心

### 3.3 Camera
POV 相机位置、FOV 相机张角
相机效果 
