# Appendix · Harness Study quick reference

> This appendix is for looking things up as you need them; it does not replace the explanations in the main text. Each section opens with a sentence or two of explanation, and each table has one row per item. The mechanisms themselves are discussed in §I–§X of the main text.

---

## A · Primary source index

The name "harness engineering" gradually caught on in 2026. The primary sources below are the ones this book cites most often, collected here for reference.

| Source | Date | Link | Core thesis |
|---|---|---|---|
| OpenAI · Harness Engineering | 2026-02-13 | [openai.com/index/harness-engineering](https://openai.com/index/harness-engineering/) | Codex's agent-first design |
| Mitchell Hashimoto · My AI Adoption Journey | 2026-02-05 | [mitchellh.com/writing/my-ai-adoption-journey](https://mitchellh.com/writing/my-ai-adoption-journey) | the HashiCorp founder's perspective (not Stanford NLP's Tatsu Hashimoto) |
| Trivedy · The Anatomy of an Agent Harness | 2026-03-10 | [blog.langchain.com/the-anatomy-of-an-agent-harness](https://blog.langchain.com/the-anatomy-of-an-agent-harness/) | 5 components; the "Agent = Model + Harness" formula |
| Birgitta Böckeler · Harness Engineering for Coding Agent Users | 2026-04-02 | [martinfowler.com/articles/harness-engineering.html](https://martinfowler.com/articles/harness-engineering.html) | a Thoughtworks consulting perspective; borrows feedforward and feedback from cybernetics as an analogy |

**Further reading**

- Lopopolo · Extreme Harness Engineering (latent.space interview, 2026-02): [latent.space/p/harness-eng](https://www.latent.space/p/harness-eng). Covers OpenAI Frontier and Symphony, and the phrase "token billionaire."

---

## B · The Evidence Graph ten edges · an observable-relation ontology

§8.4 covers it in full; this is the short lookup table. The Evidence Graph is the graph this book uses to describe how the mechanisms and cells of a running agent system relate to one another. ("Ontology" is a borrowed word here: it means the list of relation types.) There are 10 kinds of edge.

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
| contradicts | A refutes B's conclusion | what the agent claims disagrees with what the verifier observes (the most valuable diagnostic signal) |

---

## C · OWASP Top 10 for LLM Applications 2025

The OWASP list is the main source cited in §5.9 Safety. Here is a short table and the link; for the full content, [genai.owasp.org/llm-top-10](https://genai.owasp.org/llm-top-10/) is authoritative.

| ID | Name | Chapter |
|---|---|---|
| LLM01 | Prompt Injection | §5.9.4 |
| LLM02 | Sensitive Information Disclosure | §5.7 PII redaction |
| LLM03 | Supply Chain | (listed in the appendix only; not covered in the main text) |
| LLM04 | Data and Model Poisoning | §5.4 AP14 |
| LLM05 | Improper Output Handling | §5.8 verifier |
| LLM06 | Excessive Agency | §5.9 AP15 |
| LLM07 | System Prompt Leakage | §5.5 |
| LLM08 | Vector and Embedding Weaknesses | §5.9 |
| LLM09 | Misinformation | §5.8 verifier |
| LLM10 | Unbounded Consumption | §5.9 AP15 |

---

## D · Mapping industry products onto the mechanisms

This section maps the mainstream industry products and technologies of 2026 onto this book's 8 runtime mechanisms plus 1 Safety control plane. When you meet a new product, look it up in this table first, find the mechanism it mainly corresponds to, then jump to that chapter of the main text. "Primary mechanism" means the mechanism where the product's main function sits; "Other mechanisms involved" lists the further mechanisms it affects.

### D.1 Mapping mainstream industry products and technologies

| Industry name | Primary mechanism | Function | Other mechanisms involved |
|---|---|---|---|
| **MCP (Model Context Protocol)** | §5.3 Tool | tool-call protocol, interoperable across vendors | §5.4 partial (an MCP server can expose a retrieval interface) |
| **OpenAI function calling** | §5.3 Tool | tool-call protocol, within one vendor | — |
| **Anthropic tool use** | §5.3 Tool | tool-call protocol, within one vendor | — |
| **Anthropic Agent Skills open standard (SKILL.md)** | §5.5 Prompt | three-layer loading: metadata, body, and supporting files loaded on demand | §5.3 partial (a Skill can embed a tool definition) |
| **CLAUDE.md / .cursorrules / AGENTS.md** | §5.5 Prompt | project-level, loaded at startup | — |
| **hook (Claude Code / OpenCode / settings.json)** | §5.5 Prompt + §5.9 Safety | injects content at specific call points and runs safety checks | §5.6 partial |
| **system prompt (vendor built-in)** | §5.5 Prompt | injected at startup, never trimmed | — |
| **few-shot examples** | §5.5 Prompt | an inline asset, written into the user message | — |
| **LangChain prompt templates / LangSmith** | §5.5 Prompt | versioned management platform with A/B testing | — |
| **RAG (Retrieval-Augmented Generation)** | **cross-cutting** | a retrieve-and-inject engineering pattern, **not a mechanism of its own** | §5.3 (retrieval as a tool) / §5.4.2 Memory / §5.4.3 Artifact |
| **GraphRAG / HippoRAG / LightRAG / KG-RAG** | **cross-cutting** | RAG variants with a knowledge-graph backend | §5.4.2 / §5.4.3 |
| **vector DB (Pinecone / Chroma / Weaviate / Qdrant)** | §5.4.2 / §5.4.3 backend | vector retrieval storage | RAG backend |
| **knowledge graph (Neo4j / Memento)** | §5.4.2 / §5.4.3 backend | relational retrieval storage | RAG backend |
| **Memory framework (Mem0 / Letta / Memori)** | §5.4.2 Memory | an engineering wrapper for governing the memory lifecycle | — |
| **Karpathy LLM Knowledge Base / Markdown wiki** | §5.4.2 + §5.4.3 hybrid | a Markdown persistence layer | §5.5 partial |
| **Bitemporal KG (Zep / Graphiti)** | §5.4.3 Artifact | a mid-scale engineering form, with two time axes | — |
| **Enterprise Decision Platform (Palantir Foundry Ontology)** | §5.4.3 Artifact | a heavyweight engineering form, for decisions across departments | — |
| **Auto Dream / `/dream` (described in third-party blogs; not found in official docs)** | §5.4.2 Memory | one implementation of the memory consolidation lifecycle | — |
| **LangGraph nodes / states** | §5.1 Agent Loop | a control-flow orchestration implementation | — |
| **CrewAI / AutoGen** | §5.1 + multi-agent orchestration | multi-agent collaboration framework | spans several mechanisms |
| **OpenAI Assistants API** | §5.1 + §5.3 + §5.4 partial combination | a vendor integration framework | spans several mechanisms |
| **Codex CLI / Claude Code / Cursor** | §5.1 + §5.3 + §5.5 + §5.7 + §5.9 combination | a complete coding-agent harness instance | spans several mechanisms |
| **OpenAPI / GraphQL schema auto-to-tool** | §5.3 Tool | a tool-exposure technique | — |
| **Pydantic AI tools** | §5.3 Tool | a Python embedded-tool abstraction | — |
| **Inspect AI / trajectory replay tools** | §5.7 Trajectory | offline replay and audit | — |
| **OTel GenAI semantic conventions** | §5.7 Trajectory | a standard naming convention for trajectory fields | — |
| **Verifier (rule-based / LLM-as-judge / outcome reward)** | §5.8 Verifier | the three implementation classes | — |
| **PRM (Process Reward Model)** | §5.8 Verifier | the third layer, process supervision (rarely used as an online gate) | — |
| **Llama Guard / Anthropic Constitutional Classifiers** | §5.9 Safety | runtime content classifiers (Constitutional AI is a training method, not a runtime filter) | — |
| **SPIFFE** | §5.9 Safety | a workload identity standard | see Appendix E |
| **Biscuit** | §5.9 Safety | an authorization token that supports offline attenuation | see Appendix E |
| **Zanzibar** | §5.9 Safety | relation-based authorization (the paper uses ACLs and relation tuples; the industry commonly classes it as ReBAC) | see Appendix E |
| **OWASP Top 10 LLM 2025** | §5.9 Safety | the systematic mapping for LLM06 and LLM10 | see Appendix C |

### D.2 How the industry divides up a harness

The industry divides "what a harness is made of" in several ways. The opening of §V explains why this book uses 8 mechanisms plus 1 control plane; the main alternatives are set side by side here for comparison.

| Source | Count | How it divides | Relation to this book |
|---|---|---|---|
| **Augment Code, 3 layers** | 3 | Constraint / Feedback Loops / Quality Gates | divides by governance purpose; highly abstract, suited to strategy discussions |
| **Vivek Trivedy, 5 components** | 5 | System Prompts / Tools / Bundled Infrastructure / Orchestration / Hooks & Middleware | divides by engineering component; Bundled Infrastructure reads like a catch-all |
| **MongoDB, 6 items** | 6 | context / tool / planning / error recovery / validation / memory | similar granularity, but no separate Safety layer |
| **Firecrawl / DataCamp, 9 items** | 9 | model / tool / context / planning / execution / memory / feedback / safety / orchestration | finer granularity; the relations between the items are not clear |
| **This book, 8 + 1** | 8 + 1 | Agent Loop / Model / Tool / Context-Memory-Artifact / Prompt / Observation / Trajectory / Verifier + Safety | each mechanism maps to a code module; runtime mechanisms and the control plane are explicitly layered |

### D.3 How to use the reverse lookup

- For any new industry product, look it up in the "Industry name" column of §D.1, find the mechanism it mainly corresponds to, then jump to that chapter of the main text.
- If a new product spans several mechanisms, it is usually a framework or an integrated product and does not belong to any one of the 8. In that case, work out which of the 8 mechanisms it covers and which it leaves out.
- If a new product is an engineering pattern that cuts across several mechanisms (as RAG does), mark it "cross-cutting" and place it under no single mechanism.
- §D.1 cannot list every product. For one that appears later, work out where it belongs by asking which function of which mechanism it serves.

---

## E · SPIFFE, Biscuit, Zanzibar · identity, authorization tokens, and relation-based authorization

§5.9, on the Safety control plane, mentions these three schemes. They are often discussed together, but they solve problems at different levels and should be kept apart:

- **SPIFFE** (Secure Production Identity Framework for Everyone, [spiffe.io](https://spiffe.io/docs/latest/spiffe-about/spiffe-concepts/)): a **workload identity** standard. It answers "who is this service or agent?" and is commonly used to authenticate identities across service meshes. For a practical introduction to using it with LLM agents, see [SPIFFE Securing AI Agent Identity (HashiCorp blog)](https://www.hashicorp.com/en/blog/spiffe-securing-the-identity-of-agentic-ai-and-non-human-actors).
- **Biscuit**: an **authorization token with offline attenuation**. Without contacting the issuer, a holder can add restrictions to a token and derive a new token with fewer permissions, and the token can be verified offline. It supports two styles of use: as a capability token (holding it grants the right) and with ACLs. Its granularity can go down to a single task, finer than JWT.
- **Zanzibar** (Google): a **relation-based authorization** system. The paper describes permissions with ACLs and relation tuples, and the industry commonly classes it as relationship-based access control (ReBAC).

None of the three is specific to LLMs. They are general-purpose identity and authorization schemes, and this book cites them only as reference points without going into detail.

---

## F · Anti-pattern quick reference (AP01–AP20)

The book names 20 anti-patterns in all, gathered here for quick lookup. For each one, the mechanism, the data, and the conditions for recognizing it are defined in the main text of its chapter; this table lists only the name, the chapter, and a one-line mnemonic. Where the main text first mentions one, it is written as "Name (APxx, see Appendix F)".

| ID | Anti-pattern | Chapter | One-line mnemonic |
|---|---|---|---|
| AP01 | Non-Independent Reruns | §7.4 | N reruns are not independent: response caching, a fixed seed, shared state; a prefix-cache hit does not change the output |
| AP02 | Four Kinds of Leakage | §5.8 | shape leakage, answer disclosure, leading question, preference leakage |
| AP03 | Reward Hacking | §7.4 | six common forms, listed in §7.4; the gap between what is claimed and what was actually done (the declared_vs_executed gap) is an early-warning sign |
| AP04 | Artifact Claim Mismatch | §5.8 | what the agent claims disagrees with what the verifier observes |
| AP05 | Fixture / Path Classifier Bug | §7.8 | a bug in the data infrastructure reverses the pass-rate conclusion |
| AP06 | Fake-Landing Mechanism | §5.9 | the mechanism is in the repo, but on the production path it does nothing |
| AP07 | Tool Over-Design | §5.3 | tool granularity too fine, so the model has trouble picking the right one |
| AP08 | Context Bloat | §5.4 | lost in the middle; context accumulates without limit |
| AP09 | Multi-Agent Over-Decomposition | §5.1 | multi-agent systems use about 15 times the tokens of an ordinary chat (Anthropic, 2025-06); coding tasks have little that can run in parallel, so use with care |
| AP10 | Silent Try/Catch | §6.7 | the exception is swallowed, and the error produces no event |
| AP11 | Loop Blind Spot | §III / §7.8 | the agent does not know it is going in circles |
| AP12 | Sub-agent Depth Explosion | §5.9 | fork-join with no depth cap and no token cap |
| AP13 | Hook / Allowlist Bypass | §5.9 | the allow rule matches by string prefix, so a `cargo check` rule lets `cargo checkpoint` through (a real case from the author's companion project; see Volume 2 (*Architecture & Engineering*), §2.7); fix: match whole words |
| AP14 | Memory Pollution | §5.4c | long-term memory keeps accumulating wrong content |
| AP15 | Excessive Agency / Unbounded Consumption | §5.9 | OWASP LLM06 + LLM10 (2025 edition) |
| AP16 | Schema Coupling | §5.5 | the schema in the prompt, the test cases, and the verifier are hard-wired together; change one and the other two break silently |
| AP17 | Premature Optimization | §7.8 / §7.4 / §X | tuning on conclusions drawn before enough data is in; the bar is a confidence interval that does not cross 0 |
| AP18 | Stage Inflation | §7.8 | every mechanism is marked "production-ready" while the engineering is unfinished |
| AP19 | OTel Naming Drift | §5.7.4 | internal event names gradually drift from the OTel GenAI semantic conventions |
| AP20 | Overfitting to a Fixed Test Set | §7.4 | tune on a development set; keep a held-out set out of tuning and use it only to compare before and after a change; feed production failures back as case records |

---

## G · Citation index · grouped by arXiv ID prefix

This section groups the works cited in the main text by arXiv ID prefix for quick lookup; the full entries are in each chapter's footnotes.

**2210.\* (2022)**: react-yao-2022

**2302–2310.\* (2023)**: toolformer-2023 / reflexion-shinn-2023 / tot-yao-2023 / plan-solve-wang-2023 / memgpt-2023 / voyager-2305

**2405–2410.\* (2024)**: swe-agent-2024 / pav-2024

**2502–2511.\* (2025)**: plan-and-act-2025 / reflact-2025 (EMNLP 2025) / gigpo-2025 / preference-leakage-2025 (2502.01534, ICLR 2026) / mnimi-2025 / agent-prm-2025 (2511.08325) / stop-overvaluing-mad-2025 (2502.08788)

**2510–2511.\* / 2601.\* / 2603–2605.\* (2026)**: hal-2026 (2510.11977) / reward-hacking-equilibrium-2026 (2603.28063) / meta-harness-2026 (2603.28052) / nl-agent-harness-2026 (2603.25723) / claw-eval-2026 (2604.06132) / pcs-2026 (2604.11003) / reward-hacking-era-2026 (2604.13602) / llm-gaming-verifiers-2026 (2604.15149) / skill-ra-2026 (2604.24594) / ahe-2026 (2604.25850) / rhb-2026 (2605.02964) / continual-harness-2026 (2605.09998) / ahe-runtime-substrate-2026 (2605.13357) / tool-prm-bench-2026 (2601.12294) / code-as-agent-harness-survey-2026 (2605.18747) / faulty-memory-2026 (2605.12978) / fate-2026 (2605.11882) / skillopt-2026 (2605.23904)

**Non-arXiv primary sources**: deepseek-v4-tr, owasp-llm-top10-2025, openai-harness-engineering-2026, langgraph-docs
