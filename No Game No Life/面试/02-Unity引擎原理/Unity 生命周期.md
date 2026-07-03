---
title: "Unity 生命周期"
category: Unity引擎原理
tags: [Unity, Csharp, 网易互娱, 生命周期, MonoBehaviour]
frequency: ⭐⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[Unity 协程原理]]"
  - "[[Prefab 与 Instantiate]]"
  - "[[Unity 协程原理]]"
---

## 一句话结论（自测用）
> Awake(初始化自身) -> OnEnable(激活时) -> Start(依赖其他组件初始化) -> FixedUpdate(物理) -> Update(逻辑) -> LateUpdate(相机跟随) -> OnDisable(失活) -> OnDestroy(销毁)。关键区分：Awake 和 Start 都只执行一次，但 Awake 在脚本禁用时也会调用。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **完整执行顺序**：
   ```
   加载场景 → Awake() → OnEnable() → Start()
           → FixedUpdate() → Update() → LateUpdate()
           → OnGUI()（可能多次）
           → OnDisable() → OnDestroy()
   ```
2. **关键区分**：
   - **Awake**：脚本实例化时调用**一次**，**无论脚本是否启用**。用于初始化自身状态。
   - **OnEnable**：脚本激活时调用，**可反复触发**（每次 SetActive(true) 都会触发）。用于注册事件。
   - **Start**：首次启用且在 Update 之前调用一次。用于依赖其他组件的初始化（此时其他物体的 Awake 已全部执行完）。
   - **FixedUpdate**：固定间隔（默认 0.02s / 50FPS）。用于物理模拟，不受帧率影响。
   - **Update**：每帧调用一次。用于玩家输入、游戏逻辑。
   - **LateUpdate**：每帧 Update 之后调用。用于相机跟随、动画后处理。
   - **OnDisable**：脚本禁用时调用。用于注销事件。（OnDestroy 前也会调用一次）
   - **OnDestroy**：物体被销毁时调用一次。
3. **所有物体的 Awake 全部完成后才进入 Start**：这是关键特性——在自己的 Start 中可以安全获取其他物体的组件。

## 详细解析

### Awake vs Start 的实战选择
| 场景 | 用 Awake | 用 Start |
|------|---------|---------|
| 初始化自身成员变量 | 推荐 | 不必要 |
| 获取自身组件 | 推荐 | 可以但我不用 |
| 获取其他物体的组件 | **不行**（对方可能还未 Awake） | 推荐 |
| 注册消息/事件 | 不推荐 | 推荐（确保发送方已初始化） |

### OnEnable 的反复触发陷阱
- 每次 `SetActive(true)` 都会触发 `OnEnable` + `Start`（首次）
- 但 `Start` 只在 **首次** 激活时调用
- OnEnable 中注册事件前，务必先注销再注册，避免重复注册

### FixedUpdate 的物理帧率
- 默认 `Time.fixedDeltaTime = 0.02s`（50Hz）
- 可以在 `Project Settings -> Time` 中调整
- 如果帧率 < 50FPS，FixedUpdate 会在一帧内执行多次以"追赶"物理时间
- 如果帧率 > 50FPS，可能某帧不执行 FixedUpdate

### OnGUI 的特殊性
- 用于 IMGUI（立即模式 GUI），**每帧可能调用多次**（每次事件）
- 不要用于游戏 UI（用 UGUI/UI Toolkit 代替）
- 适合编辑器扩展脚本

## 面试官常见追问
- 多个物体之间的 Awake 执行顺序是什么？（不确定，不应依赖。可用 Script Execution Order 设置）
- FixedUpdate 和 Update 在同一帧的执行关系？（如果帧率低，FixedUpdate 会在一帧内多次执行；如果帧率高，某帧可能不执行 FixedUpdate）
- 销毁物体时 OnDisable 和 OnDestroy 哪个先执行？（OnDisable 先，OnDestroy 后。OnDisable 在 OnDestroy 之前总是会被调用）
- 协程在生命周期中的位置？（yield return 的协程在 Update 之后、LateUpdate 之前恢复执行）

## 我曾经的误区 / 网上常见错答
- **错**："Awake 和 Start 的区别只是执行顺序" —— 更关键的区别是 Awake 无论脚本是否启用都调用，Start 只在激活时调用
- **错**："OnEnable 和 Start 差不多" —— OnEnable 可以反复触发，Start 仅一次
- **错**："OnGUI 每帧执行一次" —— 每帧可能执行多次（每处理一个 GUI 事件）
- **错**："开始游戏后第一个执行的就是 Awake" —— 在 Awake 之前还有字段初始化（声明时赋值和 `[SerializeField]`）

## 关联知识点
- [[Unity 协程原理]]
- [[Prefab 与 Instantiate]]
- [[碰撞检测与物理系统]]
- [[动画系统]]

## 原始出处
- GitHub面经_Unity引擎 Q1-Q4
- 博客园 多论坛面经汇总 3.2 节
- 博客园 梦幻事业部外包面经 Q4
- BOSS直聘 面试评价汇总
