---
title: struct与class的区别
category: Csharp语言基础
tags:
  - Csharp
  - Unity
  - 网易互娱
  - 值类型
  - 引用类型
frequency: ⭐⭐
difficulty: 中等
companies:
  - 网易互娱
  - 网易雷火
status: new
last_reviewed:
next_review:
related:
  - "[[Csharp 值类型与引用类型]]"
  - "[[Csharp 装箱与拆箱]]"
---

## 一句话结论（自测用）
> struct 是值类型（栈上分配，赋值即拷贝），class 是引用类型（堆上分配，赋值共享引用）。struct 不能继承（可做接口），适合小数据高频场景（如 Vector3）；class 支持继承和多态，适合复杂对象。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **本质区别**：struct 是值类型，class 是引用类型。这决定了存储位置、赋值行为、GC 影响等一切差异。
2. **继承**：struct 不能继承（隐式 sealed），但可以实现接口；class 可以单继承 + 多接口。
3. **构造函数**：struct 不能有无参构造函数（Csharp 10.0 前可有了），但必有隐式无参构造（所有字段设默认值）；class 可以有任意构造函数。
4. **默认值**：struct 不能为 null（除非 `Nullable<T>`）；class 默认为 null。
5. **性能**：struct 在栈上分配，无 GC 压力，适合小数据高频创建（如 Vector3、RaycastHit）；class 在堆上分配，由 GC 管理。
6. **使用场景**：
   - struct：数据量小（< 16 字节）、生命周期短、强调值语义、高频创建销毁
   - class：数据量大、需要继承多态、长生命周期、需要引用共享

## 详细解析

### struct 何时不建议使用
1. 数据 > 16 字节（栈复制开销超过堆分配）
2. 需要频繁装箱（会抵消性能优势）
3. 逻辑复杂、方法多（每次传参都是拷贝，开销大）
4. 需要可变性（mutable struct 是常见的 bug 来源）

### mutable struct 的经典 Bug
```csharp
struct MyStruct { public int Value; }
MyStruct s = new MyStruct();
list[0].Value = 10; // 编译错误！list[0] 返回的是拷贝
// 正确做法：var temp = list[0]; temp.Value = 10; list[0] = temp;
```
这是网易面试的高频陷阱题。

### Unity 中的 struct 典范
- `Vector3`, `Vector2`, `Quaternion`, `Color`, `Ray`, `RaycastHit`
- Unity 选 struct 的原因：游戏每帧创建大量这些值，如果用 class 会持续触发 GC

## 面试官常见追问
- struct 可以实现接口吗？实现后有什么风险？（可以，但通过接口调用时会装箱，失去性能优势）
- `new struct()` 和 `default(struct)` 区别？（Csharp 10.0 前等价，之后 `new struct()` 可调用无参构造）
- Unity 的 Vector3 为什么是 struct？（游戏每帧计算大量 Vector3 运算，class 会导致帧帧 GC）
- Csharp 的 record struct 是什么？（Csharp 10.0，值类型的 record，支持 `with` 表达式但保持值语义）

## 我曾经的误区 / 网上常见错答
- **错**："struct 轻量，优先用 struct" —— 大 struct 频繁拷贝的开销可通过 class
- **错**："struct 不能有方法" —— struct 可以有方法、属性、索引器、运算符重载
- **错**："struct 是 immutable 的" —— Csharp 的 struct 是可变的（除非设计为 readonly struct）

## 关联知识点
- [[Csharp 值类型与引用类型]]
- [[Csharp 装箱与拆箱]]
- [[Csharp GC 垃圾回收]]

## 原始出处
- GitHub面经_CSharp基础 Q2
- 博客园 多论坛面经汇总 3.2 节
