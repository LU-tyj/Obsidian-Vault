---
title: "CPU与GPU优化"
category: Unity引擎原理
tags: [Unity, Csharp, 网易互娱, 性能优化, CPU, GPU]
frequency: ⭐⭐
difficulty: 困难
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[DrawCall 优化]]"
  - "[[UGUI 性能优化]]"
  - "[[对象池]]"
  - "[[内存优化与泄露]]"
---

## 一句话结论（自测用）
> CPU 优化三大方向：减少 DrawCall（合批/Instancing）、脚本降频（事件驱动/缓存引用）、物理降频（简化碰撞体）。GPU 优化四大方向：降低分辨率、LOD、减少 Overdraw、Shader 优化（half/fixed 替代 float）。定位瓶颈用 Profiler + Frame Debugger。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **CPU 优化方向**：
   | 方向 | 措施 |
   |------|------|
   | 减少 DrawCall | 合批、Instancing、图集、遮挡剔除（详见 [[DrawCall 优化]]） |
   | 脚本优化 | 缓存 GetComponent、避免 Update 中 Find/FindObjectOfType、事件驱动降频 Update、避免值类型 foreach |
   | 物理优化 | 简化碰撞体（Sphere > Box > Capsule > Convex Mesh）、降频 FixedUpdate、减少 Rigidbody 数量 |
   | 动画优化 | 远处降频更新、关闭 IK、减少 Animator 层数、GPU Skinning |
2. **GPU 优化方向**：
   | 方向 | 措施 |
   |------|------|
   | 分辨率 | 降低渲染分辨率（移动端最有效）+ 降低 RenderTexture 分辨率 |
   | LOD | 远处降模、降 Shader 复杂度 |
   | Overdraw | 不透明从前往后渲染、减少半透明重叠、遮挡剔除 |
   | Shader | half/fixed 替代 float、减少变体、精简 Pass |
   | 后处理 | 减少或降分辨率后处理（Bloom/DOF 代价高） |
   | 阴影 | 降低阴影分辨率、减少投射距离、静态物体烘焙替代实时阴影 |
3. **移动端合理目标**：
   - Batches：低端 <= 100-150，中端 <= 200-300，高端 <= 400-500
   - SetPass Calls：<= 20-30
   - 主线程 CPU 耗时：<= 16ms（60FPS）/ <= 33ms（30FPS）

## 详细解析

### 使用 Profiler 定位瓶颈
1. **CPU Usage** 面板：看哪部分逻辑耗时（Scripts / Physics / Rendering / GC）
2. **Rendering** 面板：看 Batches 和 SetPass Calls
3. **Memory** 面板：看纹理/模型/动画内存占用
4. **Frame Debugger**：逐 DrawCall 查看，找未合批、不可见物体仍在渲染等问题
5. **对比法**：记录每次迭代的 Profiler 数据，对比新增了什么开销

### Update 降频策略
```csharp
// 方案1：事件驱动（推荐）
// 替代 Update 中每帧检测，改为事件触发
Health.OnChanged += UpdateUI;

// 方案2：协程降频
IEnumerator SlowUpdate() {
    while (true) {
        // 0.5秒检测一次，不是每帧
        yield return new WaitForSeconds(0.5f);
    }
}

// 方案3：计数器降频
int frameCounter = 0;
void Update() {
    frameCounter++;
    if (frameCounter % 30 == 0) { // 每30帧执行一次
        // 重型逻辑
    }
}
```

### Shader 优化
- `half`(16位) > `fixed`(11位) > `float`(32位) -- 优先用精度低的
- 减少纹理采样次数
- 合并同类 Pass（减少 Shader 变体）
- 使用 `#pragma shader_feature` 而非 `multi_compile`（减少编译的变体数量）

## 面试官常见追问
- 怎么确定是 CPU 还是 GPU 瓶颈？（Profiler 看谁先跑满：CPU 满 GPU 等待=CPU瓶颈，反之亦然；或用 RenderDoc/XCode GPU 抓帧）
- 为什么移动端优先降分辨率？（移动端 GPU 的填充率/带宽往往是瓶颈，降分辨率效果最立竿见影）
- Overdraw 怎么查看？（Scene 视图 -> Shading Mode -> Overdraw）

## 关联知识点
- [[DrawCall 优化]]
- [[UGUI 性能优化]]
- [[对象池]]
- [[内存优化与泄露]]

## 原始出处
- GitHub面经_性能优化 Q2-Q7
- 牛客网 013_游戏引擎面经 Q5
