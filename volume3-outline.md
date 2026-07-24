# 第三卷《Harness 生产工程》· 写作思路与详细大纲

状态：大纲 v2.3 · 2026-07-20（命名手术，与 vol2 v5.4 同批：原 0.4"七条生产不变量"并入 0.3 五类生产契约的承诺句列，"不变量"术语退役——同物双名会迫使读者交叉绑定两套清单，vol2 三次审回已验证此病。上版 v2.2 · 2026-07-19：补入 Belief/World Model 的泛化测试、portfolio/fallback 评测披露与内部搜索成本分账）

上游：`volume2-outline.md`（第二卷：正确、可恢复、可验证的 Harness runtime）。

下游：Harness Lab 深度卷（评测系统、弱 reward、消融、调优与自演进）。

原料：`harness-engineering-guide.md` + `research/volume2/` 的生产运维、安全、框架与学术路线；后续需要按本卷 P0 清单补抓。

---

## 〇、卷定位

### 0.1 本卷解决什么问题

> 怎样把一个语义正确的 Harness runtime 安全、稳定、经济地部署到生产环境，并在团队、流量、依赖和版本持续变化时仍然保持可控？

第二卷关注一次执行内部发生什么；第三卷关注一个长期运行的产品怎样被建设、发布、监控、恢复和治理。

生产工程不等于“部署上云”。它至少包含五类持续能力：

1. **可靠性**：依赖失败、容量不足和局部故障不把整个系统拖垮。
2. **安全性**：身份、权限、secret、数据和供应链有明确边界。
3. **可运维性**：状态可见、告警可行动、事故可响应、恢复可演练。
4. **可演进性**：模型、prompt、工具、代码和 schema 能兼容地变化。
5. **经济性**：资源消耗有预算、容量和止损线。

### 0.2 本卷不重新定义 runtime

以下内容直接引用第二卷，不在第三卷重新发明：

- run/turn/step/tool execution 状态模型；
- State Registry；
- Effect Ledger；
- Event Schema 与 Evidence Graph；
- cancellation、checkpoint、resume 和 HITL 语义；
- principal/delegation 的运行时数据模型；
- runtime meter、limit、version 接口。

第三卷的任务是把这些 artifact 接入数据库、网络、安全、测试、发布和 SRE 体系。如果第三卷需要修改第二卷的实体或契约，必须回到第二卷修订单源真相，而不是在生产层做兼容 hack。

### 0.3 五类生产契约

每类契约自带承诺句（原"七条生产不变量"，v2.3 起并入此表，见 0.4）；服务与防护两类各背两条承诺：

| 契约 | 承诺（一句话） | 核心问题 | 主要领域 |
|---|---|---|---|
| 服务契约 | 目标可度量：每项用户承诺有 SLI、目标值和统计窗口。故障可隔离：依赖、租户、会话和 worker 的故障有明确爆炸半径 | 对用户承诺什么质量，怎样量化？ | SLI/SLO、error budget、降级、支持 |
| 防护契约 | 身份可追责：每个动作可归因到用户、agent、服务和授权链。数据可治理：数据来源、用途、位置、保留、删除和访问都有记录 | 什么风险必须被硬边界限制？ | identity、secret、sandbox、egress、tenant、supply chain |
| 变更契约 | 变更可兼容：每次变更有版本、验证、迁移、灰度和回退边界 | 什么可以改变，旧状态怎么办？ | config、model、prompt、schema、migration、deployment |
| 运营契约 | 事故可恢复：备份、恢复、降级和应急流程经过真实演练 | 谁观察、响应、恢复和复盘？ | telemetry、alert、on-call、incident、DR |
| 经济契约 | 消耗可止损：请求、token、并发、时间和成本都有硬上限与拒绝策略 | 最多消耗什么，何时拒绝或终止？ | quota、capacity、rate、token、cost、admission control |

五类契约与第二卷六类 runtime contract 形成两层结构：第二卷保证“执行语义不含糊”，第三卷保证“生产承诺不靠运气”。承诺"故障可隔离"由 §五（依赖）、§七（资源）、§十二（租户）共同兑现；"事故可恢复"由 §十六（演练）、§十八（响应）共同兑现。

### 0.4 命名裁决：生产不变量并入契约（v2.3）

原"七条生产不变量"是五类契约的承诺句（服务、防护各两条，其余一对一），一物二名与 vol2 同病——vol2 三次审回确诊"同物多名迫使读者反复重新绑定"后，两卷同批手术。v2.3 起：承诺句并入 0.3 表格，"生产不变量"作为术语退役；正文泛指时说"五类契约的承诺"；历史文件中的"七条(生产)不变量"读作"生产契约承诺句"。

### 0.5 周全性检查：生命周期 × 质量属性 × 责任主体

生产问题用三个正交维度检查：

| 维度 | 枚举 |
|---|---|
| 生命周期 | 设计、开发、测试、发布、运行、变更、退役、删除 |
| 质量属性 | 正确性、可靠性、安全、隐私、性能、成本、兼容性、可运维性 |
| 责任主体 | 产品、开发、安全、平台/SRE、数据、运维、用户、外部 provider |

示例：

- 变更 × 兼容性 × 开发/SRE：旧 checkpoint 由新 worker 恢复失败，谁阻止发布？
- 运行 × 隐私 × 数据/安全：trace 中出现完整 tool result，谁负责发现与删除？
- 退役 × 可靠性 × 平台：旧模型下线前仍有 pinned run，怎样迁移或终结？
- 发布 × 安全 × 供应链：MCP/Skill 依赖发生变化，安装时的信任结论是否仍有效？

### 0.6 读者完成判据

读完应能回答：

1. 哪些指标真正代表用户成功，而不是系统内部忙碌？
2. 数据库损坏、网络半断、provider 限流分别怎样降级？
3. agent、subagent、tool 和 operator 的身份怎样授权、撤销和审计？
4. secret 怎样在不进入模型上下文和 sandbox 的情况下被使用？
5. model/prompt/tool/schema 版本怎样组成一次可复现执行？
6. 旧 run 和旧 checkpoint 在发布后由哪版代码处理？
7. 非确定性回归怎样进入 CI/CD gate？
8. kill -9、重复副作用、磁盘写满和 429 风暴是否演练过？
9. 告警是否可行动，事故证据是否完整？
10. 一个新 Harness 上线前怎样完成 Production Readiness Review？

### 0.7 双线阅读

全卷区分两条部署线：**单机/小团队线**（单租户、桌面或小型服务、无专职 SRE——入门卷三类读者的延长线）与**企业线**（多租户、合规要求、专职平台团队）。每章"轻量/标准/高保障"三档中，轻量档即单机线的最低充分解；§十二（多租户）、§十七（值班）、§十八（事故响应）以企业线为主，单机线读者只需取其对 runtime 的接口要求。写作纪律：每章末标注两线差异，防止全卷读成企业平台手册。

---

## 一、写作与教学设计

### 1.1 不写通用 DevOps 教科书

数据库、网络、安全、测试和 SRE 只讲与 Harness 有关的变化：

- 为什么模型调用的非确定性改变重试与回归；
- 为什么工具副作用改变事务和恢复；
- 为什么长跑 run 改变发布和回滚；
- 为什么 context/memory 改变数据治理；
- 为什么 agent delegation 改变身份与权限；
- 为什么多 agent 改变容量和成本。

读者需要掌握传统概念的作用边界，不需要在本卷重新学习数据库或 Kubernetes 全部知识。

### 1.2 一条生产化主线

将第二卷参考 runtime 从“开发机可用”逐步推进到生产：

1. 定义服务目标；
2. 外置状态与迁移；
3. 加入网络韧性与容量；
4. 建立身份、secret、租户和供应链防线；
5. 建立测试与发布门禁；
6. 接入 telemetry、告警和事故流程；
7. 做故障演练和恢复验收；
8. 完成成本与生产就绪评审。

### 1.3 每章固定模板

（v2.3 注：沿用 vol2 的写作教训——本模板是交稿前完备性检查单，不充当章结构；动笔时章结构按 `volume2/SPEC.md` 的推理链＋因果叙事硬规则执行，每章 spec 附章级判据（新概念数、前向引用数上限，读者带走一图一句一动作）；vol3 的二十章问题链在开写前另立。）

1. 生产事故或风险场景；
2. 对应哪项生产承诺；
3. 传统工程根基；
4. Harness 特有增量；
5. 价值/目标 → 原则 → design choice → evidence → tradeoff；说明为什么选这个设计点、牺牲什么、什么证据会推翻它；
6. 轻量/标准/高保障三档方案；
7. 与第二卷 runtime artifact 的接口；
8. 演练或验证；
9. owner、门禁和残余风险。

### 1.4 证据与来源纪律

沿用第二卷五级来源；新增两项要求：

- 安全事件与成本事故优先使用官方 postmortem、CVE、规范或可复核报告，不用广泛转载替代一手证据；
- 厂商产品保证必须精确到版本、部署模式和责任边界，不把 marketing 的“durable/exactly-once/secure”直接当技术契约。
- 反向工程、包提取和源码考古按版本快照引用，只作为实现证据，不提升为当前产品保证；涉及现行行为时用官方文档复核。

---

## 二、章节大纲

### 第一部分 · 生产就绪的定义（§一～§三）

#### §一 Demo 到生产之间缺的是什么

- 1.1 第二卷参考 runtime 在开发机上通过全部故障实验。
- 1.2 加入真实用户、并发、第三方依赖、版本变更后新增的变量。
- 1.3 “运行成功”与“服务可靠”的差异。
- 1.4 生产故障的三源分流：model、harness、infrastructure；外加 user/external system。
- 1.5 局部修复怎样造成系统回归。
- 1.6 本卷五类生产契约（承诺句见 0.3；不另立"不变量"清单）。

交付物：Production Gap Assessment。

#### §二 服务目标：SLI、SLO 与 Error Budget

- 2.1 从用户任务成功定义指标，不从 API 200 定义成功。
- 2.2 成功率：run success、verified outcome、partial completion。
- 2.3 延迟：首 token、交互等待、run 完成、HITL 等待分开。
- 2.4 恢复指标：resume success、orphan convergence、duplicate effect。
- 2.5 安全指标：policy deny、越权尝试、secret egress、untrusted content。
- 2.6 成本指标：cost/task、token/task、tool calls、wasted retries。
- 2.7 SLO 窗口、分位数、低流量系统和长尾任务。
- 2.8 Error budget 怎样约束功能发布和可靠性投入。
- 2.9 用户体验指标不能完全由内部 telemetry 代理。

交付物：Service Level Spec、Metric Dictionary。

#### §三 Production Readiness Review

- 3.1 上线门禁覆盖架构、数据、安全、容量、测试、运维、成本。
- 3.2 风险分级：只读建议、可逆写入、不可逆高价值动作。
- 3.3 高风险等级决定 sandbox、approval、审计和人工介入强度。
- 3.4 依赖清单、数据流图、信任边界、恢复目标。
- 3.5 owner 与升级路径：谁能停服务、撤销凭据、回滚版本。
- 3.6 Known Unknowns 与残余风险登记。
- 3.7 门禁必须有证据链接，不接受“已经考虑过”。

- 3.8 为什么门禁必须结构化：知道与做到的鸿沟是结构性的——承认问题会提前产生"已经做了什么"的满足感，改变的即时成本高于不改变的即时收益，纪律随时间自然衰减。所以 PRR 不设计成"要求团队记住"，而是做成不通过就无法继续的节点。约束可靠性三级：口头约定 < 流程检查 < 结构性约束——每把一条约束下沉一级，可靠性就从人的意志力转移到系统设计。3.7 的"证据链接"是这一原则的落地形态。
- 3.9 分层控制独立性评审：逐层登记 enforcement point、失效模式、共享依赖、fail-open/closed、fallback 与验证证据；控制数量不等于 defense-in-depth，PRR 必须显式检查 common-mode failure。

交付物：Production Readiness Checklist v1、Risk Register、Control Independence Matrix。

### 第二部分 · 传统工程底座（§四～§七）

#### §四 数据库与存储工程

- 4.1 从第二卷 State Registry 推导 schema，不从 UI 页面推表。
- 4.2 SQLite、Postgres、对象存储、向量存储各自职责。
- 4.3 事务隔离、并发写、连接池、锁与热点。
- 4.4 WAL、checkpoint 与备份不能混为一谈。
- 4.5 SQLite backup API、WAL 三文件风险与活跃写者。
- 4.6 schema migration：expand/contract、双读双写的适用边界。
- 4.7 checkpoint/event schema migration 与旧 fixture。
- 4.8 artifact 大对象、去重、校验和、对象存储生命周期。
- 4.9 retention、archival、GC、legal hold、删除传播。
- 4.10 加密、密钥轮换、租户键和行级隔离。
- 4.11 restore drill：恢复的不只是数据库，还有 artifact 和版本 manifest。

演练：WAL 未 checkpoint 时备份；迁移中 kill；恢复后核对 Effect Ledger。

交付物：Storage Architecture、Migration Plan、Restore Evidence。

#### §五 网络与外部依赖韧性

- 5.1 DNS、TLS、proxy、连接池、HTTP timeout 的真实失败方式。
- 5.2 connect/read/write/total timeout 分开配置。
- 5.3 retry/backoff/jitter 与第二卷副作用语义联动。
- 5.4 circuit breaker、bulkhead、fallback、load shedding。
- 5.5 429、rate-limit headers、retry-after、共享 provider 配额。
- 5.6 partial stream、半开连接、重复 webhook、乱序消息。
- 5.7 provider failover 会改变模型能力、tool schema、context、cache 和成本。
- 5.8 fallback 不能静默降低安全或验证等级。
- 5.9 dependency health 与用户可见降级。
- 5.10 request ID 与第二卷 correlation ID 对接。
- 5.11 本地代理、企业网络和数据驻留区域。

演练：429 风暴、DNS 失败、流中断、主 provider 不可用、fallback 能力不足。

交付物：Dependency Policy、Retry Matrix、Degradation Runbook。

#### §六 配置、版本与兼容性

- 6.1 Version Manifest：代码、模型、prompt、tool、policy、schema、checkpoint、evaluator。
- 6.2 配置 schema、类型校验、启动失败和安全默认值。
- 6.3 环境变量、配置文件、feature flag、远程配置的责任边界。
- 6.4 pinned model 与浮动 alias。
- 6.5 prompt/tool/policy 作为版本化 artifact，而不是散落字符串。
- 6.6 compatibility matrix：谁能读取谁的状态与事件。
- 6.7 配置漂移：声明态与运行态对账。
- 6.8 feature flag 组合爆炸和状态不可解释风险。
- 6.9 废弃策略：旧模型、旧工具、旧 checkpoint 的退役窗口。
- 6.10 版本元数据进入第二卷 invocation/run/evidence。

演练：运行中切 tool schema；浮动模型行为变化；旧 worker 读新状态。

交付物：Version Manifest、Compatibility Matrix、Deprecation Policy。

#### §七 进程、队列、资源与容量

- 7.1 进程监督、worker pool、queue、scheduler 的职责。
- 7.2 admission control：开始任务前判断是否接得住。
- 7.3 backpressure：入口、队列、provider、stream consumer 分层。
- 7.4 CPU、内存、磁盘、文件描述符、子进程和 GPU 资源。
- 7.5 token、request、concurrency、time 四轴配额。
- 7.6 reserve → consume → reconcile 的预算账本。
- 7.7 step cap、deadline、loop/no-progress detector。
- 7.8 多 agent budget tree 与 fan-out 上限。
- 7.9 per-tenant/noisy-neighbor 隔离。
- 7.10 capacity model：平均负载不够，必须看 burst 和长尾。
- 7.11 自动扩缩容与长跑 run 的 drain/termination。

演练：无限 tool loop、递归 subagent、队列积压、磁盘写满、worker OOM。

交付物：Capacity Model、Quota Policy、Load-shedding Test。

### 第三部分 · 安全与治理（§八～§十二）

#### §八 Agentic Threat Model 与防护架构

- 8.1 用户误用、模型误行为、外部攻击者三类来源。
- 8.2 资产：secret、用户数据、artifact、工具权限、算力、审计证据。
- 8.3 attack surface：prompt、tool output、memory、MCP、Skill、网络、文件。
- 8.4 可能性 × blast radius；优先降低爆炸半径。
- 8.5 model layer、control plane、environment layer、external content 四层防线。
- 8.6 probabilistic defense 与 deterministic boundary 的分工。
- 8.7 threat model 与风险等级、SLO、测试门禁联动。
- 8.8 映射 OWASP Top 10 for Agentic Applications 2026（2025-12-09 发布，ASI01–ASI10），不把 taxonomy 当控制措施；章-风险映射：ASI03 身份与权限滥用→§九，ASI04 供应链→§十一，ASI05 意外代码执行→§八与第二卷 §十，ASI06 memory/context 投毒→§十.8，ASI08 级联失败→§十六。
- 8.9 common-mode threat：多层控制若共用同一 classifier、parser、event loop、身份源或远程 policy service，单点故障可能同时击穿所有“层”；至少保留一个依赖独立、可验证且默认拒绝的硬边界。

演练：关闭或过载共享 classifier/parser/policy service，验证独立硬边界仍 fail-closed，检测器失效会产生可见事件。

交付物：Threat Model、Control Mapping、Common-mode Failure Matrix、Residual Risk。

#### §九 Identity、Delegation 与审计

- 9.1 人类身份系统为什么不足以表达 agent authority。
- 9.2 user、agent、subagent、service、operator principal。
- 9.3 on-behalf-of 与独立 workload identity；机制锚点：OAuth 2.0 Token Exchange（RFC 8693）act claim 保留委托链、SPIFFE/SPIRE 做 workload identity；方向锚点：NIST NCCoE 概念文件（2026-02-05）——复用 OAuth/SPIFFE/OIDC 适配而非重造。
- 9.4 delegation token：scope、audience、TTL、chain、revocation。
- 9.5 least privilege、least agency、just-in-time access。
- 9.6 subagent 权限收窄和跨平台委托；诚实边界：multi-hop delegation 是当前标准未解问题，按未解写。
- 9.7 approval decision 的归属、证据和过期；状态生命周期、execution 生命周期、authority 生命周期分开评审。
- 9.8 resume/fork/retry/migration 不得静默恢复旧 permission、approval、delegation token 或 credential；例外必须显式、限时并重新验证主体、scope、audience 与版本。
- 9.9 break-glass、operator escalation 与双人控制。
- 9.10 每个 Effect Ledger 记录授权链与实际执行身份。
- 9.11 撤销后对活跃 run、挂起审批和缓存凭据的处理。

演练：撤销用户权限后旧 run 继续执行；subagent 越权；服务 token 被重放；高风险 approval 后 resume/fork 或 worker migration，验证旧 authority 过期并重新审批。

交付物：Identity Architecture、Delegation Policy、Authority Lifecycle Matrix、Audit Query。

#### §十 Secret、数据安全与隐私

- 10.1 secret 不进入 prompt、context、tool result、trace、sandbox。
- 10.2 host-side broker、短期凭据、scoped token、secret injection。
- 10.3 egress control 与允许域名不等于安全数据流。
- 10.4 数据分类：公开、内部、机密、敏感个人信息。
- 10.5 数据流图：输入、context、memory、artifact、telemetry、provider。
- 10.6 provider retention、训练使用、区域、ZDR 限制——厂商保证精确到版本与部署模式：Anthropic ZDR 仅覆盖指定端点、安全分类器结果仍保留、Covered Models 保留政策 2026-06-09 起仅适用 ZDR 组织；OpenAI background mode 数据存约 10 分钟且不兼容 ZDR。
- 10.7 telemetry sampling、redaction、访问控制、删除和 legal hold。
- 10.8 memory poisoning 与持久化注入。
- 10.9 用户删除请求怎样传播到派生摘要、向量、artifact 和日志。
- 10.10 数据最小化：能记录结构化事实时不默认记录完整内容。

演练：secret 出现在 trace；删除会话后向量仍存在；恶意 memory 跨 session 生效。

交付物：Data Flow Diagram、Retention Matrix、Secret Handling Spec。

#### §十一 MCP、Plugin、Skill 与供应链

- 11.1 代码供应链和内容供应链是两种不同风险。
- 11.2 本地工具可审计、远程工具可随时改变行为。
- 11.3 版本固定、签名、来源、SBOM、漏洞扫描。
- 11.4 tool description/prompt asset 本身也是可执行影响面。
- 11.5 MCP server capability discovery 与权限最小化。
- 11.6 安装时审核不能替代运行时内容检查。
- 11.7 dependency confusion、typosquatting、恶意更新、撤包。
- 11.8 remote tool 行为漂移检测和 kill switch。
- 11.9 第三方故障、数据留存和 incident notification 合同。
- 11.10 供应链证据进入 Version Manifest 和 Evidence Graph。
- 11.11 MCP 2026-07-28 规范（定稿前引用一律标 RC）：授权硬化（RFC 9207 iss 校验、严格 aud、OAuth 2.1+PKCE）；协议层无状态化对已部署 server 的迁移影响；Extensions 框架与正式 deprecation policy 作为 11.9 合同条款的协议层对应；11.8 kill switch 对接 tasks/cancel。

演练：远程 MCP 改变返回内容；Skill 更新扩大权限；依赖被撤回。

交付物：Supply-chain Policy、Approved Component Registry、Drift Test。

#### §十二 多租户、治理与高风险场景

- 12.1 tenant boundary 贯穿存储、缓存、队列、trace、artifact。
- 12.2 per-tenant encryption、quota、worker/bulkhead 隔离。
- 12.3 cross-tenant memory、cache、retrieval 和日志泄漏。
- 12.4 高风险行业的人工控制点与证据保留。
- 12.5 数据驻留、审计导出、模型/工具准入。
- 12.6 policy-as-code 与组织例外流程。
- 12.7 管理员能力的最小化和审计。
- 12.8 用户知情、可撤销、可申诉与 partial automation。
- 12.9 监管/合规框架只做映射，不替代技术风险分析。

演练：跨租户 ID 猜测、共享缓存污染、管理员导出敏感 trajectory。

交付物：Tenant Isolation Matrix、Governance Control Map。

### 第四部分 · 测试、发布与恢复（§十三～§十六）

#### §十三 Harness 测试金字塔

- 13.1 复用第二卷 runtime contract tests。
- 13.2 单元测试：状态机、policy、budget、reducer。
- 13.3 contract test：model provider、tool、MCP、webhook、storage。
- 13.4 integration test：stream/cancel/checkpoint/effect/evidence。
- 13.5 E2E outcome test：真实环境状态，不只看最终文本。
- 13.6 replay/resume/migration fixture 长期保留。
- 13.7 security test：越权、注入、secret egress、恶意 artifact。
- 13.8 load/soak：长跑任务、队列、context、memory、磁盘增长。
- 13.9 fault injection：kill、断网、慢依赖、写满、重复投递。
- 13.10 测试数据、环境真实性和外部依赖模拟边界。
- 13.11 surface parity contract：同一 intent 经 UI/API/SDK/scheduler 进入同一 Execution Kernel，policy、tool、cancel、resume 和 evidence 语义一致；入口适配差异不得复制执行逻辑。
- 13.12 authority lifecycle fixture：resume/fork/replay/retry/migration 不能恢复 stale approval、permission 或 credential；测试同时覆盖主体、scope、上下文和版本变化。
- 13.13 Belief/World Model 测试不能止于完整历史 replay：并列 prospective next-step、held-out transition/episode、invariant/property-based 与 planner-adversarial test；专门搜索“模型允许但现实不成立”的计划，训练历史拟合不计为泛化证据。

交付物：Test Matrix、Fixture Registry、Coverage Gaps、Model Generalization Test Pack。

#### §十四 非确定性回归与 Eval Gate

- 14.1 trial、task、grader、trajectory、outcome 统一术语。
- 14.2 pass@k、pass^k、均值、置信区间的不同问题。
- 14.3 model/harness/infrastructure 方差分流。
- 14.4 假回归的硬数字：基础设施资源配置可使 agentic eval 分数摆动至 6pp（常大于相邻模型的榜单差距），约 3× 基线资源处存在相变——以下修 flakiness、以上改变被测能力（Anthropic infrastructure noise 工程文）；单次 pass@1 波动 2.2–6pp，temperature=0 时 std 仍 >1.5pp（arXiv:2602.07150）；缓存、并发、沙箱、网络是主要噪声源。
- 14.5 code-based、model-based、human grader 组合。
- 14.6 outcome grader 优先；trajectory grader 用于诊断和约束。
- 14.7 grader calibration、leakage、reward hacking、eval awareness。
- 14.8 held-out set、golden set、生产回放样本。
- 14.9 model/prompt/tool/policy 任何变更都触发对应 eval suite。
- 14.10 CI gate 由 14.4 噪声数字反推：多次独立运行 + 统计功效分析确定 run 数，不用单次阈值；什么波动阻止合并，什么进入人工调查。
- 14.11 不把短期 task pass rate 外推为代码库长期一致性或开发者理解；若后两者属于产品承诺，必须定义独立的 longitudinal metric 与观测窗口，否则明确列为评估范围外。
- 14.12 结果协议披露：明确 single-run pass@1、best-of-n、fallback/portfolio、重试和人工筛选；公开 routing threshold、模型/effort、所有 retained/discarded runs、动作与时间预算、Public/held-out/Semi-Private、harness 是否冻结。Schema Harness 的 98.98%/95.35% 作为反例教材：它们是项目自述的 Public-set fallback portfolio 结果，不是单模型 pass@1，也未获 ARC Prize 独立验证。
- 14.13 环境交互效率与内部计算效率分别报告：真实 action、model token/request、搜索节点、CPU/GPU、wall-clock、失败重跑和货币成本分账；“内部 search 不消耗环境动作”不能简写成“zero-cost planning”。

交付物：Eval Suite Map、Regression Policy、Gate Evidence、Evaluation Disclosure Card。

素材补充：research/volume2/10（Schema 公开 trajectories、fallback 规则、官方参照、retained/discarded run 缺口与 backtest 保证边界）。

#### §十五 发布、迁移与回滚

- 15.1 无状态服务发布方式为什么不足以覆盖长跑 agent。
- 15.2 active run：drain、pin-to-version、terminate、migrate；采用 Temporal Worker Versioning（2026-03-30 GA）术语：pinned 单版本完成、auto-upgrade、draining/drained、ramp、Upgrade-on-Continue-as-New 处理长跑 workflow。
- 15.3 canary、blue-green、rainbow deployment 的选择；rainbow 一手案例：Anthropic multi-agent research system；《Scaling Managed Agents》（2026-04，brain/hands 解耦）作为 15.1 的正面案例。
- 15.4 code/model/prompt/tool/policy/schema 变更分级。
- 15.5 database 与 checkpoint migration 的顺序。
- 15.6 向前/向后兼容窗口和混部 worker。
- 15.7 rollback 只能回代码，不能自动撤销副作用或数据迁移。
- 15.8 feature flag 回滚与已进入新状态的 run。
- 15.9 发布观察窗口、自动暂停和 kill switch。
- 15.10 退役旧模型、旧工具、旧状态和旧证据 schema。

演练：新旧 worker 混部；新 tool schema 中途回滚；旧模型突然下线。

交付物：Deployment Plan、Migration Runbook、Rollback Boundary。

#### §十六 故障演练与灾难恢复

- 16.1 chaos 不是随机破坏，而是验证具体假设。
- 16.2 标准故障包：kill -9、断电、断网、429、500、slow consumer。
- 16.3 状态故障：WAL、数据库只读、artifact 丢失、checkpoint 损坏。
- 16.4 副作用故障：超时后成功、重复执行、补偿失败、状态未知。
- 16.5 安全故障：凭据泄漏、MCP 投毒、越权、跨租户读取。
- 16.6 资源故障：递归 agent、磁盘写满、queue overload、OOM。
- 16.7 RTO/RPO 与 agent 状态、artifact、evidence 的分别定义。
- 16.8 backup restore、credential rotation、provider evacuation。
- 16.9 演练证据、发现缺口、更新 runbook 和 gate。
- 16.10 Game Day 频率、owner 与停止条件。

交付物：Failure Drill Catalog、DR Evidence、Open Gaps。

### 第五部分 · 运行、事故与经济性（§十七～§二十）

#### §十七 Telemetry、告警与值班

- 17.1 第二卷 Evidence Plane 到 logs/metrics/traces 的导出。
- 17.2 OTel GenAI conventions 与内部稳定 schema 的边界。
- 17.3 RED/USE 指标与 agent-specific 指标组合。
- 17.4 run、tool、provider、queue、budget、policy 关键指标。
- 17.5 告警必须对应用户影响、owner 和可执行 runbook。
- 17.6 absence-of-event、stuck run、silent detector failure。
- 17.7 cardinality、采样、成本与隐私。
- 17.8 dashboard 不能替代告警和定期对账。
- 17.9 on-call 需要哪些只读诊断与受控操作能力。

演练：关闭 detector、制造 stuck run、告警风暴、trace 后端不可用。

交付物：Telemetry Spec、Alert Catalog、On-call Runbook。

#### §十八 事故响应与证据保全

- 18.1 事故分级：用户影响、数据、安全、成本、合规。
- 18.2 stop-the-bleeding：kill switch、禁用工具、撤销 token、降级模型。
- 18.3 保存 event、trajectory、policy trace、artifact lineage、版本 manifest。
- 18.4 隐私与证据保全之间的冲突。
- 18.5 model/harness/infrastructure/user/external 五源归因。
- 18.6 timeline 从原始事件重建，不从聊天截图猜测。
- 18.7 临时缓解、根因修复、结构性门禁分开记录。
- 18.8 同类故障第二次出现时升级 taxonomy、test 或 hard control。
- 18.9 postmortem 无责，但 owner、deadline、验证证据必须明确。

交付物：Incident Template、Evidence Preservation Procedure、Action Tracker。

#### §十九 成本、性能与容量治理

- 19.1 单次调用价格不是任务经济性。
- 19.2 cost/task、cost/success、cost/verified outcome。
- 19.3 prompt cache 的读写价格、TTL、失效层级。
- 19.4 compaction、resume、model escalation 的缓存损益。
- 19.5 多 agent 的 token、并发和协调成本。
- 19.6 自愈、retry、replan 的收益与调用次数 proxy。
- 19.7 latency/cost/quality 三角，不用单指标优化。
- 19.8 tenant/project budget、预警、软限额、硬限额。
- 19.9 unit economics 决定哪些任务值得自治执行。
- 19.10 容量与成本回归进入发布门禁。
- 19.11 model-based planning 单独计量环境动作、仿真/搜索扩展、模型 token、CPU/GPU 与 wall-clock；只有第一项可称 action-free，不能把 simulator/search 的内部消耗归零。

交付物：Cost Model、Budget Dashboard、Optimization Decision Record。

#### §二十 生产案例与最终评审

- 20.1 将第二卷参考 runtime 完整生产化。
- 20.2 从开发机 SQLite 到服务部署的架构变化。
- 20.3 逐项通过数据库、网络、安全、测试、发布、SRE 门禁。
- 20.4 执行一次模型升级、tool schema 变更和 checkpoint migration。
- 20.5 执行一次 provider 故障与灾难恢复演练。
- 20.6 复盘仍然依赖人工判断的控制点。
- 20.7 形成残余风险、技术债与下一阶段 Harness Lab 输入。

最终交付物：Production Readiness Review 完整样例。

收束：

> 生产工程不是把所有风险消灭，而是让承诺有指标、风险有边界、变更有证据、事故有恢复路径、消耗有止损线。

---

## 三、附录

- 附录 A：Production Readiness Review 模板。
- 附录 B：SLI/SLO、Error Budget 与 Metric Dictionary 模板。
- 附录 C：数据流图、Retention Matrix、Tenant Isolation Matrix。
- 附录 D：Identity/Delegation、Secret、Supply-chain 评审模板。
- 附录 E：Test Matrix、Eval Gate、Fault Drill Catalog。
- 附录 F：Deployment/Migration/Rollback/DR Runbook。
- 附录 G：Telemetry、Alert、Incident 模板。
- 附录 H：成本与容量模型。
- 附录 I：来源、检索范围、确定性与利益相关声明（系统性审查截止 2026-07-13，见 `outline-review-20260713.md`；Schema Harness 专题增量核查至 2026-07-19，见 `research/volume2/10-schema-harness.md`；MCP 2026-07-28 定稿后回核 stateless/Tasks/授权三处表述）。

---

## 四、第二、三卷接口清单

第三卷开始前，第二卷必须交付：

1. 统一实体与 ID；
2. State Registry；
3. Run State Machine；
4. Effect Ledger；
5. Runtime Trust Boundary；
6. Event Schema 与 Evidence Graph；
7. Version/Meter/Limit 接口；
8. 标准 runtime 故障包。
9. Belief/World Model Registry、Model Certificate、Plan Lease 与 Counterexample Event（适用于可显式建模任务）。

第三卷完成后，向 Harness Lab 深度卷交付：

1. 版本化 trajectory 与 outcome；
2. model/harness/infrastructure 故障标签；
3. eval suite 与 grader calibration 记录；
4. policy trace 与 verifier evidence；
5. artifact lineage；
6. 成本、延迟、恢复和资源指标；
7. 生产事故与真实失败样本。

---

## 五、P0 调研清单

已关闭（一手源见 `outline-review-20260713.md` §二，写作时回读原文）：

1. NIST agent identity → NCCoE 概念文件（2026-02-05）+ CAISI；multi-hop delegation 未解，按未解写（已落 §9.3/9.6）。
2. OWASP → Top 10 for Agentic Applications 2026，ASI01–ASI10（已落 §8.8）；MCP/Skill 供应链 CVE/事故一手源仍开放，拆入下方第 11 项。
3. Temporal Worker Versioning → 2026-03-30 GA（已落 §15.2）。
4. ZDR/数据保留边界 → Anthropic/OpenAI 已核（已落 §10.6）。
5. OTel GenAI maturity → Development、独立仓库（research/volume2/07）。
7. eval 噪声 → Anthropic infrastructure noise（6pp、3× 相变）+ arXiv:2602.07150（已落 §14.4）。
9. rainbow/drain 案例 → Anthropic 两篇 + Scaling Managed Agents（已落 §15.3）。

仍开放（P0）：

6. provider rate limit、partial stream、request ID、model deprecation 官方契约全表。
8. SQLite/Postgres backup、restore、migration 的官方最佳实践。
10. agent 成本事故可复核一手来源；找不到则降级为社区案例并明确标注。
11. MCP/Skill 供应链的实际 CVE/事故一手源（自原第 2 项拆出）。

---

## 六、第三卷写作顺序

1. 先冻结第二、三卷接口清单；
2. 写 §二 SLO 与 §三 Production Readiness Review；
3. 写 §四～§七传统工程底座；
4. 写 §八～§十二安全治理；
5. 建 Test Matrix、Version Manifest、Fault Drill Catalog；
6. 写 §十三～§十六测试与发布；
7. 写 §十七～§十九运行体系；
8. 完成 §二十生产案例；
9. 最后回写 §一和附录。

正文写作前先产出模板和可执行 gate，避免流程纪律只停留在章节建议。
