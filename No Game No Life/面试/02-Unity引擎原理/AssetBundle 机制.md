---
title: "AssetBundle 机制"
category: Unity引擎原理
tags: [Unity, Csharp, 网易互娱, AssetBundle, 资源管理]
frequency: ⭐⭐⭐
difficulty: 困难
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[Addressables]]"
  - "[[资源加载方式对比]]"
  - "[[资源卸载与内存管理]]"
  - "[[热更新方案对比]]"
---

## 一句话结论（自测用）
> AssetBundle 是 Unity 的资源包，支持按需加载、热更新、分包。加载推荐 `LoadFromFile` + LZ4 压缩。关键考点：依赖管理（Manifest）、卸载 `Unload(true/false)`、打包策略（按场景/功能/类型）。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **作用**：
   - 减小初始安装包体积（资源按需下载）
   - 实现资源热更新（更新模型/纹理/场景等）
   - 分离不同平台资源包（Android/iOS 专用）
   - 灵活的版本管理和增量更新
2. **三种加载方式**：

| 方式 | 特点 |
|------|------|
| `AssetBundle.LoadFromFile(path)` | 本地加载，最快，推荐 |
| `AssetBundle.LoadFromMemory(bytes)` | 从内存加载，注意内存峰值 |
| `UnityWebRequestAssetBundle` | 网络异步加载，适合远程资源 |

3. **三种压缩格式**：

| 格式 | 压缩率 | 解压方式 | 推荐场景 |
|------|--------|---------|---------|
| LZMA | 最高（约 50-70%） | 整包解压，首帧慢 | 网络传输 |
| LZ4（推荐） | 中等（约 50-60%） | 按需解压，即用即解 | 本地+网络通用 |
| 不压缩 | 0% | 无解压开销 | 开发调试 |

4. **卸载 `Unload(true)` vs `Unload(false)`**：
   - `Unload(true)`：卸载 Bundle 本体 + **所有已加载资源**，会导致 `MissingReference`
   - `Unload(false)`：只卸载 Bundle 的压缩数据，已加载资源**保留**
   - 场景切换用 Unload(true)，局部卸载用 Unload(false)
5. **依赖管理**：每个 AB 有 Manifest 记录依赖，加载前须先加载依赖 Bundle，否则资源可能丢失引用（如材质找不到贴图）。

## 详细解析

### 打包策略
| 策略 | 适用场景 |
|------|---------|
| **按场景分包** | 每个场景独立 AB，场景切换时加载/卸载 |
| **按功能分包** | 核心资源（不进热更包） + 功能资源（可热更） |
| **按类型分包** | 贴图 / 模型 / 音效分别打包 |
| **共享依赖提取** | 多个 Bundle 共用的资源单独打一个 Bundle |

### 依赖加载的正确流程
```csharp
// 错误做法：直接加载 targetBundle，材质丢失贴图
AssetBundle targetBundle = AssetBundle.LoadFromFile(pathToTarget);

// 正确做法：先加载依赖
AssetBundle manifestBundle = AssetBundle.LoadFromFile(pathToManifest);
AssetBundleManifest manifest = manifestBundle.LoadAsset<AssetBundleManifest>("AssetBundleManifest");
string[] deps = manifest.GetAllDependencies("target");
foreach (string dep in deps) {
    AssetBundle.LoadFromFile(pathToDep); // 加载所有依赖
}
AssetBundle targetBundle = AssetBundle.LoadFromFile(pathToTarget); // 最后加载目标
```

### AssetBundle 内存占用三部分
1. **Bundle 压缩数据**（调用 Unload(false) 可释放）
2. **序列化文件头**（Asset 的元数据索引）
3. **实际加载的 Asset 对象**（调用 Unload(true) 可释放）

## 面试官常见追问
- 为什么推荐 LZ4 而不是 LZMA？（LZ4 按需解压，加载特定资源时不需要解压整个包；LZMA 必须先解压整个包）
- `Unload(false)` 后资源还在内存吗？（在。只是 Bundle 的压缩数据释放了，已加载的资源还在）
- 如果用 `Unload(true)` 卸载了正在被引用的资源会发生什么？（变成 Missing Reference，场景中使用该资源的物体会变紫/透明）
- AssetBundle 如何实现增量更新？（对比版本文件，只下载变化的 Bundle，更新本地 Manifest）
- 很多小 AssetBundle 有什么问题？（元数据膨胀、加载次数过多、文件 IO 压力大）

## 我曾经的误区 / 网上常见错答
- **错**："LZ4 压缩率不如 LZMA，不如不用" —— LZ4 的按需解压优势远大于 LZMA 的微小压缩优势
- **错**："`LoadFromFile` 和 `LoadFromMemory` 差不多" —— LoadFromFile 从磁盘直接映射，不占托管内存；LoadFromMemory 会将全部数据加载到托管堆
- **错**："AssetBundle 只能用在手游热更" —— PC 端也可用，主要用于资源隔离和 DLC 分发

## 关联知识点
- [[Addressables]]
- [[资源加载方式对比]]
- [[资源卸载与内存管理]]
- [[资源版本管理与热更新资源]]
- [[热更新方案对比]]

## 原始出处
- GitHub面经_资源管理 Q2-Q7
- 牛客网 002_雷火实习 Q1/Q8
- 博客园 多论坛面经汇总 3.2 节
- BOSS直聘 面试评价汇总
