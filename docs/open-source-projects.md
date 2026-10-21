# 开源工程实践指南

## 开源工程的阅读顺序

```mermaid
flowchart LR
    A[确认版本与环境] --> B[运行官方最小示例]
    B --> C[绘制模块 / Topic / API 数据流]
    C --> D[选定单一模块调试]
    D --> E[建立基线与评价指标]
    E --> F[仿真或数据集验证]
    F --> G[记录问题、证据与回归测试]
```

建议从小而明确的目标切入，而不是一开始就试图部署整个自动驾驶栈。下面的工程图展示的是阅读与验证方法，不代表任何单一项目的固定内部架构。

目标是从「能启动」进阶到「能解释数据流、定位问题、验证结果」。大型工程的依赖和硬件要求可能随版本变化，请先阅读项目当前的安装说明，不要直接复制旧博客中的命令。

## 项目选择

| 项目 | 主要用途 | 建议切入点 | 注意事项 |
|---|---|---|---|
| [CARLA](https://github.com/carla-simulator/carla) | 驾驶仿真与场景评估 | 官方 Quickstart、Python API、传感器、Traffic Manager | UE4/UE5 版本与系统要求有差异 |
| [Autoware](https://github.com/autowarefoundation/autoware) | ROS 2 自动驾驶系统 | 官方安装、架构、仿真启动、车辆接口 | ROS 发行版、地图、车辆和传感器配置需匹配 |
| [Apollo](https://github.com/ApolloAuto/apollo) | 自动驾驶软件栈 | 开发环境、模块架构、Cyber RT/消息流、仿真工具 | 先核对官方支持平台和版本 |
| [OpenPCDet](https://github.com/open-mmlab/OpenPCDet) | 点云 3D 检测 | 数据准备、配置文件、基线推理与评测 | CUDA、PyTorch、编译扩展和数据格式需匹配 |
| [MMDetection3D](https://github.com/open-mmlab/mmdetection3d) | 3D 感知算法 | 模型配置、数据转换、测试脚本 | 依赖栈会随版本升级变化 |
| [Scenario Runner](https://github.com/carla-simulator/scenario_runner) | 可重复驾驶场景测试 | 示例场景、触发条件、评测记录 | 与 CARLA 版本匹配 |

## 实践项目 A：在 CARLA 中建立可复现实验

1. 选择官方文档明确支持的 CARLA 版本，记录 OS、GPU、驱动和版本号。
2. 启动示例地图与车辆，先使用 spectator 和键盘控制确认仿真正常。
3. 通过 Python API 添加 RGB 相机或 LiDAR，保存时间戳和传感器数据。
4. 设置固定路线、交通参与者和场景参数；记录随机种子（若所用接口支持）。
5. 运行一个简单规则策略，记录完成率、碰撞、越线、行驶时间和舒适性指标。
6. 保存场景配置、运行命令、日志与失败案例，确保能够重复运行。

官方入口：[CARLA GitHub](https://github.com/carla-simulator/carla) · [CARLA 文档](https://carla.readthedocs.io/)。

## 实践项目 B：理解 ROS 2 数据流

1. 完成 ROS 2 官方 Beginner Tutorials。
2. 用 rosbag 录制与回放数据，检查时间戳和 QoS。
3. 使用 TF2 展示 base_link、camera、lidar 等坐标系之间的关系。
4. 绘制节点图，标注 Topic、消息类型、频率、坐标系和数据来源。
5. 注入延迟、缺失数据或错误外参，观察下游模块的表现。

官方入口：[ROS 2 Tutorials](https://docs.ros.org/en/rolling/Tutorials.html)。

## 实践项目 C：复现一个 3D 检测基线

1. 从 [KITTI](https://www.cvlibs.net/datasets/kitti/) 或 [nuScenes](https://www.nuscenes.org/) 选择一个任务。
2. 选择 OpenPCDet 或 MMDetection3D 的一个明确版本和官方基线配置。
3. 严格按照对应版本文档准备数据，避免混用不同版本的配置。
4. 先运行官方预训练模型和评测脚本，再尝试训练或调整一个参数。
5. 报告指标、推理速度、硬件、数据划分和已知限制。
6. 通过可视化和错误分类分析漏检、误检、遮挡和距离相关问题。

## 实践项目 D：阅读 Autoware 模块链路

建议从模拟环境开始，而非直接连接真实车辆：
1. 跑通官方支持的安装与模拟器教程。
2. 找出定位、感知、规划、控制和 vehicle interface 的入口。
3. 记录每个模块的输入输出消息、坐标系、更新频率和关键参数。
4. 追踪一条从目标点到规划轨迹再到控制命令的数据链路。
5. 检查车辆接口的安全门控、状态反馈、超时处理和紧急停止行为。
6. 在仿真中验证修改，并保留回归测试结果。

官方入口：[Autoware 文档](https://docs.autoware.org/)。

## 实验交付清单

- [ ] 版本与环境记录
- [ ] 官方来源和许可证链接
- [ ] 数据集版本与获取方式
- [ ] 配置文件、命令和参数
- [ ] 基线结果与评价指标
- [ ] 可视化结果和失败样本
- [ ] 可重复执行的步骤
- [ ] 风险、局限和下一步计划

**安全提醒：** 开源算法、仿真测试和离线数据指标不构成真实道路部署的安全证明。实车实验需要经过授权的场地、专业安全流程、独立急停与相应的法规和功能安全评估。
