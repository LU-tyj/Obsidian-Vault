---
title: "Dictionary 底层原理"
category: Csharp语言基础
tags: [Csharp, Unity, 网易互娱, 哈希表, 数据结构]
frequency: ⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[List 底层原理与泛型集合]]"
---

## 一句话结论（自测用）
> Dictionary 底层是哈希表（拉链法），核心结构：buckets 数组 + entries 数组。查找 = hashCode -> bucket 索引 -> entry -> 对比 key。扩容到大于当前容量 2 倍的最小质数。冲突用拉链法（next 指针）。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **数据结构**：
   - `buckets[]`：int 数组，存 entries 的索引（-1 表示空）
   - `entries[]`：Entry 结构数组，每个 Entry 含 `key` / `value` / `hashCode` / `next`（冲突链的下一个 entry 索引）
   - `freeList` / `freeCount`：管理被删除的 entry 的回收
2. **查找流程**：
   ```
   key -> GetHashCode() -> hashCode & (buckets.Length - 1) -> bucketIndex
   buckets[bucketIndex] -> entryIndex
   entries[entryIndex].key == key ? 返回 : 沿 entries[entryIndex].next 继续
   ```
3. **插入流程**：
   - 计算 hashCode，找到 bucketIndex
   - 如果 bucket 为空，直接放；否则追加到冲突链
   - entries 数组满了触发扩容
4. **扩容**：新容量 = 大于当前容量 2 倍的最小**质数**（为什么是质数？减少哈希碰撞）
5. **冲突解决**：拉链法（Chaining），不是开放定址法。每个 Entry 有 next 字段指向链的下一个。

## 详细解析

### 为什么扩容选质数？
哈希表的索引是 `hashCode % capacity`。如果 capacity 是质数，哈希分布的均匀性更好。如果 capacity 是 2 的幂（如 `Hashtable`），可以直接用位运算 `hashCode & (capacity-1)`，但需要 hashCode 本身就均匀分布。

### 删除操作怎么处理？
`Remove(key)` 不真的删除 entry，而是将 entry 标记为 free，并加入 freeList（空闲链表）。下次插入时优先复用空闲 entry 位置。这避免了数组元素的移动。

### Dictionary vs Hashtable vs ConcurrentDictionary

| | Dictionary\<K,V\> | Hashtable | ConcurrentDictionary\<K,V\> |
|--|----------------|-----------|---------------------------|
| 泛型 | 是 | 否（存储 object） | 是 |
| 装箱 | 无 | 有 | 无 |
| 线程安全 | 否 | 部分（读安全） | 是（锁分段） |
| 获取不存在的 key | 抛异常 | 返回 null | 抛异常 / TryGetValue |
| 推荐使用 | 是 | 否 | 多线程场景 |

## 面试官常见追问
- `TryGetValue` 和 `ContainsKey + indexer` 哪个好？（TryGetValue 好，只查一次 key）
- 遍历 Dictionary 时能修改吗？（不能，会抛 `InvalidOperationException`）
- Dictionary 的 key 需要满足什么条件？（必须重写 `GetHashCode()` 和 `Equals()`，且 GetHashCode 在 key 被使用时不能变化）
- Dictionary 和 SortedDictionary 的区别？（Dictionary 是哈希表 O(1)，无序；SortedDictionary 是红黑树 O(log n)，有序）

## 我曾经的误区 / 网上常见错答
- **错**："扩容就是翻倍" —— 是大于 2 倍的最小质数，不是简单的 2 倍
- **错**："Dictionary 用开放定址法解决冲突" —— Csharp 的 Dictionary 是拉链法
- **错**："Dictionary 的 key 可以是任何类型" —— key 必须正确实现 GetHashCode 和 Equals，且作为 key 后不能修改

## 关联知识点
- [[List 底层原理与泛型集合]]
- [[Csharp 装箱与拆箱]]
- [[Csharp GC 垃圾回收]]

## 原始出处
- GitHub面经_CSharp基础 Q10
- 牛客网 002_雷火实习 Q19
