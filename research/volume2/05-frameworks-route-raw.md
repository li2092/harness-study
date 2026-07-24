# 框架与 durable execution 路线（半程原始检索材料，agent 卡死于 WebFetch ai-sdk.dev）

未经该路 agent 收尾综合，为 WebSearch/WebFetch 原始返回。综合结论已并入 volume2-outline.md。

---


===== WebSearch: LangGraph checkpointer durability modes exit async sync 2025 documentation =====
Web search results for query: "LangGraph checkpointer durability modes exit async sync 2025 documentation"

Links: [{"title":"Durable execution - Docs by LangChain","url":"https://docs.langchain.com/oss/python/langgraph/durable-execution"},{"title":"Sydney Runkle on X: \"🏗️LangGraph now offers a durability mode for fine-grained persistence control. Control how your agentic workflows resume (post crash, human intervention, timeout, you name it) with these 3 modes, from least to most durable: ⚡ \"exit\": fast (checkpoint only at end) ⚖️ \"async\":\" / X","url":"https://x.com/sydneyrunkle/status/1950934319888785498"},{"title":"Durable Execution in LangGraph: Agents That Survive Failure and Resume Where They Left Off | Vadim's blog","url":"https://vadim.blog/durable-execution-agents-that-survive-failure-and-resume-where-they-left-off"},{"title":"Durability | langgraph | LangChain Reference","url":"https://reference.langchain.com/python/langgraph/types/Durability"},{"title":"Understanding Checkpointers, Databases, API Memory ...","url":"https://support.langchain.com/articles/6253531756-understanding-checkpointers-databases-api-memory-and-ttl?threadId=285c524c-7b58-44e4-89ab-210e6393cc7e"},{"title":"Durability | langgraph_sdk | LangChain Reference","url":"https://reference.langchain.com/python/langgraph-sdk/schema/Durability"},{"title":"Mastering LangGraph Checkpointing: Best Practices for 2025","url":"https://sparkco.ai/blog/mastering-langgraph-checkpointing-best-practices-for-2025"},{"title":"checkpoints | langgraph | LangChain Reference","url":"https://reference.langchain.com/python/langgraph/checkpoints"},{"title":"Why Checkpoints Aren't Durable Execution: LangGraph","url":"https://www.diagrid.io/blog/checkpoints-are-not-durable-execution-why-langgraph-crewai-google-adk-and-others-fall-short-for-production-agent-workflows"},{"title":"Checkpoint Implementations | langchain-ai/langgraph | DeepWiki","url":"https://deepwiki.com/langchain-ai/langgraph/4.2-checkpoint-implementations"}]

Based on the web search results, here's comprehensive information about LangGraph checkpointer durability modes:

## LangGraph Durability Modes

LangGraph supports three durability modes for graph execution: 'sync', 'async', and 'exit'.

### The Three Modes

**1. "exit" Mode**
"exit" persists changes only when graph execution exits either successfully, with an error, or due to a human in the loop interrupt. This provides the best performance for long-running graphs but means intermediate state is not saved, so you cannot recover from system failures (like process crashes) that occur mid-execution.

**2. "async" Mode** 
"async" LangGraph persists changes asynchronously while the next step executes. This provides good performance and durability, but there's a small risk that LangGraph does not write checkpoints if the process crashes during execution.

**3. "sync" Mode**
"sync" LangGraph persists changes synchronously before the next step starts. This ensures that LangGraph writes every checkpoint before continuing execution, providing high durability at the cost of some performance overhead.

### Summary

These three modes range from least to most durable: "exit" (fast, checkpoint only at end), "async" (balanced, async during the next step), and "sync" (bulletproof, sync before each step).

### Deprecation Note

ShallowPostgresSaver and AsyncShallowPostgresSaver are deprecated as of version 2.0.20 and will be removed in 3.0.0. Users should transition to PostgresSaver and use the durability='exit' flag in graph invocation for similar behavior.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.


===== WebSearch: Restate durable execution AI agents design 2025 =====
Web search results for query: "Restate durable execution AI agents design 2025"

Links: [{"title":"Durable Execution Patterns for AI Agents: Building Fault-Tolerant Autonomous Systems | Zylos Research","url":"https://zylos.ai/research/2026-02-17-durable-execution-ai-agents"},{"title":"Durable Execution: The Key to Harnessing AI Agents in Production - Inngest Blog","url":"https://www.inngest.com/blog/durable-execution-key-to-harnessing-ai-agents"},{"title":"Durable Execution for AI Agent Runtimes: Checkpointing, Replay, and Recovery | Zylos Research","url":"https://zylos.ai/research/2026-04-24-durable-execution-agent-runtimes/"},{"title":"AI Agents should be serverless and durable | Restate","url":"https://www.restate.dev/blog/resilient-serverless-agents"},{"title":"Durable Execution for AI Agents","url":"https://quellixlabs.com/insights/durable-execution-long-running-ai-agent-workflows"},{"title":"Build durable agents with Restate and Pydantic AI","url":"https://pydantic.dev/articles/restate-durable-execution-pydanticai"},{"title":"Durable Agents - Restate","url":"https://docs.restate.dev/ai/patterns/durable-agents"},{"title":"Restate plugin for ADK - Agent Development Kit (ADK)","url":"https://adk.dev/integrations/restate/"}]

Here are the search results for "Restate durable execution AI agents design 2025":

## Overview

Durable execution, a programming model that guarantees code completion despite failures, has crossed into the early majority in 2025 with new offerings from AWS, Cloudflare, and Vercel, driven primarily by AI Agent infrastructure needs.

## What is Restate?

Restate is an open-source system that provides Durable Execution for applications, workflows, and agents, with a server that sits in front of serverless functions like a proxy or stateful orchestrator and manages durability, retries, and recovery.

## Key Design Patterns

Every LLM call, tool execution, and routing decision is durably persisted, with every step recorded in a journal so agents pick up exactly where they left off if crashes occur. The system records a journal of all completed steps; crashes trigger replay where completed steps return cached results without re-execution.

## 2025 Developments

Restate Cloud opened publicly in 2025 with usage-based pricing, with production use cases including AI workflows, crypto trading, and banking infrastructure. Additionally, OpenAI Agents SDK integrated durable execution in September 2025.

## Production Benefits

AI Agents introduce multiple points of failure (orchestration, probabilistic LLM behavior, tool calling, human-in-the-loop) that traditional retry logic cannot handle; durable execution provides automatic state persistence, automatic retries, and workflow resumption that make agents production-ready.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.


===== WebSearch: Inngest AgentKit durable agent workflow design 2025 =====
Web search results for query: "Inngest AgentKit durable agent workflow design 2025"

Links: [{"title":"Building Agentic Workflows That Query Millions of Rows: A Real-World Guide with AgentKit - Inngest Blog","url":"https://www.inngest.com/blog/building-agentic-workflows-that-can-query"},{"title":"Inngest - Durable Execution for Workflows & AI","url":"https://www.inngest.com/"},{"title":"Introducing useAgent: One Hook to Stream Durable AI Workflows to the Frontend - Inngest Blog","url":"https://www.inngest.com/blog/agentkit-useagent-realtime-hook"},{"title":"Temporal vs Inngest (2026): Durable Execution for AI Agents","url":"https://wetheflywheel.com/en/comparisons/temporal-vs-inngest/"},{"title":"Inngest - Developer Guides, Videos & Learning Hub","url":"https://www.inngest.com/blog"},{"title":"AgentKit | AgentKit by Inngest","url":"https://agentkit.inngest.com/"},{"title":"Agents | AgentKit by Inngest","url":"https://agentkit.inngest.com/concepts/agents"},{"title":"OpenAI AgentKit vs Google ADK vs Inngest: Complete 2025 Comparison - DEV Community","url":"https://dev.to/rshivakumar/openai-agentkit-vs-google-adk-vs-inngest-complete-2025-comparison-3b5i"},{"title":"Inngest - AI Workflow Orchestration & Agent Infrastructure","url":"https://www.inngest.com/ai"},{"title":"Test Inngest AgentKit Agents – Scenario","url":"https://langwatch.ai/scenario/agent-integration/agentkit/"}]

Based on the search results, here's what I found about Inngest AgentKit and durable agent workflow design in 2025:

## Overview

Inngest has developed AgentKit, a developer-first framework for building agentic workflows using only code. AgentKit is a framework to build AI Agents, from single model inference calls to multi-agent systems that use tools, designed with orchestration at its core, enabling developers to build, test, and deploy reliable AI applications at scale.

## Key Architecture Components

AgentKit enables developers to compose simple single-agent systems or entire systems of agents in which multiple agents can work together, combined into Networks which include a Router to determine which Agent should be called, with their system's memory recorded as Network State.

## Durable Execution

Inngest checkpoints every step of a workflow, and if your server crashes mid-execution, the workflow picks up exactly where it left off, coming from workflow engines like Temporal and AWS Step Functions. The framework provides built-in durability with automatic retries and fault tolerance.

## Streaming and UI Integration

useAgent is the React hook that enables developers to stream realtime experiences from the durable, backend AI workflows they create with AgentKit. "No WebSocket management, no state stores, no connection handling—just durable, observable AI workflows streaming to your UI".

## Real-World Example

Inngest tested AgentKit by building a multi-agent system that queries and analyzes 3.5 million powerlifting records using natural language.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.


===== WebSearch: LangGraph Platform production deployment architecture task queue persistence 2025 =====
Web search results for query: "LangGraph Platform production deployment architecture task queue persistence 2025"

Links: [{"title":"LangGraph Platform is now Generally Available: Deploy & manage long-running, stateful Agents","url":"https://www.langchain.com/blog/langgraph-platform-ga"},{"title":"LangGraph Agents in Production: Architecture, Costs & Real-World Outcomes","url":"https://www.alphabold.com/langgraph-agents-in-production/"},{"title":"LangGraph AI Framework 2025: Complete Architecture Guide + Multi-Agent Orchestration Analysis - Latenode Blog","url":"https://latenode.com/blog/ai-frameworks-technical-infrastructure/langgraph-multi-agent-orchestration/langgraph-ai-framework-2025-complete-architecture-guide-multi-agent-orchestration-analysis"},{"title":"LangGraph Multi-Agent Orchestration: Complete Framework Guide + Architecture Analysis 2025 - Latenode Blog","url":"https://latenode.com/blog/ai-frameworks-technical-infrastructure/langgraph-multi-agent-orchestration/langgraph-multi-agent-orchestration-complete-framework-guide-architecture-analysis-2025"},{"title":"LangGraph AI Framework 2025: Complete Architecture Guide + Multi-Agent Orchestration Analysis","url":"https://latenode.com/blog/langgraph-ai-framework-2025-complete-architecture-guide-multi-agent-orchestration-analysis"},{"title":"LangGraph Tutorial 2026: Build Stateful AI Agents for Enterprise","url":"https://alicelabs.ai/en/insights/langgraph-guide-2026"},{"title":"LangGraph Multi-Agent Architecture: State Control at 100K Requests/Hour | Markaicode","url":"https://markaicode.com/architecture/langgraph-multi-agent-architecture/"},{"title":"LangGraph overview - Docs by LangChain","url":"https://docs.langchain.com/oss/python/langgraph/overview"},{"title":"GitHub - langchain-ai/langgraph: Build resilient agents. · GitHub","url":"https://github.com/langchain-ai/langgraph"},{"title":"The Complete Guide to LangChain & LangGraph: 2025 Updates and Production-Ready AI Frameworks | by Zainab Ikhwan | Artificial Intelligence in Plain English","url":"https://ai.plainenglish.io/the-complete-guide-to-langchain-langgraph-2025-updates-and-production-ready-ai-frameworks-58bdb49a34b6?gi=a9f34a04a3ea"}]

I've completed the web search for your query about LangGraph Platform production deployment architecture, task queue persistence, and 2025 developments. Here's a summary of the key findings:

## LangGraph Platform Overview

LangGraph Platform is a purpose-built infrastructure and management layer for deploying and scaling long-running, stateful agents. As of October 2025, LangGraph Platform has been re-named to "LangSmith Deployment".

## Production Deployment Architecture

LangGraph organizes actions as nodes in a directed graph, enabling tasks like conditional decision-making, parallel execution, and persistent state management. For production deployments, deploying LangGraph systems in production environments requires solid infrastructure and disciplined operational strategies. As workflows grow beyond simple sequential patterns, managing concurrency becomes essential. Fault tolerance is a cornerstone of production deployment, and LangGraph supports automated retries, per-node timeouts, and the ability to pause and resume workflows at specific nodes.

## Task Queue & Persistence

Stateful persistence in LangGraph is handled via checkpointers (SqliteSaver for dev, PostgresSaver for production), enabling agents to resume mid-workflow without re-running completed steps. Additionally, the underlying RedisSaver is designed for low-latency writes and can be sharded by thread_id. In production tests on AWS ElastiCache for Redis 7.2 with cluster mode enabled, linear scaling was confirmed up to 6 shards before network bandwidth became the bottleneck.

An alternative is a stateless microservice architecture using a task queue (Celery or BullMQ) where each agent call is a discrete job with no persistent graph state. While this eliminates Redis checkpoint complexity, it forces the client to manage conversation context manually. As traffic exceeds 10K req/hr, stateless designs require an external session store anyway.

## 2025 Developments

The release of LangGraph 1.0 in October 2025 marked a watershed moment, giving organizations access to a stable, production-grade framework for building AI agents that can persist through failures, maintain state across sessions, and incorporate human oversight. The v1.1 release (December 2025) introduced additional middleware for production reliability, including model retry middleware with configurable exponential backoff and content moderation middleware.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.


===== WebSearch: Vertex AI Agent Engine sessions memory bank architecture 2025 =====
Web search results for query: "Vertex AI Agent Engine sessions memory bank architecture 2025"

Links: [{"title":"Introducing Vertex AI Memory Bank for Agents Long Term Memory | by Abish Pius | Writing in the World of Artificial Intelligence | Oct, 2025 | Medium","url":"https://medium.com/chat-gpt-now-writes-all-my-articles/introducing-vertex-ai-memory-bank-for-agents-long-term-memory-52d5c19a7f3c"},{"title":"Google's Vertex AI 'Memory Bank' and the Industry Shift to Persistent Context -- Virtualization Review","url":"https://virtualizationreview.com/articles/2025/07/09/googles-vertex-ai-memory-bank-and-the-industry-shift-to-persistent-context.aspx"},{"title":"Vertex AI GA Boosts Platform Readiness for Agents - AI CERTs News","url":"https://www.aicerts.ai/news/vertex-ai-ga-boosts-platform-readiness-for-agents/"},{"title":"New Enhanced Tool Governance in Vertex AI Agent Builder | Google Cloud Blog","url":"https://cloud.google.com/blog/products/ai-machine-learning/new-enhanced-tool-governance-in-vertex-ai-agent-builder"},{"title":"Vertex AI Memory Bank in public preview | Google Cloud Blog","url":"https://cloud.google.com/blog/products/ai-machine-learning/vertex-ai-memory-bank-in-public-preview"},{"title":"Agent Governance Comes of Age: Google Cloud Reinforces Vertex AI Guardrails – HyperFRAME Research","url":"https://hyperframeresearch.com/2025/12/24/agent-governance-comes-of-age-google-cloud-reinforces-vertex-ai-guardrails/"},{"title":"Manage your Agent User Sessions with ADK and Vertex AI Memory Engine | by Bhandari Haren | Google Cloud - Community | Medium","url":"https://medium.com/google-cloud/manage-your-user-sessions-with-adk-and-vertex-ai-memory-engine-447c53b189df"},{"title":"Architecting Agentic Memory on Google Cloud with Vertex AI Agent Engine | by Sangalo Mwenyinyo | Medium","url":"https://medium.com/@mwenyinyo/architecting-agentic-memory-on-google-cloud-with-vertex-ai-agent-engine-ee3df9842e87"},{"title":"How to build and deploy a portable AI agent that uses a managed memory service – Richard Seroter's Architecture Musings","url":"https://seroter.com/2025/10/14/how-to-build-and-deploy-a-portable-ai-agent-that-uses-a-managed-memory-service/"},{"title":"How to Configure Agent Memory with Vertex AI Agent Engine Sessions","url":"https://oneuptime.com/blog/post/2026-02-17-how-to-configure-agent-memory-with-vertex-ai-agent-engine-sessions-and-memory-bank/view"}]

Based on the search results, here's a comprehensive overview of Vertex AI Agent Engine sessions and Memory Bank architecture in 2025:

## Overview

On July 8, 2025, Google announced the public preview of Memory Bank, a new capability within the cloud-based Vertex AI Agent Engine designed to solve one of the core limitations of conversational agents: lack of persistent memory. Memory Bank and Agent Engine sessions have reached general availability to enable persistent session and memory management for production agent workloads.

## Architecture Components

The system uses a two-tiered memory approach:

**Sessions (Short-term Memory):** Sessions persist chronological interactions, enabling contextual continuity across requests. Sessions handle short-term, within-conversation memory. When a user starts a chat, a session is created.

**Memory Bank (Long-term Memory):** Memory Bank is a managed, persistent storage system that allows your Vertex AI agent to generate, refine, and retrieve long-term memories across user sessions. Memory Bank extracts salient facts and stores them for cross-session retrieval.

## Memory Extraction Process

At the end of a session (or even during it), the Agent Engine can asynchronously send the conversation history to the Memory Bank. The Memory Bank then uses a Gemini model to analyze the transcript and extract key facts, preferences, and context.

## Key Features

This product is powered by Google Cloud AI Research's novel research method (accepted by ACL 2025), using a topic-based approach that sets a new standard for how agents learn and recall information.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.


===== WebSearch: Vercel AI SDK 5 agent loop control stopWhen prepareStep abstraction =====
Web search results for query: "Vercel AI SDK 5 agent loop control stopWhen prepareStep abstraction"

Links: [{"title":"AI SDK 5 - Vercel","url":"https://vercel.com/blog/ai-sdk-5"},{"title":"Agents: Loop Control","url":"https://ai-sdk.dev/docs/agents/loop-control"},{"title":"Loop Control - AI SDK","url":"https://mintlify.wiki/vercel/ai/agents/loop-control"},{"title":"Building human-in-the-loop agents for community moderation with durable workflows | Vercel Knowledge Base","url":"https://vercel.com/kb/guide/building-human-in-the-loop-agents-for-community-moderation-with-durable-workflows"},{"title":"What is Vercel AI SDK? | VoltAgent","url":"https://voltagent.dev/blog/vercel-ai-sdk/"},{"title":"Vercel AI SDK v5 Agent Patterns: stopWhen, prepareStep, ...","url":"https://callsphere.ai/blog/vw3g-vercel-ai-sdk-v5-agent-patterns-stopwhen-preparestep"},{"title":"The Anatomy of an Agent Loop | Steve Kinney","url":"https://stevekinney.com/writing/agent-loops"},{"title":"Building AI agents with Vercel AI SDK | by Željko Šević | Jun, 2026 | Medium","url":"https://medium.com/@sevicdev/building-ai-agents-with-vercel-ai-sdk-1bd0310854c2"},{"title":"Agents: Building Agents","url":"https://ai-sdk.dev/docs/agents/building-agents"},{"title":"Building AI agents with Vercel AI SDK - DEV Community","url":"https://dev.to/zsevic/building-ai-agents-with-vercel-ai-sdk-48pa"}]

Based on the search results, I found comprehensive information about Vercel AI SDK 5's agent loop control features. Here's what I found:

## Overview

The AI SDK provides built-in loop control through two parameters: stopWhen for defining stopping conditions and prepareStep for modifying settings (model, tools, messages, and more) between steps.

## stopWhen Parameter

The stopWhen parameter controls when to stop execution when there are tool results in the last step. By default, agents stop after 20 steps using isStepCount(20). This default is a safety measure to prevent runaway loops that could result in excessive API calls and costs.

When you provide stopWhen, the agent continues executing after tool calls until a stopping condition is met. When the condition is an array, execution stops when any of the conditions are met.

## prepareStep Abstraction

While stopWhen keeps your agent running, prepareStep allows you to control the settings for each step. prepareStep can be used to compress or filter context to stay within limits or filter out irrelevant tokens, switch between models based on task complexity, adapt system instructions for different tasks, enable/disable tools as needed, and force specific tool usage (or none) when required.

The prepareStep hook runs before each LLM call and can dynamically change the model, tools, messages, or tool choice per-step.

Use prepareStep to mutate the message state that will be used by later steps. This is useful for compaction, and you decide when compaction should happen.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.


===== WebSearch: Diagrid checkpoints not durable execution LangGraph CrewAI ADK production comparison =====
Web search results for query: "Diagrid checkpoints not durable execution LangGraph CrewAI ADK production comparison"

Links: [{"title":"Why Checkpoints Aren't Durable Execution: LangGraph","url":"https://www.diagrid.io/blog/checkpoints-are-not-durable-execution-why-langgraph-crewai-google-adk-and-others-fall-short-for-production-agent-workflows"},{"title":"Take CrewAI to Production | Durable AI Agents | Diagrid","url":"https://www.diagrid.io/solutions/crewai-production"},{"title":"Take LangGraph to Production | Durable AI Agents | Diagrid","url":"https://www.diagrid.io/solutions/langgraph-production"},{"title":"Diagrid - Durable Workflows for AI Agents","url":"https://www.diagrid.io/solutions"},{"title":"Build Robust Agentic Workflows with Dapr & Dapr Agents | Diagrid Videos","url":"https://www.diagrid.io/videos/build-robust-agentic-workflows-with-dapr-dapr-agents"},{"title":"Ship Reliable AI Agents and Workflows to Production | Diagrid Docs","url":"https://docs.diagrid.io/"},{"title":"Still Not Durable: MS Agent Framework & Strands","url":"https://www.diagrid.io/blog/still-not-durable-how-microsoft-agent-framework-and-strands-agents-repeat-the-same-mistake"},{"title":"Durable execution - Docs by LangChain","url":"https://docs.langchain.com/oss/python/langgraph/durable-execution"},{"title":"What is AI Orchestration? Workflows for Durable AI Agents | Diagrid","url":"https://www.diagrid.io/ai-orchestration"},{"title":"diagrid · PyPI","url":"https://pypi.org/project/diagrid/"}]

Based on the search results, here's a comprehensive overview of the topic:

## Key Findings

Checkpointing is not production-grade durability. It's a low-level building block that shifts the hard problems onto you.

### The Core Problem

Frameworks like LangGraph, CrewAI, Google ADK, Strands and more have made it remarkably easy to prototype multi-step agent workflows, but what they actually give you is a save point — a snapshot of state that you, the developer, are responsible for detecting the need to use, manually triggering, and coordinating at scale to avoid duplicate work.

### Specific Framework Limitations

**LangGraph:** Checkpoints don't detect failures, don't trigger automatic recovery, and don't coordinate across instances. If two processes try to resume the same thread_id simultaneously (entirely possible in a distributed system recovering from a partial failure), LangGraph has no built-in coordination to prevent both from executing.

**CrewAI:** CrewAI has task replay and the @persist decorator, but no failure detection or automatic recovery.

**Google ADK:** Google ADK has SessionService and invocation_id-based resume.

### Why Architecture Changes Are Needed

LangGraph, CrewAI, Google ADK and others are not on a trajectory toward durable execution. They would need to fundamentally rearchitect their runtimes to provide it.

### Diagrid's Approach

Diagrid addresses this gap by persisting state to a remote store after every activity, surviving process crashes, OOM kills, deployments, and infrastructure failures. Dapr's actor placement service ensures each workflow is processed by exactly one instance, scaling horizontally without duplicate executions or race conditions.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.


===== WebSearch: Google ADK Agent Development Kit session memory runner architecture =====
Web search results for query: "Google ADK Agent Development Kit session memory runner architecture"

Links: [{"title":"Memory - Agent Development Kit (ADK)","url":"https://google.github.io/adk-docs/sessions/memory/"},{"title":"Remember this: Agent state and memory with ADK | Google Cloud Blog","url":"https://cloud.google.com/blog/topics/developers-practitioners/remember-this-agent-state-and-memory-with-adk"},{"title":"Google ADK — Part 2: Tools, Sessions, Memory & Multi-Agent Systems | by Rahmat Fajri | Medium","url":"https://rfajri.medium.com/google-adk-part-2-tools-sessions-memory-multi-agent-systems-eb67bb257c2b"},{"title":"Adding Sessions and Memory to Your AI Agent with Agent Development Kit (ADK) - DEV Community","url":"https://dev.to/marianocodes/adding-sessions-and-memory-to-your-ai-agent-with-agent-development-kit-adk-31ap"},{"title":"Build Long-running AI agents that pause, resume, and never lose context with ADK - Google Developers Blog","url":"https://developers.googleblog.com/build-long-running-ai-agents-that-pause-resume-and-never-lose-context-with-adk/"},{"title":"Google Agent Development Kit (ADK): Sessions, Memory, and Runtime | by DhanushKumar | Stackademic","url":"https://medium.com/@danushidk507/google-agent-development-kit-adk-sessions-memory-and-runtime-705c0730892a"},{"title":"Google ADK - Mem0","url":"https://docs.mem0.ai/integrations/google-ai-adk"},{"title":"Exploring Google’s Agent Development Kit (ADK) | by Deven Joshi | Medium","url":"https://medium.com/@d3xvn/exploring-googles-agent-development-kit-adk-71a27a609920"},{"title":"Building AI Agents with Google’s ADK – Leonie Monigatti","url":"https://www.leoniemonigatti.com/blog/building-ai-agents-with-google-adk.html"},{"title":"Google ADK - Sessions, state, and memory | Ravikanth Chaganti","url":"https://ravichaganti.com/blog/google-adk-sessions-state-and-memory/"}]

Based on the search results, here's comprehensive information about Google ADK's session memory and runner architecture:

## Session Memory Architecture

Every user interaction with an ADK agent gets a session, and that session is managed by the ADK SessionService. Each session contains important fields, like the session ID, user ID, event history (the conversation thread), and the state.

Short-term memory most often refers to the conversation history of a session. The conversation history not only records the user queries and the agent's responses, but also all tool interactions.

### Memory Service Options

The default way is in memory, by using an InMemoryMemoryService. Here, all sessions are stored raw (with the full conversation thread), and can be retrieved by the agent in further sessions using a basic keyword search.

ADK provides a way to store long-term memories persistently outside the ADK runtime, and that's with a VertexAIMemoryBankService. This memory service uses Vertex AI Memory Bank (Preview) to intelligently store and retrieve memories from past user interactions.

## Runner Architecture

At its heart, the ADK Runtime operates on an Event Loop. This loop facilitates a back and-forth communication between the Runner component and your defined "Execution Logic" (which includes your Agents, the LLM calls they make, Callbacks, and Tools).

### Event Loop Flow

An event loop is at the heart of the ADK runtime and facilitates the communication between the Runner component and the agent execution. When a user prompt arrives, the Runner hands it over to the agent for processing. The agent runs until it has something to yield, at which point it emits an event. The Runner receives the event, processes any associated actions, calls the session service to append the event to the current state, and forwards the event. After the Runner completes event processing, the agent resumes from where it was paused and continues this loop until it has no more events to yield.

User Input flows through the Runner, the Event Loop Kicks In with Agent Execution where the agent begins reasoning and decides which tools to use. The agent consults the LLM to plan its next move and executes a tool to take a real-world action. Every action and result is wrapped as an Event. These events flow through ADK's internal services, updating the current conversation history and state through the Session Service, and archiving important bits for long-term recall through the Memory Service. The final output streams back to the user in real-time.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.


===== WebFetch: https://docs.langchain.com/oss/python/langgraph/durable-execution =====
# LangGraph Durability Modes: Information Not Available

The provided documentation does not contain detailed information about LangGraph durability modes (sync/async/exit). 

The page covers:
- **Checkpointers** for short-term, thread-scoped memory
- **Stores** for long-term, cross-thread memory
- Basic quickstart examples using `InMemorySaver` and `InMemoryStore`
- Troubleshooting for common issues like thread_id length and checkpoint accumulation

**What's missing from this excerpt:**
- Specific durability mode definitions or guarantees
- Performance tradeoffs between sync/async/exit approaches
- Internal checkpointer mechanics at the code level
- Determinism requirements for resumption
- Task/interrupt behavior specifications during resume operations

**Recommendation:** To find this technical depth, consult:
1. The full checkpointers guide: `/oss/python/langgraph/checkpointers`
2. The stores guide: `/oss/python/langgraph/stores`
3. The documentation index at `https://docs.langchain.com/llms.txt`

The current page directs readers to these fuller resources but doesn't include the durability mode details you're seeking.


===== WebFetch: https://docs.restate.dev/ai/patterns/durable-agents =====
# Restate's Durable Agent Architecture

## Core Design Principles

Restate separates concerns into two components: a **Restate Server** handling orchestration and resilience, and **Agent Services** using the SDK for durability. The agent itself is "a regular function, a handler, that makes LLM calls, executes tools, and coordinates work."

## Journaling & Replay Mechanism

The system works through **step-level journaling**. When execution occurs, "every step is recorded in a journal, so if the process crashes, the agent picks up exactly where it left off."

Recovery follows this pattern:
1. Restate detects failure and restarts the handler
2. "Completed steps are replayed from the journal (no re-execution)"
3. Execution resumes from the first incomplete step

This approach ensures LLM responses aren't "re-fetched on recovery" and tool side effects avoid duplication—critical for preventing "double bookings" or "duplicate emails."

## Agent Loop Implementation

Rather than prescribing a specific loop pattern, Restate enables flexibility. Developers "control the loop" by calling the LLM, processing tool responses, and repeating until completion. Each step—LLM calls and tool executions—wraps in durable primitives like `ctx.run()`.

## Key Architectural Difference

Unlike checkpoint-based systems that save full state snapshots, Restate uses **event journaling**: recording the outcome of each discrete operation. This means "side effects are executed exactly once" through deterministic replay, not state restoration.

Human-in-the-loop integration occurs through the Restate UI, which displays "the step-by-step execution trace," enabling inspection and intervention points during agent execution.
