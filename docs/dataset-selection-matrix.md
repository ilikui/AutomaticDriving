# 自动驾驶数据集选型与评测矩阵

本页用于快速缩小数据集选择范围。数据集的任务、版本、许可和评测服务器可能变化，使用前请访问官方入口确认最新条款。“适合”表示常见研究用途，不代表数据集只支持这些任务。

## 1. 按研究问题选择

| 研究问题 | 可优先了解的数据集 | 常见任务 | 选择时要关注 |
|---|---|---|---|
| 相机 2D 检测与场景理解 | BDD100K、Cityscapes、nuImages | 检测、分割、场景属性 | 类别定义、天气/昼夜覆盖、标注密度 |
| 多模态感知 | nuScenes、Waymo Open Dataset、Argoverse 2 Sensor | 3D 检测、跟踪、融合 | 传感器布局、标定、采样频率、数据切分 |
| LiDAR 3D 检测 | KITTI、Waymo、ONCE、PandaSet | 3D 检测、点云处理 | 点云格式、类别映射、距离分布 |
| LiDAR 语义分割 | SemanticKITTI、nuScenes lidarseg | 点级语义分割 | 类别不均衡、序列划分、动态物体 |
| 运动预测 | Waymo Motion、Argoverse 2 Motion、nuScenes Prediction | 多模态轨迹预测 | 预测时域、采样频率、坐标约定 |
| 车路协同 | DAIR-V2X、V2X-Seq | 协同感知、时空对齐 | 车端/路侧标定、通信延迟、协议 |
| 长期定位与建图 | Oxford RobotCar、KITTI Odometry、MulRan | 定位、SLAM、跨季节鲁棒性 | 场景变化、传感器配置、轨迹真值 |
| 驾驶策略研究 | Waymo、nuScenes 等公开研究数据 | 表征学习、预测与规划相关研究 | 许可、闭环能力限制、离线与闭环差异 |

## 2. 官方入口

- [KITTI](https://www.cvlibs.net/datasets/kitti/)
- [SemanticKITTI](https://semantic-kitti.org/)
- [Cityscapes](https://www.cityscapes-dataset.com/)
- [nuScenes](https://www.nuscenes.org/)
- [Waymo Open Dataset](https://waymo.com/open/)
- [Argoverse 2](https://www.argoverse.org/av2.html)
- [BDD100K](https://www.vis.xyz/bdd100k/)
- [ONCE](https://once-for-auto-driving.github.io/)
- [PandaSet](https://scale.com/open-datasets/pandaset)
- [Zenseact Open Dataset](https://zod.zenseact.com/)
- [DAIR-V2X](https://thudair.baai.ac.cn/)
- [Oxford RobotCar](https://robotcar-dataset.robots.ox.ac.uk/)
- [MulRan](https://sites.google.com/view/mulran-pr/)
- [A2D2](https://www.a2d2.audi/a2d2/en.html)

## 3. 评测指标速查

| 任务 | 常见指标 | 不应忽略 |
|---|---|---|
| 2D 检测 | AP、mAP、Precision、Recall | IoU 阈值、类别平均方式、置信度阈值 |
| 3D 检测 | 3D AP、NDS（特定基准）、定位/尺寸/朝向误差 | 距离分桶、类别定义、匹配规则 |
| 多目标跟踪 | HOTA、MOTA、IDF1、ID switches | 轨迹初始化/终止规则、遮挡处理 |
| 语义分割 | mIoU、per-class IoU、准确率 | 类别不均衡、忽略标签、点数统计 |
| 运动预测 | minADE、minFDE、Miss Rate、概率校准指标 | 预测时域、候选轨迹数、概率定义 |
| 定位 / 里程计 | 平移与旋转误差、ATE、RPE | 对齐方法、尺度是否可观、轨迹片段 |
| 控制与规划 | 横纵向误差、碰撞率、规则违反、舒适性 | 约束、失败率、闭环场景覆盖 |
| 系统工程 | 延迟分位数、吞吐、资源占用、可用率 | P50/P95/P99、冷启动、传感器掉线 |

不同基准的指标名称相似，不代表计算协议一致。引用结果时同时写明数据版本、官方评测脚本版本、数据切分、模型检查点和关键配置。

## 4. 数据集评估流程

\`\`\`mermaid
flowchart TD
    A["明确研究问题"] --> B["筛选传感器与标注"]
    B --> C["核对许可和访问条件"]
    C --> D["检查官方拆分与评测协议"]
    D --> E["建立简单基线"]
    E --> F["运行官方评测脚本"]
    F --> G["分场景与长尾误差分析"]
    G --> H["保存配置、版本与结果"]
\`\`\`

## 5. 数据使用清单

- 阅读许可和使用条款，确认研究、商业使用及再分发边界。
- 保留原始官方数据切分，不把测试集用于调参。
- 检查相邻帧泄漏、场景重复和身份信息。
- 明确坐标系、单位、时间戳、类别映射和缺失值规则。
- 除总体平均值外，分析远距离、小目标、恶劣天气、遮挡和罕见场景。
- 保存数据版本或校验信息；不要未经许可把大型数据文件提交到仓库。
