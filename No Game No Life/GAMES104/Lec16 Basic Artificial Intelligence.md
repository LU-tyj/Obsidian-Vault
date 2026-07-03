## 1 Navigation
Steps: Map Representation -> Path Finding -> Path Smoothing

### 1.1 Map Representation
建立 walkable area，通过设置 Physical Collision、Climbing height、Jumping distance

方法一：Waypoint Network，创造一个路点网络，像坐地铁一样，从点到点。缺点是太固定了
方法二：用Grid来表达，把walkable area用格子来覆盖。使用简单，更新容易。但难以处理3D地图，占用大的存储空间。
方法三：Navigation Mesh，现在大部分方法。用凸多边形覆盖所有的可行走区域。但缺点是复杂的生成算法，以及不能适应 3D 空间（无人机在天上飞）
方法四：Sparse Voxel Octree，用八叉树细分空间

### 1.2 Path Finding
不论怎么表达walkable area，都是找到中心点，然后变成WayPoint Network。所有的寻路问题都是：知道起点终点，知道Network中间各个点的距离，去找到能否到达终点以及少走路。
>但在游戏中为了真实性，可能不会采用最优解

这些就是cs61b中所讲过的内容了。
主要是 A* 算法

### 1.3 Path Smoothing
在找到路径后，如何优化路径，使其走起来更加自然。
使用Funnel Algorithm。有种像视锥，然后看，找最短，如果看到终点，就直接到达。
![[Funnel Algorithm.png]]