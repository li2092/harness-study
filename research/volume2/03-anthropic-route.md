# Anthropic 路线：官方工程文章与产品契约

调研产出 · 2026-07-10 · workflow wf_2e1f15b2-4aa · Anthropic 路（从转录抢救的完整成果）

## 发现

### workflow vs agent 决策框架 + ACI

Building Effective Agents 两定义：workflow = LLM 与工具走预定义代码路径编排；agent = LLM 动态自主决定流程与工具用法。决策梯度：单次 LLM 调用（配 retrieval/example）到 workflow 到 agent，只在可验证进展但无法硬编码路径时上 agent，因为 agent 用更高延迟/成本换表现且有复合错误风险。五种 workflow 模式各有条件：prompt chaining（可干净拆固定子任务）、routing（有清晰分类分开处理更好）、parallelization（sectioning 独立并行 / voting 同任务多跑取信心）、orchestrator-workers（子任务无法预测）、evaluator-optimizer（有明确评价标准且迭代有价值）。ACI：像投入 HCI 一样投入工具接口，含 poka-yoke（改参数让 agent 更难犯错，如强制绝对路径）。反模式：别用不懂内部实现的框架（对底层的错误假设是客户出错常见来源），从直接调 API 起步，只在简单方案不够时加复杂度。

- 来源：https://www.anthropic.com/engineering/building-effective-agents
- 等级：【官方】
- 第二卷用法：第二卷开篇'架构分层从哪切'的顶层决策框架，接原料稿 §4 开头跨厂商对照。ACI+poka-yoke 进工具执行章，与 §4.6 校验三层互补。反模式进 §5.3+ 架构反模式。

### 长跑 agent harness 的状态外置与 checkpoint（全新一手文章）

Effective harnesses for long-running agents 是原料稿未覆盖的新文章。两 agent 模式：initializer 只跑一次搭环境建 feature list；coding agent 每个后续 session 做增量进展并留结构化更新。状态外置三件套：claude-progress.txt、feature_list.json（约 200+ feature 的 pass/fail，用 JSON 因比 Markdown 更不易被模型覆写）、git history（每 session 一个描述性 commit）。核心洞见：找到让 agent 用全新 context window 快速理解工作状态的方法。故障恢复：git commit 当 checkpoint，坏改动可 revert 回可用态；session 开头先跑基本测试抓未记录 bug。硬控制 vs 软约束区分明确：硬控制=限定只能改可编辑目录、JSON 格式、删/改测试不可接受；软约束=提示一次只做一个 feature、留干净环境。作者明说 Agent SDK 自带 compaction 不够用，要靠脚手架补。

- 来源：https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- 等级：【官方】
- 第二卷用法：第二卷最有价值的参照实现案例，支撑 §4.2 持久化与 §4.1 生命周期：状态外置到 crash-safe 存储正是 crash-only 哲学的产品落地。git-commit-as-checkpoint 可与 intent-result 两段式对照。compaction 不够用要靠脚手架是 §4.8 重要补充。

### orchestrator-worker 多 agent 架构与定量数据

How we built our multi-agent research system：lead agent（Opus 4）分析查询、定策略、生成带目标/输出格式/工具指引/清晰边界的任务描述，spawn 并行 subagent（Sonnet 4），每个有独立 context window、独立工具、独立探索轨迹，只回传浓缩结论。硬数据：多 agent 比单 agent Opus 4 在内部 research eval +90.2%；agent 比 chat 用约 4x token，多 agent 约 15x token；token 用量本身解释 80% 方差，加 tool 调用次数和模型选择三因子解释 95%；并行工具调用把复杂查询研究时间砍最多 90%；专测工具的 agent 改写描述后把后续任务完成时间降 40%。规模启发式写进 prompt：简单事实查证 1 agent 3-10 调用，直接对比 2-4 subagent 各 10-15，复杂研究 10+ subagent。已知瓶颈：lead 目前同步执行 subagent，等一批跑完才继续，无法中途纠偏、慢 subagent 会阻塞。

- 来源：https://www.anthropic.com/engineering/multi-agent-research-system
- 等级：【官方】
- 第二卷用法：第二卷'多 agent 编排'独立章主骨架+成本论据。15x token、80% 方差是何时该上多 agent 的量化止损线，接 §4.7 多入口并发后延伸。同步执行瓶颈是很好的半途设计/权衡教学点。

### 多 agent 生产工程教训：rainbow deployment、durable execution、tracing

同篇给运维硬经验。Rainbow deployment：agent 系统是高度有状态、几乎持续运行的 prompt/工具/执行逻辑网，部署更新时 agent 可能处在流程任意位置，因此逐步把流量从旧版切到新版、两版同时运行，避免更新打断在跑的 agent，防善意代码改动搞坏现存 agent。故障哲学：没有有效缓解时小系统故障对 agent 可能是灾难性的，出错时不能从头重启（重启昂贵且让用户沮丧），所以建能从出错点恢复的系统，把 Claude 适应性与重试逻辑+定期 checkpoint 等确定性保障结合；让 agent 知道某工具在失败并自适应效果出奇地好。可观测性：加全量生产 tracing 系统性诊断，但只监控 agent 决策模式/交互结构、不监控对话内容以保隐私。评估：把复杂工作流拆成应发生特定状态变更的离散 checkpoint。

- 来源：https://www.anthropic.com/engineering/multi-agent-research-system
- 等级：【官方】
- 第二卷用法：进 §4.12 运维通道——rainbow deployment 是更新与活跃 run 互斥的业界标准解法，补原料稿空白。确定性保障+AI 适应性混合是全卷 T4 主线又一实证。tracing/隐私取舍进 §4.10 可观测性。

### context engineering 框架：attention budget + 四策略

Effective context engineering 定义 context engineering 为在推理时策展并维护最优 token 集合，区别于只管系统提示的 prompt engineering。核心原则：找到能最大化目标达成概率的最小高信号 token 集合。机制根因：context rot（token 越多准确召回越低）+ attention budget（每新 token 消耗注意力预算）+ transformer n 平方注意力随长度被摊薄。四策略：(1) compaction 接近上限时摘要并用摘要重启新窗口；(2) structured note-taking 写 NOTES.md 到窗口外后续拉回；(3) sub-agent 专职 subagent 用干净窗口做深活只回传 1000-2000 token 浓缩摘要；(4) just-in-time retrieval 只存轻量标识（路径/查询/链接）运行时动态加载，配 head/tail 处理大数据不全量入窗。compaction 艺术在取舍：保留架构决策/未解决 bug/实现细节，丢冗余工具输出；最轻的是 tool result clearing；调法先最大化 recall 再迭代提升 precision。

- 来源：https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- 等级：【官方】
- 第二卷用法：把单薄的 §4.8 扩成第二卷一整章。attention budget/context rot 给为什么要压缩提供机制解释。四策略是小节结构。compaction 保留清单可做成 checklist。

### context editing + memory tool：API 级硬机制与定量收益

Managing context on the Claude Developer Platform（与 Sonnet 4.5 同发）。context editing：接近 token 上限时自动清除窗口内陈旧 tool call 与结果，保留对话流，无需手工 compaction。memory tool：基于文件、完全在 client 端通过 tool call 运作、开发者管存储后端，跨会话持久，让 agent 逐步建知识库、维护跨 session 项目状态。定量：memory+context editing 组合比 baseline +39%；仅 context editing +29%；100 轮 web search 评测里 context editing 让原本会因 context 耗尽失败的工作流跑完，同时降 token 消耗 84%。关键：两者都是 API/工具级硬机制，不是提示层软约束。

- 来源：https://claude.com/blog/context-management
- 等级：【官方】
- 第二卷用法：context engineering 章的硬机制落地小节——用官方产品坐实压缩必须走确定性硬路径而非指望模型自觉（T4）。39%/29%/84% 是全卷少见官方定量收益，可与 Harness-Bench 23.8pp、MAST +15.6pp 并列做工程投入有量化回报的证据链。

### code execution with MCP：把工具目录移出 context

Code execution with MCP（2025-11）指出两处浪费：所有 MCP 工具定义预载入窗口 + 中间结果反复穿过模型 context。解法是把 MCP server 呈现为代码 API/文件系统，agent 写代码调用、按需渐进发现工具（列 ./servers/ 目录、只读需要的工具文件），而非一次性读全部定义。硬数据：一个 Google Drive 到 Salesforce 工作流从 150,000 token 降到 2,000 token，省 98.7%。架构含义：工具目录从模型 context 移到代码/文件系统；中间结果默认留在执行环境（隐私，可在数据到模型前 tokenize PII）；agent 把中间结果写文件从而可恢复、可续跑、可把复用函数沉淀为 skill。

- 来源：https://www.anthropic.com/engineering/code-execution-with-mcp
- 等级：【官方】
- 第二卷用法：context engineering 章进阶小节，也是 §4.6 工具执行的架构升级视角：工具数量爆炸时工具即代码 API 是把 token 成本从线性压成按需的关键。98.7% 是极强成本论据。隐私（数据留执行环境）与副作用/沙箱主题衔接。

### writing effective tools：确定性系统与非确定性 agent 的契约

Writing effective tools for agents 核心视角：工具是一种新软件，是确定性系统与非确定性 agent 之间的契约——agent 会 hallucinate 或用错工具，故设计范式不同。原则：不要包装所有 API 端点，建少量高影响工作流工具；namespacing（前缀/后缀，如 asana_search，对评测有非平凡影响）；返回有意义 context（用 name/image_url 而非 UUID，把 UUID 换成语义化显著提精度）；token 效率（Claude Code 默认把工具响应截到 25,000 token；concise vs detailed 格式 206 降到 72 token 约三分之一）；工具描述当 steering，微调即可大幅提升（Sonnet 3.5 靠精修描述拿 SWE-bench SOTA）。工具整合：把 list_users/list_events/create_event 合成 schedule_event，多查询合成 get_customer_context。改进法：把评测 transcript 贴回 Claude Code 让 agent 自己重构工具，用 held-out test set 防过拟合。错误消息要具体可操作而非裸 traceback。

- 来源：https://www.anthropic.com/engineering/writing-tools-for-agents
- 等级：【官方】
- 第二卷用法：§4.6 工具执行章的工具设计独立小节，与 ACI 合流。25000 token 截断、concise/detailed、UUID 换语义名是可教工程动作。评测驱动+用 agent 改工具+held-out set 是很好的闭环示范，接 §5.5 评估陷阱。

### Agent SDK session：状态存哪 + continue/resume/fork

Work with sessions 把状态存哪怎么恢复做成产品契约。session 自动落盘为 ~/.claude/projects/(encoded-cwd)/*.jsonl（非字母数字字符全替换为短横，如 /Users/me/proj 变 -Users-me-proj），内容含 prompt、每次 tool call、每个 tool result、每个 response。三种返回：continue（找当前目录最近 session 不用记 ID）、resume（传具体 session ID，多用户/回到非最近时必需）、fork（从原 session 复制历史新建分支，原不变，得两个独立可分别 resume 的 ID）。跨机恢复要么搬 jsonl（cwd 必须一致），要么别依赖 resume、把结果作为应用状态喂进新 prompt（往往更鲁棒）。TypeScript 可 persistSession:false 只在内存不落盘；serverless 用 SessionStore adapter 外接存储。resume 拿到全新 session 最常见原因是 cwd 不匹配。关键定性：session 持久化的是对话，不是文件系统。

- 来源：https://code.claude.com/docs/en/agent-sdk/sessions
- 等级：【官方】
- 第二卷用法：§4.2 持久化+resume 的产品级参照。jsonl append 落盘+cwd 编码是状态存哪的具体答案。fork = LangGraph time-travel 的另一实现，可做跨厂商对照。跨机别依赖 resume、改传应用状态是很好的鲁棒性判断，进 §4.12 迁移。

### file checkpointing：Anthropic 自己的 dual-write 分裂

Rewind file changes with checkpointing 是原料稿 §3.3 dual-write 命题的产品级实证。文件 checkpoint 只追踪经 Write/Edit/NotebookEdit 工具的改动，明确警告经 Bash 命令（如 echo 重定向到 file.txt 或 sed -i）的改动不被捕获。机制：改文件前备份，每条 user message 带 checkpoint UUID，调 rewindFiles/rewind_files 传 UUID 恢复。关键分离：文件 rewind 只还原磁盘文件，不 rewind 对话——对话历史与 context 在 rewind 后保持不变。局限：只管文件内容（建/移/删目录不还原）、只在同 session 内、只管本地文件。

- 来源：https://code.claude.com/docs/en/agent-sdk/file-checkpointing
- 等级：【官方】
- 第二卷用法：教科书级案例：连 Anthropic 也把对话状态与文件系统状态分成两套独立 checkpoint，且明说 Bash 副作用无法自动回滚——正是原料稿有 intent 无 result 的非幂等副作用不能无脑回滚的官方印证。放进 §4.6 副作用一致性/§3.3。

### hooks：32 事件的确定性硬控制层

Hooks reference 是 T4 硬控制走模型输出之外确定性路径的教科书实现。32 个 hook 事件覆盖 session（SessionStart/End）、turn（UserPromptSubmit/Stop/StopFailure）、agentic loop（PreToolUse/PostToolUse/PostToolUseFailure/PostToolBatch/PermissionRequest/PermissionDenied）、agent 团队（SubagentStart/Stop）、context（PreCompact/PostCompact）等。exit 码语义：exit 0=无决定走正常流；exit 2=阻断（对可阻断事件生效）——PreToolUse exit 2 在工具执行前阻断（无论 Claude 想不想）、Stop exit 2 阻止停止继续对话、PreCompact exit 2 阻断压缩。注意 exit 1 被当非阻断错误、必须用 exit 2 才强制策略。PreToolUse 的 JSON 决定 permissionDecision: allow/deny/ask/defer + updatedInput（执行前改参数）；PostToolUse 不能撤销已执行工具、只能反馈。关键安全告诫：Bash 模式的 if 过滤是 best-effort、解析不了就 fail-open 照跑，官方明说要强制硬 allow/deny 请用 permission 系统而非 hook。

- 来源：https://code.claude.com/docs/en/hooks
- 等级：【官方】
- 第二卷用法：§4 各域硬控制的统一落地样板：hook 让压缩/权限/验证走模型外确定性路径。exit 2 语义+PreToolUse 执行前阻断是 T4 最佳教学例。hook 是 best-effort、permission 才是硬边界这一反直觉细节，正好引出 permission 六步序，教读者别把软层当硬层。

### permission 六步求值序：硬控制的优先级契约

Configure permissions 给出确定性权限求值完整优先级（比 hook 更硬一层）。六步：1) Hooks（最先，可直接 deny）到 2) Deny 规则（命中即阻断，即使在 bypassPermissions 也阻断；裸名 deny 如 Bash 直接把工具从 context 移除）到 3) Ask 规则（落到 canUseTool 回调，bypassPermissions 下也强制询问）到 4) Permission mode 到 5) Allow 规则 到 6) canUseTool 回调。六种模式：default、dontAsk（不询问直接拒）、acceptEdits（自动批文件编辑）、bypassPermissions（全放行，但 deny/ask/hook 仍先于它生效）、plan（只读探索、编辑不自动批）、auto（模型分类器批准）。硬告诫：allowed_tools 约束不了 bypassPermissions；被 allow 规则自动批准的工具永不到达 canUseTool（放这里的检查被静默绕过）；subagent 继承父的 bypassPermissions 且不可 per-subagent 覆盖，可能给 subagent 全系统权限；要每次调用都检查就用 PreToolUse hook。

- 来源：https://code.claude.com/docs/en/agent-sdk/permissions
- 等级：【官方】
- 第二卷用法：第二卷 Safety/硬控制章的核心样板——一张 deny 恒胜、hook 最先、bypass 也拦不住 deny 的优先级图就是 T4 硬控制的可实现契约。subagent 继承 bypass 的权限蔓延直接印证 Lingering Authority（arXiv:2606.22504）。auto-approve 的工具永不到 canUseTool 是很好的静默失败陷阱教学。

### prompt caching：全卷缺失的横切成本工程

Prompt caching 文档给出 agent harness 长系统提示+增长历史下的成本工程细节，原料稿完全没覆盖。最多 4 个显式 cache breakpoint，向后 20 block lookback。TTL 默认 5 分钟、可选 1 小时（额外成本），命中会免费刷新 TTL。最小可缓存长度随模型：Opus 4.8/Sonnet 4.5 为 1024 token（有的 512、有的 2048/4096）；太短不缓存但不报错，要看 cache_creation_input_tokens/cache_read_input_tokens 是否为 0。成本倍率：cache write 5 分钟 1.25x、1 小时 2x base 输入价；cache read（命中）0.1x=base 的 10%。失效层级 tools 到 system 到 messages，某层一变则该层及之后全失效（改工具定义连带全失效）。工程指引：稳定内容（tools、system）放前、易变内容（时间戳、用户输入）放后，cache_control 打在跨请求前缀完全一致的最后一个 block 上。

- 来源：https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- 等级：【官方】
- 第二卷用法：新增一节 harness 的成本/性能横切工程。0.1x 读 vs 1.25x 写的经济学决定了 harness 必须把 system prompt/工具定义放前、增长历史放后——与 context engineering、compaction 边界强耦合（每次压缩打断缓存前缀是压缩的隐性成本）。给深入工程化读者一个可算账的优化点。

### context anxiety：模型接近上限时提前收尾（需核一手源）

多处二手转述提到 Anthropic 观察到 Sonnet 4.5 出现 context anxiety——随 context 上限临近，模型倾向提前草草收尾任务；团队通过在 agent loop 里加入 context reset 缓解。这是具体的 agent 可靠性行为，但目前证据为二手（Medium/汇编），原始出处疑为 Sonnet 4.5 system card 或相关官方博文，引用前需回核一手。

- 来源：https://medium.com/@neel2108/anthropic-is-teaching-developers-how-production-agents-actually-work-9e87dc24c637
- 等级：【二手】
- 第二卷用法：context engineering 章一个模型行为副作用注脚：压缩/上限不仅影响召回，还改变模型收尾行为，故 context reset 也是一种可靠性手段。写入前必须回核 Sonnet 4.5 system card 一手源，否则只标为业界报告。

### advanced tool use（tool search / 程序化工具调用）

检索到 Anthropic 另有 2025 工程文 Introducing advanced tool use on the Claude Developer Platform，方向与 code execution with MCP 一致：面向工具数量膨胀，提供 tool search（按需检索工具定义而非全载）与 programmatic tool calling 等能力，进一步把工具目录 token 成本从预载全部改为按需发现。本次未逐字抓取正文，作为指针记录，展开前需 WebFetch 原文补细节与数字。

- 来源：https://www.anthropic.com/engineering/advanced-tool-use
- 等级：【官方】
- 第二卷用法：与 code execution with MCP、writing-tools 并入工具规模化小节，说明 Anthropic 在 2025-2026 把工具目录膨胀当一等工程问题的连续演进。第二卷正式引用前补抓正文取定量数据。

### 跨文章收敛出的 Anthropic 架构方法论主线

把五篇官方文横向看，Anthropic 一致主张可提炼为四条当路线总纲：(1) 复杂度前置为决策——do the simplest thing that works，能 workflow 不上 agent，能单调用不上 workflow；(2) 状态外置+确定性保障——长跑靠外部文件/session/memory 存状态，配 checkpoint、retry、rainbow deployment 等确定性护栏，与 AI 适应性混合；(3) 硬控制走模型外——permission 六步序+hooks+context editing/memory tool 都是确定性路径，官方反复强调别把软层当硬层；(4) context 是稀缺预算——围绕 attention budget 做 compaction/note-taking/subagent/JIT retrieval/code-execution，目标是最小高信号 token 集。

- 来源：https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- 等级：【官方】
- 第二卷用法：作为第二卷 Anthropic 路线综述或某章导语，把散在五篇的观点收成一条可讲主线再逐章展开。也可与 OpenAI/LangGraph 路线并置做跨厂商对照表（各家在这四条上的实现位置差异）。

