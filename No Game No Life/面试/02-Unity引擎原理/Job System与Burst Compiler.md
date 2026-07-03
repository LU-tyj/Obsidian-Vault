---
title: "Job System与Burst Compiler"
category: Unity引擎原理
tags: [Unity, Csharp, 网易互娱, Job System, Burst, DOTS]
frequency: ⭐
difficulty: 困难
companies: [网易互娱]
status: new
last_reviewed:
next_review:
related:
  - "[[ECS架构]]"
  - "[[Unity 协程原理]]"
  - "[[Csharp GC 垃圾回收]]"
---

## 一句话结论（自测用）
> Job System = Unity 的安全多线程框架，将计算密集任务放到 Worker Thread 并行执行。Burst Compiler = 将 Csharp Job 代码编译为高性能 LLVM 机器码。两者结合可实现接近 C++ 的性能，主要用于 DOTS/ECS 场景。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **Csharp Job System**：
   - 将计算密集型任务（寻路、物理计算、大量实体更新）从主线程移到 Worker Thread
   - 通过 `IJob` / `IJobParallelFor` 接口定义任务
   - **安全机制**：使用 `NativeContainer`（NativeArray / NativeList 等）而非托管对象，编译器通过 safety system 检测数据竞争
   - **依赖管理**：`JobHandle` 控制任务间的依赖和完成等待
   ```csharp
   [BurstCompile]
   struct MyJob : IJobParallelFor {
       [ReadOnly] public NativeArray<float> input;
       [WriteOnly] public NativeArray<float> output;
       public void Execute(int index) {
           output[index] = math.sqrt(input[index]);
       }
   }
   
   // 调度
   var job = new MyJob { input = input, output = output };
   JobHandle handle = job.Schedule(input.Length, 64);
   handle.Complete(); // 等待完成
   ```
2. **Burst Compiler**：
   - 基于 LLVM 的编译器，将 Csharp 子集（HPCsharp / High-Performance Csharp）编译为优化的原生机器码
   - 支持 SIMD 向量化指令
   - 必须是 `struct` 实现 `IJob` 接口，且 `[BurstCompile]` 标记
3. **结合使用的收益**：
   - 多线程并行（Job System）
   - SIMD 向量化（Burst）
   - 无 GC（NativeContainer 非托管内存）
   - 接近 C++ 的性能水平

## 详细解析

### NativeContainer 类型
| 类型 | 说明 |
|------|------|
| `NativeArray<T>` | 连续内存数组，仅值类型 T |
| `NativeList<T>` | 动态大小的 NativeArray |
| `NativeHashMap<K,V>` | 哈希表，非托管 |
| `NativeQueue<T>` | 队列，非托管 |

关键约束：只能在 Job 中使用 `NativeContainer`，不能用托管对象（List/Array/Dictionary 等）。

### Job 依赖链
```csharp
// Job B 依赖 Job A 完成
JobHandle handleA = jobA.Schedule();
JobHandle handleB = jobB.Schedule(handleA); // B 等待 A 完成

// 同时调度多个独立 Job
JobHandle handleC = jobC.Schedule();
JobHandle combined = JobHandle.CombineDependencies(handleB, handleC);
```

### 什么时候用 Job System？
- **适合**：大量独立元素的并行计算（寻路、物理、粒子）、CPU 密集型、能用 NativeContainer 表示数据
- **不适合**：依赖 Unity API 的逻辑（GameObject/Transform 不能进 Job）、少量数据（调度开销高于计算开销）、IO 密集型

## 面试官常见追问
- Job System 如何保证线程安全？（安全系统在编译时检测：不允许 NativeContainer 同时有多个写 Job 或有读 Job + 写 Job 并发）
- Burst 编译的代码为什么比普通 Csharp 快？（LLVM 优化 + SIMD 向量化 + 值类型零 GC + 无虚调用无接口派发）
- Job System 和 ECS 的关系？（ECS 的 System 通常用 Job System 实现并行，两者紧密配合但独立可用）

## 关联知识点
- [[ECS架构]]
- [[Unity 协程原理]]
- [[Csharp GC 垃圾回收]]

## 原始出处
- GitHub面经_性能优化 Q15
