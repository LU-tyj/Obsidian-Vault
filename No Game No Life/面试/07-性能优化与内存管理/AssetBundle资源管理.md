---
title: "AssetBundle资源管理"
category: 性能优化与内存管理
tags: [性能优化, 资源管理, AssetBundle, Addressables, 热更新, 网易互娱]
frequency: ⭐⭐⭐
difficulty: 中等
companies: [网易互娱]
status: new
last_reviewed:
next_review:
related:
  - "[[内存优化策略]]"
  - "[[GC机制与优化]]"
---

## 🎯 一句话结论（自测用）
> AssetBundle 用于减小安装包体积、按需加载资源和实现热更新。加载方式：LoadFromFile（最快）> LoadFromMemory > UnityWebRequest。压缩格式：推荐 LZ4（按需解压，兼顾速度和体积）。卸载：Unload(true) 卸载 Bundle + 所有已加载资源，Unload(false) 只卸载包体本身。Addressables 是 Unity 官方基于 AB 的上层管理系统，自动处理依赖和引用计数。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **AssetBundle 的作用**：
   - 减小初始安装包体积，按需加载
   - 实现资源热更新（模型、贴图、场景等）
   - 分离不同平台资源包（Android/iOS 专用）
   - 灵活的版本管理和增量更新
2. **加载方式对比**：
   - `LoadFromFile(path)`：从本地文件加载，最快，推荐
   - `LoadFromMemory(bytes)`：从内存加载，额外内存开销
   - `UnityWebRequestAssetBundle`：网络异步加载
   - `WWW.LoadFromCacheOrDownload`：旧版，已废弃
3. **压缩格式**：
   - LZMA：压缩率最高，但需整包解压，解压慢
   - LZ4：压缩率中等，按需解压，推荐（Unity 2017+ 默认）
   - 不压缩：最快，体积最大
4. **卸载策略**：
   - `Unload(true)`：卸载 Bundle + 所有已加载资源，会导致引用丢失
   - `Unload(false)`：只卸载 Bundle 包体数据，已加载资源保留
   - 场景切换用 Unload(true)，局部卸载用 Unload(false)
5. **依赖管理**：每个 Bundle 有 Manifest 记录依赖关系，加载前需先加载依赖的 Bundle。Addressables 自动处理依赖。
6. **打包策略**：按场景/功能/类型分包，共享依赖单独提取。

## 🔍 详细解析

### 动态加载方式总览
| 方式 | 说明 | 适用场景 |
|------|------|---------|
| Resources.Load | 读取 Resources 文件夹 | 小项目/原型 |
| AssetBundle | 独立包体，按需加载 | 大型项目、热更新 |
| Addressables | 基于 AB 的官方系统 | 现代化项目 |
| UnityWebRequest | HTTP 异步网络加载 | 远程资源下载 |

### AssetBundle 打包策略
1. **按场景分包**：每个场景独立打包
2. **按功能分包**：核心资源（不热更）+ 功能资源（可热更）
3. **按类型分包**：贴图、模型、音效分别打包
4. **共享依赖提取**：多个 Bundle 的公共资源单独打包

### Addressables vs AssetBundle
| 维度 | Addressables | AssetBundle |
|------|-------------|-------------|
| 依赖管理 | 自动 | 手动（Manifest） |
| 引用计数 | 自动 | 手动管理 |
| 远程更新 | 内置 | 需自行实现 |
| 加载/卸载 API | 简化 | 底层 API |
| 定制性 | 较低 | 高 |

### Addressables 高频考点
1. **加载是同步/异步？** 推荐异步 `Addressables.LoadAssetAsync`
2. **场景切换释放？** 无引用的资源可自动卸载
3. **对象池能用吗？** 可以，加载后实例化副本，Release AsyncOperationHandle
4. **很多小 Bundle 的缺点？** 元数据膨胀、加载次数增多

## 💬 面试官常见追问
- **Unload(true) 和 Unload(false) 的区别和使用场景？** → true 完全释放但会导致引用丢失（场景切换）；false 释放包体但保留资源引用（局部卸载）
- **如何检测资源是否被卸载干净？** → Unity Profiler Memory 面板、Memory Profiler 查看引用链
- **热更新的资源版本管理怎么做？** → 维护版本号配置、对比客户端/服务器版本、下载差异文件（增量更新）、MD5/CRC 校验
- **下载中断怎么处理？** → 断点续传（HTTP Range 头）、临时文件 + 重命名原子操作

## ⚠️ 我曾经的误区 / 网上常见错答
- 误区：把全部资源放 Resources。Resources 所有资源强制进包，不利于微端和热更新
- 误区：Unload(false) 后资源就完全释放了。只释放包体压缩数据，已加载的资源对象仍在内存中

## 🔗 关联知识点
- [[内存优化策略]]
- [[GC机制与优化]]

## 📎 原始出处
- GitHub面经_资源管理 Q1-Q7：完整 AssetBundle 知识体系
- 牛客网 002 Q1/Q8：AssetBundle 加载方式和内存管理
- 博客园汇总：AssetBundle 机制为高频考点
