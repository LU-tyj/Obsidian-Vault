---
title: "动态规划DP"
category: 数据结构与算法
tags: [算法, 数据结构, 动态规划, 网易互娱]
frequency: ⭐⭐⭐
difficulty: 较难
companies: [网易互娱, 网易雷火]
status: new
last_reviewed: 
next_review: 
related:
  - "[[二叉树高频操作]]"
  - "[[最长公共子串与最长回文子串]]"
  - "[[上楼梯与斐波那契]]"
  - "[[背包问题]]"
---

## 🎯 一句话结论（自测用）
> DP 三步走：定义状态 -> 状态转移方程 -> 初始化与边界。核心题型：背包 / 最长子串 / 上楼梯 / 最长回文子串。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **DP 核心思想**：将大问题分解为重叠子问题，用数组/哈希存储子问题结果避免重复计算
2. **上楼梯（Climbing Stairs）**：`dp[i] = dp[i-1] + dp[i-2]`，可优化为 O(1) 空间
3. **最长公共子串（Longest Common Substring）**：`dp[i][j] = (s1[i]==s2[j]) ? dp[i-1][j-1]+1 : 0`，记录最大值
4. **最长公共子序列（LCS）**：`dp[i][j] = (s1[i]==s2[j]) ? dp[i-1][j-1]+1 : max(dp[i-1][j], dp[i][j-1])`
5. **背包问题**：`dp[j] = max(dp[j], dp[j-w[i]] + v[i])`（逆序遍历）
6. **最长回文子串**：中心扩展法 O(n^2) 或 Manacher O(n)

## 🔍 详细解析

### 上楼梯（LeetCode 70）
n 阶楼梯，每次爬 1 或 2 阶，求方法数。
```cpp
int climbStairs(int n) {
    if (n <= 2) return n;
    int a = 1, b = 2;
    for (int i = 3; i <= n; i++) {
        int c = a + b;
        a = b; b = c;
    }
    return b;
}
```

### 最长公共子串（注意：子串要求连续，子序列不要求）
```cpp
int longestCommonSubstring(string s1, string s2) {
    int m = s1.size(), n = s2.size(), maxLen = 0;
    vector<vector<int>> dp(m+1, vector<int>(n+1, 0));
    for (int i = 1; i <= m; i++)
        for (int j = 1; j <= n; j++)
            if (s1[i-1] == s2[j-1]) {
                dp[i][j] = dp[i-1][j-1] + 1;
                maxLen = max(maxLen, dp[i][j]);
            }
    return maxLen;
}
```

### 最长回文子串（LeetCode 5）
中心扩展法（O(n^2)）：
```cpp
string longestPalindrome(string s) {
    int start = 0, maxLen = 0;
    for (int i = 0; i < s.size(); i++) {
        // 奇数长度
        int l = i, r = i;
        while (l >= 0 && r < s.size() && s[l] == s[r]) { l--; r++; }
        if (r - l - 1 > maxLen) { start = l + 1; maxLen = r - l - 1; }
        // 偶数长度
        l = i; r = i + 1;
        while (l >= 0 && r < s.size() && s[l] == s[r]) { l--; r++; }
        if (r - l - 1 > maxLen) { start = l + 1; maxLen = r - l - 1; }
    }
    return s.substr(start, maxLen);
}
```

### 背包问题（0/1 背包）
子集和为 m 且乘积最大（面试变体）：
`dp[i][j]` = 前 i 个元素能否组成和 j。但乘积最大需要额外记录。

## 💬 面试官常见追问
- "DP 和贪心有什么区别？" -> DP 考虑所有可能，有最优子结构；贪心每步选局部最优，不一定全局最优
- "最长子串和最长子序列的区别？" -> 子串必须连续，dp 方程为 s[i]==s[j] 时继承，否则清零；子序列不要求连续，可以跳
- "DP 如何优化空间？" -> 状态压缩（滚动数组），背包问题从二维降到一维逆序遍历

## ⚠️ 我曾经的误区 / 网上常见错答
- **误区**：上楼梯用递归直接 `return climb(n-1)+climb(n-2)`。O(2^n) 指数级，必须记忆化或迭代
- **误区**：背包内层循环正序。0/1 背包必须逆序，否则变成完全背包（物品可重复使用）

## 🔗 关联知识点
- [[上楼梯与斐波那契]]
- [[最长公共子串与最长回文子串]]
- [[背包问题]]
- [[二叉树高频操作]]

## 📎 原始出处
- 006_互娱 Q10: 最长公共子字符串(DP)、Q13: 上楼梯(迭代+记忆化)
- 014_互娱 Q14: 子集和为m且乘积最大(背包DP)
- 010_雷火 Q9: 最长回文子串
- 博客园 3.4: "动态规划（DP）极高（Medium）"
