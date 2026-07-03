---
title: "LRU缓存"
category: 算法手撕高频题
tags: [算法, 手撕代码, LRU, 哈希表, 双向链表, 网易互娱]
frequency: ⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed: 
next_review: 
related:
  - "[[哈希表与冲突解决]]"
  - "[[链表高频操作]]"
---

## 🎯 一句话结论（自测用）
> 哈希表 + 双向链表：哈希表实现 O(1) 查找，双向链表维护访问顺序（最近访问在头部，最久未用也在尾部）。get/put 都是 O(1)。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **数据结构**：`unordered_map<key, list::iterator>` + 双向链表存 `(key, value)` 对
2. **get(key)**：哈希表查 -> 存在则移到链表头部（最近访问），返回 value；不存在返回 -1
3. **put(key, value)**：
   - 已存在：更新 value，移到头部
   - 不存在：容量满则删除链表尾部（最久未用），新节点插入头部
4. **关键**：用 list 的 splice 操作 O(1) 移动节点，不要先删再加

## 🔍 详细解析

### C++ 标准实现
```cpp
class LRUCache {
private:
    int cap;
    list<pair<int, int>> cache;  // 双向链表：<key, value>
    // 哈希表：key -> 链表迭代器
    unordered_map<int, list<pair<int, int>>::iterator> map;

public:
    LRUCache(int capacity) : cap(capacity) {}

    int get(int key) {
        auto it = map.find(key);
        if (it == map.end()) return -1;
        // 移到链表头部（splice 是 O(1) 移动，不拷贝）
        cache.splice(cache.begin(), cache, it->second);
        return it->second->second;
    }

    void put(int key, int value) {
        auto it = map.find(key);
        if (it != map.end()) {
            // 已存在，更新值并移到头部
            it->second->second = value;
            cache.splice(cache.begin(), cache, it->second);
            return;
        }
        // 容量满，删除最久未用（链表尾部）
        if (cache.size() == cap) {
            int oldKey = cache.back().first;
            map.erase(oldKey);
            cache.pop_back();
        }
        // 新节点插入头部
        cache.emplace_front(key, value);
        map[key] = cache.begin();
    }
};
```

### Csharp 版本（使用 LinkedList）
```csharp
public class LRUCache
{
    private int cap;
    private LinkedList<(int key, int value)> cache = new();
    private Dictionary<int, LinkedListNode<(int key, int value)>> map = new();

    public LRUCache(int capacity) { cap = capacity; }

    public int Get(int key)
    {
        if (!map.TryGetValue(key, out var node)) return -1;
        cache.Remove(node);         // O(1)
        cache.AddFirst(node);       // O(1)
        return node.Value.value;
    }

    public void Put(int key, int value)
    {
        if (map.TryGetValue(key, out var node))
        {
            node.ValueRef.value = value;
            cache.Remove(node);
            cache.AddFirst(node);
            return;
        }
        if (cache.Count == cap)
        {
            var last = cache.Last;
            map.Remove(last.Value.key);
            cache.RemoveLast();
        }
        var newNode = new LinkedListNode<(int, int)>((key, value));
        cache.AddFirst(newNode);
        map[key] = newNode;
    }
}
```

### 为什么要双向链表 + 哈希表？
| 操作 | 只用链表 | 只用哈希表 | 双向链表+哈希 |
|------|---------|-----------|-------------|
| 查找 key | O(n) | O(1) | O(1) |
| 删除尾部 | O(1) (双向) | 无法知道最久未用 | O(1) |
| 移动到头部 | O(n) (需要先找到) | 无法记录顺序 | O(1) |

### 为什么用 splice 而不是 erase + push_front？
```cpp
// 错误做法：O(n)，因为要先找到节点在链表中的位置
cache.erase(iter);   // 需要遍历
cache.push_front({key, value});

// 正确做法：O(1)，splice 直接修改指针
cache.splice(cache.begin(), cache, map[key]);  // 直接移动，O(1)
```

### 面试中的常见变体
**LFU（Least Frequently Used，最不经常使用）**：
- 需要额外维护使用频率计数器
- 数据结构更复杂：`map<freq, list<key>>` + `map<key, {value, freq, iterator}>`

## 💬 面试官常见追问
- "为什么选择双向链表而不是单向链表？" -> 需要 O(1) 删除任意节点（已知迭代器），双向链表可以 O(1) 获取前驱节点
- "哈希表 + 双向链表中，为什么哈希表的 value 存迭代器？" -> 通过迭代器可以直接用 splice 移动节点，O(1)
- "LRU 和 LFU 的区别？" -> LRU 按最近使用时间淘汰，LFU 按使用频率淘汰。LRU 实现简单，LFU 额外维护频率

## ⚠️ 我曾经的误区 / 网上常见错答
- **误区**：用 `erase + push_front` 代替 `splice`。erase 后迭代器失效，且性能差
- **误区**：删除尾部时忘记从哈希表中删除。导致哈希表中有无效迭代器，后续访问崩溃
- **误区**：链表中只存 value 不存 key。删除尾部时需要知道 key 来清理哈希表

## 🔗 关联知识点
- [[哈希表与冲突解决]]
- [[链表高频操作]]

## 📎 原始出处
- 012_互娱 Q24: LRU（二面项目追问）
