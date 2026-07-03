---
title: "Interface与AbstractClass"
category: Csharp语言基础
tags: [Csharp, Unity, 网易互娱, 面向对象]
frequency: ⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[重载与重写]]"
  - "[[Csharp 反射]]"
---

## 一句话结论（自测用）
> Interface 定义"能做什么"（契约），可以多实现；Abstract Class 定义"是什么"（基类），可以包含实现，只能单继承。接口用于跨层次的能力定义，抽象类用于代码复用。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **核心差异表**：

| | Interface | Abstract Class |
|--|-----------|----------------|
| 继承 | 可多实现 | 只能单继承 |
| 成员实现 | 不能有实现（Csharp 8.0 前），Csharp 8.0+ 可有默认实现 | 可以有实现 |
| 构造函数 | 不能有 | 可以有 |
| 字段 | 不能声明字段 | 可以声明字段 |
| 访问修饰符 | 默认 public（不能修改） | 任意修饰符 |
| 实例化 | 不能 | 不能 |
| 使用意图 | "能做某事"（契约） | "是一种"（is-a 关系） |

2. **什么时候用接口**：
   - 不相关的类需要共享同一组行为（如 `IDisposable` 既用于文件又用于网络连接）
   - 需要多继承行为
   - 定义插件/扩展点（如 Unity 的 `IPointerClickHandler`）
3. **什么时候用抽象类**：
   - 相关类有共享代码需要复用
   - 需要非 public 成员
   - 版本控制——抽象类加新方法可提供默认实现，接口加新方法会破坏已有实现（Csharp 8.0 默认接口方法缓解了此问题）
4. **Csharp 8.0 默认接口方法**：接口可以有方法体，实现类可覆盖也可不覆盖。但这不改变接口的本质——仍然不能声明字段/构造函数。

## 详细解析

### Unity 中的接口使用典范
```csharp
// 伤害系统：任何能受伤的东西
public interface IDamageable {
    void TakeDamage(float damage);
}

// 两个完全不相关的类，实现同一个接口
public class Player : MonoBehaviour, IDamageable { ... }
public class DestructibleWall : MonoBehaviour, IDamageable { ... }

// 调用方不需要知道具体类型
void ApplyDamage(GameObject target, float damage) {
    target.GetComponent<IDamageable>()?.TakeDamage(damage);
}
```

### Unity 抽象类使用场景
```csharp
// 所有敌人的共同基类：HP、受伤逻辑已经有实现
public abstract class EnemyBase : MonoBehaviour {
    protected float hp;
    protected virtual void Die() { Destroy(gameObject); }
    public abstract void Attack(); // 子类必须实现
}
```

## 面试官常见追问
- 接口可以有静态方法吗？（Csharp 8.0+ 可以，但不能从实例调用，只能 `IInterface.StaticMethod()` 直接调用）
- 抽象类可以有非抽象方法吗？（可以，抽象类 = 必须被继承 + 可以包含抽象方法 + 可以有已实现方法）
- `abstract` 和 `virtual` 方法的区别？（abstract 必须被子类重写，没有方法体；virtual 可以被子类重写，有默认实现）
- 为什么 Csharp 不允许多继承类？（菱形继承的二义性问题——相同基类的成员/方法通过不同路径继承，不知道用哪个）

## 我曾经的误区 / 网上常见错答
- **错**："接口就是全抽象的抽象类" —— 接口是契约/能力定义，抽象类是代码复用，设计意图不同
- **错**："Csharp 不支持多继承" —— Csharp 不支持多继承类，但通过接口实现多行为继承
- **错**："接口不能有任何实现" —— Csharp 8.0 起可以有默认实现

## 关联知识点
- [[重载与重写]]
- [[Csharp 反射]]
- [[struct与class的区别]]

## 原始出处
- GitHub面经_CSharp基础 Q19
- 博客园 梦幻事业部外包面经 Q5
