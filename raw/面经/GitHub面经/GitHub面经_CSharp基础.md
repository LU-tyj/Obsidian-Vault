---
source_platform: GitHub
source_url:
  - https://github.com/unitykit/unityClientInterviewGuide
  - https://github.com/Lafree317/Unity-InterviewQuestion
  - https://github.com/GuardianOfGods/unity-interview-questions
crawl_date: 2026-07-03
crawl_agent: agent-github
company_mentioned: [通用, 网易互娱]
position: Unity客户端开发
raw: true
---

# C# 基础面试题

## 一、值类型 vs 引用类型

### Q1: 值类型和引用类型的区别？

| 对比维度 | 值类型 | 引用类型 |
|---------|--------|---------|
| 存储位置 | 栈上（或跟随引用类型在堆中） | 堆上，栈中存地址 |
| 继承自 | System.ValueType | System.Object |
| 默认值 | 该类型的默认值（不可为null） | null |
| 赋值行为 | 复制数据副本 | 复制引用地址 |
| GC | 栈自动释放 | 由 GC 回收 |
| 典型代表 | int, float, bool, char, struct, enum | string, object, class, interface, delegate, array |

> 特殊说明：struct 中的 string 成员实际存储在堆上；class 中的 int 成员也存储在堆上。

### Q2: struct 和 class 的区别？
- struct 是值类型，class 是引用类型
- struct 不能继承（但可以实现接口），class 可以继承
- struct 不能有无参构造函数（C# 10.0 之前）
- struct 在栈上分配（性能更高，但不宜过大）

---

## 二、装箱与拆箱

### Q3: 什么是装箱和拆箱？如何避免？

**装箱**：值类型 -> object（堆上分配新对象，数据复制过去）
**拆箱**：object -> 值类型（检查类型后复制回栈）

**避免方法**：
- 使用泛型（List<int> 替代 ArrayList）
- 重写 ToString() 避免 string 拼接中的装箱
- 使用 `yield return null` 代替 `yield return 0`

---

## 三、委托与事件

### Q4: 委托（Delegate）和事件（Event）的区别？

| 对比 | 委托 | 事件 |
|------|------|------|
| 本质 | 类（类型） | 委托类型的实例（对象） |
| 赋值 | 可用 `=` 直接赋值 | 不可用 `=`，只能用 `+=` / `-=` |
| 调用 | 可在类外部调用 | 只能在定义事件的类内部调用 |
| 用途 | 封装方法引用，类型安全的函数指针 | 发布-订阅模式，限制外部直接触发 |

### Q5: Action、Func、Predicate 的区别？
- **Action**：无返回值委托
- **Func**：有返回值委托
- **Predicate**：返回 bool 的委托

---

## 四、GC 垃圾回收

### Q6: GC 的原理是什么？触发时机？

**算法**：标记-清除（Mark-Sweep）+ 分代回收

**工作过程**：
1. 标记阶段：从根对象（GC Root）递归遍历引用链，标记所有可达对象
2. 清除阶段：清理未被标记的对象，释放内存
3. 压缩阶段（可选）：移动存活对象以减少碎片

**触发时机**：
- 第0代内存满时
- 手动调用 `System.GC.Collect()`
- 系统内存不足时

### Q7: GC 如何优化？列出至少 5 种方法

| 优化手段 | 具体做法 |
|---------|---------|
| 减少 new 对象 | 避免在 Update 等高频函数中创建临时对象 |
| 对象池 | 复用频繁创建/销毁的对象 |
| 字符串优化 | 使用 StringBuilder 替代 + 拼接 |
| 容器复用 | List/Dictionary 用 Clear() 而非反复 new |
| 装箱拆箱 | 避免值类型转 object |
| 使用 CompareTag | 用 CompareTag() 替代 tag == "xxx" |
| 射线检测 | 使用 RaycastNonAlloc 系列方法 |
| 缓存组件引用 | 避免每帧 GetComponent / Find |

### Q8: 什么是 GC Root？
GC Root 是一组被认为是始终可达的对象引用，包括：
- 静态变量
- 当前执行线程的栈上的局部变量
- CPU 寄存器中的对象引用
- 已终结队列中的对象

---

## 五、集合

### Q9: List 底层实现原理？
- 基于动态数组实现
- 初始容量为 0 或指定值
- Add 时若容量不足，扩容为原来的 2 倍
- 插入/删除需要移动元素（O(n)）
- 优化删除：将末尾元素交换到删除位置，再移除末尾（O(1)）

### Q10: Dictionary 底层实现原理？
- 基于哈希表（拉链法解决冲突）
- 核心结构：buckets 数组 + entries 数组
- buckets 存 entry 索引，entries 存 key/value/hash/next
- 查找流程：hashCode -> bucket -> entry -> 对比 key
- 扩容：当 entries 数量达到容量时，扩容为大于当前容量 2 倍的最小质数

### Q11: ArrayList vs List\<T\>
- ArrayList 存储 object，存在装箱拆箱
- List\<T\> 是泛型，类型安全，无装箱
- 推荐使用 List\<T\>

---

## 六、反射

### Q12: 反射的原理及使用场景？

**原理**：运行时动态获取程序集中的类型信息（元数据）

**核心类**（System.Reflection）：
- `Assembly` -- 描述程序集
- `Type` -- 描述类
- `MethodInfo` -- 描述方法
- `FieldInfo` -- 描述字段
- `PropertyInfo` -- 描述属性

**使用场景**：
- 编辑器扩展（Inspector 面板动态显示）
- 序列化/反序列化
- 依赖注入框架
- 特性（Attribute）处理

### Q13: typeof() 和 GetType() 的区别？
- `typeof()`：编译时获取类型（不能用于实例）
- `GetType()`：运行时获取实例的类型

---

## 七、异步编程

### Q14: async/await 的原理？
- async 标记方法是异步方法
- await 等待异步操作完成，不阻塞线程
- 编译器将 async 方法转化为状态机
- Unity 中异步操作也可用协程

### Q15: 协程 vs 线程
| 对比 | 协程 | 线程 |
|------|------|------|
| 执行线程 | 主线程 | 独立线程 |
| 调度 | Unity 内部调度 | OS 调度 |
| 开销 | 低 | 高 |
| 数据共享 | 天然安全 | 需加锁 |
| 适用场景 | 分帧操作、异步加载 | 密集计算（配合 Job System） |

---

## 八、其他高频题

### Q16: ref vs out
- ref：传入前必须初始化，方法内可读可写
- out：传入前可不初始化，方法内必须赋值

### Q17: 重载（Overload）vs 重写（Override）
- 重载：同一类中方法名相同、参数不同
- 重写：子类用 override 重写父类 virtual/abstract 方法

### Q18: const vs readonly
- const：编译时常量，隐式 static
- readonly：运行时常量，可在构造函数中赋值

### Q19: Interface vs Abstract Class
| | Interface | Abstract Class |
|--|-----------|----------------|
| 多继承 | 支持 | 不支持 |
| 成员实现 | 不能有实现（C# 8.0 前） | 可以有实现 |
| 构造函数 | 无 | 有 |
| 访问修饰符 | 默认 public | 可任意修饰符 |

### Q20: string vs StringBuilder
- string 不可变，每次修改创建新对象
- StringBuilder 可变，频繁修改场景使用

---

> 来源: unitykit/unityClientInterviewGuide, Lafree317/Unity-InterviewQuestion, GuardianOfGods/unity-interview-questions
