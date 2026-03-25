## 1 Introduction
工具链是让不同思维方式的人团结工作的平台。

## 2 Complicated Tool GUI
### 2.1 GUI introduction
Graphics User Interface
- **Immediate Mode**：每一帧由游戏逻辑告诉gui系统打开一个控件，比如Imgui。优点是简单，但是拓展比较差，而且需要程序员
- **Retained Mode**：把所有相关指令存在一个buffer中，让gui系统自己画，比如QT。性能好，拓展易，不用更新其指令。这里Design Pattern非常重要。

### 2.2 Design Patterns
著名的Patterns：**MVC**
![[MVC.png]]

变种：**MVP** 更彻底把Model和View 解耦。把所有复杂度集中在了 Presenter
![[MVP.png]]

推荐的是 **MVVM**，这里View就不用知道什么逻辑，只要所见即所得，ViewModel实现了数据的绑定关系，Model就是实现数据的处理。但缺点是依赖平台环境，在DataBinding容易出错。
![[MVVM.png]]
![[MVVM2.png]]

### 2.3 Load & Save
Serialization and Deserialization 其实就是对应Save（存成2进制数据）和Load（将数据加载到内存）

- **Save**
最早的时候是用Text File，比如TXT、Json、YAML、XML等，比如Unity Editor是用的就是subset of YAML

Binary Files，有更大的存储容量

由于很多资产是重复的，所以我们可以使用Asset Reference，可以参考[[2.2 Flyweight Pattern]]。比如重复出现房子10次，房子称为Definition，我们创建的为Instance.
我们还要在工具链中提供Variance的能力，这里我们就使用了 Inheritance，继承数据（把原始数据拷贝过来，然后继承改变）。

- **Load**
先读取数据，把数据拆分成语义，然后生成一个 \<field-value\> tree。
![[Parse Asset File.png]]
![[Field-value tree.png]]

- **Asset Version Compatibility**
让不同版本的资产能够兼容
简单粗暴的方法：UE让程序员为资产手写版本号，比如`if (Versiojn == 1)`。
Google的方法：Google Protocol Buffers，定义每一个数据的Field的时候，生成一个unique key，然后新旧版本只需要取自己需要的ID，如果没有就用默认
>比如 `[id][name][level]` 存储为 `(1,id)(2,name)(3,level)`

---

## 3 How to Make a Robust Tools
要关注：Undo & Redo、Crash Recovery
使用Command Pattern，将用户的操作记录成Command，参考[[2.1 Command Pattern]]，可以非常好的实现 Recovery和Undo Redo。

Command接口包含：
- UID 保准操作执行循序
- Serialize & Deserialize 让数据提供方法，Command利用这些方法实现数据。
- Data，Invoke，Revoke

三个关键的Command：Add、Delete、Update
![[Commands.png]]

---

## 4 How to make a tool chain
Find Common Building Blocks 将不同Entity数据的共同点整理出来，找出一个个原子，比如读取出float x

Schema - A Description Structure 将原子组合成分子，比如将float x、y、z结合成一个长方体的尺寸。Schema告诉工具你该怎么理解这个数据。

还需要有不同view的能力

---

## 5 What you see is what you get
在工具链提供 1:1  的preview
Editor Mode：Editor UI -> Editor Scene -> Runtime
Play in Editor

