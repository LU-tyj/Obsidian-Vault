---
title: "List 底层原理与泛型集合"
category: Csharp语言基础
tags: [Csharp, Unity, 网易互娱, 集合, 泛型]
frequency: ⭐
difficulty: 中等
companies: [网易互娱]
status: new
last_reviewed:
next_review:
related:
  - "[[Dictionary 底层原理]]"
  - "[[Csharp 装箱与拆箱]]"
---

## 一句话结论（自测用）
> List = 动态数组，扩容翻倍（newCapacity = oldCapacity * 2），插入删除 O(n)。ArrayList 存 object 有装箱，已淘汰。泛型集合（List\<T\>、Dictionary\<K,V\>）类型安全无装箱。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **List 底层 = 动态数组**：
   - 内部维护一个 `T[] _items` 数组
   - 初始容量为 0（或构造函数指定）
   - `Add()` 时若容量不足，扩容为原来的 **2 倍**
   - `Insert()` / `RemoveAt()` 需要移动元素（O(n)）
   - 优化删除：交换末尾元素到删除位置，再移除末尾（O(1)，但不保持顺序）
2. **ArrayList vs List\<T\>**：

| | ArrayList | List\<T\> |
|--|-----------|-----------|
| 元素类型 | object（所有元素都要装箱） | T（泛型，无装箱） |
| 类型安全 | 否（运行时 InvalidCastException 风险） | 是（编译时检查） |
| 性能 | 差（装箱 + 拆箱开销） | 好 |
| 推荐使用 | 否（遗留代码） | 是 |

3. **泛型的好处**：
   - 编译时类型安全
   - 无装箱拆箱，无 GC 压力
   - 代码复用（一个 `List<T>` 适用于所有 T）
   - 运行性能更优（JIT 为每个值类型生成专用版本）

## 详细解析

### List 扩容的细节
```csharp
// 内部扩容逻辑（简化）
private void EnsureCapacity(int min) {
    if (_items.Length < min) {
        int newCapacity = _items.Length == 0 ? 4 : _items.Length * 2;
        if (newCapacity < min) newCapacity = min;
        T[] newItems = new T[newCapacity];
        Array.Copy(_items, newItems, _size);
        _items = newItems; // 旧数组被 GC
    }
}
```
- 初始容量 = 4（第一次 Add 时）
- 扩容时分配新数组 + 拷贝元素 + 旧数组变成垃圾

### 优化技巧
1. 预估容量：`new List<int>(1000)` 避免多次扩容
2. `AddRange` 优于循环 `Add`：预知总容量一次性扩容
3. 大量删除用 `RemoveAll(predicate)`：内部优化，不逐元素移动

## 面试官常见追问
- List 的 `Capacity` 和 `Count` 有什么区别？（Capacity = 内部数组长度，Count = 实际元素个数）
- List 是线程安全的吗？（不是。需要线程安全用 `ConcurrentBag<T>` 或手动加锁）
- `List.ForEach` 和 `foreach` 有什么区别？（ForEach 是 List 的方法接受 Action，foreach 是 Csharp 语法；ForEach 中不能 break/continue）

## 关联知识点
- [[Dictionary 底层原理]]
- [[Csharp 装箱与拆箱]]
- [[Csharp GC 垃圾回收]]

## 原始出处
- GitHub面经_CSharp基础 Q9/Q11
