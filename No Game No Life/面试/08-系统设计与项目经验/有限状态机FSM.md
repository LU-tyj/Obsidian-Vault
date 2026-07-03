---
title: "有限状态机FSM"
category: 系统设计与项目经验
tags: [系统设计, FSM, 状态模式, AI, Unity, 网易互娱]
frequency: ⭐⭐
difficulty: 简单
companies: [网易互娱]
status: new
last_reviewed:
next_review:
related:
  - "[[设计模式在游戏开发中的应用]]"
---

## 🎯 一句话结论（自测用）
> FSM 用于管理对象在不同状态间的转换和对应行为。三种实现：enum+switch（最简单但难扩展）、状态类+IState 接口（灵活可扩展）、Animator 状态机（动画直观但逻辑耦合）。应用：角色状态（待机/移动/攻击/受击）、AI 行为、UI 界面切换、游戏流程控制。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **FSM 三要素**：状态（State）、转换条件（Transition）、动作（Action）。
2. **实现方式对比**：
   - **enum + switch**：最简单直观，适合状态少的简单逻辑。缺点：状态多时代码膨胀、难以扩展
   - **状态类 + IState 接口**：每个状态封装为独立类，状态机管理当前状态。优点：开闭原则、易扩展、复用性强
   - **Animator 状态机**：Unity Mecanim 提供可视化编辑，适合动画状态管理。缺点：逻辑与动画耦合，性能开销较大
3. **应用场景**：
   - 角色状态：Idle -> Walk -> Run -> Attack -> Hit -> Die
   - AI 巡逻：Patrol（巡逻） -> Chase（追击玩家） -> Attack（攻击） -> Return（返回）
   - UI 界面切换：MainMenu -> Settings -> InGame -> Pause -> GameOver
   - 游戏流程：Loading -> Playing -> Paused -> GameOver

## 🔍 详细解析

### IState 接口实现
```csharp
public interface IState
{
    void Enter();   // 进入状态时
    void Update();  // 每帧更新
    void Exit();    // 离开状态时
}

public class IdleState : IState
{
    private Player player;
    public IdleState(Player p) { player = p; }
    public void Enter() { player.animator.Play("Idle"); }
    public void Update() { 
        if (player.HasInput) player.fsm.ChangeState(new WalkState(player));
    }
    public void Exit() { /* 清理 */ }
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

### FSM vs 行为树
| 对比 | FSM | 行为树 |
|------|-----|--------|
| 复杂度 | 低 | 中-高 |
| 可扩展性 | 有限（状态多时爆炸） | 好（组合节点） |
| 调试可视化 | 一般 | 好 |
| 适用场景 | 简单到中等复杂度 AI | 复杂行为/AI |
| Unity 支持 | Animator FSM | Behavior Designer 等插件 |

### Animator FSM 的优缺点
优点：可视化编辑、动画过渡自然、对美术友好
缺点：每帧更新较多 Animator 时 CPU 开销大、逻辑不能完全表达（需要配合脚本）、参数传递不便

## 💬 面试官常见追问
- **Animator FSM 有什么性能问题？** → 每个 Animator 组件每帧都在计算状态转换条件，大量角色时 CPU 开销显著；Animator 的 Controller 占用内存较大
- **怎么优化 Animator FSM？** → 远处角色降低更新频率（Culling Mode）、减少 Layer 数量、合并 Controller、使用 Playable API
- **FSM 状态爆炸怎么解决？** → 引入层级状态机（Hierarchical FSM）或使用行为树替代

## ⚠️ 我曾经的误区 / 网上常见错答
- 误区：FSM 只能用于 AI。FSM 是通用的状态管理框架，UI 切换、游戏流程控制都可以用
- 误区：Animator FSM 可以做所有状态管理。Animator 设计目的是动画状态，非动画逻辑应分离

## 🔗 关联知识点
- [[设计模式在游戏开发中的应用]]
- [[事件系统与观察者模式]]

## 📎 原始出处
- GitHub面经_设计模式 Q9：状态模式在游戏中的应用
- 牛客网 012 Q22：有限状态机 FSM
