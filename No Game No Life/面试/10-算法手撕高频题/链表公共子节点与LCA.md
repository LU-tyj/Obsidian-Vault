---
title: "链表公共子节点与LCA"
category: 算法手撕高频题
tags: [算法, 手撕代码, 链表, LCA, 二叉树, 网易互娱]
frequency: ⭐⭐
difficulty: 中等
companies: [网易互娱, 网易雷火]
status: new
last_reviewed: 
next_review: 
related:
  - "[[链表高频操作]]"
  - "[[二叉树高频操作]]"
  - "[[反转链表]]"
---

## 🎯 一句话结论（自测用）
> 链表公共子节点：双指针遍历 A+B 和 B+A，首次相等即为交点。二叉树 LCA：递归，`if(root==p||root==q) return root`，看左右子树结果。

## ✅ 标准答案（结构化、可背诵，2分钟内讲完）
1. **链表相交节点**：pA 走 A->B，pB 走 B->A，首次相遇点即交点。O(m+n) 时间 O(1) 空间
2. **二叉树 LCA**：递归。root 等于 p 或 q 则返回 root；否则递归左右子树。左右都非空则 root 是 LCA，否则返回非空那边
3. **BST LCA**：利用 BST 性质，如果 p 和 q 在同一侧则去那一侧递归，否则 root 是 LCA。O(h) 时间

## 🔍 详细解析

### 链表相交节点（LeetCode 160）
```cpp
ListNode* getIntersectionNode(ListNode* headA, ListNode* headB) {
    ListNode *pA = headA, *pB = headB;
    while (pA != pB) {
        pA = pA ? pA->next : headB;
        pB = pB ? pB->next : headA;
    }
    return pA;  // 可能为 null（无交点）
}
```
**原理**：消除长度差。设 A 长度 a+c（c 为公共部分），B 长度 b+c。pA 走 a+c+b 步，pB 走 b+c+a 步，同时到达交点。

### 二叉树 LCA（LeetCode 236）
```cpp
TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
    if (!root || root == p || root == q) return root;
    
    TreeNode* left = lowestCommonAncestor(root->left, p, q);
    TreeNode* right = lowestCommonAncestor(root->right, p, q);
    
    if (left && right) return root;   // p 和 q 分别在左右子树
    return left ? left : right;        // 在同一侧，或都不在
}
```
时间复杂度 O(n)，空间 O(h)。

### BST LCA（LeetCode 235）
```cpp
TreeNode* lowestCommonAncestorBST(TreeNode* root, TreeNode* p, TreeNode* q) {
    // 保证 p->val <= q->val（方便比较）
    if (p->val > q->val) swap(p, q);
    
    while (root) {
        if (root->val > q->val)       // 都在左子树
            root = root->left;
        else if (root->val < p->val)  // 都在右子树
            root = root->right;
        else                          // root 在 [p, q] 之间，即 LCA
            return root;
    }
    return nullptr;
}
```
时间复杂度 O(h)，空间 O(1)。

### Csharp 版本
```csharp
// 链表相交节点
public ListNode GetIntersectionNode(ListNode headA, ListNode headB)
{
    ListNode pA = headA, pB = headB;
    while (pA != pB)
    {
        pA = pA == null ? headB : pA.next;
        pB = pB == null ? headA : pB.next;
    }
    return pA;
}

// 二叉树 LCA
public TreeNode LowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q)
{
    if (root == null || root == p || root == q) return root;
    var left = LowestCommonAncestor(root.left, p, q);
    var right = LowestCommonAncestor(root.right, p, q);
    if (left != null && right != null) return root;
    return left ?? right;
}
```

## 💬 面试官常见追问
- "链表相交的双指针为什么不会死循环？" -> 即使无交点，两个指针都会走完 A+B，同时到达 null，循环结束
- "LCA 递归方法中，如果 p 是 q 的祖先会怎样？" -> 递归到 p 时直接返回 p，右侧返回 null，最终返回 p。天然处理
- "LCA 有迭代解法吗？" -> 可以先用哈希表存储每个节点的父节点，再向上遍历。但递归解法更简洁

## ⚠️ 我曾经的误区 / 网上常见错答
- **误区**：链表相交用哈希表存 A 的所有节点再遍历 B。O(n) 空间，双指针 O(1) 空间更优
- **误区**：LCA 忘了处理 p/q 在树中不存在的情况。大多数面试假设 p 和 q 一定存在
- **误区**：BST LCA 用普通二叉树的方法（O(n)）。用 BST 性质可以 O(h)

## 🔗 关联知识点
- [[链表高频操作]]
- [[二叉树高频操作]]
- [[反转链表]]

## 📎 原始出处
- 006_互娱 Q14: 两个链表求公共子节点
- 003_互娱 Q6: LCA 算法
