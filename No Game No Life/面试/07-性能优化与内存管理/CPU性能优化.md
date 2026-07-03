---
title: "CPU性能优化"
category: 性能优化与内存管理
tags: [性能优化, CPU, Update优化, 脚本优化, 物理优化, 动画优化, 网易互娱]
frequency: ⭐⭐⭐
difficulty: 中等
companies: [网易互娱]
status: new
last_reviewed:
next_review:
related:
  - "[[DrawCall优化与合批策略]]"
  - "[[GC机制与优化]]"
  - "[[Profiler使用与性能瓶颈定位]]"
---

## 🎯 一句话结论（自测用）
> CPU 优化的四大方向：减少 DrawCall（合批/剔除）、降低脚本开销（缓存引用、事件驱动替代 Update）、物理降频（简化碰撞体、降频 FixedUpdate）、动画降频（远处物体降低更新频率、减少 IK 和 Animator 层数）。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **减少 DrawCall**：使用合批/Instancing/遮挡剔除减少 CPU 提交渲染指令的开销。
2. **脚本优化**：
   - 缓存 GetComponent 引用（放在 Awake/Start，不在 Update 中调用）
   - 避免在 Update 中使用 Find、FindObjectOfType
   - 将过度频繁的 Update 改为事件驱动或协程（如 0.5 秒检测一次）
   - 避免在 Update 中使用 foreach（对值类型集合会装箱）
   - 使用 CompareTag 而非 `tag == "xxx"`（字符串比较产生 GC）
3. **物理优化**：减少碰撞体复杂度（用 Box/Sphere 替代 Mesh Collider）、降频 FixedUpdate、使用简单碰撞体、减少 Rigidbody 数量。
4. **动画优化**：远处物体降低 Animator 更新频率、关闭 IK、减少 Animator 层数、使用 Playable API 替代传统 Animator。
5. **10000 个 MonoBehaviour 各自 Update vs 统一管理**：统一管理效率更高，因为减少 Csharp 到 Native 的调用次数。

## 🔍 详细解析

### 为什么 `CompareTag` 比 `tag == "xxx"` 好？
- `tag == "xxx"` 会调用 `tag` 属性的 getter，内部会分配一个新字符串，产生 GC
- `CompareTag` 直接比较内部 tag 索引值（int 比较），不产生内存分配

### 为什么克制使用 `foreach`？
- 在旧版 Mono 中，对值类型集合（如 List<struct>）使用 foreach 会产生装箱
- IL2CPP 下已修复，但仍建议对热路径使用 for 循环保证一致性

### 事件驱动替代 Update
```csharp
// 反例：每帧检测
void Update() {
    if (player.health <= 0) { Die(); }
}

// 正例：事件驱动
void OnEnable() {
    player.OnHealthChanged += CheckDeath;
}
void CheckDeath(int hp) {
    if (hp <= 0) Die();
}
```

### 物理时间步调优
- `Time.fixedDeltaTime` 默认 0.02s（50Hz），调小提高手感但增加 CPU 开销
- 需要确定性的场景（帧同步）统一在 FixedUpdate 施加力/速度
- 渲染插值使用 `Rigidbody.Interpolation` 平滑视觉

## 💬 面试官常见追问
- **为什么 10000 个 MonoBehaviour 每个有 Update 效率低？** → 每个 Update 都是从 C++ 侧通过函数指针回调到托管侧，1 万个调用 = 1 万次跨语言开销；统一管理只需一次调用
- **FindObjectOfType 为什么耗性能？** → 遍历整个场景层级来查找对象，复杂度 O(n)；应缓存引用
- **什么是 Playable API？** → Unity 新一代动画系统，比 Animator 更灵活高效，可创建动画混合图

## ⚠️ 我曾经的误区 / 网上常见错答
- 误区：协程可以替代多线程做并行计算。协程只是分时执行，无法利用多核。
- 误区：把所有逻辑放到 FixedUpdate 就是对的。非物理相关逻辑放 Update 即可。

## 🔗 关联知识点
- [[DrawCall优化与合批策略]]
- [[GC机制与优化]]
- [[Profiler使用与性能瓶颈定位]]

## 📎 原始出处
- GitHub面经_性能优化 Q2/Q3：CPU 优化方向与脚本优化
- "10000 Update calls" Unity 官方博客
- 优化.md：GC/性能瓶颈定位方法
- 多篇牛客网面经：物理优化、动画优化为面试高频追问点
