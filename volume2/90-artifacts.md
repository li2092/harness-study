# 工作制品汇编 · 全卷登记表的单一真相源

> v1 · 2026-07-17 · 随各章升级，变更记录见文末。出版形态为书末附录。
> 正文各章引用这里，不各自另开表。本文件以表格为主体是刻意的——它是评审时直接取用的登记表，不是散文。
> **引用规则（SPEC §七.10.6）**：正文引用一律"工作制品＋节号＋名称"；新增节先登记下方目录，再进正文引用。

## 节号目录

| 节 | 名称 | 一句用途 | 交付章 |
|---|---|---|---|
| A | State Registry（状态注册表） | 每个持久状态对象的 owner、存储、删除语义、崩溃后归宿 | 第六章 6.0（v5.4 自第一章下沉） |
| B | Effect Ledger（副作用账本） | 一次工具执行的四段账：intent→attempt→result→outcome | 第一章登记结构，第八章主场 |
| C | Event Schema（事件信封与类型表） | 事件流的信封字段、事件类型与四条纪律 | 第一章登记结构，第十三章主场 |
| D | Runtime Trust Boundary（运行时信任边界） | 每条信任边界的跨越方式、失败模式与对账机制 | 第十一章填充 |
| E | Entry-to-Kernel Routing Matrix（入口到内核路由矩阵） | 每个入口六列，验证 permission/cancel/resume/工具执行只在内核 | 第五章 5.11 |
| F | Intervention Point Map（干预点图） | assemble/model/execute 三处干预点的平面归属与留证 | 第十一章 11.7 |
| G | Component Register（组件卡登记册） | 八组件卡完整六栏，第十五章评审的对照标尺 | 第四章 |
| H | Run 状态转移表 | run 的全部合法转移（17 行），转移契约的合同全文 | 第五章 5.3 |
| I | Lifetime Matrix（携带物生命周期矩阵） | checkpoint/resume 携带物逐项声明，安全默认不隐式恢复 | 第六章 6.11 |
| J | Projection Contract（投影契约） | 投影三条契约（有来源/可重建/不回写）与违约形态 | 第六章 6.3 |
| K | Belief/World Model Registry（信念工件登记模板） | 信念版本六字段：版本/history cursor/provenance/scope/反例/继任链 | 第六章 6.12 |
| L | 恢复语义表与 durability 选型记录 | 四操作×四后果（L1）＋两路线选型条件（L2） | 第七章 |
| M | Tool Contract（工具契约模板） | 每个工具一份：三层校验、action class、幂等与调和声明、取消语义、派生清单、错误报文 | 第八章 8.11 |
| N | Plan Lease 与 Counterexample Event Contract（计划租约与反例事件契约） | 计划的适用前提与失效条件；预测落空即废止剩余队列的控制流事件 | 第八章 8.12 |
| O | Stream Terminal Table（流终结真值表） | 流的每种收尾一行、判成功或失败、默认 fail closed | 第九章 9.4 |
| P | Interaction Semantics Table（交互语义表） | disconnect/cancel/interrupt/suspend 四词 × 对 run 的影响 × 触发转移 × 半轮归宿 | 第九章 9.5 |
| Q | Context Assembly Spec（上下文组装规格） | context 组装的来源/优先级/预算/去重/可信度——投影而非容器 | 第十章 10.1 |
| R | Compaction Contract（压缩契约） | 压缩事务的四条纪律：失败回退/边界落盘/系统约束不进压缩/配对修复 | 第十章 10.3 |
| S | Memory Provenance（记忆来历登记） | memory 每条的 provenance/TTL/撤销标记/scope | 第十章 10.5 |
| T | Principal & Delegation Registry（主体与委托登记） | principal 五类 × 委托记录（授予者/scope/期限/再委托/撤销） | 第十一章 11.1 |
| U | Authority Lifecycle Matrix（授权生命周期矩阵） | 授权的授予/范围/期限/失效条件/恢复重验——恢复≠恢复授权 | 第十一章 11.6 |
| V | Common-mode Failure Matrix（共因失效矩阵） | 每层防御的六列：强制点/失效模式/共享件/fail-open·closed/兜底/证据 | 第十一章 11.5 |
| W | Parent-Child Run Contract（父子 run 契约表） | 六契约 × 单 agent 形态/父子继承规则/失效反例，加收敛判据与输出信任两项协调专属 | 第十二章 12.8 |
| X | Evidence Graph（证据图） | 对账边（动作/结果/artifact/完成）＋认识论七边（grounds/predicts/certifies/refutes/derived_from/realizes/invalidates） | 第十三章 13.8 |
| Y | Detector Test Record（检测器测试记录） | 每个检测器的 sabotage 验证：喂什么坏样本/期望触发/实际触发/上次验证时间 | 第十三章 13.6 |
| Z | Model Certificate（模型证书） | 五类测试（replay/prospective/held-out/invariant/planner-adversarial）＋scope/history cursor/生成 provenance/已知反例 | 第十三章 13.8 |

正文节序不是严格 A→Z：L 之后接 Q、R、S，再回到 M、N、O、P，然后从 T 排到 Z。这是逐章增补的先后；节号不改，各章按字母引用，查节以本表为准。

## A. State Registry v2（§六 6.0 交付、章末升 v2——大纲 v5.4 自 §一下沉）

用法：每个持久状态对象一行。评审时逐行问四个问题——还有谁在写它？版本字段在哪？删除它意味着什么？进程在写它的半路被杀，重启后它处于什么状态？答不出的格子就是缺口。

| 状态对象 | owner（唯一写者） | 存储（单机参考实现） | 关键字段 | 读者 | 删除语义 | 崩溃后归宿 |
|---|---|---|---|---|---|---|
| conversation | Control（run manager 代理用户操作） | `conversations` | id、tenant、created_at、schema_version | Interaction（投影）、Execution（组装 context） | 用户删除；派生物传播规则 §6.10 裁决 | 无中间态（单行原子写） |
| run | Control（run manager） | `runs` | id、conversation_id（可空）、parent_run_id、triggered_by、status、terminal_reason、state_machine_version | 全平面 | 不可单独删；随 conversation 删除时保留审计副本与否 §6.10 裁决 | status=running 的孤儿由启动扫描收敛（§5.8） |
| message | Execution（agent loop 经写路径） | `messages` | id、conversation_id、run_id、turn_no、role、content_ref、schema_version | Interaction、Execution | 随 conversation | 半轮内容归宿 §9.7 裁决；已落库的不回滚 |
| turn | —（无独立表） | `messages`/`steps` 上的 turn_no | turn_no 单调递增 | — | 随所属对象 | 以最后完整 step 判定 turn 完成度 |
| step | Execution | `steps` | id、run_id、turn_no、seq、status（不设 kind——模型调用与工具执行是 5a/5b 级子实体，各以 step_id 挂在 step 下，§6.0 实体链） | Control（恢复扫描）、Evidence | 随 run | **恢复粒度锚点**：从最后完成 step 之后继续（§七） |
| invocation 记录 | Execution（model adapter） | `invocations` | id、step_id、model_id、prompt_asset_ref、context_digest、output_ref、token 计量、schema_version | Execution（重放复用）、第三卷成本 | 随 run；内容脱敏另议（vol3） | 已记录的结果恢复时复用，不重新调用（§七） |
| effect（Effect Ledger 行） | Execution（tool executor） | `effects` | 见本文件 B 节 | Control、Evidence、人工对账 | **原则上不删**——外部世界的账 | intent 无 result → 四类处置（§8.6） |
| checkpoint | Execution（经 checkpoint 写路径） | `checkpoints` | id、run_id、step_id、包含物清单、compaction_version、state_machine_version | Control（resume） | 随 run；保留策略 vol3 | 不完整 checkpoint 必须可识别并丢弃 |
| compaction 摘要 | Execution（compaction 事务） | `messages` 特型行（第十章裁决：不独立表，沿特型行；推翻＝需独立版本审计/跨会话复用） | compaction_version、provenance（由哪些消息压成）、边界序号 | Execution（context 组装）、resume | 随 conversation | 压缩事务失败回退，不留半压缩态（§10.4） |
| memory | Execution（memory 写路径；单机参考实现可不实现，字段契约见 S 节） | `memory`（未实现前占位，模板见 S 节） | provenance、ttl、revoked/revoked_by、scope、content_ref | Execution（context 组装） | 撤销可追溯（§10.5、删除三义 §6.10） | 随所属 conversation/项目；撤销标记持久 |
| artifact | Execution（tool executor 经登记路径） | `artifacts` + 文件/对象存储 | id、lineage（创建/修改它的 effect）、checksum、version | 全平面 | 删除 ≠ 撤销外部动作（§6.10） | 文件在而登记缺、登记在而文件缺——两向对账（工具层展开 §8.10，证据边 §十三） |
| approval（HITL 待决） | Control | `approvals` | id、run_id、请求内容、requested_at、expires_at、resolved_by、decision | Interaction（呈现）、Execution（等待） | 随 run；过期是显式终态 | **挂起即持久化**：重启后待决审批仍在（§9.8）；但已决 approval 的效力不随 resume/fork 自动延续——authority 不隐式恢复，需持久化的授权显式列入契约并在变化后重验（§11.6） |
| timer | Control | `timers` | id、run_id、fire_at、purpose、status | Control（扫描） | 随 run | 进程死后由启动/周期扫描接管（§7.7） |
| event | Evidence（各组件追加） | `events` | 见本文件 C 节 | 全平面（只读） | **永不更新、原则上不删**；保留策略 vol3 | 未提交事务整体回滚，不留半行；应用层守事务边界——状态行与事件同事务落地（§6.1、C 节纪律 3） |
| policy decision | Control | 并入 `events`（type=policy.decided）——§十一裁决不独立表；推翻＝需独立于事件流的合规审计/长期保留 | principal、规则、输入摘要、决定、依据、enforcement point | Evidence、审计 | 同 event | 同 event |
| belief/world model | Execution（建模路径） | `world_models`（派生工件表，在十一张实体链表之外；未实现前占位，模板见 K 节） | model_version、history_cursor、provenance、certificate_scope、known_counterexamples | Execution（规划）、Evidence | 随所属 conversation/task；版本不可变 | **derived belief artifact，不是真相**：崩溃后取最新已认证版本，不覆盖 observation（§6.12） |

三条全表规则：每行记录一律带 `schema_version`；除顶层（conversation）外每行带完整父链外键，允许为空的层级显式置空——event 行以全量冗余 correlation 承载（C 节）；每行登记 **scope**（会话/项目/全局）——作用域是归属的一部分，注释自述不算数（§6.2）。

三条裁决注（§6.0）：attempt 不设独立实体——模型侧 invocation 行即 attempt（失败调用也成行），工具侧 effects.attempt_no 承载，跨层共享 retry budget 出现时升格；turn/compaction 摘要/policy decision 三者不设独立表（分别为字段承载、messages 特型行——§十已裁决沿特型行，policy decision 已由 §十一裁决并入 events，见本表 policy decision 行）；lease/执行权为进程内授权对象，不入本表（§6.0、§八）。

## B. Effect Ledger v2（§一登记结构，§八主场；v2 随第八章升级）

一行 = 一次 Tool Execution 的账。四段模型：intent → attempt → result → outcome。

**字段**：

| 字段 | 说明 |
|---|---|
| effect_id | `eff_` 前缀 ID |
| run_id / turn_no / step_id | correlation 链 |
| tool_name / params_ref / params_hash | 调了什么、参数指纹 |
| idempotency_key | **派生自 run_id + step 序号 + 该 step 内的 effect 序号**（第三维也可直接用模型返回的 tool_call_id），不用内存计数器——同一 step 挂多笔工具调用时各自唯一，同一笔的多次 attempt 之间不变 |
| action_class | read_only / idempotent / compensatable / non_replayable——重发语义登记（第八章 8.4；v1 的 risk_class 细化为此四类，Control 决策输入沿用） |
| derived_from_effect_id | 派生副作用指回原 action；空即自身为原 action（第八章 8.3 纪律二） |
| committed_under | 提交时校验通过的执行权凭据——单机为进程内租约标识，多实例为 fencing 编号（第八章 8.3） |
| policy_decision_ref | 谁批准的（指向 policy decision） |
| intent_at | 意图落盘时刻——**必须先于执行** |
| attempt_no / last_attempt_at | 尝试可多次 |
| result_status / result_ref / result_at | 工具返回（成/败/超时/已取消），只记一次 |
| outcome_status / outcome_evidence_ref | 外部世界真实结果 + 独立证据（verifier、对账、artifact 校验） |
| reconciliation_status | none / retried / queried / compensated / manual / **unknown** |
| schema_version | — |

**状态机**：`intended → attempting → result_recorded → outcome_verified`；异常两分支——`intended/attempting → unknown →（对账）→ 调和终局`（intent 无 result，§8.6），及 `result_recorded →（outcome 与 result 不符）→ 对账事件 → 调和终局`（§8.10）；调和终局记入 reconciliation_status（retried/queried/compensated/manual 之一）。

**八条不变量**（1-5 为 v1 原有，6-8 随第八章新增）：

1. 先写 intent 再执行副作用。写账本与改世界分属两个系统，无法一次原子提交——这个结构就是 dual-write，换哪个顺序都躲不掉。intent 先行消不掉两写之间的崩溃窗口，它决定的是崩溃之后还剩不剩线索：先执行后记账，世界变了而账上空白，连"曾经想做"都扫不出来（guide §3.3）。
2. attempt 可以多次，result 只能记录一次；重试产生新 attempt_no，不覆盖旧 result。
3. outcome 需要独立证据，不允许从 result 抄写——"tool result 成功 ≠ 外部世界成功"（§8.10）。
4. `unknown` 是合法状态而非缺失值：超时且远端不可查时，诚实标 unknown 交对账，不假装可自动回滚。
5. ledger 行是状态（可更新），每次状态转移同时向 `events` 追加对应事件（可信历史）。行与事件不一致时，以事件序列重建为准。
6. 执行权校验在副作用提交点，入口校验不算完成——await、确认框与 I/O 制造检查与提交之间的窗口；多实例形态为写入携带 fencing 编号、状态层拒绝旧编号（第八章 8.3）。
7. 派生副作用归属原 action：登记 derived_from_effect_id，纳入同一 barrier 与同一执行权校验，禁止 fire-and-forget（第八章 8.3）。
8. 执行权收回后到达的旧写入必须拒绝，并落 zombie trace 事件——拒绝本身是证据（第八章 8.3；第十三章消费）。

**四类处置表**（Reconciliation Table——intent 无 result 的调和裁决，第八章 8.6 正文表的登记版）：

| 处置 | 适用条件 | 动作 | 账的终局（reconciliation_status） |
|---|---|---|---|
| 重试 | action_class=idempotent 且 key 在保留期内 | 同 key 重发，记新 attempt_no | retried（result 补齐） |
| 查询 | 目标系统提供读接口 | 查远端实况，回填 outcome | queried |
| 补偿 | action_class=compensatable | 执行逆操作，记一笔新 effect | compensated |
| 未知 | 以上都不可用 | 标 unknown，呈现给人 | manual |

## C. Event Schema v2（§一登记结构，§十三主场——v2 随第十三章升级：correlation 八级补全＋detector/certificate 事件）

**信封字段**（每条事件必带）：

| 字段 | 说明 |
|---|---|
| event_id | `evt_` 前缀 ID |
| seq | 数据库自增序号——**顺序的真相**（§6.0 全局规则一，不信 ID 里的时间戳） |
| occurred_at | 挂钟时间，仅供人读 |
| tenant / conversation_id / run_id / turn_no / step_id / invocation_id / effect_id / artifact_id | correlation 八级全量冗余，允许为空的层级显式置空（§十三 补全 invocation/effect/artifact 三级——child 事件带父 run_id 即第十二章跨 agent 因果链的兑现） |
| type | 见下 |
| payload / payload_ref | 小负载内嵌，大负载外置引用（stub/body 分离，入门卷 §5.6） |
| source | 产生事件的组件 |
| schema_version | — |

**事件类型 v1**（按对象分组；`*` 号是恢复扫描的关键锚点）：

- run：`run.created` / `run.state_changed`* / `run.finalized`*
- step：`step.started` / `step.completed`*
- invocation：`invocation.requested` / `invocation.recorded`
- effect：`effect.intended`* / `effect.attempted` / `effect.result_recorded`* / `effect.outcome_verified` / `effect.reconciled`
- message：`message.appended`
- checkpoint / compaction：`checkpoint.created`* / `compaction.started` / `compaction.committed`* / `compaction.aborted`
- approval / timer：`approval.requested` / `approval.resolved` / `approval.expired` / `timer.set` / `timer.fired` / `timer.cancelled`
- 控制与异常：`policy.decided` / `error.raised` / `correction.appended`
- 检测器与证书（§十三 补）：`detector.probed`（sabotage 验证结果，进工作制品 Y）／ `absence.detected`（期望事件缺席告警）／ `certificate.issued`（Model Certificate 签发，进工作制品 Z）／ `model.refuted`（反例推翻模型，回指工作制品 N Counterexample Event）

**四条纪律**：

1. append-only，永不 UPDATE；记错了追加 `correction.appended` 指向原事件，不改历史。
2. 事件粒度到 step/消息完成，不逐 token——token delta 走流式投影通道，无恢复价值不入账（§6 持久化粒度纪律）。
3. 崩溃容忍按载体分。DB 型事件表由事务原子性兜底，不出半行；应用层守的是事务边界——状态行与事件同事务落地（§6.1）。文件型事件日志（入门卷 §6.3 的 JSONL）才有半行问题：进程可能死在写半行时，恢复按最后一个完整事件截断，丢尾行不算数据损坏。append-only ≠ crash-safe，两件事分开保证。
4. 内部 schema 稳定优先；OTel GenAI semantic conventions 截至 2026-07 仍为 Development 状态【规范/官方文档，见 research/volume2/07 §3】，只做导出映射不做内部依赖（§十三、第三卷 §17.2）。

## D. Runtime Trust Boundary v1（§十一 11.4 填充——模板自 §一，v1 随第十一章填）

每条信任边界一行，登记四件事。评审用法：逐行问"跨这条边界时信任怎么变、失败会怎样、拿什么对账"。

| 边界 | 跨越方式 | 跨越时信任如何变化 | 典型失败模式 | 对账/证据机制 |
|---|---|---|---|---|
| 进程 ↔ 子进程 | spawn，进程组绑定 | 子进程应收窄权限，不自动继承父全权 | 子进程比 run 活得久、脱离生命周期（§8.8） | 进程组收割＋run 终态事件 |
| 主进程 ↔ worker | 多实例任务派发 | worker 持临时授权、非持久 | 双 worker 同认领、慢者带旧 fencing 写（§5.8） | fencing 高水位＋认领事件 |
| agent ↔ subagent | 派生 child run | 权限默认收窄，绝不继承 bypass | 继承父全权（§11.3） | Principal & Delegation（T）＋policy decision |
| runtime ↔ 网络/provider | 对外请求（egress） | 出口即副作用，信息可外流 | "只读"工具藏 web 外发、跑在 policy 前（§11.4） | egress 过 policy 门禁＋policy.decided |
| runtime ↔ 数据库 | 读写持久状态 | 单写者/租约约束（§六） | dual-write、跨库事务撕裂 | 事务＋事件双轨（§6.1） |
| runtime ↔ 工具/沙箱 | 工具执行，沙箱隔离 | 沙箱默认拒绝、显式放行 | secret 进沙箱、可写路径过宽 | bubblewrap 分层＋Effect Ledger（B） |
| runtime ↔ 用户 | 交互面投影 | 投影不回写、外来输入默认不可信 | UI 当真相源（§三/§九）、prompt 注入 | 投影契约（J）＋信任标签 |

## E. Entry-to-Kernel Routing Matrix v1（§五 5.11 交付——大纲 v5.4 自 §一下沉）

规则：后四列凡不指向内核（run manager / Execution Kernel），即为入口捷径缺口。评审用法：拿被评系统逐行照填，空格或"入口自实现"即语义分叉；§五 破坏实验场景 4 的 contract test 按本表逐行验证（同一 cancel 从每个入口发起，必须路由到转移表同一行）。

| 入口 | 意图适配 | 流转发 | permission | cancel | resume | 工具执行 |
|---|---|---|---|---|---|---|
| UI | 消息/操作→intent（携 idempotency key） | 订阅事件流重建投影 | 内核 | 内核 | 内核 | 内核 |
| API | 请求体→intent（调用方自带 key） | SSE / 轮询 | 内核 | 内核 | 内核 | 内核 |
| IM 渠道 | 平台消息→intent | 消息回推（异步分片） | 内核 | 内核 | 内核 | 内核 |
| scheduler/timer | timer.fired→intent | 无人值守：结果走库与通知 | 内核 | 内核 | 内核 | 内核 |
| webhook | 外部事件（验签）→intent | 无人值守：结果走库与通知 | 内核 | 内核 | 内核 | 内核 |
| SDK/CLI | 调用→intent | 流式回调 / stdout | 内核 | 内核 | 内核 | 内核 |

## F. Intervention Point Map v1（§十一 11.7 填充，assemble 细节 §十——大纲 v5.4 自 §一下沉）

| 干预点 | 平面边界 | 回答的问题 | 挂载机制 | 证据 |
|---|---|---|---|---|
| assemble | State→Execution（投影） | 模型这次看见什么 | context assembly（工作制品 Q，§10.1） | 组装决策落 policy.decided |
| model | Control→Execution | 这次可选哪些工具/动作 | tool 暴露与 policy（§11.3） | 暴露决策落 policy.decided |
| execute | Control→Execution/外部世界 | 是否授权并真正执行 | approval/sandbox/effect intent（§8.3） | effect intent＋policy.decided |

三处分别留证，不能以一处代替另外两处。

## G. Component Register v1（§四交付，§十五 评审对照物）

八组件卡完整六栏。正文（§四）只展开样张与取舍，本表为登记全文；各深潜章升级本表对应行。
用法（评审侧）：逐行问三件事——这张卡在被评系统里叫什么？它的职责有没有唯一 owner？违约在 trajectory 里有没有事件？答不出的行就是缺口，记入评审的残余风险清单（§十五）。

| 组件 | 职责一句 | 边界（明确不做什么） | 上下游接口 | 主守契约与守约方式 | 替代方案与取舍 | L 级起步 |
|---|---|---|---|---|---|---|
| 状态层 | 持久真相唯一落点，答"现在是什么" | 不答"怎么来的/凭什么信"；不做业务裁决；不为读侧长花样 | 写侧仅单一写者；读侧全组件只读 | 真相——单写者串行化＋owner/version＋状态变化落事件 | SQLite 单写者 vs Postgres+lease（多实例）vs 内存+快照（死于撕裂） | L2 |
| 事件流 | 发生过什么的机器可读记录（append-only） | 不当队列用（无投递承诺）；不存大负载（stub/body 分离） | 统一 emit 路径写入；恢复扫描/UI 订阅/审计读 | 转移——每次转移随行 trigger/guard/终结原因 | 单机表 vs 消息队列（投递语义换运维与可对账性）；可变行+审计表已排除（§一 1.4） | L2 |
| 证据存储 | trajectory/policy 决策/verifier 结论/artifact 来历归档 | 只存不判；不管实时呈现 | 归档写入；对账/回放/评审读 | 证据——归档独立于声称方 | 与事件流合储 vs 分储（访问模式分离换一条归属线） | L2 |
| run manager | 单执行内核：准入/互斥/policy/limit/孤儿收敛 | 不碰模型与工具；不长业务逻辑 | 入口层唯一下游；run 记录与终态持有者 | 转移+权限裁决点，交互收敛义务——三类决策有事件 | 内核集中 vs 入口自治（单点与评审瓶颈换语义只实现一次）；Routing Matrix §五 5.11 | L2 |
| agent loop | 一轮任务编排：组装 context→调模型→执行工具→循环 | 不持久真相（内存即易失）；不自证正确 | 由 run manager 派发；产出经他卡落盘 | 全契约履约现场，不单独 own | 手写同步循环 vs graph 引擎（声明式能力换落盘点透明）；两种 graph §八 8.12 | L1→L2（每步 emit） |
| 入口层 | 适配意图＋转发流（UI/API/IM/scheduler） | 投影不回写；不实现 permission/cancel 捷径 | 只对 run manager | 交互呈现半边——正确性押在"不写" | 薄投影 vs 胖客户端缓存（离线体验换第二真相源） | L1 |
| model adapter | 模型调用记账员：留档复用不重调 | 不做 routing 裁决；不解释输出 | loop 调用；恢复路径读档 | 转移+证据（调用记录即事件）——Temporal activity 先例 | 库内适配 vs 独立网关（集中计量换一跳延迟与新单点） | L2 |
| tool executor | 副作用唯一大门：先落盘意图→执行→落盘结果 | policy 判定不在此；结果解释不在此 | loop 调用；执行裁决结果；账本供对账 | 副作用——intent/result 双事件，外部另取证据 | 进程内 vs 子进程沙箱 vs 远端 worker（隔离强度换执行开销） | L2 |

## H. Run 状态转移表 v1（§五交付，§十四 参考实现按表执行）

用法：代码中改 `run.status` 的唯一路径（内核 transition 函数）按本表执行；表外转移拒绝并落 `error.raised`。触发事件为语义名，落盘一律走 C 节 `run.*` 事件类型，payload 携 trigger/guard/actor/terminal_reason。评审时逐行问：这条转移在被评系统里由哪段代码执行、事件落在哪。

| # | 当前状态 | 触发事件 | guard | 目标状态 | terminal_reason | 随行事件 |
|---|---|---|---|---|---|---|
| 1 | —（创建） | 入口意图经准入 | policy/limit 通过；同 idempotency key 无既有 run | queued | — | run.created |
| 2 | queued | 内核派发 | 同会话无活跃 run 且并发额度足够 | running | — | run.state_changed |
| 3 | queued | 用户取消 | — | cancelled | user_cancelled | run.state_changed＋run.finalized |
| 4 | queued | 排队超时（timer.fired） | 超过排队 deadline | cancelled | queue_expired | 同上 |
| 5 | running | 终答落盘 | 终答与消息终态已入库 | completed | — | run.finalized |
| 6 | running | 业务失败 | 失败已归因 | failed | task_failed | run.finalized |
| 7 | running | 基础设施失败 | 重试预算耗尽 | failed | infra_failure | run.finalized |
| 8 | running | 看门狗心跳超时（进程存活） | 超过 deadline 无活跃事件（step/effect 最近时刻为存活信号，§七 7.6） | failed | infra_failure | run.finalized |
| 9 | running | 策略/预算拦截 | policy.decided=deny 或预算耗尽 | failed | policy_rejected / budget_exceeded | policy.decided＋run.finalized |
| 10 | running | 用户 Stop | 半轮内容已终态化落盘 | cancelled | user_cancelled | run.finalized |
| 11 | running | 新意图触发抢占（裁决=interrupt） | 旧 run 半轮内容已终态化落盘 | cancelled | preempted | run.state_changed＋run.finalized |
| 12 | running | 需人工输入/审批（approval.requested） | 挂起已持久化 | waiting | — | run.state_changed |
| 13 | waiting | 审批/回复到达（approval.resolved） | 授权仍有效（§11.6 重验） | running | — | run.state_changed |
| 14 | waiting | 挂起过期（approval.expired） | 超过 waiting deadline | cancelled | hitl_expired | run.finalized |
| 15 | running / waiting | 启动扫描（进程已消失） | 进程标识已消失 | interrupted | — | run.state_changed |
| 16 | interrupted | resume 裁决可续跑（§七） | state_machine_version 兼容且 checkpoint 完整 | queued | — | run.state_changed |
| 17 | interrupted | resume 裁决不可恢复 | — | failed | unrecoverable | run.finalized |

四条表级规则：终态（completed/failed/cancelled）之间无任何行——终态不许互转，判错追加更正事件；terminal_reason 逐值挂类（§五 5.4）——task_failed→业务失败，infra_failure、unrecoverable→基础设施失败，user_cancelled、preempted→用户取消，policy_rejected、budget_exceeded、queue_expired、hitl_expired→策略拒绝（后两值为时限耗尽子类，终态走 cancelled——拦下的是继续等待，与 run 出错分开）；本表变更即 schema 变更，随 state_machine_version 迁移（§五 5.10）；waiting 崩溃后不回 waiting——它经 row 15 进 interrupted，出边只有 row 16（→queued）与 row 17（→failed），表里不设 interrupted→waiting 回路是有意的：回到 queued 重跑至审批点、再次挂起，等于让审批重来一次，旧授权不跨崩溃延续，恢复即重验（§十一 11.6）。看门狗（row 8，进程在、run 卡死→直接终态）与启动扫描（row 15，进程没了、run 可能可救→interrupted 交恢复裁决）是两条不同的行，不得合并。

## I. Lifetime Matrix v1（§六 6.11 交付——checkpoint/resume 携带物逐项声明）

规则：未列入本表的携带物默认"不保存、不恢复"；新增携带物先登记再实现。安全默认值是不隐式恢复。

| 携带物 | 随 checkpoint 保存？ | 随 resume 恢复？ | 恢复前重验？ | 所属生命周期 |
|---|---|---|---|---|
| 消息游标 / 最后完整 step 序号 | 是 | 是 | 否 | 状态 |
| compaction 版本与摘要引用 | 是 | 是（必须尊重边界，§10.8） | 否 | 状态 |
| state_machine_version | 是 | 是 | 版本兼容检查（§5.10） | 执行 |
| approval（已决审批） | 否（决策证据留 events） | 否 | 需重验（§11.6） | 授权 |
| delegation token | 否 | 否 | 重新授予 | 授权 |
| credential / secret | 否 | 否 | 重新获取 | 授权 |
| 工具子进程 / 沙箱句柄 | 否 | 否（重建） | — | 执行 |
| 内存 lease / 执行权 | 否 | 否（单机重启即失效；多实例为授权账协议保证，§6.0 裁决、主场 §八） | 重新取得 | 授权 |

## J. Projection Contract v1（§六 6.3 交付）

适用对象：context（给模型的投影）、UI（给人的投影）、导出视图（trajectory/trace 的读侧）。

| 契约 | 含义 | 违约形态（已见现场） |
|---|---|---|
| 有来源 | 投影每个成分都能指回持久对象 | 来源藏隐式键（按目录编码的会话存储，§6.5）；memory 来历不明（§10.5） |
| 可重建 | 任何投影可从持久态再生，不携带独家信息 | 内存攒半轮成果（§一 agent loop 约束）；客户端缓存当真相（§三 缺口二） |
| 不回写 | 投影侧缓存/猜测/修补不得进入真相 | UI 超时标 failed（§一 1.6）；localStorage 恢复线（§三） |

## K. Belief/World Model Registry v0（§六 6.12 交付模板，§八/§十三 消费）

规则：derived belief artifact，任何版本不覆盖 observation；反例必须能触发状态表示与转移规则的共同修订（§6.12 破坏实验口径）。

| 字段 | 说明 |
|---|---|
| model_version | 单调递增，版本内容不可变 |
| history_cursor | 生成所基于的事件序号区间 |
| provenance | 生成它的模型/提示/工具版本 |
| certificate_scope | 认证范围与保证边界（全历史回测只证明 retrodictive consistency） |
| known_counterexamples | 已知反例的事件引用 |
| refuted_by / superseded_by | 吊销与继任链 |

## L. 恢复语义表与 durability 选型记录 v1（§七交付）

### L1. 四操作×四后果（§七 7.8 正文表的登记版；§九 断线重连、§十一 授权重验回指）

| 操作 | 状态 | 执行 | 副作用 | 授权 |
|---|---|---|---|---|
| resume | 从最后完整点继续，历史不动 | 接着跑未完成部分 | 已记录不重做；intent 无 result 进对账（§八） | 不自动延续，按 I 节 Lifetime Matrix 逐项重验（§11.6） |
| replay | 只读重建，不新增历史 | 决策重演（审计/调试） | 零副作用 | 无需授权 |
| fork | 复制历史开新分支 | 两线独立 | 新分支新账 | 不复制，按新 run 重新授权 |
| time travel | 回历史 checkpoint 分叉 | 从旧状态重新出发 | 旧分支已发生的副作用不消失 | 同 fork |

### L2. durability 选型记录

| 条件 | 单机最低充分解（事件表＋intent/result＋启动扫描＋timer 扫描） | checkpoint 引擎（LangGraph 类） | journal 引擎（Temporal/Restate 类） |
|---|---|---|---|
| 单机单实例、本地副作用为主 | **默认选择**（§七 7.10 七步时序） | 图编排需求强时可用，三档 durability 显式选 | 确定性改造税通常不划算 |
| 编排跨进程/跨服务 | 不够——需自建协调 | 三件缺口自建（失败检测/恢复触发/跨实例协调） | **值回票价**：账本一致性＋单派发 |
| durable timer 密度高、错过成本高 | 自建扫描维护成本上升 | 同左 | 引擎 timer 原生 |
| LLM 结果复用 | invocation 留档（§六/§七 7.2） | 需自行保证节点内不重调 | Activity 结果缓存原生 |

规则两条：任一路线都必须回答 Diagrid 三问（失败检测/恢复触发/跨实例协调），框架不管的自己建；恢复过程自身落事件（§七 L 级自检口径）。

## Q. Context Assembly Spec v1（第十章 10.1 交付，第十四章参考实现按它组装）

用法：一次 invocation 的 context 不是"塞历史"，是按本规格组装出的一份投影。评审用法：拿被评系统的 context 组装逐条问——每个成分能指回哪个持久对象？按什么排序？总量卡在多少预算？

| 维度 | 规格 |
|---|---|
| 来源 | 每个成分能指回一个持久对象（消息/摘要/检索片段/系统约束）；来路不明的不进 |
| 优先级 | 系统约束 > 当前任务态 > 近期历史 > 压缩摘要 > 检索片段；预算不足时按逆序丢 |
| 预算 | 总 token 卡在窗口预算内（留出输出与 attention 余量）；超预算触发压缩（工作制品 R） |
| 去重 | 同一事实/工具输出只保留一份，重复项折叠 |
| 可信度 | 外部检索内容标来源、降权；投影不回写——组装是选材，不改真相（工作制品 J） |

规则：组装是确定性过程，同样的持久态与同样的 policy 组装出同样的视图（resume 可重建，§10.8）。两类时变成分不在这套版本坐标里——带 TTL 的 memory 随时间失效，JIT retrieval 拉进来的外部正文随源头改动。它们不参与 replay 一致性："同一份"承诺的范围，是版本坐标覆盖得到的那部分。系统约束不进可压缩段（工作制品 R 纪律三）。

## R. Compaction Contract v1（第十章 10.3/10.4 交付）

用法：压缩是事务不是摘要。四条纪律逐条可检查，缺一条就有一类坏账。

| 纪律 | 内容 | 违约形态 |
|---|---|---|
| 失败回退 | 压缩是原子操作，中途失败整体回退到压缩前，不留半压缩态 | 摘要写一半、原文裁一截，两不着（崩溃面） |
| 边界落盘 | 登记 compaction_version 与边界序号（摘要由哪些消息压成、边界落在哪条） | 压完不记版本，resume 无从对齐 |
| 系统约束不进压缩 | 系统约束（必须/不许类）不放进可压缩段，或压缩后无条件重新注入 | 约束被摘掉，模型之后无声违反 |
| 配对修复 | 压缩后扫 tool_call/tool_result 配对，落单的一起压或一起留（第六章 6.7） | 摘要吞 result 留孤儿 call，下次调用当场报错 |

三方耦合登记（§10.3）：压缩改前缀→打断 prompt cache（成本）；resume→必须认准同一 compaction_version（§10.8）；崩溃→失败回退纪律兜。压缩改视图、不改历史（第六章 6.6，transcript 原文事务提交前不裁）。

## S. Memory Provenance v1（第十章 10.5 交付；工作制品 A memory 行的字段实化）

规则：memory 是跨会话的长期记忆，无来历的 memory 是没人认领的真相源（主线二）。每条带四样，缺来历即污染源。单机参考实现可不实现 memory——本表是"若做 memory 必须带什么"的契约。

| 字段 | 说明 |
|---|---|
| provenance | 哪个 run、基于哪些事件写的 |
| ttl | 有效期；过期即失效，不无限生效 |
| revoked / revoked_by | 撤销标记＋撤销来源，作废可追溯（删除三义，第六章 6.10） |
| scope | 会话/项目/全局——作用域即归属，注释自述不算数（第六章 6.2） |
| content_ref | 记忆正文引用（stub/body 分离） |

## M. Tool Contract v1（第八章 8.11 交付，第十五章评审逐工具索要）

用法：每个有副作用的工具一份契约，填不出的栏即缺口。三层校验的登记载体——schema 层管结构（工具入口）、语义层管前置条件（工具实现）、编排层管时机（内核），层次错位的校验是漏。

| 栏 | 说明 |
|---|---|
| tool_name / 语义一句 | 这个工具动世界的哪一部分 |
| 参数 schema | 结构校验：类型、必填、取值范围；危险参数用形态防呆消除（如强制绝对路径） |
| 语义前置条件 | 路径存在、目标可写、状态允许——工具实现内校验 |
| action_class | read_only / idempotent / compensatable / non_replayable 四选一（与 B 表同枚举） |
| 幂等声明 | 天然幂等 / 靠 key（注明 key 来源与保留期）/ 不可重放 |
| 调和方式 | 可查询（读接口是什么）/ 可补偿（逆操作是什么）/ 都不可则显式登记"只能 unknown" |
| 长运行语义 | 预计时长档位；progress 通道；partial output 归宿（落 artifact 或丢弃） |
| 取消语义 | 接受信号＋宽限期 / 到提交点再拒绝——不接受中途放弃的工具必须选后者（第八章 8.8） |
| 派生副作用清单 | 会带出的后续动作（快照、索引、通知），逐项 derived_from 归属 |
| 错误报文契约 | 结构化：code / layer / retryable / sideEffectState（none-unknown-partial-committed 四值） |

## N. Plan Lease 与 Counterexample Event Contract v1（第八章 8.12 交付）

规则：多步计划自带适用前提，前提失效计划失效；resume/重试/实例迁移不得只恢复动作队列而漏掉租约校验（第七章恢复语义接线）。

### N1. Plan Lease

| 字段 | 说明 |
|---|---|
| plan_id | 计划标识 |
| model_version | 派生自哪个信念版本（工作制品 K 对应行） |
| history_cursor | 认证时所见的事件序号区间 |
| policy_version | 依据的 policy 版本 |
| preconditions | 显式前置条件（可校验断言） |
| expires_at | 时限——计划也有保鲜期 |

失效条件三条：任一真实 observation 与预测不符；history cursor 前移而模型未重新认证；policy/authority 变化。任一命中即废止剩余动作队列，不逐步降级执行。

### N2. Counterexample Event

信封沿工作制品 C（事件信封）；专属字段：

| 字段 | 说明 |
|---|---|
| plan_id / model_version | 被废止的计划与被反驳的信念版本 |
| predicted / observed | 预测与观察（引用，非全文） |
| diff_ref | 差异详情引用 |
| invalidated_action_count | 废止的剩余动作数 |

两条消费规则：反例写入工作制品 K 的 known_counterexamples 栏，可触发 refuted_by 吊销链；反例是控制流事件——落盘同时触发废止与重新建模，只记日志不改控制流视为违约（第十三章证据边消费）。

## O. Stream Terminal Table v1（第九章 9.4 交付，第十四章 stream protocol 按表实现）

用法：流式响应的每一种收尾方式一行，判"成功交付"还是"失败关闭"。规则：默认 fail closed——没有明确读到"成功结束"信号的，一律判失败；`finish_reason` 是模型停止原因，不是传输成功提交点，不得单凭它判成功。评审用法：拿被评系统的流逐行照填，判成功的格子必须指出"成功在哪一刻、凭什么信号提交"。

| 收尾方式 | 信号 | 判定 | 说明 |
|---|---|---|---|
| typed done | 明确的结束事件（带成功语义） | 成功 | 唯一无条件算成功的一行 |
| legacy `[DONE]` | 旧式哨兵字符串 | 成功（兼容） | 仅为向后兼容保留，新协议用 typed done |
| typed error | 流内错误帧（HTTP 200 之后） | 失败 | 配套中继服务审计的 P0 现场：客户端不得跳过错误帧后推定完成 |
| EOF 无 terminal | 连接自然结束但从未见结束标记 | 失败 | "循环跑完了"不是成功信号 |
| 半帧 | 最后一帧不完整 | 失败 | 按最后一个完整帧截断，缺尾不推定成功 |
| malformed | 帧格式错乱 | 失败 | 解析不了即失败，不 fail open |
| 非法 envelope | 信封字段非法/缺失 | 失败 | 协议违规，拒绝并留证 |

配套一条提交点规则（9.4）：传输"成功"在完整内容写入下游之后提交，不在响应头（2xx）到达时提交；熔断许可带世代号、half-open 只发单个探测——与工作制品 B 提交点纪律、第五章 5.7 租约（工作制品 I 的 lease 行）同构。

## P. Interaction Semantics Table v1（第九章 9.5 交付）

用法：四个常被混用的词各一行，钉清它对 run 做什么、走第五章转移表哪一行、半轮内容归哪。规则：disconnect 不触碰 run 状态（不进转移表）；其余三词各对应唯一一条转移；四词不得互相冒充。

| 词 | 含义 | 对 run 的影响 | 触发的转移（工作制品 H） | 半轮内容归宿 |
|---|---|---|---|---|
| disconnect（断开） | 网络连接断 | 不动 run，仅剥离流、等游标重连 | 无（不进转移表） | 不受影响，run 照跑照落盘 |
| cancel（取消） | 用户 Stop 终止 run | 终止 | running→cancelled（user_cancelled） | 终态化落盘（9.7 节） |
| interrupt（抢占） | 新意图，旧 run 让路 | 终止旧 run | running→cancelled（preempted） | 先终态化落盘、再进终态（第五章 5.5"抢占先收尾"guard） |
| suspend（挂起） | 等外部输入（审批/回答） | 暂停，不终止 | running→waiting；恢复 waiting→running；过期 waiting→cancelled（hitl_expired） | 保留在挂起点，恢复时授权重验（9.8 节、第十一章 11.6 节） |

## T. Principal & Delegation Registry v1（第十一章 11.1 交付）

用法：登记谁在行使权力、权力从谁委托来。评审用法：拿被评系统的每个动作问"哪个 principal 发起、scope 多大、谁授的、到期没"。

**principal 五类**：

| principal | 是谁 | 权力来源 |
|---|---|---|
| user | 真正的权力源头 | 自身 |
| agent | 替用户干活的 | user 委托（代理身份则为 user 权力子集） |
| subagent | agent 派出的分身 | agent 委托、默认收窄 |
| tool / service | 被调用的外部服务 | 调用方按 scope 授予 |
| operator | 运维/管理员 | 独立授权，与 user 分开 |

**委托记录**（每次委托一行）：

| 字段 | 说明 |
|---|---|
| grantor / grantee | 授予者 / 受权者 |
| scope | 授予的范围（能对什么做什么） |
| expires_at | 期限——授权也有保鲜期 |
| redelegatable | 能否再往下转授 |
| revoked / revoked_by | 撤销标记＋撤销来源 |

## U. Authority Lifecycle Matrix v1（第十一章 11.6 交付——主线五收口）

规则：授权不随状态自动恢复。resume/fork/replay 重建状态与执行，绝不静默复活旧授权；确需跨恢复保留的，显式列入本表并在变化后重验。与工作制品 I（Lifetime Matrix）的授权行同源，本表补授予与失效语义。评审用法：拿被评系统每一项跨恢复保留的授权，逐条问"它显式列进契约了吗、resume/fork 后重验了吗"——没列进契约却在恢复后仍生效的，就是授权白搭车。

| 授权对象 | 授予 | 范围 | 期限 / 失效条件 | 恢复时（resume/fork/replay） |
|---|---|---|---|---|
| approval（已决审批） | 请人签字 | 该次高风险动作 | 用完即止；expires_at 过期 | 不延续，重验（§11.6、Lifetime Matrix） |
| session permission | mode/规则授予 | 该会话 | 会话结束即失效 | 不恢复，重新授予 |
| delegation token | 上游委托 | token scope | expires_at；授予者权限被收回即失效 | 不恢复，重新授予 |
| credential / secret | 密钥管理 | 特定资源 | 轮换周期 | 不恢复，重新获取 |
| lease / 执行权 | 认领取得 | 该 run 副作用提交 | 重启即失效（§6.0、§8.3） | 不恢复，重新取得 |

一句话：状态可以回卷，授权不能白搭车（§7.8 state continuity 推不出 authority continuity）。

## V. Common-mode Failure Matrix v1（第十一章 11.5 交付）

规则：纵深防御只在各层执行点与失效模式独立时成立。逐层填六列，共享同一件的层不算独立层。评审用法：数被评系统多层防御共享几个 parser/classifier，共享的那个即假底。

| 层 | 强制点 | 失效模式 | 共享依赖 | fail-open / closed | 兜底 | 证据 |
|---|---|---|---|---|---|---|
| permission deny | 求值序最先 | 规则未覆盖 | 规则库 | fail-closed | — | policy.decided |
| sandbox | 系统调用层 | 路径规则过宽 | 无（内核强制） | fail-closed | — | 沙箱拒绝事件 |
| hook（软） | 工具执行前 | 解析失败即放行 | shell/解析器 | **fail-open（危险）** | 无 | 常缺（反例，§11.2） |
| classifier（软） | 内容检查 | 误判/被绕 | 模型/规则 | 视配置 | permission | 判定事件 |

填法：`fail-open` 且共享依赖非空的层，是纵深防御里最先该补的假底。

## W. Parent-Child Run Contract v1（第十二章 12.8 交付——subagent=child run，契约沿父链继承）

规则：subagent 是 child run，不是新物种。多 agent 不引入第七类契约，是前十一章那六份在父子与并行下的递归组合。逐契约给单 agent 形态、父子继承规则、失效反例；再补协调专属的两项（收敛判据、输出信任）。评审用法：拿被评系统逐格问"这份契约在父子之间怎么继承"，答不出的那一格就是多 agent 破了的那一格。

| 契约 | 单 agent 形态 | 父子继承规则 | 失效反例 |
|---|---|---|---|
| 真相 | 持久状态是唯一真相源（工作制品 A） | child run 状态挂父，单一真相源不因分身分裂 | 每个 child 各存一份真相 → N 份漂移（主线四） |
| 转移 | run 状态机＋唯一转移表（工作制品 H） | child 状态机独立，父可观测、终态回报父 | child 卡死父不知（无 correlation） |
| 副作用 | 四段账＋幂等（工作制品 B） | child 的 effect 账挂父链，幂等 key 从父 run_id 派生 | child 副作用无账，重放双份 |
| 交互 | 交互面是投影（工作制品 J/P） | child 无直接交互面，progress 经父投影 | child 直连 UI，绕过父的收敛 |
| 权限 | 运行时硬边界＋授权有期限（工作制品 T/U） | 有效权限＝agent ∩ user 取交集，收窄不继承 bypass | 取并集或继承 bypass → 权限蔓延 / Cross-Agent 提权 |
| 证据 | 只追加＋全量关联（工作制品 C） | child trace 以父 run_id 关联，跨 agent 因果链可重建（第十三章展开） | child trace 与父断链，因果不可重建 |

协调专属两项：

| 协调项 | 规则 | 失效反例 |
|---|---|---|
| 收敛判据 | 父显式定义（全成功／多数成功／关键子任务成功），并行产出在单点收敛写 | 无单一收敛点 → infinite handoff loop（谁都不 own 任务） |
| 输出信任 | child 回传默认不可信，经独立校验（校验器与被校验者不共享判断源）方采信 | 内部即可信 → 检查器信任被检查者（MAST 验证类失效 23.5%） |

填法：六契约行任一格答不出"父子怎么继承"，或协调两项缺"单点收敛"与"独立校验"，即多 agent 的破口。双层控制流（节点内自治 loop vs 跨节点编排 graph）是本表的运行前提——编排层确定，父才谈得上"可观测、可收敛、可校验"。

## X. Evidence Graph v1（第十三章 13.8 交付——对账边＋认识论七边）

规则：证据面是一张图。对账边回答"动作、结果、artifact、完成声明怎么对上"；认识论七边回答"系统为什么相信当前模型、什么证据推翻了它"——后者补给可执行 Belief/World Model（工作制品 K），不另造平行图谱。评审用法：拿被评系统的完成声明，沿边反查到 outcome 证据；拿它的模型判断，沿边反查到 grounds 与 certifies，问 certifies 有没有 scope。

对账边（本卷新立，不承入门卷的边定义）：`action --produces--> result`、`result --verified_by--> outcome`、`effect --writes--> artifact`、`claim --substantiated_by--> evidence`。入门卷 §8.4 那十条边（prompts/calls_tool/produces/verifies/scores/blocks/repairs/hands_off/supports/contradicts）登记的是跨件、跨 cell 的可观测关系，与这四条互补；同名的 produces 在本卷收窄为 action→result，端点类型与入门卷的"件→artifact 类型"不同。

认识论七边（可执行信念，Schema Harness/MODA 载体）：

| 边 | 含义 |
|---|---|
| observation --grounds--> model_version | 观察为模型提供依据 |
| model_version --predicts--> transition | 模型预测某个转移 |
| history_set --certifies--> model_version | 完整历史为模型背书（**必带 scope**：只证 retrodictive consistency，不证 generalization） |
| counterexample --refutes--> model_version | 反例推翻模型 |
| plan --derived_from--> model_version | 计划从某模型版本派生（回指工作制品 N Plan Lease） |
| commit --realizes--> plan | 提交兑现计划 |
| mismatch --invalidates--> remaining_plan | 预测与观察不符即废止剩余计划（回指工作制品 N Counterexample Event） |

## Y. Detector Test Record v1（第十三章 13.6 交付——检测器必须证明自己会触发）

规则：报警器坏了不会响，是证据面最隐蔽的失效。每个检测器登记一条 sabotage 验证记录，定期喂已知坏样本、验证它真的触发。评审用法：问被评系统每个报警器"最后一次被验证确实会响是什么时候"，答不上来的按未自证处理。

| 字段 | 说明 |
|---|---|
| detector_id | 检测器标识 |
| watches | 它监控什么（哪类事件的缺席、哪种异常） |
| probe | 喂进去的已知坏样本（sabotage 输入） |
| expected | 期望的触发行为 |
| last_probed_at | 上次验证时间 |
| last_result | 上次验证是否触发（pass＝触发／fail＝没触发即报警器失效） |

配套 absence 检测：为关键机制登记"期望出现的事件"，声明态与运行态对账，缺席即告警（`absence.detected` 事件，工作制品 C）。

## Z. Model Certificate v1（第十三章 13.8 交付——backtest 绿不等于泛化）

规则：完整历史 backtest 只证模型解释了已见样本（retrodictive consistency），不证未见状态上的 generalization。certificate 不接受只写 backtest=green，至少并列五类测试＋scope。评审用法：拿被评系统的模型证书，查它有没有 held-out 与 planner-adversarial 两栏——只有 full-history replay 的证书，是把历史拟合当泛化。

| 项 | 说明 |
|---|---|
| full-history replay | 完整历史逐步回放（retrodictive consistency） |
| prospective prediction | 下一步预测（未回放的前瞻） |
| held-out transition | 留出的转移／leave-one-episode-out（泛化侧） |
| invariant / property test | 不变量与属性测试 |
| planner-adversarial | planner 主动搜模型漏洞的计划，验证不被误当最优解 |
| scope / history cursor / 生成 provenance（模型/提示/工具版本）/ 已知反例 | 证书边界——兑现 §6.12 的四件随身证据，不能只写 backtest=green |
| 被认证的 model_version | 本证书覆盖哪个信念版本（工作制品 K 对应行） |

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
