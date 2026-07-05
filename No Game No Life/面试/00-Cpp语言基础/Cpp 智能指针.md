---
title: "Cpp 智能指针"
category: Cpp语言基础
tags: [Cpp, 智能指针, 网易互娱, 内存管理, RAII]
frequency: ⭐⭐⭐
difficulty: 困难
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[Cpp 内存管理]]"
  - "[[Cpp 虚函数与多态]]"
  - "[[Cpp 右值引用与移动语义]]"
---

## 一句话结论（自测用）
> shared_ptr 用引用计数 + 控制块管理堆对象，unique_ptr 独占所有权（不可拷贝只可移动），weak_ptr 不增加引用计数用于打破循环引用。游戏开发中 unique_ptr 管理临时资源，weak_ptr 观察可能被销毁的对象。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **unique_ptr**：独占所有权，不可拷贝（拷贝构造/赋值 = delete），可移动。无引用计数开销，比 shared_ptr 更轻量。适用场景：生命周期明确的对象（如帧内粒子）。
2. **shared_ptr**：共享所有权，底层是**引用计数 + 控制块**。控制块存储引用计数、弱计数、删除器、分配器。引用计数的增减是原子操作（线程安全），但对象本身线程不安全。
3. **weak_ptr**：不增加引用计数，通过 `lock()` 返回 shared_ptr（若对象已释放则返回空）。专门用于打破 shared_ptr 的循环引用。
4. **make_shared vs new**：`make_shared<T>(args)` 一次性分配对象 + 控制块（减少内存碎片），且异常安全。`new T` 后构造 shared_ptr 会分配两次内存。

## 详细解析

### shared_ptr 控制块结构
```
shared_ptr<T>
+------------------+
| T* ptr           | → 指向堆上的对象
| control_block*   | → 指向控制块
+------------------+

控制块（Control Block）：
+------------------+
| 强引用计数 (use_count) |
| 弱引用计数 (weak_count) |
| 删除器 (deleter)       |
| 分配器 (allocator)     |
+------------------+
```

### 循环引用问题（经典面试题）
```cpp
class B;
class A {
    shared_ptr<B> b_ptr;  // A 持有 B
};
class B {
    shared_ptr<A> a_ptr;  // B 持有 A，形成循环
};
// 解决：将其中一个改为 weak_ptr
class B {
    weak_ptr<A> a_ptr;  // 打破循环
};
```

### shared_ptr 线程安全
- **引用计数操作**：原子操作，线程安全。
- **对象本身访问**：不是线程安全的，需外部同步。
- **赋值/重置操作**：不是线程安全的，多个线程同时修改同一个 shared_ptr 需要加锁。

### enable_shared_from_this
当需要在类内部获取自身的 shared_ptr 时，继承 `enable_shared_from_this<T>`，调用 `shared_from_this()`。原理是控制块中存储了指向对象的指针。

## 面试官常见追问
- shared_ptr 是线程安全的吗？（引用计数安全，对象本身不安全）
- make_shared 有什么缺点？（内存延迟释放：直到所有 weak_ptr 也释放才回收；自定义删除器时不能用）
- weak_ptr 的 lock() 是怎么实现的？（检查引用计数 > 0，是的话返回 shared_ptr，否则返回空）
- 游戏中哪些场景用哪种智能指针？（unique_ptr：临时资源；weak_ptr：观察已销毁对象；shared_ptr：需要共享所有权的资源但要注意循环引用）

## 我曾经的误区 / 网上常见错答
- **错**："shared_ptr 完全线程安全" —— 只有引用计数是原子操作，对象需要额外保护
- **错**："weak_ptr 可以像 shared_ptr 一样直接访问对象" —— 必须先 lock() 获取 shared_ptr
- **错**："把裸指针赋给两个 shared_ptr 没关系" —— 会创建两个独立控制块，导致 double free

## 关联知识点
- [[Cpp 内存管理]]
- [[Cpp 右值引用与移动语义]]
- [[Cpp 多线程基础]]

## 原始出处
- 史上最全的C++游戏开发面试问题总结（一）——C++基础
- 常见面试题整理——C++（游戏客户端）
- 【游戏开发面经汇总】-社招初级篇 2.1 智能指针章节
- 牛客网 006/009/011 网易互娱/雷火面经
