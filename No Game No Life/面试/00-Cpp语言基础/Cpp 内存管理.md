---
title: "Cpp 内存管理"
category: Cpp语言基础
tags: [Cpp, 内存管理, 网易互娱, 堆栈, malloc]
frequency: ⭐⭐⭐
difficulty: 困难
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[Cpp 智能指针]]"
  - "[[Cpp 构造函数与析构函数]]"
  - "[[Cpp 编译链接过程]]"
  - "[[内存布局]]"
---

## 一句话结论（自测用）
> C++ 程序内存分五个区：栈（局部变量/自动管理）、堆（new/malloc/手动释放）、全局/静态区、常量区（只读）、代码区。new 会调用构造函数 + 抛异常，malloc 仅分配内存。游戏开发用对象池/内存池减少堆分配碎片。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **五个内存区域**：
   - **栈**：存放局部变量、函数参数、返回地址，编译器自动管理，向低地址生长，速度快但空间有限（通常几 MB）
   - **堆**：new/malloc 分配，手动释放，向高地址生长，空间大但碎片化
   - **全局/静态区**：全局变量、static 变量，程序启动分配、结束时释放
   - **常量区**：字符串常量、const 修饰的全局常量，只读
   - **代码区**：存放程序二进制代码，只读
2. **new/delete vs malloc/free**：
   - new 调用构造函数，delete 调用析构函数；malloc/free 仅分配/释放内存
   - new 返回类型指针，malloc 返回 `void*` 需强转
   - new 失败抛 `std::bad_alloc` 异常，malloc 失败返回 NULL
   - new 是运算符（可重载），malloc 是函数
3. **new[] 必须配 delete[]**：否则只调用一次析构函数，数组剩余元素不会析构。底层数组头部可能存有元素个数信息用于析构。

## 详细解析

### 内存布局图示
```
高地址
+------------------+
|       栈          | ← 局部变量，向下生长
|    (Stack)       |
|       ↓↓         |
+------------------+
|                  |  ← 空闲空间
|       ↑↑         |
|    (Heap)        |
|       堆          | ← 动态分配，向上生长
+------------------+
|   全局/静态区     | ← .bss（未初始化）+ .data（已初始化）
+------------------+
|    常量区         | ← .rodata（只读数据段）
+------------------+
|    代码区         | ← .text（程序指令）
低地址
```

### operator new 重载与内存池
游戏中高频创建/销毁的对象（子弹、粒子），可通过重载 `operator new` + 内存池减少碎片：
```cpp
class Bullet {
public:
    static void* operator new(size_t size) {
        return s_Pool.Allocate(size);  // 从内存池分配
    }
    static void operator delete(void* ptr) {
        s_Pool.Deallocate(ptr);  // 归还内存池
    }
private:
    static ObjectPool s_Pool;
};
```

### 内存对齐
- 访问效率：CPU 按字（word）读取，未对齐数据需两次读取
- `alignof(T)` 查询对齐要求，`alignas(n)` 指定对齐
- 结构体内存对齐规则：成员偏移量是自身大小的整数倍；总大小是最大对齐值的整数倍

## 面试官常见追问
- malloc 的底层怎么分配内存？（brk() 系统调用（小内存）或 mmap()（大内存 > 128KB）；内部用空闲链表管理）
- delete this 可以吗？（语法上可以，但之后对象不再可用，且必须保证是 new 出来的不是栈/全局对象）
- 什么时候用 malloc 而不是 new？（对象池复用：只需分配内存不触发构造；与 C API 交互）
- 怎么检测内存泄漏？（工具：Valgrind/Linux、VLD/Windows、Instruments/Mac；代码：重载 new/delete 记录分配位置）

## 我曾经的误区 / 网上常见错答
- **错**："栈一定比堆快" —— 栈的分配快（移动指针），但访问速度相同；堆慢在分配/释放和碎片管理
- **错**："delete 后指针自动变 NULL" —— 不会，变成悬垂指针（dangling pointer），需手动设为 nullptr
- **错**："同一个指针 delete 两次一定崩溃" —— 未定义行为，可能崩溃也可能不崩溃；delete nullptr 是安全的（空操作）

## 关联知识点
- [[Cpp 智能指针]]
- [[Cpp 构造函数与析构函数]]
- [[Cpp 编译链接过程]]
- [[内存布局]]

## 原始出处
- 史上最全的C++游戏开发面试问题总结（一）——C++基础
- 常见面试题整理——C++（游戏客户端）
- 牛客网 005/008/010 网易互娱/雷火面经
