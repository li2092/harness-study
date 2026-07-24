# 第二卷《Harness 运行时架构》· 写作思路与详细大纲

状态：大纲 v5.5 · 2026-07-21（编号手术：新增"§四 参考架构蓝图"为第二部分开篇——v5.4 把蓝图件下沉后全卷缺一章完整蓝图，用户裁决方案 A；原 §四–§十四 顺移为 §五–§十五，全卷 15 章；章 spec 见 volume2/SPEC.md §十一。**历史读法规则**：本次手术前的文件——旧稿留档、评审报告、research 快照、旧审稿日志——中的 §四–§十四 一律按映射读作 §五–§十五。上版 v5.4 · 2026-07-20：§一瘦身手术——§一砍到一条主线，五平面/实体链/恢复时序/部署/双层控制流/干预点/两种 graph 下沉到首用章；"六条不变量"并入六契约承诺句、术语退役；新增章级判据。v5.3 · 2026-07-19：补入可执行 Belief/World Model、Model Certificate、Plan Lease、反例驱动重规划与评测披露接口）

**v5.5+ 权责说明（2026-07-24）**：本大纲是**高层结构 SSOT**——卷定位、六类契约（0.3）、完备性网格（0.5）、每章模板（1.2）、来源纪律（1.3）、各章章题与章职责以本文件为准。但 2026-07-19 起流程改为 spec 先行：**每章的实际推理链与章内小节结构，以 `volume2/SPEC.md` 章 spec（§四–§十九 ＝ §一–§十二 章 spec）与成稿正文为准**。本大纲第二节各章的小节清单（5.x／6.x／…／12.x）是**原始规划**，成稿时多有增删收拢（例：§十一 规划的 11.1-11.13 成稿收拢为 11.1-11.7、隔离四类由规划的 11.7 落到成稿 11.4），与成稿不一致时以 SPEC.md／正文为准。全量小节清单的回填留到**全卷定稿一次性联动**。进度状态（各章过审/待审）见 `volume2/README.md`，不进本大纲。

上游：`introduction/`（入门卷：部件学与基本 mental model）。

下游：`volume3-outline.md`（第三卷：生产工程、安全、测试、发布、SRE 与治理）。

原料：`harness-engineering-guide.md` + `research/volume2/` + Howpot 韧性摸底案例。

---

## 〇、卷定位

### 0.1 本卷只解决一个问题

> 怎样构造一个语义正确、可中断、可恢复、可验证的 Agent Harness runtime？

入门卷讲 harness 有哪些部件；第二卷讲这些部件怎样组成一个正确的运行时。这里的“正确”不是输出看起来合理，而是：

- 状态归属明确；
- 状态转移合法；
- 外部副作用可对账；
- 中断与恢复有精确定义；
- 权限在运行时边界内生效；
- 完成声明能连接到真实 outcome。

数据库运维、网络容量、安全治理、测试体系、版本发布、SLO、值班和成本治理属于第三卷。本卷只讲它们对 runtime contract 的接口要求，不展开生产制度。

### 0.2 与第三卷的边界

| 问题 | 第二卷 · 运行时架构 | 第三卷 · 生产工程 |
|---|---|---|
| 数据库 | 状态模型、事务边界、checkpoint 语义 | migration、备份恢复、容量、加密、保留 |
| 网络 | stream/cancel/retry 的运行语义 | 超时基线、熔断、限流、provider failover、容量 |
| 安全 | principal、delegation、permission、sandbox 边界 | threat model、secret、供应链、多租户、合规 |
| 可观测性 | event/trajectory/evidence 数据模型 | telemetry 管道、告警、SLO、值班、事故响应 |
| 测试 | 用故障实验证明 runtime contract | 测试金字塔、eval gate、发布门禁、chaos/soak |
| 版本 | run/checkpoint 必须携带版本 | 配置治理、迁移、灰度、回滚、兼容策略 |
| 成本 | runtime 暴露可计量资源与硬终止接口 | 预算、容量、成本模型、配额和经济性 |

判断规则：本卷回答“系统在一次运行中究竟发生什么”；第三卷回答“团队怎样长期可靠地运行和改变它”。

### 0.3 六类运行时契约

不再用十二/十三个并列机制域作为最高层分类。运行时由六类契约组织，每类契约自带一句承诺（原"六条运行时不变量"，v5.4 起并入此表，见 0.4）：

| 契约 | 承诺（一句话） | 核心问题 | 典型对象 |
|---|---|---|---|
| 真相契约 | 状态可归属：每个持久状态都有 owner、ID、版本和合法读写路径 | 哪份状态算数，谁拥有它？ | run、message、checkpoint、memory、artifact |
| 转移契约 | 转移可解释：每次状态变化都有触发事件、前置条件和终结原因 | 什么事件能让状态从 A 变成 B？ | lifecycle、concurrency、retry、resume |
| 副作用契约 | 副作用可对账：每次外部动作都有意图、执行尝试、结果和真实 outcome | 声称做了什么，外部世界实际发生了什么？ | tool intent、attempt、result、outcome |
| 交互契约 | 失败可收敛：失败、中断和恢复最终进入已定义状态；不能恢复时明确终结 | 用户、连接与后台 run 如何保持一致？ | stream、cancel、interrupt、HITL、UI projection |
| 权限契约 | 权力有边界且有期限：权限不能只靠 prompt 维持；恢复状态不等于恢复旧授权 | 谁以谁的身份、在什么边界内行动？ | principal、delegation、approval、sandbox |
| 证据契约 | 结论有证据：完成、失败和安全声明都能指向运行证据 | 凭什么相信状态、动作和完成声明？ | event、trajectory、policy trace、lineage、verifier |

承诺"失败可收敛"由两个主场共同兑现：run 终态收敛在转移契约（§五），断连/取消/挂起收敛在交互契约（§九）。传播性短句保留：**每个状态有归宿，每个故障有路径，每个中断可恢复或诚实终结。**

资源和演进不是遗漏：第二卷定义运行时需要暴露的 meter、limit、version 和 compatibility metadata；第三卷负责把它们变成生产治理。

契约与章节的映射：真相→§六、§十；转移→§五、§七；副作用→§八；交互→§九；权限→§十一、§十二；证据→§十三；§一～§三立框架，§四 蓝图枢纽，§十四、§十五综合验收。

### 0.4 命名裁决：不变量并入契约（v5.4）

原六条"运行时不变量"与六契约近乎一一对应（状态可归属↔真相、转移可解释↔转移、副作用可对账↔副作用、权力有边界且有期限↔权限、结论有证据↔证据、失败可收敛↔交互+转移），是同一组承诺的两套名字。一物二名使核心概念在 §一（推导为不变量）、§一后段（换名为契约）、§二（重列为判据要素）三次出场，读者每次都要重新绑定——本卷自己讲"同物多名会修错层"，却在核心概念上犯了同款错误。

v5.4 起：承诺句并入 0.3 表格，"不变量"作为术语退役；正文泛指这组性质时说"六契约的承诺"；历史文件中的"六(条)不变量"一律读作"六契约承诺句"。

### 0.5 周全性检查：对象 × 事件 × 边界

章节数量不代表考虑周全。运行时问题统一用三个正交维度检查：

| 维度 | 枚举 |
|---|---|
| 对象 | 状态、副作用、权限、证据 |
| 事件 | 创建、读取、修改、并发、失败、中断、恢复、删除 |
| 边界 | 进程、worker、agent/subagent、网络、数据库、provider、工具、用户 |

例如：

- 副作用 × 恢复 × 网络边界：请求超时但远端已经成功，恢复后是否重复执行？
- 权限 × 并发 × subagent 边界：并行子任务是否扩大父任务权限？
- 状态 × 中断 × 进程边界：kill -9 后 `running` 由谁收敛？
- 证据 × 删除 × 用户边界：会话删除后 artifact 和审计证据分别怎样处理？

该框架只用于检查遗漏，不在正文穷举笛卡尔积。

### 0.6 读者完成判据

读完应能回答：

1. `conversation/session/run/turn/step/invocation/tool execution/artifact` 如何关联？
2. 哪份状态是 SSOT，context 为什么不是？
3. 任意一行被 kill 后，重启怎样收敛？
4. checkpoint、journal、replay、resume、fork 有什么差异？
5. 工具超时后如何判断重试、查询、补偿还是人工调和？
6. disconnect、cancel、interrupt、suspend 有什么差异？
7. agent、subagent、tool 分别以谁的身份行动？
8. 完成声明怎样连接 tool outcome 与 artifact evidence？
9. 怎样构造一个最小但完整的 runtime？
10. 怎样用故障实验证明这些语义真的成立？

---

## 一、写作与教学设计

### 1.1 一条事故主线，一个贯穿实现

Howpot Bug 2 作为事故主线：导航跳走 → 未完成轮次未落盘 → 用户误判重问 → 新 run 抢占 → 假丢失变成真丢失。

同时构造一个最小参考 runtime：

- API/UI 入口；
- run manager；
- model adapter；
- tool executor；
- SQLite 状态层；
- event stream；
- sandbox/permission；
- evidence store。

先实现单机最低充分解；每章末尾再说明切换到 worker queue、Postgres 或 durable execution 引擎的条件。

### 1.2 每章固定模板

（v5.4 注：2026-07-19 起本模板降为交稿前完备性检查单，章结构以 `volume2/SPEC.md` 的推理链＋因果叙事硬规则为准；2026-07-20 起每章 spec 另附章级判据——新概念数与前向引用数上限、读者带走"一图一句一动作"。）

1. 用户症状或事故；
2. 落到哪类运行时契约；
3. 传统计算机科学根基；
4. Agent 增加的变量；
5. 价值/目标 → 原则 → design choice → evidence → tradeoff；说明为什么选这个设计点、牺牲什么、什么证据会推翻它；
6. 轻量/标准/重型三档设计；
7. 进入贯穿实现；
8. 主动破坏一次；
9. 输出可复用 artifact。

### 1.3 来源纪律

- 【评审】：同行评审或有统计设计的研究；
- 【预印】：明确未经同行评审和外推边界；
- 【规范/官方文档】：描述协议或产品契约；
- 【厂商实践】：工程案例，不自动外推为行业共识；
- 【经验/推导】：项目实证或综合推导。

“唯一”“空白”“业界收敛”必须附检索范围与截止日期。产品 reference、官方工程博客和厂商比较不能混为一个“官方”等级。

反向工程、npm 包提取和源码考古只能证明“所分析版本出现过这种实现”，不能替代当前产品契约；正文必须标注版本快照，并用官方文档回核当前可承诺行为。

---

## 二、章节大纲

### 第一部分 · 从架构到事故（§一～§三）

> **v5.4 手术（2026-07-20，用户裁决"大纲设计有问题"）**：v5.1 架构前移的方向不变，但 §一 在 v5.1→v5.3 三轮增补后积累了 14 个小节主题、四套分类体系（不变量/组件/平面/契约），三版正文接连被否（散→苍白→不对劲）。诊断（依据 51 处前向引用、约 40 个新概念的实测）：章职责过载 + 同物多名，病在大纲不在行文。处置：§一 砍到一条主线（读者带走一图一句一动作），被移出内容下沉到首次真正需要它的章（对应表见 §一节内）；六不变量并入六契约承诺句（0.3/0.4）；§二 不再重列六件事；§三 事故验证案例定位不变。
>
> （v5.1 重排记录：§一=参考架构与统一语言，§二=判据，§三=事故压缩为验证案例，卷首六拍开场在 §一。）

先自上而下立参考架构与六类契约（一条主线，不做全量前置），再给“正确”下判据，最后用一次真实事故检验框架的解释力。

#### §三（原 §一） 一次“数据丢失”事故：判据的反向验证 · 压缩为验证案例（章名副题 2026-07-21 随正文 v2.0 过审回写）

全卷从 Howpot Bug 2 开场：用户看到“消息丢了”，而 UI、连接、run、数据库每一层单独检查都“正常”。本章把事故逐帧拆成状态、事件与副作用的时间线，展示局部正确不等于系统正确；六类契约不是抽象分类，而是给这次事故中缺失的东西命名。

- 1.1 Howpot Bug 2 完整时间线。
- 1.2 用户看到的“丢消息”对应哪些内部状态。
- 1.3 UI、连接、run、message、数据库各自都“正常”为什么仍然出错。
- 1.4 将事故画成 state-event-effect 图。
- 1.5 区分症状修复、局部修复和系统契约修复。
- 1.6 对账六类契约（§一已立，本章不重新定义）：事故中每样缺失的东西都能在契约表上找到名字。

- 1.7 从一次事故到一类现象（23.8pp 与 MAST 数字首现 §一，本章对账引用、不重列）：同一批模型换 harness，成功率差 23.8pp（Harness-Bench，6 harness × 8 模型后端 × 106 任务）【预印】；1600+ 条多 agent 故障轨迹标注中，规范缺陷 41.77%、协调失败 36.94%、验证缺失 21.30%——三类全在系统层；不换模型，只加语义验证 +15.6pp、只改角色规范 +9.4pp（MAST，NeurIPS 2025，检索范围内唯一评审级）【评审】。
- 1.8 改进不可叠加（主场在本章）：三个组件单独共 +11.1pp，组合只 +7.3pp；预测"改动修好什么"精度 33.7%，预测"弄坏什么"仅 11.8%【预印】——局部正确不可外推，这是需要契约体系而非逐点修补的定量理由。
- 1.9 越强的模型对 harness 差异越不敏感，弱模型受伤害更大（Harness-Bench）——runtime 质量对中小模型与私有化部署价值更高（此推论首现 §一 开场，本章不重复展开）。

破坏实验：在模型调用前、流式中、落库前、工具执行后分别强杀。

交付物：事故时间线、缺失证据清单、第一版契约缺口图。

素材：guide §六；Howpot 摸底报告【经验】（正文一律脱敏：化名表见 `volume2/SPEC.md` §六；大纲与调研文件为内部资料可用真名）；research/volume2/02（1.7-1.9 定量证据均已对原文核过）。

#### §二 什么叫“正确的 runtime”

本章给“正确”下严格定义。核心动作是把散落在代码与直觉里的隐式假设（“不会重复调用”“可以继续上次会话”）改写成有 owner、触发条件、结果与证据的显式契约，并区分保证/best effort/推断/未知四档确定性。读完本章，读者应能用契约语言而非感觉讨论一个 harness 是否可靠。（v5.4：本章不重新定义六契约——承诺句在 0.3、推导在 §一；本章只做三件事：隐式假设改写成契约行、承诺分四档确定性、给验收方法。）

- 2.1 输出正确、状态正确、系统正确的差别。
- 2.2 “写了错误处理”不等于故障有归宿。
- 2.3 “有 checkpoint”不等于 durable execution。
- 2.4 隐式假设怎样改写成 contract：owner、trigger、guard、action、outcome、evidence。
- 2.5 保证、best effort、推断、未知四档确定性。
- 2.6 六契约承诺逐条配真实反例（只演示违约形态，不重列定义）。
- 2.7 runtime contract 与生产 policy 的边界。
- 2.8 为什么两个主体都会把"看起来对"当"真的对"：四层结构——症状层归因、自洽幻觉、局部对整体错、知行鸿沟。agent 侧对应物：execution alignment failure（自洽推理与工具反馈、工作区状态脱钩，Harness-Bench 故障分类占 36.4%）【预印】与 False Success 一簇【预印】；工程师侧对应物："写了错误处理"（2.2）、"有 checkpoint"（2.3）、"已经考虑过"。契约体系是对两个主体同一种认知缺陷的同一种解法：把检验从注意力、记忆和意志力下沉为结构。2.5 的四档确定性即第二层"确定性均匀化"的工程解。
- 2.9 文献坐标：六元组 ℋ=⟨ℐ_obs,𝒞,ℒ,ℐ_act,𝒮,𝒱⟩（arXiv:2606.20683）按组件切分，本卷六契约按保证切分，一个契约横跨多个组件——真相≈𝒮+𝒞（context 是投影）、转移≈ℒ、副作用≈ℐ_act、交互≈ℐ_obs、权限与证据≈𝒱 的治理/验证两半；T1-T4 四要件（arXiv:2606.10106）中 T4"控制机制独立于模型是否配合"即本章硬软之辨的文献表述。给映射是为了可对话，不是服从文献切法。

练习：把“不会重复调用”“可以继续上次会话”“用户会确认”改写为可验证契约。

交付物：Runtime Contract Register（六契约承诺的可检验改写）、Assumption Register。

素材：research/volume2/02（execution alignment、T1-T4、六元组核对）；四层框架为作者观点内化，不引外部文章。

#### §一 参考架构与检验坐标系 · 一条主线（v5.4 瘦身；章名 2026-07-21 随正文 v4.0 过审回写，原"参考架构与统一语言"，统一语言职责由章末附录 A/B 承担不变）

本章只做一件事：从"部件齐了系统还不对"推到"一张组件图 + 六类契约"。一条推理链走到底，不做全量前置——每个结构出场前必有迫使它存在的问题（写法纪律见 `volume2/SPEC.md` 硬规则 1-4）。

主线（唯一推理链）：卷首开场（入门卷回顾、读者怪事，用户口述六拍）→ 立论证据（23.8pp：问题在部件之外；方差收窄推论）→ 与在线服务的三个本质差异（进程可弃/重试无害/行为可复现三个默认值逐个失效）→ 三类威胁（状态撕裂/账对不上/无从归因，MAST 佐证）→ 六类契约（承诺句直接命名，0.3 的正文化；不经"不变量"中转）→ 职责分配长出八组件（每个组件由"朴素做法→失效方式→设计"推出；四个承重取舍——单写者、只追加、单执行内核、投影不回写——融进各自推导现场）→ 一条正常时序（九步、落盘点加粗；"任何机制要能在时序上标出位置"的全卷判断标准）→ 六契约总览表与分章地图收尾，遗留问题交 §二。

- 1.1 三个本质变量：执行跨越故障边界、副作用泄向外部世界、核心组件输出不确定。
- 1.2 三类威胁与六类契约：逐类反推承诺；第六类（权限）来自变量组合。
- 1.3 职责分配与组件图：八组件为推导终点，不是开场白；多入口单执行内核在 run manager 的失效推导内立概念（细则与 Routing Matrix 归 §五）。
- 1.4 一条正常时序：九步走查。
- 1.5 六契约总览表（0.3 表 + 主场章映射）。
- 附录（不计正文负担）：入门卷术语对照（原 3.10 全文保留）、业界命名对照（终稿前逐格回核）。

章级判据（v5.4 新增，写作红线）：新概念 ≤12、前向引用 ≤10、正文表格 ≤2；读者带走三样——组件图一张、传播性短句一句、五分钟动作一个（用六契约表自查自己的系统）。

破坏实验：真相源分叉（UI 本地状态与数据库 run 状态分叉，验证投影不回写）。

交付物：组件图、正常时序、六契约总览表、术语速查（附录对照表）。

**下沉对应表（v5.4，原 §一内容的新归属）**：

| 原 §一 内容 | 新归属 | 理由 |
|---|---|---|
| 3.1-3.6 五平面与依赖禁令 | §十一 11.0（评审落位表另供 §十五） | "谁被允许持有什么"在权限章才成为读者的真问题 |
| 3.7 实体链 + 3.8 ID/owner/correlation/version | §六 6.0 | "哪份状态算数"是状态章的开场问题；State Registry 随迁 |
| kill -9 恢复时序（原第二条时序） | §七 7.10 主场景（§五 orphan 侧先用） | 没讲状态机与重放前，七步恢复只能被动接受 |
| 3.9 部署两种放法与切换信号 | §十四 部署基线 | 造的时候才需要决定放哪 |
| 3.11 多入口单内核细则 + Routing Matrix + 入口语义分叉实验 | §五 5.11 | 入口互斥/幂等本来就是 §五 的 5.4/5.5 |
| 3.12 双层控制流 | §十二 12.0 | 跨节点调度在多 agent 章才有所指 |
| 3.13 三干预点 + Intervention Point Map | §十一 11.0（assemble 细节 §十） | 干预点即 Control 边界，权限章主场 |
| 3.14 两种 graph 之辨 | §八 8.12 引言 | world-state graph 是 planner 的搜索对象 |

素材：research/volume2/01（入门卷覆盖地图与可沿用术语清单）；立论数字核对 research/volume2/02。《Dive into Claude Code》（arXiv:2604.14228）随 3.11-3.13 下沉转入 §五/§十一 素材；research/volume2/10 随 3.14 转入 §八。

### 第二部分 · 蓝图、状态与执行语义（§四～§八）

全卷核心。开篇 §四 先摊开整张蓝图，随后依次回答四个问题：run 的状态从哪来到哪去（§五）、哪份状态算数（§六）、进程死了怎么活回来（§七）、对外部世界做过的事怎么对账（§八）。

#### §四 参考架构蓝图（v5.5 新增，2026-07-21 用户裁决方案 A）

§一 回答了"八组件为什么存在"（失效推导），本章回答"八组件各自长什么样、边界在哪、彼此怎么接"——后续每个深潜章放大蓝图的哪一格，先在这里看全图。"设计空间占比"尺的首个执行章：主角是结构与取舍，案例只当证据。完整章 spec 见 `volume2/SPEC.md` §十一。

- 4.1 蓝图怎么读：组件卡六栏（职责一句／边界=明确不做什么／上下游接口／主守契约与守约方式／替代方案与取舍／L 级起步预期）；数据流与模块边界图。
- 4.2 真相三件：状态层、事件流、证据存储——三张组件卡与各自取舍（SQLite 单写者 vs Postgres+lease；append-only 表 vs 消息队列；证据与事件分储的理由）。
- 4.3 执行两件：run manager（单执行内核）、agent loop（内存即易失）——取舍：内核集中 vs 入口自治；同步循环 vs graph 引擎（两种 graph 之辨在 §八 8.12）。
- 4.4 外界三件：入口层（投影不回写）、model adapter（留档复用不重调）、tool executor（先记账再动手）——各配一条取舍。
- 4.5 两条动线：正常九步回指 §一 1.4，本章新增"每步落盘点归哪张卡"；恢复七步概览（主场 §七 7.10）。
- 4.6 业界逐组件映射：Temporal／LangGraph／Claude Code——升格自 §一 1.4 轮廓对照与附录 B，逐组件对位并标空位。
- 4.7 部署形态一页：单机基线→多实例迁移线概览（切换信号详表在 §十四 部署基线；生产细节卷三）。
- 4.8 下沉件索引：实体链（§六 6.0）、Routing Matrix（§五 5.11）、五平面（§十一 11.0）、双层控制流（§十二 12.0）、两种 graph（§八 8.12）。

破坏实验：逐组件抽除思想实验——抽掉组件 X，哪份契约失去履行人、四问哪问答不出（§一"八是最低充分解"的逐一验证）。

交付物：Component Register（组件卡×8，§十五 评审对照物）、逐组件业界映射表、部署概览图。

素材：§一 1.4 与附录 A/B 升格；research/volume2/03-06（业界对照，终稿回核）。

#### §五 Run 生命周期状态机

run 是 harness 中最重要的状态机。本章给出完整生命周期：哪些事件触发转移、并发入口如何互斥、创建请求如何去重、被 kill 的 orphan run 由谁收敛。主张是：任何 run 在任何时刻都必须处于可解释的状态——“卡在 running”不是状态，是缺陷。

- 5.1 queued/running/waiting/interrupted/completed/failed/cancelled 定义。
- 5.2 event、guard、transition、terminal reason。
- 5.3 业务失败、基础设施失败、用户取消、策略拒绝分开建模。
- 5.4 多入口互斥：reject/enqueue/interrupt/rollback；入口除用户外还有 scheduler/timer 与 webhook。
- 5.5 入口幂等：客户端重试同一创建请求不得产生重复 run；idempotency key 的作用域、保留期与冲突应答。
- 5.6 抢占必须先收尾；旧 run 的半轮内容归宿。
- 5.7 optimistic concurrency、lock/lease、fencing token 的适用条件。
- 5.8 orphan run：启动扫描、超时扫描、双进程同时 resume。
- 5.9 进程壳层：supervision、子进程组、重启强度、二次启动。
- 5.10 状态机本身必须携带版本。
- 5.11（自 §一 3.11 下沉）多入口、单执行内核细则：UI/API/IM/scheduler 只适配 intent 与 stream，统一汇入同一 Run Manager/Execution Kernel；入口不得各自实现 permission、cancel、resume 或 tool execution 捷径；Entry-to-Kernel Routing Matrix 在本章交付。

破坏实验：两个入口同时触发同一会话；两个进程同时 resume；同一创建请求重发两次；入口语义分叉（SDK 与 UI 各写一套 permission/cancel 捷径，入口一致性 contract test 报出分叉——自 §一下沉）。

交付物：可执行状态转移表、并发策略、orphan 收敛测试、Entry-to-Kernel Routing Matrix。

素材：guide 4.1/4.7/4.9；research/volume2/04（Assistants run 状态机与退役时间线）；《Dive into Claude Code》（arXiv:2604.14228 v2，快照 Claude Code v2.1.88，第三方源码分析——4.11 实现证据，当前行为以官方文档为准）。

#### §六 状态、事件与持久化

本章确立真相归属：数据库中的持久状态是 SSOT，context 只是一次模型调用的投影，UI 是另一种投影。围绕这一主张展开状态分层、checkpoint 边界、tool_call 配对与 artifact lineage，并指出根本限制——数据库说成功不等于外部世界成功，为 §七§八 铺底。

- 6.0（自 §一 3.7/3.8 下沉）统一语言：六级实体链（Conversation→Run→Turn→Step→Invocation/Tool Execution）与关键裁决（run 可无 conversation、subagent=child run、turn 无独立表）；十一张表；ID/owner/correlation/version 四条全局规则；"重启之后用户的消息还在吗"争论场景开场；State Registry v1 在此交付、章末升 v2。
- 6.1 SSOT、事务、WAL、snapshot、event log、projection。
- 6.2 业务状态、运行状态、对话状态、工作记忆、artifact 分离。
- 6.3 context 是一次模型调用的有损读投影，UI 是另一种投影；两者都不是持久真相。
- 6.4 append-mostly transcript/rollout、trajectory、trace 的差异；完整历史负责审计与恢复，模型不必每次看见完整历史。
- 6.5 checkpoint 保存什么、明确不保存什么。
- 6.6 compaction boundary、summary provenance 与 read-time projection：压缩改变下一次 invocation 看见的视图，不反向覆盖完整 rollout/transcript。
- 6.7 tool_call/tool_result 配对和半压缩状态。
- 6.8 artifact lineage：创建、修改、输入和 verifier。
- 6.9 数据库不能代表外部副作用是否真正成功。
- 6.10 删除会话、删除运行记录、撤销外部动作不是一回事。
- 6.11 状态生命周期、execution 生命周期、authority 生命周期分别建模；checkpoint/resume 是否携带权限、approval、delegation 或 credential 必须逐项声明，安全默认值是不隐式恢复。
- 6.12 Belief/World Model 是版本化的 derived mutable artifact，不是 SSOT：event history 记录已发生事实，world model 记录当前可错信念，notes 记录工作假设，plan 记录从特定模型派生的临时动作。模型版本必须携带 history cursor、生成 provenance、certificate scope 和已知反例，不能覆盖原始 observation。

破坏实验：在消息、摘要、artifact 三处写入之间 kill -9；故意遗漏决定未来的状态变量，验证新反例能触发状态表示与转移规则共同修订，而不是只在 notes 中打补丁。

交付物：State Registry v2、持久化边界表、数据所有权表、Projection Contract、Lifetime Matrix、Belief/World Model Registry。

素材：guide §三/4.2；research/volume2/03（Agent SDK sessions；file checkpointing——对话与文件两套 checkpoint、Bash 副作用不被捕获，5.9/5.10 的产品实证）；research/volume2/10（Schema 的 event history/world model/notes/plan 分层与适用边界）。

#### §七 Durable Execution 与重放

崩溃恢复是 runtime 的试金石。本章比较 checkpoint 与 journal 两条 durable execution 路线，共同前提是：LLM 调用不能重新执行并期待相同输出，首次结果必须记录并在恢复时复用。给出单机最低充分解与升级到专用引擎的判断条件；durable timer 在此定义——定时唤醒也是持久状态。

- 7.1 重新执行与重放记录结果的区别。
- 7.2 LLM 调用不能重新执行并期待相同输出。
- 7.3 checkpoint 路线：节点边界、durability 档位、pending writes。
- 7.4 journal 路线：deterministic workflow、event history、Activity。
- 7.5 workflow decision 可重放，外部 Activity 仍可能执行多次。
- 7.6 heartbeat、timeout、retry policy、failure detection。
- 7.7 durable timer：sleep、deadline、定时唤醒、cron 触发是持久状态而非进程内定时器；进程死后由谁恢复。
- 7.8 resume、replay、fork、time travel 四种操作分别说明状态、执行、副作用和授权后果；state continuity 不自动推出 authority continuity，授权重校验移交 §十一。
- 7.9 两个 worker 同时恢复同一 execution 的协调问题。
- 7.10 单机最低充分解：事件表 + intent/result + 启动扫描 + timer 扫描；kill -9 七步恢复时序（原 §一第二条时序，自 v5.4 下沉）在此作为主场景完整走查。
- 7.11 何时需要 LangGraph/Temporal/Restate/DBOS，何时不需要。
- 7.12 边界声明：durable execution 产品生态已成熟，但 agent 专属的运行时持久化（LLM 结果复用、副作用对账、压缩边界即 checkpoint 边界的组合问题）截至 2026-07 几乎无同行评审研究（检索范围：arXiv 及 OSDI/SOSP/NSDI/EuroSys 2026，见 research/volume2/02）——本章以产品契约与传统理论降维为据。

对照：LangGraph checkpointer（durability 三档 sync/async/exit）、Temporal/Restate journal（含 durable timer）、Agent SDK session（resume/fork；session 按 cwd 编码存储，换目录 resume 得到空会话是现成反例）、OpenAI Responses/Conversations（Response 默认 30 天 TTL，挂入 Conversation 则无 TTL——“哪份状态算数”的实例）、OpenAI background mode（background=true 的轮询式长任务）。

破坏实验：Activity 已产生副作用但完成结果尚未记录时杀进程。

交付物：恢复语义表、durability 选型记录、replay fixture。

素材：research/volume2/05（LangGraph durability 三档、Diagrid 批评、Restate journal）、07 §1（Temporal×OpenAI：Runner 抽象基类→每次 agent 调用隐式 Activity 化）。

#### §八 工具执行与副作用

工具调用是模型触碰真实世界的唯一通道，也是最难对账的环节。本章用 intent→attempt→result→outcome 四段模型拆开“调了一个工具”这句话，讨论幂等、去重、补偿与“超时但远端已成功”的调和策略。落点是 Effect Ledger：每个副作用都有账可查。

- 8.1 工具是模型与真实世界之间的 Effect System。
- 8.2 intent → policy → approval → attempt → result → outcome。
- 8.3 schema、语义、编排三层校验。
- 8.4 at-most-once、at-least-once、幂等、去重、补偿。
- 8.5 幂等 key 的来源、作用域、保留期和冲突。
- 8.6 `intent without result`：重试、查询、补偿、未知四类处置。
- 8.7 长运行工具：heartbeat、progress、partial output、cancel；对照 MCP Tasks（2026-07-28 规范）：`tools/call` 返回 durable handle，`tasks/get`/`tasks/cancel` 驱动，working/input_required/completed/failed/cancelled 五态。
- 8.8 子进程生命周期与父进程绑定。
- 8.9 文件、HTTP、数据库、消息、支付的不同调和方式。
- 8.10 tool result 成功不等于真实 outcome 成功。
- 8.11 Poka-yoke：用接口形态消除危险组合。
- 8.12 开篇先立两种 graph 之辨（自 §一 3.14 下沉）：workflow graph 节点是任务/agent，管理 branch/join/retry；world-state graph 节点是对世界状态的表示，边是动作及预测转移，供 planner 搜索；二者可嵌套，不用"graph 取代 loop"概括。随后进入 Guarded Commit 与 Plan Lease：计划只对 `model_version + history_cursor + policy_version` 有效；所有真实动作经 Effect Gateway 提交，每步比较 predicted transition 与 observation。prediction、policy 或 authority 任一不一致都废止剩余计划，产生 Counterexample Event 后重新建模/规划；resume 不得恢复已失效的动作队列。

破坏实验：超时但远端实际成功；返回成功但 artifact 不存在；规划后改变世界状态或 policy，验证下一次 commit 拒绝 stale lease；制造一步 prediction mismatch，验证未执行队列被丢弃而非继续照单执行。

交付物：Effect Ledger、Tool Contract、Reconciliation Table、Plan Lease、Counterexample Event Contract。

素材：guide 3.3/4.6；research/volume2/03（writing effective tools、poka-yoke）；research/volume2/10（Schema 的内部搜索/外部 commit 分离、逐步预测对账与 plan invalidation）；MCP Tasks 引用按事实纪律第 8 条标 RC、定稿后回核。

### 第三部分 · 交互、连续性与边界（§九～§十二）

前两部分解决“系统内部对不对”，这一部分把用户、外部内容与其他 agent 拉进来：连接会断、人会打断、内容不可信、子任务会失控。

#### §九 Streaming、中断与人机挂起

用户看到的是流式 token，系统里跑的是后台 run，两者之间隔着一条随时会断的网络连接。本章严格区分 disconnect/cancel/interrupt/suspend 四个常被混用的词，给出断线续传的应用层方案与 HITL 挂起的持久化语义。主张：UI 永远是状态投影，本地状态与数据库分叉时以后者为准。

- 9.1 后台 run、网络连接、客户端视图三条时间线。
- 9.2 SSE/EventSource 提供什么，POST/fetch stream 还缺什么。
- 9.3 协议层 session 不可依赖（MCP 2026-07-28 移除 `Mcp-Session-Id` 即例证）；续传责任在应用层：cursor/sequence、snapshot + delta、replay window。
- 9.4 乱序、重复、slow consumer、backpressure、终结事件。
- 9.5 disconnect ≠ cancel；cancel ≠ interrupt；interrupt ≠ suspend。
- 9.6 取消令牌贯穿 UI → server → model → tool → child process。
- 9.7 Stop 后半轮文本、tool result 和 artifact 的归宿。
- 9.8 HITL：持久化、版本、超时、过期审批、stale resume。
- 9.9 UI 是状态投影：重拉、ErrorBoundary、熔断、导航逃逸。
- 9.10 provider partial stream/429/5xx 的 runtime 反馈接口。
- 9.11 边界声明：学术中断研究（InterruptBench/IHBench/SentinelBench）截至 2026-07 只覆盖用户主动改需求，不覆盖崩溃、抢占、被杀后的状态接续（见 research/volume2/02）——本章四词语义以工程实践与产品契约为据。

破坏实验：断网、刷新、重复连接、审批跨 session 恢复、工具忽略 cancel。

交付物：交互语义表、stream protocol、cancel propagation test。

素材：guide 4.3-4.5；research/volume2/02（中断研究窄化）、05（LangGraph interrupt=checkpoint）。

#### §十 Context、Memory 与 Artifact 的连续性

长任务终将撞上 context 上限。本章把 compaction、记忆写入与 resume 当作会相互干扰的事务处理：压缩可能中断、摘要可能遗漏系统约束、恢复可能读到旧 policy。context assembly 被定义为有来源、优先级与预算的确定性过程，而不是把历史一股脑塞进 prompt。

- 10.1 context assembly：来源、优先级、预算、去重、可信度。
- 10.2 compaction、note-taking、JIT retrieval、subagent 四种手段。
- 10.3 compaction × cache × resume 三方耦合。
- 10.4 压缩事务：失败回退、边界落盘、指令重载、配对修复。
- 10.5 memory 写入的污染、过期、撤销与 provenance。
- 10.6 artifact 是工作成果，不应隐藏在 conversation 文本中。
- 10.7 模型接近 context 上限时的行为变化。
- 10.8 model/prompt/tool/context policy 共同决定 invocation。
- 10.9 resume 必须尊重原 invocation 与 compaction 版本。
- 10.10 隐私与删除要求作为第三卷数据治理的接口。

破坏实验：压缩中断、摘要遗漏系统约束、memory 污染、resume 读旧 policy。

交付物：Context Assembly Spec、Compaction Contract、Memory Provenance。

素材：research/volume2/03（context engineering 四策略；context editing/memory tool 定量 +29%/+39%/token -84%；code execution with MCP 150K→2K）、07 §4（9.7 的一手源：Cognition——模型对窗口余量自估精确但错、一贯低估）。

#### §十一 权限、身份与运行时隔离

prompt 里写“你不许做 X”不是安全边界。本章建立运行时权限模型：谁是 principal、权力从谁委托而来、何时过期、permission 与 sandbox 哪些是硬边界哪些是软提示。以 Codex 的 execpolicy 与分层沙箱为实例，说明“默认收窄、显式升级、升级留痕”的工程形态。

- 11.0（自 §一 3.1-3.6/3.13 下沉）五平面与三干预点：按持有权把八组件分入 Interaction/Control/Execution/State/Evidence 五平面，各平面配"绝不持有"清单；平面间四条依赖禁令（Interaction 不写 State、Execution 不直连 Interaction、Control 决策必落 Evidence、State 不依赖任何平面）；三类干预点 assemble/model/execute 的平面归属与"三处分别留证"（assemble 细节在 §十）；Intervention Point Map 在本章交付，五平面落位表另供 §十五 评审。
- 11.1 principal：user、agent、subagent、tool/service、operator。
- 11.2 agent 是用户代理还是独立身份。
- 11.3 delegation chain：授予者、scope、期限、再委托、撤销。
- 11.4 least privilege 与 least agency。
- 11.5 approval 是风险决策，不是通用安全边界。
- 11.6 permission、hook、classifier、sandbox 的硬软层级；实例：Codex execpolicy 三档 allow/prompt/forbidden，规则自带 match/not_match 加载期自测；shell-escalation 的 Run/Escalate/Deny 三态协议（素材见 `research/volume2/07`）。
- 11.7 filesystem、process、network/egress、secret 四类隔离接口；实例：bubblewrap 默认整盘只读 + 按路径特异性分层覆盖，`.git`/`.codex` 在可写根下重新只读绑定。
- 11.8 subagent 权限默认收窄，不继承 bypass。
- 11.9 tool output、文件、网页、memory 的信任标签。
- 11.10 runtime 必须产出 policy decision 和权限证据。
- 11.11 defense-in-depth 只有在执行点和失效模式足够独立时才成立；permission、hook、classifier、sandbox 的控制记录至少包含 enforcement point、failure mode、shared dependency、fail-open/closed、fallback 和 evidence，不能用“有四层”代替 common-mode failure 分析。
- 11.12 resume/fork/replay 不得静默恢复旧 approval、session-scoped permission、delegation token 或 credential；确需持久化的 authority 必须显式列入契约，并在上下文、主体或版本变化后重新验证。
- 11.13 供应链、多租户、合规治理移交第三卷。

破坏实验：subagent 越权、恶意 tool result、过期 delegation、secret 进入 sandbox；高风险授权后 resume/fork，验证旧授权不会随状态静默复活；关闭多个控制层共享的 classifier/parser，验证剩余硬边界仍 fail-closed。

交付物：Runtime Trust Boundary、Principal Table、Delegation Record、Authority Lifecycle Matrix、Common-mode Failure Matrix、Intervention Point Map、五平面落位表。

#### §十二 多 Agent 协调

多 agent 不是免费的并行加速。本章先给出“是否需要多 agent”的判断，再处理父子 run 的所有权、预算与权限收窄、共享 artifact 的并发写冲突和 partial failure 的收敛。核心告诫：subagent 的输出不因为来自“内部”就更可信。

- 12.0（自 §一 3.12 下沉）双层控制流：节点内 observation→decision→action loop 与跨节点 workflow graph 调度层（依赖、并行、分支、join、重试、中间变量）；dynamic workflow 生成物先过校验、预算、权限门禁再执行；与 §十四步骤 2 对应。
- 12.1 先判断是否需要多 agent；并行不是默认收益。
- 12.2 parent/child run、task ownership、join、cancel propagation。
- 12.3 orchestrator-worker、handoff、shared workspace。
- 12.4 子任务必须携带目标、边界、预算、权限、返回 schema。
- 12.5 shared artifact 并发写、冲突和 merge。
- 12.6 partial failure、straggler、超时和 graceful degradation。
- 12.7 同步 lead 瓶颈与异步协调成本。
- 12.8 subagent 输出不是天然更可信的内部信息。
- 12.9 预算树只定义运行时 meter/limit，治理策略移交第三卷。
- 12.10 evidence aggregation 保留来源、失败和不确定性。

破坏实验：subagent 卡死、越权、返回恶意指令、覆盖共享 artifact。

交付物：Coordination Protocol、Parent-child State Table、Failure Test。

素材：research/volume2/03（multi-agent research system：15x token、token 量解释 80% 方差、lead 同步执行瓶颈——11.7 的一手数据）。

### 第四部分 · 证据、构造与评审（§十三～§十五）

收束为可交付的工程能力：证据体系（§十三）、从零构造（§十四）、评审方法（§十五）。

#### §十三 Evidence Plane

前面各章不断要求“留下证据”，本章统一定义证据体系：原始 event 与派生解释分离、correlation ID 贯穿全链、policy 决策可追溯、完成声明必须连到 outcome 证据。特别处理两类沉默失败：该发生的事件没发生，以及检测器本身失效——检测器必须证明自己会触发。

- 13.1 诊断、审计、验证、用户反馈四类证据用途。
- 13.2 原始 event、派生 trace、trajectory、transcript、metric。
- 13.3 correlation IDs：tenant/session/run/turn/step/invocation/effect/artifact。
- 13.4 Observe First, Interpret Later：热路径写事实，离线 reducer 解释（出处：Codex rollout-trace README，见 `research/volume2/07`）。
- 13.5 policy trace：谁在何时因何规则允许/拒绝。
- 13.6 artifact lineage 与 verifier evidence。
- 13.7 content 默认按敏感数据处理（对照 rollout-trace “tracing is not telemetry” 的边界声明），采集策略移交第三卷。
- 13.8 absence-of-event、沉默失败、声明态/运行态对账。
- 13.9 sabotage validation：检测器必须证明能触发。
- 13.10 completion claim 必须连接 outcome evidence。
- 13.11 为可执行信念增加认识论边：`observation --grounds--> model_version`、`model_version --predicts--> transition`、`history_set --certifies--> model_version`、`counterexample --refutes--> model_version`、`plan --derived_from--> model_version`、`commit --realizes--> plan`、`mismatch --invalidates--> remaining_plan`；这些边扩展现有 Evidence Graph，不另建平行图谱。
- 13.12 Model Certificate 必须限定 scope：完整历史 backtest 只证明 retrodictive consistency，不证明未见状态上的 generalization；certificate 记录 model version、history cursor、测试集合/覆盖、失败反例和签发时版本，不能只写 `backtest=green`。

破坏实验：吞掉一个错误、关闭一个检测器、制造“成功但无 artifact”；注入历史外的新转移和一个会被 planner 利用的模型漏洞，验证 certificate 不会被误当成全局正确性，counterexample 会吊销模型与剩余计划。

交付物：Event Schema、Evidence Graph（继承入门卷 §八十边定义，见 §一附录对照表）、Detector Test Record、Model Certificate、Counterexample Event Schema。

素材：research/volume2/02（沉默失败一簇：60 天静默/67 空检查/70% 靠人工发现）、07 §2（rollout-trace 与 "tracing is not telemetry"）、10（Schema trajectories、证据边与 backtest 保证边界）。

#### §十四 从零构造一个最小但完整的 Runtime

全卷的动手验收。按依赖顺序把前面定义的契约逐一实现成最小参考 runtime，每一步配正常与失败两条 trajectory；完成后用标准故障包证明六契约承诺在实现中真实成立，而不是停留在文档里。

先立部署基线（自 §一 3.9 下沉）：单机与服务两种放法，逻辑架构不变，各组件切换信号——SQLite→Postgres（多写者/备份不够用）、单例→分布式锁或 lease（多实例）、进程内任务（工具子进程沙箱）→worker queue、进程内广播→事件总线。

按依赖顺序实现：

1. 实体、ID 与 State Registry；
2. 单一 Execution Kernel 与 run 状态机：先实现 node-local loop，再增加一个含 branch/join 的最小 graph workflow；
3. model invocation record；
4. tool intent/result/outcome；
5. event stream 与客户端重建；
6. cancel 与 HITL；
7. checkpoint/resume 与 durable timer；
8. permission/sandbox 与 authority lifecycle；
9. context assembly/compaction；
10. 在一个状态紧凑、转移可观察的案例中实现 `world model → history replay certificate → search/dry-run → guarded commit → counterexample/replan`；该路径是显式可建模任务的扩展，不要求所有 agent 任务都构造完整 simulator；
11. parent/child run；
12. Evidence Plane；
13. runtime meter/limit/version 接口；
14. 标准故障包验证。

每一步展示：最小数据结构、关键伪代码、正常 trajectory、失败 trajectory、验证证据。

交付物：语言无关 executable spec（底线交付，成书不被实现进度阻塞）；可运行参考实现（加分交付）。两者共用同一套标准故障包验收；第三卷接口清单以 executable spec 为准。

#### §十五 Runtime 架构评审

把全卷方法压缩成读者能带走的东西：五件评审工具加一个 90 分钟流程，用于审查任何现有系统。评审的产出不是“通过/不通过”，而是一张有 owner 的残余风险清单。

五件核心工具：

1. **Component Register**（§四 交付，v5.5 补列）：八组件卡逐张对位被评系统自画的组件图，对不上即标红——评审的开场标尺。
2. **State Registry**：状态、owner、存储、版本、读写者。
3. **Effect Ledger**：意图、权限、执行、幂等、outcome、调和。
4. **Boundary Map**：进程、网络、身份、工具、信任边界。
5. **Runtime Contract Matrix**：六类契约 × 正确性/可靠性/安全/用户反馈/可测试性。

原 13×13 机制矩阵保留为“热点交叉发现表”，不要求填满。三元交叉、用户行为和时间漂移用场景卡另列。

90 分钟评审流程：

1. 画边界；
2. 登记状态；
3. 登记副作用；
4. 检查六契约承诺；
5. 选择高风险场景；
6. 指定破坏实验；
7. 明确残余风险及第三卷 owner。

收束：模型可以不确定，runtime 不能不知道自己发生了什么。

评审判定线补两条（2026-07-21 记，§一 v4.0 增补段的回响）：一条问"这是 framework 思维还是 harness 思维"；另一条问**"这个团队敢不敢动自己的 core"**——§一 1.3 立的反格言（能跑不再是不动的理由；敢动的前提是检验体系）在评审场景的操作化：看该团队最近一次对 core 的测试/调优/局部重构发生在什么时候、有没有配套测量数据。停在"第一天智能水平"且只在外围打补丁的系统，评审时按高残余风险记。

---

## 三、附录

附录承载正文不便展开的可复用材料：模板供评审直接取用，对照表和场景卡供写作与检查遗漏，勘误表保证与既有 guide 的一致性。

- 附录 A：术语、实体、事件和 terminal reason。
- 附录 B：State Registry、Belief/World Model Registry、Effect Ledger、Plan Lease、Boundary Map 模板。
- 附录 C：热点交叉发现表与约 30 张场景卡。
- 附录 D：标准 runtime 故障包（含 stale plan、prediction mismatch、planner exploit）。
- 附录 E：Claude Code/Agent SDK、Codex、OpenAI Agents SDK、LangGraph、Temporal、Restate、MCP Tasks（2026-07-28）对照。
- 附录 F：来源、检索范围、确定性与利益相关声明。
- 附录 G：`harness-engineering-guide.md` 勘误表。

---

## 四、事实修正纪律

以下是核查中发现的易错表述，写作时必须按此口径落笔，不得回退到二手转述：

1. OpenAI Assistants API 截至 2026-07-13 是已 deprecated、计划于 2026-08-26 关闭，不写成已经关闭。
2. “LLM 调用不可重放”改为“不能重新执行并期待相同输出；首次结果应记录并在恢复时复用”。
3. “副作用 exactly-once 靠重放”改为“workflow decision 可重放；Activity/工具可能执行多次，依赖幂等、去重或补偿”。
4. SSE 的 `id/Last-Event-ID/retry` 只属于 EventSource 能力；服务端 replay、快照与其他流协议仍需实现。
5. OTel GenAI conventions 标明 maturity；内容字段默认敏感。
6. context anxiety 使用 Cognition 一手来源。
7. 所有“唯一评审级”“业界收敛”“学术空白”限制到检索范围与日期。
8. MCP 2026-07-28 规范定稿（发布日 2026-07-28）前引用一律标注 Release Candidate；定稿后回核 stateless、Tasks、授权硬化三处表述再落稿。

---

## 五、第二卷写作顺序

（v5.4 废止旧顺序。）2026-07-17 用户裁决：按阅读顺序逐章写、一章一审；2026-07-20 起 spec 先行——每章先审半页章 spec（推理链＋段落地图＋章级判据）再写正文。执行细则见 `volume2/SPEC.md` 与 `volume2/WRITING-PLAN.md`。原"先冻结术语再写语义"的动机由 v5.4 下沉方案吸收：各章自带首用概念的冻结职责（实体链在 §六、五平面在 §十一、部署基线在 §十四）。

第二卷完成后，第三卷直接复用其 runtime artifacts，不重新定义状态、事件和副作用语义。
