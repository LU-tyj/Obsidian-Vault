---
title: Csharp 值类型与引用类型
category: Csharp语言基础
tags:
  - Csharp
  - Unity
  - 网易互娱
  - 内存管理
frequency: ⭐⭐⭐
difficulty: 中等
companies:
  - 网易互娱
  - 网易雷火
status: new
last_reviewed:
next_review:
related:
  - "[[Csharp 装箱与拆箱]]"
  - "[[struct与class的区别]]"
  - "[[Csharp GC 垃圾回收]]"
---

## 一句话结论（自测用）
> 值类型存栈（数据本体），引用类型存堆（栈上只存地址）。赋值时值类型复制数据，引用类型复制地址。struct 是值类型，class 是引用类型。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **存储位置**：值类型分配在栈上（跟随所在上下文，如在 class 内部则随 class 在堆上）；引用类型的对象分配在堆上，栈上只保存指向堆的引用地址。
2. **赋值行为**：值类型赋值发生值拷贝，两个变量独立；引用类型赋值只复制引用地址，两个变量指向同一对象。
3. **默认值**：值类型有默认值（如 int 默认 0），不可为 null；引用类型默认为 null。
4. **继承链**：值类型继承自 `System.ValueType`（而 `System.ValueType` 又继承 `System.Object`）；引用类型直接继承 `System.Object`。
5. **GC 影响**：值类型出作用域自动释放（不产生 GC 压力）；引用类型由 GC 负责回收。
6. **典型代表**：值类型 = int / float / bool / char / struct / enum；引用类型 = string / object / class / interface / delegate / array。

## 详细解析

### struct 中嵌套引用类型，class 中嵌套值类型
这个追问非常高频：
- struct 内部声明的 `string` 成员，字符串数据仍在**堆**上，struct 本身只存 8 字节引用指针。
- class 内部声明的 `int` 成员，数据随 class 实例在**堆**上分配。

结论：**值类型/引用类型决定的是它自身的分配形态，而不是它成员的分配形态。**

### struct 为什么不能有无参构造函数（Csharp 10.0 之前）
因为 struct 是值类型，CLR 要求值类型的默认初始化必须是"全零内存"。如果允许自定义无参构造，每次 `new struct()` 和 `default(struct)` 的行为就会不一致。Csharp 10.0 放宽了此限制。

### "struct 一定在栈上"是对的吗？
**不完全对。** struct 作为局部变量确实在栈上，但：
- struct 是 class 的成员时，随 class 在堆上
- 装箱后的 struct 在堆上
- lambda/闭包捕获的 struct 在堆上
- 静态 struct 字段在堆上（High Frequency Heap）

## 面试官常见追问
- struct 里面可以放 class 成员吗？内存怎么分布？（可以，string 字段存的是堆引用指针）
- struct 能做接口吗？（可以做接口实现，但装箱时会丢失性能优势）
- `int` 和 `System.Int32` 是什么关系？（int 是 Int32 的 Csharp 别名，都是值类型）
- 什么场景用 struct？（小数据量、高频创建销毁、强调数据独立性，如 Vector3）

## 我曾经的误区 / 网上常见错答
- **错**："值类型一定在栈，引用类型一定在堆" —— struct 作为 class 成员时在堆上
- **错**："struct 不能有方法" —— struct 可以有方法、属性、索引器，只是不能继承
- **错**："string 是值类型" —— string 是引用类型，但有不可变性（immutable）使其行为看似像值类型

## 关联知识点
- [[Csharp 装箱与拆箱]]
- [[struct与class的区别]]
- [[Csharp GC 垃圾回收]]
- [[Csharp 常量与参数修饰符]]

## 原始出处
- GitHub面经_CSharp基础 Q1-Q2
- 牛客网 005_雷火一面 Q5
- 博客园 多论坛面经汇总 3.2 节
