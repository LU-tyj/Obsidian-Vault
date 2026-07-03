---
title: "Csharp 反射"
category: Csharp语言基础
tags: [Csharp, Unity, 网易互娱, 反射, 元数据]
frequency: ⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[Csharp 委托与事件]]"
  - "[[Interface与AbstractClass]]"
---

## 一句话结论（自测用）
> 反射 = 运行时动态获取类型元数据（字段/方法/属性等）。核心类：`Type`、`Assembly`、`MethodInfo`。Unity 中用于编辑器扩展、序列化、特性处理。缺点：性能差、无法 AOT 裁剪。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **什么是反射**：运行时动态获取程序集中类型的信息（元数据），并可以动态创建实例、调用方法、访问字段。
2. **核心类（System.Reflection）**：
   - `Assembly`：描述程序集，通过 `Assembly.Load()` 或 `typeof(T).Assembly` 获取
   - `Type`：描述类/结构/枚举等类型，通过 `typeof()` 或 `obj.GetType()` 获取
   - `MethodInfo`：描述方法，`type.GetMethod("MethodName")`
   - `FieldInfo`：描述字段，`type.GetField("fieldName", BindingFlags)`
   - `PropertyInfo`：描述属性，`type.GetProperty("propName")`
3. **使用场景**：
   - **编辑器扩展**：Inspector 面板动态显示字段（Unity 内置就是反射驱动的）
   - **序列化/反序列化**：JsonUtility、OdinSerializer 等
   - **依赖注入**：Zenject / VContainer 框架通过反射扫描需要注入的类型
   - **特性（Attribute）处理**：通过反射读取类/方法上的特性标记
   - **动态调用**：通过方法名字符串调用方法
4. **性能开销**：反射比直接调用慢 10-100 倍，高频调用需要缓存 `MethodInfo` / `FieldInfo`，或用 `Expression Tree` + `Delegate.CreateDelegate` 优化。

## 详细解析

### typeof() vs GetType() vs is vs as
| 操作 | 时机 | 作用 | 示例 |
|------|------|------|------|
| `typeof(T)` | 编译时 | 获取已知类型的 Type | `typeof(int)` |
| `obj.GetType()` | 运行时 | 获取实例的实际类型 | `3.GetType()` -> Int32 |
| `is` | 运行时 | 类型兼容检查，返回 bool | `obj is string` |
| `as` | 运行时 | 安全转换，失败返回 null | `obj as string` |

### 反射 + 委托优化（高频追问）
```csharp
// 慢：每次调用都反射
MethodInfo method = typeof(MyClass).GetMethod("DoSomething");
method.Invoke(instance, null);

// 快：反射一次，缓存为委托
var action = (Action)Delegate.CreateDelegate(typeof(Action), instance, method);
action(); // 接近直接调用速度
```

### Unity 中反射的 IL2CPP 问题
IL2CPP 是 AOT 编译，会裁剪掉"没用到的代码"。反射调用可能因为代码被裁剪而失败。解决：
- 在 `link.xml` 中保留类型
- 使用 `[Preserve]` 特性
- 避免反射调用被裁剪的类型

## 面试官常见追问
- 反射很慢，慢在哪？（元数据查找、安全检查、参数装箱拆箱、Invoke 的参数数组分配）
- 如何用反射创建泛型实例？（`typeof(List<>).MakeGenericType(typeof(int))`）
- `BindingFlags` 的作用？（控制访问级别搜索：Public/NonPublic/Instance/Static 等组合）
- 反射能访问 private 成员吗？（能！需要 `BindingFlags.NonPublic | BindingFlags.Instance`）

## 我曾经的误区 / 网上常见错答
- **错**："Unity 游戏运行时应该多用反射" —— 游戏运行时尽量不用反射，编辑器工具可以用
- **错**："`typeof()` 和 `GetType()` 差不多" —— typeof 编译时确定，GetType 运行时确定，性能差距大
- **错**："AOT 环境下反射都不能用" —— 可以用，但需要保留被反射的类型不被裁剪

## 关联知识点
- [[Csharp 委托与事件]]
- [[Interface与AbstractClass]]
- [[IL2CPP与Mono]]

## 原始出处
- GitHub面经_CSharp基础 Q12-Q13
- 博客园 多论坛面经汇总 3.2 节
