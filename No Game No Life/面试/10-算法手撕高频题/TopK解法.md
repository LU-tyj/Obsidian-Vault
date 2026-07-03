---
title: "TopK解法"
category: 算法手撕高频题
tags: [算法, 手撕代码, TopK, 堆, 快排, 网易互娱]
frequency: ⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed: 
next_review: 
related:
  - "[[TopK问题]]"
  - "[[快速排序]]"
  - "[[堆排序]]"
---

## 🎯 一句话结论（自测用）
> 找最大 K 个 -> 小顶堆 O(nlogk)。找最小 K 个 -> 大顶堆。QuickSelect 期望 O(n) 但不稳定。面试两种都写。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **堆解法**：大小为 K 的小顶堆（找最大），遍历数组，大于堆顶则替换。O(nlogk)
2. **QuickSelect**：类似快排分区，分区后 pivot 位置 == k 则停止。期望 O(n)，最坏 O(n^2)
3. **两解对比**：K 小用堆，K 大用 QuickSelect

## 🔍 详细解析

### 解法一：小顶堆（找最大的 K 个）
```cpp
vector<int> topKLargest(vector<int>& nums, int k) {
    // 小顶堆，greater<int> 使堆顶是最小值
    priority_queue<int, vector<int>, greater<int>> minHeap;
    
    for (int x : nums) {
        minHeap.push(x);
        if (minHeap.size() > k) minHeap.pop();
    }
    
    vector<int> res;
    while (!minHeap.empty()) {
        res.push_back(minHeap.top());
        minHeap.pop();
    }
    return res;
}
```

### 解法二：QuickSelect（找第 K 大的元素）
```cpp
int partition(vector<int>& nums, int l, int r) {
    int pivot = nums[r];
    int i = l;
    for (int j = l; j < r; j++) {
        if (nums[j] < pivot) {
            swap(nums[i], nums[j]);
            i++;
        }
    }
    swap(nums[i], nums[r]);
    return i;
}

int quickSelect(vector<int>& nums, int l, int r, int k) {
    if (l == r) return nums[l];
    
    int pivotIdx = partition(nums, l, r);
    
    if (pivotIdx == k) return nums[pivotIdx];
    else if (pivotIdx < k) return quickSelect(nums, pivotIdx + 1, r, k);
    else return quickSelect(nums, l, pivotIdx - 1, k);
}

int findKthLargest(vector<int>& nums, int k) {
    // 第 K 大 = 升序数组第 (n-k) 小
    return quickSelect(nums, 0, nums.size() - 1, nums.size() - k);
}
```

### Csharp 版本（堆解法）
```csharp
public int[] TopKLargest(int[] nums, int k)
{
    // .NET 6+ PriorityQueue（默认小顶堆）
    var minHeap = new PriorityQueue<int, int>();
    foreach (int x in nums)
    {
        minHeap.Enqueue(x, x);
        if (minHeap.Count > k) minHeap.Dequeue();
    }
    
    int[] res = new int[k];
    for (int i = 0; i < k; i++)
        res[i] = minHeap.Dequeue();
    return res;
}
```

### Csharp 版本（QuickSelect）
```csharp
public int FindKthLargest(int[] nums, int k)
{
    return QuickSelect(nums, 0, nums.Length - 1, nums.Length - k);
}

private int QuickSelect(int[] nums, int left, int right, int k)
{
    if (left == right) return nums[left];
    int pivotIdx = Partition(nums, left, right);
    if (pivotIdx == k) return nums[pivotIdx];
    else if (pivotIdx < k) return QuickSelect(nums, pivotIdx + 1, right, k);
    else return QuickSelect(nums, left, pivotIdx - 1, k);
}

private int Partition(int[] nums, int left, int right)
{
    int pivot = nums[right], i = left;
    for (int j = left; j < right; j++)
        if (nums[j] < pivot) (nums[i++], nums[j]) = (nums[j], nums[i]);
    (nums[i], nums[right]) = (nums[right], nums[i]);
    return i;
}
```

### 场景变体：大玩家排行榜（数据动态变化）
```cpp
// 维护一个大小为 K 的小顶堆，支持动态更新
class TopKRanking {
    priority_queue<int, vector<int>, greater<int>> minHeap;
    int capacity;
public:
    TopKRanking(int k) : capacity(k) {}
    
    void insert(int score) {
        if (minHeap.size() < capacity) {
            minHeap.push(score);
        } else if (score > minHeap.top()) {
            minHeap.pop();
            minHeap.push(score);
        }
    }
    
    void remove(int score) {
        // 需要增强数据结构支持删除（如 multiset 或两个堆）
        // 简单场景用 multiset
    }
};
```

## 💬 面试官常见追问
- "堆解法中，为什么找最大 K 个用小顶堆？" -> 小顶堆堆顶是最小值，当元素 > 堆顶时替换，保留的就是最大的 K 个
- "QuickSelect 的最坏情况是什么？如何避免？" -> 每次选到最小/最大元素 -> O(n^2)。随机化基准避免
- "海量数据 TopK（内存放不下）怎么处理？" -> 分治 + 堆：分块读取，每块求 TopK，最后合并

## ⚠️ 我曾经的误区 / 网上常见错答
- **误区**：找最大 K 个用大顶堆。会不断弹出最大值，最后剩下的是最小的 K 个
- **误区**：QuickSelect 中 k 的含义。第 K 大在升序数组中对应索引 n-k，不是 k
- **误区**：堆大小为 K 后，新元素 < 堆顶时不处理（漏掉潜在的大元素）。正确逻辑：只有 > 堆顶才替换

## 🔗 关联知识点
- [[TopK问题]]
- [[快速排序]]
- [[堆排序]]

## 📎 原始出处
- 002_雷火 Q18: TopK
- 007_互娱 Q5: TopK排序问题
