# 论文与研究方向导航

本页优先提供稳定的检索入口和经典方向，避免把不断变化的论文排行榜当作固定教材。阅读时应回到论文原文、作者代码和正式发表页面，确认年份、版本、数据集与评测协议。

## 1. 先读综述，建立问题地图

- [Self-Driving Cars: A Survey](https://arxiv.org/search/?query=Self-Driving+Cars%3A+A+Survey&searchtype=all)：自动驾驶总体技术栈的综述检索入口。
- [Planning and Decision-Making for Autonomous Vehicles](https://arxiv.org/search/?query=Planning+and+Decision-Making+for+Autonomous+Vehicles&searchtype=all)：规划与决策研究入口。
- [A Survey of Motion Planning and Control Techniques for Self-Driving Urban Vehicles](https://arxiv.org/search/?query=A+Survey+of+Motion+Planning+and+Control+Techniques+for+Self-Driving+Urban+Vehicles&searchtype=all)：运动规划和控制综述入口。
- [End-to-End Autonomous Driving: Challenges and Frontiers](https://arxiv.org/search/?query=End-to-End+Autonomous+Driving+Challenges+and+Frontiers&searchtype=all)：端到端驾驶问题与挑战的检索入口。
- [Foundation Models in Autonomous Driving](https://arxiv.org/search/?query=Foundation+Models+in+Autonomous+Driving&searchtype=all)：基础模型、视觉语言模型和驾驶决策的研究入口。

以上部分链接是按标题构造的 arXiv 检索入口，而不是特定论文版本的永久链接；请核对作者、年份、发表状态及论文全文后再引用。

## 2. 按主题阅读

### 感知与 3D 目标检测
- 图像 2D/3D 检测、点云检测、语义分割和多目标跟踪。
- 关注遮挡、远距离小目标、长尾类别、恶劣天气和域迁移。
- 配套代码：[OpenPCDet](https://github.com/open-mmlab/OpenPCDet)、[MMDetection3D](https://github.com/open-mmlab/mmdetection3d)。

### BEV 与多传感器融合
- 从早期/中期/后期融合的区别开始，再研究 BEV 表征、跨模态对齐与融合。
- 重点记录每个传感器贡献了什么信息、对齐误差如何传播，以及传感器缺失时的退化行为。
- 数据入口：[nuScenes](https://www.nuscenes.org/)、[Waymo Open Dataset](https://waymo.com/open/)。

### 定位、SLAM 与地图
- 学习视觉/激光 SLAM、GNSS/INS 融合、回环检测、地图匹配和定位置信度。
- 关注动态物体、退化场景、地图变化、时间同步与坐标系误差。

### 预测、规划与控制
- 轨迹预测、行为预测、搜索规划、优化规划、MPC 和轨迹跟踪。
- 不只比较平均误差，也要研究可行性、碰撞风险、舒适性和规划可解释性。
- 可结合 [CommonRoad](https://commonroad.in.tum.de/) 进行规划相关研究。

### 端到端驾驶、VLM/VLA 与世界模型
- 区分纯视觉端到端、模块化系统与混合式系统。
- 检查数据规模、闭环评测、泛化能力、失效模式和算力成本。
- 对语言解释或开放式评测结果保持谨慎，要求可量化的闭环证据。

### 安全、鲁棒性与评测
- 场景覆盖、故障注入、分布外数据、传感器失效、可解释性和安全约束。
- 结合仿真回归测试与真实数据评估，不以单一排行榜名次替代风险分析。

## 3. 论文阅读卡片模板

每篇论文建议记录：
- **书目信息**：标题、作者、年份、会议/期刊、DOI/arXiv。
- **研究问题**：论文具体解决什么，为什么重要？
- **关键假设**：依赖哪些传感器、数据、场景和计算资源？
- **核心方法**：输入、输出、模型/优化目标和关键设计。
- **实验设计**：数据集、划分、基线、指标、消融实验。
- **主要结果**：哪些结论由实验支持？提升是否公平可比？
- **局限与失败模式**：作者承认什么问题？还存在哪些风险？
- **代码复现**：仓库、commit/tag、环境、命令、结果差异。
- **关联卡片**：前置概念、对比方法、后续工作和可验证问题。

## 4. 研究资料的可信度检查

- 预印本不等于同行评审通过的正式论文。
- 不同数据集、数据划分或评测协议下的指标不可直接横向比较。
- 复现代码可能滞后于论文或只实现部分方法。
- 对 SOTA 宣称，检查对比基线是否公平、计算资源是否一致、是否报告方差和失败案例。
- 对自动驾驶安全相关结论，要求超越离线精度的闭环和场景证据。
