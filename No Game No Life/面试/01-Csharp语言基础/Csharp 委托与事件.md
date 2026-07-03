---
title: "Csharp 委托与事件"
category: Csharp语言基础
tags: [Csharp, Unity, 网易互娱, 委托, 事件, 观察者模式]
frequency: ⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[Unity 生命周期]]"
  - "[[Csharp GC 垃圾回收]]"
---

## 一句话结论（自测用）
> 委托 = 类型安全的函数指针，用来封装方法引用。事件 = 委托的包装器，限制外部只能 `+=`/`-=` 不能直接 `=` 赋值或外部调用。Action(无返回值)、Func(有返回值)、Predicate(返回bool) 是内置泛型委托。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **委托（Delegate）的本质**：
   - 一个类（`System.Delegate` 的子类），可以封装一个或多个方法引用（多播委托）
   - 类型安全的函数指针：编译时检查方法签名是否匹配
   - 声明：`delegate void MyDelegate(int x);`
2. **事件（Event）的本质**：
   - 委托类型的**实例**加上 `event` 关键字修饰
   - 编译器将 `event` 编译为私有委托字段 + 公开的 `add`/`remove` 访问器（类似属性）
   - 核心限制：外部只能用 `+=`/`-=`，不能 `=` 赋值，不能外部调用 `Invoke()`
3. **委托 vs 事件对比表**：

| | 委托 | 事件 |
|--|------|------|
| 本质 | 类型（类） | 委托类型的成员 |
| 外部赋值 | `=` 直接覆盖 | 不允许（只允许 +=/-=） |
| 外部调用 | 可以 | 不允许（只能在定义类内部 Invoke） |
| 用途 | 封装方法引用 | 发布-订阅模式，限制外部触发 |

4. **内置泛型委托**：
   - `Action`：无返回值（0-16 参数）
   - `Func<TResult>`：有返回值（0-16 参数 + 1 返回类型）
   - `Predicate<T>`：返回 bool（等价 `Func<T, bool>`）

## 详细解析

### 事件防止内存泄漏
事件最常见的 Bug：订阅者对象已销毁，但发布者仍持有委托引用，导致订阅者无法被 GC。
```csharp
// OnEnable 注册，OnDisable 注销 -- Unity 标准实践
void OnEnable() => EventManager.OnGameStart += HandleGameStart;
void OnDisable() => EventManager.OnGameStart -= HandleGameStart;
```

### 多播委托的调用链
```csharp
Action action = MethodA;
action += MethodB;
action += MethodC;
action(); // 依次调用 A -> B -> C，如果 B 抛异常则 C 不执行
// 解决方案：GetInvocationList() 逐个 try-catch 调用
```

### 事件为什么设计为"不可外部赋值"？
核心动机：防止外部代码用 `=` 将你的事件覆盖掉（清空所有订阅者），这是最常见的委托 bug。事件语法糖强制使用 `+=`/`-=`。

### UnityEvent vs Csharp Event
| | UnityEvent | Csharp event |
|--|-----------|----------|
| 序列化 | Inspector 可见，可序列化 | 不可序列化 |
| 性能 | 较慢（通过反射调用） | 快（直接调用） |
| 动态添加监听 | 支持 Inspector 拖拽 | 仅代码 |
| 使用场景 | Editor 配置 | 纯代码逻辑 |

## 面试官常见追问
- 委托可以指向多个方法吗？如何获取所有方法？（多播委托，`GetInvocationList()`）
- 事件和委托的底层有什么关系？（事件编译为私有委托字段 + add/remove 访问器）
- 匿名方法和 Lambda 是委托吗？（Lambda 表达式可以转换为委托类型或表达式树）
- 委托的 `BeginInvoke` / `EndInvoke` 是什么？（旧版异步调用模式，已不推荐，用 async/await 替代）

## 我曾经的误区 / 网上常见错答
- **错**："事件是一种特殊的委托" —— 事件是委托的实例加上封装，不是新的类型
- **错**："Action 和 Func 是关键字" —— 是 `System` 命名空间的泛型委托类型，不是 Csharp 关键字
- **错**："Lambda 和委托是一回事" —— Lambda 是语法，可以编译为委托（delegate）或表达式树（Expression）
- **错**："事件注册后不注销也没关系" —— 这是内存泄漏的常见原因

## 关联知识点
- [[Unity 生命周期]]
- [[Csharp GC 垃圾回收]]
- [[内存优化与泄露]]

## 原始出处
- GitHub面经_CSharp基础 Q4-Q5
- 牛客网 002_雷火实习 Q13
- 博客园 多论坛面经汇总 3.2 节
