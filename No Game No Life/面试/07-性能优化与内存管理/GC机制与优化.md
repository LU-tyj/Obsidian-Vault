---
title: "GC机制与优化"
category: 性能优化与内存管理
tags: [性能优化, GC, 内存管理, 垃圾回收, Csharp, Unity, 网易互娱]
frequency: ⭐⭐⭐
difficulty: 中等
companies: [网易互娱]
status: new
last_reviewed:
next_review:
related:
  - "[[内存优化策略]]"
  - "[[对象池设计]]"
  - "[[CPU性能优化]]"
---

## 🎯 一句话结论（自测用）
> Unity Csharp GC 采用标记-清除 + 分代回收（3 代）。优化三板斧：避免频繁分配（对象池、StringBuilder 替代字符串拼接）、减少装箱（泛型集合替代 ArrayList、避免 object 参数）、资源生命周期管理（Addressables Release、事件注销）。Lua GC 采用三色标记清除，无分代。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **GC 触发机制**：
   - 托管堆内存不足时自动触发
   - 可手动调用 `System.GC.Collect()`（应尽量避免）
   - 触发时所有托管线程暂停（Stop-the-World）
2. **分代回收**：
   - Gen0：新创建的小对象，回收最快最频繁
   - Gen1：从 Gen0 晋升的对象，缓冲层
   - Gen2：长期存活的对象，回收最慢
   - 大对象堆（LOH）：超过 85000 字节的对象，不参与分代迁移
3. **GC 优化三板斧**：
   - 避免频繁分配：对象池复用、StringBuilder 替代 string +/Format、避免 LINQ 生成闭包和临时列表
   - 减少装箱：泛型集合替代 ArrayList、避免将值类型作为 object 参数传递、用 `Conditional` 关闭 Log
   - 生命周期管理：场景切换时注销事件/委托、协程及时停止、Addressables Release
4. **Csharp GC vs Lua GC**：
   - Csharp：标记-清除 + 分代（3 代）
   - Lua：标记-清除、三色标记（白色=可回收，灰色=中间态，黑色=存活），不分代

## 🔍 详细解析

### GC 触发时机
1. 第 0 代充满时（最频繁）
2. `GC.Collect()` 被调用（应避免）
3. 系统内存不足时
4. App 进入后台时（iOS）

### 内存分配热点识别
| 操作 | GC 压力 | 替代方案 |
|------|---------|---------|
| `string + string` | 每次产生新字符串 | StringBuilder |
| `foreach` (值类型集合) | 旧 Mono 会装箱 | for 循环 |
| `LINQ` | 生成闭包和临时对象 | 手动循环 |
| `ArrayList` | 装箱 | `List<T>` |
| `Debug.Log` | 字符串拼接 | `Conditional` 关闭 |
| `Instantiate/Destroy` | 频繁分配释放 | 对象池 |
| 闭包/Lambda | 生成匿名类 | 提取为命名方法或缓存委托 |
| 协程的 `new WaitForSeconds` | 每次新对象 | 缓存 WaitForSeconds 实例 |

### 常见内存泄漏原因
1. **静态变量持有对象引用**：GC 无法回收
2. **事件/委托未注销**：对象仍被事件源引用
3. **AssetBundle 未释放**：Unload(false) 后资源常驻
4. **Resources.Load 后未 Unload**
5. **协程未停止**：一直在运行，持有对象引用
6. **单例持有已销毁对象的引用**

### Lua GC 三色标记
| 颜色 | 含义 |
|------|------|
| 白色（新） | GC 标记阶段后新创建 |
| 白色（旧） | 可回收状态 |
| 灰色 | 已标记，但其引用的对象未扫描完 |
| 黑色 | 存活，所有引用已标记完毕 |

### 检测工具
- Unity Profiler (Memory 模块)
- Memory Profiler（查看引用链）
- dotMemory（深度分析）
- XCode Instruments（iOS）
- 使用 `Profiler.BeginSample` / `EndSample` 标记关键区域

## 💬 面试官常见追问
- **为什么字符串拼接会产生 GC？** → Csharp 中 string 是 immutable 的，每次拼接都创建新字符串对象，旧字符串变成垃圾
- **装箱和拆箱的开销在哪里？** → 装箱在堆上分配新对象并拷贝值类型数据；拆箱需要检查和拷贝回栈上
- **怎么判断是不是 GC 导致的卡顿？** → Profiler 看 GC.Alloc 和 GC.Collect 的耗时分布；如果 GC 耗时占比高且频率高，说明有内存分配热点
- **Lua 三色标记如何保证增量式 GC？** → 分步执行标记阶段和清除阶段，插入正常执行，减少 Stop-the-World 时间

## ⚠️ 我曾经的误区 / 网上常见错答
- 误区：`string.Format` 比 `+` 拼接好。两者都产生 GC，应使用 StringBuilder
- 误区：关闭 GC 可以提升性能。Csharp 中无法真正关闭 GC，且堆满后会强制回收，更影响性能
- 误区：Unity 没有 GC。Unity 使用 IL2CPP 后依然有 GC（IL2CPP 实现自己的 GC，非 Mono 的 Boehm GC）

## 🔗 关联知识点
- [[内存优化策略]]
- [[对象池设计]]
- [[CPU性能优化]]

## 📎 原始出处
- GitHub面经_性能优化 Q9：常见内存泄漏原因及检测工具
- 优化.md：GC/内存优化的三板斧
- GitHub面经_Lua与热更新 Q12/Q13：Lua GC 与 Csharp GC 对比
- 博客园汇总：GC 机制为极高频考点
