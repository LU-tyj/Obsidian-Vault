[[GAMES104_Lecture02.pdf]]

## 1 Layers of Game Engine
具体有5层架构组成
- **Tool Layer** : 游戏引擎操作界面，编辑环境。
- **Function Layer** : Rendering，Animation，Physics等等。
- **Resource Layer** : 资源层，控制各种的存储。
- **Core Layer** : 核心层，包含基本的函数方法。
- **Platform Layer** : 在平台上如何运行

---

## 2 Resource - How to Access My Data
**目的**：resource -> assets
各种资源文件格式转换成统一的资源格式，例如png、jpeg等图片格式压缩方式不同，且不适合GPU直接处理，需要统一转换成dts格式（可以直接在GPU中使用），这种转换提取有用数据（例如word格式中有许多无用信息），并压缩，节省存储空间和运算效率。

定义一个描述资产关系的文件（脚本，[XML](https://link.zhihu.com/?target=https%3A//blog.csdn.net/RCHT1_Hideonbush/article/details/124000339)），例如说明模型、贴图、动画对应的文件分别是哪些，以使引擎在运行时加载对应的资产。

游戏引擎最核心的功能就是数据之间的关联。游戏工程文件中会给每一个asset配置一个全局的独一的文件识别号GUID（global unique identify）

**作用**：管理游戏中所有资产实时的生命周期。

---

## 3 Function - How to Make the World Alive
**Tick**：帧、时间、运动、变化。
>游戏引擎就是每tick把游戏的逻辑跑了一遍。先进行logic，再进行render。这是上古两大神兽，如下图所示
![[Dive_to_Ticks.png]]

在每一个tick中（简化版本）：
1. Fetch animation frame of character.
2. Drive the skeleton and skin of character.
3. Renderer process all rendering jobs in an iteration of render tick for each frame.
4. 

Function 层还会面临 Multi-Threading的性能问题。

---

## 4 Core
游戏引擎的基层，以效率为先，与操作系统底层类似。
**Math Library**：追求数学库的效率，比如 Q_rsqrt 开根号。
**Data Structure and Containers** 
**Memory Management** 

要求高质量代码，绝对的安全性和效率。

---

## 5 Platform - Target on Different Platform
目的是使游戏开发不受平台差异的影响。例如不同的平台会使用不同的图形API，平台层通过Render Hardware Interface（RHI）来解决这些差异问题，利用虚函数对这些图形API进行封装。

---

## 6 Tool - Allow Anyone to Create Game 
前面的层均为 runtime 时考虑的层，工具层允许别人使用引擎的层。
![[Tool_Digital_Content_Creation.png]]

