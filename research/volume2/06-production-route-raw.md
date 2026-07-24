# 生产运维与可观测性路线（半程原始检索材料，agent 卡死于 WebFetch langfuse.com）

未经该路 agent 收尾综合，为 WebSearch/WebFetch 原始返回。综合结论已并入 volume2-outline.md。

---


===== WebSearch: OpenTelemetry GenAI semantic conventions agent span tool span 2025 2026 =====
Web search results for query: "OpenTelemetry GenAI semantic conventions agent span tool span 2025 2026"

Links: [{"title":"OpenTelemetry for AI Systems: LLM and Agent Observability (2026) | Uptrace","url":"https://uptrace.dev/blog/opentelemetry-ai-systems"},{"title":"OpenTelemetry for AI Agents: Observability, Tracing, and the GenAI Semantic Conventions | Zylos Research","url":"https://zylos.ai/research/2026-02-28-opentelemetry-ai-agent-observability"},{"title":"OpenTelemetry GenAI Conventions for AI Agents in 2026 | CallSphere Blog","url":"https://callsphere.ai/blog/vw3c-opentelemetry-genai-conventions-ai-agents-2026"},{"title":"How OpenTelemetry Traces LLM Calls, Agent Reasoning, and MCP Tools | Greptime","url":"https://greptime.com/blogs/2026-05-09-opentelemetry-genai-semantic-conventions"},{"title":"Inside the LLM Call: GenAI Observability with OpenTelemetry | OpenTelemetry","url":"https://opentelemetry.io/blog/2026/genai-observability/"},{"title":"Semantic conventions for generative client AI spans | OpenTelemetry","url":"https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/"}]

I found comprehensive information about OpenTelemetry GenAI semantic conventions related to agent spans and tool spans. Here's what the search results show:

## Current Status and Scope

The OpenTelemetry Generative AI Observability SIG began work in April 2024, and as of early 2026, the conventions cover four primary areas: LLM client spans, agent spans, events (for capturing prompt/completion content), and metrics. As of May 2026, the GenAI and MCP semantic conventions remain in Development status.

## Agent and Tool Spans

For agents, each tool call, LLM invocation, and retrieval step becomes a child span, producing a full trace of the reasoning chain. You can wrap your top-level agent invocation function with an invoke_agent span, which creates the root of the decision tree.

## Standardized Attributes

Model name and token counts are defined by the OpenTelemetry GenAI semantic conventions. When an agent calls an LLM provider, the instrumentation should emit a span with gen_ai.operation.name set to chat (or text_completion for older models).

## Industry Adoption

The industry is converging on OpenTelemetry as the standard telemetry layer for AI agent systems, with major vendors including Datadog, Honeycomb, and New Relic already supporting these conventions, and frameworks such as LangChain, CrewAI, AutoGen, and AG2 emitting OTel-compliant spans natively or via instrumentation packages.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.


===== WebSearch: LangSmith Langfuse trace model design agent run turn tool call observability =====
Web search results for query: "LangSmith Langfuse trace model design agent run turn tool call observability"

Links: [{"title":"Agent & LLM Observability Platform - LangSmith","url":"https://www.langchain.com/langsmith/observability"},{"title":"AI Agent Observability, Tracing & Evaluation with Langfuse - Langfuse","url":"https://langfuse.com/blog/2024-07-ai-agent-observability-with-langfuse"},{"title":"LLM Observability & Application Tracing (Open Source) - Langfuse","url":"https://langfuse.com/docs/observability/overview"},{"title":"15 AI Agent Observability Tools in 2026: AgentOps & Langfuse","url":"https://aimultiple.com/agentic-monitoring"},{"title":"Langfuse","url":"https://langfuse.com/"},{"title":"Langfuse vs LangSmith: Which Observability Platform Fits Your LLM Stack? - ZenML Blog","url":"https://www.zenml.io/blog/langfuse-vs-langsmith"},{"title":"Laminar vs Langfuse vs LangSmith: LLM Observability Compared (2026) | Laminar","url":"https://laminar.sh/blog/2026-01-29-laminar-vs-langfuse-vs-langsmith-llm-observability-compared"},{"title":"Top 6 Agent Observability Platforms (2026): A Developer's Ranking | Laminar","url":"https://laminar.sh/article/2026-04-23-top-6-agent-observability-platforms"},{"title":"Top 5 LLM and Agent Observability Tools in 2026 | MLflow","url":"https://mlflow.org/top-5-agent-observability-tools/"},{"title":"Top 6 AI Agent Observability Platforms for 2026 - Confident AI","url":"https://www.confident-ai.com/knowledge-base/compare/best-ai-agent-observability-tools-2026"}]

Here's what I found about LangSmith, Langfuse, trace models, design patterns, agent runs, and tool call observability:

## Overview

LangSmith Observability gives you complete visibility into agent behavior, while Langfuse is an open-source AI engineering platform that provides deep insights into metrics such as latency, cost, and error rates.

## Trace Design & Data Models

Both platforms use different approaches to structure traces:

**Langfuse's Model:** Langfuse frames tracing as structured logs for every request, capturing prompts, responses, token usage, latency, and intermediate steps like tool calls or retrieval. Its data model is traces -> observations -> sessions, and observations can be nested and typed (generations, tool calls, retrieval steps).

**LangSmith's Model:** LangSmith provides end-to-end tracing that captures every significant operation as a "run" within a trace. Each trace represents a complete execution of your application chain or agent. LangSmith tracks prompts, tool calls, LLM outputs, token usage, latency, and cost at granular levels.

## Agent Observability & Tool Calls

Application tracing is structured logs of every request that capture the exact prompt sent, the model's response, token usage, latency, and any tools or retrieval steps in between. Agent traces are deeply nested with heavy payloads. A single conversation can generate megabytes of data across dozens of runs and tool calls.

## Framework Integration

LangSmith can be integrated with any agent stack using Python, Typescript, Go, or Java SDKs, while Langfuse is built on OpenTelemetry, so anything that emits OTEL traces can be ingested, making it possible to plug it into any stack without being locked into a specific agent framework.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.


===== WebSearch: LLM agent production postmortem incident cost runaway infinite loop engineering blog 2025 =====
Web search results for query: "LLM agent production postmortem incident cost runaway infinite loop engineering blog 2025"

Links: [{"title":"The Agent That Spent $47K on Itself: An Autonomous-Loop Postmortem - DEV Community","url":"https://dev.to/gabrielanhaia/the-agent-that-spent-47k-on-itself-an-autonomous-loop-postmortem-3313"},{"title":"What 1,200 Production Deployments Reveal About LLMOps in 2025 - ZenML Blog","url":"https://www.zenml.io/blog/what-1200-production-deployments-reveal-about-llmops-in-2025"},{"title":"Agentic Token Explosion: How to Attribute, Budget, and Control LLM Costs When AI Runs in CI/CD","url":"https://www.truefoundry.com/blog/llm-cost-attribution-agentic-cicd"},{"title":"I Spent $0.20 Reproducing the Multi-Agent Loop That Cost Someone $47K | by Msatfi89 | Medium","url":"https://medium.com/@mohamedmsatfi1/i-spent-0-20-reproducing-the-multi-agent-loop-that-cost-someone-47k-7f57c51f3c06"},{"title":"The Agent Deployment Gap: Why Your LLM Loop Isn't Production-Ready (And What to Do About It) - ZenML Blog","url":"https://www.zenml.io/blog/the-agent-deployment-gap-why-your-llm-loop-isnt-production-ready-and-what-to-do-about-it"},{"title":"AI Agent Failure Modes: What Goes Wrong in Production","url":"https://www.trantorinc.com/blog/ai-agent-failure-modes-what-goes-wrong-design-resilience"},{"title":"AI Agent Loop Token Costs: How to Constrain Context | Augment Code","url":"https://www.augmentcode.com/guides/ai-agent-loop-token-cost-context-constraints"},{"title":"The Agent That Burned $4,200 in 63 Hours: A Production AI Postmortem | by Sattyam Jain | Apr, 2026 | Medium","url":"https://medium.com/@sattyamjain96/the-agent-that-burned-4-200-in-63-hours-a-production-ai-postmortem-d38fd9586a85"},{"title":"The Hidden Cost of Agentic AI: Why Most Projects Still Die Before Production | Splunk","url":"https://www.splunk.com/en_us/blog/observability/why-most-projects-still-die-before-production.html"},{"title":"AI Agents Burn 50x More Tokens Than Chats | LeanOps","url":"https://leanopstech.com/blog/agentic-ai-cost-runaway-token-budget-2026/"}]

I found several relevant results about LLM agent production incidents involving runaway infinite loops and significant costs. Here are the key findings:

## The $47,000 Incident

The most notable case involved four LangChain agents with no step cap that ran for 11 days of recursion, resulting in a $47,000 LLM API spend on an internal research tool. This story was first written up on Medium and picked up by Tech Startups in November 2025.

The multi-agent system for market data research escalated from $127 in weekly costs to $47,000 over four weeks due to an infinite conversation loop between agents running undetected for 11 days. More specifically, Agent A requested help from Agent B, which in turn asked Agent A for clarification, creating a recursive pattern that neither agent had the logic to break.

## Key Lessons and Recommended Safeguards

The recommended approach involves three key assertions: step cap, budget limit, and loop detector — to prevent runaway iteration, credit card charges, and the exact failure mode where two agents kept talking because no code told them to stop.

The $47,000 incident was not caused by bad engineering. It was caused by a missing layer — specifically the absence of middleware that inspects tool calls for patterns indicating the system is stuck.

The incident has become a widely referenced case study in engineering blogs about the production deployment challenges of autonomous AI agents.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.


===== WebSearch: NeMo Guardrails Llama Guard input output validation architecture production 2025 =====
Web search results for query: "NeMo Guardrails Llama Guard input output validation architecture production 2025"

Links: [{"title":"AI Guardrails: Implementing Safety for Production LLM Apps","url":"https://bigdataboutique.com/blog/ai-guardrails-implementing-safety-production-llm-apps"},{"title":"LLM Guardrails: Setup Guide 2026 - AI Workflow Lab","url":"https://aiworkflowlab.dev/article/llm-guardrails-production-defense-in-depth-safety-systems-nemo-guardrails-ai-openai"},{"title":"LLM Guardrails: Production Safety Layers Reference 2026","url":"https://www.digitalapplied.com/blog/llm-guardrails-production-safety-layers-reference-2026"},{"title":"AI Agent Guardrails: NeMo, LlamaGuard & Safety Layers (2026)","url":"https://cowork.ink/blog/ai-agent-guardrails/"},{"title":"Building Guardrails for Large Language Models","url":"https://arxiv.org/pdf/2402.01822"},{"title":"Guardrails Architecture — NVIDIA NeMo Platform Documentation","url":"https://docs.nvidia.com/nemo/microservices/latest/guardrails/concepts/architecture.html"},{"title":"AI Guardrails Compared: NeMo vs Guardrails AI vs Llama Guard","url":"https://particula.tech/blog/ai-guardrails-compared-nemo-guardrails-ai-llama-guard"},{"title":"Evaluating the Robustness of Large Language Model Safety Guardrails Against Adversarial Attacks","url":"https://arxiv.org/pdf/2511.22047"}]

Based on the search results, here's what I found about NeMo Guardrails, Llama Guard, and their input/output validation architecture for production:

## NeMo Guardrails Architecture

NVIDIA NeMo Guardrails takes an orchestration approach using its Colang DSL to define conversational policies covering input rails, output rails, dialog rails, and retrieval rails, with action hooks for calling external classifiers or APIs mid-flow. Recent releases added parallel rails execution and OpenTelemetry-based tracing.

NeMo provides programmable dialog rails in the Colang DSL across five pipeline stages at under 50ms per check on GPU, best for controlling conversation flow. The framework's dialog-rail architecture models the full dialog between user and LLM, meaning it can track multi-turn injection attempts that single-turn classifiers miss.

However, NeMo v0.17.0 (October 2025) is the latest stable release; NVIDIA explicitly states the project is not recommended for production as-is in its current beta state.

## Llama Guard in Production

Meta Llama Guard 4 is a 12-billion-parameter natively multimodal safety classifier, released April 30, 2025, created by pruning the Llama 4 Scout pre-trained mixture-of-experts model into a dense architecture and fine-tuning for content safety classification across text and images. It classifies content against customizable policy categories on both inputs and outputs.

## Combined Architecture for Production

The combined open-source stack many teams converge on is: Presidio strips PII at ingress, Prompt Guard 2 detects injection inline, NeMo Guardrails orchestrates dialog policy, Llama Guard 4 classifies output safety, and a schema validator gates structured output.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.


===== WebSearch: LLM agent token budget rate limit governance concurrency cost engineering production =====
Web search results for query: "LLM agent token budget rate limit governance concurrency cost engineering production"

Links: [{"title":"Rate limiting for LLM applications: Why it matters and how to implement it","url":"https://portkey.ai/blog/rate-limiting-for-llm-applications/"},{"title":"LLM Rate Limiting and Token Quotas in Production | metacto","url":"https://www.metacto.com/blogs/llm-rate-limiting-token-quotas-production"},{"title":"AI Agent Cost Optimization: Token Economics and FinOps in Production | Zylos Research","url":"https://zylos.ai/research/2026-02-19-ai-agent-cost-optimization-token-economics/"},{"title":"Rate Limiting in AI Gateway : The Ultimate Guide","url":"https://www.truefoundry.com/blog/rate-limiting-in-llm-gateway"},{"title":"Token-Based Rate Limiting: How to Manage AI Agent API Traffic in 2026 - Zuplo","url":"https://zuplo.com/learning-center/token-based-rate-limiting-ai-agents"},{"title":"How to Implement LLM Rate Limiting","url":"https://oneuptime.com/blog/post/2026-01-30-llm-rate-limiting/view"},{"title":"AI Agent Cost Governance: Cap Token Spend Smartly","url":"https://isimplifyme.com/blog/ai-agent-cost-governance"},{"title":"Top 5 AI Gateways to Monitor and Control the Costs of LLMs","url":"https://www.getmaxim.ai/articles/top-5-ai-gateways-to-monitor-and-control-the-costs-of-llms/"},{"title":"LLM Cost Optimization for Agent Workflows: A Practical Guide - DEV Community","url":"https://dev.to/omnithium/llm-cost-optimization-for-agent-workflows-a-practical-guide-49c1"}]

Based on the search results, here's a comprehensive overview of LLM agent token budget, rate limiting, governance, concurrency, and cost engineering in production:

## Key Frameworks and Approaches

To design production-grade LLM rate limiting, you need token-based, request-based, and cost-based controls that align traffic with both compute capacity and budget constraints.

Per-tenant quotas exist along three axes: token budget, request rate, concurrency. All three are enforced. This is critical because request rate limits catch concurrency and abuse patterns that token budgets miss. A buggy customer integration or a stuck agent loop hits a wall instead of consuming your entire budget.

## Token Budget Management

Token budgets reflect actual cost — a single long RAG query can equal a thousand short chats — so capping tokens enforces real economic fairness. Token-based limits control how much model computation occurs by enforcing tokens per minute (TPM) or tokens per day.

AI agent cost governance is the practice of setting per-agent token budgets, enforcing tool-call ceilings, and instrumenting observability hooks so that an organization can predict, attribute, and control LLM spend without degrading the workflows users depend on. It treats tokens as a metered utility rather than an unbounded operational expense.

## Agent-Specific Challenges

Agents make 3–10x more LLM calls than simple chatbots — a single user request can trigger planning, tool selection, execution, verification, and response generation, easily consuming 5x the token budget of a direct chat completion. An unconstrained agent solving a software engineering task can cost $5–8 per task in API fees alone.

## Best Practices

Budget values should be derived from empirical p99 consumption measurements, not guesses. In 2026, the teams shipping sustainable agent systems are treating cost as a first-class engineering concern alongside latency and reliability.

Budgets are reserved before the call and reconciled against actual usage after. Upstream provider headroom is allocated across tenants explicitly, with reserved slices and a shared burst pool.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.


===== WebFetch: https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-spans/ =====
# GenAI Semantic Conventions - Information Unavailable

Based on the web page content provided, I cannot extract the specific span definitions, attribute names, or nesting structures you've requested.

The page contains only a **redirect notice** stating:

> "GenAI semantic conventions have moved to the [OpenTelemetry GenAI semantic conventions repository](https://github.com/open-telemetry/semantic-conventions-genai). This page has moved and is no longer maintained in this repository."

**What's missing from this source:**
- No span name definitions (chat, execute_tool, etc.)
- No attribute specifications (gen_ai.operation.name, gen_ai.agent.id, etc.)
- No nesting or relationship documentation
- No stability status information
- No token usage attribute details

**To obtain the information you need**, you would need to:
1. Access the official OpenTelemetry GenAI semantic conventions repository directly
2. Review their current documentation for precise attribute names and span hierarchies
3. Check their repository for stability status and development version

The page provided only serves as a pointer to the relocated documentation rather than containing the technical specifications themselves.


===== WebFetch: https://opentelemetry.io/blog/2026/genai-observability/ =====
# OpenTelemetry GenAI Observability: Span Hierarchy and Data Model

## Span Hierarchy Architecture

The document describes a clear hierarchical structure for agent operations:

> "the top-level `invoke_agent` span with child `chat` spans for each LLM call and `execute_tool` spans for each tool invocation"

This maps agent execution as:
- **Root span**: `invoke_agent` (entire agent interaction)
- **Child spans**: `chat` (LLM calls) and `execute_tool` (tool invocations)

## Content Capture: Spans vs. Events

Content handling uses span attributes rather than distinct events. The page indicates: 

> "messages and tool calls are captured as structured span attributes such as `gen_ai.system_instructions`, `gen_ai.input.messages`, and `gen_ai.output.messages`"

Content capture is **optional and disabled by default** due to sensitivity concerns, requiring explicit enablement via configuration.

## Key Metrics Defined

Two primary metric types are specified:

1. **`gen_ai.client.operation.duration`** — LLM call latency histogram
2. **`gen_ai.client.token.usage`** — token consumption histogram (filterable by input/output type)

## 2025-2026 Status

The document provides **no information about 2025-2026 developments**. It only notes the conventions are "under active development" and solicits community feedback, suggesting this represents the current baseline rather than future roadmap details.


===== WebFetch: https://docs.nvidia.com/nemo/microservices/latest/guardrails/concepts/architecture.html =====
# NeMo Guardrails Architecture Analysis

Based on the provided documentation, I can only offer limited insights, as the page doesn't detail the five rail types or their execution mechanics.

## What the Documentation Shows

The architecture places guardrails as an intermediary layer: **"NeMo Guardrails places NemoGuard NIMs between your application and the application's LLM."** This positions the safety layer before and after model inference.

The workflow demonstrates sequential checking: user input flows to NemoGuard models for content safety validation, then—if approved—to the generation model (like Llama Nemotron), followed by output validation before returning responses to the application.

The platform supports multiple configurations simultaneously: **"A single NeMo Guardrails instance can serve multiple applications and help manage multiple guardrail configurations and LLMs."**

## Critical Limitations

The provided webpage does not address:
- The five specific rail categories (input, dialog, output, retrieval, execution)
- Parallel vs. sequential execution modes
- Latency characteristics
- Integration specifics with external classifiers
- Detailed request/response flow positions for different rail types

To obtain comprehensive architectural details about rail execution patterns and latency profiles, you would need to consult additional NeMo documentation sections or API references not included in this excerpt.
