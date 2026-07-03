---
title: "TopK问题"
category: 数据结构与算法
tags: [算法, 数据结构, TopK, 堆, 网易互娱]
frequency: ⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed: 
next_review: 
related:
  - "[[排序算法]]"
  - "[[堆排序]]"
---

## 🎯 一句话结论（自测用）
> TopK 标准解：找最大 K 个用小顶堆 O(nlogk)，找最小 K 个用大顶堆。全排序 O(nlogn) 浪费。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **TopK 问题定义**：从 n 个元素中找出最大/最小的 K 个
2. **堆解法（最优）**：
   - 找最大 K 个 -> 小顶堆（大小为 K），遍历元素，大于堆顶则替换，O(nlogk)
   - 找最小 K 个 -> 大顶堆（大小为 K），遍历元素，小于堆顶则替换，O(nlogk)
3. **快速选择（QuickSelect）**：类似快排分区，期望 O(n)，最坏 O(n^2)
4. **100万数据选前1万**：小顶堆 O(nlog10000)
5. **排行榜场景变体**：玩家战斗力频繁变化取前1000名 -> 优先队列（在线算法），或桶排序（战斗力范围有限时 O(n)）

## 🔍 详细解析

### 堆解法代码思路
```cpp
vector<int> topKLargest(vector<int>& nums, int k) {
    priority_queue<int, vector<int>, greater<int>> minHeap;  // 小顶堆
    for (int x : nums) {
        minHeap.push(x);
        if (minHeap.size() > k) minHeap.pop();
    }
    vector<int> res;
    while (!minHeap.empty()) { res.push_back(minHeap.top()); minHeap.pop(); }
    return res;
}
```
时间复杂度 O(nlogk)，空间 O(k)。

### 快速选择（QuickSelect）思路
```cpp
int quickSelect(vector<int>& nums, int l, int r, int k) {
    if (l == r) return nums[l];
    int pivot = partition(nums, l, r);
    if (pivot == k) return nums[pivot];
    else if (pivot < k) return quickSelect(nums, pivot+1, r, k);
    else return quickSelect(nums, l, pivot-1, k);
}
```
期望 O(n)，最坏 O(n^2)。适用于不需要全排序的场景。

### 面试场景题：大玩家排行榜设计
需求：玩家战斗力频繁变化，取前 1000 名。
- **方案一（优先队列）**：动态排名，维护一个大小为 1000 的小顶堆。玩家战力变化时更新堆。O(nlog1000)
- **方案二（桶排序）**：战斗力最多 1 万 -> 1 万个桶，每桶存该战斗力的玩家列表。取前 1000 时从大到小遍历桶。O(10000)
- **方案三（分段区间排序）**：先分桶，再在每个桶内排序。用于"查询某个排名段的玩家"

## 💬 面试官常见追问
- "TopK 在海量数据（无法一次加载到内存）怎么处理？" -> 分治 + 堆：将数据分成多个小文件，每个文件求 TopK，再合并。或使用 MapReduce
- "堆解法和快排解法什么时候选哪个？" -> K 很小时堆更优，K 接近 n 时全排序可能更简单
- "如果数据有重复怎么办？" -> 堆解法天然支持重复。快速选择需要注意去重逻辑

## ⚠️ 我曾经的误区 / 网上常见错答
- **误区**：找最大 K 个用大顶堆。大顶堆会每次弹出最大值，剩下的是最小的 K 个。正确：找最大 K 个用小顶堆
- **误区**：面试只说堆解法。忘了提 QuickSelect 和桶排序（数据范围有限时的 O(n) 解法），体现广度不够
- **误区**：说 TopK 用「先排序再取前 K」。O(nlogn) 不是最优，除非你还需要全排序结果

## 🔗 关联知识点
- [[排序算法]]
- [[堆排序]]
- [[快速排序]]

## 📎 原始出处
- 002_雷火 Q18: TopK 与 反转链表、括号匹配 一同考察
- 007_互娱 Q5: TopK 排序问题; Q6: 大玩家排行榜
- 004_互娱 Q11: 排行榜设计（优先队列/桶排序）
- GitHub Q6: 100 万数据选出前 1 万大的数
- 博客园 3.4: "TopK 频率高 LeetCode Medium"
