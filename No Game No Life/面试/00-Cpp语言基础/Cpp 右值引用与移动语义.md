---
title: "Cpp 右值引用与移动语义"
category: Cpp语言基础
tags: [Cpp, C++11, 移动语义, 右值引用, 网易互娱]
frequency: ⭐⭐
difficulty: 困难
companies: [网易互娱, 网易雷火]
status: new
last_reviewed:
next_review:
related:
  - "[[Cpp 指针与引用]]"
  - "[[Cpp 深拷贝与浅拷贝]]"
  - "[[Cpp 智能指针]]"
  - "[[Cpp C++11新特性]]"
---

## 一句话结论（自测用）
> 左值 = 可取地址的持久对象；右值 = 临时对象/字面量（不可取地址）。`&&` 是右值引用，绑定右值后可以"偷"其资源（移动而非拷贝）。`std::move` 将左值转为右值引用，`std::forward` 保持值类别完美转发。游戏传递大资源（纹理、模型数据）时必须用移动避免深拷贝。

## 标准答案（结构化、可背诵，2分钟内讲完）
1. **左值 vs 右值**：
   - 左值：可取地址、有名字、持久存在（如变量 `int a = 5;`，a 是左值）
   - 右值：不可取地址、临时对象/字面量（如 `5`、`std::string("temp")`、函数返回的临时对象）
   - 有一个简单判断法：能放在赋值号左边的通常就是左值，但不绝对
2. **右值引用 `T&&`**：可以绑定到右值的引用。让编译器知道这个对象"即将被销毁，可以安全窃取其资源"。
3. **移动构造函数与移动赋值**：
   - 移动构造函数：`ClassName(ClassName&& other) noexcept` — 窃取 other 的资源（如指针），将 other 置为安全析构状态
   - 移动赋值运算符：类似，释放自身旧资源，窃取 other 资源
4. **std::move**：无条件将左值转为右值引用（cast to rvalue）。注意：move 本身不移动任何东西，只是类型转换
5. **std::forward**：有条件转发——传入左值则转发为左值引用，传入右值则转发为右值引用。用于完美转发。

## 详细解析

### 移动赋值的标准写法
```cpp
class MyVector {
    int* data;
    size_t size;
public:
    // 移动构造函数
    MyVector(MyVector&& other) noexcept
        : data(other.data), size(other.size) {
        other.data = nullptr;  // 让 other 安全析构
        other.size = 0;
    }
    // 移动赋值
    MyVector& operator=(MyVector&& other) noexcept {
        if (this != &other) {
            delete[] data;
            data = other.data;
            size = other.size;
            other.data = nullptr;
            other.size = 0;
        }
        return *this;
    }
};
```

### 为什么不需要用 std::move 返回局部对象
编译器会做 RVO/NRVO 优化，直接在调用方栈帧上构造对象。如果加上 `std::move`，反而阻止了 RVO（因为类型变了），导致额外的移动构造调用。

### 引用折叠规则
- `T& &` → `T&`
- `T& &&` → `T&`
- `T&& &` → `T&`
- `T&& &&` → `T&&`

只有右值引用的右值引用才保持右值引用，其余全折叠为左值引用。这是 `std::forward` 实现的基础。

## 面试官常见追问
- move 之后对象还能用吗？（处于"有效但未指定"状态，可以安全析构或赋新值，但不要读其内容）
- 移动构造为什么加 noexcept？（vector 扩容时如果移动构造不是 noexcept，会用拷贝代替移动来保证异常安全）
- 什么时候该写移动构造函数？（类管理堆资源时，如 vector、string 等大对象）
- forward 和 move 区别？（move = 无条件转为右值，forward = 有条件转发保持原始值类别）

## 我曾经的误区 / 网上常见错答
- **错**："std::move 执行了移动操作" —— 它只是一个 static_cast，真正的移动由移动构造函数/移动赋值完成
- **错**："移动后原来的对象就销毁了" —— 对象仍在，只是资源被窃取，处于空状态
- **错**："返回局部变量要用 std::move" —— 反而阻止 RVO 优化，直接 return 即可

## 关联知识点
- [[Cpp 指针与引用]]
- [[Cpp 深拷贝与浅拷贝]]
- [[Cpp 智能指针]]
- [[Cpp C++11新特性]]

## 原始出处
- 史上最全的C++游戏开发面试问题总结（一）——C++基础
- 常见面试题整理——C++（游戏客户端）
- 牛客网 014/020 网易互娱面经
