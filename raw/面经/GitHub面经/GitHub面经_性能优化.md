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

# 性能优化面试题

## 一、性能优化总览

### Q1: "你是如何做好 Unity 项目性能优化的？"（开放题）

**高分回答框架**：

**1. 工程管理层面（最重要）**:
- 从项目第一天起引入多平台测试和性能监控
- 专人 Review 代码 + 性能参数统计（每次迭代对比 Batches、Main Thread 等）
- 动态清零性能问题

**2. 定位问题**:
- Profiler + Frame Debugger 检查 CPU/GPU/内存瓶颈
- 对比法：对比上次测试与本次开发记录，快速定位引入问题的代码

**3. 针对性优化**: 见以下各专项

---

## 二、CPU 优化

### Q2: CPU 优化的主要方向？

| 方向 | 具体措施 |
|------|---------|
| **减少 DrawCall** | 合批、Instancing、图集、遮挡剔除 |
| **脚本优化** | Update 降频（事件驱动）、缓存组件引用、避免高开销 API |
| **物理优化** | 减少碰撞体复杂度、降频 FixedUpdate、使用简单碰撞体 |
| **动画优化** | 远处物体降低更新频率、关闭 IK、减少 Animator 层数 |

### Q3: 如何降低脚本导致的 CPU 开销？
1. 缓存 GetComponent 引用（在 Awake/Start 中）
2. 避免在 Update 中使用 Find、FindObjectOfType
3. 将过度频繁的 Update 改为事件驱动或协程（如 0.5 秒检测一次）
4. 避免在 Update 中使用 foreach（值类型集合）
5. 使用正确的 Tags 比较方法（CompareTag 而非 tag == "xxx"）

### Q4: 减少 DrawCall 的 10 种方法？
1. 静态合批（Static Batching）
2. 动态合批（Dynamic Batching）
3. GPU Instancing
4. SRP Batcher（URP/HDRP）
5. 图集合并（Atlas）
6. 减少 Shader Pass 数量
7. 遮挡剔除（Occlusion Culling）
8. LOD（细节层次）
9. 合理的渲染排序（减少状态切换）
10. UI 优化（Canvas 合理划分、动静分离）

---

## 三、GPU 优化

### Q5: GPU 优化的主要方向？
1. **分辨率缩放** -- 移动端最有效的优化手段
2. **LOD** -- 远处物体降模
3. **后处理轻量化** -- 或关闭不必要的后处理
4. **减少 Overdraw** -- 避免大量半透明重叠
5. **Shader 优化** -- 用 half/fixed 代替 float
6. **实时阴影控制** -- 降低分辨率、减少投射距离、使用静态烘焙替代

### Q6: 移动端 DrawCall 的合理目标值？
- **低端机**: <= 100~150 Batches
- **中端机**: <= 200~300 Batches
- **高端机**: <= 400~500 Batches
- **SetPass Calls**: 尽可能控制在 20~30 以内

### Q7: Overdraw 如何优化？
- 合理的渲染顺序（不透明物体从前往后，透明物体从后往前）
- 使用遮挡剔除减少不可见物体的绘制
- UI 减少重叠、关闭不必要的 Raycast Target

---

## 四、内存优化

### Q8: 内存优化的主要策略？

1. **贴图压缩**: ASTC > ETC2 > PVRTC（按平台选择）
2. **关闭 Read/Write Enabled**: 贴图不会在内存中保留两份
3. **透明通道分离**: 无透明通道可用 ETC 压缩
4. **Reduce model complexity**: 降低模型面数、骨骼数
5. **Resources 源文件控制**: 避免所有资源放 Resources
6. **按需加载**: AssetBundle / Addressables（不一次性加载全部）
7. **Lightmap 替代实时光**: 静态物体用烘焙
8. **控制 RenderTexture 分辨率**

### Q9: 常见的内存泄露原因？
1. **静态变量持有对象引用** -- GC 无法回收
2. **事件/委托未注销** -- 对象被事件源引用
3. **AssetBundle 未释放** -- 调用 Unload(false) 后资源常驻
4. **Resources.Load 后未 Unload**
5. **协程未停止** -- 持有对象引用
6. **单例持有已销毁对象的引用**

**检测工具**: Unity Profiler, Memory Profiler, dotMemory

### Q10: AssetBundle.Unload(true) vs Unload(false)？
- **Unload(true)**: 卸载 Bundle 及所有从中加载的资源（可能有引用丢失风险）
- **Unload(false)**: 只卸载 Bundle 包体本身，已加载资源保留
- 必须注意：Unload(true) 会导致已加载的资源对象变为 Missing

---

## 五、UI 优化

### Q11: UI 优化的核心策略？

| 优化项 | 说明 |
|-------|------|
| **动静分离** | 动态 UI 和静态 UI 放在不同的 Canvas 下 |
| **图集化** | 同一界面的图整合为一张图集 |
| **Mask 优化** | RectMask2D 替代 Mask（省 DC） |
| **Raycast Target** | 不需要交互的 UI 关闭该选项 |
| **TMP 替代 Text** | TextMeshPro 顶点数更少 |
| **ScrollView 对象池** | 只实例化可见区域的条目 |
| **减少 Canvas 数量** | 每个 Canvas 的更新都会重建整个 Canvas 网格 |

---

## 六、对象池优化

### Q12: 对象池的核心价值？
- 减少 GC 触发（避免频繁 Instantiate/Destroy）
- 降低 CPU 峰值（预创建，消除运行时分配）
- 减少内存碎片
- 提升游戏流畅度

### Q13: 对象池的关键设计点？
1. **预热**: 游戏开始时预生成一定数量
2. **动态扩容**: 池不够时自动生成额外对象
3. **回收策略**: 限定最大数量，超出销毁或延迟回收
4. **状态重置**: 回收时必须重置对象所有状态

---

## 七、Unity 特有优化

### Q14: IL2CPP vs Mono 的区别？
- **Mono**: JIT 编译，支持动态代码生成
- **IL2CPP**: AOT 编译，iOS 必需，性能更好（约 1.5x），不支持 Emit
- 主流项目选择 IL2CPP（性能 + iOS 支持）

### Q15: Job System 和 Burst Compiler？
- **Job System**: 多线程任务调度，将计算密集型任务放到工作线程
- **Burst Compiler**: 将 C# 代码编译为高性能机器码
- 结合使用可实现接近 C++ 的性能
- 应用: 寻路、物理计算、大量实体处理

---

## 八、快速检查清单

面试中能脱口而出的 10 条常用性能优化：
1. 对象池 -> 减少 GC
2. 静态/动态合批 -> 减少 DrawCall
3. LOD -> 降低远处物体渲染开销
4. 图集 -> 合批 UI，减少 DC
5. URP + SRP Batcher -> 高效渲染
6. 贴图压缩（ASTC）+ 关闭 Read/Write -> 降低内存
7. StringBuilder 替代 string + -> 避免 GC
8. Update 降频 / 事件驱动 -> 降低 CPU
9. AssetBundle / Addressables 按需加载 -> 控制内存峰值
10. 物理：减少碰撞体复杂度、降频 FixedUpdate

---

> 来源: unitykit/unityClientInterviewGuide, Lafree317/Unity-InterviewQuestion
