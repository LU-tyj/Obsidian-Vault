---
title: "JobSystem与Burst编译器"
category: 性能优化与内存管理
tags: [性能优化, Job System, Burst, DOTS, 多线程, Unity, 网易互娱]
frequency: ⭐⭐
difficulty: 较难
companies: [网易互娱]
status: new
last_reviewed:
next_review:
related:
  - "[[CPU性能优化]]"
  - "[[GC机制与优化]]"
---

## 🎯 一句话结论（自测用）
> Job System 将计算密集型任务从主线程调度到工作线程，利用多核并行；Burst Compiler 将 Csharp Job 代码编译为高性能机器码。两者结合可接近 C++ 性能。应用场景：寻路、物理计算、大量实体处理、粒子更新、碰撞预筛。数据必须使用 NativeArray/NativeSlice，避免托管对象，结构体应为 blittable。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **Job System 原理**：
   - 将计算任务封装为 Job（实现 IJob 或 IJobParallelFor）
   - 通过 JobHandle 管理依赖链和调度
   - Unity 自动将 Job 分配到工作线程执行
   - 结果回主线程后应用到 GameObject/Component
2. **Burst Compiler 原理**：
   - 针对 Csharp 子集的 AOT 编译器
   - 编译为 LLVM IR，再生成优化后的机器码
   - 利用 SIMD 指令集和自动向量化
   - 需要 `[BurstCompile]` 标记
3. **使用条件**：
   - 数据使用 `NativeArray<T>`、`NativeSlice<T>` 等原生容器
   - 不能包含托管对象引用（class、string 等）
   - 结构体应为 blittable（非托管类型）
   - 不能在 Job 内访问 UnityEngine 对象或主线程 API
4. **主线程通信**：
   - 生产者 Job 写入 NativeQueue/NativeList
   - 主线程 `jobHandle.Complete()` 后读取并应用到 GameObject
   - UI 或物理修改必须回到主线程
5. **IL2CPP vs Mono**：
   - Mono：JIT 编译，支持动态代码生成（如 Emit）
   - IL2CPP：AOT 编译，iOS 必需，性能约 1.5x，不支持 Emit

## 🔍 详细解析

### Job 类型
| Job 接口 | 说明 |
|---------|------|
| IJob | 单个 Job 执行一次 |
| IJobParallelFor | 并行执行，每个索引独立 |
| IJobParallelForTransform | 并行操作 Transform（只读） |

### 依赖链管理
```csharp
JobHandle jobA = jobAHandle.Schedule();
JobHandle jobB = jobBHandle.Schedule(jobA); // B 依赖 A
JobHandle jobC = jobCHandle.Schedule();
JobHandle combined = JobHandle.CombineDependencies(jobB, jobC); // 等待 B 和 C
combined.Complete(); // 主线程等待
```

### 注意事项
1. **避免过早 Complete**：主线程 `Complete` 阻塞等待 Job 完成，过早调用失去并行优势
2. **NativeArray 生命周期**：必须在 Job 完成后才能释放 NativeArray
3. **内存分配器**：使用 `Allocator.TempJob`（Job 期间）或 `Allocator.Persistent`（长期）
4. **禁用 Safety Checks**：Release 构建时关闭以提高性能

### Burst 优化原理
- 自动向量化（SIMD）：将循环操作映射到 CPU 的 SIMD 指令
- 函数内联：消除函数调用开销
- 循环展开：减少分支预测失败
- 常量折叠：编译期计算常量表达式

## 💬 面试官常见追问
- **Job System 和 Csharp Task/Thread 的区别？** → Job System 由 Unity 调度，无上下文切换开销（利用 Job Stealing），自动负载均衡；Csharp Thread 由 OS 调度，有上下文切换开销
- **什么情况下 Job System 反而更慢？** → 数据量太小（调度开销 > 计算收益）、频繁 Complete 阻塞、数据拷贝太多
- **Burst 不能编译什么？** → 无法编译托管对象（class、string、委托）、try-catch、foreach（对 NativeArray 可以）
- **和 ECS 的关系？** → DOTS = ECS + Job System + Burst，三者配合使用效果最佳但不必须捆绑

## ⚠️ 我曾经的误区 / 网上常见错答
- 误区：DOTS 必须三者一起用。Job System + Burst 可独立于 ECS 使用于传统 GameObject
- 误区：IL2CPP 后没有 GC。IL2CPP 有自己实现的 GC，不是 Mono 的 Boehm GC

## 🔗 关联知识点
- [[CPU性能优化]]
- [[GC机制与优化]]

## 📎 原始出处
- GitHub面经_性能优化 Q15：Job System 和 Burst Compiler
- 多线程与Job.md：Job 调度注意事项与主线程通信
