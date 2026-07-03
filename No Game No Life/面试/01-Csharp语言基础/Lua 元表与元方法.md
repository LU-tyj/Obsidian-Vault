---
title: "Lua 元表与元方法"
category: Csharp语言基础
tags: [Csharp, Lua, Unity, 网易互娱, 热更新]
frequency: ⭐⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[Lua 闭包]]"
  - "[[Lua GC]]"
  - "[[Csharp与Lua交互原理]]"
  - "[[热更新方案对比]]"
---

## 一句话结论（自测用）
> 元表（Metatable）是一张用来定义另一张表行为的普通表。`__index` 在查询不到 key 时提供回退，`__newindex` 在给不存在的 key 赋值时拦截——这是 Lua 实现继承和面向对象的基础。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **元表本质**：一张普通 table，通过 `setmetatable()` 绑定到目标表上，用于重定义目标表的默认行为。
2. **核心元方法**：
   - `__index`：访问表中不存在的 key 时调用。可以设为函数或另一个表（最常用于实现继承）。
   - `__newindex`：给表中不存在的 key 赋值时调用。可用来拦截赋值操作（如实现只读表）。
   - `__call`：把表当函数调用时触发。
   - `__add / __sub / __mul / __div`：算术运算符重载。
   - `__eq / __lt / __le`：比较运算符重载。
   - `__tostring`：自定义 `tostring()` 行为。
3. **`__index` 访问流程**：查表 `t[key]` → 不存在 → 检查元表 `__index` → 如果是函数则调用返回 → 如果是表则在该表中查 → 都没有返回 nil。
4. **`__index` vs `__newindex`**：`__index` 是读拦截，`__newindex` 是写拦截。两者互不影响。

## 详细解析

### `__index` 实现继承的原理
```lua
local parent = { x = 10, y = 20 }
local child = {}
setmetatable(child, { __index = parent })
print(child.x)  -- 输出 10，从 parent 表查找
```
child 本身没有 x，通过元表的 `__index` 指向 parent，实现了类似"原型链"的继承效果。这就是 Lua 面向对象的基础——通过设置 `ClassName.__index = ClassName`（类本身作为实例的 `__index`），实例就可以访问类的方法。

### `__newindex` 的实际应用
- **只读表**：`__newindex` 设为抛出错误的函数
- **属性代理**：拦截赋值操作，转发到另一个对象
- **数据绑定**：修改时通知观察者（类似 MVVM）

### rawget / rawset
`rawget(t, k)` 和 `rawset(t, k, v)` 会跳过元表机制，直接访问表本身。这在元方法内部需要访问原始数据时非常重要，避免无限递归。

## 面试官常见追问
- Lua 怎么实现面向对象？（通过 `__index` 指向类表实现继承，冒号语法传递 self）
- `__index` 设为函数和设为表的区别？（函数更灵活可动态计算，表更简单直接）
- 元表可以嵌套吗？（表可以有元表，元表本身也可以有元表，形成链）
- `__mode` 是什么？（弱引用表，k/v 设置弱引用模式，用于缓存和自动释放）
- `__gc` 是什么？（Lua 5.2+，自定义最终化器，类似 Csharp 的析构函数）

## 我曾经的误区 / 网上常见错答
- **错**："元表是 Lua 的特殊类型" —— 元表就是普通 table，只是被 `setmetatable` 赋予了特殊含义
- **错**："`__index` 和 `__newindex` 必须成对出现" —— 两者独立设置，可以只要一个
- **错**："`__index` 查不到就报错" —— 查不到返回 nil，不会报错

## 关联知识点
- [[Lua 闭包]]
- [[Lua GC]]
- [[Csharp与Lua交互原理]]
- [[xLua 热更原理]]
- [[热更新方案对比]]

## 原始出处
- GitHub面经_Lua与热更新 Q7
- 牛客网 005_雷火一面 Q6
- 博客园 多论坛面经汇总 3.2 节
