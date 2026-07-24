# 学术与评测路线：guide 引源核对 + 2026 新工作

调研产出 · 2026-07-10 · workflow wf_2e1f15b2-4aa · 学术核对路（完整）

## 总结

Part A 七篇逐条核对：MAST(2503.13657，NeurIPS2025 评审级，占比41.77/36.94/21.30、Kappa0.88，已被 IBM+Berkeley IT-Bench 扩展)、Harness-Bench(2605.27922，23.8pp=NanoBot76.2-OpenClaw52.4、8后端6harness106任务)、六元组综述(2606.20683，notation 逐符号吻合)、T1-T4(2606.10106)、非加性(2604.25850，+11.1→+7.3pp、预测修好33.7%/弄坏11.8%)、沉默失败(2606.14589，60天/67空检查/70%人工发现) 六项全部与 guide 一致。唯一关键出入：自愈代价(2606.01416) guide 引的'15-25%成功率/20-40%延迟'查无实据，实为 +4.3~10.6pp、成本用调用次数 proxy，须勘误。Part B：中断研究井喷但仍只覆盖'用户改主意'不覆盖崩溃/抢占；durable execution 已成产业运动(DBOS/AWS/MS/Temporal 全产品)而学术仅预印(Springdrift 等)。判断'agent 专属运行时状态持久化几乎无同行评审研究'2026-07 仍成立且缺口扩大——需把 guide 措辞从'持久化无研究'精修为'agent 专属持久化无评审研究'，是第二卷最硬的'业界领先'空白点。

## 发现

### MAST 已定稿并被扩展引用（Part A 核对）

arXiv:2503.13657 'Why Do Multi-Agent LLM Systems Fail?' 与 guide 描述完全一致：NeurIPS 2025 Datasets & Benchmarks Track 正式收录（proceedings.neurips.cc + OpenReview id=fAjbYBmonr），已有 v2。三类占比精确核对无误：规范问题 41.77%、agent 间失调 36.94%、任务验证 21.30%（guide 写 41.8/36.9/21.3，取整正确）；Cohen's Kappa=0.88；1600+ 轨迹、7 框架。被引扩展已发生：IBM Research + UC Berkeley（Cemri, Pan, Stoica + IBM 团队）用 MAST 分析 310 条 SRE 场景的 IT-Bench 轨迹（Gemini-3-Flash / Kimi-K2 / GPT-OSS-120B），把多智能体故障分类法迁到企业 IT 运维场景。唯一未独立复核的小点：guide 标注的 'spotlight' 与干预实验 +15.6pp/+9.4pp 具体数字本轮未逐字复验（D&B track 收录已确认）。

- 来源：https://openreview.net/forum?id=fAjbYBmonr ; https://huggingface.co/blog/ibm-research/itbenchandmast ; https://ucb-mast.notion.site/
- 等级：【评审】
- 第二卷用法：第二卷'工程质量是独立变量'一章的锚点论据；MAST 是全套 harness 文献里唯一稳固过同行评审的一手源，可作为定量基石。IT-Bench 扩展作为'分类法可迁移到运维域'的案例，放在'故障归因与分类标签库'一节。

### Harness-Bench 23.8pp 精确核实 + 新增可用细节（Part A 核对）

arXiv:2605.27922 'Harness-Bench: Measuring Harness Effects across Models in Realistic Agent Workflows'（12 作者，含北大/Qiyuan Tech，2026-05-27，仅 v1）。23.8pp 差异逐字确认：NanoBot 76.2 vs OpenClaw 52.4，'giving a 23.8-point gap under the same task set and model-backend pool'。规模：6 个可配置 harness × 8 个 API 模型后端全因子矩阵、106 个沙箱离线任务、5194 条执行轨迹。execution-alignment failures 定义为'plausible reasoning becomes decoupled from tool feedback, workspace state, evidence, or verifiable output contracts'，占故障 36.4%（contract/format 违规）。新增可写进教程的定量结论：'Stronger model backends tend to achieve higher mean scores while exhibiting lower cross-harness variance'——越强的模型对 harness 配置越不敏感，弱模型受 harness 差异伤害更大。guide 对 harness 的引述语（'调控模型调用并将模型输出转化为外部工作空间中操作的系统层'）与原文表述（'the system layer that manages context, tools, state, constraints, permissions, tracing, and recovery'）语义一致但非逐字，教程正式引用建议改用原文措辞。

- 来源：https://arxiv.org/html/2605.27922v1 ; https://arxiv.org/abs/2605.27922
- 等级：【预印】
- 第二卷用法：'工程质量是独立变量'章的头号定量证据（23.8pp）。'越强模型对 harness 越不敏感'这条新细节可支撑一个反直觉论点：harness 工程对中小模型/本地部署的价值更高——正好贴民航/企业私有化部署场景，放在开篇立论或成本论证段。

### harness 六元组综述——notation 逐字吻合（Part A 核对）

arXiv:2606.20683 'From Question Answering to Task Completion: A Survey on Agent System and Harness Design'（Jianyuan Guo, Zhiwei Hao, Chengcheng Wang 等 15 作者，2026-06-14，v1）。六元组 notation 与 guide 逐符号一致：ℋ=⟨ℐ_obs, 𝒞, ℒ, ℐ_act, 𝒮, 𝒱⟩ = 观察接口/上下文管理/控制循环/动作接口/状态与产物存储/验证与治理。原文 Section 5 逐块拆解运行时职责。配套 GitHub（Awesome-Agent-Harness）标注综述覆盖 110+ 论文、23 个系统，并有 OpenReview 版本（id=eONq7FdiHa）。注意：初次检索时小模型把另一篇的 H=(E,T,C,S,L,V) 误挂到本篇，实际本篇就是 guide 用的那套 ℐ_obs 记号，无出入。

- 来源：https://arxiv.org/html/2606.20683v1 ; https://github.com/Gloriaameng/Awesome-Agent-Harness
- 等级：【预印】
- 第二卷用法：第二卷分析骨架的直接来源，六元组当全书结构主轴。综述覆盖 110+ 论文这一点，可用来向读者说明'harness 已成独立研究领域'，佐证教程存在的必要性。

### T1-T4 四要件——核对一致（Part A 核对）

arXiv:2606.10106 'What makes a harness a harness: necessary and sufficient conditions for an agent harness'（单作者 Sanderson Oliveira de Macedo，2026-06）。四核心要件 loop/tools/context/control 与 guide 的 T1 agent loop / T2 tool interface / T3 context management / T4 control mechanisms 完全对应。论文明确动机与 guide 一致：术语被滥用（有时指整个产品 Claude Code/Codex CLI，有时指 SWE-bench 评测脚手架，有时混同 SDK/IDE 插件/orchestrator），需要一个能一致纳入与排除案例的参照定义。围绕引擎（模型）的外围件清单：tool registry / context manager / memory / agent loop / verifier / retry+model switch / observability / guardrails / deterministic handlers。

- 来源：https://arxiv.org/abs/2606.10106 ; https://arxiv.org/html/2606.10106
- 等级：【预印】
- 第二卷用法：'什么算 harness'定义章的判定工具。T4（控制机制独立于模型是否配合）作为区分'真 harness'与'prompt 层软约束'的分水岭，是第二卷反模式章'软约束冒充硬控制'的理论依据。单作者预印本，引用需标局限。

### 组件非加性——数字精确但需重贴标签（Part A 核对，含框架性修正）

arXiv:2604.25850 实际标题是 'Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses'（Jiahang Lin, Shichun Liu 等，复旦系团队，v4 2026-05-18）。数字逐字确认：'The three positive single-component gains sum to +11.1 pp against full AHE's +7.3 pp'（非加性成立），且给了机理——memory/middleware/system-prompt 都推向同类闭包式验证，堆叠只是重复 re-check。预测精度也确认并可补强：fix-precision 33.7% / fix-recall 51.4%，regression-precision 11.8% / regression-recall 11.1%——即'agent 能说清一个改动为什么该有帮助，却说不出它即将弄坏哪些任务'。重要提醒：这不是一篇纯粹研究'非加性'的论文，而是一个自改进 harness 系统（AHE，三支柱可观测性：component/experience/decision observability）的系统论文，非加性与预测精度是其中的发现。guide 把它当'非加性研究'引用没错，但第二卷若展开应交代它其实是'harness 自动演化'工作——这本身是 Part B 的一个方向（自改进 harness）。

- 来源：https://arxiv.org/html/2604.25850 ; https://arxiv.org/abs/2604.25850
- 等级：【预印】
- 第二卷用法：'改进不可叠加、回归难预测'一节的核心数字（+11.1→+7.3pp；预测'修好'33.7% vs 预测'弄坏'11.8%）。补上 recall（51.4% vs 11.1%）能让'预测破坏几乎是瞎猜'的论点更狠。另可单开一节介绍 AHE 作为'自改进 harness'前沿（呼应 Self-Harness / HarnessBridge / HarnessX 一批新预印）。

### 自愈代价——guide 数字与该论文不符，需修正（Part A 核对，关键出入）

arXiv:2606.01416 'Self-Healing Agentic Orchestrators for Reliable Tool-Augmented LLM Systems'（Rahul Suresh Babu, Adarsh Agrawal，2026-06-02，v1）框架与 guide 一致（monitor-detect-diagnose-recover-verify 环），但 guide 引的定量结论对不上。guide 写'提升成功率 15-25%、带来 20-40% 延迟开销'——原文实测是：自愈 98.8% vs retry-only 94.5%（+4.3pp）；高压场景 97.3% vs 86.7%（+10.6pp）；单次恢复预算下 94.0% vs 85.3%。成本用的是相对调用次数 proxy 而非延迟百分比：自愈 3.25 反而低于 full replanning 3.63，但高于 retry-only（单预算下 3.13 vs 2.15）。论文自承局限是'合成任务比真实用户目标简单、不覆盖生产变异性'，并没有 guide 说的'对训练外新故障模式效果有限'那句话。结论：guide 的 15-25%/20-40% 两个数字在这篇里查无实据，方向（自愈有收益但吃算力）对，数字须替换为 +4.3~10.6pp / 调用数 proxy 上升约 45%（vs retry-only）。原始 15-25%/20-40% 可能来自另一份笔记的误并，第二卷不要照抄。

- 来源：https://arxiv.org/html/2606.01416v1 ; https://arxiv.org/pdf/2606.01416
- 等级：【预印】
- 第二卷用法：'恢复与自愈的代价意识'一节必须改数字：用 +4.3pp（常规）/ +10.6pp（高压）表达收益，用'调用次数相对上升、但低于全量重规划'表达成本。教训本身（自愈非免费、要有界+断路器+可观测）保留。这是本轮最重要的一处需回改，建议在第二卷标注'原 guide 数字勘误'。

### 沉默失败——核实无误，但已从'孤例'变成'一簇'（Part A 核对 + 框架修正）

arXiv:2606.14589 'When Errors Become Narratives: A Longitudinal Taxonomy of Silent Failures in a Production LLM Agent Runtime'（单作者 Wei Wu + 一个 AI 协作者，单一 personal-assistant 生产系统自 2026-03 连续运行，Draft v0.3，非同行评审）。细节逐条确认：五类 A 环境/平台怪癖、B 设计假设不匹配、C 错误吞噬与稀释、D 链式幻觉与编造、E 操作遗漏与取证盲点；22 起事故、meta-pattern 至少 28 次；~70% 靠人工观察输出发现而非测试/健康检查/治理审计；最长静默 60 天（外置 SSD 备份路径 EPERM，macOS TCC 全盘访问拒绝）；67 个空检查跨 21 个不变量执行 exec('') 空跑数月，靠新 invariant 的 sabotage validation 拒绝'失败不了'才暴露。guide 的单作者/单系统/非评审局限标注准确。但需更新框架：沉默失败已不是单一来源——同月出现 arXiv:2606.08162（Entropy Principle）与 2606.09863（False Success: 'From Confident Closing to Silent Failure'），构成一个 2026-06 的小簇。

- 来源：https://arxiv.org/html/2606.14589v1 ; https://arxiv.org/abs/2606.09863 ; https://arxiv.org/pdf/2606.08162
- 等级：【预印】
- 第二卷用法：'可观测性与沉默失败'一节的现场素材（60 天/67 空检查/70% 人工发现/sabotage validation）质量极高，且系统是 macOS+cron+SSD 备份——与 Howpot 案例同域，可直接并列。第二卷应把'单一非评审源'的措辞升级为'一簇早期预印，仍缺大样本评审'，既诚实又显示领域在成形。

### 中断/恢复研究井喷——但仍只覆盖'用户改主意'，guide 的空白判断成立（Part B）

中断类 benchmark 2026 H1 明显扩张，但语义边界没变。InterruptBench（arXiv:2604.00892 'When Users Change Their Mind'，Philip S. Yu 等，2026-04-01，预印）逐字确认三类 Addition/Revision/Retraction，且明确'exclusively user-initiated interruptions'——不含崩溃、基础设施故障、强制抢占。新出的 IHBench（arXiv:2606.19595，语音 agent 后中断恢复，10 企业域、6 种中断、27 个 audio-LM 配置，闭源模型随对话变长退化慢约 3.3×）和 SentinelBench（arXiv:2606.05342，长运行监控 agent）依然是'用户/环境输入型中断'，不是运行时被迫中断后的状态恢复。结论：guide 的判断'中断研究只覆盖用户改需求、不覆盖运行时强制中断（崩溃/抢占/进程被杀后的接续）'到 2026-07 仍然成立。

- 来源：https://arxiv.org/abs/2604.00892 ; https://arxiv.org/abs/2606.19595v1 ; https://arxiv.org/pdf/2606.05342
- 等级：【预印】
- 第二卷用法：第二卷'中断语义分层'章可明说：学界把'中断'窄化为'用户改需求'，而工程实践里最难的是'进程崩溃/被抢占后的状态接续'——这块几乎无学术覆盖。这是教程可以理直气壮说'业界跑在学术前面'的第一个具体空白点。IHBench 的 3.3× 退化数据可作为'长程 + 中断双重压力下模型能力断崖'的旁证。

### 运行时状态持久化：判断仍成立且缺口在扩大（Part B 核心判断）

对'运行时状态持久化几乎没有同行评审研究'的 2026-07 复核结论：仍然成立，且应细化。学术侧只有预印本触及、无顶会/期刊专门实证：Springdrift（arXiv:2604.04660，单作者 Seamus Brady，持久化运行时 + case-based memory + 规范安全，未实证 crash-recovery 正确性）、Turn: A Language for Agentic Computation（2603.08755）、AgentRunner（2605.10223）、CAAF 确定性（2604.17025）；六元组综述等只把状态存储 𝒮/durable execution 当组件列出、不做机制实证；Harness-Bench 把 recovery 当一个配置维度但不隔离持久化机制。搜 OSDI/SOSP/NSDI/EuroSys 2026 未见 agent 状态持久化专文。关键细化：durable execution 本身有几十年 DB/分布式的评审文献（ARIES、saga、workflow recovery），缺的是**agent 专属**的持久化研究——LLM 调用不可重放、工具副作用对账、压缩边界即 checkpoint 边界这些新问题。所以正确说法不是'持久化无研究'，而是'agent 特有的运行时状态持久化几乎无评审研究，传统持久化理论需降维借用'。

- 来源：https://arxiv.org/pdf/2604.04660 ; https://paper.lingyunyang.com/reading-notes/conference/nsdi-2026
- 等级：【预印】
- 第二卷用法：这是第二卷最有价值的'学术空白点'招牌。建议专设一节：先承认传统持久化（WAL/ARIES/durable execution）有厚实评审基础，再点明 agent 三个新问题无人系统研究，最后收到'第三章借传统理论降维'的写法上。把 guide 原话从'持久化无研究'精修为'agent 专属持久化无评审研究'，更准也更难被挑刺。

### Durable execution 已成产业运动——业界领先的实证（Part B）

与学术空白形成对照，运行时持久化/checkpoint 在业界 2025-2026 已产品化落地，全部是官方文档/工程博客级别、无一同行评审：DBOS（数据库落 workflow+step 状态，直接集成 OpenAI Agents SDK）、AWS Lambda Durable Functions（2025-12 发布，支持 steps/waits/checkpoints/replay/retries/long suspensions）、Microsoft Durable Task for AI agents（2026-04 更新，定位 checkpointing+coordination 基础设施）、Microsoft Agent Framework 的 Checkpoint Manager、Temporal+OpenAI/LangGraph、Mastra durable agents。核心工程共识与 guide 3.3/4.2 一致：'You cannot replay an LLM call and pretend it is the same event—输出必须首次记录、恢复时复用'（非确定性隔离）。有一条常被引的定量（需降级标注）：>4 小时长运行 agent 若无状态持久化，因 API 超时/基础设施中断导致整体失败的风险高 90%——来源是 Indium 商业博客（二手，非评审，勿当硬数据）。

- 来源：https://vadim.blog/durable-execution-llm-agents/ ; https://www.indium.tech/blog/7-state-persistence-strategies-ai-agents-2026/ ; https://mastra.ai/blog/what-are-durable-ai-agents
- 等级：【官方】
- 第二卷用法：第二卷'持久化时机'与'durable execution 降维'章的业界对照。列一张'官方系统 vs 学术产出'对照表（DBOS/AWS/MS/Temporal 全是产品，学术只有预印），直观展示'业界跑在学术前面'。90% 那条只能当'业界宣称'引用并标明是商业博客、无评审支撑。

### harness 已在 2026 上半年结晶为独立领域——由业界博客引领（Part B 元发现）

'agent harness'从术语变成命名领域，集中发生在 2026 H1，且是业界博客先立标杆、学术预印随后井喷。业界一手源：Anthropic 两篇工程文（'Effective harnesses for long-running agents'、'Harness design for long-running application development'）、OpenAI 'Harness engineering: leveraging Codex in an agent-first world'、Thoughtworks/Birgitta Böckeler 在 martinfowler.com 的综合、MongoDB/Faros.ai 等。学术侧同期一簇预印（多数未评审）：六元组综述 2606.20683、T1-T4 2606.10106、Harness-Bench 2605.27922、AHE 2604.25850，外加 HarnessBridge（2606.12882 可学习双向控制器）、HarnessX（2606.14249 可组合自演化 harness foundry）、Self-Harness（2606.09498 自改进 harness）、Meta-Harness（Lee et al. 2026）、Code as Agent Harness（2605.18747）、Harness Engineering as Categorical Architecture（2605.12239）、Stop Comparing LLM Agents Without Disclosing the Harness（2605.23950）、Cambridge Open Engage 'Harness Resilience'。整个领域里唯一稳过评审的仍是 MAST（NeurIPS 2025）。

- 来源：https://rmax.ai/notes/harness-new-model-agent-systems-2026/ ; https://www.mongodb.com/company/blog/technical/agent-harness-why-llm-is-smallest-part-of-your-agent-system ; https://arxiv.org/abs/2606.14249
- 等级：【二手】
- 第二卷用法：可作第二卷引言的'领域正在成形'背书：术语 2026 才收敛、业界博客立标杆、学术在追赶。这既解释了为什么教程此刻有价值（领域新、缺系统性中文梳理），也给出'一手源以官方工程博客为主、预印为辅、评审极少'的引用分级基调。HarnessBridge/HarnessX/Self-Harness 可归入'自改进/自适应 harness'前沿一节。

### MAST 之外的故障分类与评测方法学新工作（Part B）

故障分类/评测方法 2026 H1 有若干可补充 guide 的新工作：AgentAtlas（arXiv:2605.20530 'Beyond Outcome Leaderboards'）提出六门控制决策策略（six-gate control-decision policy）作为统一评分单元、并区分 taxonomy-aware vs blind 方法量化'模型表观能力有多少来自 prompt 监督'、做了 15 benchmark 覆盖审计；安全 benchmark 分类法一致性分析（2605.16282）；StressWeb（2604.16385，web agent 在真实交互变异下的鲁棒性诊断）；Holistic Evaluation and Failure Diagnosis of AI Agents（2605.14865）。产业侧故障清单可当反面对照：Pazi 五模式（cron 失败/工具失败/入站超时/prompt 腐化/执行超时）、Latitude 六模式（部分完成/幻觉完成/动作误用/上下文溢出/推理-行动脱节/无限循环）。这些多为预印或商业博客，评审级仍稀缺。

- 来源：https://arxiv.org/html/2605.20530v1 ; https://arxiv.org/html/2605.16282v1 ; https://arxiv.org/pdf/2604.16385
- 等级：【预印】
- 第二卷用法：第二卷'故障分类与归因'章的补充料。AgentAtlas 的'taxonomy-aware vs blind'（多少能力来自 prompt 监督）可支撑一个论点：评测若不控 harness/prompt 变量，会把 harness 红利误记到模型头上——呼应 Harness-Bench 主题。产业五/六模式清单可当'工程师视角的故障速查表'放附录，与 MAST 的学术分类互补。

### 评测方法学：pass^k 与三源方差分解仍是薄弱环节（Part B 补充）

guide 5.5 引的 arXiv:2603.29231（三源方差分解模型侧/环境侧/harness 侧、pass^k 而非 pass@1、基础设施故障 trial 计零分）代表的评测严谨性议题，在 2026 H1 仍未见被大样本评审工作系统化承接——检索到的相关工作（AgentAtlas 的多轴评估、Holistic Evaluation and Failure Diagnosis 2605.14865）触及但未替代。同时 Harness-Bench 本身用'冻结任务集/沙箱/预算/超时/评估器、只变 harness'的受控设计，正是 pass^k 精神在 harness 维度的落地，可与 2603.29231 互引。整体判断：'验收要 pass^k、故障要三源分流'目前更多是预印/评测圈共识，缺教科书级评审背书——又一个业界实践先于学术定型的点。

- 来源：https://arxiv.org/html/2605.20530v1 ; https://arxiv.org/pdf/2605.14865
- 等级：【预印】
- 第二卷用法：第二卷'评估与归因的陷阱'章：把 pass^k、三源方差、基础设施 trial 计零分讲成'评测纪律'，并诚实标注这些仍是共识而非评审定论。Harness-Bench 的受控实验设计可当'如何正确做 harness A/B'的正面范例。

## 对大纲的建议

1. 第二卷开篇沿用六元组综述 arXiv:2606.20683 的 ℋ=⟨ℐ_obs,𝒞,ℒ,ℐ_act,𝒮,𝒱⟩ 作全书结构主轴（已逐符号核对无误），并用'harness 2026 才结晶为命名领域、业界博客立标杆、学术预印井喷、唯 MAST 过评审'作为引言背书，交代本书的引用分级基调。

2. 设一章'工程质量是独立变量'，主论据用 Harness-Bench 23.8pp（NanoBot 76.2 vs OpenClaw 52.4，8 后端×6 harness）+ MAST 三类占比（41.77/36.94/21.30，Kappa 0.88，NeurIPS 2025 评审级）。补入 Harness-Bench 新细节'越强模型对 harness 越不敏感'，引出'harness 工程对中小/私有化部署价值更高'的推论。

3. 设一章'改进不可叠加'，用 AHE 论文 arXiv:2604.25850 精确数字：单组件合 +11.1pp、组合仅 +7.3pp；预测'修好'fix-precision 33.7%/recall 51.4% vs 预测'弄坏'regression-precision 11.8%/recall 11.1%。同章顺带介绍 AHE/Self-Harness/HarnessBridge/HarnessX 作为'自改进 harness'前沿。

4. 把'运行时状态持久化'单列为招牌空白章：先承认传统 durable execution（WAL/ARIES/saga）有厚实评审基础，再点明 agent 三个新问题（LLM 不可重放、工具副作用对账、压缩边界即 checkpoint 边界）几乎无评审研究，最后用'官方系统 vs 学术产出'对照表（DBOS/AWS Durable Functions/MS Durable Task/Temporal 全是产品，学术只有 Springdrift 等预印）实证'业界跑在学术前面'。措辞从 guide 的'持久化无研究'精修为'agent 专属持久化无评审研究'。

5. '中断语义分层'章明说学术把'中断'窄化为'用户改主意'（InterruptBench 三分类 Addition/Revision/Retraction，仅 user-initiated；IHBench/SentinelBench 同理），而工程最难的'崩溃/抢占/被杀后状态接续'几乎无学术覆盖——第二个'业界领先'空白点。IHBench 的 3.3× 退化数据当长程+中断双压下的能力断崖旁证。

6. '可观测性与沉默失败'章直接用 arXiv:2606.14589 的现场数据（60 天最长静默、67 个空检查空跑数月、70% 靠人工发现、sabotage validation），并与 Howpot 同域案例（macOS+cron+SSD 备份）并列。把 guide 的'单一非评审源'升级为'一簇早期预印（2606.14589/08162/09863）仍缺大样本评审'。

7. 勘误专栏或脚注：第二卷务必修正 guide 对 arXiv:2606.01416 自愈代价的引用——原文是 +4.3pp（常规）/+10.6pp（高压）、成本用调用次数 proxy（自愈 3.25 < 全量重规划 3.63、> retry-only 2.15），guide 原写的'15-25% 成功率/20-40% 延迟'查无实据，方向对但数字须替换。

8. 评测方法章把 pass^k、三源方差分解、基础设施 trial 计零分讲成'评测纪律'，用 Harness-Bench 的受控实验设计当正面范例、AgentAtlas 的 taxonomy-aware vs blind 佐证'不控 harness 变量会把红利误记到模型头上'，并诚实标注这些仍是评测圈共识而非教科书级评审定论。

