# 附录 · Harness Study 速查

> 本附录供查阅时按需翻检，不替代正文讲解。每一节配一两句说明，表内一行一项；机制的讨论在正文第一至十章。

---

## A · 一手资料索引

2026 年 harness engineering 这个名字逐渐通行，下面几份一手材料在书中引用最多，集中列出供查阅。

| 来源 | 日期 | 链接 | 核心命题 |
|---|---|---|---|
| OpenAI · Harness Engineering | 2026-02-13 | [openai.com/index/harness-engineering](https://openai.com/index/harness-engineering/) | Codex 的 agent 优先（agent-first）设计 |
| Mitchell Hashimoto · My AI Adoption Journey | 2026-02-05 | [mitchellh.com/writing/my-ai-adoption-journey](https://mitchellh.com/writing/my-ai-adoption-journey) | HashiCorp 创始人的视角（不是 Stanford NLP 的 Tatsu Hashimoto） |
| Trivedy · The Anatomy of an Agent Harness | 2026-03-10 | [blog.langchain.com/the-anatomy-of-an-agent-harness](https://blog.langchain.com/the-anatomy-of-an-agent-harness/) | 5 项组件；"Agent = Model + Harness"公式 |
| Birgitta Böckeler · Harness Engineering for Coding Agent Users | 2026-04-02 | [martinfowler.com/articles/harness-engineering.html](https://martinfowler.com/articles/harness-engineering.html) | Thoughtworks 咨询视角；借用控制论的前馈与反馈作类比 |

**延伸阅读**

- Lopopolo · Extreme Harness Engineering（latent.space 访谈，2026-02）：[latent.space/p/harness-eng](https://www.latent.space/p/harness-eng)。谈 OpenAI Frontier 与 Symphony，以及"token 亿万富翁"（token billionaire）的说法。

---

## B · Evidence Graph 10 边 · 可观测关系本体

§8.4 详细讲，这里是速查短表。Evidence Graph 是本书用来描述 agent 系统运行后各机制、各单元之间关系的图（"本体"一词是借用，这里指关系的类型清单），共 10 种边。

| 边 | A → B 含义 | 典型场景 |
|---|---|---|
| prompts | A 向 B 提供指令 | Prompt Assets → Agent Loop |
| calls_tool | A 把 B 当作工具调用 | Agent Loop → Tool Registry |
| produces | A 产生 B 类 artifact | Agent Loop → TrajectoryRecord |
| verifies | A 验证 B 的输出 | Verifier → Agent Loop artifact |
| scores | A 给 B 的输出打分 | Outcome Judge → run |
| blocks | A 阻止 B 的动作 | Safety → Agent Loop（权限拒绝，记为 Blocked）|
| repairs | A 修复 B 的错误 | 故障切换 → 主 provider 出错 |
| hands_off | A 把控制权交给 B | 主 agent → 副 harness |
| supports | A 的输出佐证 B 的结论 | 多个来源的 verifier 结论一致 |
| contradicts | A 反驳 B 的结论 | agent 的声称与 verifier 的观测不一致（最有价值的诊断信号）|

---

## C · OWASP Top 10 for LLM Applications 2025

§5.9 Safety 的主要引用，这里给短表和链接。完整内容以 [genai.owasp.org/llm-top-10](https://genai.owasp.org/llm-top-10/) 为准。

| ID | 名称 | 对应章节 |
|---|---|---|
| LLM01 | Prompt Injection | §5.9.4 |
| LLM02 | Sensitive Information Disclosure | §5.7 PII 脱敏 |
| LLM03 | Supply Chain | （仅在附录列出，正文不展开）|
| LLM04 | Data and Model Poisoning | §5.4 AP14 |
| LLM05 | Improper Output Handling | §5.8 verifier |
| LLM06 | Excessive Agency | §5.9 AP15 |
| LLM07 | System Prompt Leakage | §5.5 |
| LLM08 | Vector and Embedding Weaknesses | §5.9 |
| LLM09 | Misinformation | §5.8 verifier |
| LLM10 | Unbounded Consumption | §5.9 AP15 |

---

## D · 机制与业界产品的对应总图

把 2026 年主流的业界产品和技术，对应到本书的 8 个 runtime 机制加 1 个 Safety 控制面。拿到一个新产品，先在这张表里反查，找到它主要对应的机制，再跳到正文相应章节。"主要对应机制"指该产品最主要的功能落在哪个机制上；"涉及其他机制"指它还影响到哪些机制。

### D.1 业界主流产品与技术的对应

| 业界名字 | 主要对应机制 | 涉及职能 | 涉及其他机制 |
|---|---|---|---|
| **MCP（Model Context Protocol）** | §5.3 Tool | 工具调用协议，跨厂商互操作 | §5.4 部分（MCP server 可以暴露检索接口） |
| **OpenAI function calling** | §5.3 Tool | 工具调用协议，厂商内部 | — |
| **Anthropic tool use** | §5.3 Tool | 工具调用协议，厂商内部 | — |
| **Anthropic Agent Skills open standard（SKILL.md）** | §5.5 Prompt | 三层加载：元数据、正文、支持文件按需加载 | §5.3 部分（Skill 可以内嵌工具定义） |
| **CLAUDE.md / .cursorrules / AGENTS.md** | §5.5 Prompt | 项目级、启动时加载 | — |
| **hook（Claude Code / OpenCode / settings.json）** | §5.5 Prompt + §5.9 Safety | 在特定调用时机注入内容，并做安全检查 | §5.6 部分 |
| **system prompt（厂商内置）** | §5.5 Prompt | 启动时注入，从不裁剪 | — |
| **few-shot examples** | §5.5 Prompt | 内联资产，写在 user 消息里 | — |
| **LangChain prompt templates / LangSmith** | §5.5 Prompt | 版本化管理平台，支持 A/B 测试 | — |
| **RAG（Retrieval-Augmented Generation）** | **横切** | 检索加注入的工程模式，**不是单独的机制** | §5.3（检索作为工具）/ §5.4.2 Memory / §5.4.3 Artifact |
| **GraphRAG / HippoRAG / LightRAG / KG-RAG** | **横切** | 以知识图谱为后端的 RAG 变体 | §5.4.2 / §5.4.3 |
| **vector DB（Pinecone / Chroma / Weaviate / Qdrant）** | §5.4.2 / §5.4.3 的后端 | 向量检索存储 | RAG 后端 |
| **知识图谱（Neo4j / Memento）** | §5.4.2 / §5.4.3 的后端 | 关系检索存储 | RAG 后端 |
| **Memory framework（Mem0 / Letta / Memori）** | §5.4.2 Memory | 记忆生命周期治理的工程封装 | — |
| **Karpathy LLM Knowledge Base / Markdown wiki** | §5.4.2 + §5.4.3 混合 | Markdown 持久层 | §5.5 部分 |
| **Bitemporal KG（Zep / Graphiti）** | §5.4.3 Artifact | 中等规模的工程形态，双时间轴 | — |
| **Enterprise Decision Platform（Palantir Foundry Ontology）** | §5.4.3 Artifact | 重型工程形态，跨部门决策 | — |
| **Auto Dream / `/dream`（第三方博客描述，官方文档未见）** | §5.4.2 Memory | 记忆巩固（consolidation）生命周期的一种实现 | — |
| **LangGraph nodes / states** | §5.1 Agent Loop | 控制流编排的实现 | — |
| **CrewAI / AutoGen** | §5.1 + 多智能体编排 | 多 agent 协作框架 | 横跨多个机制 |
| **OpenAI Assistants API** | §5.1 + §5.3 + §5.4 部分组合 | 厂商集成的框架 | 横跨多个机制 |
| **Codex CLI / Claude Code / Cursor** | §5.1 + §5.3 + §5.5 + §5.7 + §5.9 组合 | 编码 agent 的完整 harness 实例 | 横跨多个机制 |
| **OpenAPI / GraphQL schema 自动转工具** | §5.3 Tool | 工具暴露技术 | — |
| **Pydantic AI tools** | §5.3 Tool | Python 内嵌的工具抽象 | — |
| **Inspect AI / trajectory replay tools** | §5.7 Trajectory | 离线回放与审计 | — |
| **OTel GenAI semconv** | §5.7 Trajectory | trajectory 字段命名的标准约定 | — |
| **Verifier（rule-based / LLM-as-judge / outcome reward）** | §5.8 Verifier | 三大类实现 | — |
| **PRM（Process Reward Model）** | §5.8 Verifier | 第三层，过程监督（线上作为关口较少见） | — |
| **Llama Guard / Anthropic Constitutional Classifiers** | §5.9 Safety | 运行时的内容分类器（Constitutional AI 是训练方法，不是运行时过滤器） | — |
| **SPIFFE** | §5.9 Safety | 工作负载身份标准 | 见附录 E |
| **Biscuit** | §5.9 Safety | 可离线衰减（offline attenuation）的授权令牌 | 见附录 E |
| **Zanzibar** | §5.9 Safety | 关系型授权（论文用 ACL 与关系元组，业界常归为 ReBAC） | 见附录 E |
| **OWASP Top 10 LLM 2025** | §5.9 Safety | LLM06 与 LLM10 的系统对应 | 见附录 C |

### D.2 业界对 harness 构成的几种切法

"harness 由哪些部分构成"，业界有多种切法。本书采用 8 个机制加 1 个控制面的理由见第五章开头，这里把主要切法并列，供读者对比。

| 切法来源 | 项数 | 切法 | 与本书的关系 |
|---|---|---|---|
| **Augment Code 3 层** | 3 | Constraint / Feedback Loops / Quality Gates | 按治理目的切，抽象度高，适合战略讨论 |
| **Vivek Trivedy 5 项** | 5 | System Prompts / Tools / Bundled Infrastructure / Orchestration / Hooks & Middleware | 按工程组件切；Bundled Infrastructure 像个杂物袋 |
| **MongoDB 6 项** | 6 | context / tool / planning / error recovery / validation / memory | 颗粒度相近，但没有独立的 Safety 层 |
| **Firecrawl / DataCamp 9 项** | 9 | model / tool / context / planning / execution / memory / feedback / safety / orchestration | 颗粒度更细，各项之间的关系不明显 |
| **本书 8 + 1** | 8 + 1 | Agent Loop / Model / Tool / Context-Memory-Artifact / Prompt / Observation / Trajectory / Verifier + Safety | 每个机制对应代码模块；runtime 机制与控制面显式分层 |

### D.3 反向查询的用法

- 拿到任何一个业界新产品，在 §D.1 的"业界名字"列里反查，找到主要对应的机制后，跳到正文相应章节。
- 如果新产品横跨多个机制，它通常是框架或集成产品，不属于 8 个机制中的某一个。这时要看清它覆盖了 8 个机制中的哪几个、漏了哪几个。
- 如果新产品是横切多个机制的工程模式（像 RAG 那样），标为"横切"，不归入任何单一机制。
- §D.1 不可能穷尽所有产品。新出现的产品，按"它解决的是哪个机制的哪项职能"来反推对应位置。

---

## E · SPIFFE、Biscuit、Zanzibar · 身份、授权令牌与关系型授权

§5.9 Safety 控制面提到的这三个方案常被放在一起讨论，但它们解决的是不同层面的问题，要分开看：

- **SPIFFE**（Secure Production Identity Framework for Everyone，[spiffe.io](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/)）：**工作负载身份**标准，回答"这个服务或 agent 是谁"，常用于服务网格之间的身份认证。用在 LLM agent 场景的实践介绍见 [SPIFFE Securing AI Agent Identity (HashiCorp blog)](https://www.hashicorp.com/en/blog/spiffe-securing-the-identity-of-agentic-ai-and-non-human-actors)。
- **Biscuit**：**可离线衰减的授权令牌**。持有者可以在不联系签发方的情况下，给令牌追加限制、派生出权限更小的令牌，并能离线验证；同时支持能力令牌（capability，持有即有权）与 ACL 两种用法。颗粒度可以细到单个任务，比 JWT 更细。
- **Zanzibar**（Google）：**关系型授权**系统。论文用 ACL 与关系元组（relation tuples）描述权限，业界常把它归为基于关系的访问控制（ReBAC）。

三者都不是 LLM 专用技术，而是通用的身份与授权方案，本书只作参考锚点，不展开。

---

## F · 反模式速查（AP01–AP20）

全书共 20 个反模式（anti-pattern），集中速查。每一项的机制、数据和判断条件在对应章节的正文里定义，这里只列名称、所在章节和一句速记。正文首次出现时写作"名称（APxx，见附录 F）"。

| ID | 反模式 | 章节 | 一句速记 |
|---|---|---|---|
| AP01 | 复跑不独立 | §7.4 | N 次复跑不独立：响应缓存、固定 seed、共享状态；前缀缓存命中不改变输出 |
| AP02 | 四类泄漏（Leakage） | §5.8 | 形状泄漏、答案明示、暗示性问句、偏好泄漏（preference leakage） |
| AP03 | 奖励投机（Reward Hacking） | §7.4 | 六种常见形态见 §7.4；"声称与实际的差距"（declared_vs_executed gap）是预警信号 |
| AP04 | 产物声明不符（Artifact Claim Mismatch） | §5.8 | agent 的声称与 verifier 的观测不一致 |
| AP05 | 测试夹具与路径分类器缺陷（Fixture / Path Classifier Bug） | §7.8 | 数据基础设施的 bug 让通过率结论反转 |
| AP06 | 假落地机制 | §5.9 | 机制在仓库里，生产路径上什么都不做 |
| AP07 | 工具过度设计（Tool Over-Design） | §5.3 | 工具粒度过细，模型选不准 |
| AP08 | 上下文膨胀（Context Bloat） | §5.4 | 中段遗失（lost in the middle），上下文无上限地累积 |
| AP09 | 多 agent 过度拆分（Multi-Agent Over-Decomposition） | §5.1 | 多 agent 系统约耗普通对话 15 倍 token（Anthropic，2025-06）；编码任务可并行部分少，慎用 |
| AP10 | 静默吞异常（Silent Try/Catch） | §6.7 | 异常被吞掉，错误没有产生事件 |
| AP11 | 循环盲区（Loop Blind Spot） | §3 / §7.8 | agent 不知道自己在绕圈 |
| AP12 | 子 agent 深度爆炸（Sub-agent Depth Explosion） | §5.9 | fork-join 不限深度、不限 token |
| AP13 | Hook 与白名单绕过（Hook / Allowlist Bypass） | §5.9 | 放行规则按字符串前缀匹配，`cargo checkpoint` 被 `cargo check` 放过（作者配套项目实例，见第二卷 2.7 节）；修复：按完整词匹配 |
| AP14 | 记忆污染（Memory Pollution） | §5.4.2 | 长期记忆不断累积错误内容 |
| AP15 | 过度代理与无限制消耗（Excessive Agency / Unbounded Consumption） | §5.9 | OWASP LLM06 + LLM10（2025 版） |
| AP16 | Schema 耦合（Schema Coupling） | §5.5 | prompt 里的 schema、测试用例与 verifier 三者硬连在一起，改一处，另两处无声出错 |
| AP17 | 过早优化（Premature Optimization） | §7.8 / §7.4 / §10 | 数据还没收够就下结论调优；以置信区间不跨 0 为准 |
| AP18 | 阶段虚标（Stage Inflation） | §7.8 | 每个机制都标"可上生产"，实际工程没做完 |
| AP19 | OTel 命名漂移（OTel Naming Drift） | §5.7.4 | 内部事件名与 OTel GenAI 语义约定逐渐偏离 |
| AP20 | 对固定测试集过拟合 | §7.4 | 开发集调参、留出集不参与调参只作改动前后的对照；线上失败回流为判例 |

---

## G · 引用文献索引 · 按 arXiv 编号前缀分组

正文脚注引用的文献按 arXiv 编号前缀分组速查，标签与各章脚注一致，完整条目见脚注。编号前缀表示提交年月，与发表年份可能不同（例如 hal-2026 的编号是 2510.11977）。

**22xx.\*（2022）**：react-yao-2022（2210.03629）

**23xx.\*（2023）**：reflexion-shinn-2023（2303.11366） / voyager-2305（2305.16291） / lost-in-middle-2024（2307.03172）

**24xx.\*（2024）**：routellm-2024（2406.18665） / genrm-poll（2408.15240、2404.18796） / pav-2024（2410.08146）

**25xx.\*（2025）**：zep-2025（2501.13956） / preference-leakage（2502.01534） / magellan-alp（2502.07709） / plan-and-act-2025（2503.09572） / mem0-2025（2504.19413） / self-correction-survey-2025（2504.21625） / gigpo-2025（2505.10978） / socratic-prm-bench-2026（2505.23474） / weak-reward-rl（2506.00103、2511.02463） / one-token-fool-2025（2507.08794） / self-evolving-survey-2026（2507.21046） / behavioral-fingerprinting-2025（2509.04504） / composite-rewards-2026（2509.15557） / memgen-2026（2509.24704） / hal-2026（2510.11977） / agent-prm-2025（2511.08325） / agent-evolver-2026（2511.10395） / mnimi-2025（2511.22118） / cdct-2025（2512.17920） / ssr-2026（2512.18552）

**26xx.\*（2026）**：tool-prm-bench（2601.12294） / trajectory-informed-memory-2026（2603.10600） / agent-her-2026（2603.21357） / erl-2026（2603.24639） / meta-harness-2026（2603.28052） / reward-hacking-equilibrium-2026（2603.28063） / claw-eval-2026（2604.06132） / artifacts-as-memory-2026（2604.08756） / dive-cc-2026（2604.14228） / swe-trace-2026（2604.14820） / llm-gaming-verifiers-2026（2604.15149） / taco-2026（2604.19572） / ahe-2026（2604.25850） / rhb-2026（2605.02964） / continual-harness-2026（2605.09998） / fate-2026（2605.11882） / faulty-memory-2026（2605.12978） / code-as-agent-harness-survey-2026（2605.18747） / skillopt-2026（2605.23904）

**脚注未给 arXiv 编号的来源**：gpt3-few-shot-2020 / cot-wei-2022 / self-consistency-wang-2022 / llmcompiler-2024 / swe-bench-verified / anthropic-skills-spec / anthropic-multi-agent-research / dynamic-workflows / anthropic-effective-agents / harness-routing-2026 / era-of-experience / pass-at-k / claude-code-auto-dream / karpathy-autoresearch-2026 / philschmid-pass-k

---

## H · 中英术语对照表

跨章统一用词的参考。本表与三卷共用的 [`术语对照表.md`](../术语对照表.md) 保持一致；后者还列出了借用术语的本书用法与学科标准用法的差别、作者惯用词的替换以及外部事实核查记录，有出入时以它为准。

分级：A 已有公认中文译法（全用中文）；B 推荐中译；C 首次出现时中文括注，之后保留英文；D 厂商、产品、人名全用英文。

### H.A · 已有公认中文译法

| 英文 | 中文 | 说明 |
|---|---|---|
| agent | 智能体 | 正文可保留 agent，需要中文时用"智能体" |
| context | 上下文 | 每一轮由历史算出、实际发给模型的那一份；与"历史"（持久化保存的完整记录）区分 |
| context engineering | 上下文工程 | 2025-06 由 Shopify 的 Tobi Lütke 发帖推广，Karpathy 附议后流行 |
| prompt | 提示词 | — |
| prompt engineering | 提示工程 | — |
| prompt caching / prefix caching | 提示词缓存 / 前缀缓存 | 缓存前缀的计算结果，不缓存输出，不改变采样分布；与响应缓存（response caching）不同 |
| tool | 工具 | — |
| tool call | 工具调用 | — |
| memory | 记忆 | — |
| cache | 缓存 | — |
| inference | 模型调用（推理调用） | 指一次模型调用；为免与 reasoning 混淆，本书不单写"推理" |
| reward | 奖励 | 强化学习术语 |
| policy | 策略 | 本书取访问控制义：决定一个工具调用能否执行、是否需要审批的规则集；不同于强化学习中的策略 π |
| orchestration | 编排 | — |
| sandbox | 沙箱 | 指 OS 级隔离；工具代码内的路径校验称"工具层校验" |
| LLM | 大模型 / 大语言模型 | — |

### H.B · 推荐中译

| 英文 | 推荐中文 |
|---|---|
| harness | 保留英文，不译。首次出现写"harness（包在模型外面、负责上下文、工具、执行、权限与留痕的那一层程序）"；不译作"智能体框架"，以免与 LangChain、LangGraph 这类 agent 开发框架混淆 |
| reasoning | 推理（思考过程），指模型内部的思维链（chain-of-thought）；与 inference（模型调用）区分 |
| turn | 轮：一次模型调用，加上它触发的工具执行 |
| exchange（本书英文版用语） | 回合：从一条用户消息开始、到模型给出最终回复为止，一个回合包含多轮 |
| run | 运行：一次任务从开始到终态（完成、失败、取消）的全过程 |
| session | 会话：同一用户与同一 agent 的一段连续交互，可包含多次 run |
| observation surface | 观测面（本书术语，首次出现时括注 observation surface） |
| behavioral probing | 行为探测（本书也称"把脉"） |
| position bias | 位置偏置：模型对上下文不同位置的信息利用程度不同，lost-in-the-middle 是最有名的表现（§5.4） |
| prefill / time to first token | 预填充 / 首 token 延迟：生成前先处理整段输入的一步 / 从发出请求到收到第一个输出 token 的时间；输入越长两者越大（§5.4） |
| observation pack | 观测包：harness 每轮为模型组装的结构化观测，列出工具结果的摘要、状态、完整内容的引用和估算 token 数（§5.4） |
| valid time / transaction time | 有效时间 / 事务时间：事实在现实中何时为真 / 系统何时知道、何时改动这条记录；两条时间轴合称双时态（bitemporal，§5.4.3） |

### H.C · 首次括注、后续保留英文

| 英文 | 首次出现写法 |
|---|---|
| verifier | verifier（验证器） |
| trajectory | trajectory（轨迹；本书指持久化的执行事件流及其视图） |
| scratchpad | scratchpad（草稿区） |
| artifact | artifact（产物 / 制品） |
| hook | hook（钩子） |
| Skill | Skill（技能包，Anthropic 2025-10 开放标准） |
| ACI | ACI（agent-computer interface，智能体-计算机接口，SWE-agent 提出） |
| MCP | MCP（模型上下文协议，Anthropic 2024-11） |
| RAG | RAG（检索增强生成，Lewis et al. 2020） |
| ReAct | ReAct（Reason + Act 范式） |
| agent loop | agent loop（智能体主循环） |
| episode | episode（一局 / 一次任务） |
| rollout | rollout（一次推演） |
| scaffold | scaffold（支架 / 脚手架；研究文献常用，与 harness 近义） |
| tool schema、patch、diff、fork | 不译（技术语境保留） |

### H.D · 厂商 / 产品 / 人名 · 保留英文

- **厂商**：Anthropic、OpenAI、Google、DeepSeek、Moonshot、Meta、Microsoft
- **产品**：Claude、GPT、Gemini、Codex、Cursor、Kimi、LangChain、LangGraph
- **人名**：Karpathy、Schulman、钱学森、Norbert Wiener 等
- **通用计算机术语**：API、JSON、SSE、HTTP、REST 等不译
