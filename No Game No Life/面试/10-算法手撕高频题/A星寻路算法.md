---
title: "A星寻路算法"
category: 算法手撕高频题
tags: [算法, 手撕代码, A*, 寻路, 游戏开发, 网易互娱]
frequency: ⭐⭐
difficulty: 较难
companies: [网易互娱, 网易雷火]
status: new
last_reviewed: 
next_review: 
related:
  - "[[图算法与A星寻路]]"
  - "[[点在三角形内判断]]"
  - "[[射线与AABB相交]]"
---

## 🎯 一句话结论（自测用）
> `F = G + H`。Open List（待探索）用最小堆按 F 排序，Closed List（已探索）用哈希表。每次取 F 最小的节点拓展，找到终点后回溯父节点得路径。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **核心公式**：`F = G + H`。G=起点到当前实际代价，H=当前到终点启发式估计（曼哈顿/欧几里得）
2. 起点入 Open List（最小堆），F=H
3. 循环：取出 Open List 中 F 最小的节点 -> 是终点则回溯路径 -> 不是则遍历邻居
4. 邻居不在 Closed List 中：算新 G，若更优则更新 F/G/H/父节点，放入 Open List
5. Open List 为空仍未找到 -> 不可达
6. 启发式必须可接受（admissible，不高估），否则不一定最优

## 🔍 详细解析

### C++ 完整实现
```cpp
struct Node {
    int x, y;
    int g, h;       // g: 起点到当前，h: 当前到终点
    int f() const { return g + h; }
    Node* parent;
    
    // 用于优先队列（小顶堆按 F 排序）
    bool operator>(const Node& other) const { return f() > other.f(); }
};

vector<pair<int,int>> AStar(
    vector<vector<int>>& grid, 
    pair<int,int> start, 
    pair<int,int> end) 
{
    int rows = grid.size(), cols = grid[0].size();
    
    // 8 方向（或 4 方向）
    int dx[] = {-1,-1,-1, 0,0, 1,1,1};
    int dy[] = {-1, 0, 1,-1,1,-1,0,1};
    
    // 启发式函数：曼哈顿距离 / 欧几里得距离
    auto heuristic = [&](int x, int y) {
        // 曼哈顿（适用于 4 方向移动）
        return abs(x - end.first) + abs(y - end.second);
        // 欧几里得（适用于 8 方向移动）
        // return sqrt(pow(x-end.first,2) + pow(y-end.second,2));
    };
    
    // Open List: 优先队列（小顶堆）
    priority_queue<Node, vector<Node>, greater<Node>> openList;
    // 记录每个节点的最优 G 值
    vector<vector<int>> bestG(rows, vector<int>(cols, INT_MAX));
    // 存储所有动态分配的 Node（简化内存管理）
    vector<vector<Node*>> nodeMap(rows, vector<Node*>(cols, nullptr));
    
    // 起点
    auto startNode = new Node{start.first, start.second, 0, 0, nullptr};
    startNode->h = heuristic(start.first, start.second);
    startNode->parent = nullptr;
    bestG[start.first][start.second] = 0;
    nodeMap[start.first][start.second] = startNode;
    openList.push(*startNode);
    
    Node* endNode = nullptr;
    
    while (!openList.empty()) {
        Node current = openList.top();
        openList.pop();
        
        // 跳过已被更新的过时记录
        if (current.g > bestG[current.x][current.y]) continue;
        
        if (current.x == end.first && current.y == end.second) {
            endNode = nodeMap[current.x][current.y];
            break;
        }
        
        for (int k = 0; k < 8; k++) {
            int nx = current.x + dx[k];
            int ny = current.y + dy[k];
            
            // 边界检查 + 障碍检查
            if (nx < 0 || nx >= rows || ny < 0 || ny >= cols || grid[nx][ny] == 1)
                continue;
            
            // 对角线移动检查（防止穿墙）
            if (dx[k] != 0 && dy[k] != 0) {
                if (grid[current.x + dx[k]][current.y] == 1 ||
                    grid[current.x][current.y + dy[k]] == 1)
                    continue;
            }
            
            int moveCost = (dx[k] != 0 && dy[k] != 0) ? 14 : 10;  // 对角线代价
            int newG = current.g + moveCost;
            
            if (newG < bestG[nx][ny]) {
                bestG[nx][ny] = newG;
                if (!nodeMap[nx][ny])
                    nodeMap[nx][ny] = new Node{nx, ny, 0, 0, nullptr};
                auto neighbor = nodeMap[nx][ny];
                neighbor->g = newG;
                neighbor->h = heuristic(nx, ny);
                neighbor->parent = nodeMap[current.x][current.y];
                openList.push(*neighbor);
            }
        }
    }
    
    // 回溯路径
    vector<pair<int,int>> path;
    while (endNode) {
        path.push_back({endNode->x, endNode->y});
        endNode = endNode->parent;
    }
    reverse(path.begin(), path.end());
    
    return path;
}
```

### Csharp / Unity 核心逻辑
```csharp
public class AStarNode : IComparable<AStarNode>
{
    public int x, y;
    public int g, h;
    public int F => g + h;
    public AStarNode parent;
    
    public int CompareTo(AStarNode other) => F.CompareTo(other.F);
}

public List<Vector2Int> AStar(int[,] grid, Vector2Int start, Vector2Int end)
{
    var openList = new SortedSet<AStarNode>();  // 或 PriorityQueue
    var closedSet = new HashSet<Vector2Int>();
    var nodeMap = new Dictionary<Vector2Int, AStarNode>();
    
    int Heuristic(Vector2Int a, Vector2Int b)
        => Mathf.Abs(a.x - b.x) + Mathf.Abs(a.y - b.y);
    
    var startNode = new AStarNode { x = start.x, y = start.y, h = Heuristic(start, end) };
    openList.Add(startNode);
    nodeMap[start] = startNode;
    
    while (openList.Count > 0)
    {
        var current = openList.Min;
        openList.Remove(current);
        
        if (current.x == end.x && current.y == end.y)
            return ReconstructPath(current);
        
        closedSet.Add(new Vector2Int(current.x, current.y));
        
        // 遍历 8 个邻居（同上逻辑）
        // ...
    }
    
    return null;  // 不可达
}
```

### A* 寻路 vs Dijkstra vs BFS 代码对比
```cpp
// BFS：无权图最短路径（仅靠队列）
void BFS(Graph& g, int start) {
    queue<int> q;
    vector<bool> visited(g.size());
    q.push(start); visited[start] = true;
    while (!q.empty()) {
        int v = q.front(); q.pop();
        for (int u : g[v]) {
            if (!visited[u]) { visited[u] = true; q.push(u); }
        }
    }
}

// Dijkstra：加权图最短路径（优先队列按 G 排序）
void Dijkstra(Graph& g, int start) {
    priority_queue<pair<int,int>, vector<pair<int,int>>, greater<>> pq;
    vector<int> dist(g.size(), INF);
    pq.push({0, start}); dist[start] = 0;
    while (!pq.empty()) {
        auto [d, v] = pq.top(); pq.pop();
        if (d > dist[v]) continue;
        for (auto [u, w] : g[v]) {
            if (dist[u] > dist[v] + w) {
                dist[u] = dist[v] + w;
                pq.push({dist[u], u});
            }
        }
    }
}

// A*：在 Dijkstra 基础上加启发式 F = G + H
// 唯一区别：pq 按 G+H 排序而不是仅按 G
```

### 面试要点速查
| 概念 | 说明 |
|------|------|
| F = G + H | 总代价 = 已走 + 预估 |
| G | 起点到当前的实际距离（准确值） |
| H | 当前到终点的启发式估计（必须不高估） |
| Open List | 待探索节点，用最小堆/优先队列 |
| Closed List | 已探索节点，用哈希表 |
| 启发式 | 曼哈顿（4方向）、欧几里得（8方向）、对角线 |
| 时间复杂度 | O(E)，但启发式好时接近 O(V) |

## 💬 面试官常见追问
- "H 很高估会怎样？" -> 不一定找到最短路径，但可能更快（牺牲最优性换速度）
- "A* 和 JPS（Jump Point Search）的区别？" -> JPS 是 A* 的优化，跳过无用的中间节点直接跳到"关键点"，适合均匀网格
- "如何处理动态障碍物？" -> 检测到碰撞后从当前位置重新 A*（局部重规划），或用 D* Lite 增量更新
- "Open List 用什么数据结构最优？" -> 二叉堆（标准）、斐波那契堆（理论上更快但常数大）、分桶队列（当 F 值范围有限时）

## ⚠️ 我曾经的误区 / 网上常见错答
- **误区**：只用 G 排 Open List。A* 的核心是用 F=G+H，只用 G 就是 Dijkstra
- **误区**：忘记处理过时节点。当节点的 G 值被更新后，旧记录还在优先队列中，取出时需检查 `g > bestG`
- **误区**：对角线移动时没检查"穿墙"。两个对角线相邻的格子如果都是墙仍可能穿过（需同时检查两个方向的邻居是否为墙）

## 🔗 关联知识点
- [[图算法与A星寻路]]
- [[点在三角形内判断]]
- [[射线与AABB相交]]

## 📎 原始出处
- GitHub Q7-Q12: A* 算法原理、数据结构、完整流程、Dijkstra 对比
- BOSS 七: 二面问 A* 寻路算法
- 博客园 面经3: 塞尔达拼装 + Tilemap拼接 + A*寻路
