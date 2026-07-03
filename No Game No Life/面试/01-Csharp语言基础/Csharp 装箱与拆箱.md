---
title: "Csharp 装箱与拆箱"
category: Csharp语言基础
tags: [Csharp, Unity, 网易互娱, GC, 性能优化]
frequency: ⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[Csharp 值类型与引用类型]]"
  - "[[Csharp GC 垃圾回收]]"
  - "[[struct与class的区别]]"
---

## 一句话结论（自测用）
> 装箱 = 值类型转 object（堆上分配新对象，复制数据）。拆箱 = object 转回值类型（类型检查 + 复制回栈）。避免方法：使用泛型、避免值类型做接口参数、重写 ToString() 避免字符串拼接装箱。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **装箱（Boxing）**：
   - 在堆上分配一个对象（含类型信息 + 同步块索引）
   - 将值类型的数据复制到该对象中
   - 返回该对象的引用
   - 产生 GC 压力
2. **拆箱（Unboxing）**：
   - 检查 object 引用是否为 null
   - 检查 object 中的类型是否与目标类型一致（不一致抛 `InvalidCastException`）
   - 将数据从堆复制回栈上的值类型变量
   - 拆箱本身不分配堆内存，但检查有 CPU 开销
3. **哪一步开销大？** 装箱开销大（堆分配 + GC），拆箱较小但类型检查有风险。
4. **避免方法**：
   - 使用泛型代替 `ArrayList` / 非泛型集合
   - 值类型重写 `ToString()`、`GetHashCode()`、`Equals()` 避免调用 `object` 基类方法
   - 避免值类型转为接口类型（会装箱）
   - `string.Format` / `Console.WriteLine` 时值类型先用 `.ToString()` 转 string

## 详细解析

### 哪些操作会隐性装箱？
```csharp
int x = 42;
object obj = x;                          // 显式装箱
string s = "value: " + x;                // 字符串拼接，x 先装箱再调 ToString()
Console.WriteLine("{0}", x);             // 格式化输出装箱
IComparable c = x;                        // 值类型转接口 -- 装箱！
ArrayList list = new ArrayList();        // 非泛型集合
list.Add(x);                              // 装箱！
var enumerator = list.GetEnumerator();   // 值类型迭代器转接口 -- 装箱！（foreach 的隐藏装箱）
```

### foreach 对 List\<T\> 的装箱陷阱
```csharp
List<int> list = new List<int> { 1, 2, 3 };
// List<T>.GetEnumerator() 返回值类型 Enumerator
// foreach 调用 GetEnumerator() 返回值类型，不装箱 -- 安全
foreach (int x in list) { } // 无装箱

// 但如果：
IList<int> iList = list;
foreach (int x in iList) { } // IList<T> 返回 IEnumerator<T> 接口 -- 装箱！
```

### Unity 中常见的装箱来源
1. `tag == "xxx"` -- 每次产生 string 比较（string 是引用类型但 tag getter 有某种开销）；用 `CompareTag()` 替代
2. `yield return 0` -- 0 是 int 值类型，yield return 期望 object，发生装箱；用 `yield return null` 替代
3. 协程 `StartCoroutine("MethodName")` -- 字符串参数分配

## 面试官常见追问
- 拆箱时类型不匹配会怎样？（`InvalidCastException`）
- `int?` (Nullable\<int\>) 的装箱行为？（非 null 时装箱为 int；null 时装箱为 null 引用）
- `(int)obj` 和 `obj as int?` 的区别？（前者可能拆箱失败抛异常，后者是安全转换）

## 我曾经的误区 / 网上常见错答
- **错**："装箱就是把值类型放到堆上" —— 还要加上类型信息指针和同步块索引，比单纯的数据复制多 16 字节（64位）
- **错**："拆箱就是把数据从堆复制回栈" —— 还有类型检查步骤
- **错**："泛型完全消除了装箱" —— 泛型消除了大部分，但值类型转 `object` / 接口时仍然装箱

## 关联知识点
- [[Csharp 值类型与引用类型]]
- [[Csharp GC 垃圾回收]]
- [[struct与class的区别]]
- [[List 底层原理与泛型集合]]

## 原始出处
- GitHub面经_CSharp基础 Q3
- 博客园 多论坛面经汇总 3.2 节
