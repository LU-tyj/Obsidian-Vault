---
title: "射线与AABB相交"
category: 算法手撕高频题
tags: [算法, 手撕代码, 几何, 图形学, 网易互娱]
frequency: ⭐
difficulty: 中等
companies: [网易雷火]
status: new
last_reviewed: 
next_review: 
related:
  - "[[点在三角形内判断]]"
  - "[[图算法与A星寻路]]"
---

## 🎯 一句话结论（自测用）
> Slab 方法（Kay-Kajiya）：分别计算射线与 AABB 三个轴对齐面的 t 区间 `[t_min, t_max]`，取所有 `t_min` 的最大值和所有 `t_max` 的最小值。若 `t_min <= t_max` 且 `t_max >= 0` 则相交。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **AABB（轴对齐包围盒）**：由 `(minX,minY,minZ)` 和 `(maxX,maxY,maxZ)` 定义
2. **Slab 方法原理**：射线与 AABB 相交 = 射线同时处于三个轴对齐面对之间的时间段
3. **算法步骤**：
   - 对每个轴：计算射线与两个边界平面的 t 值
   - 若方向分量为 0：射线与该轴平行，检查原点是否在区间内
   - 否则：`t1 = (min - origin) / dir`，`t2 = (max - origin) / dir`
   - 记录 `t_min = max(min(t1,t2))`，`t_max = min(max(t1,t2))`
4. 若 `t_min <= t_max` 且 `t_max >= 0` 则相交

## 🔍 详细解析

### C++ 标准实现（Slab 方法）
```cpp
struct Vec3 { float x, y, z; };
struct Ray { Vec3 origin, direction; };
struct AABB { Vec3 min, max; };

bool rayAABBIntersect(Ray ray, AABB aabb, float& t) {
    float tmin = -INFINITY, tmax = INFINITY;
    
    // 对每个轴（x, y, z）
    for (int i = 0; i < 3; i++) {
        float origin = (&ray.origin.x)[i];
        float dir = (&ray.direction.x)[i];
        float boxMin = (&aabb.min.x)[i];
        float boxMax = (&aabb.max.x)[i];
        
        if (abs(dir) < 1e-6f) {
            // 射线与该轴平行
            if (origin < boxMin || origin > boxMax)
                return false;  // 原点不在区间内，不相交
        } else {
            float invDir = 1.0f / dir;
            float t1 = (boxMin - origin) * invDir;
            float t2 = (boxMax - origin) * invDir;
            if (t1 > t2) swap(t1, t2);  // 保证 t1 <= t2
            
            tmin = max(tmin, t1);  // 进入所有面的最晚时刻
            tmax = min(tmax, t2);  // 离开任意面的最早时刻
            
            if (tmin > tmax) return false;  // 交集为空
        }
    }
    
    t = tmin;  // 返回交点距离
    return tmax >= 0;  // 相交点在射线前方
}
```

### 更清晰的版本
```cpp
bool rayAABBIntersect(Ray ray, AABB aabb, float& tNear, float& tFar) {
    float tMinX, tMaxX, tMinY, tMaxY, tMinZ, tMaxZ;
    
    // X 轴
    if (abs(ray.direction.x) < 1e-6f) {
        if (ray.origin.x < aabb.min.x || ray.origin.x > aabb.max.x)
            return false;
    } else {
        float invDx = 1.0f / ray.direction.x;
        tMinX = (aabb.min.x - ray.origin.x) * invDx;
        tMaxX = (aabb.max.x - ray.origin.x) * invDx;
        if (tMinX > tMaxX) swap(tMinX, tMaxX);
    }
    
    // Y 轴（同理）
    // Z 轴（同理）
    
    // 取交集
    tNear = max({tMinX, tMinY, tMinZ});
    tFar = min({tMaxX, tMaxY, tMaxZ});
    
    return tNear <= tFar && tFar >= 0;
}
```

### Csharp / Unity 版本
```csharp
using UnityEngine;

public static bool RayAABBIntersect(Ray ray, Bounds bounds, out float distance)
{
    distance = 0f;
    Vector3 invDir = new(
        1f / ray.direction.x,
        1f / ray.direction.y,
        1f / ray.direction.z
    );

    Vector3 t1 = Vector3.Scale(bounds.min - ray.origin, invDir);
    Vector3 t2 = Vector3.Scale(bounds.max - ray.origin, invDir);

    float tMin = Mathf.Max(Mathf.Min(t1.x, t2.x), Mathf.Min(t1.y, t2.y), Mathf.Min(t1.z, t2.z));
    float tMax = Mathf.Min(Mathf.Max(t1.x, t2.x), Mathf.Max(t1.y, t2.y), Mathf.Max(t1.z, t2.z));

    if (tMin <= tMax && tMax >= 0)
    {
        distance = tMin >= 0 ? tMin : tMax;
        return true;
    }
    return false;
}
```

### 面试中可能问的扩展
**射线与球相交**：
```cpp
bool raySphereIntersect(Ray ray, Vec3 center, float radius, float& t) {
    Vec3 oc = ray.origin - center;
    float a = dot(ray.direction, ray.direction);
    float b = 2.0f * dot(oc, ray.direction);
    float c = dot(oc, oc) - radius * radius;
    float disc = b * b - 4 * a * c;
    if (disc < 0) return false;
    t = (-b - sqrt(disc)) / (2.0f * a);
    return t >= 0;
}
```

### 为什么用 Slab 方法？
- Slab 方法对 AABB 效率最优（O(1)，只涉及简单的 min/max 运算）
- 相比使用 GJK 等通用算法，Slab 利用了 AABB 的轴对齐特性
- 广泛用于 BVH（包围盒层级结构）中的射线检测

### 面试追问：BVH 中如何用 AABB 加速射线检测？
```cpp
// BVH 节点
struct BVHNode {
    AABB bounds;
    BVHNode* left;
    BVHNode* right;
    // ... 三角形数据
};

void rayBVHTraverse(Ray ray, BVHNode* node) {
    float t;
    if (!rayAABBIntersect(ray, node->bounds, t)) return;  // 未命中包围盒
    if (t > currentClosest) return;  // 已找到更近的交点
    
    if (node->isLeaf()) {
        // 与节点内所有三角形检测
        for (auto& tri : node->triangles)
            intersectTriangle(ray, tri);
    } else {
        rayBVHTraverse(ray, node->left);
        rayBVHTraverse(ray, node->right);
    }
}
```

## 💬 面试官常见追问
- "Slab 方法的原理是什么？" -> 把问题分成三个一维 interval 求交，3D 相交 = 三个 1D interval 同时相交
- "如果射线原点在 AABB 内部怎么办？" -> t_min 会 < 0，t_max > 0，依然相交。取 t_max 作为交点
- "优化方向？" -> 对方向分量平行的轴提前返回 false，用 SIMD 同时计算三个轴

## ⚠️ 我曾经的误区 / 网上常见错答
- **误区**：忘了处理方向分量为 0（除零）。需要用 `abs(dir) < epsilon` 判断，而不是 `dir == 0`
- **误区**：`t1` 和 `t2` 不保证 `t1 <= t2`。因为方向可能为负，`(min-origin)/dir > (max-origin)/dir` 可能成立
- **误区**：只检查 `t_min <= t_max`，没检查 `t_max >= 0`。如果 `t_max < 0` 表示交点在射线背后

## 🔗 关联知识点
- [[点在三角形内判断]]
- [[图算法与A星寻路]]

## 📎 原始出处
- 005_雷火 Q27: 射线与 AABB 相交（代码实现）
