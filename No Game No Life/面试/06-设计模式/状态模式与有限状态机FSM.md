---
title: "状态模式与有限状态机FSM"
category: 设计模式
tags: [设计模式, 状态模式, FSM, 游戏AI, 网易互娱]
frequency: ⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed: 
next_review: 
related:
  - "[[ECS架构与组件模式]]"
  - "[[命令模式与策略模式]]"
  - "[[单例模式]]"
---

## 🎯 一句话结论（自测用）
> 状态模式让对象行为随状态变化。游戏实现三方案：enum+switch（简单）、IState接口（解耦）、Animator状态机（动画状态）。角色状态管理、AI行为、UI切换都用它。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **状态模式定义**：允许对象在内部状态改变时改变其行为，看起来像换了类
2. **三种实现方式**：
   - **简单 FSM**：`enum + switch`，适合状态少且逻辑简单
   - **状态类**：每个状态一个类实现 `IState` 接口（Enter/Update/Exit），适合复杂状态逻辑
   - **Animator 状态机**：Unity 内置，适合动画状态切换（带混合过渡）
3. **应用场景**：角色状态（待机/行走/攻击/受击）、AI 行为（巡逻/追击/逃跑）、UI 界面切换、游戏流程（菜单/游戏中/暂停/结算）
4. **状态模式 vs 行为树**：状态机适合简单线性切换，行为树适合复杂 AI 决策

## 🔍 详细解析

### 方案一：enum + switch（简单 FSM）
```csharp
public enum PlayerState { Idle, Walk, Attack, Hurt }

public class Player : MonoBehaviour
{
    private PlayerState state = PlayerState.Idle;

    void Update()
    {
        switch (state)
        {
            case PlayerState.Idle: /* ... */ break;
            case PlayerState.Walk: /* ... */ break;
            case PlayerState.Attack: /* ... */ break;
        }
    }
}
```
优点：简单直观。缺点：switch 膨胀快，难扩展。

### 方案二：状态类（IState 接口，推荐）
```csharp
public interface IState
{
    void Enter();
    void Update();
    void Exit();
}

public class IdleState : IState
{
    private Player player;
    public IdleState(Player p) => player = p;
    public void Enter() { /* 播放 Idle 动画 */ }
    public void Update() { if (Input.GetKey(KeyCode.W)) player.ChangeState(new WalkState(player)); }
    public void Exit() { }
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
优点：每个状态独立、易扩展。缺点：类数量多。

### 方案三：Animator 状态机
Unity Mecanim 系统，通过 Animator Controller 配置状态和过渡条件。
```csharp
animator.SetBool("IsWalking", true);
animator.SetTrigger("Attack");
```
优点：可视化编辑、支持混合过渡。缺点：仅适合动画相关的状态，不适合纯逻辑状态。

### 三种方案对比
| | enum+switch | IState 类 | Animator |
|--|------------|-----------|----------|
| 状态耦合 | 高 | 低 | 中 |
| 代码量 | 少 | 多 | 少（可视化） |
| 灵活性 | 低 | 高 | 中（限动画） |
| 维护性 | 差（switch 膨胀） | 好 | 好 |

### 状态模式 vs 行为树
| | 状态机 | 行为树 |
|--|--------|--------|
| 适用 | 简单线性状态切换 | 复杂 AI 决策 |
| 可复用性 | 低 | 高（节点可复用） |
| 调试 | 简单 | 容易可视化 |
| 游戏示例 | 角色基础状态 | 敌人 AI（巡逻/侦查/战斗） |

## 💬 面试官常见追问
- "FSM 和行为树的区别？什么时候用哪个？" -> FSM 适合简单切换（角色状态），行为树适合复杂决策（BOSS AI）
- "状态模式如何避免状态爆炸？" -> 分层状态机（Hierarchical FSM），子状态共享父状态的逻辑
- "状态切换时需要注意什么？" -> 正确清理前一个状态（Exit 中取消订阅/Timer）、防止循环切换

## ⚠️ 我曾经的误区 / 网上常见错答
- **误区**：FSM 和状态模式是一回事。状态模式是 GoF 设计模式，FSM 是具体实现方式。状态模式可以不用 FSM 实现
- **误区**：Animator 可以替代所有状态机。Animator 适合动画状态，不适合纯逻辑状态（如网络状态、游戏流程控制）

## 🔗 关联知识点
- [[ECS架构与组件模式]]
- [[命令模式与策略模式]]
- [[单例模式]]

## 📎 原始出处
- 012_互娱 Q22: 有限状态机（FSM）项目追问
- GitHub Q9: 状态模式实现方式（enum+switch / IState / Animator）、IState 接口代码
- GitHub Q22: 行为树 vs 状态机
- 博客园 3.1: 设计模式参考
