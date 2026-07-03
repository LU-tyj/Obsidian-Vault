---
title: "Prefab 与 Instantiate"
category: Unity引擎原理
tags: [Unity, Csharp, 网易互娱, Prefab, Instantiate]
frequency: ⭐⭐
difficulty: 简单
companies: [网易互娱]
status: new
last_reviewed:
next_review:
related:
  - "[[Unity 生命周期]]"
  - "[[对象池]]"
  - "[[AssetBundle 机制]]"
---

## 一句话结论（自测用）
> Prefab 是 GameObject 的资产模板，支持批量修改和复用。Instantiate 的底层流程：深拷贝所有组件和子物体 -> Awake() -> OnEnable()（如果激活） -> 下一帧 Start()。注意：Instantiate 是同步操作，大量实例化会卡帧。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **Prefab 的概念**：
   - 将 GameObject（含组件、子物体、属性配置）保存为 Project 中的资产模板
   - 拖入场景创建实例，运行时通过 `Instantiate()` 动态生成
   - Prefab 修改可以**同步**到所有实例（Unity 2018.3+ Prefab Mode 支持嵌套 Prefab）
2. **Instantiate 的底层流程**：
   1. **深拷贝**：复制原 GameObject 的所有组件数据和子物体层次结构
   2. **Awake()**：实例化时立即调用（无论物体是否激活）
   3. **OnEnable()**：如果物体是激活状态则调用
   4. **下一帧 Update 之前**：`Start()` 调用
3. **Prefab 变体（Prefab Variant）**：
   - 基于已有 Prefab 创建变体，继承基础 Prefab 的属性
   - 基础 Prefab 的修改会自动同步到变体
   - 变体可以覆盖特定属性
4. **性能和最佳实践**：
   - `Instantiate` 是同步操作，在实例化复杂 Prefab 时可能卡帧
   - 大量创建用**对象池**替代
   - 异步加载可用 `Addressables.InstantiateAsync`

## 详细解析

### Instantiate 的性能开销分析
1. **内存分配**：深拷贝的每个组件和子物体都在堆上分配
2. **序列化数据反序列化**：从 Prefab 的序列化数据重建对象
3. **Awake / OnEnable**：所有组件依次执行
4. **渲染数据创建**：MeshRenderer 需要创建渲染数据

对于复杂的 Prefab（含 SkinnedMeshRenderer、大量子物体），`Instantiate` 可能耗时 10-100ms。

### PrefabUtility（编辑器专用）
```csharp
// 编辑器中将实例的修改应用到 Prefab
PrefabUtility.ApplyPrefabInstance(gameObject, InteractionMode.UserAction);
// 断开 Prefab 连接
PrefabUtility.UnpackPrefabInstance(gameObject, PrefabUnpackMode.Completely, InteractionMode.UserAction);
// 注意：这些都是 Editor 代码，不能用于运行时
```

### 嵌套 Prefab
Unity 2018.3 引入，一个 Prefab 内部可以引用另一个 Prefab 作为子物体。修改内部 Prefab 会同步到所有引用的地方。

## 面试官常见追问
- `GameObject.Instantiate` 和 `Object.Instantiate` 的区别？（没有本质区别，GameObject 是 Object 的子类，内部调用相同逻辑）
- Instantiate 和对象池的使用场景如何区分？（频繁创建销毁用对象池；一次性场景加载用 Instantiate）
- Prefab 中的 override 是什么意思？（实例的属性值覆盖了 Prefab 的默认值，Inspector 中加粗显示）

## 我曾经的误区 / 网上常见错答
- **错**："Instantiate 后马上就能用 Start 中的数据" —— Start 在下一帧执行，如果需要立即初始化，放在 Awake 中调用或手动执行初始化方法
- **错**："Prefab 变体就是新建一个 Prefab" —— 变体继承了基础 Prefab 的链接，修改基础 Prefab 会同步到变体

## 关联知识点
- [[Unity 生命周期]]
- [[对象池]]
- [[AssetBundle 机制]]

## 原始出处
- GitHub面经_Unity引擎 Q22-Q23
- 博客园 梦幻事业部外包面经 Q3
