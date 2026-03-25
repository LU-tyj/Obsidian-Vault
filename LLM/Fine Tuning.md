## 1  Introduction
![[Overview_of_LLMs.png]]
### 1.1 Definition
**Fine-tuning（微调）** 是在预训练大语言模型基础上，使用任务或领域数据继续训练，使模型能力对齐特定目标（如问答、指令遵循、领域知识、偏好对齐）。

### 1.2 Motivation
- **领域适配**：预训练语料与业务域（医疗/法律/金融）分布偏移
    
- **指令遵循与对齐**：减少幻觉，提高安全与可控性
    
- **任务特化**：摘要、对话、信息抽取、代码生成
    
- **成本与效率**：通过参数高效微调（PEFT）降低算力与存储

### 1.3 Types of Fine-tuning
-  **SFT（Supervised Fine-Tuning）**
	使用高质量指令-响应对（Instruction-Response pairs）进行监督学习，来处理目标任务，比如分类问题。
- **Instruction Fine-Tuning via Prompt Engineering**
	使用“指令-响应对”对模型进行监督微调（SFT），让模型“内化”指令遵循能力。
- **Unsupervised Fine-Tuning**
	用非标记数据进行微调

### 1.4 Fine-tuning vs RAG（检索增强生成）
**RAG（Retrieval-Augmented Generation）** 是指将外部知识检索结果拼接到 Prompt 中，不改变模型参数。
RAG 的具体流程为：根据用户的问题搜索向量库中相似的内容，拼接到提示词中。更新简单，不需要额外训练，因此对算力消耗小。

![[RAG_vs_Fine_tuning.png]]

---

## 2 Fine-tuning Pipeline for LLM
![[Fine-tuning_LLM_process.jpg]]

### 2.1 Dataset Preparation
微调需要正确、规范的数据集或者QA，通常是 `<input, output>` 对（instruction fine-tuning）。

### 2.2 Model Initialisation
选择合适的 pre-trained model，并加载 pre-trained weights。

### 2.3 Training Setup
设置超参数，设置训练数据，设置 `optimisers` 和 `loss function`。

### 2.4 Fine-tuning
选择合适的微调方案，在[[Fine Tuning#3 Techniques of Fine-tuning]]会有提及。

### 2.5 Validation&Evaluation
在测试集和验证集上测试微调的结果。

> 剩下的就是微调后的模型的部署和维护

---

## 3 Techniques of Fine-tuning
### 3.1 Steps Involved in Fine-Tuning
1.  **Initialise the Pre-Trained Tokenizer and Model.** 
2. **Modify the Model’s Output Layer.** 
	调整 Output layer 来适应目标任务，比如针对分类任务添加softmax层，对于文字生成任务改变 decoding 机制。
3. **Choose an Appropriate Fine-Tuning Strategy.**  
	比如Task-Specific Fine-Tuning；Domain-Specific Fine-Tuning；PEFT；HFT。
4. **Set Up the Training Loop.**
	包括data loading, loss computation, backpropagation, and parameter updates。
5. **Incorporate Techniques for Handling Multiple Tasks.**
	针对多任务的微调可以使用 multiple adapters 或 MoE
6. **Monitor Performance on a Validation Set.**
	根据在Validation set上的表现，修改超参数（比如`batch_num, lr dropout_rate`）。
7. **Prune and optimise the Model (if necessary).**
8. **Continuous Evaluation and Iteration.**

### 3.2 PEFT techniques
![[Taxonomy_of_PEFT.png]]
Parameter Efficient Fine Tuning [(PEFT)](https://github.com/huggingface/peft) 是只微调一部分模型参数，减少算力的开销。主要介绍LoRA为代表的方法。

#### 3.2.1 Adapters
添加额外的可训练参数或者全连接层，只对这些参数进行更新。

#### 3.2.2 LoRA and QLoRA
Low-Rank Adaptation (LoRA) 通过引入一个低秩矩阵 $ΔW=BA$ 来近似参数更新方向，从而冻结原矩阵的参数，只需要对A、B进行训练。
QLoRA则是在LoRA的基础上对权重进行量化。
以及DoRA是在LoRA的基础上，加入了weight这个标量这个训练参数。
![[Fine-tuning_vs_LoRA.png]]

### 3.3 HFT
冻结一半模型参数，对另一半进行调整。
![[Half_Fine_Tuning.jpg]]

---

## Reference
1. [Hugging Face LLM-course](https://huggingface.co/learn/llm-course/) : Hugging Face上关于LLM的教程
2. [The Ultimate Guide to Fine](https://arxiv.org/html/2408.13296v1) : 详细的微调种类和微调方法
3. [LLMs from scratch](https://github.com/rasbt/LLMs-from-scratch): 第6章包含分类LLM微调的具体教程
4. [RAG 简单介绍](https://www.bilibili.com/video/BV1JLN2z4EZQ/?spm_id_from=333.337.search-card.all.click&vd_source=ad716d3306df63ce18d6c86f46fec345) : 通俗易懂介绍 RAG 的原理