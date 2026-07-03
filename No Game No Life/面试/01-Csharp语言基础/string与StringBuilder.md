---
title: "string与StringBuilder"
category: Csharp语言基础
tags: [Csharp, Unity, 网易互娱, 字符串, GC]
frequency: ⭐⭐
difficulty: 简单
companies: [网易互娱]
status: new
last_reviewed:
next_review:
related:
  - "[[Csharp GC 垃圾回收]]"
  - "[[Csharp 值类型与引用类型]]"
---

## 一句话结论（自测用）
> string 是不可变的（immutable），每次修改都创建新对象（GC 压力）。StringBuilder 内部是可变字符数组，频繁修改场景使用。同一个内容的字符串值只存一份（字符串驻留）。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **string 的特性**：
   - **不可变性**：一旦创建，内容不可修改。`s += "a"` 实际上是创建了一个新的 string 对象。
   - **字符串驻留（String Interning）**：编译时常量字符串只存一份在驻留池中，相同内容指向同一内存地址。
   - **引用类型但行为像值类型**：`==` 被重载为内容比较（而非引用比较）。
2. **StringBuilder 的特性**：
   - 内部维护一个可变的 `char[]` 数组，支持原地修改。
   - 扩容机制：容量不足时扩容为当前容量的 2 倍。
   - 支持链式调用：`sb.Append("a").Append("b").Append("c")`
3. **使用场景判断**：
   - **用 string**：少量拼接（< 5 次）、字符串内容不变化、需要比较/Hash
   - **用 StringBuilder**：循环中拼接、大量字符串操作、Update 中的字符串处理
4. **Unity 特别提醒**：`tag == "xxx"` 会产生 string 临时对象，用 `CompareTag("xxx")` 替代。

## 详细解析

### 字符串驻留的内部机制
```csharp
string a = "hello";
string b = "hello";
// a 和 b 指向堆上同一个 "hello" 对象
Console.WriteLine(object.ReferenceEquals(a, b)); // True（编译时常量）

string c = new StringBuilder().Append("hel").Append("lo").ToString();
Console.WriteLine(object.ReferenceEquals(a, c)); // False（运行时创建，未驻留）
// 手动驻留：string.Intern(c)
```

### GC 视角的性能对比
```csharp
// 差：循环中产生 100 个临时 string 对象
string result = "";
for (int i = 0; i < 100; i++) {
    result += i.ToString(); // 每次都是新 string！
}

// 好：只产生 1 个 string 对象
var sb = new StringBuilder();
for (int i = 0; i < 100; i++) {
    sb.Append(i);
}
string result = sb.ToString();
```

### Unity 的字符串 GC 陷阱
1. `Debug.Log(gameObject.name + " is active")` -- 拼接产生临时 string
2. `tag == "Player"` -- 用 `CompareTag("Player")` 代替
3. `gameObject.name` 的 setter 会产生 GC（因为内部 name 的 set 是 native 调用）
4. `transform.Find("ChildName")` -- 字符串参数，考虑缓存 Transform 引用

## 面试官常见追问
- `StringBuilder` 的默认容量是多少？（16个字符）
- string 的 `==` 比较的是引用还是值？（值比较，Csharp 重载了 string 的 `==`）
- `string.Empty` 和 `""` 的区别？（没有区别，指向同一个驻留的空字符串对象）
- 为什么不把所有 string 都换成 StringBuilder？（StringBuilder 本身也有开销，小量拼接不值得；StringBuilder 不能直接传给需要 string 的 API）

## 我曾经的误区 / 网上常见错答
- **错**："string 是值类型" —— string 是引用类型，只是不可变性 + `==` 重载让它看起来像值类型
- **错**："StringBuilder 总是比 string 快" —— 少量拼接（< 3-5 次）时，string 的内联优化可能更快，StringBuilder 本身有创建开销
- **错**："字符串驻留让所有相同内容的字符串都是同一个对象" —— 只有编译时常量和手动 `string.Intern()` 才会驻留

## 关联知识点
- [[Csharp GC 垃圾回收]]
- [[Csharp 值类型与引用类型]]

## 原始出处
- GitHub面经_CSharp基础 Q20
- 博客园 梦幻事业部外包面经 Q6
