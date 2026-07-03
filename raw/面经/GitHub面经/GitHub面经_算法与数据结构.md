---
source_platform: GitHub
source_url:
  - https://github.com/unitykit/unityClientInterviewGuide
  - https://github.com/Lafree317/Unity-InterviewQuestion
crawl_date: 2026-07-03
crawl_agent: agent-github
company_mentioned: [通用, 网易互娱]
position: Unity客户端开发
raw: true
---

# 算法与数据结构面试题

## 一、排序算法

### Q1: 十大排序算法的复杂度与稳定性？

| 排序算法 | 平均时间复杂度 | 稳定性 |
|---------|----------------|--------|
| 冒泡排序 | O(n^2) | 稳定 |
| 选择排序 | O(n^2) | 不稳定 |
| 插入排序 | O(n^2) | 稳定 |
| 希尔排序 | O(n log n) | 不稳定 |
| 归并排序 | O(n log n) | 稳定 |
| 快速排序 | O(n log n) | 不稳定 |
| 堆排序 | O(n log n) | 不稳定 |
| 计数排序 | O(n+k) | 稳定 |
| 桶排序 | O(n+k) | 稳定 |
| 基数排序 | O(n*k) | 稳定 |

### Q2: 不稳定的排序算法有哪些？
选择排序、快速排序、堆排序、希尔排序

### Q3: 基本有序时选什么排序？
插入排序。快速排序在基本有序时可能退化到 O(n^2)

### Q4: 快速排序的空间复杂度？
O(log n)（递归栈深度），不是 O(1)

### Q5: 各排序算法的核心思想？
- **冒泡**: 相邻比较交换，每轮把最大元素"冒"到最后
- **选择**: 每轮选最小放到已排序末尾
- **插入**: 将未排序元素插入已排序序列的合适位置
- **快速**: 选基准，分区，递归排序左右
- **堆排序**: 利用完全二叉树堆结构，不断取堆顶
- **归并**: 分治，将已排序子序列合并

### Q6: 100 万数据选出前 1 万大的数？
**解法**: 小顶堆
- 先拿前 1 万个建堆
- 遍历剩余元素，若大于堆顶则替换并调整堆
- 时间复杂度: O(n log m)，m=10000

---

## 二、A* 寻路算法（核心）

### Q7: A* 算法的原理？

**核心公式**: `F = G + H`
- **F**: 总代价
- **G**: 从起点到当前点的实际距离
- **H**: 当前点到终点的启发式估计距离（常用曼哈顿距离）

### Q8: A* 的数据结构？
- **Open List（开启列表）**: 待评估节点集合
- **Closed List（关闭列表）**: 已评估节点集合
- 优化：使用最小堆/优先队列管理 Open List，每次取 F 最小的节点

### Q9: A* 算法流程？
1. 起点放入 Open List
2. 取 Open List 中 F 值最小的节点 -> 放入 Closed List
3. 检查该节点是否为终点 -> 是则结束
4. 遍历周围可行走节点：
   - 已在 Closed List 或障碍 -> 跳过
   - 不在 Open List -> 加入，计算 F、G、H，设父节点
   - 已在 Open List -> 若新 G 更小则更新
5. 重复步骤 2-4 直到找到终点或 Open List 为空
6. 从终点沿父节点回溯 -> 得到路径

### Q10: 动态障碍如何处理？
- 重新寻路：从当前节点重新执行 A*
- 局部路径修正：只在障碍附近重新规划
- 分层寻路：先粗网格 A*，细节局部调整

### Q11: Dijkstra vs A\* vs BFS/DFS？

| 算法 | 优点 | 缺点 |
|------|------|------|
| BFS | 无权图最短路径 | 遍历全图 |
| DFS | 不遍历全图 | 不一定最优 |
| Dijkstra | 加权图最短路径 | 无方向性，效率低 |
| A\* | 效率高、路径较优 | 需好的启发式函数 |

### Q12: NavMesh 与 A\* 的区别？
- NavMesh: Unity 内置的导航系统，基于多边形/网格的寻路
- A\*: 基于栅格的寻路算法，可自定义实现
- NavMesh 适合复杂地形（如 3D 场景），A\* 适合网格地图

---

## 三、数据结构

### Q13: 数组 vs 链表？

| | 数组 | 链表 |
|--|------|------|
| 内存分配 | 连续内存 | 非连续（堆分配） |
| 随机访问 | O(1) | O(n) |
| 插入/删除 | O(n)（需移动） | O(1)（已知位置） |
| 适用场景 | 频繁查询、固定大小 | 频繁增删、动态大小 |

### Q14: 栈 vs 队列？
- **栈（Stack）**: LIFO（后进先出）-- 函数调用、撤销操作
- **队列（Queue）**: FIFO（先进先出）-- 消息队列、BFS

### Q15: BFS vs DFS？
| | BFS | DFS |
|--|-----|-----|
| 数据结构 | 队列（Queue） | 栈（Stack）/ 递归 |
| 特点 | 按层遍历 | 一路走到黑再回溯 |
| 应用 | 无权图最短路径 | 连通性、拓扑排序 |

### Q16: 哈希冲突解决方法？
1. **链地址法（拉链法）**: 同一哈希值用链表存储
2. **开放地址法**: 冲突后找下一个空位（线性探测、二次探测、双重哈希）
3. **再哈希法**: 使用多个哈希函数
4. **公共溢出区**: 冲突数据放入溢出表

---

## 四、高频手写题

### Q17: 判断整数是否为 2 的 n 次方？
```csharp
public static bool IsPowerOfTwo(int number)
{
    return number > 0 && (number & (number - 1)) == 0;
}
```

### Q18: 求二进制中 1 的个数？
```csharp
int CountOnes(int n)
{
    int count = 0;
    while (n > 0)
    {
        n &= (n - 1);  // 消除最低位的 1
        count++;
    }
    return count;
}
```

### Q19: 斐波那契数列（迭代 vs 递归）？
```csharp
// 迭代（推荐）
static int Fib(int n)
{
    if (n <= 2) return 1;
    int a = 1, b = 1;
    for (int i = 3; i <= n; i++)
    {
        int c = a + b;
        a = b;
        b = c;
    }
    return b;
}
```

### Q20: 判断奇偶数（位运算）？
```csharp
public static bool IsEven(int number) => (number & 1) == 0;
public static bool IsOdd(int number) => (number & 1) == 1;
```

---

## 五、游戏开发特殊算法

### Q21: 游戏中常用的随机算法？
- 普通随机：Random.Range
- 加权随机：使用权重数组 + 累积概率
- 洗牌算法（Fisher-Yates）：生成随机序列

```csharp
// Fisher-Yates 洗牌
void Shuffle<T>(T[] array)
{
    for (int i = array.Length - 1; i > 0; i--)
    {
        int j = Random.Range(0, i + 1);
        (array[i], array[j]) = (array[j], array[i]);
    }
}
```

### Q22: 行为树 vs 状态机？
- 状态机：适合简单的状态切换逻辑
- 行为树：适合复杂的 AI 决策，可复用节点，易于调试

### Q23: 塔防游戏"从几万敌人中选血量最低目标"怎么优化？
- 分帧计算：每帧只计算一部分
- Job System 多线程并行
- 使用堆/优先队列维护最值
- 空间分区（如四叉树）缩小搜索范围
- 距离平方比较（避免开根号）

---

> 来源: unitykit/unityClientInterviewGuide, Lafree317/Unity-InterviewQuestion
