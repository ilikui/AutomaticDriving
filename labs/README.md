# 自动驾驶可运行实验

实验的目标是把知识转成可重复验证的结果。每个实验至少记录：问题、假设、数据、基线、指标、结果、环境版本和已知局限。

## 实验路线

| 编号 | 实验 | 依赖 | 目标 |
|---|---|---|---|
| LAB-001 | 一维匀速模型 + Kalman Filter | Python 3.10+ 标准库 | 理解预测、观测更新与估计误差 |
| LAB-002 | 2D 坐标系变换与外参检查 | Python 3.10+ 标准库 | 验证变换方向、单位、矩阵组合和逆变换 |
| LAB-003 | 一维多传感器融合 | Python 3.10+ 标准库 | 用逆方差加权融合合成观测，比较 RMSE |
| LAB-004 | Pure Pursuit 几何路径跟踪 | Python 3.10+ 标准库 | 理解前视目标、曲率与转向角关系 |
| LAB-005 | 鲁棒一维传感器融合 | Python 3.10+ 标准库 | 使用中位数 / MAD 门限识别粗大异常值，再按方差加权 |
| LAB-006 | CARLA 场景复现与回归测试 | CARLA / Scenario Runner | 固定版本、种子、场景与指标，保留失败案例 |
| LAB-005 | CARLA 场景复现与指标记录 | CARLA | 固定场景、随机种子与版本，建立回归测试 |

## LAB-001：一维匀速 Kalman Filter

代码：[`python/kalman_1d.py`](python/kalman_1d.py)，测试：[`python/test_kalman_1d.py`](python/test_kalman_1d.py)。

只需安装 Python 3.10 或更高版本，不依赖 NumPy。运行：

```bash
python labs/python/kalman_1d.py
python -m unittest discover -s labs/python -p 'test_*.py' -v
```

实验会生成确定性的合成观测，输出每一步的真实位置、观测值、估计值与误差。它是用于理解状态估计的教学模型，不是可直接用于车辆定位的生产实现。

## LAB-002：二维坐标系变换

代码：[`python/coordinate_transform_2d.py`](python/coordinate_transform_2d.py)，测试：[`python/test_coordinate_transform_2d.py`](python/test_coordinate_transform_2d.py)。

采用约定：`T_parent_child` 将 child 坐标系中的点变换到 parent 坐标系。示例覆盖平移、旋转、矩阵组合和逆变换。自动驾驶工程中必须明确坐标系命名、变换方向、角度单位和长度单位；不能只凭矩阵数值猜测方向。

运行：

```bash
python labs/python/coordinate_transform_2d.py
python -m unittest discover -s labs/python -p 'test_*.py' -v
```

## LAB-003：一维多传感器融合

代码：[`python/sensor_fusion_1d.py`](python/sensor_fusion_1d.py)，测试：[`python/test_sensor_fusion_1d.py`](python/test_sensor_fusion_1d.py)。

以合成的相机距离测量和雷达距离测量为例，按测量方差的倒数加权，输出单传感器与融合估计的 RMSE。这个实验假设测量无偏、相互独立，并且观测的是同一个已对齐标量；它**没有**实现目标关联、坐标转换、时间同步或异常值抑制，不能直接代表真实的相机—雷达融合系统。

运行：

```bash
python labs/python/sensor_fusion_1d.py
python -m unittest discover -s labs/python -p 'test_*.py' -v
```

## LAB-004：Pure Pursuit 几何路径跟踪

代码：[`python/pure_pursuit.py`](python/pure_pursuit.py)，测试：[`python/test_pure_pursuit.py`](python/test_pure_pursuit.py)。

实现前视目标点选择、车辆坐标系变换、几何曲率和前轮转角计算，并提供简单运动学自行车模型演示。当前示例用于理解几何关系，不包含速度自适应前视距离、执行器延迟、转向限幅、道路边界约束或真实车辆动力学。

运行：

```bash
python labs/python/pure_pursuit.py
python -m unittest discover -s labs/python -p 'test_*.py' -v
```

## LAB-005：鲁棒一维传感器融合

代码：[`python/sensor_fusion_robust.py`](python/sensor_fusion_robust.py)，测试：[`python/test_sensor_fusion_robust.py`](python/test_sensor_fusion_robust.py)。

在 LAB-003 的逆方差加权基线前加入中位数与 MAD（median absolute deviation）异常值门限，并报告接受的观测索引、融合估计和方差。适用于理解“先做质量门控，再做估计”的思路；样本很少时鲁棒统计能力有限，阈值需要依据传感器噪声和场景校准。此例不处理目标关联、时间同步、坐标对齐或相关噪声。

```bash
python labs/python/sensor_fusion_robust.py
python -m unittest discover -s labs/python -p 'test_*.py' -v
```

自动化测试：仓库的 [Python Labs GitHub Actions](../.github/workflows/python-labs.yml) 会在相关代码推送和 Pull Request 时，使用 Python 3.11 与 3.12 执行单元测试并运行实验脚本。

## LAB-006：CARLA 场景复现与回归测试

配置记录模板：[`carla/scenario-template.yaml`](carla/scenario-template.yaml)；完整方法：[`docs/carla-reproducibility.md`](../docs/carla-reproducibility.md)。

这一项先建立可复现的实验规范，不假装在当前环境中已经运行 CARLA。记录 CARLA / Scenario Runner 版本、地图、天气、同步模式、固定步长、随机种子、交通参与者、传感器参数、终止条件与指标定义。每次优先只改变一个变量；碰撞、超时和越线等失败案例也要保留。运行前请按实际版本把模板字段映射到 CARLA 原生配置。

## 实验记录模板

- **问题与假设：**
- **环境 / 版本 / 提交：**
- **输入数据及来源：**
- **基线与对照组：**
- **评价指标：**
- **结果（含失败案例）：**
- **可复现命令：**
- **局限与下一步：**

## 安全边界

所有实验均用于离线学习、仿真和数据分析。未经独立安全论证、硬件保护和专业验证，不要将示例算法直接用于真实车辆控制或道路测试。
