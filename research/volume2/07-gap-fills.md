# 缺口补抓（主会话直连，curl 带 30s 超时）

2026-07-10 · 补 workflow 卡死未完成的四个缺口，另有两处意外收获。

## 1. Temporal × OpenAI Agents SDK 集成机制（原 OpenAI 路缺口）

来源：https://temporal.io/blog/announcing-openai-agents-sdk-integration 【官方】

- 集成的关键一步：OpenAI 把 `Runner` 改成 abstract base class，Temporal 提供自己的 Runner 实现——**每次 agent/模型调用被隐式包成一个 Temporal Activity**，开发者代码里"nary a mention of a Temporal Activity"。
- 编排跑在 Workflow 里：Temporal 记录每个 Activity 的调用参数、完成状态、返回值；崩溃后重放已完成 Activity 的缓存结果，从第一个未完成步骤继续。
- 卖点原话："code the happy path, and Temporal does the error handling for you"；甚至支持"修 bug 后继续执行运行中的 app"。
- agentic loop 在 Workflow 里就是普通 Python while 循环，`invoke_model` / `invoke_tool` 两个 Activity 交替。
- 教程用法：§五 durable execution 谱系——"把 agent loop 变 durable 的最小改动面"实例；印证 guide 4.2 "外部交互全部 Activity 化"。

## 2. Codex 沙箱/审批/持久化 一手仓库材料（原 OpenAI 路缺口）

developers.openai.com 直连 SSL 失败（curl 35），改从 github.com/openai/codex 仓库 README 取证，反而更一手。【官方】

### execpolicy（codex-rs/execpolicy/README.md）
- 策略引擎围绕 `prefix_rule(pattern, decision, justification, match, not_match)`：decision 三档 **allow / prompt / forbidden**（默认 allow）。
- **match / not_match 是加载期验证的示例调用**——"think of them as unit tests"。策略规则自带测试，加载时就验证规则真的匹配/不匹配预期命令。可与"破坏验证（sabotage validation）"并列讲：检测器/策略上线必须证明自己会触发。
- forbidden 规则的 justification 建议附替代方案（如 "Use `jj` instead of `git`"）——拒绝要给出路，呼应"错误消息 actionable"。

### shell-escalation（codex-rs/shell-escalation/README.md）
- 拦截 `execve(2)`，经共享 fd 走协议，服务端三应答：**Run**（沙箱内执行）/ **Escalate**（把 fd 转发出去在沙箱外忠实执行，完成后回传 exit code）/ **Deny**（打印错误退出 1）。
- 为此维护了一个打过 `EXEC_WRAPPER` 补丁的 zsh。
- 教程用法：§八 沙箱与审批分层——"沙箱内默认执行、需要时显式升级、升级有协议有审计"的三态流。

### linux-sandbox + core（README）
- bubblewrap 是默认文件系统沙箱：`--ro-bind / /` **默认整个文件系统只读**，writable roots 用 `--bind` 分层打开；`.git`、resolved `gitdir:`、`.codex` 在可写根下**重新以只读绑定**保护。
- 附加 `PR_SET_NO_NEW_PRIVS` + seccomp 网络过滤（进程内）。
- 分层覆盖语义：`/repo=write, /repo/a=none, /repo/a/b=write` 按路径特异性顺序生效——窄的可写子路径能重新打开宽的只读/拒绝父路径，更窄的拒绝仍然赢。
- 降级链有告警：bwrap 缺失→用捆绑的 bwrap 并走正常通知路径发启动警告；无法创建 user namespace→启动警告而不是等运行时沙箱失败（fail-fast 实例）；WSL1 直接拒绝进入沙箱路径。
- macOS 走 Seatbelt（/usr/bin/sandbox-exec），workspace-write 策略同样保 `.git`/`.codex` 只读。

### rollout-trace（codex-rs/rollout-trace/README.md）——意外收获
- 核心设计选择原话："**observe first, interpret later**"。热路径不建语义图，只写有序原始事件 + payload 引用（trace.jsonl + payloads/*.json + manifest.json）；离线 reducer（replay_bundle，确定性）重建 state.json 语义图（threads/turns、模型可见对话、runtime objects、interaction edges）。
- 明确声明"Rollout tracing is not telemetry"——只写本地、不上传，内容敏感。
- 教程用法：§九可观测性——与入门卷 stub/body 物理分离同构的业界实现；"热路径最小开销 + 离线重建"是 trace 架构的一条主流路线。

## 3. OTel GenAI semconv 现状（原生产运维路缺口）

来源：github.com/open-telemetry/semantic-conventions-genai（已从主 semconv 仓库迁出为独立仓库）【官方】

- 整体 Status 仍为 **Development**（README 与各 span 页均标注）。
- Span 分类比二手转述丰富：`create_agent` / `invoke_agent`（client 与 internal 两变体）/ `execute_tool` / `invoke_workflow` / `plan` / `memory` / `retrieval` / `inference` / `embeddings`（见 docs/gen-ai/ 与 reference/reports/）。
- 内容捕获（gen_ai.input.messages / output.messages / system_instructions / tool-definitions）有 JSON schema 约束，span 上可记 JSON 字符串、事件上必须结构化；默认关闭（敏感）。
- 另有厂商专属约定（Anthropic/OpenAI/Bedrock/Azure）与 **MCP 专门约定**（mcp.md）。
- 教程用法：§九——引用时明确"仍在 Development、独立仓库"，属性表写作时从该仓库 gen-ai-agent-spans.md 逐字取。

## 4. context anxiety 一手源核实（原 Anthropic 路标注"需回核"）

**归因修正：一手源是 Cognition，不是 Anthropic system card。**

来源：https://cognition.ai/blog/devin-sonnet-4-5-lessons-and-challenges（2025-09/10）【官方（Cognition）】

- Sonnet 4.5 是 Cognition 见到的第一个"对自己 context window 有感知"的模型，该感知改变行为：模型自认为接近窗口上限时**抄近路、留下未完成任务**——即使实际余量充足。
- 模型对剩余 token 的自估"consistently underestimates...very precise but wrong"（一贯低估，估得很精确但是错的）。
- 教程用法：§八上下文管理——"上限不仅影响召回，还改变模型收尾行为"的一手证据；缓解思路（容量余量、对模型显式沟通预算）写作时回读原文取细节。Anthropic 路线笔记里"出处疑为 Sonnet 4.5 system card"的猜测作废。

## 未竟事项

- developers.openai.com 的 approval modes 用户文档仍未抓到（SSL 层失败，疑与网络环境有关）；写 §八时可用浏览器手工核对，或以仓库 README + 社区文档交叉为准。
- OTel 具体属性名全表、LangGraph durability 三档 reference 页逐字、Langfuse observation types——写到对应章节时定点抓取。
