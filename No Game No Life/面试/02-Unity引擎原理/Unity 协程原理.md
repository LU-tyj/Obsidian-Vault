---
title: "Unity 协程原理"
category: Unity引擎原理
tags: [Unity, Csharp, 网易互娱, 协程, IEnumerator]
frequency: ⭐⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[Unity 生命周期]]"
  - "[[Csharp GC 垃圾回收]]"
  - "[[async_await与协程对比]]"
---

## 一句话结论（自测用）
> Unity 协程 = Csharp 的 `IEnumerator` + `yield` 语法糖，**运行在主线程**上，通过分步执行实现"等待"效果，不是多线程。Unity 内部维护协程状态机，在 Update 之后调用 `MoveNext()` 推进执行。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **原理**：
   - 底层是 Csharp 迭代器（`IEnumerator` / `IEnumerable`）+ `yield return` 语法
   - 协程方法编译后变成一个**状态机类**，`MoveNext()` 方法推动状态跳转
   - Unity 引擎在**主线程**的 Update 之后、LateUpdate 之前检查协程状态，调用 `MoveNext()`
   - `yield return null` = 下一帧继续；`yield return new WaitForSeconds(n)` = n 秒后继续
2. **与线程的本质区别**：
   - 协程在主线程运行，线程在独立线程运行
   - 协程不能做密集计算（会卡主线程），线程可以
   - 协程可以安全调用 Unity API，线程不能
   - 协程调度由 Unity 引擎管理，线程由 OS 管理
3. **使用场景**：
   - 延时操作（WaitForSeconds）
   - 异步加载资源（配合 AssetBundle / Addressables）
   - 分帧处理大量计算（每帧算一点，避免卡顿）
   - 等待条件满足（WaitUntil / WaitWhile）

## 详细解析

### yield return 指令全解
| yield 指令 | 等待条件 |
|-----------|---------|
| `yield return null` | 下一帧 Update 后继续 |
| `yield return new WaitForSeconds(n)` | n 秒后继续（受 Time.timeScale 影响） |
| `yield return new WaitForSecondsRealtime(n)` | n 秒后继续（不受 Time.timeScale 影响） |
| `yield return new WaitForEndOfFrame()` | 渲染完成后继续 |
| `yield return new WaitForFixedUpdate()` | 下一次 FixedUpdate 后继续 |
| `yield return new WaitUntil(() => condition)` | 条件为 true 时继续 |
| `yield return new WaitWhile(() => condition)` | 条件为 false 时继续 |
| `yield return StartCoroutine(another)` | 等待另一个协程执行完毕 |
| `yield break` | 立即结束协程 |

### 协程的生命周期管理
1. **启动**：`StartCoroutine(IEnumerator)` 或 `StartCoroutine("MethodName")`（字符串方式性能差，不推荐）
2. **停止**：`StopCoroutine(coroutine)` / `StopAllCoroutines()` / 禁用或销毁脚本时自动停止
3. **重要**：`StopCoroutine` 只能停止以 `StartCoroutine(IEnumerator)` 启动的协程，字符串方式需要用字符串停止

### 协程为什么不能做密集计算？
因为协程本质是切分 Csharp 代码块的语法糖，不是真正的异步。每一段代码块仍然在主线程的 Update 之后执行。如果你的协程体内有大量计算，仍然会卡住主线程。解决方法：
- **时间分片**：在协程内每计算一小段就 `yield return null`
- **Job System**：把密集计算放到工作线程
- **不要用协程**：用真正的多线程（注意不能调 Unity API）

## 面试官常见追问
- 协程是线程吗？（不是。协程在主线程上跑，不是多线程）
- 协程在生命周期中哪个阶段执行？（Update 之后、LateUpdate 之前。yield 指令决定具体时机）
- 如何实现一个"等待直到动画播放完毕"的协程？（`yield return new WaitWhile(() => animator.GetCurrentAnimatorStateInfo(0).normalizedTime < 1f)`）
- `yield return null` 和 `yield return new WaitForEndOfFrame()` 的区别？（前者在 Update 后，后者在渲染完成后）
- StopCoroutine 为什么有时候不生效？（检查是否用了 `StartCoroutine("MethodName")` 字符串重载，这个很难被 IEnumerator 方式停止）

## 我曾经的误区 / 网上常见错答
- **错**："协程 = 轻量级线程" —— 协程不是线程，是单线程上的协作式调度
- **错**："WaitForSeconds 的计时是从 yield 开始" —— 实际的等待从该帧渲染完成后才开始计算
- **错**："协程的方法名重载比较好" —— 字符串重载有 GC 分配、无法传参、调试困难三重劣势
- **错**："脚本禁用后协程还在" —— 不会，MonoBehaviour 的协程依赖其宿主组件，禁用/销毁即停止

## 关联知识点
- [[Unity 生命周期]]
- [[Csharp GC 垃圾回收]]
- [[async_await与协程对比]]
- [[对象池]]
- [[Job System与Burst Compiler]]

## 原始出处
- GitHub面经_Unity引擎 Q5-Q7
- GitHub面经_CSharp基础 Q14-Q15
- 博客园 多论坛面经汇总 3.2 节
- BOSS直聘 面试评价汇总
