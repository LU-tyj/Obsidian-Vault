---
title: "Csharp GC 垃圾回收"
category: Csharp语言基础
tags: [Csharp, Unity, 网易互娱, GC, 内存管理]
frequency: ⭐⭐⭐
difficulty: 困难
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[Csharp 装箱与拆箱]]"
  - "[[Csharp 值类型与引用类型]]"
  - "[[Unity 协程原理]]"
  - "[[对象池]]"
---

## 一句话结论（自测用）
> Csharp GC 使用**标记-清除 + 分代回收**：从 GC Root 出发标记可达对象，清除不可达对象，第0代满了就触发。Unity 侧最核心的优化是**减少堆分配**（对象池、缓存引用、避免 Update 中 new）。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **算法**：标记-清除（Mark-Sweep）+ 压缩（Compact）+ 分代回收（Generational）
2. **三代模型**：
   - Gen 0：存放新创建的小对象，回收最频繁（通常几毫秒）
   - Gen 1：从 Gen 0 存活下来的对象，作为 Gen 0 和 Gen 2 的缓冲
   - Gen 2：长期存活的大对象，回收代价最大
   - LOH（Large Object Heap）：大于 85000 字节的对象直接放此，不参与分代
3. **工作流程**：
   - 标记阶段：从 GC Root 出发遍历引用链，标记所有可达对象
   - 清除阶段：清理未被标记的对象，释放内存
   - 压缩阶段（可选）：移动存活对象消除碎片
4. **触发时机**：Gen 0 内存满 / 手动 `GC.Collect()` / 系统内存不足
5. **GC Root 包括**：静态变量、线程栈上的局部变量、CPU 寄存器中的引用、已终结队列中的对象

## 详细解析

### GC Root 详解
面试中常用追问：**一个对象没有被任何变量引用，为什么没被 GC？**
答案：因为 GC 只看**可达性**而非引用计数。两个相互引用的对象（循环引用），如果没有被 GC Root 间接引用到，依然会被回收。Csharp 不像 C++ `shared_ptr` 那样有循环引用问题。

### Unity 中 GC 优化的 8 条铁律
| 优化手段 | 具体做法 |
|---------|---------|
| 对象池 | 复用频繁创建/销毁的对象（子弹、粒子） |
| 缓存组件引用 | Awake/Start 中 GetComponent，避免每帧查找 |
| StringBuilder | 替代 + 拼接字符串 |
| 容器复用 | List/Dictionary 用 Clear() 而非反复 new |
| 避免装箱 | 值类型不要转 object，用泛型替代 |
| CompareTag | 用 `CompareTag()` 替代 `tag == "xxx"`（后者产生 string 临时对象） |
| RaycastNonAlloc | 用 `Physics.RaycastNonAlloc` 替代 `Physics.Raycast` |
| 避免 Update 中 new | foreach 值类型集合也会有 GC 分配 |

### 增量 GC（Incremental GC）
Unity 2019+ 引入，将 GC 工作分散到多帧执行，减少单帧卡顿。但**不减少总 GC 时间**，只分摊。

## 面试官常见追问
- GC 怎么知道一个对象是否存活？（从 GC Root 出发做可达性分析，不是引用计数）
- `GC.Collect()` 什么时候需要手动调用？（场景切换时主动清理，避免下一次自动 GC 时机不合适导致卡顿）
- Unity 的 foreach 为什么有 GC？（遍历值类型集合时，迭代器是值类型但 `IEnumerator` 接口是引用类型，发生了装箱）
- LOH 为什么不分代？（大对象复制代价太大，不参与压缩以提高性能）
- 什么情况下对象不会被 GC？（静态变量持有引用、事件未注销、单例持有已销毁对象引用）

## 我曾经的误区 / 网上常见错答
- **错**："对象的引用计数归零就会被 GC" —— Csharp 是可达性分析，不是引用计数
- **错**："把变量设为 null 就能立即释放" —— null 只是解除引用，GC 时机不由你控制
- **错**："GC.Collect() 可以解决所有内存问题" —— 手动调用会让 Gen 对象晋升代，反而增大下次回收代价
- **错**："struct 不用 GC" —— struct 如果是 class 成员，随 class 被 GC；装箱后的 struct 也会被 GC

## 关联知识点
- [[Csharp 值类型与引用类型]]
- [[Csharp 装箱与拆箱]]
- [[string与StringBuilder]]
- [[对象池]]
- [[Unity 协程原理]]
- [[内存优化与泄露]]

## 原始出处
- GitHub面经_CSharp基础 Q6-Q8
- GitHub面经_性能优化 Q8-Q10
- 博客园 多论坛面经汇总 3.2 节
