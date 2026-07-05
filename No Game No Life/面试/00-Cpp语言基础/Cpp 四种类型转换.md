---
title: "Cpp 四种类型转换"
category: Cpp语言基础
tags: [Cpp, 类型转换, cast, 网易互娱]
frequency: ⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[Cpp 虚函数与多态]]"
  - "[[Cpp 指针与引用]]"
---

## 一句话结论（自测用）
> C++ 四种 cast 各有职责：static_cast = 编译期安全转换（基本类型/父转子不安全），dynamic_cast = 运行时多态安全向下转换（失败返回 null），const_cast = 去掉 const/volatile 属性，reinterpret_cast = 暴力位重解释（最危险，慎用）。游戏网络包序列化常用 reinterpret_cast。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **static_cast**：编译期检查的类型转换。用于基本类型转换（`int→float`）、void* 转回原类型、父类指针转子类指针（不安全，不检查）。不检查运行期类型，转换可能出错。
2. **dynamic_cast**：运行期检查的多态类型转换。只用于含虚函数的类层次。将基类指针/引用转为派生类指针/引用，失败时指针返回 nullptr、引用抛 `std::bad_cast`。内部依赖 RTTI（虚表中的 type_info）。
3. **const_cast**：移除或添加 const/volatile 限定符。**不改变底层类型**。去掉 const 后修改原 const 对象是 UB（未定义行为）。唯一合法用途是将 const 指针传给只接受非 const 的旧 C API。
4. **reinterpret_cast**：最低级的转换，重新解释比特位。用于指针和整数互转、不同类型指针互转、函数指针互转。**不保证可移植性**。游戏网络包序列化：`reinterpret_cast<PacketHeader*>(buffer)`。

## 详细解析

### 对比表
| 特性 | static_cast | dynamic_cast | const_cast | reinterpret_cast |
|------|------------|-------------|-----------|-----------------|
| 运行期检查 | 无 | 有（RTTI） | 无 | 无 |
| 失败行为 | 编译OK但不安全 | 返回nullptr/抛异常 | — | 未定义行为 |
| 适用场景 | 基本类型、void* | 多态向下转换 | 去const | 指针/整数互转 |
| 性能 | 最快 | 有开销（查type_info） | 无开销 | 无开销 |
| 安全等级 | 较安全 | 安全 | 危险 | 最危险 |

### C 风格转换 vs C++ cast
```cpp
// C 风格 — 什么都干，不直观
Derived* d = (Derived*)base_ptr;

// C++ cast — 明确意图，便于查找和 code review
Derived* d = dynamic_cast<Derived*>(base_ptr); // 明确是做多态转换
int i = static_cast<int>(3.14);               // 明确是基本类型转换
```

C++ cast 的优势：编译器可以部分检查合理性；grep 可搜索；意图明确。

## 面试官常见追问
- dynamic_cast 的底层实现依赖什么？（RTTI / type_info，通过虚表第一个槽位获取）
- 为什么 dynamic_cast 只能用于有虚函数的类？（无虚函数 = 无虚表 = 无 RTTI 信息，编译报错）
- const_cast 去掉 const 后修改真的安全吗？（用于原对象本身是非 const 的情况安全；原对象是 const 则 UB）
- 为什么游戏开发中慎用 dynamic_cast？（运行时开销，频繁调用会影响性能；更好的做法是虚函数或类型枚举）

## 我曾经的误区 / 网上常见错答
- **错**："static_cast 向下转换是安全的" —— static_cast 不做运行期检查，转错类型可能内存越界
- **错**："const_cast 可以用来改变类型" —— 只能改 const/volatile，不能改变底层类型
- **错**："reinterpret_cast 可以随便用，效率很高" —— 不可移植，不同平台的二进制布局不同

## 关联知识点
- [[Cpp 虚函数与多态]]
- [[Cpp 指针与引用]]

## 原始出处
- 史上最全的C++游戏开发面试问题总结（一）——C++基础
- 【游戏开发面经汇总】- 计算机基础篇
- 牛客网 008 网易互娱游戏研发一面二面
