# 工作制品汇编 · 全卷登记表的单一真相源

> v1 · 2026-07-17 · 随各章升级，变更记录见文末。出版形态为书末附录。
> 正文各章引用这里，不各自另开表。本文件以表格为主体是刻意的——它是评审时直接取用的登记表，不是散文。
> **引用规则（SPEC §七.10.6）**：正文引用一律"工作制品＋节号＋名称"；新增节先登记下方目录，再进正文引用。

## 节号目录

![](figures/embed/tb-90-1a.png)

![](figures/embed/tb-90-1b.png)

![](figures/embed/tb-90-1c.png)

正文节序不是严格 A→Z：L 之后接 Q、R、S，再回到 M、N、O、P，然后从 T 排到 Z。这是逐章增补的先后；节号不改，各章按字母引用，查节以本表为准。

## A. State Registry v2（第六章 6.0 交付、章末升 v2——大纲 v5.4 自第一章下沉）

用法：每个持久状态对象一行。评审时逐行问四个问题——还有谁在写它？版本字段在哪？删除它意味着什么？进程在写它的半路被杀，重启后它处于什么状态？答不出的格子就是缺口。

![](figures/embed/tb-90-2a.png)

![](figures/embed/tb-90-2b.png)

![](figures/embed/tb-90-2c.png)

三条全表规则：每行记录一律带 `schema_version`；除顶层（conversation）外每行带完整父链外键，允许为空的层级显式置空——event 行以全量冗余 correlation 承载（C 节）；每行登记 **scope**（会话/项目/全局）——作用域是归属的一部分，注释自述不算数（6.2 节）。

三条裁决注（6.0 节）：attempt 不设独立实体——模型侧 invocation 行即 attempt（失败调用也成行），工具侧 effects.attempt_no 承载，跨层共享 retry budget 出现时升格；turn/compaction 摘要/policy decision 三者不设独立表（分别为字段承载、messages 特型行——第十章已裁决沿特型行，policy decision 已由第十一章裁决并入 events，见本表 policy decision 行）；lease/执行权为进程内授权对象，不入本表（6.0 节、第八章）。

## B. Effect Ledger v2（第一章登记结构，第八章主场；v2 随第八章升级）

一行 = 一次 Tool Execution 的账。四段模型：intent → attempt → result → outcome。

**字段**：

![](figures/embed/tb-90-3.png)

**状态机**：`intended → attempting → result_recorded → outcome_verified`；异常两分支——`intended/attempting → unknown →（对账）→ 调和终局`（intent 无 result，8.6 节），及 `result_recorded →（outcome 与 result 不符）→ 对账事件 → 调和终局`（8.10 节）；调和终局记入 reconciliation_status（retried/queried/compensated/manual 之一）。

**八条不变量**（1-5 为 v1 原有，6-8 随第八章新增）：

1. 先写 intent 再执行副作用。写账本与改世界分属两个系统，无法一次原子提交——这个结构就是 dual-write，换哪个顺序都躲不掉。intent 先行消不掉两写之间的崩溃窗口，它决定的是崩溃之后还剩不剩线索：先执行后记账，世界变了而账上空白，连"曾经想做"都扫不出来（guide 3.3 节）。
2. attempt 可以多次，result 只能记录一次；重试产生新 attempt_no，不覆盖旧 result。
3. outcome 需要独立证据，不允许从 result 抄写——"tool result 成功 ≠ 外部世界成功"（8.10 节）。
4. `unknown` 是合法状态而非缺失值：超时且远端不可查时，诚实标 unknown 交对账，不假装可自动回滚。
5. ledger 行是状态（可更新），每次状态转移同时向 `events` 追加对应事件（可信历史）。行与事件不一致时，以事件序列重建为准。
6. 执行权校验在副作用提交点，入口校验不算完成——await、确认框与 I/O 制造检查与提交之间的窗口；多实例形态为写入携带 fencing 编号、状态层拒绝旧编号（第八章 8.3）。
7. 派生副作用归属原 action：登记 derived_from_effect_id，纳入同一 barrier 与同一执行权校验，禁止 fire-and-forget（第八章 8.3）。
8. 执行权收回后到达的旧写入必须拒绝，并落 zombie trace 事件——拒绝本身是证据（第八章 8.3；第十三章消费）。

**四类处置表**（Reconciliation Table——intent 无 result 的调和裁决，第八章 8.6 正文表的登记版）：

![](figures/embed/tb-90-4.png)

## C. Event Schema v2（第一章登记结构，第十三章主场——v2 随第十三章升级：correlation 八级补全＋detector/certificate 事件）

**信封字段**（每条事件必带）：

![](figures/embed/tb-90-5.png)

**事件类型 v1**（按对象分组；`*` 号是恢复扫描的关键锚点）：

- run：`run.created` / `run.state_changed`* / `run.finalized`*
- step：`step.started` / `step.completed`*
- invocation：`invocation.requested` / `invocation.recorded`
- effect：`effect.intended`* / `effect.attempted` / `effect.result_recorded`* / `effect.outcome_verified` / `effect.reconciled`
- message：`message.appended`
- checkpoint / compaction：`checkpoint.created`* / `compaction.started` / `compaction.committed`* / `compaction.aborted`
- approval / timer：`approval.requested` / `approval.resolved` / `approval.expired` / `timer.set` / `timer.fired` / `timer.cancelled`
- 控制与异常：`policy.decided` / `error.raised` / `correction.appended`
- 检测器与证书（第十三章补）：`detector.probed`（sabotage 验证结果，进工作制品 Y）／ `absence.detected`（期望事件缺席告警）／ `certificate.issued`（Model Certificate 签发，进工作制品 Z）／ `model.refuted`（反例推翻模型，回指工作制品 N Counterexample Event）

**四条纪律**：

1. append-only，永不 UPDATE；记错了追加 `correction.appended` 指向原事件，不改历史。
2. 事件粒度到 step/消息完成，不逐 token——token delta 走流式投影通道，无恢复价值不入账（第六章持久化粒度纪律）。
3. 崩溃容忍按载体分。DB 型事件表由事务原子性兜底，不出半行；应用层守的是事务边界——状态行与事件同事务落地（6.1 节）。文件型事件日志（入门卷 6.3 节的 JSONL）才有半行问题：进程可能死在写半行时，恢复按最后一个完整事件截断，丢尾行不算数据损坏。append-only ≠ crash-safe，两件事分开保证。
4. 内部 schema 稳定优先；OTel GenAI semantic conventions 截至 2026-07 仍为 Development 状态【规范/官方文档】，只做导出映射不做内部依赖（第十三章、第三卷 17.2 节）。

## D. Runtime Trust Boundary v1（第十一章 11.4 填充——模板自第一章，v1 随第十一章填）

每条信任边界一行，登记四件事。评审用法：逐行问"跨这条边界时信任怎么变、失败会怎样、拿什么对账"。

![](figures/embed/tb-90-6.png)

## E. Entry-to-Kernel Routing Matrix v1（第五章 5.11 交付——大纲 v5.4 自第一章下沉）

规则：后四列凡不指向内核（run manager / Execution Kernel），即为入口捷径缺口。评审用法：拿被评系统逐行照填，空格或"入口自实现"即语义分叉；第五章破坏实验场景 4 的 contract test 按本表逐行验证（同一 cancel 从每个入口发起，必须路由到转移表同一行）。

![](figures/embed/tb-90-7.png)

## F. Intervention Point Map v1（第十一章 11.7 填充，assemble 细节第十章——大纲 v5.4 自第一章下沉）

![](figures/embed/tb-90-8.png)

三处分别留证，不能以一处代替另外两处。

## G. Component Register v1（第四章交付，第十五章评审对照物）

八组件卡完整六栏。正文（第四章）只展开样张与取舍，本表为登记全文；各深潜章升级本表对应行。
用法（评审侧）：逐行问三件事——这张卡在被评系统里叫什么？它的职责有没有唯一 owner？违约在 trajectory 里有没有事件？答不出的行就是缺口，记入评审的残余风险清单（第十五章）。

![](figures/embed/tb-90-9a.png)

![](figures/embed/tb-90-9b.png)

## H. Run 状态转移表 v1（第五章交付，第十四章参考实现按表执行）

用法：代码中改 `run.status` 的唯一路径（内核 transition 函数）按本表执行；表外转移拒绝并落 `error.raised`。触发事件为语义名，落盘一律走 C 节 `run.*` 事件类型，payload 携 trigger/guard/actor/terminal_reason。评审时逐行问：这条转移在被评系统里由哪段代码执行、事件落在哪。

![](figures/embed/tb-90-10a.png)

![](figures/embed/tb-90-10b.png)

四条表级规则：终态（completed/failed/cancelled）之间无任何行——终态不许互转，判错追加更正事件；terminal_reason 逐值挂类（第五章 5.4）——task_failed→业务失败，infra_failure、unrecoverable→基础设施失败，user_cancelled、preempted→用户取消，policy_rejected、budget_exceeded、queue_expired、hitl_expired→策略拒绝（后两值为时限耗尽子类，终态走 cancelled——拦下的是继续等待，与 run 出错分开）；本表变更即 schema 变更，随 state_machine_version 迁移（第五章 5.10）；waiting 崩溃后不回 waiting——它经 row 15 进 interrupted，出边只有 row 16（→queued）与 row 17（→failed），表里不设 interrupted→waiting 回路是有意的：回到 queued 重跑至审批点、再次挂起，等于让审批重来一次，旧授权不跨崩溃延续，恢复即重验（第十一章 11.6）。看门狗（row 8，进程在、run 卡死→直接终态）与启动扫描（row 15，进程没了、run 可能可救→interrupted 交恢复裁决）是两条不同的行，不得合并。

## I. Lifetime Matrix v1（第六章 6.11 交付——checkpoint/resume 携带物逐项声明）

规则：未列入本表的携带物默认"不保存、不恢复"；新增携带物先登记再实现。安全默认值是不隐式恢复。

![](figures/embed/tb-90-11.png)

## J. Projection Contract v1（第六章 6.3 交付）

适用对象：context（给模型的投影）、UI（给人的投影）、导出视图（trajectory/trace 的读侧）。

![](figures/embed/tb-90-12.png)

## K. Belief/World Model Registry v0（第六章 6.12 交付模板，第八章/第十三章消费）

规则：derived belief artifact，任何版本不覆盖 observation；反例必须能触发状态表示与转移规则的共同修订（6.12 节破坏实验口径）。

![](figures/embed/tb-90-13.png)

## L. 恢复语义表与 durability 选型记录 v1（第七章交付）

### L1. 四操作×四后果（第七章 7.8 正文表的登记版；第九章断线重连、第十一章授权重验回指）

![](figures/embed/tb-90-14.png)

### L2. durability 选型记录

![](figures/embed/tb-90-15.png)

规则两条：任一路线都必须回答 Diagrid 三问（失败检测/恢复触发/跨实例协调），框架不管的自己建；恢复过程自身落事件（第七章 L 级自检口径）。

## Q. Context Assembly Spec v1（第十章 10.1 交付，第十四章参考实现按它组装）

用法：一次 invocation 的 context 不是"塞历史"，是按本规格组装出的一份投影。评审用法：拿被评系统的 context 组装逐条问——每个成分能指回哪个持久对象？按什么排序？总量卡在多少预算？

![](figures/embed/tb-90-16.png)

规则：组装是确定性过程，同样的持久态与同样的 policy 组装出同样的视图（resume 可重建，10.8 节）。两类时变成分不在这套版本坐标里——带 TTL 的 memory 随时间失效，JIT retrieval 拉进来的外部正文随源头改动。它们不参与 replay 一致性："同一份"承诺的范围，是版本坐标覆盖得到的那部分。系统约束不进可压缩段（工作制品 R 纪律三）。

## R. Compaction Contract v1（第十章 10.3/10.4 交付）

用法：压缩是事务不是摘要。四条纪律逐条可检查，缺一条就有一类坏账。

![](figures/embed/tb-90-17.png)

三方耦合登记（10.3 节）：压缩改前缀→打断 prompt cache（成本）；resume→必须认准同一 compaction_version（10.8 节）；崩溃→失败回退纪律兜。压缩改视图、不改历史（第六章 6.6，transcript 原文事务提交前不裁）。

## S. Memory Provenance v1（第十章 10.5 交付；工作制品 A memory 行的字段实化）

规则：memory 是跨会话的长期记忆，无来历的 memory 是没人认领的真相源（主线二）。每条带四样，缺来历即污染源。单机参考实现可不实现 memory——本表是"若做 memory 必须带什么"的契约。

![](figures/embed/tb-90-18.png)

## M. Tool Contract v1（第八章 8.11 交付，第十五章评审逐工具索要）

用法：每个有副作用的工具一份契约，填不出的栏即缺口。三层校验的登记载体——schema 层管结构（工具入口）、语义层管前置条件（工具实现）、编排层管时机（内核），层次错位的校验是漏。

![](figures/embed/tb-90-19.png)

## N. Plan Lease 与 Counterexample Event Contract v1（第八章 8.12 交付）

规则：多步计划自带适用前提，前提失效计划失效；resume/重试/实例迁移不得只恢复动作队列而漏掉租约校验（第七章恢复语义接线）。

### N1. Plan Lease

![](figures/embed/tb-90-20.png)

失效条件三条：任一真实 observation 与预测不符；history cursor 前移而模型未重新认证；policy/authority 变化。任一命中即废止剩余动作队列，不逐步降级执行。

### N2. Counterexample Event

信封沿工作制品 C（事件信封）；专属字段：

![](figures/embed/tb-90-21.png)

两条消费规则：反例写入工作制品 K 的 known_counterexamples 栏，可触发 refuted_by 吊销链；反例是控制流事件——落盘同时触发废止与重新建模，只记日志不改控制流视为违约（第十三章证据边消费）。

## O. Stream Terminal Table v1（第九章 9.4 交付，第十四章 stream protocol 按表实现）

用法：流式响应的每一种收尾方式一行，判"成功交付"还是"失败关闭"。规则：默认 fail closed——没有明确读到"成功结束"信号的，一律判失败；`finish_reason` 是模型停止原因，不是传输成功提交点，不得单凭它判成功。评审用法：拿被评系统的流逐行照填，判成功的格子必须指出"成功在哪一刻、凭什么信号提交"。

![](figures/embed/tb-90-22.png)

配套一条提交点规则（9.4）：传输"成功"在完整内容写入下游之后提交，不在响应头（2xx）到达时提交；熔断许可带世代号、half-open 只发单个探测——与工作制品 B 提交点纪律、第五章 5.7 租约（工作制品 I 的 lease 行）同构。

## P. Interaction Semantics Table v1（第九章 9.5 交付）

用法：四个常被混用的词各一行，钉清它对 run 做什么、走第五章转移表哪一行、半轮内容归哪。规则：disconnect 不触碰 run 状态（不进转移表）；其余三词各对应唯一一条转移；四词不得互相冒充。

![](figures/embed/tb-90-23.png)

## T. Principal & Delegation Registry v1（第十一章 11.1 交付）

用法：登记谁在行使权力、权力从谁委托来。评审用法：拿被评系统的每个动作问"哪个 principal 发起、scope 多大、谁授的、到期没"。

**principal 五类**：

![](figures/embed/tb-90-24.png)

**委托记录**（每次委托一行）：

![](figures/embed/tb-90-25.png)

## U. Authority Lifecycle Matrix v1（第十一章 11.6 交付——主线五收口）

规则：授权不随状态自动恢复。resume/fork/replay 重建状态与执行，绝不静默复活旧授权；确需跨恢复保留的，显式列入本表并在变化后重验。与工作制品 I（Lifetime Matrix）的授权行同源，本表补授予与失效语义。评审用法：拿被评系统每一项跨恢复保留的授权，逐条问"它显式列进契约了吗、resume/fork 后重验了吗"——没列进契约却在恢复后仍生效的，就是授权白搭车。

![](figures/embed/tb-90-26.png)

一句话：状态可以回卷，授权不能白搭车（7.8 节 state continuity 推不出 authority continuity）。

## V. Common-mode Failure Matrix v1（第十一章 11.5 交付）

规则：纵深防御只在各层执行点与失效模式独立时成立。逐层填六列，共享同一件的层不算独立层。评审用法：数被评系统多层防御共享几个 parser/classifier，共享的那个即假底。

![](figures/embed/tb-90-27.png)

填法：`fail-open` 且共享依赖非空的层，是纵深防御里最先该补的假底。

## W. Parent-Child Run Contract v1（第十二章 12.8 交付——subagent=child run，契约沿父链继承）

规则：subagent 是 child run，不是新物种。多 agent 不引入第七类契约，是前十一章那六份在父子与并行下的递归组合。逐契约给单 agent 形态、父子继承规则、失效反例；再补协调专属的两项（收敛判据、输出信任）。评审用法：拿被评系统逐格问"这份契约在父子之间怎么继承"，答不出的那一格就是多 agent 破了的那一格。

![](figures/embed/tb-90-28.png)

协调专属两项：

![](figures/embed/tb-90-29.png)

填法：六契约行任一格答不出"父子怎么继承"，或协调两项缺"单点收敛"与"独立校验"，即多 agent 的破口。双层控制流（节点内自治 loop vs 跨节点编排 graph）是本表的运行前提——编排层确定，父才谈得上"可观测、可收敛、可校验"。

## X. Evidence Graph v1（第十三章 13.8 交付——对账边＋认识论七边）

规则：证据面是一张图。对账边回答"动作、结果、artifact、完成声明怎么对上"；认识论七边回答"系统为什么相信当前模型、什么证据推翻了它"——后者补给可执行 Belief/World Model（工作制品 K），不另造平行图谱。评审用法：拿被评系统的完成声明，沿边反查到 outcome 证据；拿它的模型判断，沿边反查到 grounds 与 certifies，问 certifies 有没有 scope。

对账边（本卷新立，不承入门卷的边定义）：`action --produces--> result`、`result --verified_by--> outcome`、`effect --writes--> artifact`、`claim --substantiated_by--> evidence`。入门卷 8.4 节那十条边（prompts/calls_tool/produces/verifies/scores/blocks/repairs/hands_off/supports/contradicts）登记的是跨件、跨 cell 的可观测关系，与这四条互补；同名的 produces 在本卷收窄为 action→result，端点类型与入门卷的"件→artifact 类型"不同。

认识论七边（可执行信念，Schema Harness/MODA 载体）：

![](figures/embed/tb-90-30.png)

## Y. Detector Test Record v1（第十三章 13.6 交付——检测器必须证明自己会触发）

规则：报警器坏了不会响，是证据面最隐蔽的失效。每个检测器登记一条 sabotage 验证记录，定期喂已知坏样本、验证它真的触发。评审用法：问被评系统每个报警器"最后一次被验证确实会响是什么时候"，答不上来的按未自证处理。

![](figures/embed/tb-90-31.png)

配套 absence 检测：为关键机制登记"期望出现的事件"，声明态与运行态对账，缺席即告警（`absence.detected` 事件，工作制品 C）。

## Z. Model Certificate v1（第十三章 13.8 交付——backtest 绿不等于泛化）

规则：完整历史 backtest 只证模型解释了已见样本（retrodictive consistency），不证未见状态上的 generalization。certificate 不接受只写 backtest=green，至少并列五类测试＋scope。评审用法：拿被评系统的模型证书，查它有没有 held-out 与 planner-adversarial 两栏——只有 full-history replay 的证书，是把历史拟合当泛化。

![](figures/embed/tb-90-32.png)

素材：一个公开 model-based harness 项目（实名待第六章终稿裁决）的公开 retained trajectories 里有大 final world model＋多份 level-specific 候选程序，说明"代码化"带来 inspectability、却不自动带来最小描述或泛化。引用纪律照 research/volume2/10（不引自述分数、不写 runtime 已开源、无 license 不复制代码）。

## 变更记录

| 版本 | 日期 | 变更 | 依据章节 |
|---|---|---|---|
| v1 | 2026-07-17 | 初版：Registry 15 行、Ledger 四段模型、Event 信封+24 类、Boundary 模板 | §一（原 §三，2026-07-19 架构前移重排） |
| v1.1 | 2026-07-19 | 大纲 v5.2 对齐：approval 行补 authority 不隐式恢复语义；新增 E（Entry-to-Kernel Routing Matrix）、F（Intervention Point Map）模板 | §一、§十 |
| v1.2 | 2026-07-20 | 大纲 v5.4 归属调整（§一瘦身下沉）：A 归 §五、E 归 §四、F 归 §十；文中"六不变量"表述一律读作"六契约承诺句"（行内编号为 v5.4 旧编号，v5.5 后读作：A 归 §六、E 归 §五、F 归 §十一） | 大纲 0.3/0.4、§一下沉表 |
| v1.3 | 2026-07-21 | 补记：新增 G（Component Register v1，八卡六栏＋评审用法行，随 §四 v1.0 产出） | §四 |
| v1.4 | 2026-07-21 | 新增 H（Run 状态转移表 v1，17 行＋三条表级规则；四维评审后看门狗自启动扫描行拆出为独立 failed(infra_failure) 行）；E 升 v1（意图适配/流转发两列填齐、新增 webhook 行、补 contract test 用法） | §五 |
| v2 | 2026-07-23 | A 升 v2：belief/world model 行、scope 全表规则（第三条）、三条裁决注（attempt 不设实体/三样不设表/lease 不入表）；新增 I（Lifetime Matrix v1）、J（Projection Contract v1）、K（Belief/World Model Registry v0 模板） | §六 |
| v2.1 | 2026-07-23 | 新增 L（恢复语义表 L1 四操作×四后果＋L2 durability 选型记录） | §七 |
| v2.2 | 2026-07-23 | B 升 v2：新增 action_class（v1 risk_class 细化）/derived_from_effect_id/committed_under 三字段、不变量 5→8（提交点校验/派生归属/zombie trace）、四类处置表并入（Reconciliation Table 归此）；新增 M（Tool Contract v1）、N（Plan Lease 与 Counterexample Event Contract v1）。四维评审后修正：reconciliation_status 枚举补 queried 并与处置表终局列统一、状态机补"result 与 outcome 不符"第二异常分支、A 表 artifact 行两向对账指针补 §8.10 主场 | §八 |
| v2.3 | 2026-07-23 | 新增 O（Stream Terminal Table v1，流终结真值表七行＋提交点规则）、P（Interaction Semantics Table v1，四词×对 run 影响×转移×半轮归宿）；A 表 message/approval 两行的 §9.7/§9.8 裁决在第九章正文兑现 | §九 |
| v2.4 | 2026-07-23 | 新增 Q（Context Assembly Spec v1）/R（Compaction Contract v1，四纪律)/S（Memory Provenance v1）；A 表 compaction 摘要行裁决不独立表＋补 compaction_version 字段、memory 行由占位实化为契约形态（owner/字段/撤销语义，指向 S 节） | §十 |
| v2.5 | 2026-07-23 | 新增 T（Principal & Delegation Registry v1）/U（Authority Lifecycle Matrix v1，主线五收口）/V（Common-mode Failure Matrix v1）；D 填充（Runtime Trust Boundary v1，七边界）、F 填充（Intervention Point Map v1，三干预点＋证据列）；A 表 policy decision 行裁决并入 events、补 principal＋enforcement point 字段 | §十一 |
| v2.6 | 2026-07-24 | 新增 W（Parent-Child Run Contract v1，父子 run 契约表：六契约×单 agent 形态/父子继承规则/失效反例＋收敛判据与输出信任两项协调专属）——subagent=child run、契约沿父链继承的登记形态 | §十二 |
| v2.7 | 2026-07-24 | C 升 v2：correlation 八级补全（信封加 invocation_id/effect_id/artifact_id，child 事件带父 run_id ＝第十二章跨 agent 因果链兑现）＋新增 detector/certificate 事件（detector.probed/absence.detected/certificate.issued/model.refuted）；新增 X（Evidence Graph v1，对账边＋认识论七边）/Y（Detector Test Record v1，检测器 sabotage 验证）/Z（Model Certificate v1，五类测试＋scope，backtest 绿≠泛化） | §十三 |
| v2.8 | 2026-07-26 | I 表补 prompt asset 两行——塑形片段随 checkpoint 记版本号或内容哈希、按记录版本重建（状态生命周期），系统约束片段不保存不恢复、恢复时取当前版（授权生命周期）；A 表 invocation 行 prompt_asset_ref 相应补版本要求。兑现 §10.8 新列的第三类时变成分处置 | §十 |
