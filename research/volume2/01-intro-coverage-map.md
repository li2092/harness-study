# 入门卷覆盖面地图（第二卷划界依据）

调研产出 · 2026-07-10 · workflow wf_2e1f15b2-4aa · 盘点路

## 各章覆盖

### README.md

- **已覆盖**：全卷定位与目录：入门卷=导论级 explainer，把 8 件 runtime + Safety 控制面 + 工程模式 + Harness Lab + 可组合性矩阵 + 控制论四原则'全骨架走一遍'，每件给 What/Why/How-to-start 三档 mental model；六问完成判据；三类读者跳读建议；50 张配图索引。
- **深度**：概览（元框架+导读）
- **深度卷承诺**：明确承诺'后续会有逐章/逐模块展开版'——每件 runtime 件/每件工程模式/Harness Lab 五层都会有独立深度卷，覆盖更细工程纪律/业界 case/落地踩坑；§5.1 深讲卷在后续展开卷（规划中）。下一档完成判据=读者能独立设计+独立调优一个 harness。

### 01-why-harness.md

- **已覆盖**：问题定义：LLM 是纯函数 vs 任务是多步有状态有副作用；三个权威定义递进（Willison/Hashimoto/Trivedy）；agent=model+harness 排除式定义；CPU+OS 类比及其两处边界（确定性vs概率性）；verifier(输出闸门)+tool policy(输入闸门)两道 P0 闸门；coding→办公→垂域的产品化光谱（半成品/成品）；Meta-Harness 6倍差+7.7pp 实测锚。
- **深度**：概念+机制 framing（定义层，非工程细节）
- **深度卷承诺**：无显式深度卷承诺

### 02-prehistory.md

- **已覆盖**：2020-2022 模型当函数用时代；prompt engineering 三件套（few-shot/CoT/self-consistency）机制与限制；2022-10 两分水岭（LangChain Chain=DAG非loop / ReAct 论文）；为什么仍是函数用（状态在进程内存/regex解析工具/try-except失败）；关系数据库当Redis类比+不稳定性累积数学锚(0.95^n)。首次定义 trajectory/ablation/replayability。
- **深度**：概念史+机制
- **深度卷承诺**：无

### 03-autogpt.md

- **已覆盖**：AutoGPT 内部架构；五种典型翻车（无限循环/工具级联失败/上下文爆炸/目标漂移/不可复现）逐条对应 harness 对策；'模型不是问题环境支撑才是'根本结论；AutoGPT 未彻底失败（转 AutoGPT Platform 显式编排）；实习生类比完整落到 8 件 runtime + Safety 控制面 9 个工程对象；引出 outer loop。首次定义 schema/verifier/policy。
- **深度**：机制（翻车→对策映射，概念对应）
- **深度卷承诺**：5.1.6 dynamic workflow 前指

### 04-harness-emerges.md

- **已覆盖**：harness 词源（test/eval/training harness）；2023-2025'做但没名字'六个术语；function calling(2023-06)与tool use(2023-11)两锚点；2026 命名收敛四人协奏(Hashimoto/Lopopolo/Trivedy/Böckeler)；跨代视角五代算法约束层；harness 与 MLOps 同辈非父子；Code as Agent Harness 综述并行；LangGraph 演化；framework vs harness 根本区分(DOS vs Linux)；为什么 harness 词胜出(马具隐喻三层)。
- **深度**：概念史深讲
- **深度卷承诺**：无（是概念定型章）

### 05-00-mechanisms-overview.md

- **已覆盖**：为什么收敛到 8 件 runtime + 1 件 Safety cross-cutting 控制面（对比 Augment 3层/Trivedy 5项/arxiv 9件切法）；三工程约束（7±2认知/对应代码模块/控制面显式分层）；Safety 为何是横切不是第9件（control plane vs data plane，OS 内核类比及边界）；流水线8工位+质保监管员类比；★件 vs 实现★ mental model（RAG不是件是横切检索模式、MCP是Tool协议实现、Skill是Prompt Asset组织模式）。
- **深度**：framing（切法论证+件vs实现二分）
- **深度卷承诺**：业界归位放到各章'业界归位卡片'+§99附录§D

### 05-01-agent-loop.md

- **已覆盖**：Agent Loop=思考结构非while循环（OODA/侦探类比）；一次 ReAct 调用具体形态+tool_call/tool_result配对协议不变量；ReAct 八假设退化表（2彻底失效/3部分失效/2有条件/1仍成立）；16→5 条主流进化方向；multi-agent over-decomposition(15x token五成因)+Codex深度cap；四问决策流程；plan-and-execute+ReAct+verifier 三层hybrid；dynamic harness/dynamic workflow（弱reward用workflow/强reward用副harness）；5.1.7 弱reward智能上限/learning by doing/MCTS/主动性=探索策略。P0。
- **深度**：含工程细节+机制深讲（重头戏承重墙）
- **深度卷承诺**：5.1.7 末明确：'入门卷把问题和判别维度立起来就够了；展开卷会把给弱reward域造验证信号的全部已知手段逐件过一遍'；dynamic harness+workflow 标'作者正在实践仍在演进，按当前实践给方向不当定论'

### 05-02-model-adapter.md

- **已覆盖**：各家 API 方言的工程代价；最小 ModelAdapter 接口形状(Completion五字段)；单provider也要Adapter边界（Claude Code四通道实例）；多provider两条路（最小公分母 vs 全特性+capability flag）；token计费归一化；★Routing四决策★(failover/escalation/cost/capability matching)+completion可重试vs工具重试危险边界+circuit breaker；learned router(RouteLLM/GPT-5分流)；thinking多档profile policy；模型'没调工具'三成因（文本标签/tool_choice/长中文prompt带偏）。P0(边界)/P1(多provider+Routing)。
- **深度**：含工程细节
- **深度卷承诺**：5.3 strict schema/ToolPolicy 前指；无独立深度卷显式承诺

### 05-03-tool-registry.md

- **已覆盖**：agent调工具vs人调API根本差别；ACI四原则（命名可推/schema紧致/错误actionable/权限可推）；Tool五字段+CC实际9字段；Registry三件事(schema校验/policy决策/执行审计)；Tool Batch四模式(parallel_read/sequential_write/barrier/background_sidecar)+ObservationPack收口；web_search/web_fetch抬有效智能；strict vs lenient schema+fail-closed normalization+禁热改；policy解耦到独立配置层+PolicyRegistry调用前注入；raw vs sanitized error+tool poisoning/rug-pull+pinning；requires_confirmation+审批缓存；Skill-RA select_for动态子集。P0。
- **深度**：含工程细节深讲
- **深度卷承诺**：业界归位卡片指向§99附录§D；无独立深度卷承诺

### 05-04-context-memory-artifact.md

- **已覆盖**：三层按时间尺度拆(Context单turn/Memory跨turn/Artifact跨run)+OS内存层次类比+Artifacts as Memory论点；Context治理(有效窗口/micro-compact/auto-compact必保留四类元素+压缩回归测试/rolling window/prompt caching 6条约束+cache hit监控/lost-in-the-middle四应对/多模态)；Memory(必要性判定五问/stateless合法场景/4类记忆/写入-检索-TTL-invalidation-consolidation/Auto Dream/memory rot三防御/scratchpad边界/多agent共享/toB六必备五未解/Mem0-Zep-Letta对照)；Artifact(四类场景/三工程层级 Lightweight-BitemporalKG-Palantir Ontology/RAG横切/索引维护/toB八纪律/Build-vs-Buy三阶段/Skill as artifact/verifier ground truth)。P0/P1/P2。
- **深度**：极深，含大量工程细节（全卷最长，容错率最低）
- **深度卷承诺**：bitemporal查询封装/Build-vs-Buy等给到选型建议深度，未显式承诺深度卷但内容已到工程细节；RAG pipeline明说'需要的读者去找专门资料'

### 05-05-prompt-assets.md

- **已覆盖**：指令性内容资产化（版本/回滚/A-B/审计）；五件物理形态(system prompt/CLAUDE.md-AGENTS.md/SKILL.md frontmatter+progressive disclosure/hook mandatory/prompt模板)四维对照；P0-P5六优先级裁剪顺序；写给agent不写给人+不信记忆信推理(调用前注入)；版本化只存hash+family切换在run边界+tested_models模型侧变更触发回归；多语种anchor+per-language tail/多场景prompt family；反injection prompt层(出口剥离reasoning/历史侧tool_call配对)；业务规则堆system prompt误区三判定维度；Schema Coupling误区。P0。
- **深度**：含工程细节
- **深度卷承诺**：业界归位卡片→§99附录§D；无独立深度卷承诺

### 05-06-observation-surface.md

- **已覆盖**：三层定位(self-evolution基础设施层/runtime feedback层/作者本地实例化层)；observation≠logging(读者与时机)；stub/body物理分离+按run结局分级留存；多模态ContentPart五类(Text/Image/FileContent/FileRef/PreprocessError)；observation-trajectory协同+OTel；schema设计StepSnapshot 22字段；过载/失真两误区；self-evolution五路径(AHE/Voyager/Reflexion/Experience Replay/Self-Generated)；作者本地件 MechanismEvent四态/absence-of-event第五信号/decision-point vs execution-point/ObservationPack。
- **深度**：含工程细节+明标作者本地实例化（非业界day-1必备）
- **深度卷承诺**：harness件之上可对接 Harness Lab 工作台'在后面 Harness Lab 章节展开，本节不展开'；作者实例化明标'不作业界标准，读者可选别的形态'

### 05-07-trajectory.md

- **已覆盖**：trajectory≠log两层论点；trajectory 作为回退/存档读档前提（可寻址turn/artifact版本/checkpoint粒度）；event taxonomy 9-15类+公共字段(timestamp/event_id/parent_event_id/run_id DAG)；单JSON(.traj) vs JSONL存储取舍；OTel GenAI semconv(Development状态)+W3C trace context；replayability三基线；三误区(缺失/冗余/不可diff)+稳定字段vs volatile字段+CI回归；PII脱敏；trajectory作self-evolution训练数据+trajectory_schema_version永不break。P0。
- **深度**：含工程细节
- **深度卷承诺**：承载self-evolution的本地件同§5.6；工作台是消费trajectory的进阶选项'不是前提'

### 05-08-verifier.md

- **已覆盖**：防agent自欺骗；三层framing(Hard Gate/RLVR、Outcome Judge/LLM-as-judge、PRM)各自能与不能；Hard Gate判定环境与写权限隔离；Outcome Judge Preference Leakage(same model/inheritance/same family)+跨family judge+rubric工程化+multi-judge+校准集；PRM(AgentPRM/ToolPRMBench/Socratic-PRMBench)；三层组合(串联gate/加权/co-evolving)；Reward Hacking四/七模式+五对策；Leakage四防御(形状/答案明示/暗示问句/Preference)；shared responsibility四层定位verifier到Harness层。P0。
- **深度**：含工程细节
- **深度卷承诺**：章末framing澄清：verifier三层是harness件，'harness件之上还可对接一套meta-工作台…在后面Harness Lab章节展开，不在§5.8'；PRM+self-evolution集成'2026还是研究热点'

### 05-09-safety.md

- **已覆盖**：Safety=cross-cutting控制面非第9件(OS syscall gate同构/blast radius/不能全自动/演进慢)；shared responsibility 4层(Model/Harness/Tools/Environment)+Agent Control Plane；维度一4层权限决策(permission mode/allow-deny-ask/Hooks/sandbox评估顺序)；维度二HITL+Auto-review+workflow-level approval；维度三OWASP LLM Top10 v2025(LLM01注入/06过度自主/08向量/10无界消耗)；维度四物理sandbox(Seatbelt/bubblewrap/K8s)+Trust Profile+Capability Token/SPIFFE/OAuth；代码不LLM原则(hard vs soft gate)；fork-join安全约束；四误区AP06/12/13/15；secrets broker。cross-cutting。
- **深度**：含工程细节
- **深度卷承诺**：Capability Token/agent identity'2026还没完全收敛的标准，生产可暂走OAuth+手工管scope'；fork-join具体实现'在后面工程模式章节展开'

### 05-10-turn-walkthrough.md

- **已覆盖**：一次agent turn Step 0→7微型流程（Prompt Assets装配→Agent Loop→Model Adapter→Tool Registry+Safety四层→Context-Memory-Artifact写入→Observation→Trajectory落盘→Verifier）+Safety横切每步；8件事件驱动非序列；作者构造教学示例非真实trajectory。
- **深度**：教学构造流程（机制协作可视化）
- **深度卷承诺**：点出Context auto-compact/Memory invalidation/Verifier复杂判定在跨turn/跨run才显价值，引出§5.11

### 05-11-end-to-end.md

- **已覆盖**：17 turn 修 logging bug 端到端；跨turn协作(Prompt稳定前缀复用/Agent Loop外化/stub-body/auto-compact在Turn11/HITL在Turn16 git push四层介入/Verifier按turn类型选择性启动)；跨run ablation矩阵7配置(关Verifier/关Context/关Safety/关Trajectory/关Prompt examples/关Agent Loop)；教学构造非实证。
- **深度**：教学构造端到端示例
- **深度卷承诺**：跨run ablation'是Harness Lab章节的主题，本节只点到为止'

### 06-engineering-patterns.md

- **已覆盖**：工程模式=跨件组合pattern(同GoF抽象层)；六件：CacheSafeParams/prefix-stable(cache-safe forking+DeepSeek自动前缀缓存适配+reasoning_content跨轮权衡)、Constrained类型/typestate(phantom type+语言依赖Rust>Go>Python)、JSONL Session(append-only+崩溃一致性+checkpoint/resume)、Isolation Modes三档(InProcess/Worktree/Remote)、三层history(Rollout/Compaction/Initial Context)、fork-join concurrency(provider并发槽自适应)；三误区(假落地/过度抽象/silent try-catch)；业界对照(Codex/OpenCode/Claude Code/OpenHands)；渐进引入顺序。
- **深度**：含工程细节
- **深度卷承诺**：章末明说'不构成完整harness工程，provider选型/runtime选语言/部署架构/observability工具链/CI-CD集成…是项目维度trade-off，本章不展开'；业界2026'正在收敛但还没标准化，未来2-3年可能新增或淘汰pattern'

### 07-harness-lab.md

- **已覆盖**：Outer Loop 元工程；工作台4属性(吞任意harness/自动评测/自动调优/识别消化不了的)+AblationProfile/TrajectoryRecord；harness件层vs工作台层承载关系(非替代)；把脉(探针三段式/四族探针A-D/模型快照锚点)；五层 Observe(analysis.db 5表/HAL)-Score(L2 Reward三层与§5.8 verifier三层区分/component swap)-Ablate(Phase A/B/C+McNemar+Bootstrap CI+Bandit+功效前置+局部正确全局有害例)-Tune(harness config search非RL训权重/Hyperband/Optuna/GiGPO借鉴)-Iterate(4收敛条件/AHE/Meta-Harness/autoresearch/Continual Harness)；Cache共谋+per-run nonce；Reward Hacking 7模式；业界5类工作台对照；5误区。
- **深度**：含工程细节但明标 L4 Tune/L5 Iterate 工程0行、设计骨架
- **深度卷承诺**：★重点承诺★ L4 Tune 与 L5 Iterate '工程实施0行，设计骨架已清楚工程实施还空白，读者当未来工程方向看不是现成工具'；Ablate'工程落地还在早期'；工作台整体'是6-12月渐进搭起来的工程基础设施，不是short-term部署目标'；L1-L2用SQLite analysis.db已落地但schema未展开

### 08-composability.md

- **已覆盖**：跨single-run进入multi-harness composition；乐高+集装箱类比；三轴正交：封装(Skill spec/MCP server/GPTs/OA自定义应用四档)、拓扑(single/local sub-agent/remote/sub-harness四档)、交互边界(in-process/MCP transport/A2A/handoff四档)；Evidence Graph 10边可观测关系本体(prompts/calls_tool/produces/verifies/scores/blocks/repairs/hands_off/supports/contradicts)；副harness cell 5维度本体(领域实体/属性/关系规则/状态机/操作集)+IntentRouter反例；三误区(万能prompt/拓扑选过头/协议选过早)；5阶段渐进。
- **深度**：含工程细节，作者提出概念（副harness/5维度本体/Evidence Graph 为本教程提出非业界统一术语）
- **深度卷承诺**：业界2026'还在乐高早期，跨厂商stud标准未收敛，fragmentation是预期不是bug'；A2A'当前别commit，等spec稳定再migrate'；可组合架构'3-6月渐进搭，长期建设方向不是short-term部署目标'

### 09-cybernetics.md

- **已覆盖**：控制论四原则(可观测/可控/稳定/闭环反馈)作为整卷元规则收束；四原则↔全卷件映射；四原则↔常见误区映射(AP01-18归位)；declared_vs_executed gap前哨指标(≥10%告警/可用Evidence Graph边计算)；钱学森1954工程控制论(未知特性系统/non-interacting controls/perturbation theory/von Neumann错误控制)；钱学森1990综合集成法/HWMSE/五件'光定量评判不了'场景；温控空调+汽车四大件类比及边界；Böckeler feedforward+feedback+iterate control flow vocabulary；Code as Agent Harness 6挑战归位四原则。
- **深度**：元规则 framing 收束（方法论层，非新机制）
- **深度卷承诺**：无（是方法论根收束章）；把业界6件open challenges定位为'四原则某一档的frontier缺口'

### 10-learning-path.md

- **已覆盖**：三类读者路径(想入行学生-建mental model+跑通开源harness+写最小single-agent；AI PM-vibe选型升到工程纪律+control panel dashboard+要求L0-L5 maturity grading；给AI看-教程作context+AI给设计工程师implement)；三类共同误区AP17 premature optimization统一判定线(8件runtime≥6件稳定才上后面章节)；AP17=从容取舍同一件事两名；agent harness=钱学森方法论在AI工程延续。
- **深度**：导读（读者路径，非工程内容）
- **深度卷承诺**：提及配套《Agent Harness 落地 Spec·给agent可执行版》(11-harness-prompt.md)作执行清单与正文分工；下一档(2027+)一定有新件但四原则不变

## 可直接沿用的术语（第二卷回指不重讲）

- harness / agent = model + harness（Trivedy 排除式定义）
- framework vs harness（permissive vs prescriptive，DOS vs Linux）
- harness engineering（Hashimoto 28字定义）+ 与 MLOps 同辈非父子
- 8 件 runtime + 1 件 Safety cross-cutting 控制面（8+1 切法）
- 件 vs 实现二分（RAG=横切检索模式非件、MCP=Tool协议实现、Skill=Prompt Asset组织模式）
- run 与 turn（一 run 含多 turn；跨 turn / 跨 run 区分）
- Agent Loop / Inner Loop / Outer Loop
- ReAct 家族（vanilla ReAct / Plan-Execute / Reflexion / Skill-Based Hierarchical）+ ReAct 八假设退化
- thought-action-observation 三元组 + tool_call/tool_result 配对协议不变量
- multi-agent over-decomposition（15x token）+ orchestration
- dynamic harness / dynamic workflow / 弱reward-workflow 强reward-副harness 判别
- Model Adapter 边界 / Routing 四决策(failover/escalation/cost/capability matching) / capability flag / circuit breaker
- Tool Registry / ACI / ToolPolicy / Tool Batch 四模式 / ObservationPack
- strict vs lenient schema / fail-closed normalization / requires_confirmation / Skill-RA select_for
- Context / Memory / Artifact 三层时间尺度
- micro-compact / auto-compact / rolling window / prompt caching / lost-in-the-middle
- stateless 必要性判定五问 / memory rot / consolidation(Auto Dream) / scratchpad
- Artifact 三工程层级(Lightweight / Bitemporal KG / Enterprise Decision Platform) / bitemporal(valid time+system time)
- Prompt Assets 五形态(system prompt/CLAUDE.md/SKILL.md/hook/模板) / P0-P5 优先级 / progressive disclosure
- 调用前注入(PolicyRegistry/hook) / 不信记忆信推理 / prompt family
- Observation Surface / stub-body 物理分离 / ContentPart / MechanismEvent 四态 / absence-of-event / decision-point vs execution-point
- self-evolution / observability-driven evolution / skill library / verbal reinforcement
- Trajectory / event taxonomy / event_id-parent_event_id DAG / JSONL vs 单JSON(.traj) / replayability
- OTel GenAI semconv / W3C trace context / trajectory_schema_version
- Verifier 三层(Hard Gate/RLVR、Outcome Judge/LLM-as-judge、PRM)
- Reward Hacking(七模式) / Leakage 四防御 / Preference Leakage / verifier 校准集
- Safety 控制面 = cross-cutting(OS syscall gate 同构) / shared responsibility 4层(Model/Harness/Tools/Environment)
- 4层权限决策(permission mode/allow-deny-ask/Hooks/sandbox) / HITL / Auto-review / workflow-level approval
- OWASP LLM Top10 v2025(LLM01注入/06过度自主/08向量/10无界消耗) / sandbox(Seatbelt/bubblewrap/K8s) / Trust Profile / Capability Token / secrets broker
- 代码不 LLM 原则(hard gate vs soft gate)
- 工程模式(engineering pattern) 六件：CacheSafeParams/prefix-stable、typestate/Constrained、JSONL Session、Isolation Modes(InProcess/Worktree/Remote)、三层history(Rollout/Compaction/Initial Context)、fork-join
- cache-safe forking / provider 并发槽自适应 / checkpoint-resume
- Harness Lab / 工作台 4 属性 / Observe-Score-Ablate-Tune-Iterate 五层
- 把脉(Model Probe)/探针三段式/四族探针 / AblationProfile / TrajectoryRecord
- Cache 共谋 / per-run nonce / Phase A-B-C 消融 / McNemar / Bootstrap CI
- 可组合性三轴(封装/拓扑/交互边界) / 副 harness cell / 5 维度本体 / Evidence Graph 10 边
- MCP / A2A / handoff pattern / sub-agent vs sub-harness
- 控制论四原则(可观测/可控/稳定/闭环反馈) / 钱学森工程控制论 / feedforward-feedback-iterate
- declared_vs_executed gap 前哨指标 / 假落地(AP06) / premature optimization(AP17) / stage inflation(AP18)

## 划界建议

1. 先建立最重要的认知：入门卷不是浅层概览卷——05-* 系列、06、07、08 大量章节已经写到'含工程细节'深度（接口形状、字段清单、判定线、误区对策、业界实现对照、起步建议四维度）。第二卷《harness 架构与工程化》若按'机制是什么/为什么这样设计'重讲会大面积冗余。第二卷的差异化定位应是'这些件怎么拼成一个系统/模块边界怎么切/代码级架构怎么落地'，即从'分件讲解'升到'架构组合与工程化实现'。

2. 可直接沿用、只需回指引用不必重讲的术语（入门卷都有专门术语 box 定义）：run/turn、agent=model+harness、framework vs harness、8+1 件命名、件vs实现二分、ReAct 家族、ACI、Context/Memory/Artifact 三层时间尺度、stub/body、trajectory/replayability/event taxonomy、verifier 三层名词、Safety cross-cutting、工程模式六件命名、控制论四原则、feedforward-feedback-iterate。第二卷首次出现时用'见入门卷 §X'一句带过即可。

3. 入门卷只讲了概览、第二卷应升级重讲的机制（这些是入门卷明确留白或点到为止的）：(1) Harness Lab 的 L4 Tune 与 L5 Iterate——入门卷反复诚实标注'工程实施 0 行、只是设计骨架'，第二卷若做工程化就必须升级为完整实现（agent harness 专用 HPO 处理 Cache 共谋/mixed 搜索空间/variable cost；autonomous evolution loop 落地）；(2) 05-01 §5.1.7 弱 reward 造验证信号——入门卷明确 promise'展开卷逐件过'，属第二卷/深度卷纯新增；(3) dynamic harness + dynamic workflow（05-01 §5.1.6）——入门卷标'作者正在实践仍在演进'，第二卷可升级为架构级讲解；(4) 副 harness 5 维度本体 + Evidence Graph 10 边（08）——入门卷提出概念给了 PPT/数据治理例子，第二卷若以架构为主轴需升级为完整本体设计方法论+状态机实现+routing/handoff 具体机制。

4. 纯新增（入门卷完全没有、第二卷新写）：(1) 具体架构分层图/模块边界/目录结构/接口契约的代码级设计——入门卷是概念+机制，几乎没有系统架构图；(2) 项目维度工程取舍——06 章末明说'provider 选型/runtime 选语言/部署架构/observability 工具链/CI-CD 集成是项目 trade-off，本章不展开'，这些是第二卷主场；(3) 作者本地工作台（Harness Lab）L1-L2 的 SQLite analysis.db 5 表 schema——入门卷提到但未展开；(4) 副 harness 的 handoff/routing 编排器实现与 dynamic harness 调度器。

5. 严格继承入门卷的'作者本地实例化 vs 业界共识'标注纪律。入门卷非常克制地把这些标为'作者实践案例、非业界 day-1 必备'：ObservationPack、MechanismEvent 四态、StepSnapshot 22 字段、absence-of-event、Harness Lab 五层工作台、副 harness cell、5 维度本体、Evidence Graph 10 边、AblationProfile、把脉/探针三段式。第二卷若把这些作为架构主干展开，必须延续同样标注——说清哪些是业界 SOTA 共识、哪些是本教程作者体系，不能让读者误以为是业界标准。

6. 入门卷每个 05-*/06/07/08 章都有'起步建议·四维度（注意什么/怎么设计/怎么测试/写什么 prompt）'。第二卷不要重复这套起步建议，但可以把其中'怎么设计'一维升级到架构级（模块划分、依赖方向、扩展点），把'怎么测试'升级到系统级回归/集成测试与 harness 自身 CI。

7. 注意入门卷已把'为什么这样设计'的论证做透（每件都有替代方案对比+业界 citation+误区判定线）。第二卷讲架构时可直接站在这些结论上，用'如入门卷 §X 论证'承接，把篇幅让给'如何实现'而非'为何如此'。特别是 verifier 三层、Cache 共谋、Reward Hacking、Preference Leakage、Safety 4 层权限、OWASP 映射这些已被入门卷讲到工程细节，第二卷只需在架构上标明它们各自落在哪个模块/哪条数据流上。

8. 配套件的分工可直接复用：入门卷已有 11-harness-prompt.md（给 agent 的可执行落地 Spec，Phase 0-3+每步 gate）、12-harness-prompt-lite.md（TDD lite）、99-appendix.md（8件速查表+件×业界产品归位总图§D+一手引源汇总）。第二卷讲落地执行时应回指这份 Spec 而非重写；讲件到产品的映射时回指附录 §D；引用一手源时复用附录汇总，保持全集单一引源真相。

