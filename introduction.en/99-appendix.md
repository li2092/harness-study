# Appendix · Harness Study quick reference

> This appendix is a lookup tool, for browsing as needed; it does not replace the main text's exposition. Each item gets one or two anchor lines plus one row per item in the tables; the mechanism discussions are in the main text, §I–§X.

---

## A · Primary source index

The four primary materials behind the industry's 2026 convergence on harness-engineering naming, the most frequently cited, gathered here for quick reference.

| Source | Date | Link | Core thesis |
|---|---|---|---|
| OpenAI · Harness Engineering | 2026-02-13 | [openai.com/index/harness-engineering](https://openai.com/index/harness-engineering/) | Codex's agent-first design |
| Lopopolo · Extreme Harness Engineering | 2026-02 | [latent.space/p/harness-eng](https://www.latent.space/p/harness-eng) | OpenAI Frontier & Symphony · the token-billionaire framing |
| Mitchell Hashimoto · My AI Adoption Journey | 2026-02-05 | [mitchellh.com/writing/my-ai-adoption-journey](https://mitchellh.com/writing/my-ai-adoption-journey) | the HashiCorp founder's perspective (not Stanford NLP's Tatsu Hashimoto) |
| Trivedy · The Anatomy of an Agent Harness | 2026-03-10 | [blog.langchain.com/the-anatomy-of-an-agent-harness](https://blog.langchain.com/the-anatomy-of-an-agent-harness/) | 5 components · the "Agent = Model + Harness" formula |

---

## B · The Evidence Graph ten edges · an observable-relation ontology

§8.4 covers it in full; here is a short lookup table. The ten edges cover the cross-part, cross-cell relational network of a running agent system.

| Edge | A → B meaning | Typical case |
|---|---|---|
| prompts | A supplies instructions to B | Prompt Assets → Agent Loop |
| calls_tool | A invokes B as a tool | Agent Loop → Tool Registry |
| produces | A produces a B-class artifact | Agent Loop → TrajectoryRecord |
| verifies | A verifies B's output | Verifier → Agent Loop artifact |
| scores | A scores B's output | Outcome Judge → run |
| blocks | A stops B's action | Safety → Agent Loop (ToolBlocked) |
| repairs | A fixes B's error | Contract Repair → schema violation |
| hands_off | A transfers control to B | Main agent → sub-harness |
| supports | A's output corroborates B's conclusion | multi-source verifier agreement |
| contradicts | A refutes B's conclusion | Agent declared vs verifier observed (the most valuable diagnostic signal) |

---

## C · OWASP Top 10 for LLM Applications 2025

§5.9 Safety is the primary reference; here is a short table plus a link. The full table is authoritative at [genai.owasp.org/llm-top-10](https://genai.owasp.org/llm-top-10/).

| ID | Name | Chapter |
|---|---|---|
| LLM01 | Prompt Injection | §5.9.4 |
| LLM02 | Sensitive Information Disclosure | §5.7 PII redaction |
| LLM03 | Supply Chain | (appendix only · not expanded) |
| LLM04 | Data and Model Poisoning | §5.4 AP14 |
| LLM05 | Improper Output Handling | §5.8 verifier |
| LLM06 | Excessive Agency | §5.9 AP15 |
| LLM07 | System Prompt Leakage | §5.5 |
| LLM08 | Vector and Embedding Weaknesses | §5.9 |
| LLM09 | Misinformation | §5.8 verifier |
| LLM10 | Unbounded Consumption | §5.9 AP15 |

---

## D · Part × industry product / technology placement map

The mainstream 2026 products and technologies, placed back onto the 8 parts + the 1 Safety control plane. With a new product in hand, look it up in this table first, find its primary part, then jump to the corresponding main-text chapter. "Primary part" = where the product's main abstraction function belongs; "other parts involved" = its cross-part influence.

### D.1 Placing the mainstream products / technologies

| Industry name | Primary part | Function | Other parts involved |
|---|---|---|---|
| **MCP (Model Context Protocol)** | §5.3 Tool | tool-call protocol · cross-vendor interoperability | §5.4 partial (an MCP server can expose a retrieval interface) |
| **OpenAI function calling** | §5.3 Tool | tool-call protocol · within-vendor | — |
| **Anthropic tool use** | §5.3 Tool | tool-call protocol · within-vendor | — |
| **Anthropic Agent Skills open standard (SKILL.md)** | §5.5 Prompt | three-layer loading · metadata + body + supporting files on demand | §5.3 partial (a Skill can embed a tool definition) |
| **CLAUDE.md / .cursorrules / AGENTS.md** | §5.5 Prompt | project-level startup load | — |
| **hook (Claude Code / OpenCode / settings.json)** | §5.5 Prompt + §5.9 Safety | call-time injection + safety check | §5.6 partial |
| **system prompt (vendor built-in)** | §5.5 Prompt | startup injection · never trimmed | — |
| **few-shot examples** | §5.5 Prompt | inline asset · written into the user message | — |
| **LangChain prompt templates / LangSmith** | §5.5 Prompt | versioned management platform · A/B testing | — |
| **RAG (Retrieval-Augmented Generation)** | **cross-cutting** | a retrieve-and-inject engineering pattern · **not a part** | §5.3 (retrieval as tool) / §5.4.2 Memory / §5.4.3 Artifact |
| **GraphRAG / HippoRAG / LightRAG / KG-RAG** | **cross-cutting** | graph-backend variants of RAG | §5.4.2 / §5.4.3 |
| **vector DB (Pinecone / Chroma / Weaviate / Qdrant)** | §5.4.2 / §5.4.3 backend | vector retrieval storage | RAG backend |
| **knowledge graph (Neo4j / Memento)** | §5.4.2 / §5.4.3 backend | relational retrieval storage | RAG backend |
| **Memory framework (Mem0 / Letta / Memori)** | §5.4.2 Memory | lifecycle-governance engineering wrapper | — |
| **Karpathy LLM Knowledge Base / Markdown wiki** | §5.4.2 + §5.4.3 hybrid | a Markdown persistence layer | §5.5 partial |
| **Bitemporal KG (Zep / Graphiti)** | §5.4.3 Artifact | mid-size engineering tier · dual time axes | — |
| **Enterprise Decision Platform (Palantir Foundry Ontology)** | §5.4.3 Artifact | heavy engineering tier · cross-department decisions | — |
| **Auto Dream / `/dream`** | §5.4.2 Memory | a consolidation-lifecycle implementation | — |
| **LangGraph nodes / states** | §5.1 Agent Loop | a control-flow orchestration implementation | — |
| **CrewAI / AutoGen** | §5.1 + multi-agent orchestration | multi-agent collaboration framework | spans several parts |
| **OpenAI Assistants API** | §5.1 + §5.3 + §5.4 partial combination | a vendor integration framework | spans several parts |
| **Codex CLI / Claude Code / Cursor** | §5.1 + §5.3 + §5.5 + §5.7 + §5.9 combination | a complete coding-agent harness instance | spans several parts |
| **OpenAPI / GraphQL schema auto-to-tool** | §5.3 Tool | a tool-exposure technique | — |
| **Pydantic AI tools** | §5.3 Tool | a Python embedded-tool abstraction | — |
| **Inspect AI / trajectory replay tools** | §5.7 Trajectory | offline replay + audit | — |
| **OTel GenAI semconv** | §5.7 Trajectory | a trajectory-schema standard | — |
| **Verifier (rule-based / LLM-as-judge / outcome reward)** | §5.8 Verifier | the three implementation classes | — |
| **PRM (Process Reward Model)** | §5.8 Verifier | the third layer, process supervision | — |
| **Llama Guard / Anthropic constitutional AI** | §5.9 Safety | content filter / approval gate | — |
| **SPIFFE / biscuit / Zanzibar** | §5.9 Safety | industrial capability-token solutions | see appendix E |
| **OWASP Top 10 LLM 2025** | §5.9 Safety | the LLM06 + LLM10 systematic mapping | see appendix C |

### D.2 A comparison of industry framings

The industry has several ways of cutting "how many parts a harness is made of." The reasoning for this volume's 8+1 is at the head of §V; the main framings are gathered here for comparison.

| Framing source | Count | The cut | Relation to this volume |
|---|---|---|---|
| **Augment Code, 3 layers** | 3 | Constraint / Feedback Loops / Quality Gates | a governance-purpose cut · high abstraction · suits strategy discussion |
| **Vivek Trivedy, 5 components** | 5 | System Prompts / Tools / Bundled Infrastructure / Orchestration / Hooks & Middleware | an engineering-component cut · Bundled Infrastructure is a catch-all bag |
| **MongoDB, 6 parts** | 6 | context / tool / planning / error recovery / validation / memory | the same granularity tier · lacks an independent Safety face |
| **Firecrawl / DataCamp, 9 parts** | 9 | model / tool / context / planning / execution / memory / feedback / safety / orchestration | finer granularity · the inter-part relations are not visible |
| **This volume, 8+1** | 8 + 1 | Agent Loop / Model / Tool / Context-Memory-Artifact / Prompt / Observation / Trajectory / Verifier + Safety | part count controlled to cognitive capacity · runtime parts and the control plane explicitly layered |

### D.3 How to use the reverse lookup

- With any new industry product in hand, look it up in the "industry name" column of §D.1, find its primary part, then jump to the corresponding main-text chapter.
- If a new product spans several parts, it is usually a framework or integration product, not one of the 8 parts — identify which of the 8 it covers and which it omits.
- If a new product is a cross-cutting pattern (an engineering pattern that cuts across several parts, like RAG), mark it "cross-cutting" and place it under no single part.
- §D.1 cannot exhaust every industry product; for one that appears later, place it by working backward from "which function of which part's abstraction does it solve."

---

## E · SPIFFE / biscuit · industrial capability-token solutions

The capability-token solutions mentioned by the §5.9 Safety control plane — SPIFFE ([spiffe.io](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/) · Secure Production Identity Framework · a cross-service-mesh identity standard) + biscuit (offline-verifiable auth tokens · task-level capabilities at a finer grain than JWT). A practical introduction to using SPIFFE in the LLM-agent setting is in [SPIFFE Securing AI Agent Identity (HashiCorp blog)](https://www.hashicorp.com/en/blog/spiffe-securing-the-identity-of-agentic-ai-and-non-human-actors), and the capability-token design shares its lineage with Google Zanzibar. Neither is LLM-specific; both are general industry implementations of capability-based security, used here only as an anchor, not expanded.

---

## F · Common-pitfall quick reference (AP01–AP19)

The 19 common pitfalls accumulated across the whole volume, gathered for quick lookup. The mechanism + data + judgment line are defined in full in the corresponding chapter of the main text; here are only the name + chapter + a one-line mnemonic.

| ID | Pitfall | Chapter | One-line mnemonic |
|---|---|---|---|
| AP01 | cache collusion | §7.4 | N reruns are non-i.i.d. · the per-run nonce fixes it |
| AP02 | the four kinds of leakage | §5.8 | shape leakage / answer spelled out / leading question / preference leakage |
| AP03 | the 7 Reward Hacking patterns | §7.4 | declared_vs_executed gap is the early warning |
| AP04 | Artifact Claim Mismatch | §5.8 | agent declared vs verifier observed disagree |
| AP05 | Fixture / Path Classifier Bug | §7.8 | a data-infrastructure bug that inverts the pass rate |
| AP06 | a fake-landing mechanism | §5.9 | the protocol is in the repo but the production path is a noop |
| AP07 | Tool Over-Design | §5.3 | tool granularity too fine, the LLM cannot choose |
| AP08 | Context Bloat | §5.4 | lost in the middle · context accumulates unbounded |
| AP09 | Multi-Agent Over-Decomposition | §5.1 | Anthropic's 15x cost · don't reach for multi-agent on coding |
| AP10 | Silent Try/Catch | §5.7 / §6 | swallow the exception · the error produces no event |
| AP11 | Loop Blind Spot | §5.6 | the agent does not know it is looping |
| AP12 | Sub-agent Depth Explosion | §5.9 | fork-join without a depth cap / without a token cap |
| AP13 | Hook / Allowlist Bypass | §5.9 | `cargo checkpoint` waved through by a `cargo check` rule |
| AP14 | Memory Pollution | §5.4c | long-term memory accumulates contamination |
| AP15 | Excessive Agency / Unbounded Consumption | §5.9 | OWASP LLM06 + LLM10 |
| AP16 | Schema Coupling | §5.5 | the prompt schema is hard-coupled to the actual data |
| AP17 | Premature Optimization | §7.8 / §7.4 / §10 | tuning before there is baseline data |
| AP18 | Stage Inflation | §7.8 | every mechanism marked production-ready while the engineering is unbuilt |
| AP19 | OTel Naming Drift | §5.7 | internal event names drift from the OTel GenAI semconv |

---

## G · Citation index · grouped by arxiv prefix

The main citation table is in `citations-manifest.md`; here is a quick lookup grouped by arxiv prefix.

**2210.\* (2022)**: react-yao-2022

**2302–2310.\* (2023)**: toolformer-2023 / reflexion-shinn-2023 / tot-yao-2023 / plan-solve-wang-2023 / memgpt-2023 / voyager-2305

**2405–2410.\* (2024)**: swe-agent-2024 / pav-2024

**2502–2511.\* (2025)**: plan-and-act-2025 / reflact-2025 (EMNLP 2025) / gigpo-2025 / preference-leakage-2025 (2502.01534 · ICLR 2026) / mnimi-2025 / agent-prm-2025 (2511.08325) / stop-overvaluing-mad-2025 (2502.08788)

**2510–2511.\* / 2601.\* / 2603–2605.\* (2026)**: hal-2026 (2510.11977) / reward-hacking-equilibrium-2026 (2603.28063) / meta-harness-2026 (2603.28052) / nl-agent-harness-2026 (2603.25723) / claw-eval-2026 (2604.06132) / pcs-2026 (2604.11003) / reward-hacking-era-2026 (2604.13602) / llm-gaming-verifiers-2026 (2604.15149) / skill-ra-2026 (2604.24594) / ahe-2026 (2604.25850) / rhb-2026 (2605.02964) / continual-harness-2026 (2605.09998) / ahe-runtime-substrate-2026 (2605.13357) / tool-prm-bench-2026 (2601.12294) / code-as-agent-harness-survey-2026 (2605.18747) / faulty-memory-2026 (2605.12978) / fate-2026 (2605.11882) / skillopt-2026 (2605.23904)

**Non-arxiv primary sources**: deepseek-v4-tr · owasp-llm-top10-2025 · openai-harness-engineering-2026 · langgraph-docs
