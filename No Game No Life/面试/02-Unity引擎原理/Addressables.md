---
title: "Addressables"
category: Unity引擎原理
tags: [Unity, Csharp, 网易互娱, Addressables, 资源管理]
frequency: ⭐⭐
difficulty: 中等
companies: [网易互娱]
status: new
last_reviewed:
next_review:
related:
  - "[[AssetBundle 机制]]"
  - "[[资源加载方式对比]]"
  - "[[资源卸载与内存管理]]"
---

## 一句话结论（自测用）
> Addressables 是 Unity 官方基于 AssetBundle 的上层资源管理系统，通过地址（Address）而非路径加载资源。核心优势：自动依赖管理、引用计数自动释放、远程更新版本管理。适合中小型项目快速开发。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **Addressables 是什么**：Unity 官方的资源管理系统，基于 AssetBundle，提供地址寻址、异步加载、依赖管理、远程分发等能力。
2. **核心概念**：
   - **Address（地址）**：资源的唯一字符串标识，替代文件路径。如 `"playerPrefab"` 而非 `"Assets/Prefabs/Player.prefab"`
   - **AssetReference**：强类型的资源引用，不直接引用对象，避免加载时全量依赖
   - **AsyncOperationHandle**：异步操作的句柄，用于跟踪加载状态和释放资源
   - **Group（分组）**：资源的逻辑分组，对应底层一个或多个 AssetBundle
3. **加载方式**：
   ```csharp
   // 异步加载（推荐）
   var handle = Addressables.LoadAssetAsync<GameObject>("playerPrefab");
   await handle.Task;
   GameObject player = handle.Result;
   
   // 实例化
   var instanceHandle = Addressables.InstantiateAsync("playerPrefab");
   // 释放
   Addressables.Release(handle);
   Addressables.ReleaseInstance(instanceHandle);
   ```
4. **与 AssetBundle 的关系**：Addressables 底层仍是 AssetBundle，但自动管理了依赖、分组、版本和加载/卸载。

## 详细解析

### AssetBundle vs Addressables 选择指南
| 因素 | AssetBundle | Addressables |
|------|-------------|-------------|
| 开发效率 | 低（手动管理依赖） | 高（自动管理） |
| 控制粒度 | 精细 | 一般 |
| 学习成本 | 高 | 中等 |
| 版本管理 | 手动 | 内置 |
| 适用团队 | 大厂（有成熟工具链） | 中小团队 |
| 性能优化空间 | 大（可深度定制） | 有限 |

### Addressables 的高频考点
1. **异步加载是必须的**：`LoadAssetAsync` 异步加载，`WaitForCompletion()` 同步等待但不推荐
2. **引用计数**：每次 `LoadAssetAsync` 增加引用计数，`Release` 减少；计数归零时资源可被卸载
3. **场景切换**：`Addressables.LoadSceneAsync` 异步加载场景，同时管理场景依赖资源
4. **小 Bundle 过多问题**：元数据膨胀 + 加载次数多 + IO 开销

### Addressables 内存管理
```csharp
// 正确流程：
var handle = Addressables.LoadAssetAsync<Sprite>("icon");
Sprite sprite = handle.Result;
// ... 使用 sprite ...
Addressables.Release(handle); // 释放加载句柄

// 注意：Release 不立即卸载资源，只是减少引用计数
// 调用 Resources.UnloadUnusedAssets() 才会真正释放引用计数为 0 的资源
```

## 面试官常见追问
- Addressables 的依赖怎么管理的？（分析 Asset 引用关系 -> 自动分组 -> 生成 .bundle 依赖图）
- Addressables 和 AssetBundle 可以共存吗？（可以，但通常不混用，增加管理复杂度）
- 为什么推荐 Addressables 异步加载？（避免主线程卡帧，大资源同步加载可导致明显卡顿）
- `AssetReference` 和直接引用的区别？（AssetReference 不加载实际对象，只是存地址字符串，减少内存占用）

## 我曾经的误区 / 网上常见错答
- **错**："Addressables 是 AssetBundle 的替代品" —— 是 AssetBundle 的上层封装，底层还是 AssetBundle
- **错**："Release 后资源立即被释放" —— 只是引用计数减 1，实际释放时机由系统决定
- **错**："Addressables 适合所有项目" —— 需要深度定制资源管理的团队更适合直接用 AssetBundle

## 关联知识点
- [[AssetBundle 机制]]
- [[资源加载方式对比]]
- [[资源卸载与内存管理]]
- [[资源版本管理与热更新资源]]

## 原始出处
- GitHub面经_资源管理 Q8-Q10
- BOSS直聘 面试评价汇总
