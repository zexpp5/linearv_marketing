# AI Agent绩效

`AI Agent绩效` 是 LinearVision 当前第一批具体产品之一。

它面向的不是“怎么把第一个 Agent 搭出来”，而是“当企业已经有多个 Agent 之后，怎么知道这些 Agent 是否真的在创造价值”。

## 一个前提判断

这个产品评估的不是“Agent 多聪明”，而是“它是否稳定地创造业务结果”。

因此，讨论 `AI Agent绩效` 时，必须先把 Agent 当成一个有职责、有边界、有交接关系的虚拟岗位，而不是一个抽象模型能力。

## 方向判断

围绕这个产品，有两种容易混淆的方向：

- `Agent KPI OS`
- `Human + Agent KPI OS`

当前更合理的方向，不是把 human 和 agent 当成并列的一等执行对象，而是：

`Human-controlled Agent KPI OS`

也就是：

- 人负责设目标、设阈值、审批、干预和复盘
- Agent 负责执行任务、做决策、调用工具
- 系统负责把 Agent 行为映射到结果、成本和 ROI

这比“人和 Agent 并列考核”的抽象更稳，也更容易落地。

## 产品定位

这是一个面向企业 AI Agent 的绩效、可观测性和经营管理产品。

它帮助客户回答四个问题：

- 哪些 Agent 真正在稳定产出
- 哪些 Agent 成本高但效果差
- 哪些 Agent 需要更多人工接管
- 哪些 Agent 应该继续扩、整改，还是下线

## 为什么现在需要这个产品

很多企业已经到了这样的阶段：

- Agent 已经不是 1 个，而是 5 个、10 个、20 个
- 大家都在说“已经落地了”，但没有统一绩效标准
- 没有人能说清楚每个 Agent 的成功率、错误率、接管率和 ROI
- 管理层开始问“这些 Agent 到底值不值”

`AI Agent绩效` 就是用来把这种“模糊落地”变成“可管理、可比较、可决策”的。

## 核心价值

- 让企业从“部署了多少 Agent”转向“哪些 Agent 真有绩效”
- 给技术负责人一套可运营的 Agent 管理视图
- 给业务负责人一套能看懂的投入产出视图
- 给管理层一个关于扩张、收缩和整改的依据

## 核心能力方向

- Agent 台账：统一梳理每个 Agent 的负责人、职责、数据输入、输出动作和服务对象
- 指标体系：效率、质量、财务、风险/安全四类 KPI
- 异常识别：发现高失败率、高冲突率、高人工回退率的 Agent
- 对比分析：不同 Agent、不同团队、不同流程之间的横向比较
- ROI 视图：把 Agent 绩效转成业务负责人能理解的时间、成本和结果

## 核心对象与系统分层

| 层级 | 主体 | 主要职责 | 核心关注 |
| --- | --- | --- | --- |
| Owner 层 | 人 | 设目标、定阈值、审批 | ROI / 风险 / 产出 |
| Operator 层 | 人 | 调 prompt、调流程、设规则 | success / fail / escalation |
| Executor 层 | Agent | 执行 task / decision / tool use | task success / latency / quality |
| Outcome 层 | 业务结果 | 收入、成本、时效、质量 | value realization |

这意味着：

- 人不是主要被考核的 worker
- 人是控制环里的操作者和结果享受者
- Agent 才是执行绩效的主要计算对象

## KPI 设计原则

- 先定义业务目标，再定义 Agent 能否完成它
- 先定义权限和责任边界，再定义 KPI
- 不只看自动化率，要同时看质量和风险
- 必须先有人工基准线，再看引入 Agent 后的增量价值
- 高风险流程里，人工审核本身也应该是 KPI 体系的一部分
- 不把产品退化成日志 dashboard，而要把 `action -> outcome -> value` 这条映射链做出来

## 两个方向对比

| 维度 | Agent KPI OS | Human-controlled Agent KPI OS |
| --- | --- | --- |
| 核心对象 | agent / trace | human control + agent execution + outcome |
| 人的角色 | 边缘 | 目标设定、审批、干预、受益 |
| 产品归类 | eval / observability 工具 | agent analytics + control plane |
| 风险 | 容易退化成 logging tool | 更完整，但仍可控 |
| 更适合当前阶段 | 是 | 更准确的升级定义 |

结论：

- `Agent KPI OS` 方向本身没错
- 但如果不把 human 放在控制环里，就会太静态
- 如果直接做 `Human + Agent KPI OS`，又会过重，容易滑向 HR / workflow / org system

## 最小必要系统闭环

| 环节 | 主体 | 输入 | 输出 |
| --- | --- | --- | --- |
| Goal Setting | human | 业务目标 | KPI target |
| Policy Config | human | 风险 / 预算 / 规则 | control policy |
| Execution | agent | task / context / tools | actions / results |
| Monitoring | system | trace / outcome | KPI / dashboard |
| Intervention | human | alerts / exceptions | override / fix |
| Optimization | system + human | historical KPI | prompt / flow / policy update |

## 产品路径判断

| 阶段 | 产品形态 | 核心能力 | 目标 |
| --- | --- | --- | --- |
| Phase 1 | Agent KPI OS | trace -> success / eval | 替代纯 observability 工具 |
| Phase 2 | + workflow layer | task / flow abstraction | 跨 agent 评估 |
| Phase 3 | human control loop | goal / policy / intervention | 人在控制环内 |
| Phase 4 | optimization system | assignment / ROI optimization | 系统级优化 |

这个路径比一开始就做完整的 “Human + Agent KPI OS” 更现实。

## 四类 KPI 结构

### 1. 效率类

- 任务完成时间
- 自动化率
- 单位人力产出
- 平均响应时间

### 2. 质量类

- 一次解决率
- 准确率
- 可用回复率
- 人工返工率

### 3. 财务类

- 节省成本
- 带来收入
- ROI
- GMV 或转化提升

### 4. 风险与安全类

- 违规率
- 幻觉率
- 越权调用次数
- 人工介入次数

## 典型适用场景

- 企业已经部署多个 Agent，但没有统一指标
- 不同团队各自做 Agent，结果无法横向比较
- 管理层开始要求汇报 AI 产出，而团队只能讲 demo
- 客户已经开始怀疑部分 Agent 是否应该继续投入

## 对应的客户阶段

这个产品最适合：

- 混乱期客户
- 危机期客户
- 重构期客户

它本质上是一个“让 Agent 体系重新可管理”的切口。

## 与 `See / Think / Act` 的关系

- `See`：采集 Agent 运行信号、任务结果、人工介入情况和异常记录
- `Think`：评估每个 Agent 的绩效、可靠性和价值
- `Act`：触发预警、整改建议、下线建议或优化计划

## 对外怎么讲

### 简短版

`AI Agent绩效` 帮你看清楚每一个 Agent 是否真的在创造价值。

### 更业务版

不是所有上线的 Agent 都值得继续投。`AI Agent绩效` 帮你把 Agent 从“能跑”变成“能管理、能比较、能算账”。

### 更偏管理层版

如果你已经有一批 Agent 在跑，下一步不是继续堆数量，而是先看清楚哪些值得扩、哪些该整改、哪些该停。

## 当前产品边界

这个产品当前不等于一个完整的“AI Agent 平台”。

它更适合作为：

- Agent 体系治理的第一入口
- 事故后重建的第一步
- `AI Sprint` 之后的持续管理层

## 当前最重要的 MVP

首版不需要做得很大，优先聚焦：

- Agent 台账
- 核心指标面板
- 人工接管和异常事件记录
- ROI 基础测算

## MVP 之外，不要过早做的东西

- 完整的 human-worker 统一建模
- 复杂组织绩效系统
- 自动任务调度优化
- 过重的 org OS 叙事

这些方向不是永远不做，而是不适合作为第一阶段产品定义。

## 核心抽象

| 抽象 | 定义 |
| --- | --- |
| Task | 可评估的最小工作单元 |
| Action | agent 或 human 的行为 |
| Decision | 可归因的关键判断节点 |
| Outcome | 业务结果 |
| Cost | 资源消耗 |
| Value | 业务收益 |
| KPI | `f(action -> outcome)` |

## 对 LinearVision 的意义

- 这是一个很容易和客户当前痛点对上的具体产品
- 它把“架构”和“治理”转成了更可销售的业务语言
- 它天然适合作为后续更大部署和更深产品化的入口
- 它真正的壁垒不在 dashboard，而在于把 Agent 行为稳定映射到业务结果

## 配套方法文档

如果要进一步定义某个 Agent 的岗位说明、职责边界和 KPI 模板，见 [Agent_岗位与KPI设计.md](/Users/lance7in/workspace/repos/my/linearv_marketing/公司定位/03_定位与品牌/Agent_岗位与KPI设计.md)。
