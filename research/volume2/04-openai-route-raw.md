# OpenAI 路线（半程原始检索材料，agent 卡死于 WebFetch temporal.io）

未经该路 agent 收尾综合，为 WebSearch/WebFetch 原始返回。综合结论已并入 volume2-outline.md。

---


===== WebSearch: OpenAI "A practical guide to building agents" PDF design principles =====
Web search results for query: "OpenAI "A practical guide to building agents" PDF design principles"

Links: [{"title":"OpenAI - A Practical Guide To Building Agents | PDF | Databases | Customer Relationship Management","url":"https://www.scribd.com/document/859991951/OpenAI-a-Practical-Guide-to-Building-Agents"},{"title":"Principles of Building AI Agents PDF: A Comprehensive Guide to Designing and Deploying AI Agents - Lawhustle","url":"https://golawhustle.com/blogs/principles-building-ai-agents-pdf"},{"title":"A guide to building AI agents by OpenAI [PDF] | DeepakNess","url":"https://deepakness.com/raw/guide-to-building-ai-agents/"},{"title":"OpenAI’s — A Practical Guide To Building Agents — Breakdown - zubair - Medium","url":"https://medium.com/@zubairspov/openais-a-practical-guide-to-building-agents-breakdown-9c99ca50dcda"},{"title":"A Practical Guide to Building Agents by OpenAI","url":"https://aiengineerguide.com/blog/practical-guide-to-building-agents-openai/"},{"title":"A practical guide to building agents | OpenAI","url":"https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/"},{"title":"A practical guide to building agents","url":"https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf"},{"title":"A-Practical-Guide-to-Building-Agents/a-practical-guide-to-building-agents.pdf at main · ai-agents-simplified/A-Practical-Guide-to-Building-Agents","url":"https://github.com/AI-Agents-Simplified/A-Practical-Guide-to-Building-Agents/blob/main/a-practical-guide-to-building-agents.pdf"}]

Based on the search results, here's what I found about OpenAI's "A Practical Guide to Building Agents" PDF:

## Overview

This is a comprehensive guide to designing, orchestrating, and deploying AI agents—covering use cases, model selection, tool design, guardrails, and multi-agent patterns. The guide provides practical insights for product and engineering teams on building agents powered by large language models (LLMs).

## Key Design Principles

The guide emphasizes several core design principles:

1. **Component Design**: The key principle is to keep components flexible, composable, and driven by clear, well-structured prompts.

2. **Tool Integration**: Tools extend your agent's capabilities by using APIs from underlying applications or systems, with each tool having a standardized definition, enabling flexible, many-to-many relationships between tools and agents.

3. **Multi-Agent Orchestration**: The guide highlights two broadly applicable patterns: the Manager pattern where a central "manager" agent coordinates multiple specialized agents via tool calls, and the Decentralized pattern where multiple agents operate as peers, handing off tasks to one another based on their specializations.

## Content Coverage

The ebook covers topics like what an AI agent is, when you should create an agent, design foundations, multi-agent systems, and guardrails.

The official PDF is available at: https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.


===== WebSearch: OpenAI Agents SDK handoffs guardrails sessions tracing architecture design =====
Web search results for query: "OpenAI Agents SDK handoffs guardrails sessions tracing architecture design"

Links: [{"title":"Agents SDK | OpenAI API","url":"https://developers.openai.com/api/docs/guides/agents"},{"title":"OpenAI Agents SDK","url":"https://openai.github.io/openai-agents-python/"},{"title":"Building Multi-Agents with OpenAI Agent SDK | by Johni Douglas Marangon | Medium","url":"https://medium.com/@johnidouglasmarangon/building-multi-agents-with-openai-agent-sdk-8dd9ecfb7663"},{"title":"Handoffs - OpenAI Agents SDK","url":"https://openai.github.io/openai-agents-python/handoffs/"},{"title":"OpenAI Agents SDK: Practical Guide to Building Agent Workflows | UI Bakery Blog","url":"https://uibakery.io/blog/openai-agents-sdk"},{"title":"Mastering the OpenAI Agents SDK: A Field Guide for Busy Developers & AI VPs &mdash; Cohorte Engineering Blog","url":"https://cohorte.co/blog/mastering-the-openai-agents-sdk-a-field-guide-for-busy-developers-ai-vps"},{"title":"OpenAI Agents SDK Deep Dive: Agents, Tools, Handoffs, and Guardrails Explained — Openai agents sdk documentation 2026 tools handoffs tracing | CallSphere Blog","url":"https://callsphere.ai/blog/openai-agents-sdk-deep-dive-agents-tools-handoffs-guardrails-2026"},{"title":"OpenAI Agent SDK Features, Tools and Developer Insights","url":"https://mem0.ai/blog/openai-agents-sdk-review"},{"title":"OpenAI Agents SDK Prompting Guide: Tools, Handoffs, Guardrails, Tracing (2026) | SurePrompts","url":"https://sureprompts.com/blog/openai-agents-sdk-prompting-guide"},{"title":"OpenAI Agents SDK Explained: Architecture & How It Works","url":"https://www.botonomy.ai/blog/agentic-ai/open-ai-agents-sdk/"}]

Based on the search results, here's a comprehensive overview of the OpenAI Agents SDK architecture and its key components:

## Core Architecture

The OpenAI Agents SDK enables you to build agentic AI apps in a lightweight, easy-to-use package with very few abstractions. It's a production-ready upgrade of the previous experimentation for agents, Swarm.

## Key Components

**Agents**: Agents are LLMs equipped with instructions and tools, and agents as tools/handoffs allow agents to delegate to other agents for specific tasks.

**Handoffs**: Handoffs allow an agent to delegate tasks to another agent, which is particularly useful in scenarios where different agents specialize in distinct areas. The Agents SDK runner performs the tool loop, switches agents after handoffs, and stops when the run finishes or pauses for approval.

**Guardrails**: Guardrails run input validation and safety checks in parallel with agent execution, and fail fast when checks do not pass. Guardrails validate inputs and outputs before and after agent execution, run in parallel with the agent and can either filter content (validation guardrails) or halt execution entirely (tripwire guardrails).

**Sessions**: Sessions are a persistent memory layer for maintaining working context within an agent loop.

**Tracing**: Tracing is built-in for visualizing, debugging, and monitoring workflows, with support for the OpenAI suite of evaluation, fine-tuning, and distillation tools.

## Execution Model

When you call `Runner.run()`, the SDK enters a while-loop that repeatedly calls the active agent's model, executes tool calls, processes handoffs, and checks guardrails — until the agent produces a final output or hits `max_turns`.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.


===== WebSearch: OpenAI Assistants API deprecation sunset Responses API migration 2026 =====
Web search results for query: "OpenAI Assistants API deprecation sunset Responses API migration 2026"

Links: [{"title":"Deprecations | OpenAI API","url":"https://developers.openai.com/api/docs/deprecations"},{"title":"Assistants migration guide | OpenAI API","url":"https://developers.openai.com/api/docs/assistants/migration"},{"title":"OpenAI Assistants API will be deprecated in August 2026, what happens to Azure OpenAI? - Microsoft Q&A","url":"https://learn.microsoft.com/en-us/answers/questions/5571874/openai-assistants-api-will-be-deprecated-in-august"},{"title":"OpenAI Assistants API Shutdown: The 2026 Migration Guide | ClonePartner Blog","url":"https://clonepartner.com/blog/openai-assistants-api-shutdown-the-2026-migration-guide/"},{"title":"The OpenAI Assistants API in 2026: A Field Guide to the Shutdown, the Migration, and What Comes Next | SocialCrawl","url":"https://www.socialcrawl.dev/blog/openai-assistants-api-2026-shutdown-migration-guide"},{"title":"Assistants API beta deprecation — August 26, 2026 sunset - Announcements - OpenAI Developer Community","url":"https://community.openai.com/t/assistants-api-beta-deprecation-august-26-2026-sunset/1354666"},{"title":"OpenAI Assistants API Deprecation: Migration Guide (Updated January 28, 2026)","url":"https://ragwalla.com/docs/guides/openai-assistants-api-deprecation-2026-migration-guide-wire-compatible-alternatives"},{"title":"Assistants API beta deprecation — August 26, 2026 sunset - Page 2 - Announcements - OpenAI Developer Community","url":"https://community.openai.com/t/assistants-api-beta-deprecation-august-26-2026-sunset/1354666?page=2"},{"title":"OpenAI Deprecates Three Image APIs by December 2026 | AI Weekly","url":"https://aiweekly.co/alerts/openai-deprecates-three-image-apis-by-december-2026"},{"title":"OpenAI's Assistants API is Deprecated: Migrate to the New Responses API","url":"https://syntackle.com/blog/openai-assistants-to-responses-api/"}]

## Search Results Summary

Based on the web search for "OpenAI Assistants API deprecation sunset Responses API migration 2026", here are the key findings:

### Deprecation Timeline
OpenAI notified developers on August 26th, 2025 of the Assistants API's deprecation and removal from the API one year later, on August 26, 2026. The API will shut down on August 26, 2026.

### Migration to Responses API
After achieving feature parity in the Responses API, OpenAI deprecated the Assistants API, which will shut down on August 26, 2026. OpenAI is moving from the Assistants API to the new Responses API for a simpler and more flexible mental model where responses are simpler—send input items and get output items back—and you also get better performance and new features like deep research, MCP, and computer use.

### Key Changes
Assistants become Prompts (dashboard-only), Threads become Conversations, Runs become Responses, and Run Steps become Items. Assistants were persistent API objects that bundled model choice, instructions, and tool declarations—created and managed entirely through the API, while their replacement, prompts, can only be created in the dashboard.

### Hard Cutoff
On August 26, 2026, all Assistants API endpoints are permanently removed, and requests to /v1/assistants, /v1/threads, and related endpoints will fail. OpenAI has stated there is no extension option.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.


===== WebSearch: openai codex CLI Rust sandbox Seatbelt Landlock approval modes github =====
Web search results for query: "openai codex CLI Rust sandbox Seatbelt Landlock approval modes github"

Links: [{"title":"OpenAI Codex CLI: Official Description & Setup Guide (Updated 2026-02) - SmartScope","url":"https://smartscope.blog/en/generative-ai/chatgpt/openai-codex-cli-comprehensive-guide/"},{"title":"Codex CLI is Going Native · openai/codex · Discussion #1174","url":"https://github.com/openai/codex/discussions/1174"},{"title":"codex/AGENTS.md at main · openai/codex","url":"https://github.com/openai/codex/blob/main/AGENTS.md"},{"title":"OpenAI Codex CLI: The Rust-Powered Terminal Agent Taking on Claude Code - Botmonster Tech","url":"https://botmonster.com/posts/openai-codex-cli-rust-powered-ai-agent/"},{"title":"Sandbox – Codex | OpenAI Developers","url":"https://developers.openai.com/codex/concepts/sandboxing"},{"title":"Agent approvals & security – Codex | OpenAI Developers","url":"https://developers.openai.com/codex/agent-approvals-security"},{"title":"Codex CLI Guide: OpenAI's Terminal Agent for GPT-5.5 (2026)","url":"https://www.aimadetools.com/blog/codex-cli-complete-guide/"},{"title":"all commands in sandbox mode fail and need approval · Issue #3140 · openai/codex","url":"https://github.com/openai/codex/issues/3140"},{"title":"OpenAI Codex CLI -- Sandbox Analysis Report | Agent Safehouse","url":"https://agent-safehouse.dev/docs/agent-investigations/codex"},{"title":"Sandboxing - Codex CLI","url":"https://mintlify.wiki/openai/codex/concepts/sandboxing"}]

Based on the search results, here's what I found about OpenAI Codex CLI's sandboxing architecture with Rust, Seatbelt, and Landlock:

## Overview

OpenAI Codex CLI is an open-source Rust-built terminal coding agent, with Rust accounting for roughly 95% of the codebase as of early 2026.

## Sandboxing Implementation

Codex pairs GPT-5.4's 272K default context window (configurable up to 1M tokens) with operating-system-level sandboxing via Apple Seatbelt on macOS and Landlock/seccomp on Linux.

### Platform-Specific Details:

**macOS:**
macOS uses Seatbelt policies and runs commands using sandbox-exec with a profile (-p) that corresponds to the --sandbox mode selected. When restricted read access enables platform defaults, Codex appends a curated macOS platform policy (instead of broadly allowing /System) to preserve common tool compatibility.

**Linux:**
Linux uses bwrap plus seccomp by default. On Linux, Codex builds its own CLI that uses Landlock/seccomp via the linux-sandbox helper.

**Windows:**
Windows uses the Linux sandbox implementation when running in Windows Subsystem for Linux 2 (WSL2). WSL1 was supported through Codex 0.114; starting in 0.115, the Linux sandbox moved to bwrap, so WSL1 is no longer supported.

## Approval Modes

In the Auto preset (for example, --sandbox workspace-write --ask-for-approval on-request), Codex can read files, make edits, and run commands in the working directory automatically. Codex asks for approval to edit files outside the workspace or to run commands that require network access.

For more detailed information, you can view the source code in the [OpenAI Codex GitHub repository](https://github.com/openai/codex).


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.


===== WebSearch: Temporal OpenAI Agents SDK durable execution integration 2025 =====
Web search results for query: "Temporal OpenAI Agents SDK durable execution integration 2025"

Links: [{"title":"Production-ready agents with the OpenAI Agents SDK + Temporal | Temporal","url":"https://temporal.io/blog/announcing-openai-agents-sdk-integration"},{"title":"Durable Agent with Tools - OpenAI Agents SDK | Temporal Platform Documentation","url":"https://docs.temporal.io/ai-cookbook/openai-agents-sdk-python"},{"title":"Temporal and OpenAI Launch AI Agent Durability with Public Preview Integration - InfoQ","url":"https://www.infoq.com/news/2025/09/temporal-aiagent/"},{"title":"Temporal | Pydantic Docs","url":"https://pydantic.dev/docs/ai/integrations/durable_execution/temporal/"},{"title":"Building durable agents with Temporal and AI SDK by Vercel | Temporal","url":"https://temporal.io/blog/building-durable-agents-with-temporal-and-ai-sdk-by-vercel"},{"title":"Introducing Temporal and agentic sandboxes: The OpenAI agents SDK | Temporal","url":"https://temporal.io/blog/introducing-temporal-and-agentic-sandboxes-openai-agents-sdk"},{"title":"OpenAI Agents SDK Integration is now in Public Preview | Temporal","url":"https://temporal.io/changelog/open-ai-agents-sdk-integration-pp"},{"title":"Durable Digest: August 2025 | Temporal","url":"https://temporal.io/blog/durable-digest-august-2025"},{"title":"Temporal and OpenAI Launch Integration for Scalable AI Agent Production","url":"https://techintelpro.com/news/temporal-and-openai-launch-integration-for-scalable-ai-agent-production"},{"title":"Temporal + OpenAI Sandbox: Production AI Workflows","url":"https://www.xgrid.co/resources/temporal-openai-agents-sdk-sandbox-production-ai-workflows/"}]

Based on the search results, here's a comprehensive overview of the Temporal OpenAI Agents SDK durable execution integration:

## Overview

OpenAI and Temporal have teamed up to add Durable Execution to agents built using OpenAI's Agents SDK, with the integration released in Public Preview. Temporal unveiled a public preview integration with the OpenAI Agents SDK, introducing durable execution capabilities to AI agent workflows built using OpenAI's framework.

## Key Capabilities

AI agents built with the OpenAI Agents SDK will stand up to production challenges, with rate-limited LLMs automatically progressing when capacity is available, sporadic network connectivity being handled through retries, and crashed long-running tasks resuming from where they left off, saving compute and token costs.

## How It Works

The integration works by wrapping OpenAI agents inside Temporal workflows, where reasoning loops and tool calls are orchestrated as discrete steps, with state persisted in Temporal's event history log backed by scalable databases like Cassandra, MySQL, or PostgreSQL, and each external interaction implemented as a Temporal Activity.

## Broader Ecosystem Integration

Temporal is becoming the durability layer for the entire agent ecosystem, with integrations with Pydantic AI, Vercel's AI SDK, and Amazon Bedrock Strands, with more coming soon.

## Recent Expansion

OpenAI shipped sandbox support in the Agents SDK allowing agents to execute code, manipulate files, and run shell commands inside isolated sandbox environments powered by providers like Modal, Daytona, Docker, and E2B, with Temporal working with OpenAI's engineering team to build a Temporal extension for this release.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.


===== WebFetch: https://developers.openai.com/codex/agent-approvals-security =====
REDIRECT DETECTED: The URL redirects to a different host.

Original URL: https://developers.openai.com/codex/agent-approvals-security
Redirect URL: https://learn.chatgpt.com/docs/agent-approvals-security
Status: 308 Permanent Redirect

To complete your request, I need to fetch content from the redirected URL. Please use WebFetch again with these parameters:
- url: "https://learn.chatgpt.com/docs/agent-approvals-security"
- prompt: "Extract all details about approval modes/policies (on-request, on-failure, never, untrusted, etc.), how approval interacts with the sandbox layers, escalation flow when a sandboxed command fails, and the security model. Quote specific mode names and the decision logic."


===== WebFetch: https://developers.openai.com/codex/concepts/sandboxing =====
stream has been aborted


===== WebFetch: https://openai.github.io/openai-agents-python/handoffs/ =====
# Handoffs Design Details

## Implementation as Tools

Handoffs function as LLM-callable tools. As stated: "Handoffs are represented as tools to the LLM. So if there's a handoff to an agent named `Refund Agent`, the tool would be called `transfer_to_refund_agent`."

## Core Components

**Agent Registration**: Agents expose handoffs through a `handoffs` parameter accepting either plain Agent instances or customized `Handoff` objects.

**Tool Customization**: The `handoff()` function enables configuration including:
- `tool_name_override`: Replaces the default naming pattern
- `tool_description_override`: Customizes the tool's description
- `on_handoff`: A callback executed when the handoff triggers, receiving agent context and optional parsed input
- `input_type`: Defines the schema for handoff arguments using Pydantic models

## Input Handling

**input_type Purpose**: Captures model-generated metadata at handoff time (reason, priority, summary) without replacing the receiving agent's main input or controlling destination selection.

**Input Filters**: The `input_filter` function receives `HandoffInputData` containing conversation history, pre-handoff items, and new items, returning modified `HandoffInputData` to control what the next agent observes.

## Nested Handoff History

When `RunConfig.nest_handoff_history` is enabled, prior conversations collapse into a single assistant summary within `<CONVERSATION HISTORY>` blocks, supporting multiple sequential handoffs.

## Recommended Practices

The SDK provides `RECOMMENDED_PROMPT_PREFIX` from `agents.extensions.handoff_prompt` to ensure models understand handoff semantics properly.
