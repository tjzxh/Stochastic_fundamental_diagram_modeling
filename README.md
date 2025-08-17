# 🚦 On the Stochastic Fundamental Diagram  
**Official Code Repository for the Article:**  
[On the Stochastic Fundamental Diagram: A General Micro-Macroscopic Traffic Flow Modeling Framework](https://doi.org/10.1016/j.commtr.2025.100163)  

![SFD Illustration](https://github.com/user-attachments/assets/6244bcb9-83f5-424b-8183-b468a0c37753)

---

## 📖 Overview  
Traffic congestion and its inherent **stochasticity** remain key challenges in urban mobility.  
This repository provides the implementation of the **Leader-Follower Conditional Distribution-based Stochastic Traffic Modeling (LFCD-STM)** framework — a novel approach bridging **microscopic driver interactions** and **macroscopic traffic flow patterns**.  

🔑 **Key Contributions:**  
- 📊 Introduces a **probabilistic representation of leader-follower behavior**.  
- 🔗 Employs the **Markov chain principle** to derive joint platoon distributions.  
- 📈 Provides **analytical functions** for both **mean** and **variance** of the stochastic fundamental diagram (SFD).  
- ✅ Validated with **NGSIM I-80**, **US-101**, and **HighD** datasets.  

---

## 🌉 Bridging Micro ↔ Macro  
The LFCD-STM framework offers:  
- 🔹 **Real-time traffic flow estimation**  
- 🔹 **Enhanced simulation of macroscopic dynamics**  
- 🔹 **Robust traffic control strategies** accounting for uncertainty  
- 🔹 **Foundations for CAV (Connected & Automated Vehicles) optimization**  

This research advances the vision of **sustainable, adaptive, and efficient traffic management systems**.  

---

## 🌏 Bilingual Abstract  

### English  
The framework connects **microscopic stochasticity** to **macroscopic uncertainty**, enabling more reliable modeling of the stochastic fundamental diagram. Results show high consistency with real-world traffic patterns, paving the way for smarter congestion mitigation and CAV deployment.  

### 中文  
**微观与宏观的完美衔接：新方法助力随机交通流基本图的建模**  

该研究提出 **基于前后车条件分布的随机交通流建模 (LFCD-STM)** 框架，以布朗运动为基础描述前后车的条件概率分布，并通过马尔可夫链推导车队速度联合分布，从而得到流量-密度基本图的均值与方差。在多个数据集上的验证表明方法能准确复现交通流的随机性特征。  

该框架不仅适用于**基本图预测与仿真**，还可用于设计**鲁棒性更强的交通控制策略**，并为**网联自动驾驶车辆**的混合交通分析与控制提供理论支持。  

---

## 📂 Repository Structure  
```bash
├── data/              # Processed and sample trajectory datasets
├── src/               # Core implementation of LFCD-STM
│   ├── preprocessing/ # Data processing scripts
│   ├── modeling/      # Leader-Follower & Markov chain models
│   └── visualization/ # Plotting and analysis tools
├── results/           # Reproduced figures and validation outputs
└── README.md          # Project documentation
