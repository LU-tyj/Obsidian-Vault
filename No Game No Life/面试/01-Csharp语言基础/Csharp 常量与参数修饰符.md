---
title: "Csharp 常量与参数修饰符"
category: Csharp语言基础
tags: [Csharp, Unity, 网易互娱]
frequency: ⭐
difficulty: 简单
companies: [网易互娱]
status: new
last_reviewed:
next_review:
related:
  - "[[Csharp 值类型与引用类型]]"
---

## 一句话结论（自测用）
> `ref` 传入前须初始化（可读写），`out` 传入前可不初始化（必须赋值）。`const` = 编译时常量（隐式 static），`readonly` = 运行时常量（可在构造函数赋值）。核心区分场景：const 用于永远不会变的值（如 Math.PI），readonly 用于实例化时确定的值。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **ref vs out**：

| | ref | out |
|--|-----|-----|
| 传入前 | 必须初始化 | 可不初始化 |
| 方法内 | 可读可写 | 必须赋值 |
| 使用场景 | 传入并可能修改 | 输出多个返回值 |
| 调用方 | 变量前加 ref | 变量前加 out |

2. **const vs readonly**：

| | const | readonly |
|--|-------|----------|
| 赋值时机 | 声明时 | 声明时或构造函数 |
| 隐式 static | 是 | 否（实例字段需加 static） |
| 编译时 vs 运行时 | 编译时常量 | 运行时常量 |
| 适用范围 | 基本类型 + string + enum + null | 任意类型 |
| 跨程序集引用 | 值被内联到调用方 | 引用（不会内联） |

3. **const 的"内联"陷阱**：
   ```csharp
   // Assembly A
   public const int MaxHealth = 100;
   
   // Assembly B 引用了 A.MaxHealth
   // 如果 A 改成 const int MaxHealth = 200 并重新编译
   // 但 B 没有重新编译，B 中内联的值仍是 100！
   // 解决：用 static readonly 替代 const 做跨程序集常量
   ```

## 详细解析

### out 的实用场景
```csharp
// int.TryParse 的经典 out 用法
if (int.TryParse("123", out int result)) {
    Console.WriteLine(result); // 123
}

// Csharp 7.0+ 内联 out 变量声明
SomeMethod(out var x, out var y);
```

### in 参数修饰符（Csharp 7.2）
```csharp
// in = 只读引用传递，避免大 struct 的拷贝开销
void ProcessLargeStruct(in LargeStruct data) {
    // data 只读，不可修改
}
```
当 struct > 16 字节时，`in` 传递比传值（拷贝）性能好。

### `readonly` 的实际应用
```csharp
public class GameConfig {
    public readonly string PlayerName;           // 实例 readonly：构造时确定
    public static readonly int MaxPlayers = 10;  // 静态 readonly
    public GameConfig(string name) {
        PlayerName = name; // 构造函数中赋值
    }
}
```

## 面试官常见追问
- `const` 和 `static readonly` 性能区别？（const 编译期内联，运行时零开销；static readonly 每次访问读内存，多一次指针解引用）
- out 能用于属性吗？（不能，out 需要变量地址/引用，属性是方法包装的）
- ref 和 out 在 IL 层面的区别？（IL 层面都编译为 `&` 引用传递，区别只在编译期检查规则不同）

## 关联知识点
- [[Csharp 值类型与引用类型]]
- [[struct与class的区别]]

## 原始出处
- GitHub面经_CSharp基础 Q16/Q18
