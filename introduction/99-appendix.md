---
title: Harness Study · 智能体的工程实践 · 附录
title_en: Harness Study · The Engineering Practice for AI Agents · Appendix
chapter: 99-appendix
status: draft-v0.4
last_updated: 2026-06-02
purpose: 查阅型速查附录 · 不替代正稿讲解 · 8 件速查表 + 引源汇总
---

# 附录 · Harness Study v0.4 速查

> 本附录是查阅型速查工具——8 件速查表 · 不替代正稿讲解。每件配 1-2 句 framing 锚 + 表内 1 行 1 件 · 不展开机制讨论。机制讨论在 §一-§十 正稿。

---

## A · K1-K7 关键判断引源（BRD 起源归档 §2.2）

K1-K7 是 BRD 起源归档（`docs/brd-source/2026-05-11-direction-and-grill-session-01.md §2.2`）锁的 7 件关键判断 · v0.4 多处直接引用 · 集中在这里查。

| ID | 关键判断 | v0.4 引用章节 |
|---|---|---|
| K1 | 主 harness = 元 coding agent · "做 agent 的 agent" | §一 / §二 / §10 |
| K2 | 副 harness 是被生成的不是手写的 | §八 / §10.3 |
| K3 | 传递的不是代码 · 是配置 bundle（Docker / Skill / MCP / OA 平台对比） | §8.1 封装轴 |
| K4 | 教程最终读者包括 AI（非技术用户把教程发给 AI · AI 替他落地） | §一 阅读路标 / §10.3 |
| K5 | 宏观目标 = 推动行业认知 · 真正的北极星 | §一 / §10 章末 |
| K6 | 副 harness 落地形态模块化（独立 agent / 接口 / 后台模块 / UI 对话） | §8.2 拓扑轴 |
| K7 | learn-harness 是独立产品 · 不绑 Agent-Z | §一 / §10 |

---

## B · 一手 source 索引

业界 2026 harness engineering 命名收敛的 4 件一手材料 · 出现频率最高 · 集中查阅。

| 来源 | 日期 | 链接 | 核心命题 |
|---|---|---|---|
| OpenAI · Harness Engineering | 2026-02-13 | [openai.com/index/harness-engineering](https://openai.com/index/harness-engineering/) | Codex agent-first 设计 · CC 端 403 · 本地 source notes 替代 |
| Lopopolo · Extreme Harness Engineering | 2026-02 | [latent.space/p/harness-eng](https://www.latent.space/p/harness-eng) | OpenAI Frontier & Symphony · token billionaire framing |
| Mitchell Hashimoto · My AI Adoption Journey | 2026-02-05 | [mitchellh.com/writing/my-ai-adoption-journey](https://mitchellh.com/writing/my-ai-adoption-journey) | HashiCorp · 非 Stanford NLP Tatsu Hashimoto |
| Trivedy · The Anatomy of an Agent Harness | 2026-03-10 | [blog.langchain.com/the-anatomy-of-an-agent-harness](https://blog.langchain.com/the-anatomy-of-an-agent-harness/) | 11 组件 · "Agent = Model + Harness" 公式 |

---

## C · Evidence Graph 10 边 · 可观测关系本体

§8.4 详写 · 这里短表速查。10 边覆盖 agent 系统跑起来后跨件 + 跨 cell 关系网络。

| 边 | A → B 含义 | 典型场景 |
|---|---|---|
| prompts | A 提供指令给 B | Prompt Assets → Agent Loop |
| calls_tool | A invoked B 作工具 | Agent Loop → Tool Registry |
| produces | A 产生 B 类 artifact | Agent Loop → TrajectoryRecord |
| verifies | A 验证 B 的输出 | Verifier → Agent Loop artifact |
| scores | A 给 B 输出打分 | Outcome Judge → run |
| blocks | A 阻止 B 的 action | Safety → Agent Loop（ToolBlocked）|
| repairs | A 修复 B 的错误 | Contract Repair → schema violation |
| hands_off | A 转移控制权给 B | Main agent → sub-harness |
| supports | A 输出佐证 B 结论 | Multi-source verifier 一致 |
| contradicts | A 反驳 B 结论 | Agent declared vs verifier observed（最有价值诊断信号）|

---

## D · OWASP Top 10 for LLM Applications 2025

§5.9 Safety 主引 · 这里短表 + 链接。**编号已 WebFetch 核**（2026-05-23 · LLM06 / LLM08 / LLM10 准确 · 全表以 [genai.owasp.org/llm-top-10](https://genai.owasp.org/llm-top-10/) PDF 为准）。

| ID | 名称 | v0.4 章节 |
|---|---|---|
| LLM01 | Prompt Injection | §5.9 AP13 |
| LLM02 | Sensitive Information Disclosure | §5.7 PII 脱敏 |
| LLM03 | Supply Chain | （附录 only · 不展开）|
| LLM04 | Data and Model Poisoning | §5.4 AP14 |
| LLM05 | Improper Output Handling | §5.8 verifier |
| LLM06 | Excessive Agency | §5.9 AP15 |
| LLM07 | System Prompt Leakage | §5.5 |
| LLM08 | Vector and Embedding Weaknesses | §5.9 |
| LLM09 | Misinformation | §5.8 verifier |
| LLM10 | Unbounded Consumption | §5.9 AP15 |

---

## E · 件 × 业界产品 / 技术 归位总图

业界 2026 主流产品 / 技术反向归位到 8 件 + 1 件 Safety · 拿到新产品先反向查这表 · 找到主归件后跳到对应正稿章节。"主归件" = 该产品最主要的抽象功能归位 · "涉及其他件" = 跨件影响。

### E.1 业界主流产品 / 技术归位

| 业界名字 | 主归件 | 涉及职能 | 涉及其他件 |
|---|---|---|---|
| **MCP（Model Context Protocol）** | §5.3 Tool | 工具调用协议 · 跨厂商互操作 | §5.4 部分（MCP server 可 expose 检索接口） |
| **OpenAI function calling** | §5.3 Tool | 工具调用协议 · 厂商内 | — |
| **Anthropic tool use** | §5.3 Tool | 工具调用协议 · 厂商内 | — |
| **Anthropic Agent Skills open standard（SKILL.md）** | §5.5 Prompt | 两层加载模式 · metadata + body | §5.3 部分（Skill 可内嵌 tool definition） |
| **CLAUDE.md / .cursorrules / AGENTS.md** | §5.5 Prompt | 项目级 startup load | — |
| **hook（Claude Code / OpenCode / settings.json）** | §5.5 Prompt + §5.9 Safety | 调用时机注入 + safety check | §5.6 partial |
| **system prompt（厂商内置）** | §5.5 Prompt | 启动注入 · 永不裁剪 | — |
| **few-shot examples** | §5.5 Prompt | inline asset · 写 user message | — |
| **LangChain prompt templates / LangSmith** | §5.5 Prompt | 版本化管理平台 · A/B test | — |
| **RAG（Retrieval-Augmented Generation）** | **横切件** | 检索-注入工程模式 · **不是件** | §5.3（retrieval as tool）/ §5.4.2 Memory / §5.4.3 Artifact |
| **GraphRAG / HippoRAG / LightRAG / KG-RAG** | **横切件** | RAG 的图谱 backend 变体 | §5.4.2 / §5.4.3 |
| **vector DB（Pinecone / Chroma / Weaviate / Qdrant）** | §5.4.2 / §5.4.3 backend | 向量检索存储 | RAG backend |
| **知识图谱（Neo4j / Memento）** | §5.4.2 / §5.4.3 backend | 关系检索存储 | RAG backend |
| **Memory framework（Mem0 / Letta / Memori）** | §5.4.2 Memory | lifecycle 治理工程封装 | — |
| **Karpathy LLM Knowledge Base / Markdown wiki** | §5.4.2 + §5.4.3 混合 | Markdown 持久层 | §5.5 partial |
| **Bitemporal KG（Zep / Graphiti）** | §5.4.3 Artifact | 中型工程层级 · 双时间轴 | — |
| **Enterprise Decision Platform（Palantir Foundry Ontology）** | §5.4.3 Artifact | 重型工程层级 · 跨部门决策 | — |
| **Auto Dream / `/dream`** | §5.4.2 Memory | consolidation lifecycle 实现 | — |
| **LangGraph nodes / states** | §5.1 Agent Loop | 控制流编排实现 | — |
| **CrewAI / AutoGen** | §5.1 + multi-agent orchestration | 多 agent 协作框架 | 横跨多件 |
| **OpenAI Assistants API** | §5.1 + §5.3 + §5.4 部分组合 | 厂商集成 framework | 横跨多件 |
| **Codex CLI / Claude Code / Cursor** | §5.1 + §5.3 + §5.5 + §5.7 + §5.9 组合 | coding agent 完整 harness 实例 | 横跨多件 |
| **OpenAPI / GraphQL schema 自动转工具** | §5.3 Tool | 工具暴露技术 | — |
| **Pydantic AI tools** | §5.3 Tool | Python 内嵌工具抽象 | — |
| **Inspect AI / trajectory replay tools** | §5.7 Trajectory | 离线 replay + audit | — |
| **OTel GenAI semconv** | §5.7 Trajectory | trajectory schema 标准 | — |
| **Verifier（rule-based / LLM-as-judge / outcome reward）** | §5.8 Verifier | 三大类实现 | — |
| **PRM（Process Reward Model）** | §5.8 Verifier | 第三层 process supervision | — |
| **Llama Guard / Anthropic constitutional AI** | §5.9 Safety | content filter / approval gate | — |
| **SPIFFE / biscuit / Zanzibar** | §5.9 Safety | capability token 工业方案 | 见附录 F |
| **OWASP Top 10 LLM 2025** | §5.9 Safety | LLM06 + LLM10 系统映射 | 见附录 D |

### E.2 业界 framing 切法对照

业界有多种"harness 由几件构成"的切法 · v0.4 选 8+1 件的理由见 §五章首。这里把主要 framing 一并列出 · 供读者对比：

| framing 来源 | 件数 | 切法 | 跟 v0.4 关系 |
|---|---|---|---|
| **Augment Code 3 层** | 3 | Constraint / Feedback Loops / Quality Gates | 治理目的切法 · 抽象度高 · 适合战略讨论 |
| **Vivek Trivedy 5 项** | 5 | System Prompts / Tools / Bundled Infrastructure / Orchestration / Hooks & Middleware | 工程组件切法 · Bundled Infrastructure 是杂物袋 |
| **MongoDB 6 件** | 6 | context / tool / planning / error recovery / validation / memory | 跟 v0.4 同档颗粒度 · 缺 Safety 独立面 |
| **Firecrawl / DataCamp 9 件** | 9 | model / tool / context / planning / execution / memory / feedback / safety / orchestration | 颗粒度更细 · 件间关系不显 |
| **v0.4 入门版 8+1 件** | 8 + 1 | Agent Loop / Model / Tool / Context-Memory-Artifact / Prompt / Observation / Trajectory / Verifier + Safety | 件数控件认知容量 · runtime 件跟控制面显式分层 |

### E.3 反向查询纪律

- 拿到任何业界新产品 · 反向查 §E.1 的 "业界名字" 列 · 找到主归件后跳到对应正稿章节
- 如果新产品横跨多件 · 它通常是 framework / 集成产品 · 不是 8 件之一——读者要识别它覆盖了 8 件中哪几件 / 漏了哪几件
- 如果新产品是横切模式（像 RAG 那样横切多件的工程模式）· 标"横切件" · 不归任何单一件
- §E.1 表不可能穷尽业界所有产品 · 新出现的产品按"它解决的是哪件抽象功能的哪个职能"反推归位

### E.4 命名映射 · 内部 / 业界分歧修正集中查

| v0.4 用词 | 内部 / 业界另一称 | 修正源 |
|---|---|---|
| `hook.rs` | CLAUDE.md 写 `builtin_hooks.rs` | N4 audit · 以代码为准 |
| fork-join concurrency | `design/20 §T05` 实际写"前台/后台模式 + 结果回流" | Rev1.2 · plan 引入的现代命名 |
| Skills 2025-12-18 open standard | 2025-10-16 初版 | Rev1.2 修正 |
| Mitchell Hashimoto | 非 Stanford NLP Tatsu Hashimoto | Rev1.2 normalize |
| Karpathy Sequoia 2026-04-20 | plan 原写 2026-04-30 | Rev1.2 事件日修正 |
| PCS Sanity Checks 2026 | Rewolinski et al. 含 Bin Yu 非一作 | Rev1.2 标题修正 |
| Mnimi 2025-11-27 | plan 原写 2026-11 | Rev1.2 修正 |
| PRM · Process Reward Model | v0.4-plan 原写 Process Soft Signal | §5.8 升级名 |
| MODA-RL 工作台 | 业界缺这层抽象 · 跟 W&B / Hyperband / AgentRM 不重合 | [[moda-rl-as-harness-workbench-not-harness]] |
| Harness Lab | v0.4-plan v2 原写 Meta Loop | Rev1.1 · 跟 Agent Loop / Inner-Outer Loop framing 对齐 |

---

## F · SPIFFE / biscuit 一句脚注

§5.9 Safety 控制面提到 capability token 工业方案——SPIFFE（[spiffe.io](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/) · Secure Production Identity Framework · 跨 service mesh 身份标准）+ biscuit（offline-verifiable auth tokens · 短期任务级 capability 比 JWT 颗粒度细 · **biscuitsec.org URL 现 HTTP 403 失效 · 命名保留**）。SPIFFE 用在 LLM agent 场景的实战介绍见 [SPIFFE Securing AI Agent Identity (HashiCorp blog)](https://www.hashicorp.com/en/blog/spiffe-securing-the-identity-of-agentic-ai-and-non-human-actors)。内部 capability token 设计跟 Google Zanzibar 同源 framing 详引见 `docs/2026-05-02-enterprise-agent-platform-survey.md § Capability-Based Authorization` 段。两件都不是 LLM 专用 · 是业界通用 capability-based security 实现 · v0.4 仅作 anchor 不展开。

---

## G · 19 常见误区速查表（AP01-AP19）

整本累计 19 常见误区 · 集中速查。**机制 + 数据 + 判定** 三件齐定义在对应章节正稿——这里只列名 + 章节归属 + 一句速记。

| ID | 常见误区 | 章节 | 一句速记 |
|---|---|---|---|
| AP01 | Cache 共谋 | §7.4 | N 次复跑非 i.i.d. · per-run nonce 解 |
| AP02 | Leakage 四类 | §5.8 | 形状泄漏 / 答案明示 / 暗示性问句 / preference leakage |
| AP03 | Reward Hacking 7 模式 | §7.4 | declared_vs_executed gap 前哨 |
| AP04 | Artifact Claim Mismatch | §5.8 | agent declared vs verifier observed 不一致 |
| AP05 | Fixture / Path Classifier Bug | §7.1 | 60% pass rate → 75-87% 反转的数据基础设施 bug |
| AP06 | 假落地机制 | §5.9 | 协议在仓库但生产路径 noop |
| AP07 | Tool Over-Design | §5.3 | 工具粒度过细 LLM 选不准 |
| AP08 | Context Bloat | §5.4 | lost in the middle · context 累积 unbounded |
| AP09 | Multi-Agent Over-Decomposition | §5.1 | Anthropic 15x cost · coding 别上 multi-agent |
| AP10 | Silent Try/Catch | §5.7 / §6 | swallow exception · 错误没产生 event |
| AP11 | Loop Blind Spot | §5.6 | agent 不知道自己在循环 |
| AP12 | Sub-agent Depth Explosion | §5.9 | fork-join 不限深度 / 不限 token |
| AP13 | Hook / Allowlist Bypass | §5.9 | `cargo checkpoint` 被 `cargo check` 放行 |
| AP14 | Memory Pollution | §5.4c | long-term memory 累积污染 |
| AP15 | Excessive Agency / Unbounded Consumption | §5.9 | OWASP LLM06 + LLM10 |
| AP16 | Schema Coupling | §5.5 | prompt schema 跟实际数据强耦合 |
| AP17 | Premature Optimization | §7.1 / §7.4 / §10 | 没基础数据就调优 · "从容取舍" 同名 |
| AP18 | Stage Inflation | §7.2 | 每件机制标 production ready 但工程未落地 |
| AP19 | OTel Naming Drift | §5.7 | 内部 event name 漂移跟 OTel GenAI semconv |

---

## H · arxiv 全表 · 按 prefix 分组

正稿主表在 `citations-manifest.md` · 这里按 arxiv prefix 分组 + 待二次核标注。

**2210.* (2022)**：react-yao-2022 ✓

**2302-2310.* (2023)**：toolformer-2023 ✓ / reflexion-shinn-2023 ✓ / tot-yao-2023 ✓ / plan-solve-wang-2023 ✓ / memgpt-2023 ✓ / voyager-2305 ✓

**2405-2410.* (2024)**：swe-agent-2024 ✓ / pav-2024 ✓ 🔧（Rev1.2 修年份）

**2502-2511.* (2025)**：plan-and-act-2025 ✓ / reflact-2025 ✓ 🔧（EMNLP 2025）/ gigpo-2025 ✓ / preference-leakage-2025 ✓ (arxiv 2502.01534 · ICLR 2026 接收) / mnimi-2025 ✓ 🔧（Rev1.2 修日期）/ agent-prm-2025 ✓ (arxiv 2511.08325) / **stop-overvaluing-mad-2025** ✓（arxiv 2502.08788 · 备引）

**2510-2511.* / 2603-2605.* (2026)**：hal-2026 ✓ 🔴 (arxiv 2510.11977) / reward-hacking-equilibrium-2026 ✓ 🔴 (arxiv 2603.28063) / meta-harness-2026 ✓ (arxiv 2603.28052) / nl-agent-harness-2026 ✓ (arxiv 2603.25723) / claw-eval-2026 ✓ (arxiv 2604.06132) / pcs-2026 ✓ 🔧 (arxiv 2604.11003) / reward-hacking-era-2026 ✓ (arxiv 2604.13602) / llm-gaming-verifiers-2026 ✓ (arxiv 2604.15149) / skill-ra-2026 ✓ (arxiv 2604.24594) / ahe-2026 ✓ (arxiv 2604.25850) / rhb-2026 ✓ (arxiv 2605.02964) / **continual-harness-2026** ✓ ➕ (arxiv 2605.09998) / ahe-runtime-substrate-2026 ✓ (arxiv 2605.13357 · 已核全文 2026-05-30 · Tier2) / tool-prm-bench-2026 ✓ (arxiv 2601.12294) / **code-as-agent-harness-survey-2026** ✓ ➕ (arxiv 2605.18747 · 同期并行综述) / **faulty-memory-2026** ✓ ➕ (arxiv 2605.12978 · consolidation 退化 · 2026-05-28 self-evolution 批) / **fate-2026** ✓ ➕ (arxiv 2605.11882 · 安全对齐 self-evolution) / **skillopt-2026** ✓ ➕ (arxiv 2605.23904 · skill 自进化)

**待二次核 ⌛**：openai-harness-engineering-2026（CC 端 403 · 用 source notes 替代）+ langgraph-docs（粒度过粗 · 待补具体章节）。**ahe-runtime-substrate-2026 已核全文 2026-05-30**（HKBU + 北师大珠海 · Tier2 预印本 · 移出待核）

**已亲核（2026-05-23 verify pass）**：deepseek-v4-tr §3.6.2 ✓（本地 PDF 目录 line 109 + 正文 line 1431-1472）+ owasp-llm-top10-2025 ✓（WebFetch verify · LLM06 / LLM08 / LLM10 编号准确）

**URL 失效**：biscuit-auth ✗（biscuitsec.org HTTP 403 · 命名保留 · 替代源用 spiffe-hashicorp-agent-blog）

---

## I · 中英术语对照表 · 双语版准备

中英双版准备 · 入门版方案 C **分级混杂** —— A 全中文 · B 推荐中译 · C 首次中文括注后续英文 · D 厂商人名全英文。新内容上稿前查这张表 · 跨章统一 · 不要凭直觉随手翻译。

### I.A · 已有公认中文译法 · 全本中文化

| 英文 | 中文 | 业界对照 |
|---|---|---|
| agent | 智能体 | 机器之心 / Anthropic 中文 / 达摩院统一 |
| context | 上下文 | 全行业统一 |
| context engineering | 上下文工程 | Karpathy 2025 起统一 |
| prompt | 提示词 | 机器之心统一 |
| prompt engineering | 提示工程 | 全行业统一 |
| tool | 工具 | 全行业统一 |
| tool call | 工具调用 | OpenAI / Anthropic 中文统一 |
| memory | 记忆 | 机器之心统一 |
| cache | 缓存 | 全行业统一 |
| inference | 推理 | 全行业统一 |
| reward | 奖励 | RL 中文统一 |
| policy | 策略 | RL 中文统一 |
| orchestration | 编排 | 全行业统一 |
| sandbox | 沙箱 | 安全 / 容器界统一 |
| LLM | 大模型 / 大语言模型 | 中文社区"大模型"日常 / LLM 论文 |

### I.B · 推荐中译 + 全本统一

| 英文 | 推荐中文 | 处理 |
|---|---|---|
| observation surface | 观测面 | v0.4 自创术语 · 首次"观测面（observation surface）"+ 后续"观测面" · 全本统一 |
| reasoning vs inference | 同译"推理"易混 · §5.1 章首必区分 | reasoning = 思考过程 / model 内部 chain-of-thought · inference = 一次模型调用 · 首次区分后保留英文 reasoning |
| harness | Harness（驾驭层 · 智能体外层框架）| 宝玉 2026-04 引爆"驾驭工程"比喻 · 多数作者保留英文 · §一首次给意译 + 后续保留 Harness |

### I.C · 中文无统一译法 · 首次括注 + 后续保留英文

| 英文 | 首次出现 | 后续 |
|---|---|---|
| verifier | verifier（验证器） | verifier |
| trajectory | trajectory（轨迹） | trajectory |
| scratchpad | scratchpad（草稿区） | scratchpad |
| artifact | artifact（产物 / 制品） | artifact |
| hook | hook（钩子） | hook |
| Skill | Skill（技能包 · Anthropic 2025-10 推开放标准） | Skill |
| ACI | ACI（agent-computer interface · 智能体-计算机接口） | ACI |
| MCP | MCP（模型上下文协议 · Anthropic 2024-11 推） | MCP |
| RAG | RAG（检索增强生成 · Lewis et al. 2020） | RAG |
| ReAct | ReAct（Reason + Act 范式） | ReAct |
| agent loop | agent loop（智能体主循环） | agent loop |
| tool schema | tool schema | tool schema |
| episode | episode（一局 / 一次任务） | episode |
| rollout | rollout（一次推演） | rollout |
| patch / diff / fork | patch / diff / fork | 不译（git 语境） |

### I.D · 厂商 / 产品 / 人名 · 全保留英文

- **厂商**：Anthropic / OpenAI / Google / DeepSeek / Moonshot / Meta / Microsoft
- **产品**：Claude / GPT / Gemini / Codex / Cursor / Kimi / LangChain / LangGraph
- **人名**：Karpathy / Schulman / 钱学森 / Norbert Wiener / 其他人名
- **通用计算机术语**：API / JSON / SSE / HTTP / REST · 不译

### I.E · 调用纪律

1. 新内容上稿前查 §I 表 · 表外新词跟用户对齐归类后入表
2. 翻译歧义 / 多译并存 · 优先用 §I.A 已有公认译法 · 不在 §I.A 的查 §I.B/C
3. 英文版翻译时**反向查表** · 中文版按 §I 落实 · 跨章不一致优先以 §I 为准
4. 术语表本身可以演化 · 但 v0.4 锁定后不轻易动 · 改动走 Rev1.X 修正源记录

---

## 附录使用纪律

1. **附录是查阅型工具不是阅读型材料** · 按需翻查 · 不必从头读
2. **机制讨论永远在正稿** · 附录只给 anchor + 速记 · 不展开
3. **修正源记录纪律** · 命名 / 日期 / 标题修正都标 Rev1.X 来源 + N4 / 用户拍板 出处
4. **arxiv prefix 分组** · `26YY.NNNNN` 是 arxiv 2026-YY-MM 上传 · 大致按时间排序
5. **待二次核 ⌛ 标记** · 正稿引用前必核 · CC 端 fetch 403 时用本地 source notes 替代

---

附录到此 · 整本 v0.4 explainer 已按章节拆进 `introduction/`：§一-§四（01-04）/ §五总述 + §5.1-§5.11（05-00 至 05-11）/ §六-§十（06-10）/ 配套 Harness Prompt（11-harness-prompt + 12-harness-prompt-lite）/ 本附录（99-appendix）速查。
