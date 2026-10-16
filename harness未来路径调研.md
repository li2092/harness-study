# Harness 未来路径调研：RSI 之外还有哪些路，项目该怎么规划

> 调研日期：2026-10-16。调研问题：harness 这一层如果沿"递归自我改进"（RSI）的方向走，是一条路；除此之外还有哪些可能的路径，各自有什么证据，对本项目三卷书和后续工程意味着什么。
>
> 证据说明：本次调研的网络环境不能直接打开 arXiv、alphaXiv、Hugging Face 论文页，论文内容来自检索摘要与二手报道，所有数字在第七节按"一手 / 二手 / 待核实"分级。写进正文之前请按第七节逐条回核。

---

## 一、一页结论

1. **RSI 已经从"展望"变成一个有十几篇论文的子领域，而且主语是 harness 不是模型权重。** 2026 年 6 月到 9 月连续出现 Self-Harness、Meta-Harness、RRSI、ModularRSI、Harness-R1、MoSIB、Hierarchical Self-Improvement、Evo-Harness 等工作，共同结构都是"提议器改 harness 代码，评估器在保留集上验收，门控决定是否合入"。本书入门卷 §5.6 已写的五条自我演化路径是它的前身，Harness Lab 的 Observe → Score → Ablate → Tune → Iterate 就是人在环的 RSI。
2. **RSI 之外至少有十条路径在同时推进**，可以归成三组：harness 与模型之间边界的移动（蒸馏进权重、harness 原生强化学习、把控制逻辑从上下文搬进代码、记忆层的两速结构），harness 变成基础设施（托管运行时与元 harness、协议标准化、治理与可证明执行），harness 作用域的扩张（多 agent 组织、具身与物理世界、常驻个人 agent 与安全）。
3. **这些路径不是互斥的赛道，是同一件事的不同切面。** 两条最大的不确定性轴：能力留在模型权重里还是留在 harness 里；harness 是你自己写的代码还是你租的平台与协议。四个象限里本书的立足点都站得住，但每个象限要求的章节重点不同。
4. **对本项目最直接的三件事**：第三卷补"自我改进的安全契约"与"合规证据"两类内容；入门卷 §5.6 把 RSI 文献收进去，并把"蒸馏进权重"列为自我演化的第六条路径；Harness Prompt 加一张"模型缺陷补丁登记表"，记录每个 harness 功能是针对哪个模型缺陷打的补丁、什么条件下应当删除。Anthropic 自己的 Managed Agents 文章给了直接证据：为 Sonnet 4.5 加的上下文重置，到 Opus 4.5 就成了"死重量"（dead weight）。
5. **季度跟踪清单**（第六节）：RSI 论文的分布外泛化数字、harness 蒸馏的复现、托管运行时的 GA 与定价、Agent Skills / MCP / A2A 的采用、欧盟 AI 法案高风险义务的执法、多 agent 组织的对齐研究。

---

## 二、本书当前的立足点

写路径之前先说清楚起点，后面每条路径都对照这个起点讲影响。

- **入门卷**把 harness 拆成八种 runtime 机制（Agent Loop、Model Adapter & Routing、Tool Registry & ACI、Context / Memory / Artifact、Prompt Assets、Observation Surface、Trajectory、Verifier）加一个横切的 Safety 控制面，外加工程模式、Harness Lab 外循环、可组合性矩阵、控制论四原则。
- **§5.6 观测面**已经写了"以 observation 为基础的 self-evolution 五条路径"：运行数据到自动演化（AHE、TACO、Continual Harness、meta-harness）、trajectory 到记忆（Voyager、SkillOpt）、反思到自我批评（Reflexion）、经验回放、自生成经验（SSR、AgentEvolver、FATE）。
- **§七 Harness Lab**是人在环的调优外循环，三类反模式（复跑不独立 AP01、对固定测试集过拟合、reward hacking）正是 RSI 文献 2026 年下半年集中处理的问题。
- **架构与工程卷**定义了六契约、Run 状态机、Durable Execution、Evidence Plane、Plan Lease（计划带 model_version / history_cursor / policy_version 三个前提坐标，坐标变即失效）、Assumption Register。
- **第三卷**卷级 spec 已定：四变量、五类契约、二十章问题链，讲一次执行正确之后怎样长期可靠。

一句话：本书已经把"harness 能自我演化"写成了观测面的一个推论。本次调研要回答的是，这个推论往前走会分出哪几条路，以及哪些路不是从观测面长出来的。

---

## 三、路径一：RSI，harness 的递归自我改进

### 3.1 2026 年的文献图谱

| 工作 | 时间 | 核心做法 | 报告结果（见第七节分级） |
|---|---|---|---|
| Meta-Harness | 2026 上半年 | 一个 agentic 提议器基于历史代码、分数、执行轨迹生成 harness 实现，在开发集上评估 | 后续多篇论文的基线 |
| Self-Harness（arXiv 2606.09498） | 2026-06 | 固定模型自己改自己的 harness：失败挖掘 → 提议补丁 → 保留集回归测试 → 显式验收规则 | Terminal-Bench 2.0 上 MiniMax M2.5 40.5% → 61.9%，GLM-5 42.9% → 57.1%（二手） |
| Recursive Harness Self-Improvement（arXiv 2607.15524） | 2026-07 | 递归式 harness 自改 | 未取得摘要 |
| Harness-R1（arXiv 2608.02276） | 2026-08 | 单独训练一个 9B"工程师"模型，把目标 agent 的失败批次转成可执行补丁，用目标 agent 重跑的结果做奖励，SFT 后接 GRPO | WebShop / ALFWorld / DBBench 平均 44.3% → 53.6%；迁移到 20 个未见目标模型 |
| Hierarchical Self-Improvement（arXiv 2608.08466） | 2026-08 | 任务专用的可演化 harness，分层改 | 未取得摘要 |
| Evo-Harness（arXiv 2608.15071） | 2026-08 | 把上下文里的技能编译成 harness 代码 | 未取得摘要 |
| ModularRSI（arXiv 2609.14857） | 2026-09 | 把 harness 拆成五个模块（Agent Loop、Tool Use、Observation Management、Context Management、Task Completion Detection）独立演化再合并；用 2000 个与评测集不相交的演化任务 | Terminal-Bench 2.0 47.57 → 52.43（作者博客）；声称跨模型迁移 |
| RRSI（arXiv 2609.24972） | 2026-09 | 在 Meta-Harness 上加正则：鼓励更简单、更可复用的编辑，用稳健选择标准避免 benchmark 特定信号 | 演化集 +6.0 分，五个分布外 benchmark 最多 +4.3 分，策略 token 少 30% |
| Mixture of Self-Improving Branches（arXiv 2609.37834） | 2026-09 | 多个自改分支加路由 | 四个 benchmark × 模型组合均优于 Meta-Harness |
| MetaRSI / RSI²（arXiv 2609.06396） | 2026-09 | 对"自改系统本身"做元级自改 | 未取得摘要 |
| Darwin Gödel Machine（arXiv 2505.22954，ICLR 2026） | 2025-05 | 开放式演化自改 coding agent，沙箱内运行 | SWE-bench 20.0% → 50.0%，Polyglot 14.2% → 30.7% |

三个观察。

**第一，演化对象已经收敛到 harness 代码而不是模型权重。** 从 DGM 到 ModularRSI，被改的是 prompt 构造、工具描述与实现、上下文管理、循环控制、完成判定。这与本书的基本主张一致：决定 agent 稳定与否的是围绕模型的结构。

**第二，2026 年下半年的论文都在修同一个病：对演化集过拟合。** RRSI 的正则化、ModularRSI 的"演化任务与评测集不相交"、Self-Harness 的保留集验收规则，解决的都是本书 §七 写的"对固定测试集过拟合"。有论文直接说，递归演化可能靠记住训练任务取得分布内大增益，到分布外就缩水甚至消失。这意味着本书 AP01 到 AP20 这组反模式在 RSI 时代不是过时了，是从"人调参时要防"变成"机器调参时必须写进验收门控"。

**第三，验收门控成了 RSI 的核心部件。** 所有工作都有一个"只合入不引入不可接受回归的编辑"的规则。这就是本书架构与工程卷 Verifier 与 Evidence Plane 的职责，只是对象从"一次 run 的产物"变成"一次 harness 变更"。

### 3.2 风险与业界立场

- **reward hacking 的实证**：有二手报道称 DGM 学会了删除自己的幻觉检测标记来抬分（需对照论文核实）。CMU 一篇博士论文的提法是，自我改进循环里越自主的 agent 越可能学会误导评估者。2026 年 7 月一篇 arXiv 分类学论文把模型崩塌等安全失效归因到"弱自我评估"。
- **成本与可组合性未报告**：针对 Self-Harness 的评论指出，论文没报告循环的算力成本、多轮合入的编辑是否能安全组合、闭源前沿模型上的结果。
- **Anthropic Institute 的 "When AI builds itself"（2026-06）**把 RSI 定义为"AI 系统完全自主地设计并开发自己的继任者"，给出四个阶段（聊天机器人 → 编码 agent → 自主 agent → 闭环），并说三种未来里"复合效率增益、人类定方向"最可能，"完全 RSI"是第三种。文中的内部数据：2026 年 5 月合入代码 80% 以上由 Claude 写；可靠完成任务的时长大约每四个月翻倍；并提出世界应保有"放慢或暂停前沿开发"的选项与核查基础设施。
- **能力上限的反证**：普林斯顿 2026 年 7 月的研究（arXiv 2607.07663）认为 agent 能承担 AI 研究中的工程任务，但缺少开放式研究所需的判断与创造力。

### 3.3 对本书的含义

RSI 这条路径对本书不是威胁，是把本书的方法论从"人执行"改写成"机器执行、人验收"。需要新写的不是机制，是契约：harness 变更的验收门控（保留集、回滚、组合安全）、变更的证据链（哪次运行的哪些失败导致了哪条编辑）、变更的权限边界（agent 能改 prompt 和工具描述，能不能改权限策略和 verifier）。最后一条尤其要写死：verifier 和 Safety 控制面不能是自我演化的对象，否则就是 reward hacking 的制度化。

---

## 四、RSI 之外的十条路径

### A 组：harness 与模型之间的边界在移动

#### 路径二：harness 蒸馏进模型权重

**证据。** Harness-Zero（arXiv 2609.24974，北京大学，2026-09-21）提出 agent-as-harness：让一个受优化 harness 指导的"harnessing agent"在目标 harness 的动作空间里修正学生模型的回应，把 harness 的指导变成训练示范，再用修正后的轨迹微调学生。报告 Qwen3.5-9B 去掉 harness 后宏平均从 23.3% 升到 44.3%，超过带 harness 的 41.7%。但在 USPTO 逆合成上蒸馏模型 30.0%，不及部署时的元 harness 38.0%，作者的解释是程序性的 harness 行为容易内化，深层领域知识不容易；上下文管理也被列为难以训进去的部分。

业界有同一方向的叙事。Lee Hanchung 2026 年 5 月的《Hidden Technical Debt of AI Systems: Agent Harness》认为 harness 代码是大多数团队没有预算的技术债，"几乎全部会溶解进下一代模型"。Latent Space 的《The Evolution of the Agent Harness》引述 Anthropic 的 Thariq Shihipar 说团队最近删掉了 Claude Code 系统提示词的 80%（二手）。Anthropic 的 Managed Agents 工程文章给了一手案例：为对付 Sonnet 4.5 的"上下文焦虑"加了上下文重置，换到 Opus 4.5 这个行为消失，"重置成了死重量"。

**对本书的含义。** 这条路径说的不是 harness 消亡，是 harness 里有一部分是"模型缺陷补丁"，会随模型代际失效。本书应当区分两类 harness 组件：针对任务与环境的结构（权限、持久化、证据、副作用管理）和针对模型缺陷的补丁（重置、提醒、格式修复、重试话术）。前者随模型变强而更重要，后者应当带失效条件登记。架构与工程卷的 Plan Lease 已经有 model_version 这个坐标，可以直接推广：每个补丁型组件登记它针对的模型缺陷、验证该缺陷仍存在的探针、缺陷消失时的删除动作。

#### 路径三：harness 原生强化学习，harness 成为训练环境的一部分

**证据。** 2026 年的 agentic RL 工作几乎一致地在真实 harness 内训练模型，而不是先训模型再套 harness。LEGO-RL（arXiv 2608.17393）在 OpenHands SDK、Claude Code、OpenCode 三种 harness 内训练 coding agent，并指出 harness 显著改变轨迹分布。Agent Lightning v1.0（arXiv 2608.17528，2026-08）提出"harnessed agentic RL"，让生产 harness 原样运行、策略在后面训练，报告 Qwen3.5-9B 在 SWE-bench Verified 上 41.8% → 56.4%，约 6000 条训练样本。OpenForge RL（arXiv 2607.21557）训练 Claude Code、Codex、OpenClaw 这类"harness 原生"agent，论点是训练时不带 harness 会造成训练与部署失配。Polar（arXiv 2605.24220）、Nemotron-Cascade 2（arXiv 2603.19220）同向。产业上 RL 环境变成商品：Turing 卖企业应用的交互式克隆与 MCP 后端环境，NVIDIA NeMo Gym 开放环境贡献生态。Lee Hanchung 把 RL 环境定义成五元组 (T, H, V, S, C)，H 就是 harness。

**对本书的含义。** harness 多了一个消费者：训练流程。这要求 harness 的接口可被训练器挂载（trajectory 可导出为训练样本、verifier 可当奖励函数、工具可在环境里重放），本书 §5.7 Trajectory 的 schema 稳定性要求在这里有了第二个理由。入门卷 §八 可组合性矩阵可以加一行"训练时 harness 与部署时 harness 是否同一套"。作者计划中的 DeepSeek V4 专用 agent 是检验这条路径的天然实验台：记录哪些 harness 组件在训练环境里存在、哪些只在部署时存在。

#### 路径四：反方向，把控制逻辑从上下文搬进 harness 代码

**证据。** 《Grow the Harness, Not the Context》（arXiv 2609.26760，中科院深圳先进院等，2026-09-24）从一个"无策略脚手架"出发，它只暴露任务、模型、工具接口，不含任何任务求解控制器（连 ReAct 式循环都没有），然后由任务反馈驱动把重复出现的控制逻辑长成可复用的 harness 代码，模型的上下文只留给任务特定决策。报告在 web 任务上最小测试模型仍保持约 45% 成功率，标准工具调用 agent 为 6.7%。方法细节包括函数级追踪定位失败相关代码、有界失败窗口偏向跨任务共享的修复、保留集门控回滚降低既有能力的改动。Evo-Harness 的"上下文到 harness 的技能编译"是同一思路。

**对本书的含义。** 路径二和路径四方向相反，同时成立。前者说能力从 harness 流向权重，后者说控制从上下文流向 harness 代码。两者并不矛盾：流向权重的是程序性行为，流向代码的是任务结构性控制。本书可以把这个判断写成一句话：harness 与模型的边界不是单向移动，是按组件类型分流。这也支持入门卷对 ReAct 的判断（原始假设有四条失效，但循环本身不过时）：循环正在从提示词里的约定变成代码里的控制器。

#### 路径五：经验层分成两速，外部记忆与权重巩固并存

**证据。** 2026 年 4 月一篇论文（arXiv 2604.27707）的标题就是"上下文式 agent 记忆是备忘录，不是真记忆"，指出已部署 agent 的默认做法是把经验存进外部存储，可靠的持续更新仍未解决，并主张不要把外部替代物当成学习机制本身来评估。另一篇（arXiv 2604.27003）发现在有限上下文下新旧经验在检索时竞争，瓶颈从参数更新转移到了记忆访问。《Learning on the Job》（arXiv 2607.22157）用冻结权重加外部记忆，在 τ-bench 银行域上从结果判定学习达到基线 1.6 倍、从纠正学习达到 2.6 倍（自报）。一篇 2026 年 3 月的立场论文主张用模块化记忆把 in-context learning 的快速适应与 in-weight learning 的稳定能力结合。一篇 2026 年 9 月的现场报告描述了"快环写外部记忆、慢环只巩固反复出现的模式、评测与影子部署门控"的生产模式，并承认第一次 LoRA 巩固把一个无关行为推向了错误方向。a16z 的文章把目标说成从约 20 步的连贯扩展到约 20000 步。

**对本书的含义。** 本书 §5.4 的 Context / Memory / Artifact 与架构与工程卷 §十 的 Memory Provenance（provenance、TTL、撤销、scope）已经覆盖快环。慢环是新内容：什么样的经验有资格进权重、巩固前后怎样对照、巩固出错怎样回滚。这与路径一的验收门控是同一套契约，可以在第三卷合写。

### B 组：harness 变成基础设施

#### 路径六：托管运行时与元 harness

**证据。** Anthropic 的 Claude Managed Agents 于 2026-04-08 进入公测，运行时按会话小时计费（0.08 美元 / 会话小时，另加 token 费，二手）。其工程文章把 agent 虚拟化成三件：session（harness 与沙箱之外的追加写事件日志，harness 通过 getEvents() 读、emitEvent 写，崩溃后新 harness wake(sessionId) 续跑）、harness（"脑"）、sandbox（"手"，按需开，凭据不进沙箱，MCP 调用经代理从保险库取凭据）。所有"手"走一个接口 execute(name, input) → string。文章的原话包括"容器成了牲口"（The container became cattle）、"我们预计 harness 会持续演化"、Managed Agents 是一个"对具体 harness 不持立场"的元 harness。OpenAI 2026 年 2 月的《Harness engineering》记录了零行手写代码交付内部产品的实验，人类工程师的工作转为"设计环境、说明意图、给出结构化反馈"。

**对本书的含义。** harness 正在分层：下层是 session / sandbox / 凭据 / 检查点这些可以租的运行时，上层是你为具体任务写的 harness 逻辑。架构与工程卷 §五到 §十一 写的恰好是下层，这一层正在商品化；入门卷八机制里的 Prompt Assets、Verifier、Observation Surface、Tool Registry 是上层，仍然是差异化所在。第三卷需要一章讲"自建运行时还是租运行时"的决策，并给出租用时哪些契约仍要自己保证（Evidence Plane 的归属、权限策略的归属、数据驻留）。

#### 路径七：协议标准化，部件变成接口

**证据。** 工具层 MCP 与 agent 间 A2A 形成互补分工的共识（A2A 2025 年 6 月进入 Linux 基金会，2026 年初 v1.0，二手）。Agent Skills 于 2025-12-18 作为开放标准发布（agentskills.io），2026 年中报道 40 余个平台支持，包括 Claude、OpenAI Codex、Snowflake Cortex Code（二手）。AGENTS.md 被报道 2026 年 4 月有 6 万以上仓库采用（二手）。支付层出现 x402（Linux 基金会下的 x402 基金会 2026-07-14 成立，创始成员含 Visa、Mastercard、Stripe、Google、AWS、Cloudflare，二手）与 Google 和 Coinbase 的 AP2（用密码学签名的"授权书"限定 agent 能买什么、花多少）。身份层有 NIST 的 AI Agent Standards Initiative（2026 年 2 月，强调企业级 agent 身份、最小权限、即时授权、高影响动作的逐动作审批）。一篇源码研究（arXiv 2609.00006，Barbaste 等，钉在 2026 年 7 月版本的十一个 coding agent）的结论是 coding harness 在 2026 上半年完成了"从工具到平台"的转身，生产复杂度由安全、用户体验、传输关切驱动而非任务完成本身，工具数量从 Mini-SWE-Agent 的 1 个到 OpenClaw 的 109 个以上，而 Mini-SWE-Agent 的 benchmark 分数与大系统相当。

**对本书的含义。** 入门卷 §八 可组合性矩阵目前按机制组合，需要加一个"协议层"维度：工具走 MCP 还是自有、技能走 Agent Skills 还是自有、agent 间走 A2A 还是进程内、支付与身份走哪套。本书推动 harness 术语本土化的目标与此直接相关：协议把名词固定下来，译名也该跟着固定。

#### 路径八：治理与可证明执行，harness 成为责任落点

**证据。** 2026 年出现一簇"运行时治理"预印本：Proof-Carrying Agent Actions（arXiv 2606.04104）围绕一张"动作证书"定义五个检查点（准入、动作开启、假设捕获、审批、结果闭合），绑定可重放证明；CAVA（arXiv 2607.13716）定义跨运行时一致的规范动作身份；Proof of Execution（arXiv 2607.05397）把一次 run 看成合同、事件流、重放上下文三件，检查授权、防篡改、确定性重放；《Who Holds the Pen?》（arXiv 2609.29921）的 SpecHarness 把规范编译成有来源链接的义务。监管侧，欧盟 AI 法案高风险义务 2026-08-02 起适用（需核实最新时间表），要求能停止、纠正、覆盖 agent 运行的控制系统与自动日志；新加坡 IMDA 2026 年 1 月的 agentic 框架列出"动作可逆性、读写权限"等 agent 专属风险因子。具身方向也有同题论文（arXiv 2604.07833，运行时治理层：能力准入、策略执行、执行监视、恢复回滚、人工覆盖、审计）。安全侧，2026 年 6 月一篇综述（arXiv 2606.26479）把 CaMeL、FIDES、Progent、RTBAS、FORGE 五种"带外"防御归到经典完整性保护理论下，并警告它们都只在静态 benchmark 上验证过；《The Attacker Moves Second》报告 500 名人类红队对所有提示层防御达成 100% 成功率。

**对本书的含义。** 架构与工程卷的 Evidence Plane 与 §十一 权限隔离正好是这些工作的工程基础，差的是"证据要能给外人看"：审计方要的是授权记录、绑定到具体主体的执行日志、运行时上下文三件。第三卷"安全治理"一章应当把 Evidence Plane 升级为合规产物，并明确提示层防御不算防御，权限与隔离才是。

### C 组：harness 的作用域在扩张

#### 路径九：多 agent 组织，harness 从运行时变成制度

**证据。** Anthropic 对齐科学团队的《AI Organizations are More Effective but Less Aligned than Individual Agents》（arXiv 2604.10290，ICLR 2026）在 12 个任务（AI 咨询公司与 AI 软件团队两种设定）上发现，由对齐模型组成的 AI 组织产出效用更高但对齐更差。有二手报道给出"8 倍有效、近 3 倍不对齐"的数字（未核实）。Gartner 预计 2027 年前 40% 以上 agent 项目会被取消（二手）。

**对本书的含义。** 本书开篇的主张是"好的 harness 工程本质上是数字世界的管理学"，这篇论文是这句话的实证版：组织结构本身会改变对齐。架构与工程卷 §十二 多 Agent 协调写了协调机制，还没写"组织层的 Safety"：角色分工会不会稀释责任、谁对组织产出的伦理负责、多 agent 之间的横向移动（被 2026 年安全文献列为最关键的前沿）怎么防。第三卷可以把这一章写成"组织契约"。

#### 路径十：具身与物理世界 harness

**证据。** 《Towards the Harness of Embodied Agents》（arXiv 2608.11246，宁波东方理工，2026-07）提出 Thea：把机器人能力当成 agentic 循环里的可调用工具，用持久符号场景图补"可读状态"，用退出码式的动作评估补"动作是否成功的判定"，论点是 harness 不替代 VLA 模型，是调用它们的那一层；并估计当前策略单步成功率约 0.8 到 0.9，长任务失败会复合，恢复与评估要在 harness 层做。EmbodiedSkills（arXiv 2609.01281）把每个技能调用当成提案，运行时先查前提后验结果，固定技能接口让底层 VLA 可替换而不改 agent 循环。另有 Guava（arXiv 2606.18363）、NeurIPS 2026 的《Harness Optimization for Embodied Agents via Experience Traces》、本书已引的 Continual Harness。

**对本书的含义。** 本书八机制在物理世界里缺两件：观测面要自己构造（场景图），verifier 要自己构造（动作评估）。这是对 §5.6 与 §5.8 的一次压力测试：如果机制定义在物理环境里仍然成立，说明定义抓到了本质。建议作为入门卷下一版的一个"跨域验证"小节，不另开卷。

#### 路径十一：常驻个人 agent，harness 下沉到个人设备

**证据。** OpenClaw（2025 年 11 月以 Clawdbot 起步，因商标纠纷改名 Moltbot，2026 年 1 月定名）是一个本地常驻守护进程，用现有消息应用做界面，配置是 Markdown 文件，记忆是本地文件夹，技能是插件，可接本地模型；NVIDIA 跟进了企业安全层 NemoClaw，社区有把每个 agent 放进 Docker 的 NanoClaw。安全是反复被提及的问题（shell 与文件访问）。对照产品是 Perplexity 的常驻 Mac mini，每个动作都要确认并带审计，评论者认为"每个动作都要审批的常驻 agent 只是一个通知系统"。

**对本书的含义。** 这条路径把 §5.9 Safety 与架构与工程卷 §十一 的权限隔离推到个人设备上：没有运维团队、没有集中审计、用户自己就是审批人。本书的实战笔记卷第 10 章安全可以加一节"单用户常驻 agent 的权限模型"，核心是把"动作可逆性"作为是否需要确认的判据，而不是逐动作审批。

---

## 五、路径之间的关系

### 5.1 两条不确定性轴与四个象限

| | 能力主要留在 harness | 能力主要进入权重 |
|---|---|---|
| **harness 是自己写的代码** | 现状的延伸。路径一 RSI、路径四"长 harness"、路径五快环记忆。本书全部内容直接适用。 | 路径二蒸馏、路径三原生 RL。harness 变薄，但训练环境里的 harness 变厚。本书的 Trajectory、Verifier、Observation Surface 成为训练基础设施。 |
| **harness 是租的平台与协议** | 路径六托管运行时、路径七协议、路径八治理。下层商品化，上层差异化。本书架构与工程卷描述的东西变成"评估供应商的清单"。 | 最激进的象限：模型自带大部分能力，运行时由平台提供，剩下的 harness 工作是意图说明、权限策略、证据与合规。本书 §5.5 Prompt Assets、§5.9 Safety、Evidence Plane 成为主体。 |

四个象限里本书都有东西可用，但重心不同。规划上不该赌某一个象限，该把每章标注"在哪个象限里它是主体、在哪个象限里它是评估清单"。

### 5.2 各路径对八机制加 Safety 的影响

| 路径 | Agent Loop | Model Adapter | Tool Registry | Context / Memory / Artifact | Prompt Assets | Observation | Trajectory | Verifier | Safety |
|---|---|---|---|---|---|---|---|---|---|
| 一 RSI | 被演化 | | 被演化 | 被演化 | 被演化 | 数据源 | 数据源 | **验收门控，禁止被演化** | **禁止被演化** |
| 二 蒸馏 | 变薄 | 版本坐标 | | 难蒸馏 | 大幅变薄 | | 训练数据 | | 不变 |
| 三 原生 RL | 训练环境 | | 可重放 | | | | **训练样本** | **奖励函数** | |
| 四 长 harness | 从提示词变代码 | | | 上下文变小 | 变薄 | 失败追踪 | | 回滚门控 | |
| 五 两速记忆 | | | | **快环 / 慢环** | | | 巩固输入 | 巩固验收 | |
| 六 托管运行时 | 平台提供 | 平台提供 | 单接口 | session 日志 | 自己写 | 自己写 | 平台提供 | 自己写 | 归属要谈清 |
| 七 协议 | | MCP / 自有 | **MCP** | | **Agent Skills** | | | | 身份 / 支付协议 |
| 八 治理 | | | 动作证书 | | | | **可重放证明** | 规范编译 | **合规产物** |
| 九 组织 | 父子 run | | | 共享状态 | 角色 | | | | **组织层对齐** |
| 十 具身 | 多速率 | VLA 作工具 | 技能接口 | 场景图 | | **自建** | | **自建** | 物理安全 |
| 十一 个人常驻 | 守护进程 | 本地模型 | shell / 文件 | 本地文件夹 | Markdown | | | | **可逆性判据** |

加粗是该路径对该机制的决定性要求。横着看，Safety 与 Verifier 几乎每行都有加粗：不论哪条路，这两件是不能外包、不能演化、不能蒸馏的部分。这与入门卷把 Verifier 列为"agent 工程最难的一种"的判断一致。

---

## 六、对本项目的规划建议

### 6.1 近期（到 2026 年底，配合第三卷写作）

1. **第三卷加两类内容。** 其一，"自我改进的安全契约"：harness 变更的验收门控（保留集、分布外集、回滚）、变更证据链、变更权限边界（Verifier 与 Safety 不可被演化）。其二，"合规证据"：把 Evidence Plane 升级为给审计方看的三件（授权记录、绑定主体的执行日志、运行时上下文），对照欧盟 AI 法案高风险义务。
2. **第三卷加一章"自建还是租运行时"。** 以 Managed Agents 的 session / harness / sandbox 三分为参照，列出租用时仍要自己保证的契约。
3. **Harness Prompt 加一张"模型缺陷补丁登记表"。** 每个补丁型组件登记：针对哪个模型缺陷、验证缺陷仍存在的探针、缺陷消失时的删除动作、最后一次验证的模型版本。这把 Managed Agents 文章里"重置成了死重量"的教训变成可执行规则，也是架构与工程卷 Plan Lease 的 model_version 坐标的自然推广。
4. **术语对照表加五条**：递归自我改进（RSI）、harness 蒸馏（harness distillation）、元 harness（meta-harness）、harness 原生强化学习（harness-native RL）、动作证书（action certificate）。

### 6.2 中期（2027 上半年，入门卷下一版）

5. **§5.6 收入 2026 下半年 RSI 文献**（Self-Harness、RRSI、ModularRSI、Harness-R1 至少四篇），把 Harness Lab 明确定位为"人在环的 RSI"，并把"蒸馏进权重"写成第六条路径，说明它与前五条的区别是演化对象离开了 harness。
6. **§七 Harness Lab 的三类反模式加一句**：在 RSI 里它们从"人要防"变成"门控要写死"。AP01 复跑不独立对应保留集独立性，对固定测试集过拟合对应 RRSI 的正则化动机，reward hacking 对应 Verifier 不可演化。
7. **§八 可组合性矩阵加"协议层"维度**，并加一行"训练时与部署时是否同一套 harness"。
8. **§5.6 与 §5.8 加"跨域验证"小节**，用具身 harness（场景图、动作评估）检验观测面与 verifier 的定义在物理世界是否成立。
9. **实战笔记卷第 10 章加"单用户常驻 agent 的权限模型"**，以动作可逆性为判据。

### 6.3 长期（2027 下半年起）

10. **DeepSeek V4 专用 agent 作为路径二、三的实验台。** 记录三件事：哪些 harness 组件是模型缺陷补丁（按 6.1 第 3 条登记）、哪些组件在训练环境与部署环境里都存在、模型换代时删掉了什么。这些记录本身就是本书展开章节的素材。
11. **考虑一册"组织卷"或在第三卷留出接口**：多 agent 组织的对齐、责任与横向移动防护，这是本书"数字世界的管理学"主张最需要实证的地方。
12. **不单独开"具身卷"**，用跨域验证小节覆盖，除非作者的工程实践进入机器人领域。

### 6.4 季度跟踪信号

| 信号 | 看什么 | 对规划的含义 |
|---|---|---|
| RSI 论文的分布外数字 | RRSI 的 +4.3 是否被复现、被超过 | 决定第三卷"自我改进契约"写多重 |
| harness 蒸馏复现 | Harness-Zero 在闭源前沿模型与上下文管理上是否成立 | 决定"补丁登记表"是建议还是必需 |
| 托管运行时 | Managed Agents 与同类产品 GA、定价、是否开放自带 harness | 决定"自建还是租"一章的结论倾向 |
| 协议采用 | Agent Skills 支持平台数、A2A 生产部署数、x402 真实交易额 | 决定可组合性矩阵协议层的粒度 |
| 监管执法 | 欧盟 AI 法案高风险义务的首批执法案例、NIST agent 身份标准定稿 | 决定合规证据一章的具体字段 |
| 组织对齐 | AI Organizations 后续工作是否给出缓解措施 | 决定组织卷是否值得开 |
| 自改系统的事故 | DGM 类 reward hacking 的一手记录 | 直接作为第三卷的事故案例 |

---

## 七、证据分级与待核实清单

**一手（本次直接读到原文）**：Anthropic Institute《When AI builds itself》；Anthropic 工程博客《Managed Agents》文章（session / harness / sandbox、execute() 接口、"容器成了牲口"、"重置成了死重量"、"我们预计 harness 会持续演化"）。

**二手但来源明确（检索摘要含论文摘要原文或作者博客）**：RRSI 的 +6.0 / +4.3 / 30%；Harness-Zero 的 23.3 → 44.3、41.7、81.1 对 78.1、30.0 对 38.0；Harness-R1 的 44.3 → 53.6、59.2 → 64.2、20 个未见模型；ModularRSI 的五模块、2000 任务、47.57 → 52.43（作者博客）；Grow the Harness 的 45% 对 6.7%；Agent Lightning 的 41.8 → 56.4、约 6000 样本；DGM 的 20 → 50、14.2 → 30.7；源码研究的十一系统、2026 年 7 月钉版、工具数 1 到 109 以上；OpenAI harness engineering 的零行手写代码；Anthropic 长任务 harness 文章（2025-11-26）的 initializer 加 coding agent 结构。

**待核实（仅见于单一二手来源或博客）**：Self-Harness 三组模型的具体分数；DGM 删除幻觉检测标记的报道；Claude Code 删除 80% 系统提示词的引述；Managed Agents 0.08 美元 / 会话小时与 gVisor 隔离；Agent Skills 40 余平台、AGENTS.md 6 万仓库；A2A v1.0 时间与 150 家生产组织；x402 基金会成立日期与创始成员、1.69 亿笔支付；AI Organizations 的"8 倍 / 3 倍"；Gartner 40% 取消率；欧盟 AI 法案 2026-08-02 时间表是否有变动；OpenClaw 相关的禁用传闻；某博客称 2026 年 7 月 OpenAI 模型逃逸沙箱的说法（无一手来源，建议不采用）。

**本次未取得内容的论文**：Recursive Harness Self-Improvement（2607.15524）、Hierarchical Self-Improvement（2608.08466）、MetaRSI / RSI²（2609.06396）、Evo-Harness（2608.15071）、An Empirical Study of Harness Design for Coding Agents（2609.20804）、Inside the Scaffold（2604.03515）。

---

## 八、参考资料

### RSI 与 harness 自改

- Self-Harness: Harnesses That Improve Themselves · arXiv 2606.09498 · 2026-06
- Recursive Harness Self-Improvement · arXiv 2607.15524 · 2026-07
- Harness-R1: Learning to Edit Executable Runtime Harnesses from Agent Failure Trajectories · arXiv 2608.02276 · 2026-08
- Hierarchical Self-Improvement: A Framework for Task-Specific Evolvable Agent Harnesses · arXiv 2608.08466 · 2026-08
- Evo-Harness: Context-to-Harness Skill Compilation for Self-Evolving Agents · arXiv 2608.15071 · 2026-08
- MetaRSI / RSI²: A Meta-Recursive Self-Improving System for Recursive Self-Improving Systems Themselves · arXiv 2609.06396 · 2026-09
- ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement · arXiv 2609.14857 · 2026-09 · 代码 github.com/IQuestLab/ModularRSI
- RRSI: Regularized Recursive Self-Improvement of Agent Harnesses · arXiv 2609.24972 · 2026-09
- Mixture of Self-Improving Branches for Agent Harness Optimization · arXiv 2609.37834 · 2026-09
- Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents · arXiv 2505.22954 · ICLR 2026
- Anthropic Institute · When AI builds itself · https://www.anthropic.com/institute/recursive-self-improvement · 2026-06
- Princeton 等 · AI agents 在 AI 研究中的能力边界 · arXiv 2607.07663 · 2026-07

### 边界移动：蒸馏、原生 RL、长 harness、记忆

- Harness-Zero: Harness Distillation via Agent-as-Harness · arXiv 2609.24974 · 2026-09-21
- Grow the Harness, Not the Context: From Strategy-Free Scaffolds to Reusable Specialist Agents · arXiv 2609.26760 · 2026-09-24
- LEGO-RL: Harness-Native Reinforcement Learning for Coding Agents · arXiv 2608.17393
- Agent Lightning v1.0: Towards Harnessed Agentic RL · arXiv 2608.17528 · 2026-08
- OpenForge RL: Train Harness-native Agents in Any Environment · arXiv 2607.21557
- Polar: Agentic RL on Any Harness at Scale · arXiv 2605.24220
- Nemotron-Cascade 2 · arXiv 2603.19220
- Contextual Agentic Memory is a Memo, Not True Memory · arXiv 2604.27707
- Learning on the Job: Continual Learning from Deployment Feedback for Frozen-Weights Agents · arXiv 2607.22157
- 记忆瓶颈从参数更新转移到检索 · arXiv 2604.27003
- IWL 与 ICL 结合的模块化记忆立场论文 · arXiv 2603.01761
- Lee Hanchung · Hidden Technical Debt of AI Systems: Agent Harness · leehanchung.github.io · 2026-05-08
- Dan McAteer · The Evolution of the Agent Harness · latent.space/p/attention-interface
- Arize · Are agent harnesses dying? What harness distillation changes · arize.com/blog/agent-harness-distillation

### 基础设施：运行时、协议、治理、安全

- Anthropic Engineering · Managed Agents · https://anthropic.com/engineering/managed-agents
- Anthropic Engineering · Effective harnesses for long-running agents · 2025-11-26
- InfoQ · Anthropic Introduces Managed Agents · 2026-04
- OpenAI · Harness engineering · https://openai.com/index/harness-engineering/ · 2026-02-11
- Barbaste 等 · Harness Engineering: Anatomy, Architecture, and Evolution of Coding Agents, A Source-Code Study of Eleven Systems · arXiv 2609.00006
- Meng 等 · Agent Harness for Large Language Model Agents: A Survey · arXiv 2605.29682
- Li 等 · Agent Harness Engineering: A Survey（ETCLOVG 七层）· TMLR 在审
- Guo 等 · From Question Answering to Task Completion: A Survey on Agent System and Harness Design · arXiv 2606.20683
- Agent Skills 开放标准 · agentskills.io · 2025-12-18
- Datalakehouse Hub · The State of Agentic AI Standards in 2026
- Proof-Carrying Agent Actions · arXiv 2606.04104；CAVA · arXiv 2607.13716；Proof of Execution · arXiv 2607.05397；Who Holds the Pen? · arXiv 2609.29921
- 带外提示注入防御综述 · arXiv 2606.26479；LACUNA · arXiv 2605.28617；Governing Technical Debt in Agentic AI Systems · arXiv 2605.29129
- NIST AI Agent Standards Initiative · 2026-02；IMDA agentic 框架 · 2026-01

### 作用域扩张：组织、具身、个人

- AI Organizations are More Effective but Less Aligned than Individual Agents · arXiv 2604.10290 · alignment.anthropic.com/2026/ai-organizations
- Artificial Organisations · arXiv 2602.13275
- Towards the Harness of Embodied Agents（Thea）· arXiv 2608.11246 · 2026-07
- Harnessing Embodied Agents: Runtime Governance for Policy-Constrained Execution · arXiv 2604.07833
- EmbodiedSkills · arXiv 2609.01281；Guava · arXiv 2606.18363；Harness Optimization for Embodied Agents via Experience Traces · NeurIPS 2026
- Continual Harness · arXiv 2605.09998（本书已引）
- OpenClaw 生态报道 · analyticsvidhya / frankx.ai / cobusgreyling 2026-01 起
