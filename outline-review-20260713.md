# 第二、三卷大纲评审 · 2026-07-13

评审对象：`volume2-outline.md`（v3）、`volume3-outline.md`（v1）。核查方式：对照 `research/volume2/` 既有调研 + 本次联网检索（检索日 2026-07-13）。

## 一、总体结论

两卷大纲**结构成立，可以进入写作**。第二卷"六类契约 + 六不变量 + 对象×事件×边界"的组织方式比机制域并列更抗遗漏；两卷边界表（vol2 §0.2）划分清晰且判断规则可执行；事实修正纪律（vol2 第四节）7 条经核查全部成立。

主要问题不在结构，在**时效性**：两份大纲的外部事实基线大致停在 2025 年底，2025-12 至 2026-07 之间发生了至少 6 件直接影响章节内容的事，其中 **MCP 2026-07-28 新规范**（两周后定稿）是两卷共同的最大缺口。另有第二卷 3 个主题遗漏、第三卷 P0 清单 7/10 项本次已可关闭。

## 二、事实核查结果

| # | 大纲声明 | 结论 | 说明 |
|---|---|---|---|
| 1 | Assistants API 已 deprecated、2026-08-26 关闭（vol2 四.1） | ✅ 准确 | 2025-08-26 通告，一年后关停，无延期 |
| 2 | LangGraph durability 三档（vol2 §6.3） | ✅ 准确 | 官方即 `sync`/`async`/`exit` 三档，写作时可逐字引 |
| 3 | Temporal：decision 可重放、Activity 可能多次执行（vol2 四.3） | ✅ 准确 | 与官方文档一致 |
| 4 | OTel GenAI conventions 标 maturity（vol2 四.5） | ✅ 已核 | 仍为 Development、独立仓库（research/07 已有） |
| 5 | context anxiety 用 Cognition 一手源（vol2 四.6） | ✅ 已核 | research/07 已定位 |
| 6 | "OWASP Agentic Top 10 映射"（vol3 §8.8） | ⚠️ 需精确化 | 正式名称 **OWASP Top 10 for Agentic Applications 2026**，2025-12-09 发布，编号 ASI01–ASI10；大纲写法模糊，且未利用其分类做章节映射 |
| 7 | "NIST agent identity"（vol3 P0-1） | ✅ 已有一手源 | NCCoE 概念文件 *Accelerating the Adoption of Software and AI Agent Identity and Authorization*（2026-02-05，评论期至 04-02）+ CAISI AI Agent Standards Initiative；结论是"复用 OAuth/SPIFFE/OIDC 做适配而非重造"，multi-hop delegation 仍未解 |
| 8 | Temporal Worker Versioning（vol3 P0-3） | ✅ 已 GA | **2026-03-30 GA**；pinned/auto-upgrade 两种行为、drain/drained 语义、Upgrade-on-Continue-as-New 进 Public Preview——§15.2 的 pin-to-version 有官方术语可直接落 |
| 9 | ZDR 边界（vol3 P0-4） | ✅ 已核 | Anthropic ZDR 仅覆盖指定端点，安全分类器结果仍保留；OpenAI background mode 存约 10 分钟、**不兼容 ZDR**；Anthropic Covered Models 新政策 2026-06-09 生效（仅 ZDR 组织适用） |
| 10 | eval 噪声（vol3 P0-7） | ✅ 已有一手源 | Anthropic《Quantifying infrastructure noise in agentic coding evals》：资源配置可摆动分数至 **6pp**，≈3× 基线资源处存在相变；arXiv 2602.07150《On Randomness in Agentic Evals》：单次 pass@1 波动 2.2–6pp，temp=0 时 std 仍 >1.5pp |
| 11 | rainbow deployment 案例（vol3 P0-9） | ✅ 已有一手源 | Anthropic multi-agent research system 工程文；另有《Effective harnesses for long-running agents》《Scaling Managed Agents》（2026-04）两篇直接相关 |
| 12 | MCP 供应链（vol3 §11）/ 长运行工具（vol2 §7.7） | ❌ 缺最新规范 | **MCP 2026-07-28 规范 RC 已发布**（两卷均未提及，见下） |

### MCP 2026-07-28 规范（最大时效缺口）

定稿日 2026-07-28（本大纲日期 15 天后），是 MCP 发布以来最大修订，且恰好命中两卷多个章节：

- **协议层无状态化**：`Mcp-Session-Id` 从 Streamable HTTP 移除 → 直接影响 vol2 §8 的重连/续传论述（不能再假设协议层 session）。
- **Tasks 扩展**：`tools/call` 可返回 durable handle，`tasks/get`/`tasks/cancel` 驱动，状态五态（working / input_required / completed / failed / cancelled）→ 就是 vol2 §7.7"长运行工具"的业界标准契约形状，应作为对照写入。
- **授权硬化**：RFC 9207 `iss` 校验、严格 `aud` 校验、OAuth 2.1 + PKCE → vol3 §11 与 §9 的直接材料。
- **Extensions 框架 + 正式 deprecation policy** → vol3 §11.9 / §6.9 的依据。

## 三、第二卷细化建议（优先）

### 3.1 需补的主题（结构性遗漏）

1. **Durable timer / 定时唤醒**（建议入 §四或 §六新增小节）：sleep、deadline、定时 resume、cron 触发的 run 是运行时状态而非进程内 setTimeout；进程死后 timer 谁恢复。Temporal timer、scheduled task 均是现成对照。目前 §4/§6 完全没有时间维度的状态。
2. **入口幂等**（§4.4 扩展）：客户端重试 POST 造成重复 run——client-supplied idempotency key 在 run 创建边界的语义。§7 只讲了工具侧幂等，入口侧缺失。
3. **MCP Tasks 对照**（§7.7 + §8）：见上节；附录 E 对照表加一列。

### 3.2 既有小节的细化点

- **§六**：6.10 对照中补 OpenAI Responses `background=true`（轮询式长任务，替代 Assistants Runs 的超时场景）与 Conversations 对象（无 30 天 TTL，与 Response 默认 30 天 TTL 对比——正好是"哪份状态算数"的实例）；Agent SDK 的 resume/fork 补一个已核实的坑：session 按 cwd 编码存储，换目录 resume 会得到空会话——可作 §6.8/§9.9 的真实反例。
- **§十**：research/07 已抓到的 Codex 一手材料应显式落位：execpolicy 的 allow/prompt/forbidden 三档 + `match/not_match` 加载期自测（呼应 §12.9 sabotage validation）；shell-escalation 的 Run/Escalate/Deny 三态协议（10.6 硬软层级的实例）；bubblewrap 默认全只读 + 按路径特异性分层覆盖（10.7 filesystem 隔离的实例）。大纲目前未指明这些素材归属，写作时容易丢。
- **§十二**：12.4 "Observe First, Interpret Later" 建议直接标注出处为 Codex rollout-trace README（research/07 已核），并引其"tracing is not telemetry"的边界声明支撑 12.7。
- **§八**：8.2 之外补一条"协议层 session 不可依赖"（MCP 无状态化即例证），把续传责任明确压到应用层 cursor/replay window 上——这会让 8.3 的论证更硬。

### 3.3 无需改动

卷定位、边界表、六契约/六不变量、章节顺序、写作顺序、事实修正纪律——均成立，不建议再动顶层结构。

## 四、第三卷细化建议

- **§八.8**：改为"映射 OWASP Top 10 for Agentic Applications 2026（ASI01–ASI10）"，并加一张章-风险映射表：ASI03（Agent Identity & Privilege Abuse）→§9；ASI06（Memory & Context Poisoning）→§10.8；ASI04（Supply Chain）→§11；ASI05（Unexpected Code Execution）→§8/vol2 §10；ASI08（Cascading Agent Failures）→§16。保留原句"不把 taxonomy 当控制措施"。
- **§九**：钉住 NCCoE 概念文件为锚点源；9.3/9.4 落到具体机制：OAuth 2.0 Token Exchange（RFC 8693）`act` claim 保留委托链、SPIFFE/SPIRE 做 workload identity；并明确写出"multi-hop delegation 是当前标准未解问题"——这正是 9.6 跨平台委托的诚实边界。
- **§十**：10.6 细化到已核实边界：ZDR 不覆盖的例外（安全分类器、code execution 等标 No 的功能）、OpenAI background mode 不兼容 ZDR、Covered Models 2026-06-09 政策——都是"厂商保证精确到版本与部署模式"（1.4 新增要求）的现成练习题。
- **§十一**：加 MCP 2026-07-28 小节：授权硬化（iss/aud 校验）、stateless 迁移对已部署 server 的影响、extensions 与 deprecation policy 作为 11.9 合同条款的协议层对应物；11.8 的 kill switch 可对接 `tasks/cancel`。
- **§十四**：14.4 用硬数字重写：基础设施噪声可达 6pp（常大于相邻模型的榜单差距）、≈3× 资源相变（以下修 flakiness、以上改变被测能力）、单次 pass@1 波动 2.2–6pp → 直接推出 14.10 的 CI gate 规则（多次独立运行 + 统计功效分析定 run 数，而非单次阈值）。
- **§十五**：15.2/15.3 采用 Temporal GA 术语（pinned 保证单版本完成、draining/drained、ramp、Upgrade-on-Continue-as-New 处理长跑 workflow）；rainbow deployment 引 Anthropic 多智能体系统文；补引《Scaling Managed Agents》（brain/hands 解耦）作为 15.1 "无状态发布不够"的正面案例。
- **P0 清单状态更新**：1、2、3、4、5、7、9 已定位一手源（本文件第二节），可改标"已解决，写作时回读原文"；剩余 6（provider 契约全表）、8（备份最佳实践）、10（成本事故一手源）保持 P0。

## 五、遗留判断

- 两卷契约框架（6+5）对称、接口清单（vol3 第四节）完整，未发现循环依赖。
- vol3 §12.9 "合规框架只做映射" 的立场建议保持，勿因 EU AI Act 等展开成合规章。
- 大纲 v3/v1 的版本号建议在采纳修改后分别升 v4/v2，并把本文件核查日期写入各自的检索截止声明（vol2 四.7 / vol3 附录 I）。

## Sources

- [OWASP Top 10 for Agentic Applications for 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [NCCoE: Software and AI Agent Identity and Authorization](https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization) / [概念文件 PDF](https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf)
- [MCP 2026-07-28 Specification Release Candidate](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/) / [Tasks extension](https://modelcontextprotocol.io/extensions/tasks/overview)
- [Temporal: Worker Versioning GA](https://temporal.io/blog/ga-worker-versioning-public-preview-upgrade-on-continue-as-new) / [文档](https://docs.temporal.io/production-deployment/worker-deployments/worker-versioning)
- [LangGraph Durable Execution](https://docs.langchain.com/oss/python/langgraph/durable-execution)
- [OpenAI Background mode](https://developers.openai.com/api/docs/guides/background) / [Conversation state](https://developers.openai.com/api/docs/guides/conversation-state) / [Deprecations](https://developers.openai.com/api/docs/deprecations)
- [Claude Agent SDK: Sessions](https://platform.claude.com/docs/en/agent-sdk/sessions)
- [Anthropic ZDR 适用范围](https://privacy.claude.com/en/articles/8956058-i-have-a-zero-data-retention-agreement-with-anthropic-what-products-does-it-apply-to) / [Covered Models 保留政策](https://support.claude.com/en/articles/15425996-data-retention-practices-for-mythos-class-models)
- [Anthropic: Quantifying infrastructure noise in agentic coding evals](https://www.anthropic.com/engineering/infrastructure-noise)
- [On Randomness in Agentic Evals (arXiv 2602.07150)](https://arxiv.org/pdf/2602.07150)
- [Anthropic: multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) / [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) / [Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents)
