# 修订记录

本卷 2026 年 9 月修订。读过 0727 版的读者，可以从这一章了解改了哪里。

## 修订范围与原则

这次修订对照一手资料核查了书中引用的外部事实，统一了三卷的术语，修正了几处前后矛盾，并按"让第一次读的人也读得懂"的标准重写了大量段落。书的观点、章节结构、8 个 runtime 机制加 1 个 Safety 控制面的框架都没有变。

三卷共用的术语约定与外部事实的核查结论，见仓库根目录的 [`术语对照表.md`](../术语对照表.md)。英文版（`introduction.en/`）尚未同步。

## 结论与建议有变化的地方

这几处改动会影响读者的做法，建议优先看：

- **"cache 共谋"拆成两条反模式**（§7.4、附录 F）。旧版认为提供商的前缀 KV cache 会让 N 次复跑变成非独立样本，对策是在 prompt 前部加 per-run nonce。核查后，DeepSeek、OpenAI 的官方文档都写明前缀缓存只匹配输入前缀，输出照样逐 token 生成，命中不改变输出。修订后：
  - **AP01 改名"复跑不独立"**：来源是客户端或评测工具的响应缓存、固定 seed、复跑之间共享的文件与记忆和工作区、temperature 0 时缓存命中带来的逐字复现。
  - **新增 AP20"对固定测试集过拟合"**：反复对着同一套测试集调 prompt、规则与工具描述，测评成功率高而上线后表现差。附作者的真实经历、诊断方法（含区分输入扰动与缓存影响的四组对照实验）与预防方法（开发集与留出集分开、线上失败回流为判例、同时报告 pass@1 与 pass^k）。
  - **per-run nonce 保留**，重新定位为"输入扰动测试"的简便实现：放在 prompt 开头时，测到的多样性里混有模型对输入微小变化的敏感度。
- **动态工具子集会降低缓存命中率**（§5.3）。旧版把"按任务挑工具子集"的收益写成提高提示词缓存命中率；工具段排在缓存前缀最前面，子集一变整段都要重算，修订后移到代价一栏。追加消息也不会破坏已有前缀的缓存，旧版"prefix cache 塌方"的说法已删。
- **循环停止条件**（§5.1）。基础 ReAct 循环在模型不再请求工具时结束，步数上限只是兜底；"由 verifier 判定达到目标才停"是本书主张的附加判定，不是循环本身的定义。
- **typestate 的作用范围**（§6.2）。编译期类型只约束 harness 开发者写的代码，拦不住模型在运行时发出的工具调用；旧版写给 agent 的"你的调用会被编译期类型检查"一句已删。
- **hook 的强制性**（§5.5、§5.9）。分为阻断型（代码直接拦截，属强制）与注入型（保证在正确时刻注入，模型是否遵循仍不确定）。
- **Memory 的定义**（§5.4）。旧版称 Memory 为"跨 turn 但不跨 run 的工作记忆"，与后文的认知科学对应冲突。修订后 Memory 指"harness 在模型外维护的、跨多次调用可读写的状态"；认知科学的工作记忆对应本书的 Context。

## 事实更正

| 位置 | 旧版说法 | 修订后 |
|---|---|---|
| §一、§5.1 | 整段输出在一次前向计算中完成 | 每产生一个 token 做一次前向计算 |
| §二 | 2020 年 6 月 OpenAI 发布 GPT-3 并给出第一个公开 API | 2020-06-11 以私测形式开放，2021-11-18 取消候补名单 |
| §二 | ReAct 第一次正式提出 Thought-Action-Observation 循环（Princeton）；LangChain 是行业第一次系统性封装 | ReAct 是这一范式最有影响的表述（Princeton 与 Google Research Brain），先行工作有 WebGPT、SayCan、MRKL、AI Chains；LangChain 是最早流行起来的开源封装之一 |
| §三 | AutoGPT 没有状态记忆，goal 藏在 prompt 里会被截断；GPT-4 窗口 4K–16K | AutoGPT 每轮重新注入 ai_goals，也有向量记忆后端，失败主因是检索回来的记忆不可靠、没有循环检测；GPT-4 发布时窗口为 8K 与 32K |
| §三 | OWASP LLM08 Excessive Agency | 2025 版为 LLM06（2023–24 版为 LLM08） |
| §四 | Claude Code 2024-04 alpha、2024-06 GA；Codex CLI 2024 发布；Cursor Composer 2023 起 | Claude Code 2025-02-24 研究预览、2025-05-22 GA；Codex CLI 2025-04-16；Cursor Composer 2024-07 起，2024-11 出现 agent 模式。据此推出的"已运行近两年""命名滞后约两年"同步修正 |
| §四 | context engineering 由 Karpathy 提出 | 2025-06 由 Tobi Lütke 发帖推广，Karpathy 附议 |
| §四 | 与 Wiener 控制论"完全同构"；MLOps 教科书 2018–2019；DENDRAL 与 MYCIN 开会发现没有共同名字 | 改为可以借前馈、反馈语言类比；Hapke & Nelson 2020、吴恩达 MLOps 课程 2021；删去无出处的情节 |
| §四 | DOS 程序跳过文件系统直接操作 inode | DOS 使用 FAT，没有 inode；改为"直接读写磁盘扇区" |
| §5.0 | 用人类短期记忆容量 7±2 论证 8 个机制；控制面/数据面来自 OS 工程 | 删去 7±2 论证；控制面/数据面源自网络设备，后被 SDN、Kubernetes 沿用；Safety 控制面在安全领域的对应概念是引用监视器 |
| §5.1 | OODA 由 Boyd 在 1960 年代提出 | 1970–80 年代（《Patterns of Conflict》） |
| §5.1 | Anthropic 在 2024 年推出并行工具调用；Anthropic 文章原话"don't use multi-agent for coding tasks" | OpenAI 2023-11 率先支持并行工具调用；Anthropic 原文无此句，改为转述"多数编码任务可真正并行的部分比研究任务少" |
| §5.1 | reasoning model 把"想"和"做"拆成两个独立的资源池；"思考更长就更对"已被证伪 | 拆开的是通道，思考 token 通常仍计入总输出额度；部分任务上存在测试时计算的逆向缩放，并非普遍成立 |
| §5.2 | prompt caching 只有 Anthropic 大力推；Codex CLI 是单 provider | 各家都有提示词缓存，实现与计费不同；Codex CLI 可配置多个 provider |
| §5.3 | OpenAI strict mode 与 harness 的"拦下重试"是一回事；schema 规范化 fail-closed | 模型侧严格模式（约束解码）与 harness 侧执行前校验分开写；改为启动期快速失败（fail-fast） |
| §5.4 | 命中前缀缓存后只算前缀以外的 token；中段信息"召回率"下降 | 命中部分按折扣价计费；指标是准确率，降幅可超过 20 个百分点 |
| §5.4 | Mem0 在 LongMemEval 上分数较高；Zep 63.8% vs Mem0 49.0%，GPT-4o，同行评议 | Mem0 论文评测用 LoCoMo；Zep 预印本在 LongMemEval 上 gpt-4o-mini 55.4%→63.8%、gpt-4o 60.2%→71.2%（均对比全上下文基线），未与 Mem0 比较；49.0% 找不到出处，已删 |
| §5.4 | 双时态模型最早源自 McCarthy 1963 年情景演算 | 出自时态数据库研究（Snodgrass & Ahn 1985，valid time 与 transaction time） |
| §5.4 | Claude Code 的 Auto Dream 机制（24 小时、5 个会话、200 行） | 官方文档与更新日志无记载，改为"据第三方博客描述"；官方可核实的是 auto memory 在会话开始加载 MEMORY.md 前 200 行或 25KB |
| §5.5 | CLAUDE.md / AGENTS.md 由 Anthropic 2024 年推出 | CLAUDE.md 是 Claude Code 的约定；AGENTS.md 由 OpenAI 2025-08 发布，现由 Linux Foundation 旗下 Agentic AI Foundation 托管 |
| §5.5 | system prompt 衰减与 lost-in-the-middle 同源 | 开头位置本身不吃亏；长对话后规则遵循率下降是另一种现象 |
| §5.7 | OTel GenAI semconv 与 W3C Trace Context 同源；replay 可以零成本复现消融 | 二者是两层：W3C Trace Context 传递 trace 标识，GenAI semconv 是属性命名约定；回放只能复现到行为分叉点为止 |
| §5.7、§5.8 | Inspect AI 由 UK AISI 开源，内建 PRM | AISI 于 2025-02 更名为 AI Security Institute，Inspect 由 AISI 与 Meridian Labs 共同开发；没有内建 PRM |
| §5.8 | RLVR 在工程层落地为 Hard Gate；Preference Leakage 指 judge 与 agent 相关 | Hard Gate 是运行时检查，RLVR 是训练范式；Preference Leakage 研究的是合成数据生成模型与 judge 的关联 |
| §5.9 | 权限求值顺序 deny → allow → ask | Claude Code 规则层为 deny → ask → allow，先匹配先生效；Agent SDK 完整顺序为 Hooks → Deny → Ask → Permission mode → Allow → canUseTool |
| §5.9 | 物理 sandbox；用正则检测提示词注入；OWASP 官方 LLM01 测试套件 | OS 级沙箱；注入检测主要靠分类器，只能降低风险；OWASP 没有官方测试套件，改用 AgentDojo、InjecAgent 等 |
| §5.11 | 先 push main 再提 PR；死锁因 Handler 自带锁 | 先推功能分支再向 main 提 PR；死锁因同一把不可重入锁被重复获取（Handler 自带的锁本是 RLock） |
| §7 | HPO 的 acquisition function（如 Hyperband） | 采集函数属于贝叶斯优化 / TPE，Hyperband 用 successive halving |
| §5.1 | Claude Code 内循环"不是一个简单的 while 块"；七个继续点、十一个终止出口；出处未注 | 按第三方分析（arXiv 2604.14228）改为外层仍是 while 循环、单轮承载十步以上机制；终止改为十种终止原因；补脚注 |
| §5.8.7、图 5.21 | overlap_pos / overlap_neg 对照组列为偏好泄漏的对策 | 该对照组检测的是预期答案被字面暴露，移到第二类"答案明示"并写明构造与判定规则；偏好泄漏的对策改为 judge 与 agent 跨模型家族 |
| §7.4 Phase B、实施 Spec 第 7 条 | "工具参数自动补全"在端到端单点消融里关掉后通过率不降反升 | 这次消融没有运行记录。改用一条真实的工程记录：参数解析失败就换成空对象、照常调用工具，遮蔽了错误信号；注明它由专项审计发现，没有做过开关对比 |
| §八 | MCP 传输有 stdio、SSE、WebSocket 三种；handoff 不共享状态、隔离最强 | 标准传输只有 stdio 与 Streamable HTTP（2026-07-28 版已去掉会话 ID）；handoff 默认把完整对话历史交给接收方 |
| §九 | 两句英文标为 Wiener 1948 原话；可观测性出自 Wiener；钱学森"70 年前"提出开放复杂巨系统 | 《控制论》原书无此两句，已删；可观测性、可控性出自 Kalman 1960；开放复杂巨系统论文发表于 1990 年 |
| §九 | 消融即钱学森的扰动理论；恒温器靠功率上限防振荡 | 消融对应系统辨识；恒温器靠回差避免频繁启停 |
| §12 | 通用 TDD 提示词；disabledTools 白名单 | 通用落地提示词（评测先行）；disabledTools 是黑名单 |
| 附录 | Constitutional AI 是运行时过滤器；SPIFFE、Biscuit、Zanzibar 同属 capability token | Constitutional AI 是训练方法，运行时方案是 Constitutional Classifiers；三者分别是身份标准、授权令牌、关系型授权 |

## 结构变化

| 旧版 | 修订后 |
|---|---|
| 第五章 8 件 runtime 加 1 件 Safety 控制面 | 8 个 runtime 机制加 1 个 Safety 控制面（全卷不再用"件"指机制） |
| §5.6 三层定位 | 两个作用加一个案例 |
| §5.5.5 反 prompt-injection 在 prompt 层的纪律 | 消息边界与历史完整性（注入防御见 §5.9） |
| §5.5 prompt 片段优先级 P0–P5 | 裁剪层级 L0–L5（避免与全书 P0 优先级撞名） |
| §7.4 防 Cache 共谋 | 防复跑不独立与测试集过拟合 |
| 各章"常见误区"小节 | 系统行为称"失效模式"，工程做法称"反模式" |
| 第十二章 通用 TDD 提示词 | 通用落地提示词（评测先行） |
| 附录 D 件 × 业界产品归位总图 | 机制与业界产品的对应总图 |
| 附录 E capability token 工业方案 | 身份、授权令牌与关系型授权 |
| 附录 F 常见误区速查（AP01–AP19） | 反模式速查（AP01–AP20），每条写中文名与英文名 |
| README 两组"六问" | 合并为一组"读完入门卷应该能回答的六个问题" |

## 术语调整

| 旧版 | 修订后 |
|---|---|
| 件（指机制） | 个、机制、组件 |
| 常见误区 | 失效模式 / 反模式 / 误区，按性质区分 |
| harness（智能体框架 / 驾驭层） | 保留英文，首次出现给一句说明性定义 |
| Cache 共谋 | 复跑不独立（AP01） |
| 流式累积 | 增量累积 |
| 召回率（指长上下文利用） | 准确率 |
| system_prompt_hash | prompt_hash（每轮完整 prompt 的指纹，不是不变量） |
| Skill-RA | 保留，注明是本书用语，业界常称工具检索（tool retrieval） |
| 把脉 | 行为探测（本书也称"把脉"） |
| inference / reasoning | 模型调用 / 推理（思考过程） |
| policy | 本书取访问控制义，不同于强化学习中的策略 |
| 物理 sandbox | OS 级沙箱 |
| 自我改进 | 自我演化（self-evolving，也称 self-improving） |
| 落地 Spec | 实施 Spec |
| 17 turn（§5.11 标题与图 5.28） | 17 步（16 轮 agent turn 加 1 次压缩） |
| 过程软信号（§三） | PRM（过程奖励模型），与 §5.8 一致 |
| 观察包装（§四） | 观测面，与 §5.6 一致 |

## 行文调整

全卷把当作逗号、句号使用的间隔号"·"改回了中文标点，减少了中英夹杂与作者惯用语（件、纪律、判定线等），破折号基本清零，"业界已收敛""事实标准"等依据不足的说法改为"某某提出""某某的做法"，没有出处的数字标为经验值，长段拆成了列表，内部术语在首次出现处补了白话解释。这类改动不逐条列出。

章节交叉引用逐条核对过：指向不存在内容的引用已改到实际位置（如 §5.4c 改为 §5.4.2，§5.9 的 ToolBlocked 改为权限拒绝，§5.2 的契约修复改为故障切换）；附录 G 改为与各章脚注标签一一对应。

## 尚未同步的内容

- 本卷 PDF 仍是 0727 版，将按本版重新构建。
- 配图已对照本版正文逐张核对并修改（中英文版同步）：与正文冲突的说法、残留的惯用词已改，每段图中文字最多保留一处破折号，左侧竖色条样式改为整圈细边框。
