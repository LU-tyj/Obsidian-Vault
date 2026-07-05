---
title: "Cpp const与static"
category: Cpp语言基础
tags: [Cpp, const, static, 网易互娱, 关键字]
frequency: ⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[Cpp 内存管理]]"
  - "[[Cpp 指针与引用]]"
  - "[[Cpp 编译链接过程]]"
---

## 一句话结论（自测用）
> const 是编译期约束，防止误修改（"我承诺不修改"）；static 控制存储期和可见性（全局 static = 文件内可见，局部 static = 只初始化一次，类 static = 所有对象共享）。const 修饰的成员函数不能修改成员变量（本质是修饰 this 指针）。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **const 的四种用法**：
   - **const 变量**：声明不可修改的常量，编译器会做类型检查（优于 `#define`）
   - **const 指针**：`const int* p`（指向常量的指针）vs `int* const p`（指针本身是常量）
   - **const 函数参数**：`void func(const T& obj)` — 避免拷贝 + 保证不修改
   - **const 成员函数**：`int getValue() const` — 不能修改成员变量，只能调用其他 const 成员函数。本质是 `const T* this`
2. **static 的四种作用**：
   - **static 全局变量**：限制在本文件（内部链接），避免命名冲突
   - **static 局部变量**：程序生命周期内只初始化一次，函数调用间保持值。线程安全的初始化（C++11 保证）
   - **static 成员变量**：类级别共享，属于类而非对象。需类外定义
   - **static 成员函数**：可通过 `类名::函数()` 调用，无 this 指针，只能访问 static 成员
3. **const 与宏的区别**：const 有类型检查、作用域、调试可见；宏只是预处理器文本替换。

## 详细解析

### const 的实现原理
const 本质是**编译期检查**，不做运行时保护。编译器会对声明为 const 的变量做常量折叠，并在赋值时检查。不合理使用 `const_cast` 去掉 const 后修改，如果是位于只读数据段（.rodata）的常量会引发段错误。

### mutable 关键字
`mutable` 修饰的成员变量，即使在 const 成员函数中也可以修改。典型用途：缓存计算结果（如 mutable 的 hash 值）。

### const 成员函数的重载
可以基于 const 重载——const 对象调用 const 版本，非 const 对象调用非 const 版本：
```cpp
int& at(int idx);           // 非 const 版本
const int& at(int idx) const; // const 版本
```

### static 存储位置
- static 变量存储在全局/静态区（.data 或 .bss）
- 在 main() 之前初始化、main() 之后销毁
- 不同编译单元的 static 初始化顺序不确定（Static Initialization Order Fiasco）

## 面试官常见追问
- const 真的能防止被修改吗？（编译期可以，运行时不能——`const_cast` + `mutable` + 通过指针间接修改）
- static 局部变量的初始化是线程安全的吗？（C++11 起保证：多线程同时首次调用，只有一个线程执行初始化）
- 为什么 static 成员函数不能访问非 static 成员？（没有 this 指针，不知道操作哪个对象的数据）
- constexpr 和 const 的区别？（constexpr 强制编译期求值，const 可能是运行期初始化后不可变）

## 我曾经的误区 / 网上常见错答
- **错**："const 变量一定在常量区" —— 只有编译期确定的值才可能在常量区；const 局部变量仍在栈上
- **错**："static 变量一定比堆变量更持久" —— static 生命周期是程序级别，但可见性受限
- **错**："const 成员函数绝对不能修改任何成员" —— mutable 成员可以被 const 函数修改

## 关联知识点
- [[Cpp 内存管理]]
- [[Cpp 指针与引用]]
- [[Cpp 编译链接过程]]

## 原始出处
- 史上最全的C++游戏开发面试问题总结（一）——C++基础
- 【游戏开发面经汇总】- 计算机基础篇
- 牛客网 008/009/010 网易互娱面经
