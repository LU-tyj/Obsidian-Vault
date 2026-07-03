---
title: "Lua GC"
category: Csharp语言基础
tags: [Csharp, Lua, Unity, 网易互娱, GC]
frequency: ⭐⭐
difficulty: 中等
companies: [网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[Csharp GC 垃圾回收]]"
  - "[[Lua 元表与元方法]]"
  - "[[Lua 闭包]]"
---

## 一句话结论（自测用）
> Lua GC 使用**三色标记-清除**算法（不分代）：白色=可回收，灰色=中间态，黑色=存活。与 Csharp GC 的最大区别：Lua 不分代、用三色而非两色、清理过程分阶段。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **算法**：标记-清除（Mark-Sweep），三色标记
2. **三色标记**：

| 颜色 | 含义 |
|------|------|
| **白色（新）** | GC 标记阶段后新创建的对象，默认色 |
| **白色（旧）** | 上一轮未被标记，可回收 |
| **灰色** | 中间状态，已标记但其引用的对象还未扫描完成 |
| **黑色** | 已标记 + 所有引用对象都已扫描，确定存活 |

3. **标记阶段流程**：
   - 从根节点（全局表、注册表、线程栈）出发，将可达对象放入 gray 链表
   - 不断从 gray 取出对象移至黑色，扫描其引用对象（白色 -> 灰色）
   - gray 链表为空时标记完成，所有白色对象是可回收的
4. **清除阶段**：遍历全局对象链表（allgc），释放白色对象
5. **Lua GC vs Csharp GC 对比**：

| | Csharp GC | Lua GC |
|--|-------|--------|
| 算法 | 标记-清除 + 压缩 + 分代 | 标记-清除（三色标记） |
| 分代 | 3 代（Gen 0/1/2） | 不分代 |
| 增量/并发 | 支持增量 GC（Unity 2019+） | 支持增量 GC（Lua 5.1+ `collectgarbage("step")`） |
| 触发方式 | 自动 + 手动 | 自动 + `collectgarbage()` |
| 弱引用 | 无内置 | 有（`__mode` 元方法） |

## 详细解析

### Lua 弱引用表
```lua
-- 弱 key 表：key 没有被其他地方引用时，该键值对自动被 GC
local cache = {}
setmetatable(cache, { __mode = "k" })  -- 或 "v"（弱 value）/ "kv"（都弱）

-- 常用于：缓存、对象属性存储（对象销毁时属性自动释放）
```

### collectgarbage 常用操作
```lua
collectgarbage("collect")  -- 立即执行一次完整 GC
collectgarbage("count")    -- 返回当前内存使用量（KB）
collectgarbage("stop")     -- 停止自动 GC
collectgarbage("restart")  -- 重启自动 GC
collectgarbage("step", n)  -- 执行 n KB 内存的增量 GC
collectgarbage("setpause", p)  -- 设置 GC 暂停参数
collectgarbage("setstepmul", m) -- 设置 GC 步进乘数
```

### Lua 5.4 的分代 GC
Lua 5.4 引入了分代 GC 模式（可选），将对象分为"年轻"和"年老"。年轻对象被更频繁回收。但这是可选模式，默认仍是增量标记-清除。

### 网易面试常见追问：Lua 内存泄漏如何排查？
1. `collectgarbage("count")` 前后对比，看是否增长
2. 检查全局表 `_G` 中是否有未清理的引用
3. 检查闭包是否持有已不需要的 upvalue
4. 检查事件/回调是否未注销
5. 避免：全局变量、未释放的 userdata、循环引用（Lua 5.1 不会回收循环引用的 table，5.2+ 修复）

## 面试官常见追问
- 三色标记和两色标记有什么区别？（三色可以渐进式执行，灰色状态让 GC 可以暂停/恢复，不卡死）
- Lua 为什么不分代？（历史原因，5.4 可选分代；Lua 对象通常生命周期较短，简化设计）
- `__gc` 元方法是什么？（Lua 5.2+ 的自定义终结器，在对象被 GC 时调用，类似 Csharp 析构函数）
- Lua 的循环引用会被 GC 吗？（Lua 5.2+ 可以，因为是可达性分析而非引用计数）

## 我曾经的误区 / 网上常见错答
- **错**："Lua GC 和 Csharp GC 一样" —— 核心区别：Csharp 分代 + 压缩，Lua 不分代（默认）+ 不压缩
- **错**："Lua 5.1 不能处理循环引用" —— 可以！Lua 是标记-清除，天然处理循环引用
- **错**："white 和 black 就够了，为什么有 gray" —— gray 支持增量 GC，可以在任意时刻暂停/恢复

## 关联知识点
- [[Csharp GC 垃圾回收]]
- [[Lua 元表与元方法]]
- [[Lua 闭包]]
- [[热更新方案对比]]

## 原始出处
- GitHub面经_Lua与热更新 Q12-Q13
- 博客园 多论坛面经汇总 3.2 节
