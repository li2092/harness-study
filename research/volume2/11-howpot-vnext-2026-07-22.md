# Howpot vNext 素材快照（2026-07-10 → 2026-07-22）

> 采集日期：2026-07-22。来源：`/Users/jimi/ClaudeCode/Howpot`（feat/vnext 分支，采集时 HEAD `25edd6e5`）。
> 与 08-* 快照的关系：08 覆盖到 2026-07-09 摸底＋复审（§三 已消化）；本文件收集其后 154 个提交（07-10→07-22，爆发日 07-21 单日 51 个）的新素材。内部资料，不出版，可用真名；进正文一律按"桌面案例项目"口径脱敏，并逐条过暴露面台账（见 §五 悬案）。
> 一手文档指针：`howpot-chat/docs/decisions/ADR-001~008`、`howpot-chat/specs/agent-core-relay-resilience-audit-2026-07-21.md`（496 行，第二次审计）、`howpot-chat/specs/STATUS.md`、`howpot-chat/specs/evidence/`（gate 记录＋raw verdicts＋SHA-256 索引）、`howpot-chat/specs/development-orchestration/spec.md`（650 行）。

## 一、整体叙事：从"修 bug"到"契约工程"的一个月

这批改动自身就是一条可写进书里的弧线：

1. **07-09 摸底**（08 快照，§三 已用）：9 路审计、三缺口、S0 三 PR。
2. **07-21 第二次审计**：对两份中间文档（replan＋Codex 内核对比报告）做**正确性校验**后重排队列——发现修复路线图本身漏掉了 5 个跨系统 P0（silent success、熔断计数、PII 共享、run 并发写、Gate 双写口）。审计结论第 4 条原话："当前最危险的问题不是'重试不够多'，而是现役生产路径正在暴露 silent success"。
3. **E0 批次止血（B0-B4）**：每批次一个 ADR＋一个冻结 Gate 记录＋raw dispatch/review/qa 三份原始 verdict＋精确 candidate SHA，先红测后修复，owner 逐批验收。B0-B3 已验收，B4 已冻结派工。
4. **O0 开发编排治理**：把"用 agent 开发 Howpot"本身规范化成 Plan/WorkItem/Assignment/Run/Lease 契约（650 行 spec），与产品线分轨审批。

这条弧线的教学价值：同一个团队，从 §三 那种"事故→修补"进化到"审计→契约→批次门禁→冻结证据"，正是本卷从 §三 到 §十五 的路径在现实中的复演。

## 二、素材条目（按卷二章节归位）

### §五 Run 生命周期状态机（刚成稿，以下是印证＋升级素材）

1. **10 秒等待阈值 ≠ 放行超时**（audit P0-4 → ADR-007 §2）。原始 bug：`tryStart()` abort 旧 run 后 `waitForFinish()` 等 10 秒，超时**静默放行**新 run——write/edit/git 是 block-interrupt 工具不接受 abort，旧 run 卡住超 10 秒即新旧并发写工作区。修复裁决原话："10 秒只是可观测性阈值，不是 safety timeout，不得 resolve barrier、替换 map entry 或发放 lease"；STATUS 追加"后续批次不得把 10 秒等待阈值实现为 replacement 放行超时"。→ §五 5.5"抢占必须先收尾"的失效变体三号：等待有上限、上限一到放行＝把 barrier 做成了定时炸弹。极佳反例，§五 或 §八 修订时可补一句。
2. **防链式抢占**（ADR-007 §1.4）：同一停止窗口内多个 replacement 请求按到达顺序排队，"不得因为各自调用 tryStart() 而连续 abort 刚获得 lease 的前序等待者"。Gate 红测："并发 3 个以上 same-session 请求时严格按 intent 顺序发 lease，不产生'新 Run 刚启动即被后一 waiter abort'的链式抢占"。→ §五 破坏实验场景 1 的产品实测版（现成 N=3 类证据）。
3. **replacement intent 不预插消息行**（ADR-007 §1.5）：获得 lease 前不写 user/assistant 行，拿到 lease 后"恰好持久化一次"；进程在 intent 获 lease 前退出"不会伪造已执行记录"。→ §五 5.6 幂等＋§六 写时机。
4. **"正在安全停止"是 typed transient 状态，不是消息**（ADR-007 §2.2）："该状态不是 assistant prose，不进入会话消息、model view 或组织归档"。→ 投影与持久真相的边界又一例（§九 9.9 / §六 6.3）。
5. **进程重启后内存 lease 无效**（ADR-007 §4.3）＋ shutdown 时 drain run admission（commit `9c96fb38`）：退出流程先停止准入。→ §五 5.9 退出顺序的产品落地（对照 §三 kill_node 两秒强杀的旧形态——同一个系统前后两个时代）。
6. **B3 全程先红后绿**：`test(agent): reproduce run lease overlap`（87ab2264）→ `fix(agent): enforce run side-effect lease`（00a71427）；review 回流也是先 `reproduce B3 review blockers` 再修。Gate 文件 §3 标题就叫"变更前红测"。→ §二 破坏实验文化的开发流程版。

### §八 工具执行与副作用（本批最大增量，D2/E2 尚未实施、设计已冻结）

7. **lease 校验必须在副作用提交点**（ADR-007 §3.3）："仅在 agent/tool-call 入口校验不算完成，因为 await、确认框和 I/O 会制造 TOCTOU"——write/edit/git 在实际提交前复核 lease。→ §八 commit gate/Effect Gateway 的一手实现依据；与 §五 5.7 TOCTOU 同根，层次更深（工具内部的 check-to-commit 窗口）。
8. **派生副作用归属原 action**（ADR-007 §3.4）：write/edit 派生的 auto git snapshot "属于原 action：必须可等待并纳入 barrier，或在每个 git add/commit 提交点再次校验同一 lease。禁止 fire-and-forget 脱离 Run 生命周期"。B3 修复还包括 `git path lease ownership loss`（fd8dde10）与 `deferred native tool identities`（e0fa277a）。→ §八 lineage＋派生动作的归属问题，书里目前没有这个案例类型。
9. **zombie trace**（ADR-007 §3.6）：lease 释放后发生的旧 lease mutation "必须拒绝并写脱敏 zombie trace"。→ 被拒动作也要留证——§十三 absence/拒绝证据。
10. **四种 action class**（audit §5.5）：`read_only / idempotent / compensatable / non_replayable`；durable intent/result 首期**只覆盖 write/edit/git 三类高副作用**，"不先铺满所有工具"，partial/unknown 禁自动 replay、交人工调和。→ §八 8.4/8.6 的产品参数化＋"增量铺开"的工程节奏素材。
11. **异常回滚用 `pop()` 猜测**（audit P1 表）：多步失败按数组末尾弹出，可能弹掉 tool result 留下孤儿 tool_call；改为 step checkpoint 回滚＋alignment verifier。→ §六 6.7 tool_call 配对的反例实例。

### §九 Streaming（ADR-006 全篇是 §九 的主证据包）

12. **HTTP 200 之后流内报错、客户端吞成成功**（audit P0-1，证据链到 file:line）：Relay 在已返回 200 的 SSE 里写 `{"error":{"message":...}}`；Howpot `streamChat()` 只处理 usage/choices，无 choices 的帧 `continue`；循环结束**无条件产出 finish**。"空回复或半截回复可能以成功结束……客户端 retry 分类根本没有机会执行"。→ silent success 的传输层形态；§二"假通过"的近亲，§九 9.2/9.4 开场级案例。
13. **Terminal truth table**（ADR-006）：typed done / legacy [DONE] / typed error / EOF 无 terminal / 半帧 / malformed / 非法 envelope——每种结尾一行，全部 fail closed；"`finish_reason` 是模型停止原因，不是传输成功提交点"。→ §九 终结事件语义的现成登记表（书中可做成"流终结真值表"artifact）。
14. **熔断计数的成功提交点错位**（audit P0-2）：收到 2xx headers 即 `recordSuccess()` 清零失败计数，"连续三次 200 后中断"的上游永远打不开 circuit；half-open 无单 probe 所有权。修复：circuit permit 带 generation＋唯一 permit id，half-open 单 probe lease，"成功在 terminal 写入 downstream 后提交"。→ "成功在哪一刻算数"的第三个现场（§二 假通过在验收层、P0-1 在流层、这个在熔断层）；lease 模式在熔断层的复现。
15. **retryable 随 partial delivery 降级**（ADR-006）：客户端已交付 delta 后，typed `retryable:true` 强制降为 false——只保留"提交输出前可重试"。→ §九 9.10＋attempt 边界（E1）。
16. **跨层重试放大**（audit P1）：Relay 同主模型最多 11 次 × Agent 最多 3 次，无共享 deadline/budget——"11×3 乘法放大"。→ §九/卷三 分层重试预算的定量画像。
17. **脱敏与长度上限进 wire contract**（ADR-006）：用户可见 message ≤240 字符、诊断 ≤512、控制字符折叠、secret redaction 规则精确到 escaped JSON 的有界替换。→ §九/§十三 内容边界，也是"契约细到字符数"的样张。

### §二 判据 ＋ §十三 证据（Gate 造假与证据治理）

18. **`hasChanges` 曾写死 `true`**（ADR-008 背景 ＋ audit A8）：`run_verification` 硬编码；`successCriteria` 不在耐久契约里，占位值可通过。修复裁决："禁止任何 hasChanges: true/false 常量兜底"，缺失/stale 时必须真实执行一次 collect，失败返回 `changes_unknown` 并 fail closed；"常量和 UI 自报值不能充当硬门事实"，Gate fact 必须携带 `source、observedAt、artifactId/hash`（audit §5.6）。→ §二 fixture classifier 事故的同款（判据自己说谎），且这次是"事实来源不可信"变体——可作 §十三 13.10 completion claim 的反例。
19. **阶段双写入口**（audit P0-5 → ADR-008 §4）：`CodingController.transition()` 之外，`applyCompletionDecision()` 直改 `current_stage`——"Controller 是唯一 transition seam"的测试与实现不一致。修复：唯一 mutator＋expected-from CAS＋durable event 同事务；"completion policy 只计算候选 decision，不能直接持久化 stage"；验收反例第 3 条"直接调用 Store/SQL 改 stage 必须失败或无法编译"。→ §五"唯一路径纪律"在另一台状态机（Coding stage machine）上的独立复演——同款病、同款药，跨状态机成立的证据。
20. **ADR 自带验收反例清单**（ADR-008 尾节五条）：每条都是"什么必须失败"。→ negative control 从评测线（§二 破坏实验）长进了决策文档模板。
21. **证据治理五规则**（specs/evidence/README）：Gate 从模板创建；raw dispatch/review/qa 必存、Gate 正文只引用不替代；**Gate 冻结后不回改正文，owner 决策只追加后记**；fixture canonical hash 只在索引维护、升版新增不覆盖；原始证据必须脱敏。→ §十三 append-only 纪律应用在"开发过程证据"上；§十五 评审可直接要这套东西。
22. **candidate SHA 新鲜度规则**（STATUS §4）："candidate SHA 必须是 Review/QA 实际验证的精确提交；candidate 变化后旧结论立即 stale"——QA 曾拒绝过一个 stale SHA（gate 文件 §14.1"QA verdict、rejected SHA 与 candidate freshness"）。→ 评审结论绑定证据版本，§二 测量学"cache 摧毁 i.i.d."的流程版。
23. **"AI 自测只能写已实现/待验收；验收通过只能 owner 批准"**（STATUS §5）。→ 用户 CLAUDE.md 纪律第 10 条在产品仓库制度化的实证——learn-harness 方法论线直接引用。

### §十一 权限与隔离

24. **PII vault 跨请求共享可变状态**（audit P0-3 → B2）：单例 PIIEngine 持有可变 vault，chat/fetch 共用；并发请求可互相清空/污染映射，"在更坏的交错下存在跨请求错误还原风险"。修复：vault request-scoped，"pattern/config 可以共享，映射表不能共享"；B2 gate 补双并发交错测试。→ §十一 隔离边界（状态的 scope 归属），也是 §六"谁拥有这份状态"的隐私版。
25. **"只读"集合里藏着网络外发**（audit A9）：pre-exec 的"只读"工具含 `web_search/web_fetch/image_analyze`，跑在 policy/permission 之前——"不仅是执行顺序错误，还可能在门禁前发生网络与隐私外发"。→ §十一 read-only ≠ 无副作用（信息外流是副作用）；admission 顺序：先 run lease → 不可变 RunContext → policy → 一切外呼（audit P1 表）。
26. **Hook 静默 fail-open**（audit P1 表）：hook 命令非 0、HTTP 非 2xx、网络失败默认放行且缺审计。→ §一 1.3 hook 假落地的产品同款＋§十一 11.11 fail-open/closed 显式化。
27. **Skill 激活状态跨会话泄漏**（audit A10）：注释声称 session scope，实际按 projectPath 缓存共享。→ 注释与实现分叉（§二 隐式假设三形态之一"代码注释"）＋scope 声明必须可验证。

### §六 / §七（实体链与恢复的设计输入）

28. **Attempt 层**（audit §5.1）：Howpot 统一状态链是 Task→Run→Step→**Attempt**→Action，attemptId＝"同一步的网络/模型尝试；失败输出不可混入下一 attempt"。**本卷实体链（Conversation→Run→Turn→Step→Invocation/Tool Execution）没有 Attempt 层**——§六 6.0 冻结实体链时要么吸收（invocation 之下/之侧加 attempt），要么在裁决里说明为何不设（单机低重试场景 invocation 即 attempt）。这是本批素材里唯一直接挑战既有大纲结构的一条，写 §六 前必须裁决。
29. **结构化错误协议**（audit §5.2）：`ExecutionError{code, layer, phase, retryable, retryScope, sideEffectState, userActionRequired, causeId}`——尤其 `sideEffectState: none/unknown/partial/committed` 进错误对象。→ §八 8.6 / §九 错误分类的现成 schema 参照。
30. **E2 恢复设计**（audit §6）：崩溃后扫描未决 action："先 reconcile workspace/process/DB，再决定 mark committed、compensate 或请求用户"。→ §七/§八 对账三选一的产品表述。

### §十二 / §十四 / §十五

31. **Development Orchestration spec**（650 行，O0 已过 owner 评审修订）：把多 agent 开发本身契约化——Project/Plan/WorkItem/Assignment/Run 层级、managed worktree 生命周期、依赖/端口/数据库/Secret 隔离、Review 非强制单点＋QA 独立于 Review、findings 契约、shadow/enforce/break-glass、**Lease 与 zombie writer**（§8.4——lease 模式第三次出现：run 副作用、circuit probe、编排 worker）。→ §十二 多 agent 协调的完整一手案例；learn-harness"用 harness 方法管理 harness 开发"的元案例。
32. **fault injection 六场景族矩阵**（audit §5.8）：网络/流、用户操作、工具/模型、存储/进程、Relay、平台——含"连点发送、Stop 时 write/git、回滚后立即发送"这类用户行为族。→ §十四 标准故障包的现实对照表（比书中四杀丰富一个量级）。
33. **指标纪律**（audit §5.7）："不使用'调用成功率'冒充'任务成功率'"；`verified_run_success_rate`（成功终态且 verifier evidence 有效）；`silent_success_violation` 目标必须为 0。→ §二 测量学/§十三 的产品级指标定义。
34. **优化闭环**（audit §5.9）：eval corpus 含"历史真实失败的匿名化最小复现"、baseline trajectory diff、grounded verifier 优先 LLM judge 补充、达阈值才 canary、线上失败自动进候选 corpus。→ 四问"改进有数据吗"的完整产品化；与 Agent-Z harness 的 reward/消融体系互为印证。

### 方法论线（learn-harness / 认知诚实）

35. **对输入文档做正确性校验**（audit §2）：replan 的 15 条结论逐条判定"成立/成立但不完整/不成立"；Codex 对比报告的"路线选对了""Howpot 更强"被降级——"属于架构判断，不是可证伪的代码事实"；后续引用强制三标签 `code fact / inference / recommendation`"不得混写"。→ 认知诚实标准的工程化现场；§十五 评审"对 postmortem 归格"的姊妹动作（对 plan 归格）。
36. **审计边界声明**（audit 开头）："未连接生产 4098/4099……生产事件发生频率、真实账务和长流结论仍需在 E3 验证"；P0-1 特意注明"由于本轮未读生产日志，本文不推断实际发生次数"。→ 与本卷"数字逐条回核、不外推"同款纪律的独立样本。

## 三、与既有正文的接线与冲突点

| 本批素材 | 既有正文位置 | 关系 |
|---|---|---|
| 10 秒放行超时（条 1） | §五 5.5 抢占先收尾 | 新失效变体，§五 修订可补一句或留 §八 |
| 链式抢占红测（条 2） | §五 破坏实验场景 1 | 产品实测版，可升级"实证状态"行 |
| lease epoch active→stopping→terminal（ADR-007 §3.1） | §五 5.2"过渡语义由 guard 承载不单列状态" | **表面冲突需说清**：Howpot 的 stopping 是 lease（副作用许可）的状态，不是 run 状态机加第八态——恰好可作"lease 状态机与 run 状态机分层"的正面例证，但写作时必须点破，否则读者会拿它反驳 5.2 |
| Attempt 层（条 28） | §六 6.0 实体链（未写） | **结构裁决项**，写 §六 前必须定 |
| 阶段双写入口（条 19） | §五 5.3 唯一路径纪律 | 跨状态机复演，§五/§六 均可引 |
| hasChanges 造假（条 18） | §二 开场 fixture classifier | 同病第二例，§十三 主场更合适（避免 §二 重复） |
| PII vault（条 24） | §十一（未写） | 主场素材 |
| Terminal truth table（条 13） | §九（未写） | 主场素材，可直接 artifact 化 |
| 第二次审计整体 | §三"摸底先于动刀" | 闭环续集：摸底→修→再摸底→契约化，§十五 或卷尾可用 |

## 四、脱敏标准（2026-07-22 用户裁决，SPEC §七.6）

- **标准**：关键名字（产品名 Howpot/H-Relay/relay-next、内部系统名）必须脱敏；产品功能与作用照实说清即可；负面机制细节不因"可能指纹化"删减；不设逐条签字的暴露面台账。§三 threadKey/毫秒指纹悬案与 §五"确认挂起锁死"悬案已按此关闭。
- **落法**：正文沿用"桌面案例项目"匿名标签；Relay 类组件写作"配套中继服务"或按功能描述（"模型请求中继层"）；条 24-25 的 PII 缺陷照机制写，脱敏名字即可。
- 数字与 file:line：本文件保留原文坐标；进正文按入门卷惯例保留通用 file:line、隐去仓库名。
- 时间线：全部为 2026-07 内，与 §三"2026-07 摸底"同窗口。

## 五、采集方法与完整度

静态读码未做（仅读文档与提交信息）；ADR-001~008 中读了 006/007/008 全文与 001 的存在性；audit 496 行全读；gate 文件读了 e0-04 的节结构（append-only 回流闭环形态确认）；orchestration spec 读了节结构。B1/B2 gate 正文、raw verdicts、`replan-2026-07-21.md`、`project-context-and-org-intelligence-design-2026-07-21.md` 未读——写 §九/§十一/§十二 时按需补读。所有条目标注均可通过文首指针回核原文。
