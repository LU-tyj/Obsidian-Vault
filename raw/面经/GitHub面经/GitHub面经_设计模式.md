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

# 设计模式面试题

## 一、七大设计原则（SOLID 及其他）

1. **单一职责原则（SRP）**: 一个类只负责一个功能领域
2. **开闭原则（OCP）**: 对扩展开放，对修改关闭
3. **里氏替换原则（LSP）**: 子类可以替换父类
4. **依赖倒置原则（DIP）**: 依赖抽象而非具体实现
5. **接口隔离原则（ISP）**: 使用多个专门接口而非单一总接口
6. **迪米特法则**: 最少知道原则
7. **合成复用原则**: 优先组合而非继承

---

## 二、单例模式

### Q1: 单例模式的作用和实现？

**作用**: 全局唯一实例，控制资源访问

**Unity 中的单例**:
```csharp
public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }
        Instance = this;
        DontDestroyOnLoad(gameObject);
    }
}
```

### Q2: 单例模式的多线程安全问题？
- 使用 lock 或双重检查锁定
- C# 中可以用静态构造函数或 Lazy\<T\>
- Unity 中主线程模式，一般不需要担心

### Q3: 单例的缺点？
- 全局状态，测试困难
- 隐式依赖，降低代码可读性
- 违反单一职责原则

---

## 三、观察者模式 / 事件系统

### Q4: 观察者模式的作用？
- 定义一对多依赖关系
- 当主题状态变化时，所有观察者自动收到通知

**C# 实现方式**:
- 原生 event / delegate
- UnityEvent
- 自定义 EventManager / MessageCenter

### Q5: UnityEvent vs C# event？
| | UnityEvent | C# event |
|--|------------|----------|
| 序列化 | 可在 Inspector 中显示 | 不可 |
| 性能 | 较低（有反射开销） | 较高 |
| 适用场景 | 编辑器可视化配置 | 纯代码使用 |

### Q6: 事件中心（EventManager）怎么设计？
- 使用 Dictionary<EventType, Delegate> 存储事件
- 提供 Register / UnRegister / Trigger 方法
- 注意：场景切换时需要清理事件注册，否则导致对象无法被 GC

---

## 四、对象池模式

### Q7: 对象池的作用和实现？

**作用**: 复用频繁创建/销毁的对象，减少 GC 压力

**基本实现**:
```csharp
public class ObjectPool<T> where T : new()
{
    private Stack<T> pool = new Stack<T>();

    public T Get()
    {
        return pool.Count > 0 ? pool.Pop() : new T();
    }

    public void Release(T obj)
    {
        // 重置对象状态
        pool.Push(obj);
    }
}
```

**Unity 中使用**:
- 预热（Pre-warm）: 游戏开始时预先生成一定数量对象
- GameObject 版本：维护 inactive GameObject 列表
- 推荐使用 `UnityEngine.Pool.ObjectPool<T>` (Unity 2021+)

---

## 五、工厂模式

### Q8: 简单工厂 vs 工厂方法 vs 抽象工厂？
- **简单工厂**: 一个工厂类根据参数创建不同产品
- **工厂方法**: 工厂基类定义创建接口，子类决定具体创建什么
- **抽象工厂**: 创建一系列相关产品族的工厂

**Unity 应用**: 创建不同类型的敌人、道具、技能等

---

## 六、状态模式 / 有限状态机（FSM）

### Q9: 状态模式在游戏中的应用？

**实现方式**:
1. **简单 FSM**: 使用 enum + switch
2. **状态类**: 每个状态一个类，实现 IState 接口
3. **Animator 状态机**: Unity 内置，适合动画状态

```csharp
public interface IState
{
    void Enter();
    void Update();
    void Exit();
}

public class StateMachine
{
    private IState currentState;

    public void ChangeState(IState newState)
    {
        currentState?.Exit();
        currentState = newState;
        currentState?.Enter();
    }

    public void Update() => currentState?.Update();
}
```

**应用场景**:
- 角色状态管理（待机、行走、攻击、受击）
- AI 行为树配套使用
- UI 界面切换

---

## 七、组件模式

### Q10: 什么是组件模式？
- Unity 本身的核心架构模式
- 将不同功能分散到独立的 Component 中
- 每个 Component 负责单一功能
- 组合优于继承

**示例**: 一个 "敌人" 由 MeshFilter + MeshRenderer + Collider + EnemyAI + Health 等多个 Component 组合而成

---

## 八、其他常用模式

### Q11: 命令模式的应用？
- RTS 单位命令队列
- 回放系统（存储操作序列）
- 撤销/重做功能

### Q12: 策略模式的应用？
- AI 行为切换（巡逻、追击、逃跑）
- 伤害计算公式选项
- 资源加载策略选择

### Q13: 外观模式？
- 提供统一的接口访问多个子系统
- 例如：AudioManager 封装背景音乐、音效等多个 AudioSource 管理

### Q14: 依赖注入（DI）在 Unity 中的应用？
- 使用构造函数注入或属性注入
- 减少 GameObject.Find / FindObjectOfType 的耦合
- 常用框架：Zenject / VContainer

---

## 九、设计模式面试速查

| 模式 | 核心作用 | 游戏应用 |
|------|---------|---------|
| 单例 | 全局唯一实例 | GameManager, AudioManager |
| 观察者 | 一对多通知 | UI 更新, 成就系统 |
| 对象池 | 对象复用 | 子弹, 敌人生成 |
| 工厂 | 对象创建分离 | 道具生成, 敌人创建 |
| 状态 | 行为随状态变化 | 角色状态, 游戏流程 |
| 组件 | 功能拆分组合 | Unity 核心架构 |
| 命令 | 请求封装 | 操作队列, 回放 |
| 策略 | 算法可替换 | AI 行为, 伤害公式 |
| 外观 | 统一接口 | 复杂系统的简化入口 |
| 桥接 | 抽象实现分离 | 跨平台渲染 |

---

> 来源: unitykit/unityClientInterviewGuide, Lafree317/Unity-InterviewQuestion
