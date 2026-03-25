## 1 Particle System
### 1.1 Particle
粒子的属性：Postition, Velocity, Size, Color, Lifetime

Life Cycle（最简版）如下图：
![[Particle Life Cycle.png]]

**Particle Emitter**：用来定义发射的规则以及如何渲染
把一堆Emitter集合在一起后，就变成了 **Particle System**
>比如 Flame Emitter + Smoke Emitter + Spark Emitter = Flame Particle System

- **Particle Spawn Position**：不仅可以是一个点，还可以时一个空间、区域
- **Particle Spawn Mode**：Continuous、Burst

Simulate 要考虑重力、空气阻力、风力，按照[[Lec10 Physics System - Basic Concepts]]中计算每个粒子的运动状态，最复杂的是加上与环境的互动，实际上调用物理系统会非常慢（粒子太多了）

particle又可以分为 
- **Billboard Particle** 始终朝向Camera的贴图
- **Mesh Particle** 每个Particle都是一个3D model
- **Ribbon Particle** 一个光带，在飞行过程中不断产生Spawn，使用曲线插值，可以用于斩击特效 

### 1.2 Particle System Rendering 
就像Alpha Blending Order，我们要对Particle进行排序（一堆Particle Emittor & System），可以对全局进行排序，可以写rules
>全局：Per system -> Per emitter -> Within emitter
>Rules：可以依照 Particle 离 camera 的距离，也可以在 Systems 或 Emitters 之间。

如果直接对Particle进行直接渲染可能会出现很大的性能开销（透明），可以通过进行half-resolution进行渲染，把屏幕像素数量缩小4倍，然后再进行渲染

### 1.3 GPU Particle
如果 Particle 每一帧都要进行渲染，会造成 GPU 开销很大（别忘了还有Game Code），所以需要并行

1. Initial State. 先定一个一个Particle Pool，包含所有Particle的具体信息；再定一个Dead List，里面包含没有使用激活的 Particle，以及一个 Alive List
2. Spawn Particle. 从 Dead List 末尾取几个 Particle加入 Alive List 中
3. Simulate. 对Allive Particle进行simulation，然后再把新死的放入Dead List。这里就是使用了[[3.1 Double Buffer]]的设计模式
4. Sort, Render and Swap Alive List.
![[GPU Particle Simulate.png]]![[Sort, Render and Swap Alive Lists.png]]

 用GPU处理Collision可以通过：**Depth Buffer Collision**，通过GPU中的Z-buffer来判断是否产生碰撞。

---

## 2 Sound System
### 2.1 Sound Basics
- **Volume** 音量（压强） 分贝
- **Pitch** 音频 声音是否尖锐
- **Timbre** 音色 由很多基波叠在一起

PCM (Pulse-code Modulation) 采样 量化 编码 -> 计算机上声音的表达
- **Sampling** 采样密度在声波频率两倍以上就是无损
- **Quantizing** bit-depth，存储每一个采样点的音频的振幅的字节数量
- **Audio Format** 各种类似mp3、wav的格式，游戏引擎大多使用OGG，因为没有专利可以随便用
![[Audio Format.png]]

### 2.2 3D Audio Rendering
**Listener** 类似观察者，包含 position、velocity（多普勒效应）、orientation

为了实现空间感Spatialization，我们需要 Panning、Soundfield、Binaural Audio

1. **Panning**
调整Speaker上不同通道的声音来实现空间感，包括Linear Panning、Equal Power Panning等
- Attenuation
	声音的衰弱，不同频率衰减不同
	最简单的是一个基础形状，比如球形、胶囊形等等
- Obstruction & Occlusion
	声波的衍射，以及声波被墙隔住了。CastRays到Listener，检测障碍物的材质
- Reverb
	混响（例如山洞中喊）。由Direct、Echo、Tail（多次反弹，可能被材质吸收）组成
- The Doppler Effect

2. **Soundfield**
声场，在VR游戏中使用。可以不知道Listener的位置，直接对空间上进行声音的采样

声音引擎一般用 fmod 和 wwise


