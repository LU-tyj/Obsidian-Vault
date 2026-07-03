---
title: "MVC与MVVM"
category: 设计模式
tags: [设计模式, MVC, MVVM, 架构, 网易互娱]
frequency: ⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed: 
next_review: 
related:
  - "[[ECS架构与组件模式]]"
  - "[[观察者模式与事件系统]]"
---

## 🎯 一句话结论（自测用）
> MVC：Model（数据）+ View（显示）+ Controller（逻辑，用户输入）。MVVM：ViewModel 替代 Controller，通过数据绑定（Binding）自动同步 View 和 Model。Unity UI 常用 MVP 或 MVVM + UniRx 实现。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **MVC（Model-View-Controller）**：
   - Model：数据和业务逻辑
   - View：UI 显示
   - Controller：处理用户输入，更新 Model，通知 View 刷新
   - 问题：Controller 容易臃肿，View 和 Controller 耦合
2. **MVP（Model-View-Presenter）**：
   - Presenter 持有 View 引用，主动更新 View。View 只负责渲染，不感知 Model
3. **MVVM（Model-View-ViewModel）**：
   - ViewModel 替代 Controller，通过数据绑定（Binding）自动同步
   - View 和 ViewModel 完全解耦，适合 WPF/XAML/Unity UI
4. **游戏中的应用**：UI 管理（背包、商城主界面用 MVP/MVVM）、编辑器工具（MVC）

## 🔍 详细解析

### 三种架构对比
| | MVC | MVP | MVVM |
|--|-----|-----|------|
| View 和 Model 的关系 | View 知道 Model | View 不知道 Model | View 不知道 Model |
| 中间层 | Controller | Presenter | ViewModel |
| 更新方式 | View 拉取/Controller 推送 | Presenter 调用 View 接口 | 数据绑定自动同步 |
| 测试性 | Controller 较难测试 | Presenter 可 Mock View | ViewModel 可独立测试 |
| Unity 适用 | 基本可用 | 推荐（易测试） | 需要绑定框架（UniRx） |

### MVC in Unity 示例
```csharp
// Model
public class PlayerModel
{
    public int Health { get; set; }
    public event Action<int> OnHealthChanged;
}

// View
public class HealthBarView : MonoBehaviour
{
    public Slider healthSlider;
    public void UpdateHealth(int health) => healthSlider.value = health;
}

// Controller
public class PlayerController : MonoBehaviour
{
    private PlayerModel model = new();
    private HealthBarView view;

    void Start() => view = GetComponent<HealthBarView>();
    
    public void TakeDamage(int damage)
    {
        model.Health -= damage;
        view.UpdateHealth(model.Health);
    }
}
```

### MVVM in Unity（使用 UniRx）
```csharp
// ViewModel
public class PlayerViewModel
{
    public ReactiveProperty<int> Health { get; } = new(100);
    public void TakeDamage(int d) => Health.Value -= d;
}

// View（自动绑定，无需手动调用 UpdateHealth）
public class HealthBarView : MonoBehaviour
{
    public Slider healthSlider;
    public PlayerViewModel viewModel;

    void Start()
    {
        viewModel.Health
            .Subscribe(h => healthSlider.value = h)
            .AddTo(this);  // 自动管理生命周期
    }
}
```

### 游戏 UI 框架选型建议
| 场景 | 推荐架构 | 原因 |
|------|---------|------|
| 简单 UI | 无框架 / Controller | 不必要引入复杂度 |
| 复杂 UI 系统（背包/商城） | MVP | Presenter 可独立测试 |
| 数据驱动 UI（WPF/编辑器） | MVVM | 数据绑定省代码 |
| UI 框架选型 | StrangeIoC / Zenject | 成熟 IOC 框架 |

## 💬 面试官常见追问
- "为什么 MVVM 比 MVC 好测试？" -> ViewModel 不依赖 View，可以纯 UnitTest。MVC 的 Controller 需要 Mock View
- "Unity 中如何实现数据绑定？" -> UniRx 的 ReactiveProperty、INotifyPropertyChanged、自定义 BindableProperty
- "MVVM 和观察者模式的关系？" -> MVVM 的数据绑定本质上是观察者模式的自动化版本

## ⚠️ 我曾经的误区 / 网上常见错答
- **误区**：MVC 中 Model 可以直接更新 View。MVC 标准中 View 应该通过观察者模式从 Model 获取更新，Controller 负责协调
- **误区**：MVVM 一定比 MVC 好。小项目引入 MVVM（需要额外框架）是过度设计
- **误区**：Unity 只能用 MVC。Unity 本身是组件模式，MVC 是上层 UI 架构选择

## 🔗 关联知识点
- [[ECS架构与组件模式]]
- [[观察者模式与事件系统]]
- [[命令模式与策略模式]]

## 📎 原始出处
- 005_雷火 Q2: MVC/MVVM 对比
