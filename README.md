### Stochastic Fundamental Diagram Modeling based on Maximum entropy principle 
**Official Code Repository for the Article：**  
[On the Stochastic Fundamental Diagram: A General Micro-Macroscopic Traffic Flow Modeling Framework](https://doi.org/10.1016/j.commtr.2025.100163)  

![SFD Illustration](https://github.com/user-attachments/assets/6244bcb9-83f5-424b-8183-b468a0c37753)


### 📖 Overview / 简介  

Traffic fundamental diagram and its inherent **stochasticity** remain key challenges in traffic flow theory.  
This repository provides the implementation of the **Leader-Follower Conditional Distribution-based Stochastic Traffic Modeling (LFCD-STM)** framework — a novel approach bridging **microscopic stochastic behavior** and **macroscopic traffic fundamental diagram**.
交通流基本图及其**内生随机性**仍是交通流理论中的关键难题。  
本仓库提供了 **基于前后车条件分布的随机交通流建模（LFCD-STM）** 框架的实现，该方法创新性地将**微观随机行为**与**宏观交通特性**联系起来。 

### 🔑 Key Contributions / 主要贡献
- 📊 Probabilistic representation of leader-follower behavior/提出了前后车交互的**概率表示方法**    
- 🔗 Markov chain principle for platoon modeling/基于**马尔可夫链原理**建立车队联合分布  
- 📈 Analytical mean and variance functions of the stochastic fundamental diagram (SFD)/推导了随机基本图的**均值与方差解析函数** 
- ✅ Validation on **NGSIM I-80**, **US-101**, and **HighD** datasets/在 **NGSIM I-80**、**US-101**、**HighD** 数据集上验证有效性  


### 🗂️ Code Components / 代码说明  

| File | Purpose (English) | 功能（中文） |
|------|-------------------|-------------|
| **`fd_data.py`** | Aggregate the Fundamental Diagram (FD) from trajectory data | 从轨迹数据聚合基本图 |
| **`fd_data_frame.py`** | Aggregate the FD from each frame of trajectory data | 基于每一帧轨迹数据聚合基本图 |
| **`fd_fit.py`** | Fit the FD using the aggregated FD | 对聚合后的基本图进行拟合 |
| **`filter_data.py`** | Preprocess the trajectory data | 预处理轨迹数据 |
| **`lamda_spacing_calibration.py`** | Calibrate the relation between λ (lambda) and spacing | 校准 λ 参数与车间距的关系 |
| **`max_loglikelihood.py`** | Calibrate λ using maximum entropy distribution | 基于最大熵分布校准 λ 参数 |
| **`mean_std_fill_plot.py`** | Plot the SFD (mean ± std) | 绘制随机基本图（均值 ± 方差） |
| **`micro_change_macro.py`** | Macro change under micro parameter variations | 分析微观参数变化对宏观的影响 |
| **`plot_lamda_spacing.py`** | Plot λ–spacing relation | 绘制 λ–车间距关系 |
| **`sensitive_analysis.py`** | Sensitivity analysis of the derived function | 对推导函数进行敏感性分析 |


### 📚 Citation / 引用  

If you use this code, please cite our paper:  

```bibtex
@article{ZHANG2025100163,
title = {On the stochastic fundamental diagram: A general micro-macroscopic traffic flow modeling framework},
journal = {Communications in Transportation Research},
volume = {5},
pages = {100163},
year = {2025},
issn = {2772-4247},
doi = {https://doi.org/10.1016/j.commtr.2025.100163},
url = {https://www.sciencedirect.com/science/article/pii/S2772424725000034},
author = {Xiaohui Zhang and Jie Sun and Jian Sun},
keywords = {Stochastic fundamental diagram, Brownian dynamic, Markov chain, Maximum entropy}
}
