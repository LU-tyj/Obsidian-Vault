---
title: "Lua 闭包"
category: Csharp语言基础
tags: [Csharp, Lua, Unity, 网易互娱, 闭包]
frequency: ⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[Lua 元表与元方法]]"
  - "[[Lua GC]]"
  - "[[热更新方案对比]]"
---

## 一句话结论（自测用）
> 闭包 = 函数 + 它引用的外部变量（upvalue）。闭包可以实现数据隔离（每个闭包实例各自独立）、数据共享（多个闭包共享同一个 upvalue）、迭代器（闭包内保存状态）。雷火面试高频：闭包在热更新中的 upvalue 缓存陷阱。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **定义**：闭包 = 函数 + 其引用环境（upvalue）。upvalue 是函数外部定义的、被函数内部引用的局部变量。
2. **三大特性**：
   - **数据隔离**：不同实例的闭包，upvalue 各自独立——每个闭包有自己的一份 upvalue 副本
   - **数据共享**：多个闭包共享同一个 upvalue（在同一个作用域中创建时）
   - **迭代器**：闭包内保存状态，每次调用返回下一元素
3. **典型代码示例**：
   ```lua
   -- 闭包示例：计数器
   function createCounter()
       local count = 0          -- count 是 upvalue
       return function()
           count = count + 1    -- 闭包捕获并修改 upvalue
           return count
       end
   end

   local c1 = createCounter()
   local c2 = createCounter()
   print(c1()) -- 1（c1 的 count 独立）
   print(c1()) -- 2
   print(c2()) -- 1（c2 的 count 独立，数据隔离）
   ```

## 详细解析

### 数据共享 vs 数据隔离
```lua
-- 数据共享：两个闭包共享同一个 upvalue
local count = 0
local inc = function() count = count + 1 end
local get = function() return count end
-- inc 和 get 共享 count

-- 数据隔离：每次调用 createCounter 创建独立的 upvalue
-- 见上面的 createCounter 示例
```

### 闭包在热更新中的陷阱（雷火高频）
当通过 `require` 加载的模块中使用了闭包，热更时重新 require 会创建新闭包，但旧的闭包如果还在被其他地方引用（如事件回调），它持有的 upvalue 仍是旧的。**热更后需要重新注册事件，确保新代码使用新闭包。**

```lua
-- 热更前
local count = 0
function module.increment()
    count = count + 1
end

-- 热更后：新模块的 count 是 0，但老的闭包可能在 UI 按钮回调中
-- 解决方法：热更后重新注册所有事件回调
```

### Csharp 闭包 vs Lua 闭包
| | Csharp Lambda 闭包 | Lua 闭包 |
|--|---------------|---------|
| 捕获方式 | 编译器生成 DisplayClass | upvalue 机制 |
| 变量修改 | 可以修改捕获的变量 | 可以修改 upvalue |
| foreach 陷阱 | 捕获循环变量的常见 bug | Lua 用数值 for 没有类似问题 |

## 面试官常见追问
- 闭包和普通函数的区别？（闭包携带创建时的环境 upvalue，普通函数不携带）
- Lua 闭包怎么实现数据隔离？（每次执行外层函数创建新的 upvalue，不同闭包实例有独立的 upvalue）
- 热更时闭包有什么注意事项？（旧闭包可能持有旧的 upvalue，热更后需要重新注册回调）
- 闭包的 upvalue 什么时候被 GC？（当闭包本身不再被引用时）

## 我曾经的误区 / 网上常见错答
- **错**："Lua 的所有函数都是闭包" —— 严格来说，不引用外部变量的函数不是闭包（无 upvalue）
- **错**："闭包就是匿名函数" —— 命名函数也可以是闭包（只要引用了外部变量），匿名函数不引用外部变量也不是闭包
- **错**："闭包的 upvalue 在函数内部" —— upvalue 在函数外部，被闭包引用

## 关联知识点
- [[Lua 元表与元方法]]
- [[Lua GC]]
- [[热更新方案对比]]

## 原始出处
- GitHub面经_Lua与热更新 Q11
- 牛客网 005_雷火一二面 Q4
