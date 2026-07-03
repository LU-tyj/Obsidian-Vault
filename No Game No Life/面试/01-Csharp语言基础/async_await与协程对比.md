---
title: "async_await与协程对比"
category: Csharp语言基础
tags: [Csharp, Unity, 网易互娱, 异步, 协程]
frequency: ⭐
difficulty: 中等
companies: [网易互娱]
status: new
last_reviewed:
next_review:
related:
  - "[[Unity 协程原理]]"
  - "[[Csharp GC 垃圾回收]]"
---

## 一句话结论（自测用）
> `async/await` = Csharp 编译器生成状态机的异步语法糖，不阻塞线程。Unity 协程 = 基于 `IEnumerator` 的主线程分步执行。区别：async/await 可以真正异步（Task 在线程池跑），协程始终在主线程；async/await 返回 `Task`，协程返回 `IEnumerator`。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **async/await 原理**：
   - `async` 标记方法是异步方法
   - `await` 等待异步操作完成，**不阻塞当前线程**
   - 编译器将 async 方法转化为**状态机**，在 await 处分段执行
   - 返回值是 `Task` / `Task<T>`，可以用 `.Result` 或 `await` 获取结果
2. **Unity 协程原理**：
   - 基于 `IEnumerator` + `yield` 语法
   - 运行在**主线程**
   - `yield return null` = 下一帧继续
   - 调度由 Unity 引擎在 Update 之后管理
3. **关键区别**：

| | async/await | Unity 协程 |
|--|------------|-----------|
| 执行线程 | 可在线程池（await Task.Run） | 仅主线程 |
| 返回值 | Task / Task\<T\> | IEnumerator |
| 调度 | .NET TaskScheduler | Unity 引擎 Update 后 |
| 适用 | 网络请求、文件 IO、CPU 密集（Task.Run） | 延时、分帧、动画 |
| Unity API | 不能直接调 | 可以 |
| 异常处理 | try-catch | try-catch（有限支持） |

4. **Unity 中 async/await 使用注意事项**：
   - `await` 后的代码可能在**非主线程**执行，不能访问 Unity API
   - 需要用 `UnityMainThreadDispatcher` 或 UniTask 来安全切回主线程
   - **UniTask** 是 Unity 的零 GC 异步方案，解决原生 Task 的 GC 问题

## 详细解析

### UniTask -- Unity 的 async/await 最佳实践
```csharp
// 原生 Task：每次 await 产生 GC（状态机装箱）
async Task<int> GetDataAsync() { ... }

// UniTask：零 GC 的 async/await（基于值类型状态机）
async UniTask<int> GetDataAsync() { ... }

// UniTask 的优势：
// 1. 零 GC（struct 状态机）
// 2. 支持 Unity 生命周期（playerLoop）
// 3. 可安全调用 Unity API
// 4. 支持 CancellationToken
await UniTask.Delay(1000); // 类似 WaitForSeconds
await UniTask.Yield();     // 类似 yield return null
await UniTask.NextFrame(); // 等下一帧
```

### 什么时候用协程，什么时候用 async/await？
- **协程**：分帧处理大量循环、等待动画完成、需要安全调用 Unity API
- **async/await（UniTask）**：网络请求、文件 IO、需要返回值、需要 CancellationToken 取消

## 面试官常见追问
- async 方法没写 await 会怎样？（同步执行，编译器会警告）
- `Task.Result` 和 `await` 的区别？（Result 会阻塞当前线程，await 不阻塞）
- unity 协程能用 async/await 替代吗？（UniTask 可以替代大部分协程场景，且功能更强大）

## 关联知识点
- [[Unity 协程原理]]
- [[Csharp GC 垃圾回收]]

## 原始出处
- GitHub面经_CSharp基础 Q14-Q15
