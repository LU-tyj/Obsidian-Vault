---
source_platform: GitHub
source_url:
  - https://github.com/unitykit/unityClientInterviewGuide
  - https://github.com/Lafree317/Unity-InterviewQuestion
  - https://github.com/GuardianOfGods/unity-interview-questions
crawl_date: 2026-07-03
crawl_agent: agent-github
company_mentioned: [通用, 网易互娱]
position: Unity客户端开发
raw: true
---

# Unity 引擎面试题

## 一、生命周期

### Q1: Unity 生命周期执行顺序？

```
Awake() -> OnEnable() -> Start()
       -> FixedUpdate() -> Update() -> LateUpdate()
       -> OnGUI()
       -> OnDisable() -> OnDestroy()
```

### Q2: Awake、Start、OnEnable 的区别？
- **Awake**: 脚本实例化时调用一次，无论脚本是否启用
- **OnEnable**: 脚本启用时调用，可反复触发
- **Start**: 脚本首次启用且在 Update 之前调用一次

### Q3: Update vs FixedUpdate vs LateUpdate
| | Update | FixedUpdate | LateUpdate |
|--|--------|-------------|------------|
| 调用频率 | 每帧 | 固定间隔（默认0.02s） | 每帧（Update之后） |
| 受帧率影响 | 是 | 否 | 是 |
| 用途 | 逻辑控制、输入检测 | 物理模拟 | 相机跟随、动画后处理 |

### Q4: OnGUI 什么时候调用？
- 每帧可能调用多次
- 用于 IMGUI（立即模式 GUI），不推荐用于游戏 UI
- 适合编辑器扩展脚本

---

## 二、协程

### Q5: 协程的原理和使用场景？

**原理**：
- 基于 C# 迭代器（IEnumerator）+ yield 语法糖
- 运行在**主线程**，不是多线程
- Unity 内部维护协程状态机，通过 MoveNext() 分步执行

**使用场景**：
- 延时操作（WaitForSeconds）
- 异步加载资源
- 分帧处理大量计算
- 等待异步操作（WaitUntil, WaitWhile）

### Q6: 协程 vs 线程的区别（Unity 中）？
- 协程在主线程运行，线程独立运行
- 协程不能做密集计算（会卡主线程），线程可以
- 协程调度由 Unity 管理，线程由 OS 管理
- Unity API 只能在主线程调用，所以协程可安全调用而线程不能

### Q7: 如何停止协程？
- `StopCoroutine(coroutine)` -- 停止指定协程
- `StopAllCoroutines()` -- 停止所有协程
- 脚本禁用 / 销毁时协程自动停止

---

## 三、物理系统

### Q8: 碰撞发生的必要条件？
- 两个物体都必须有 Collider 组件
- 至少其中一个物体有 Rigidbody 组件
- （对于触发器则使用 IsTrigger = true）

### Q9: 碰撞三个阶段？
```
OnCollisionEnter -> OnCollisionStay -> OnCollisionExit
OnTriggerEnter  -> OnTriggerStay  -> OnTriggerExit
```

### Q10: Collider vs Trigger 的区别？
- Collider：产生物理碰撞，有碰撞反馈（弹开、停止等）
- Trigger：仅检测进入/离开，不产生物理反馈

### Q11: Raycast 的优化方法？
- 使用 LayerMask 过滤，减少检测对象
- 使用 `Physics.RaycastNonAlloc` 避免 GC
- 控制射线检测距离（maxDistance）
- 对静态物体使用 `Physics.Raycast` 的重载指定检测类型

---

## 四、UGUI

### Q12: Canvas 的三种渲染模式？
| 模式 | 说明 | 适用场景 |
|------|------|---------|
| Screen Space - Overlay | UI 永远在最上层 | HUD、血条 |
| Screen Space - Camera | UI 绑定到指定相机，受相机影响 | 3D UI 效果 |
| World Space | UI 在世界空间中，像 3D 物体 | 游戏中漂浮文字 |

### Q13: UGUI 合批条件？
- 同一 Canvas 下
- 相同 Material
- 相同的纹理（同一图集）
- 相同的渲染层级

### Q14: 如何优化 UGUI 性能？
| 优化项 | 说明 |
|-------|------|
| 动静分离 | 将动态 UI 和静态 UI 放在不同 Canvas 下 |
| 图集化 | 同一界面的图整合为一张图集，减少 DrawCall |
| RectMask2D 替代 Mask | Mask 额外增加 DrawCall，RectMask2D 不占用 |
| 取消不必要的 Raycast Target | 不需要交互的 UI 关闭 Raycast Target |
| 使用 TMP 替代 Text | TextMeshPro 顶点数更少，性能更好 |
| ScrollView 对象池 | 只实例化可见区域的条目 |

### Q15: Mask vs RectMask2D？
- **Mask**: 使用模板缓冲（Stencil），占 2 个 DC，不支持合批
- **RectMask2D**: 通过 IClipper 实现裁剪，无额外 DC，只能矩形遮罩

---

## 五、动画系统

### Q16: Unity 动画系统的演变？
1. **Legacy Animation** -- 旧版，已废弃
2. **Mecanim** -- Animator + AnimatorController + 状态机
3. **PlayableGraph** -- 更灵活的动画图 API，可编程控制
4. **Motion Matching** -- 基于动画数据库的智能匹配

### Q17: Animator 中的动画是否全部加载到内存？
- 会加载 AnimatorController 中引用的所有 AnimationClip
- 优化方式：使用 AnimatorOverrideController 按需替换动画

### Q18: 动画混合（Blend Tree）的作用？
- 根据参数（如速度、方向）在多个动画间平滑过渡
- 1D Blend Tree：单一参数混合（如 walk -> run）
- 2D Blend Tree：两个参数混合（如方向 + 速度）

---

## 六、坐标系统

### Q19: Unity 的五大坐标系？
1. **世界坐标（World Space）** -- 全局坐标系
2. **局部坐标（Local Space）** -- 相对于父物体的坐标
3. **屏幕坐标（Screen Space）** -- 像素坐标，左下角为 (0,0)
4. **视口坐标（Viewport Space）** -- 归一化坐标，(0,0) 到 (1,1)
5. **GUI 坐标** -- 左上角为 (0,0)

### Q20: 点乘和叉乘的应用？
- **点乘（Dot）**: 判断两个向量的夹角（>0 同向，<0 反向，=0 垂直）
  - 应用：判断前后、视角检测
- **叉乘（Cross）**: 得到垂直向量，判断左右方向
  - 应用：判断目标在自己左边还是右边

### Q21: 四元数的作用？
- 表示旋转，避免万向节锁
- 如何产生：`Quaternion.Euler(x, y, z)` 或 `Quaternion.LookRotation(direction)`
- 插值：`Quaternion.Lerp` / `Quaternion.Slerp`

---

## 七、Prefab 与实例化

### Q22: Prefab 的概念和作用？
- 将 GameObject 保存为资产模板
- 便于复用、批量修改（Prefab 变更可同步到所有实例）
- 运行时通过 `Instantiate()` 动态生成

### Q23: Instantiate 的底层过程？
1. 深拷贝原始 GameObject 的所有组件和子物体
2. 调用所有组件的 Awake()
3. 如果物体激活，调用 OnEnable()
4. 在下一帧调用 Start()

---

## 八、常用 API

### Q24: GameObject.Find vs Transform.Find vs FindObjectOfType
- `GameObject.Find`: 遍历整个场景，极慢，禁止在 Update 中调用
- `Transform.Find`: 在当前物体的子物体中查找，相对高效
- `FindObjectOfType<T>`: 查找特定类型的第一个组件，也较慢
- 推荐：在 Awake/Start 中缓存引用

### Q25: GetComponent 的性能考虑？
- 每帧调用有性能开销
- 应在 Awake/Start 中获取并缓存
- Unity 2019+ 有增量 GC，但缓存仍然是最佳实践

---

> 来源: unitykit/unityClientInterviewGuide, Lafree317/Unity-InterviewQuestion, GuardianOfGods/unity-interview-questions
