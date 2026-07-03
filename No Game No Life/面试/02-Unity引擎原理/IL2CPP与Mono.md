---
title: "IL2CPP与Mono"
category: Unity引擎原理
tags: [Unity, Csharp, 网易互娱, IL2CPP, Mono, 编译]
frequency: ⭐
difficulty: 中等
companies: [网易互娱]
status: new
last_reviewed:
next_review:
related:
  - "[[Csharp 反射]]"
  - "[[热更新方案对比]]"
---

## 一句话结论（自测用）
> Mono = JIT 编译（运行时编译 IL 为机器码，支持动态代码生成），IL2CPP = AOT 编译（提前将 IL 转 C++ 再编译为机器码）。iOS 强制 IL2CPP（禁止 JIT），性能约 1.5x Mono。代价：不支持 `System.Reflection.Emit`、编译时间长、包体增大。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **Mono 的特点**：
   - JIT（Just-In-Time）编译：运行时将 Csharp IL 编译为机器码
   - 支持动态代码生成（`System.Reflection.Emit`）
   - 启动快（不需要提前编译）
   - 缺点：运行时编译有性能开销、iOS 禁止 JIT
2. **IL2CPP 的特点**：
   - AOT（Ahead-Of-Time）编译：提前将 Csharp IL 转换为 C++ 代码，再编译为 Native 机器码
   - 性能约 Mono 的 1.5x（无 JIT 开销 + C++ 编译器优化）
   - iOS 必需（App Store 不允许运行时可写可执行内存页）
   - 更好的代码安全性（更难反编译为可读 Csharp 代码）
3. **IL2CPP 的限制**：
   - 不支持 `System.Reflection.Emit`（动态生成 IL 代码）
   - 编译时间长（构建时需要 IL -> C++ -> Native 两步编译）
   - 包体增大（C++ 代码量大于 IL 字节码）
   - 泛型虚拟方法可能有性能问题（需要额外的运行时查找表）
4. **选择建议**：当前主流项目选 IL2CPP（性能 + iOS 支持），PC/Mac 开发期可用 Mono 加速迭代。

## 详细解析

### IL2CPP 的编译流程
```
Csharp 源码 -> Roslyn 编译 -> CIL (IL 字节码)
-> IL2CPP.exe 转换 -> C++ 源码
-> 平台 C++ 编译器 (Xcode/Clang/MSVC) -> Native 机器码
```

### Managed Code Stripping
IL2CPP 会裁剪掉"未使用的代码"（Bytecode Stripping），减少包体。但可能误删反射需要的代码。解决：
```xml
<!-- link.xml -->
<linker>
  <assembly fullname="Assembly-CSharp">
    <type fullname="MyNamespace.MyClass" preserve="all" />
  </assembly>
</linker>
```

### IL2CPP 和 HybridCLR 的关系
HybridCLR（原huatuo）在 IL2CPP 的基础上增加了 **Interpreter** 模式，可以在 AOT 环境下解释执行补充的 IL 代码——这就是它实现 Csharp 热更新的关键。它的本质是：IL2CPP（AOT）+ 补充元数据 DLL（Interpreter 执行）。

## 面试官常见追问
- 为什么 iOS 不允许 JIT？（iOS 内核的安全策略：不允许将写权限内存页转为可执行，防止动态代码注入攻击）
- IL2CPP 比 Mono 快多少？（约 1.5 倍，取决于代码类型。数学计算提升大，IO 密集型提升小）
- 怎么解决 IL2CPP 裁剪导致反射失败？（link.xml 保留、`[Preserve]` 特性、避免反射调用被裁剪的类型）

## 关联知识点
- [[Csharp 反射]]
- [[热更新方案对比]]

## 原始出处
- GitHub面经_性能优化 Q14
- 博客园 多论坛面经汇总 3.2 节
