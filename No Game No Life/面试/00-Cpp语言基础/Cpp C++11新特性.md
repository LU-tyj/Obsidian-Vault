---
title: "Cpp C++11新特性"
category: Cpp语言基础
tags: [Cpp, C++11, 现代Cpp, 网易互娱]
frequency: ⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[Cpp 右值引用与移动语义]]"
  - "[[Cpp 智能指针]]"
  - "[[Cpp 模板与泛型编程]]"
---

## 一句话结论（自测用）
> C++11 六大核心特性：auto 自动类型推导、nullptr 替代 NULL、智能指针（unique_ptr/shared_ptr/weak_ptr）、右值引用 + 移动语义、lambda 匿名函数、constexpr 编译期计算。这六个是所有面试的必问项。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **auto**：编译器根据初始化表达式自动推导变量类型。但不能用于函数参数、非静态成员变量。配合 range-for 遍历容器非常简洁：`for (auto& item : vec)`。
2. **nullptr**：类型是 `std::nullptr_t`，可隐式转换为任意指针类型。解决旧 `NULL`（本质是 #define NULL 0）导致的函数重载匹配歧义。
3. **智能指针**：`unique_ptr`（独占）、`shared_ptr`（共享+引用计数）、`weak_ptr`（观察，破循环引用）。替代裸指针，RAII 自动管理。
4. **右值引用与移动语义**：`T&&` 绑定右值，实现资源"窃取"而非"拷贝"。`std::move` 左值转右值，`std::forward` 完美转发。
5. **lambda 表达式**：`[capture](params) -> ret { body }`。捕获列表可指定值捕获 `[=]`、引用捕获 `[&]`、mutable 等。
6. **constexpr**：编译期常量/函数，确保在编译期完成计算，减少运行期开销。C++14/17 进一步放宽限制。

## 详细解析

### 其他重要 C++11 特性
- **列表初始化**：`vector<int> v = {1, 2, 3};` 统一初始化语法，防止窄化转换
- **范围 for**：`for (auto& x : container)` 语法糖
- **= default / = delete**：显式声明使用/禁用编译器默认生成的函数
- **override / final**：override 确保重写基类虚函数（编译期检查），final 禁止继承/重写
- **线程库**：`std::thread`、`std::mutex`、`std::atomic`、`std::lock_guard` / `std::unique_lock`
- **unordered 容器**：`unordered_map`、`unordered_set` 基于哈希表

### lambda 表达式详解
```cpp
// [捕获列表](参数列表) -> 返回类型 { 函数体 }
auto add = [](int a, int b) -> int { return a + b; };

int x = 10;
auto copy_x = [x]() { return x; };        // 值捕获，只读
auto ref_x  = [&x]() { x++; };           // 引用捕获，可修改
auto mixed  = [=, &x]() { /* x引用，其他值 */ };
auto mutable_lambda = [x]() mutable { x++; return x; }; // mutable 允许修改值捕获的副本
```

### nullptr 为什么比 NULL 好
```cpp
void func(int);
void func(char*);
func(NULL);   // 调用 func(int)，不是期望的 func(char*)
func(nullptr); // 调用 func(char*)，正确！
```
因为 `NULL` 本质是 `0`（整数），`nullptr` 是真正的空指针类型。

## 面试官常见追问
- lambda 的底层实现是什么？（编译器生成一个匿名仿函数类，捕获的变量变成类的成员）
- auto 不能用在哪些地方？（函数参数、非静态成员变量、模板实参（C++17 前））
- constexpr 和 const 的区别？（constexpr 强制编译期求值；const 可以是运行期确定后不可变）
- C++14/17 有什么重要的新特性？（C++14：泛型 lambda、`make_unique`；C++17：`std::optional`、`std::variant`、结构化绑定、if constexpr）

## 我曾经的误区 / 网上常见错答
- **错**："auto 会降低性能" —— auto 只是编译期类型推导，生成的代码和手写类型完全一样（零运行时开销）
- **错**："lambda 只能用在 STL 算法中" —— lambda 是通用的匿名函数对象，可用于回调、线程、条件变量等任何需要函数对象的场景
- **错**："nullptr 就是 0" —— nullptr 类型是 `std::nullptr_t`，有类型安全的隐式转换

## 关联知识点
- [[Cpp 右值引用与移动语义]]
- [[Cpp 智能指针]]
- [[Cpp 模板与泛型编程]]

## 原始出处
- 史上最全的C++游戏开发面试问题总结（一）——C++基础
- 常见面试题整理——C++（游戏客户端）
- 【游戏开发面经汇总】- 计算机基础篇
