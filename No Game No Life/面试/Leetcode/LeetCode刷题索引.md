---
title: LeetCode刷题索引
category: 算法
tags:
  - LeetCode
  - 刷题
  - HOT100
  - 面试
date: 2026-07-04
---

# LeetCode 刷题索引

> 选题规则：**HOT 100 全收录** + 每专题固定配额补齐。按 [灵茶山艾府题单](https://leetcode.cn/discuss/post/3141566/ru-he-ke-xue-shua-ti-by-endlesscheng-q3yd/) 的 12 大专题组织。
> 
> 标注 `[HOT100]` 的题为 LeetCode HOT 100 经典面试题，优先完成。

## 统计总览

| 专题 | 子类型数 | 选题总数 | HOT100 题数 |
|------|----------|----------|-------------|
| 滑动窗口与双指针 | 2 | 15 | 3 |
| 二分算法 | 3 | 12 | 6 |
| 单调栈 | 3 | 10 | 3 |
| 网格图 | 2 | 10 | 2 |
| 位运算 | 3 | 10 | 1 |
| 图论算法 | 6 | 20 | 2 |
| 动态规划 | 7 | 35 | 19 |
| 常用数据结构 | 8 | 30 | 12 |
| 数学算法 | 4 | 12 | 1 |
| 贪心与思维 | 5 | 18 | 4 |
| 链表、树与回溯 | 6 | 33 | 33 |
| 字符串 | 6 | 10 | 0 |
| **合计** | | **215** | **86** |

---

## 1. 滑动窗口与双指针（15 题，HOT100 3 题）

### 定长滑动窗口（10 题）

- [x] [438. 找到字符串中所有字母异位词](https://leetcode.cn/problems/find-all-anagrams-in-a-string/) **[HOT100]** ✅ 2026-07-04
- [x] [3. 无重复字符的最长子串](https://leetcode.cn/problems/longest-substring-without-repeating-characters/) **[HOT100]** ✅ 2026-07-04
- [x] [76. 最小覆盖子串](https://leetcode.cn/problems/minimum-window-substring/) **[HOT100]** ✅ 2026-07-04
- [ ] [1456. 定长子串中元音的最大数目](https://leetcode.cn/problems/maximum-number-of-vowels-in-a-substring-of-given-length/) `1263`
- [ ] [1343. 大小为 K 且平均值大于等于阈值的子数组数目](https://leetcode.cn/problems/number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold/) `1317`
- [ ] [3090. 每个字符最多出现两次的最长子字符串](https://leetcode.cn/problems/maximum-length-substring-with-two-occurrences/) `1329`
- [ ] [2090. 半径为 k 的子数组平均值](https://leetcode.cn/problems/k-radius-subarray-averages/) `1358`
- [ ] [2379. 得到 K 个黑块的最少涂色次数](https://leetcode.cn/problems/minimum-recolors-to-get-k-consecutive-black-blocks/) `1360`
- [ ] [1052. 爱生气的书店老板](https://leetcode.cn/problems/grumpy-bookstore-owner/) `1418`
- [ ] [1493. 删掉一个元素以后全为 1 的最长子数组](https://leetcode.cn/problems/longest-subarray-of-1s-after-deleting-one-element/) `1423`

### 单序列双指针（5 题）

- [ ] [2000. 反转单词前缀](https://leetcode.cn/problems/reverse-prefix-of-word/) `1199`
- [ ] [3643. 垂直翻转子矩阵](https://leetcode.cn/problems/flip-square-submatrix-vertically/) `1235`
- [ ] [832. 翻转图像](https://leetcode.cn/problems/flipping-an-image/) `1243`
- [ ] [3823. 反转一个字符串里的字母后反转特殊字符](https://leetcode.cn/problems/reverse-letters-then-special-characters-in-a-string/) `1250`
- [ ] [3775. 反转元音数相同的单词](https://leetcode.cn/problems/reverse-words-with-same-vowel-count/) `1392`

---

## 2. 二分算法（12 题，HOT100 6 题）

### 二分查找（6 题）

- [ ] [34. 在排序数组中查找元素的第一个和最后一个位置](https://leetcode.cn/problems/find-first-and-last-position-of-element-in-sorted-array/) **[HOT100]**
- [ ] [35. 搜索插入位置](https://leetcode.cn/problems/search-insert-position/) **[HOT100]**
- [ ] [981. 基于时间的键值存储](https://leetcode.cn/problems/time-based-key-value-store/) `1146`
- [ ] [1385. 两个数组间的距离值](https://leetcode.cn/problems/find-the-distance-value-between-two-arrays/) `1235`
- [ ] [1170. 比较字符串最小字母出现频次](https://leetcode.cn/problems/compare-strings-by-frequency-of-the-smallest-character/) `1432`
- [ ] [2300. 咒语和药水的成功对数](https://leetcode.cn/problems/successful-pairs-of-spells-and-potions/) `1477`

### 其他（4 题）

- [ ] [74. 搜索二维矩阵](https://leetcode.cn/problems/search-a-2d-matrix/) **[HOT100]**
- [ ] [153. 寻找旋转排序数组中的最小值](https://leetcode.cn/problems/find-minimum-in-rotated-sorted-array/) **[HOT100]**
- [ ] [33. 搜索旋转排序数组](https://leetcode.cn/problems/search-in-rotated-sorted-array/) **[HOT100]**
- [ ] [4. 寻找两个正序数组的中位数](https://leetcode.cn/problems/median-of-two-sorted-arrays/) **[HOT100]**

### 二分答案（2 题）

- [ ] [3824. 减小数组使其满足条件的最小 K 值](https://leetcode.cn/problems/minimum-k-to-reduce-array-within-limit/) `1531`
- [ ] [1283. 使结果不超过阈值的最小除数](https://leetcode.cn/problems/find-the-smallest-divisor-given-a-threshold/) `1542`

---

## 3. 单调栈（10 题，HOT100 3 题）

### 基础单调栈（6 题）

- [ ] [739. 每日温度](https://leetcode.cn/problems/daily-temperatures/) **[HOT100]**
- [ ] [1019. 链表中的下一个更大节点](https://leetcode.cn/problems/next-greater-node-in-linked-list/) `1571`
- [ ] [962. 最大宽度坡](https://leetcode.cn/problems/maximum-width-ramp/) `1608`
- [ ] [901. 股票价格跨度](https://leetcode.cn/problems/online-stock-span/) `1709`
- [ ] [768. 最多能完成排序的块 II](https://leetcode.cn/problems/max-chunks-to-make-sorted-ii/) `1788`
- [ ] [3814. 预算下的最大总容量](https://leetcode.cn/problems/maximum-capacity-within-budget/) `1796`

### 最小字典序（2 题）

- [ ] [1081. 不同字符的最小子序列](https://leetcode.cn/problems/smallest-subsequence-of-distinct-characters/) `316`
- [ ] [402. 移掉 K 位数字](https://leetcode.cn/problems/remove-k-digits/) `1800`

### 矩形面积（2 题）

- [ ] [84. 柱状图中最大的矩形](https://leetcode.cn/problems/largest-rectangle-in-histogram/) **[HOT100]**
- [ ] [42. 接雨水](https://leetcode.cn/problems/trapping-rain-water/) **[HOT100]**

---

## 4. 网格图（10 题，HOT100 2 题）

### 网格图DFS（7 题）

- [ ] [200. 岛屿数量](https://leetcode.cn/problems/number-of-islands/) **[HOT100]**
- [ ] [3619. 总价值可以被 K 整除的岛屿数目](https://leetcode.cn/problems/count-islands-with-total-value-divisible-by-k/) `1461`
- [ ] [2658. 网格图中鱼的最大数目](https://leetcode.cn/problems/maximum-number-of-fish-in-a-grid/) `1490`
- [ ] [1034. 边界着色](https://leetcode.cn/problems/coloring-a-border/) `1579`
- [ ] [1020. 飞地的数量](https://leetcode.cn/problems/number-of-enclaves/) `1615`
- [ ] [2684. 矩阵中移动的最大次数](https://leetcode.cn/problems/maximum-number-of-moves-in-a-grid/) `1626`
- [ ] [1254. 统计封闭岛屿的数目](https://leetcode.cn/problems/number-of-closed-islands/) `1659`

### 网格图BFS（3 题）

- [ ] [994. 腐烂的橘子](https://leetcode.cn/problems/rotting-oranges/) **[HOT100]**
- [ ] [1926. 迷宫中离入口最近的出口](https://leetcode.cn/problems/nearest-exit-from-entrance-in-maze/) `1638`
- [ ] [1091. 二进制矩阵中的最短路径](https://leetcode.cn/problems/shortest-path-in-binary-matrix/) `1658`

---

## 5. 位运算（10 题，HOT100 1 题）

### 位运算基础（6 题）

- [ ] [1009. 十进制整数的反码](https://leetcode.cn/problems/complement-of-base-10-integer/) `476`
- [ ] [3370. 仅含置位位的最小整数](https://leetcode.cn/problems/smallest-number-with-all-set-bits/) `1199`
- [ ] [3226. 使两个整数相等的位更改次数](https://leetcode.cn/problems/number-of-bit-changes-to-make-two-integers-equal/) `1247`
- [ ] [1356. 根据数字二进制下 1 的数目排序](https://leetcode.cn/problems/sort-integers-by-the-number-of-1-bits/) `1258`
- [ ] [461. 汉明距离](https://leetcode.cn/problems/hamming-distance/) `1282`
- [ ] [2220. 转换数字的最少位翻转次数](https://leetcode.cn/problems/minimum-bit-flips-to-convert-number/) `1282`

### 位运算性质（3 题）

- [ ] [1486. 数组异或操作](https://leetcode.cn/problems/xor-operation-in-an-array/) `1181`
- [ ] [2980. 检查按位或是否存在尾随零](https://leetcode.cn/problems/check-if-bitwise-or-has-trailing-zeros/) `1234`
- [ ] [1720. 解码异或后的数组](https://leetcode.cn/problems/decode-xored-array/) `1284`

### 其他（1 题）

- [ ] [136. 只出现一次的数字](https://leetcode.cn/problems/single-number/) **[HOT100]**

---

## 6. 图论算法（20 题，HOT100 2 题）

### 图DFS（8 题）

- [ ] [207. 课程表](https://leetcode.cn/problems/course-schedule/) **[HOT100]**
- [ ] [797. 所有可能的路径](https://leetcode.cn/problems/all-paths-from-source-to-target/) `1383`
- [ ] [1306. 跳跃游戏 III](https://leetcode.cn/problems/jump-game-iii/) `1397`
- [ ] [841. 钥匙和房间](https://leetcode.cn/problems/keys-and-rooms/) `1412`
- [ ] [2316. 统计无向图中无法互相到达点对数](https://leetcode.cn/problems/count-unreachable-pairs-of-nodes-in-an-undirected-graph/) `1604`
- [ ] [1319. 连通网络的操作次数](https://leetcode.cn/problems/number-of-operations-to-make-network-connected/) `1633`
- [ ] [2492. 两个城市间路径的最小分数](https://leetcode.cn/problems/minimum-score-of-a-path-between-two-cities/) `1680`
- [ ] [3310. 移除可疑的方法](https://leetcode.cn/problems/remove-methods-from-project/) `1711`

### 图BFS（3 题）

- [ ] [3243. 新增道路查询后的最短距离 I](https://leetcode.cn/problems/shortest-distance-after-road-addition-queries-i/) `1568`
- [ ] [1311. 获取你好友已观看的视频](https://leetcode.cn/problems/get-watched-videos-by-your-friends/) `1653`
- [ ] [3015. 按距离统计房屋对数目 I](https://leetcode.cn/problems/count-the-number-of-houses-at-a-certain-distance-i/) `1658`

### 拓扑排序（3 题）

- [ ] [287. 寻找重复数](https://leetcode.cn/problems/find-the-duplicate-number/) **[HOT100]**
- [ ] [2115. 从给定原材料中找到所有可以做出的菜](https://leetcode.cn/problems/find-all-possible-recipes-from-given-supplies/) `1679`
- [ ] [2359. 找到离给定两个节点最近的节点](https://leetcode.cn/problems/find-closest-node-to-given-two-nodes/) `1715`

### 最短路（3 题）

- [ ] [1462. 课程表 IV](https://leetcode.cn/problems/course-schedule-iv/) `1693`
- [ ] [3341. 到达最后一个房间的最少时间 I](https://leetcode.cn/problems/find-minimum-time-to-reach-last-room-i/) `1721`
- [ ] [3112. 访问消失节点的最少时间](https://leetcode.cn/problems/minimum-time-to-visit-disappearing-nodes/) `1757`

### 其他（2 题）

- [ ] [785. 判断二分图](https://leetcode.cn/problems/is-graph-bipartite/) `1625`
- [ ] [1042. 不邻接植花](https://leetcode.cn/problems/flower-planting-with-no-adjacent/) `1712`

### 网络流（1 题）

- [ ] [1947. 最大兼容性评分和](https://leetcode.cn/problems/maximum-compatibility-score-sum/) `1704`

---

## 7. 动态规划（35 题，HOT100 19 题）

### 其他（20 题）

- [ ] [64. 最小路径和](https://leetcode.cn/problems/minimum-path-sum/) **[HOT100]**
- [ ] [62. 不同路径](https://leetcode.cn/problems/unique-paths/) **[HOT100]**
- [ ] [1143. 最长公共子序列](https://leetcode.cn/problems/longest-common-subsequence/) **[HOT100]**
- [ ] [72. 编辑距离](https://leetcode.cn/problems/edit-distance/) **[HOT100]**
- [ ] [300. 最长递增子序列](https://leetcode.cn/problems/longest-increasing-subsequence/) **[HOT100]**
- [ ] [32. 最长有效括号](https://leetcode.cn/problems/longest-valid-parentheses/) **[HOT100]**
- [ ] [238. 除了自身以外数组的乘积](https://leetcode.cn/problems/product-of-array-except-self/) **[HOT100]**
- [ ] [1991. 找到数组的中间位置](https://leetcode.cn/problems/find-the-middle-index-in-array/) `724`
- [ ] [2574. 左右元素和的差值](https://leetcode.cn/problems/left-and-right-sum-differences/) `1206`
- [ ] [3707. 相等子字符串分数](https://leetcode.cn/problems/equal-score-substrings/) `1262`
- [ ] [3912. 数组中的有效元素](https://leetcode.cn/problems/valid-elements-in-an-array/) `1273`
- [ ] [3788. 分割的最大得分](https://leetcode.cn/problems/maximum-score-of-a-split/) `1306`
- [ ] [2270. 分割数组的方案数](https://leetcode.cn/problems/number-of-ways-to-split-array/) `1334`
- [ ] [3904. 最小稳定下标 II](https://leetcode.cn/problems/smallest-stable-index-ii/) `1352`
- [ ] [2256. 最小平均差](https://leetcode.cn/problems/minimum-average-difference/) `1395`
- [ ] [845. 数组中的最长山脉](https://leetcode.cn/problems/longest-mountain-in-array/) `1437`
- [ ] [3147. 从魔法师身上吸取的最大能量](https://leetcode.cn/problems/taking-maximum-energy-from-the-mystic-dungeon/) `1460`
- [ ] [2012. 数组美丽值求和](https://leetcode.cn/problems/sum-of-beauty-in-the-array/) `1468`
- [ ] [2909. 元素和最小的山形三元组 II](https://leetcode.cn/problems/minimum-sum-of-mountain-triplets-ii/) `1479`
- [ ] [2501. 数组中最长的方波](https://leetcode.cn/problems/longest-square-streak-in-an-array/) `1480`

### DP入门（6 题）

- [ ] [70. 爬楼梯](https://leetcode.cn/problems/climbing-stairs/) **[HOT100]**
- [ ] [198. 打家劫舍](https://leetcode.cn/problems/house-robber/) **[HOT100]**
- [ ] [121. 买卖股票的最佳时机](https://leetcode.cn/problems/best-time-to-buy-and-sell-stock/) **[HOT100]**
- [ ] [53. 最大子数组和](https://leetcode.cn/problems/maximum-subarray/) **[HOT100]**
- [ ] [152. 乘积最大子数组](https://leetcode.cn/problems/maximum-product-subarray/) **[HOT100]**
- [ ] [2606. 找到最大开销的子字符串](https://leetcode.cn/problems/find-the-substring-with-maximum-cost/) `1422`

### 背包DP（3 题）

- [ ] [416. 分割等和子集](https://leetcode.cn/problems/partition-equal-subset-sum/) **[HOT100]**
- [ ] [322. 零钱兑换](https://leetcode.cn/problems/coin-change/) **[HOT100]**
- [ ] [279. 完全平方数](https://leetcode.cn/problems/perfect-squares/) **[HOT100]**

### 区间DP（2 题）

- [ ] [5. 最长回文子串](https://leetcode.cn/problems/longest-palindromic-substring/) **[HOT100]**
- [ ] [546. 移除盒子](https://leetcode.cn/problems/remove-boxes/) `1107`

### 树形DP（2 题）

- [ ] [543. 二叉树的直径](https://leetcode.cn/problems/diameter-of-binary-tree/) **[HOT100]**
- [ ] [124. 二叉树中的最大路径和](https://leetcode.cn/problems/binary-tree-maximum-path-sum/) **[HOT100]**

### 划分DP（1 题）

- [ ] [139. 单词拆分](https://leetcode.cn/problems/word-break/) **[HOT100]**

### 博弈DP（1 题）

- [ ] [1025. 除数博弈](https://leetcode.cn/problems/divisor-game/) `1435`

---

## 8. 常用数据结构（30 题，HOT100 12 题）

### 其他（9 题）

- [ ] [155. 最小栈](https://leetcode.cn/problems/min-stack/) **[HOT100]**
- [ ] [20. 有效的括号](https://leetcode.cn/problems/valid-parentheses/) **[HOT100]**
- [ ] [394. 字符串解码](https://leetcode.cn/problems/decode-string/) **[HOT100]**
- [ ] [146. LRU 缓存](https://leetcode.cn/problems/lru-cache/) **[HOT100]**
- [ ] [1441. 用栈操作构建数组](https://leetcode.cn/problems/build-an-array-with-stack-operations/) `1180`
- [ ] [844. 比较含退格的字符串](https://leetcode.cn/problems/backspace-string-compare/) `1228`
- [ ] [921. 使括号有效的最少添加](https://leetcode.cn/problems/minimum-add-to-make-parentheses-valid/) `1242`
- [ ] [2696. 删除子串后的字符串最小长度](https://leetcode.cn/problems/minimum-string-length-after-removing-substrings/) `1282`
- [ ] [1047. 删除字符串中的所有相邻重复项](https://leetcode.cn/problems/remove-all-adjacent-duplicates-in-string/) `1286`

### 枚举技巧（6 题）

- [ ] [1. 两数之和](https://leetcode.cn/problems/two-sum/) **[HOT100]**
- [ ] [3185. 构成整天的下标对数目 II](https://leetcode.cn/problems/count-pairs-that-form-a-complete-day-ii/) `1010`
- [ ] [1512. 好数对的数目](https://leetcode.cn/problems/number-of-good-pairs/) `1161`
- [ ] [2441. 与对应负数同时存在的最大正整数](https://leetcode.cn/problems/largest-positive-integer-that-exists-with-its-negative/) `1168`
- [ ] [2016. 增量元素之间的最大差值](https://leetcode.cn/problems/maximum-difference-between-increasing-elements/) `1246`
- [ ] [3880. 两个值之间的最小绝对差值](https://leetcode.cn/problems/minimum-absolute-difference-between-two-values/) `1257`

### 堆（5 题）

- [ ] [23. 合并 K 个升序链表](https://leetcode.cn/problems/merge-k-sorted-lists/) **[HOT100]**
- [ ] [295. 数据流的中位数](https://leetcode.cn/problems/find-median-from-data-stream/) **[HOT100]**
- [ ] [1046. 最后一块石头的重量](https://leetcode.cn/problems/last-stone-weight/) `1173`
- [ ] [3264. K 次乘运算后的最终数组 I](https://leetcode.cn/problems/final-array-state-after-k-multiplication-operations-i/) `1178`
- [ ] [2558. 从数量最多的堆取走礼物](https://leetcode.cn/problems/take-gifts-from-the-richest-pile/) `1277`

### 前缀和（4 题）

- [ ] [560. 和为 K 的子数组](https://leetcode.cn/problems/subarray-sum-equals-k/) **[HOT100]**
- [ ] [437. 路径总和 III](https://leetcode.cn/problems/path-sum-iii/) **[HOT100]**
- [ ] [523. 连续的子数组和](https://leetcode.cn/problems/continuous-subarray-sum/) `974`
- [ ] [1523. 在区间范围内统计奇数数目](https://leetcode.cn/problems/count-odd-numbers-in-an-interval-range/) `1209`

### 差分（3 题）

- [ ] [56. 合并区间](https://leetcode.cn/problems/merge-intervals/) **[HOT100]**
- [ ] [2848. 与车相交的点](https://leetcode.cn/problems/points-that-intersect-with-cars/) `1230`
- [ ] [1893. 检查是否区域内所有整数都被覆盖](https://leetcode.cn/problems/check-if-all-the-integers-in-a-range-are-covered/) `1307`

### 字典树（1 题）

- [ ] [208. 实现 Trie (前缀树)](https://leetcode.cn/problems/implement-trie-prefix-tree/) **[HOT100]**

### 并查集（1 题）

- [ ] [3873. 添加一个点后可激活的最大点数](https://leetcode.cn/problems/maximum-points-activated-with-one-addition/) `947`

### 队列（1 题）

- [ ] [239. 滑动窗口最大值](https://leetcode.cn/problems/sliding-window-maximum/) **[HOT100]**

---

## 9. 数学算法（12 题，HOT100 1 题）

### 数论（9 题）

- [ ] [3790. 最小全 1 倍数](https://leetcode.cn/problems/smallest-all-ones-multiple/) `1015`
- [ ] [2413. 最小偶倍数](https://leetcode.cn/problems/smallest-even-multiple/) `1145`
- [ ] [2427. 公因子的数目](https://leetcode.cn/problems/number-of-common-factors/) `1172`
- [ ] [1979. 找出数组的最大公约数](https://leetcode.cn/problems/find-greatest-common-divisor-of-array/) `1184`
- [ ] [1952. 三除数](https://leetcode.cn/problems/three-divisors/) `1204`
- [ ] [3658. 奇数和与偶数和的最大公约数](https://leetcode.cn/problems/gcd-of-odd-and-even-sums/) `1220`
- [ ] [3618. 根据质数下标分割数组](https://leetcode.cn/problems/split-array-by-prime-indices/) `1227`
- [ ] [1492. n 的第 k 个因子](https://leetcode.cn/problems/the-kth-factor-of-n/) `1232`
- [ ] [3591. 检查元素频次是否为质数](https://leetcode.cn/problems/check-if-any-element-has-prime-frequency/) `1235`

### 其他（1 题）

- [ ] [169. 多数元素](https://leetcode.cn/problems/majority-element/) **[HOT100]**

### 计算几何（1 题）

- [ ] [1232. 缀点成线](https://leetcode.cn/problems/check-if-it-is-a-straight-line/) `1247`

### 随机算法（1 题）

- [ ] [961. 在长度 2N 的数组中找出重复 N 次的元素](https://leetcode.cn/problems/n-repeated-element-in-size-2n-array/) `1162`

---

## 10. 贪心与思维（18 题，HOT100 4 题）

### 基本贪心策略（6 题）

- [ ] [3074. 重新分装苹果](https://leetcode.cn/problems/apple-redistribution-into-boxes/) `1198`
- [ ] [3545. 不同字符数量最多为 K 时的最少删除数](https://leetcode.cn/problems/minimum-deletions-for-at-most-k-distinct-characters/) `1211`
- [ ] [3745. 三元素表达式的最大值](https://leetcode.cn/problems/maximize-expression-of-three-elements/) `1218`
- [ ] [1221. 分割平衡字符串](https://leetcode.cn/problems/split-a-string-in-balanced-strings/) `1220`
- [ ] [3402. 使每一列严格递增的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-make-columns-strictly-increasing/) `1246`
- [ ] [2279. 装满石头的背包的最大数量](https://leetcode.cn/problems/maximum-bags-with-full-capacity-of-rocks/) `1249`

### 思维题（5 题）

- [ ] [49. 字母异位词分组](https://leetcode.cn/problems/group-anagrams/) **[HOT100]**
- [ ] [3428. 最多 K 个元素的子序列的最值之和](https://leetcode.cn/problems/maximum-and-minimum-sums-of-at-most-size-k-subsequences/) `891`
- [ ] [2733. 既不是最小值也不是最大值](https://leetcode.cn/problems/neither-minimum-nor-maximum/) `1148`
- [ ] [3432. 统计元素和差值为偶数的分区方案](https://leetcode.cn/problems/count-partitions-with-even-sum-difference/) `1200`
- [ ] [3875. 构造奇偶一致的数组 I](https://leetcode.cn/problems/construct-uniform-parity-array-i/) `1200`

### 区间贪心（4 题）

- [ ] [55. 跳跃游戏](https://leetcode.cn/problems/jump-game/) **[HOT100]**
- [ ] [763. 划分字母区间](https://leetcode.cn/problems/partition-labels/) **[HOT100]** `1443`
- [ ] [45. 跳跃游戏 II](https://leetcode.cn/problems/jump-game-ii/) **[HOT100]** `1700`
- [ ] [646. 最长数对链](https://leetcode.cn/problems/maximum-length-of-pair-chain/) `435`

### 字典序贪心（2 题）

- [ ] [1323. 6 和 9 组成的最大数字](https://leetcode.cn/problems/maximum-69-number/) `1194`
- [ ] [3216. 交换后字典序最小的字符串](https://leetcode.cn/problems/lexicographically-smallest-string-after-a-swap/) `1243`

### 构造（1 题）

- [ ] [1304. 和为零的 N 个不同整数](https://leetcode.cn/problems/find-n-unique-integers-sum-up-to-zero/) `1167`

---

## 11. 链表、树与回溯（33 题，HOT100 33 题）

### DFS遍历（10 题）

- [ ] [94. 二叉树的中序遍历](https://leetcode.cn/problems/binary-tree-inorder-traversal/) **[HOT100]**
- [ ] [104. 二叉树的最大深度](https://leetcode.cn/problems/maximum-depth-of-binary-tree/) **[HOT100]**
- [ ] [101. 对称二叉树](https://leetcode.cn/problems/symmetric-tree/) **[HOT100]**
- [ ] [226. 翻转二叉树](https://leetcode.cn/problems/invert-binary-tree/) **[HOT100]**
- [ ] [230. 二叉搜索树中第 K 小的元素](https://leetcode.cn/problems/kth-smallest-element-in-a-bst/) **[HOT100]**
- [ ] [98. 验证二叉搜索树](https://leetcode.cn/problems/validate-binary-search-tree/) **[HOT100]**
- [ ] [108. 将有序数组转换为二叉搜索树](https://leetcode.cn/problems/convert-sorted-array-to-binary-search-tree/) **[HOT100]**
- [ ] [105. 从前序与中序遍历序列构造二叉树](https://leetcode.cn/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) **[HOT100]**
- [ ] [114. 二叉树展开为链表](https://leetcode.cn/problems/flatten-binary-tree-to-linked-list/) **[HOT100]**
- [ ] [215. 数组中的第K个最大元素](https://leetcode.cn/problems/kth-largest-element-in-an-array/) **[HOT100]** `912`

### 前后指针（9 题）

- [ ] [206. 反转链表](https://leetcode.cn/problems/reverse-linked-list/) **[HOT100]**
- [ ] [24. 两两交换链表中的节点](https://leetcode.cn/problems/swap-nodes-in-pairs/) **[HOT100]**
- [ ] [25. K 个一组翻转链表](https://leetcode.cn/problems/reverse-nodes-in-k-group/) **[HOT100]**
- [ ] [19. 删除链表的倒数第 N 个结点](https://leetcode.cn/problems/remove-nth-node-from-end-of-list/) **[HOT100]**
- [ ] [160. 相交链表](https://leetcode.cn/problems/intersection-of-two-linked-lists/) **[HOT100]**
- [ ] [2. 两数相加](https://leetcode.cn/problems/add-two-numbers/) **[HOT100]**
- [ ] [21. 合并两个有序链表](https://leetcode.cn/problems/merge-two-sorted-lists/) **[HOT100]**
- [ ] [148. 排序链表](https://leetcode.cn/problems/sort-list/) **[HOT100]**
- [ ] [138. 随机链表的复制](https://leetcode.cn/problems/copy-list-with-random-pointer/) **[HOT100]**

### 回溯（8 题）

- [ ] [17. 电话号码的字母组合](https://leetcode.cn/problems/letter-combinations-of-a-phone-number/) **[HOT100]**
- [ ] [78. 子集](https://leetcode.cn/problems/subsets/) **[HOT100]**
- [ ] [39. 组合总和](https://leetcode.cn/problems/combination-sum/) **[HOT100]**
- [ ] [131. 分割回文串](https://leetcode.cn/problems/palindrome-partitioning/) **[HOT100]**
- [ ] [22. 括号生成](https://leetcode.cn/problems/generate-parentheses/) **[HOT100]**
- [ ] [46. 全排列](https://leetcode.cn/problems/permutations/) **[HOT100]**
- [ ] [51. N 皇后](https://leetcode.cn/problems/n-queens/) **[HOT100]**
- [ ] [79. 单词搜索](https://leetcode.cn/problems/word-search/) **[HOT100]**

### 快慢指针（3 题）

- [ ] [234. 回文链表](https://leetcode.cn/problems/palindrome-linked-list/) **[HOT100]**
- [ ] [141. 环形链表](https://leetcode.cn/problems/linked-list-cycle/) **[HOT100]**
- [ ] [142. 环形链表 II](https://leetcode.cn/problems/linked-list-cycle-ii/) **[HOT100]**

### BFS遍历（2 题）

- [ ] [199. 二叉树的右视图](https://leetcode.cn/problems/binary-tree-right-side-view/) **[HOT100]**
- [ ] [102. 二叉树的层序遍历](https://leetcode.cn/problems/binary-tree-level-order-traversal/) **[HOT100]**

### LCA（1 题）

- [ ] [236. 二叉树的最近公共祖先](https://leetcode.cn/problems/lowest-common-ancestor-of-a-binary-tree/) **[HOT100]**

---

## 12. 字符串（10 题，HOT100 0 题）

### KMP（4 题）

- [ ] [1392. 最长快乐前缀](https://leetcode.cn/problems/longest-happy-prefix/) `1876`
- [ ] [3036. 匹配模式数组的子数组数目 II](https://leetcode.cn/problems/number-of-subarrays-that-match-a-pattern-ii/) `1895`
- [ ] [3008. 找出数组中的美丽下标 II](https://leetcode.cn/problems/find-beautiful-indices-in-the-given-array-ii/) `2016`
- [ ] [3529. 统计水平子串和垂直子串重叠格子的数目](https://leetcode.cn/problems/count-cells-in-overlapping-horizontal-and-vertical-substrings/) `2105`

### 其他（2 题）

- [ ] [1032. 字符流](https://leetcode.cn/problems/stream-of-characters/) `1970`
- [ ] [2430. 对字母串可执行的最大删除数](https://leetcode.cn/problems/maximum-deletions-on-a-string/) `2102`

### Manacher（1 题）

- [ ] [2472. 不重叠回文子字符串的最大数目](https://leetcode.cn/problems/maximum-number-of-non-overlapping-palindrome-substrings/) `2013`

### 后缀数组（1 题）

- [ ] [1163. 按字典序排在最后的子串](https://leetcode.cn/problems/last-substring-in-lexicographical-order/) `1864`

### 子序列自动机（1 题）

- [ ] [792. 匹配子序列的单词数](https://leetcode.cn/problems/number-of-matching-subsequences/) `1695`

### 字符串哈希（1 题）

- [ ] [1316. 不同的循环子字符串](https://leetcode.cn/problems/distinct-echo-substrings/) `1837`

---

## 参考资料

- [灵茶山艾府：如何科学刷题？](https://leetcode.cn/discuss/post/3141566/ru-he-ke-xue-shua-ti-by-endlesscheng-q3yd/)
- [LeetCode HOT 100](https://leetcode.cn/studyplan/top-100-liked/)

> 最后更新：2026-07-04