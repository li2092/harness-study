# 第二卷 · 正文表格嵌入图源（SSOT）

> 由 `gen_embeds.py extract` 生成。**之后改表格内容请改本文件**，再跑 `python gen_embeds.py regen`；
> 正文 md 里只留 `figures/embed/*.png` 引用。编辑区（审稿日志/变更记录）表格未抽取，仍在正文 md。

## tb-01-1 · 01-architecture-v4.0.md · 原 L25

| 契约 | 承诺 |
|---|---|
| 真相契约 | 状态可归属：哪份状态算数、归谁写，从不含糊 |
| 转移契约 | 转移可解释：状态从 A 到 B，说得出凭什么 |
| 副作用契约 | 副作用可对账：声称做过的事，外部世界对得上账 |
| 交互契约 | 失败可收敛：失败、中断和恢复最终进入已定义状态 |
| 权限契约 | 权力有边界且有期限：恢复状态不等于恢复旧授权 |
| 证据契约 | 结论有证据：完成与安全声明能指向运行证据 |

## tb-01-2 · 01-architecture-v4.0.md · 原 L100

| 级 | 含义 | 判断 |
|---|---|---|
| L0 | 没机制 | — |
| L1 | 能跑 | 代码合并、单测通过 |
| L2 | 能看 | 生产路径埋了事件，trace 里查得到 |
| L3 | 能评 | 有 reward 信号或 verifier 判定 |
| L4 | 能比 | 有 on/off 消融，单跑能看出贡献 |
| L5 | 能优 | 参数可自动搜索 |

## tb-01-3 · 01-architecture-v4.0.md · 原 L135

| 组件 | 主守契约 | 不设防的失效方式与约束（一句） |
|---|---|---|
| model adapter | 转移＋证据 | 恢复时把没跑完的部分重跑一遍——模型输出不确定，重跑制造第二个版本的历史；出路是每次调用完整留档（模型标识、参数、上下文摘要、输出），复用记录、永不重调 |
| agent loop | （被所有契约约束） | 内存攒半轮成果，进程一死全部蒸发——领全卷最硬的约束：内存里攒的一切要么立刻落盘，要么等于不存在 |
| 入口层（UI/API/IM/scheduler） | 交互契约 | 前端超时自作主张把任务标失败，用户照着重发，两个 run 并行写一个会话——所以界面显示的一切都是投影，即持久状态的只读呈现，投影不回写，UI 的聪明猜测活不过一次刷新 |

## tb-01-4 · 01-architecture-v4.0.md · 原 L192

| 契约 | 核心问题 | 主场 | 四原则重点格 |
|---|---|---|---|
| 真相契约 | 哪份状态算数，谁拥有它？ | 第六章、第十章 | 可观测（状态可归属才可观测） |
| 转移契约 | 什么事件能让状态从 A 变成 B？ | 第五章、第七章 | 可观测＋稳定（恢复即重放转移） |
| 副作用契约 | 声称做了什么，外部世界实际发生了什么？ | 第八章 | 可控（对账硬门）＋闭环 |
| 交互契约 | 用户、连接与后台 run 如何保持一致？ | 第九章（与第五章分头兑现） | 稳定（断流不等于断 run） |
| 权限契约 | 谁以谁的身份、在什么边界内行动？ | 第十一章、第十二章 | 可控（边界与期限） |
| 证据契约 | 凭什么相信状态、动作和完成声明？ | 第十三章 | 全部四格的地基 |

## tb-01-5 · 01-architecture-v4.0.md · 原 L243

| 入门卷 | 本卷落位 |
|---|---|
| Agent Loop | agent loop（1.4；新约束：内存即易失） |
| Model Adapter & Routing | model adapter（1.4；routing 决策归 run manager） |
| Tool Registry & ACI | tool executor（1.4；policy 决策归 run manager，第十一章展开） |
| Context / Memory / Artifact | 状态层中的持久对象；context 是投影（第六章、第十章） |
| Prompt Assets | run manager 按配置注入，agent loop 组装时消费（第十章） |
| Observation Surface | 事件流的输入侧 |
| Trajectory / Event Stream | 事件流 + 证据存储（第十三章） |
| Verifier | 证据存储供证 + run manager 门禁（第十三章） |
| Safety 控制面 | run manager 的 policy/approval + 权限契约（第十一章） |
| 控制论四原则（第九章） | 本卷检验坐标系（1.3；入门卷问"部件对上原则了吗"，本卷问"怎么证明没骗我"） |

## tb-01-6 · 01-architecture-v4.0.md · 原 L266

| 本卷 | Claude Code / Agent SDK | OpenAI（Responses） | LangGraph | Temporal |
|---|---|---|---|---|
| Conversation | session（jsonl） | Conversation（原 Thread） | thread | — |
| Run | 一次触发的 agentic 执行 | Response（原 Run） | 一次 graph invoke | Workflow Execution |
| Turn | turn | Item 序列的一段 | superstep | Workflow Task（近似） |
| Step / Tool Execution | tool_use / tool_result 块 | Item | node/task 执行 | Activity |

## tb-02-1 · 02-correct-runtime-v1.0.md · 原 L52

| 要素 | 回答的问题 |
|---|---|
| owner | 谁负责让这条承诺成立 |
| trigger | 什么事件触发它 |
| guard | 什么前置条件必须先成立 |
| action | 系统做什么 |
| outcome | 结束于哪个已定义状态 |
| evidence | 拿什么证明它发生过 |

## tb-02-2 · 02-correct-runtime-v1.0.md · 原 L185

| 假设原文 | 所属契约 | 当前形态（注释/口头/分支缺失） | 确定性档位 | 六要素缺哪几格 | owner |
|---|---|---|---|---|---|
| "SSE 断开 run 继续跑" | 交互 | 代码注释 | 声称保证，实为 best effort | outcome、evidence | 无 |
| … | | | | | |

## tb-03-1 · 03-incident-v2.0.md · 原 L61

| 帧 | 事件 | M5 所在载体 | R1 输出所在载体 | SQLite | 用户看到的 |
|---|---|---|---|---|---|
| 0 | 会话空闲 | — | — | M1–M4 | 完整历史 |
| 1 | 用户发送 M5 | 前端内存、请求体 | — | M1–M4 | M5 上屏 |
| 2 | RunManager 创建 R1 | 服务端内存 | — | M1–M4 | 生成中 |
| 3 | 模型流式输出 | 服务端内存 | 服务端内存、SSE 流、前端内存 | M1–M4 | 回复逐字出现 |
| 4 | 点击链接，webview 原地导航 | 服务端内存 | 服务端内存（前端副本蒸发） | M1–M4 | 外部网页 |
| 5 | SSE 断开，R1 依设计后台续跑 | 服务端内存 | 服务端内存 | M1–M4 | 外部网页 |
| 6 | 后退，SPA 重载，读库 | 服务端内存 | 服务端内存 | M1–M4 | 少一轮，"丢了" |
| 7 | 用户发 M5′，R2 抢占：abort R1 并覆盖注册 | 服务端内存（即将无主） | 同左 | M1–M4 | 新回答生成中 |
| 8 | R1 收尾，isCurrentRun 判假，跳过落库 | 随 R1 上下文回收 | 同左 | M1–M4 | 新回答继续 |
| 9 | R2 完成，落库 | 永久消失 | 永久消失 | M1–M4、M5′、R2 | 一切"正常" |

## tb-03-2 · 03-incident-v2.0.md · 原 L112

| 契约 | 本次事故中的缺口 | 最先失守的问 |
|---|---|---|
| 真相契约 | 运行中的对话没有真相源；唯一写路径挂在 run 收尾 | 看得见吗——运行中一轮在任何持久载体都查不到 |
| 转移契约 | 抢占转移没有定义旧 run 数据的归宿；后续复审又见 TOCTOU 间隙 | 看得见吗——帧 7 的抢占决策没有事件 |
| 副作用契约 | 擦边：工具的文件改动实时落盘，但归属消息可随进程终止丢失 | 看得见吗——外部改动与对话的账断了归属 |
| 交互契约 | 断开安全但无接回；后台完成零通知；用户依据过期画面做出致损决策 | 扰动下稳吗——断开这个扰动把投影推离真相 |
| 权限契约 | 一次点击就把运行时容器带离应用；导航边界零防线 | 管得住吗——webview 的去向没有任何干预点 |
| 证据契约 | 3.4 那份缺失证据清单本身 | 看得见吗——十帧没有一帧有运行时记录背书 |

## tb-04-1 · 04-blueprint.md · 原 L14

| 栏 | 状态层（单机基线：SQLite，WAL 模式） |
|---|---|
| 职责 | 持久真相的唯一落点，回答"现在是什么"；允许写它的组件只有一个 |
| 边界 | 不答"怎么来的／凭什么信"（归事件流与证据存储）；不做业务裁决；不为读侧长花样 |
| 接口 | 写侧仅执行路径经单一写者入库；读侧全组件只读 |
| 主守契约与守约方式 | 真相契约——单写者串行化并发写；持久对象带 owner 与 version；状态变化落事件 |
| 替代方案与取舍 | 单机 SQLite 单写者（换掉一类并发问题，上限吞吐）；多实例 Postgres＋lease（"谁是写者"降为协议保证）；内存＋快照已被第一章 1.4 排除（败在状态撕裂） |
| L 级起步预期 | L2——状态变化有事件可查。低于 L2 的状态层，就是第三章那套系统的样子 |

## tb-04-2 · 04-blueprint.md · 原 L69

| 本卷组件 | Temporal | LangGraph（OSS 图库） | Claude Code |
|---|---|---|---|
| 状态层 | workflow state（重放重建） | checkpointer 持久化的 state dict | session jsonl（同一份，状态即回放） |
| 事件流 | event history（核心资产） | checkpoint 序列（近似） | transcript 事件行（与左格同一制品） |
| 证据存储 | —（history 兼职，无验证归档位） | —（无独立证据层，checkpoint 不含验证结论） | transcript 兼职，无独立对账层 |
| run manager | Temporal Server（准入/重试/定时） | —（OSS 库：invoke 由调用方自管；托管的 Agent Server 有 Runs API、cron jobs 与 double-texting 四裁决，这格由平台盖住） | 单进程内隐式（session 级） |
| agent loop | workflow 代码（须确定性） | graph 的节点执行 | 内置 agent loop |
| model adapter | activity（记录复用不重调） | 节点内自调（无调用级留档，崩在节点半途即重调） | 内置（transcript 留档） |
| tool executor | activity（同上） | tool node（副作用语义自管） | tool_use 块＋hook/permission 门 |
| 入口层 | client SDK | 调用方应用 | CLI/IDE 前端 |

## tb-05-1 · 05-run-lifecycle.md · 原 L32

| 状态 | 回答的处境 | 停留上限与超时归宿 |
|---|---|---|
| queued | 已接受、未执行（互斥或额度） | 排队超时→cancelled（queue_expired） |
| running | 正在消耗执行资源 | 心跳超时→看门狗按基础设施失败收尾（5.8） |
| waiting | 等一个系统给不出的输入 | 自带 deadline，过期是显式终态 |
| interrupted | 进程非自愿消失，任务未完 | 由恢复裁决送往续跑或终态（第七章） |
| completed / failed / cancelled | 三种结局，下游行为不同 | 终态即终点 |

## tb-05-2 · 05-run-lifecycle.md · 原 L52

| 当前状态 | 触发事件 | guard | 目标状态（终结原因） |
|---|---|---|---|
| queued | 内核派发 | 同会话无活跃 run 且额度足够 | running |
| running | 新意图触发抢占 | 旧 run 半轮内容已终态化落盘 | cancelled（preempted） |
| running / waiting | 启动扫描发现进程不在 | 进程标识已消失 | interrupted |

## tb-06-1 · 06-state-persistence.md · 原 L16

| 级 | 实体 | 一句定义 | 关键裁决 |
|---|---|---|---|
| 1 | Conversation | 用户视角的持续对话，消息的归属容器 | 可以没有——scheduler/webhook 触发的 run 不挂会话 |
| 2 | Run | 一次触发到终态的执行（第五章的主角） | subagent 归为 child run（parent_run_id），非独立实体 |
| 3 | Turn | 一次用户意图之内的完整交互回合 | 不设独立表——messages/steps 上的 turn_no 单调递增 |
| 4 | Step | 一次模型决策及其工具结果的闭环 | 恢复粒度锚点：从最后完整 step 之后继续（第七章） |
| 5a | Invocation | 一次真实发生的模型调用 | 每次调用一行，失败的调用也留档——invocation 即 attempt |
| 5b | Tool Execution | 一次工具副作用（Effect Ledger 一行） | 重试记在 attempt_no 上，不另立实体 |

## tb-06-2 · 06-state-persistence.md · 原 L69

| 保存 | 明确不保存（及理由） |
|---|---|
| 消息游标、最后完整 step 序号 | 文件系统与外部副作用——另有账本（第八章），回滚是另一件事 |
| compaction 版本与摘要引用 | 授权——approval、delegation 不随 checkpoint 走，安全默认不隐式恢复（6.11 节） |
| state_machine_version 等版本钉 | 模型内部状态——不可得，invocation 记录代之 |
| 包含物清单本身 | ——每个 checkpoint 自述包含什么；不完整的 checkpoint 必须可识别、必须丢弃 |

## tb-07-1 · 07-durable-execution.md · 原 L36

| | checkpoint 路线 | journal 路线 |
|---|---|---|
| 持久单位 | 节点边界的状态快照 | 每个操作的调用与结果 |
| 恢复方式 | 读最近快照，从断点继续 | 重放代码，已完成步骤按账本返回 |
| 对代码的要求 | 状态可序列化 | workflow 段必须确定性，不确定操作全部出账 |
| 代表 | LangGraph（三档 durability） | Temporal、Restate（event history / journal） |

## tb-07-2 · 07-durable-execution.md · 原 L69

| 操作 | 状态 | 执行 | 副作用 | 授权 |
|---|---|---|---|---|
| resume | 从最后完整点继续，历史不动 | 接着跑未完成部分 | 已记录的不重做；intent 无 result 的进对账（第八章） | 不自动延续，按 Lifetime Matrix 逐项重验（第十一章 11.6 节） |
| replay | 只读重建，不新增历史 | 决策重演，用于审计与调试 | 零副作用——重放读账本 | 无需授权（只读） |
| fork | 复制历史开新分支，原线不动 | 两条线各自独立往前 | 新分支的动作是新账，从零记 | **不复制**——新分支按新 run 重新走授权 |
| time travel | 回到历史某个 checkpoint 分叉 | 从旧状态重新出发 | 旧分支已发生的副作用不消失——回到过去改不了已寄出的邮件 | 同 fork，不继承 |

## tb-08-1 · 08-tools-effects.md · 原 L84

| 处置 | 适用条件 | 动作 | 账的终局 |
|---|---|---|---|
| 重试 | action class 为 idempotent，key 在保留期内 | 同 key 重发，记新 attempt_no | retried——result 补齐，最坏也只是"再确认一次" |
| 查询 | 目标系统提供读接口 | 查远端实况，回填 outcome | queried——账收平，动作一次没多做 |
| 补偿 | action class 为 compensatable | 执行逆操作，记一笔新 effect | compensated——补偿也是副作用，也走四段账 |
| 未知 | 以上都不可用 | 标 unknown，呈现给人 | manual——诚实交给人裁决 |

## tb-08-2 · 08-tools-effects.md · 原 L109

| 目标系统 | 天然能力 | 首选调和 | 陷阱 |
|---|---|---|---|
| 本地文件 | 可读回校验（存在性、checksum） | 查询对账 | 旁路写：不经工具的写入不进账（8.10 节） |
| HTTP API | 取决于对端：幂等 key？查询端点？ | 幂等重试，或查询回填 | "超时但远端已成功"且对端不可查——只能 unknown |
| 数据库 | 事务 | 事务边界内天然原子 | 跨库、跨事务的写退回 dual-write 处境 |
| 消息队列 | 至少一次投递＋消费端去重 | 幂等消费 | broker 承诺的 exactly-once 只覆盖 broker 内部 |
| 支付 | 双边记账，有对账单 | 定期对账 | 实时接口的成败与日终对账单可能不一致 |

## tb-14-1 · 14-build.md · 原 L60

| fixture | 出处 | 破坏场景 | 主守契约 |
|---|---|---|---|
| contract test | 第五章 | 双入口同触发／双进程同 resume／同请求重发／入口语义分叉 | 转移 |
| atomicity fixture | 第六章 | 消息落库／compaction 摘要／artifact 登记，三处相邻写入两两之间 kill -9 | 真相（原子性） |
| replay fixture | 第七章 | 工具副作用已发生、结果未记录时杀进程 | 副作用（恢复侧） |
| reconciliation fixture | 第八章 | 超时远端已成功／成功但 artifact 缺失／policy 变化拒 stale lease／单步 mismatch 废队列 | 副作用 |
| cancel propagation test | 第九章 | 断网重连／刷新页面／抢占／审批跨会话恢复 | 交互 |
| compaction fixture | 第十章 | 压缩中断／摘要遗漏系统约束／memory 污染／resume 读旧版本 | 真相（连续性） |
| permission fixture | 第十一章 | subagent 越权／恶意 tool result／过期 delegation 后 resume／secret 进 sandbox／关闭共享件 | 权限 |
| coordination fixture | 第十二章 | 越权 subagent／并发写同一 artifact／慢 subagent 阻塞／恶意回传 | 权限＋副作用（父子） |
| detector/certificate fixture | 第十三章 | 吞错误／关检测器／成功但无 artifact／模型漏洞 | 证据 |

## tb-14-2 · 14-build.md · 原 L86

| 触发信号 | 从 | 切到 |
|---|---|---|
| 多写者／单机备份不够用 | SQLite | Postgres |
| 多实例并发 | 单例 | 分布式锁或 lease |
| 工具子进程要沙箱／隔离 | 进程内任务 | worker queue |
| 跨实例分发事件 | 进程内广播 | 事件总线 |

## tb-15-1 · 15-review.md · 原 L22

| 工具 | 出处 | 评审时逐项问 | 对不上意味着 |
|---|---|---|---|
| Component Register（工作制品 G） | 第四章 | 八张组件卡逐张对位被评系统自画的组件图 | 缺了哪个组件、哪份契约没人守 |
| State Registry（工作制品 A） | 第六章 | 每个状态的 owner／存储／版本／读写者 | 状态无主、多写者互相覆盖、无版本可回滚 |
| Effect Ledger（工作制品 B） | 第八章 | 每个副作用的意图／权限／执行／幂等／outcome／调和 | 副作用没账、没幂等、拿 result 当 outcome |
| Runtime Trust Boundary（工作制品 D） | 第十一章 | 进程／网络／身份／工具／信任边界怎么跨、怎么对账 | 边界糊、软提示当硬边界用 |
| Runtime Contract Matrix | 六契约横轴承自第一章（六契约立于 1.2 节）；五审查维度是本章新起的评审镜 | 六契约 × 正确性／可靠性／安全／用户反馈／可测试性 | 哪一格空着、哪份契约根本没有检验 |

## tb-15-2 · 15-review.md · 原 L61

| 残余风险 | 契约 | 触发场景 | owner | 期限 |
|---|---|---|---|---|
| 工具超时后重试，远端已成功 | 副作用 | reconciliation fixture | （第三卷 owner） | — |
| subagent 继承父的全放行 | 权限 | permission fixture | （第三卷 owner） | — |
| 某检测器从未验证过会触发 | 证据 | detector/certificate fixture | （第三卷 owner） | — |

## tb-90-1 · 90-artifacts.md · 原 L9

| 节 | 名称 | 一句用途 | 交付章 |
|---|---|---|---|
| A | State Registry（状态注册表） | 每个持久状态对象的 owner、存储、删除语义、崩溃后归宿 | 第六章 6.0（v5.4 自第一章下沉） |
| B | Effect Ledger（副作用账本） | 一次工具执行的四段账：intent→attempt→result→outcome | 第一章登记结构，第八章主场 |
| C | Event Schema（事件信封与类型表） | 事件流的信封字段、事件类型与四条纪律 | 第一章登记结构，第十三章主场 |
| D | Runtime Trust Boundary（运行时信任边界） | 每条信任边界的跨越方式、失败模式与对账机制 | 第十一章填充 |
| E | Entry-to-Kernel Routing Matrix（入口到内核路由矩阵） | 每个入口六列，验证 permission/cancel/resume/工具执行只在内核 | 第五章 5.11 |
| F | Intervention Point Map（干预点图） | assemble/model/execute 三处干预点的平面归属与留证 | 第十一章 11.7 |
| G | Component Register（组件卡登记册） | 八组件卡完整六栏，第十五章评审的对照标尺 | 第四章 |
| H | Run 状态转移表 | run 的全部合法转移（17 行），转移契约的合同全文 | 第五章 5.3 |
| I | Lifetime Matrix（携带物生命周期矩阵） | checkpoint/resume 携带物逐项声明，安全默认不隐式恢复 | 第六章 6.11 |
| J | Projection Contract（投影契约） | 投影三条契约（有来源/可重建/不回写）与违约形态 | 第六章 6.3 |
| K | Belief/World Model Registry（信念工件登记模板） | 信念版本六字段：版本/history cursor/provenance/scope/反例/继任链 | 第六章 6.12 |
| L | 恢复语义表与 durability 选型记录 | 四操作×四后果（L1）＋两路线选型条件（L2） | 第七章 |
| M | Tool Contract（工具契约模板） | 每个工具一份：三层校验、action class、幂等与调和声明、取消语义、派生清单、错误报文 | 第八章 8.11 |
| N | Plan Lease 与 Counterexample Event Contract（计划租约与反例事件契约） | 计划的适用前提与失效条件；预测落空即废止剩余队列的控制流事件 | 第八章 8.12 |
| O | Stream Terminal Table（流终结真值表） | 流的每种收尾一行、判成功或失败、默认 fail closed | 第九章 9.4 |
| P | Interaction Semantics Table（交互语义表） | disconnect/cancel/interrupt/suspend 四词 × 对 run 的影响 × 触发转移 × 半轮归宿 | 第九章 9.5 |
| Q | Context Assembly Spec（上下文组装规格） | context 组装的来源/优先级/预算/去重/可信度——投影而非容器 | 第十章 10.1 |
| R | Compaction Contract（压缩契约） | 压缩事务的四条纪律：失败回退/边界落盘/系统约束不进压缩/配对修复 | 第十章 10.3 |
| S | Memory Provenance（记忆来历登记） | memory 每条的 provenance/TTL/撤销标记/scope | 第十章 10.5 |
| T | Principal & Delegation Registry（主体与委托登记） | principal 五类 × 委托记录（授予者/scope/期限/再委托/撤销） | 第十一章 11.1 |
| U | Authority Lifecycle Matrix（授权生命周期矩阵） | 授权的授予/范围/期限/失效条件/恢复重验——恢复≠恢复授权 | 第十一章 11.6 |
| V | Common-mode Failure Matrix（共因失效矩阵） | 每层防御的六列：强制点/失效模式/共享件/fail-open·closed/兜底/证据 | 第十一章 11.5 |
| W | Parent-Child Run Contract（父子 run 契约表） | 六契约 × 单 agent 形态/父子继承规则/失效反例，加收敛判据与输出信任两项协调专属 | 第十二章 12.8 |
| X | Evidence Graph（证据图） | 对账边（动作/结果/artifact/完成）＋认识论七边（grounds/predicts/certifies/refutes/derived_from/realizes/invalidates） | 第十三章 13.8 |
| Y | Detector Test Record（检测器测试记录） | 每个检测器的 sabotage 验证：喂什么坏样本/期望触发/实际触发/上次验证时间 | 第十三章 13.6 |
| Z | Model Certificate（模型证书） | 五类测试（replay/prospective/held-out/invariant/planner-adversarial）＋scope/history cursor/生成 provenance/已知反例 | 第十三章 13.8 |

## tb-90-2 · 90-artifacts.md · 原 L44

| 状态对象 | owner（唯一写者） | 存储（单机参考实现） | 关键字段 | 读者 | 删除语义 | 崩溃后归宿 |
|---|---|---|---|---|---|---|
| conversation | Control（run manager 代理用户操作） | `conversations` | id、tenant、created_at、schema_version | Interaction（投影）、Execution（组装 context） | 用户删除；派生物传播规则 6.10 节裁决 | 无中间态（单行原子写） |
| run | Control（run manager） | `runs` | id、conversation_id（可空）、parent_run_id、triggered_by、status、terminal_reason、state_machine_version | 全平面 | 不可单独删；随 conversation 删除时保留审计副本与否 6.10 节裁决 | status=running 的孤儿由启动扫描收敛（5.8 节） |
| message | Execution（agent loop 经写路径） | `messages` | id、conversation_id、run_id、turn_no、role、content_ref、schema_version | Interaction、Execution | 随 conversation | 半轮内容归宿 9.7 节裁决；已落库的不回滚 |
| turn | —（无独立表） | `messages`/`steps` 上的 turn_no | turn_no 单调递增 | — | 随所属对象 | 以最后完整 step 判定 turn 完成度 |
| step | Execution | `steps` | id、run_id、turn_no、seq、status（不设 kind——模型调用与工具执行是 5a/5b 级子实体，各以 step_id 挂在 step 下，6.0 节实体链） | Control（恢复扫描）、Evidence | 随 run | **恢复粒度锚点**：从最后完成 step 之后继续（第七章） |
| invocation 记录 | Execution（model adapter） | `invocations` | id、step_id、model_id、prompt_asset_ref（含版本号或内容哈希，塑形片段按它重建，10.8 节）、context_digest、output_ref、token 计量、schema_version | Execution（重放复用）、第三卷成本 | 随 run；内容脱敏另议（vol3） | 已记录的结果恢复时复用，不重新调用（第七章） |
| effect（Effect Ledger 行） | Execution（tool executor） | `effects` | 见本文件 B 节 | Control、Evidence、人工对账 | **原则上不删**——外部世界的账 | intent 无 result → 四类处置（8.6 节） |
| checkpoint | Execution（经 checkpoint 写路径） | `checkpoints` | id、run_id、step_id、包含物清单、compaction_version、state_machine_version | Control（resume） | 随 run；保留策略 vol3 | 不完整 checkpoint 必须可识别并丢弃 |
| compaction 摘要 | Execution（compaction 事务） | `messages` 特型行（第十章裁决：不独立表，沿特型行；推翻＝需独立版本审计/跨会话复用） | compaction_version、provenance（由哪些消息压成）、边界序号 | Execution（context 组装）、resume | 随 conversation | 压缩事务失败回退，不留半压缩态（10.4 节） |
| memory | Execution（memory 写路径；单机参考实现可不实现，字段契约见 S 节） | `memory`（未实现前占位，模板见 S 节） | provenance、ttl、revoked/revoked_by、scope、content_ref | Execution（context 组装） | 撤销可追溯（10.5 节、删除三义 6.10 节） | 随所属 conversation/项目；撤销标记持久 |
| artifact | Execution（tool executor 经登记路径） | `artifacts` + 文件/对象存储 | id、lineage（创建/修改它的 effect）、checksum、version | 全平面 | 删除 ≠ 撤销外部动作（6.10 节） | 文件在而登记缺、登记在而文件缺——两向对账（工具层展开 8.10 节，证据边第十三章） |
| approval（HITL 待决） | Control | `approvals` | id、run_id、请求内容、requested_at、expires_at、resolved_by、decision | Interaction（呈现）、Execution（等待） | 随 run；过期是显式终态 | **挂起即持久化**：重启后待决审批仍在（9.8 节）；但已决 approval 的效力不随 resume/fork 自动延续——authority 不隐式恢复，需持久化的授权显式列入契约并在变化后重验（11.6 节） |
| timer | Control | `timers` | id、run_id、fire_at、purpose、status | Control（扫描） | 随 run | 进程死后由启动/周期扫描接管（7.7 节） |
| event | Evidence（各组件追加） | `events` | 见本文件 C 节 | 全平面（只读） | **永不更新、原则上不删**；保留策略 vol3 | 未提交事务整体回滚，不留半行；应用层守事务边界——状态行与事件同事务落地（6.1 节、C 节纪律 3） |
| policy decision | Control | 并入 `events`（type=policy.decided）——第十一章裁决不独立表；推翻＝需独立于事件流的合规审计/长期保留 | principal、规则、输入摘要、决定、依据、enforcement point | Evidence、审计 | 同 event | 同 event |
| belief/world model | Execution（建模路径） | `world_models`（派生工件表，在十一张实体链表之外；未实现前占位，模板见 K 节） | model_version、history_cursor、provenance、certificate_scope、known_counterexamples | Execution（规划）、Evidence | 随所属 conversation/task；版本不可变 | **derived belief artifact，不是真相**：崩溃后取最新已认证版本，不覆盖 observation（6.12 节） |

## tb-90-3 · 90-artifacts.md · 原 L73

| 字段 | 说明 |
|---|---|
| effect_id | `eff_` 前缀 ID |
| run_id / turn_no / step_id | correlation 链 |
| tool_name / params_ref / params_hash | 调了什么、参数指纹 |
| idempotency_key | **派生自 run_id + step 序号 + 该 step 内的 effect 序号**（第三维也可直接用模型返回的 tool_call_id），不用内存计数器——同一 step 挂多笔工具调用时各自唯一，同一笔的多次 attempt 之间不变 |
| action_class | read_only / idempotent / compensatable / non_replayable——重发语义登记（第八章 8.4；v1 的 risk_class 细化为此四类，Control 决策输入沿用） |
| derived_from_effect_id | 派生副作用指回原 action；空即自身为原 action（第八章 8.3 纪律二） |
| committed_under | 提交时校验通过的执行权凭据——单机为进程内租约标识，多实例为 fencing 编号（第八章 8.3） |
| policy_decision_ref | 谁批准的（指向 policy decision） |
| intent_at | 意图落盘时刻——**必须先于执行** |
| attempt_no / last_attempt_at | 尝试可多次 |
| result_status / result_ref / result_at | 工具返回（成/败/超时/已取消），只记一次 |
| outcome_status / outcome_evidence_ref | 外部世界真实结果 + 独立证据（verifier、对账、artifact 校验） |
| reconciliation_status | none / retried / queried / compensated / manual / **unknown** |
| schema_version | — |

## tb-90-4 · 90-artifacts.md · 原 L105

| 处置 | 适用条件 | 动作 | 账的终局（reconciliation_status） |
|---|---|---|---|
| 重试 | action_class=idempotent 且 key 在保留期内 | 同 key 重发，记新 attempt_no | retried（result 补齐） |
| 查询 | 目标系统提供读接口 | 查远端实况，回填 outcome | queried |
| 补偿 | action_class=compensatable | 执行逆操作，记一笔新 effect | compensated |
| 未知 | 以上都不可用 | 标 unknown，呈现给人 | manual |

## tb-90-5 · 90-artifacts.md · 原 L116

| 字段 | 说明 |
|---|---|
| event_id | `evt_` 前缀 ID |
| seq | 数据库自增序号——**顺序的真相**（6.0 节全局规则一，不信 ID 里的时间戳） |
| occurred_at | 挂钟时间，仅供人读 |
| tenant / conversation_id / run_id / turn_no / step_id / invocation_id / effect_id / artifact_id | correlation 八级全量冗余，允许为空的层级显式置空（第十三章补全 invocation/effect/artifact 三级——child 事件带父 run_id 即第十二章跨 agent 因果链的兑现） |
| type | 见下 |
| payload / payload_ref | 小负载内嵌，大负载外置引用（stub/body 分离，入门卷 5.6 节） |
| source | 产生事件的组件 |
| schema_version | — |

## tb-90-6 · 90-artifacts.md · 原 L150

| 边界 | 跨越方式 | 跨越时信任如何变化 | 典型失败模式 | 对账/证据机制 |
|---|---|---|---|---|
| 进程 ↔ 子进程 | spawn，进程组绑定 | 子进程应收窄权限，不自动继承父全权 | 子进程比 run 活得久、脱离生命周期（8.8 节） | 进程组收割＋run 终态事件 |
| 主进程 ↔ worker | 多实例任务派发 | worker 持临时授权、非持久 | 双 worker 同认领、慢者带旧 fencing 写（5.8 节） | fencing 高水位＋认领事件 |
| agent ↔ subagent | 派生 child run | 权限默认收窄，绝不继承 bypass | 继承父全权（11.3 节） | Principal & Delegation（T）＋policy decision |
| runtime ↔ 网络/provider | 对外请求（egress） | 出口即副作用，信息可外流 | "只读"工具藏 web 外发、跑在 policy 前（11.4 节） | egress 过 policy 门禁＋policy.decided |
| runtime ↔ 数据库 | 读写持久状态 | 单写者/租约约束（第六章） | dual-write、跨库事务撕裂 | 事务＋事件双轨（6.1 节） |
| runtime ↔ 工具/沙箱 | 工具执行，沙箱隔离 | 沙箱默认拒绝、显式放行 | secret 进沙箱、可写路径过宽 | bubblewrap 分层＋Effect Ledger（B） |
| runtime ↔ 用户 | 交互面投影 | 投影不回写、外来输入默认不可信 | UI 当真相源（第三章/第九章）、prompt 注入 | 投影契约（J）＋信任标签 |

## tb-90-7 · 90-artifacts.md · 原 L164

| 入口 | 意图适配 | 流转发 | permission | cancel | resume | 工具执行 |
|---|---|---|---|---|---|---|
| UI | 消息/操作→intent（携 idempotency key） | 订阅事件流重建投影 | 内核 | 内核 | 内核 | 内核 |
| API | 请求体→intent（调用方自带 key） | SSE / 轮询 | 内核 | 内核 | 内核 | 内核 |
| IM 渠道 | 平台消息→intent | 消息回推（异步分片） | 内核 | 内核 | 内核 | 内核 |
| scheduler/timer | timer.fired→intent | 无人值守：结果走库与通知 | 内核 | 内核 | 内核 | 内核 |
| webhook | 外部事件（验签）→intent | 无人值守：结果走库与通知 | 内核 | 内核 | 内核 | 内核 |
| SDK/CLI | 调用→intent | 流式回调 / stdout | 内核 | 内核 | 内核 | 内核 |

## tb-90-8 · 90-artifacts.md · 原 L175

| 干预点 | 平面边界 | 回答的问题 | 挂载机制 | 证据 |
|---|---|---|---|---|
| assemble | State→Execution（投影） | 模型这次看见什么 | context assembly（工作制品 Q，10.1 节） | 组装决策落 policy.decided |
| model | Control→Execution | 这次可选哪些工具/动作 | tool 暴露与 policy（11.3 节） | 暴露决策落 policy.decided |
| execute | Control→Execution/外部世界 | 是否授权并真正执行 | approval/sandbox/effect intent（8.3 节） | effect intent＋policy.decided |

## tb-90-9 · 90-artifacts.md · 原 L188

| 组件 | 职责一句 | 边界（明确不做什么） | 上下游接口 | 主守契约与守约方式 | 替代方案与取舍 | L 级起步 |
|---|---|---|---|---|---|---|
| 状态层 | 持久真相唯一落点，答"现在是什么" | 不答"怎么来的/凭什么信"；不做业务裁决；不为读侧长花样 | 写侧仅单一写者；读侧全组件只读 | 真相——单写者串行化＋owner/version＋状态变化落事件 | SQLite 单写者 vs Postgres+lease（多实例）vs 内存+快照（死于撕裂） | L2 |
| 事件流 | 发生过什么的机器可读记录（append-only） | 不当队列用（无投递承诺）；不存大负载（stub/body 分离） | 统一 emit 路径写入；恢复扫描/UI 订阅/审计读 | 转移——每次转移随行 trigger/guard/终结原因 | 单机表 vs 消息队列（投递语义换运维与可对账性）；可变行+审计表已排除（第一章 1.4） | L2 |
| 证据存储 | trajectory/policy 决策/verifier 结论/artifact 来历归档 | 只存不判；不管实时呈现 | 归档写入；对账/回放/评审读 | 证据——归档独立于声称方 | 与事件流合储 vs 分储（访问模式分离换一条归属线） | L2 |
| run manager | 单执行内核：准入/互斥/policy/limit/孤儿收敛 | 不碰模型与工具；不长业务逻辑 | 入口层唯一下游；run 记录与终态持有者 | 转移+权限裁决点，交互收敛义务——三类决策有事件 | 内核集中 vs 入口自治（单点与评审瓶颈换语义只实现一次）；Routing Matrix 第五章 5.11 | L2 |
| agent loop | 一轮任务编排：组装 context→调模型→执行工具→循环 | 不持久真相（内存即易失）；不自证正确 | 由 run manager 派发；产出经他卡落盘 | 全契约履约现场，不单独 own | 手写同步循环 vs graph 引擎（声明式能力换落盘点透明）；两种 graph 第八章 8.12 | L1→L2（每步 emit） |
| 入口层 | 适配意图＋转发流（UI/API/IM/scheduler） | 投影不回写；不实现 permission/cancel 捷径 | 只对 run manager | 交互呈现半边——正确性押在"不写" | 薄投影 vs 胖客户端缓存（离线体验换第二真相源） | L1 |
| model adapter | 模型调用记账员：留档复用不重调 | 不做 routing 裁决；不解释输出 | loop 调用；恢复路径读档 | 转移+证据（调用记录即事件）——Temporal activity 先例 | 库内适配 vs 独立网关（集中计量换一跳延迟与新单点） | L2 |
| tool executor | 副作用唯一大门：先落盘意图→执行→落盘结果 | policy 判定不在此；结果解释不在此 | loop 调用；执行裁决结果；账本供对账 | 副作用——intent/result 双事件，外部另取证据 | 进程内 vs 子进程沙箱 vs 远端 worker（隔离强度换执行开销） | L2 |

## tb-90-10 · 90-artifacts.md · 原 L203

| # | 当前状态 | 触发事件 | guard | 目标状态 | terminal_reason | 随行事件 |
|---|---|---|---|---|---|---|
| 1 | —（创建） | 入口意图经准入 | policy/limit 通过；同 idempotency key 无既有 run | queued | — | run.created |
| 2 | queued | 内核派发 | 同会话无活跃 run 且并发额度足够 | running | — | run.state_changed |
| 3 | queued | 用户取消 | — | cancelled | user_cancelled | run.state_changed＋run.finalized |
| 4 | queued | 排队超时（timer.fired） | 超过排队 deadline | cancelled | queue_expired | 同上 |
| 5 | running | 终答落盘 | 终答与消息终态已入库 | completed | — | run.finalized |
| 6 | running | 业务失败 | 失败已归因 | failed | task_failed | run.finalized |
| 7 | running | 基础设施失败 | 重试预算耗尽 | failed | infra_failure | run.finalized |
| 8 | running | 看门狗心跳超时（进程存活） | 超过 deadline 无活跃事件（step/effect 最近时刻为存活信号，第七章 7.6） | failed | infra_failure | run.finalized |
| 9 | running | 策略/预算拦截 | policy.decided=deny 或预算耗尽 | failed | policy_rejected / budget_exceeded | policy.decided＋run.finalized |
| 10 | running | 用户 Stop | 半轮内容已终态化落盘 | cancelled | user_cancelled | run.finalized |
| 11 | running | 新意图触发抢占（裁决=interrupt） | 旧 run 半轮内容已终态化落盘 | cancelled | preempted | run.state_changed＋run.finalized |
| 12 | running | 需人工输入/审批（approval.requested） | 挂起已持久化 | waiting | — | run.state_changed |
| 13 | waiting | 审批/回复到达（approval.resolved） | 授权仍有效（11.6 节重验） | running | — | run.state_changed |
| 14 | waiting | 挂起过期（approval.expired） | 超过 waiting deadline | cancelled | hitl_expired | run.finalized |
| 15 | running / waiting | 启动扫描（进程已消失） | 进程标识已消失 | interrupted | — | run.state_changed |
| 16 | interrupted | resume 裁决可续跑（第七章） | state_machine_version 兼容且 checkpoint 完整 | queued | — | run.state_changed |
| 17 | interrupted | resume 裁决不可恢复 | — | failed | unrecoverable | run.finalized |

## tb-90-11 · 90-artifacts.md · 原 L229

| 携带物 | 随 checkpoint 保存？ | 随 resume 恢复？ | 恢复前重验？ | 所属生命周期 |
|---|---|---|---|---|
| 消息游标 / 最后完整 step 序号 | 是 | 是 | 否 | 状态 |
| compaction 版本与摘要引用 | 是 | 是（必须尊重边界，10.8 节） | 否 | 状态 |
| prompt asset · 塑形片段（few-shot／输出格式／流程模板） | 是（记版本号或内容哈希） | 是（按记录的版本重建，10.8 节） | 否 | 状态 |
| prompt asset · 系统约束片段（身份／安全规则） | 否 | 否（恢复时取当前版，不取旧版） | — | 授权 |
| state_machine_version | 是 | 是 | 版本兼容检查（5.10 节） | 执行 |
| approval（已决审批） | 否（决策证据留 events） | 否 | 需重验（11.6 节） | 授权 |
| delegation token | 否 | 否 | 重新授予 | 授权 |
| credential / secret | 否 | 否 | 重新获取 | 授权 |
| 工具子进程 / 沙箱句柄 | 否 | 否（重建） | — | 执行 |
| 内存 lease / 执行权 | 否 | 否（单机重启即失效；多实例为授权账协议保证，6.0 节裁决、主场第八章） | 重新取得 | 授权 |

## tb-90-12 · 90-artifacts.md · 原 L246

| 契约 | 含义 | 违约形态（已见现场） |
|---|---|---|
| 有来源 | 投影每个成分都能指回持久对象 | 来源藏隐式键（按目录编码的会话存储，6.5 节）；memory 来历不明（10.5 节） |
| 可重建 | 任何投影可从持久态再生，不携带独家信息 | 内存攒半轮成果（第一章 agent loop 约束）；客户端缓存当真相（第三章缺口二） |
| 不回写 | 投影侧缓存/猜测/修补不得进入真相 | UI 超时标 failed（第一章 1.6）；localStorage 恢复线（第三章） |

## tb-90-13 · 90-artifacts.md · 原 L256

| 字段 | 说明 |
|---|---|
| model_version | 单调递增，版本内容不可变 |
| history_cursor | 生成所基于的事件序号区间 |
| provenance | 生成它的模型/提示/工具版本 |
| certificate_scope | 认证范围与保证边界（全历史回测只证明 retrodictive consistency） |
| known_counterexamples | 已知反例的事件引用 |
| refuted_by / superseded_by | 吊销与继任链 |

## tb-90-14 · 90-artifacts.md · 原 L269

| 操作 | 状态 | 执行 | 副作用 | 授权 |
|---|---|---|---|---|
| resume | 从最后完整点继续，历史不动 | 接着跑未完成部分 | 已记录不重做；intent 无 result 进对账（第八章） | 不自动延续，按 I 节 Lifetime Matrix 逐项重验（11.6 节） |
| replay | 只读重建，不新增历史 | 决策重演（审计/调试） | 零副作用 | 无需授权 |
| fork | 复制历史开新分支 | 两线独立 | 新分支新账 | 不复制，按新 run 重新授权 |
| time travel | 回历史 checkpoint 分叉 | 从旧状态重新出发 | 旧分支已发生的副作用不消失 | 同 fork |

## tb-90-15 · 90-artifacts.md · 原 L278

| 条件 | 单机最低充分解（事件表＋intent/result＋启动扫描＋timer 扫描） | checkpoint 引擎（LangGraph 类） | journal 引擎（Temporal/Restate 类） |
|---|---|---|---|
| 单机单实例、本地副作用为主 | **默认选择**（第七章 7.10 七步时序） | 图编排需求强时可用，三档 durability 显式选 | 确定性改造税通常不划算 |
| 编排跨进程/跨服务 | 不够——需自建协调 | 三件缺口自建（失败检测/恢复触发/跨实例协调） | **值回票价**：账本一致性＋单派发 |
| durable timer 密度高、错过成本高 | 自建扫描维护成本上升 | 同左 | 引擎 timer 原生 |
| LLM 结果复用 | invocation 留档（第六章/第七章 7.2） | 需自行保证节点内不重调 | Activity 结果缓存原生 |

## tb-90-16 · 90-artifacts.md · 原 L291

| 维度 | 规格 |
|---|---|
| 来源 | 每个成分能指回一个持久对象（消息/摘要/检索片段/系统约束）；来路不明的不进 |
| 优先级 | 系统约束 > 当前任务态 > 近期历史 > 压缩摘要 > 检索片段；预算不足时按逆序丢 |
| 预算 | 总 token 卡在窗口预算内（留出输出与 attention 余量）；超预算触发压缩（工作制品 R） |
| 去重 | 同一事实/工具输出只保留一份，重复项折叠 |
| 可信度 | 外部检索内容标来源、降权；投影不回写——组装是选材，不改真相（工作制品 J） |

## tb-90-17 · 90-artifacts.md · 原 L305

| 纪律 | 内容 | 违约形态 |
|---|---|---|
| 失败回退 | 压缩是原子操作，中途失败整体回退到压缩前，不留半压缩态 | 摘要写一半、原文裁一截，两不着（崩溃面） |
| 边界落盘 | 登记 compaction_version 与边界序号（摘要由哪些消息压成、边界落在哪条） | 压完不记版本，resume 无从对齐 |
| 系统约束不进压缩 | 系统约束（必须/不许类）不放进可压缩段，或压缩后无条件重新注入 | 约束被摘掉，模型之后无声违反 |
| 配对修复 | 压缩后扫 tool_call/tool_result 配对，落单的一起压或一起留（第六章 6.7） | 摘要吞 result 留孤儿 call，下次调用当场报错 |

## tb-90-18 · 90-artifacts.md · 原 L318

| 字段 | 说明 |
|---|---|
| provenance | 哪个 run、基于哪些事件写的 |
| ttl | 有效期；过期即失效，不无限生效 |
| revoked / revoked_by | 撤销标记＋撤销来源，作废可追溯（删除三义，第六章 6.10） |
| scope | 会话/项目/全局——作用域即归属，注释自述不算数（第六章 6.2） |
| content_ref | 记忆正文引用（stub/body 分离） |

## tb-90-19 · 90-artifacts.md · 原 L330

| 栏 | 说明 |
|---|---|
| tool_name / 语义一句 | 这个工具动世界的哪一部分 |
| 参数 schema | 结构校验：类型、必填、取值范围；危险参数用形态防呆消除（如强制绝对路径） |
| 语义前置条件 | 路径存在、目标可写、状态允许——工具实现内校验 |
| action_class | read_only / idempotent / compensatable / non_replayable 四选一（与 B 表同枚举） |
| 幂等声明 | 天然幂等 / 靠 key（注明 key 来源与保留期）/ 不可重放 |
| 调和方式 | 可查询（读接口是什么）/ 可补偿（逆操作是什么）/ 都不可则显式登记"只能 unknown" |
| 长运行语义 | 预计时长档位；progress 通道；partial output 归宿（落 artifact 或丢弃） |
| 取消语义 | 接受信号＋宽限期 / 到提交点再拒绝——不接受中途放弃的工具必须选后者（第八章 8.8） |
| 派生副作用清单 | 会带出的后续动作（快照、索引、通知），逐项 derived_from 归属 |
| 错误报文契约 | 结构化：code / layer / retryable / sideEffectState（none-unknown-partial-committed 四值） |

## tb-90-20 · 90-artifacts.md · 原 L349

| 字段 | 说明 |
|---|---|
| plan_id | 计划标识 |
| model_version | 派生自哪个信念版本（工作制品 K 对应行） |
| history_cursor | 认证时所见的事件序号区间 |
| policy_version | 依据的 policy 版本 |
| preconditions | 显式前置条件（可校验断言） |
| expires_at | 时限——计划也有保鲜期 |

## tb-90-21 · 90-artifacts.md · 原 L364

| 字段 | 说明 |
|---|---|
| plan_id / model_version | 被废止的计划与被反驳的信念版本 |
| predicted / observed | 预测与观察（引用，非全文） |
| diff_ref | 差异详情引用 |
| invalidated_action_count | 废止的剩余动作数 |

## tb-90-22 · 90-artifacts.md · 原 L377

| 收尾方式 | 信号 | 判定 | 说明 |
|---|---|---|---|
| typed done | 明确的结束事件（带成功语义） | 成功 | 唯一无条件算成功的一行 |
| legacy `[DONE]` | 旧式哨兵字符串 | 成功（兼容） | 仅为向后兼容保留，新协议用 typed done |
| typed error | 流内错误帧（HTTP 200 之后） | 失败 | 配套中继服务审计的 P0 现场：客户端不得跳过错误帧后推定完成 |
| EOF 无 terminal | 连接自然结束但从未见结束标记 | 失败 | "循环跑完了"不是成功信号 |
| 半帧 | 最后一帧不完整 | 失败 | 按最后一个完整帧截断，缺尾不推定成功 |
| malformed | 帧格式错乱 | 失败 | 解析不了即失败，不 fail open |
| 非法 envelope | 信封字段非法/缺失 | 失败 | 协议违规，拒绝并留证 |

## tb-90-23 · 90-artifacts.md · 原 L393

| 词 | 含义 | 对 run 的影响 | 触发的转移（工作制品 H） | 半轮内容归宿 |
|---|---|---|---|---|
| disconnect（断开） | 网络连接断 | 不动 run，仅剥离流、等游标重连 | 无（不进转移表） | 不受影响，run 照跑照落盘 |
| cancel（取消） | 用户 Stop 终止 run | 终止 | running→cancelled（user_cancelled） | 终态化落盘（9.7 节） |
| interrupt（抢占） | 新意图，旧 run 让路 | 终止旧 run | running→cancelled（preempted） | 先终态化落盘、再进终态（第五章 5.5"抢占先收尾"guard） |
| suspend（挂起） | 等外部输入（审批/回答） | 暂停，不终止 | running→waiting；恢复 waiting→running；过期 waiting→cancelled（hitl_expired） | 保留在挂起点，恢复时授权重验（9.8 节、第十一章 11.6 节） |

## tb-90-24 · 90-artifacts.md · 原 L406

| principal | 是谁 | 权力来源 |
|---|---|---|
| user | 真正的权力源头 | 自身 |
| agent | 替用户干活的 | user 委托（代理身份则为 user 权力子集） |
| subagent | agent 派出的分身 | agent 委托、默认收窄 |
| tool / service | 被调用的外部服务 | 调用方按 scope 授予 |
| operator | 运维/管理员 | 独立授权，与 user 分开 |

## tb-90-25 · 90-artifacts.md · 原 L416

| 字段 | 说明 |
|---|---|
| grantor / grantee | 授予者 / 受权者 |
| scope | 授予的范围（能对什么做什么） |
| expires_at | 期限——授权也有保鲜期 |
| redelegatable | 能否再往下转授 |
| revoked / revoked_by | 撤销标记＋撤销来源 |

## tb-90-26 · 90-artifacts.md · 原 L428

| 授权对象 | 授予 | 范围 | 期限 / 失效条件 | 恢复时（resume/fork/replay） |
|---|---|---|---|---|
| approval（已决审批） | 请人签字 | 该次高风险动作 | 用完即止；expires_at 过期 | 不延续，重验（11.6 节、Lifetime Matrix） |
| session permission | mode/规则授予 | 该会话 | 会话结束即失效 | 不恢复，重新授予 |
| delegation token | 上游委托 | token scope | expires_at；授予者权限被收回即失效 | 不恢复，重新授予 |
| credential / secret | 密钥管理 | 特定资源 | 轮换周期 | 不恢复，重新获取 |
| lease / 执行权 | 认领取得 | 该 run 副作用提交 | 重启即失效（6.0 节、8.3 节） | 不恢复，重新取得 |

## tb-90-27 · 90-artifacts.md · 原 L442

| 层 | 强制点 | 失效模式 | 共享依赖 | fail-open / closed | 兜底 | 证据 |
|---|---|---|---|---|---|---|
| permission deny | 求值序最先 | 规则未覆盖 | 规则库 | fail-closed | — | policy.decided |
| sandbox | 系统调用层 | 路径规则过宽 | 无（内核强制） | fail-closed | — | 沙箱拒绝事件 |
| hook（软） | 工具执行前 | 解析失败即放行 | shell/解析器 | **fail-open（危险）** | 无 | 常缺（反例，11.2 节） |
| classifier（软） | 内容检查 | 误判/被绕 | 模型/规则 | 视配置 | permission | 判定事件 |

## tb-90-28 · 90-artifacts.md · 原 L455

| 契约 | 单 agent 形态 | 父子继承规则 | 失效反例 |
|---|---|---|---|
| 真相 | 持久状态是唯一真相源（工作制品 A） | child run 状态挂父，单一真相源不因分身分裂 | 每个 child 各存一份真相 → N 份漂移（主线四） |
| 转移 | run 状态机＋唯一转移表（工作制品 H） | child 状态机独立，父可观测、终态回报父 | child 卡死父不知（无 correlation） |
| 副作用 | 四段账＋幂等（工作制品 B） | child 的 effect 账挂父链，幂等 key 从父 run_id 派生 | child 副作用无账，重放双份 |
| 交互 | 交互面是投影（工作制品 J/P） | child 无直接交互面，progress 经父投影 | child 直连 UI，绕过父的收敛 |
| 权限 | 运行时硬边界＋授权有期限（工作制品 T/U） | 有效权限＝agent ∩ user 取交集，收窄不继承 bypass | 取并集或继承 bypass → 权限蔓延 / Cross-Agent 提权 |
| 证据 | 只追加＋全量关联（工作制品 C） | child trace 以父 run_id 关联，跨 agent 因果链可重建（第十三章展开） | child trace 与父断链，因果不可重建 |

## tb-90-29 · 90-artifacts.md · 原 L466

| 协调项 | 规则 | 失效反例 |
|---|---|---|
| 收敛判据 | 父显式定义（全成功／多数成功／关键子任务成功），并行产出在单点收敛写 | 无单一收敛点 → infinite handoff loop（谁都不 own 任务） |
| 输出信任 | child 回传默认不可信，经独立校验（校验器与被校验者不共享判断源）方采信 | 内部即可信 → 检查器信任被检查者（MAST 验证类失效 23.5%） |

## tb-90-30 · 90-artifacts.md · 原 L481

| 边 | 含义 |
|---|---|
| observation --grounds--> model_version | 观察为模型提供依据 |
| model_version --predicts--> transition | 模型预测某个转移 |
| history_set --certifies--> model_version | 完整历史为模型背书（**必带 scope**：只证 retrodictive consistency，不证 generalization） |
| counterexample --refutes--> model_version | 反例推翻模型 |
| plan --derived_from--> model_version | 计划从某模型版本派生（回指工作制品 N Plan Lease） |
| commit --realizes--> plan | 提交兑现计划 |
| mismatch --invalidates--> remaining_plan | 预测与观察不符即废止剩余计划（回指工作制品 N Counterexample Event） |

## tb-90-31 · 90-artifacts.md · 原 L495

| 字段 | 说明 |
|---|---|
| detector_id | 检测器标识 |
| watches | 它监控什么（哪类事件的缺席、哪种异常） |
| probe | 喂进去的已知坏样本（sabotage 输入） |
| expected | 期望的触发行为 |
| last_probed_at | 上次验证时间 |
| last_result | 上次验证是否触发（pass＝触发／fail＝没触发即报警器失效） |

## tb-90-32 · 90-artifacts.md · 原 L510

| 项 | 说明 |
|---|---|
| full-history replay | 完整历史逐步回放（retrodictive consistency） |
| prospective prediction | 下一步预测（未回放的前瞻） |
| held-out transition | 留出的转移／leave-one-episode-out（泛化侧） |
| invariant / property test | 不变量与属性测试 |
| planner-adversarial | planner 主动搜模型漏洞的计划，验证不被误当最优解 |
| scope / history cursor / 生成 provenance（模型/提示/工具版本）/ 已知反例 | 证书边界——兑现 6.12 节的四件随身证据，不能只写 backtest=green |
| 被认证的 model_version | 本证书覆盖哪个信念版本（工作制品 K 对应行） |

## tb-99-1 · 99-appendix.md · 原 L20

| 章·节 | 这一层的形态 |
|---|---|
| 第一章 1.3 | hook 假落地：机制有名字两个月、事件一条没有；立 L0-L5 尺与假落地诊断公式 |
| 第二章 | 判据自己会说谎：评测器出错时没有报警器会响，因为报警器就是它 |
| 第三章 | 半途设计——机制只接一半的线，比没有机制更危险（制造"已保障"假象）；假落地公式的桌面版再次命中 |
| 第十章 | 压缩最容易缺这一格：系统里有压缩功能（L1 在），trajectory 里查不到压缩事件与版本号（L2 缺）——压缩常被当成一次性动作，做完就忘 |
| 第十三章 13.6 | **主场收口**：诊断变成机制。absence-of-event 检测（声明态与运行态对账，缺席即告警）＋ sabotage validation（定期给检测器喂一个已知坏样本，验证它真会触发，结果记进工作制品 Y） |
| 第十四章 14.3 | 构造层判据：一份契约算不算点亮，看的是它的**失败 trajectory**——只演正常路径，证明的仅仅是"不出错时它能跑" |
| 第十五章 | 评审自己也会假落地：声称"每季度做架构评审"（有名字），却拿不出上次的残余风险清单与 owner 落实记录（无证据） |
| 各章 L 级自检 | "半格"记账：有名字没事件的机制照实标为记录在案的缺口，不冒充已落地 |

## tb-99-2 · 99-appendix.md · 原 L37

| 章·节 | 这一层的形态 |
|---|---|
| 第一章 1.4 | agent loop 内存即易失，不持久真相 |
| 第三章 | 运行中的对话没有真相源（SSOT），UI 无真相源、靠猜的投影骗用户做致损决策 |
| 第六章 6.3 | 立投影三契约（有来源/可重建/不回写）＋ SSOT；工作制品 J |
| 第九章 | 断流不等于断 run，UI 掉线不是任务掉线；投影可断、可旧、可重建，run 不受影响 |
| 第十章 10.1／10.3 | context 是投影不是容器——它是给某一次模型调用看的读视图，按来源、优先级、预算确定性组装；压缩只改视图不改历史，摘要是新增的行、绝不写回去盖掉原文 |
| 第十三章 13.2 | 证据的五种载体只有一种是真相：原始 event 是 append-only 的事实，trajectory 等其余四种都是从它派生的投影 |
| 第十五章 15.1 | 连人也算：架构师讲的是他脑子里的系统，那也是一层投影，隔着线上真相还有一层 |

## tb-99-3 · 99-appendix.md · 原 L53

| 章·节 | 这一层的形态 |
|---|---|
| 第二章 | 验收层：pass=true 假通过——执行方自报成功，无人独立判定 |
| 第五章 5.5 | run 终态 guard：半轮内容终态化落盘，抢占才允许发生 |
| 第八章 8.3 / 8.10 | 工具提交点：lease 校验从入口搬到副作用提交点（关掉 TOCTOU 窗口）；result 是报告、outcome 是实况、独立取证、两向对账 |
| 第九章 9.4 | 传输层：成功不在 2xx 响应头提交、在内容写入下游之后提交；流终结真值表默认 fail closed |
| 第十二章 12.7 | 多 agent 层：child 的回传是子 agent 的自述，不是外部世界替它作的证——"内部"不构成可信的理由（12.6 同理：没跑完、结果未知是合法终态 unknown，不许伪造成成功） |
| 第十三章 13.5 | 证据层：completion claim 必须连到 outcome evidence——完成声明不连 outcome，就是拿自述当事实 |
| 第十四章 14.6 | 集成验收层：验收不看"能跑"，看标准故障包全绿——九章留下的 fixture 在这里汇编成逐格验收表 |

## tb-99-4 · 99-appendix.md · 原 L69

| 章·节 | 这一层的形态 |
|---|---|
| 第一章 1.4 | 语义层：N 个入口各自实现取消/权限，"取消"长出三种语义；解法是 run manager 单执行内核 |
| 第五章 5.3 | 转移层：N 处 UPDATE 各带隐式状态机→唯一内核 transition 路径；表外转移拒绝 |
| 第六章 | 状态层：单一写者串行化，谁能写这张表由 owner 定 |
| 第八章 8.3 | 副作用层：Effect Gateway 是副作用的唯一大门，旁路写靠两向对账兜 |
| 第十二章 12.5 | 并发层：worktree 只管执行期隔离，写路径仍要单点化或用显式 reducer 合并，父 run 在 merge 这个唯一收敛点上仲裁 |

## tb-99-5 · 99-appendix.md · 原 L83

| 章·节 | 这一层的形态 |
|---|---|
| 第五章 | waiting 状态——run 停下等外部输入 |
| 第六章 6.11 | 三生命周期分离（状态/执行/授权）；lease 分层，执行权不进实体链 |
| 第七章 7.8 | 四操作四后果表里授权列：resume/replay/fork/time travel 没有一种自动携带旧授权 |
| 第八章 8.3 | committed_under：副作用提交点校验当刻的执行权 |
| 第九章 9.8 | 挂起恢复时授权重验——checkpoint 存了挂起，不管三天前的授权是否还有效 |
| 第十章 10.8 | 恢复时 prompt asset 要拆两半：塑形行为的那部分按崩溃前那一版重建，**系统约束取当前版**——约束在 run 中途收紧了、恢复还照旧版走，等于绕过刚立的新规则。与 11.6 是同一句话的两种说法 |
| 第十一章 11.6 | **主场收口**：resume／fork／replay 重建的是状态与执行，绝不顺手把旧授权一起复活；确需跨恢复保留的授权必须显式列进契约，并在上下文、主体、版本上逐项重验。工作制品 U（Authority Lifecycle Matrix）是它的登记表 |

## tb-99-6 · 99-appendix.md · 原 L99

| 章·节 | 这一层的形态 |
|---|---|
| 第一章 1.1 | 三本质变量之一：副作用泄向外部世界，超时重试一个"发邮件"工具，客户收到两封 |
| 第七章 7.5 | 重放/重新执行之辨：决策 exactly-once，动作只能 at-least-once＋幂等 |
| 第八章 8.4–8.6 | at-least-once＋幂等消费；四类处置（重试/查询/补偿/未知）；幂等 key 的来源/作用域/保留期 |
| 第九章 9.10 | retryable 随交付进度降级（delta 已交付不能整段重发）；跨层重试放大 |
| 第十四章 14.6 | 验收层：replay 与 reconciliation 两个 fixture 进标准故障包——幂等不再靠声称，要在故障包里被逐格判定 |
| 第十五章 15.4 | 评审桌上：残余风险清单模板第一行的示例就是它——"工具超时后重试，远端已成功"，契约记副作用，触发场景记 reconciliation fixture |

## tb-99-7 · 99-appendix.md · 原 L126

| 术语 | 一句定义 | 立于 | 关联 |
|---|---|---|---|
| 六契约 | 真相/转移/副作用/交互/权限/证据——运行时正确性拆成的六份可检验承诺 | 1.2 | 四问·工作制品全部 |
| 四问（检验坐标系） | 可观测/可控/稳定/闭环——控制论四原则的操作面，检验每份契约是否被守住 | 1.3 | 六契约 |
| L0-L5 成熟度尺 | 机制成熟度分级（本书系分级，非业界通则）：L1 能跑、L2 能看、L3 能评… | 1.3 | 假落地公式 |
| 假落地诊断公式 | 有名字（L1 在）＋无事件（L2 缺）＝假落地嫌疑高 | 1.3 | 主线一 |
| 半途设计 | 机制只接一半的线（写了没接通、接通没生效），比没有机制更危险 | 3.1 | 假落地公式 |

## tb-99-8 · 99-appendix.md · 原 L136

| 术语 | 一句定义 | 立于 | 关联 |
|---|---|---|---|
| SSOT（单一真相源） | 持久状态是唯一真相，context 与 UI 都是它的投影 | 6.3 | 投影三契约·主线二 |
| 投影 | 从持久真相派生、可丢可重建、不回写的读视图 | 6.3 | 工作制品 J |
| 实体链 | Conversation→Run→Turn→Step→Invocation/Tool Execution 六级归属 | 6.0 | 工作制品 A |
| TOCTOU | 检查与使用之间的时间窗，并发下被写坏世界的缝 | 2.7 | 5.7·8.3 |
| CAS（乐观并发） | run 行带 version、更新走 compare-and-swap，冲突者重读重试 | 5.7 | lease·fencing |
| lease（租约） | 带 TTL 的执行权凭据，持有者心跳续租；进程内授权对象，不进实体链 | 5.7 | 主线五·工作制品 I |
| fencing token | 租约每次授予带的单调递增编号，状态层拒旧编号写入，防"不知道自己已出局"的写者 | 5.7 | lease·8.3 |
| 看门狗 | 扫"超 deadline 再无活跃事件"的 run、送终态；活跃事件即心跳 | 5.8/7.6 | state_machine_version |

## tb-99-9 · 99-appendix.md · 原 L149

| 术语 | 一句定义 | 立于 | 关联 |
|---|---|---|---|
| 重放 vs 重新执行 | 重放读已落盘的记录（世界不动），重新执行把动作再做一遍（世界可能再变） | 7.1 | 主线三 |
| invocation（模型调用记录） | 每次模型调用完整留档，恢复时复用、永不重调；即重放缓存 | 7.2 | 工作制品 A |
| 四段账 | intent→attempt→result→outcome，副作用的四段记录 | 8.2 | 工作制品 B |
| Effect Gateway | tool executor 的提交面（intent 落盘＋执行权校验），副作用唯一出口；非新组件 | 8.3 | 主线三/四 |
| action class | read_only/idempotent/compensatable/non_replayable——工具重发语义四类 | 8.4 | 工作制品 B |
| Plan Lease | 计划的适用前提（model_version＋history_cursor＋policy_version），任一变即失效 | 8.12 | 工作制品 N |

## tb-99-10 · 99-appendix.md · 原 L160

| 术语 | 一句定义 | 立于 | 关联 |
|---|---|---|---|
| 四词辨析 | disconnect/cancel/interrupt/suspend——四件不同的事，各落转移表不同位置 | 9.5 | 工作制品 P |
| 流终结真值表 | 流的每种收尾一行、判成功或失败、默认 fail closed | 9.4 | 工作制品 O·主线三 |
| cursor / replay window | 下行事件的单调序号＋断线后从游标补发，应用层自建续传 | 9.3 | — |

## tb-99-11 · 99-appendix.md · 原 L182

| 章 | 破坏动作 | 观测点（盯这些字段/事件） | 通过判定 |
|---|---|---|---|
| 5 | 双入口毫秒级同触发同会话 | events 两条意图的裁决事件；runs 活跃行数 | 恰一个进 running，另一个落 reject/enqueue/interrupt 显式事件 |
| 5 | 双进程同 resume 同一孤儿 | 认领事件与写入路径 | 恰一个认领；单机实例锁拒第二个，多实例慢者被 fencing 拒写且有事件 |
| 6 | 三处写入之间 kill -9（三杀） | 各表内容与事件表截断点；配对不变量扫描；checkpoint 完整性标记 | 已提交完整可见、未提交不留半行；事件按最后完整行截断可重建 |
| 7 | 副作用已发生、result 未落时 kill -9 | effect 账本该行状态；恢复后的调和事件；副作用是否被二次执行 | 该行停在 intent 有 result 无、标 unknown 进调和、不自动重放 |
| 8 | 超时但远端已成功 / 返回成功但 artifact 缺 / 改 policy / 单步 mismatch | effect 账本行状态；effect.* 与反例事件；外部世界实况 | 幂等重试无双份 / outcome 取证对出矛盾 / 拒 stale lease / 废剩余队列 |
| 9 | 断网 / 刷新 / 抢占 / 审批跨 session 恢复 | run 状态与转移事件；下行事件游标；半轮 message 落盘状态；授权重验记录 | run 不受连累、按游标补全、半轮终态化、授权重验再放行 |

## tb-99-12 · 99-appendix.md · 原 L203

| 想查的字段属于 | 去工作制品 | 内容 |
|---|---|---|
| 持久状态对象的 owner/存储/删除/崩溃归宿 | A · State Registry | 每个持久对象一行，含 conversation/run/message/step/invocation/effect/checkpoint/timer/event 等 |
| 副作用四段账字段 | B · Effect Ledger | effect_id、idempotency_key、action_class、committed_under、intent_at、四段状态、reconciliation_status |
| 事件信封字段 | C · Event Schema | event_id、seq、correlation 链、type、payload、source；事件类型全表 |
| run 转移的触发/guard/终结原因 | H · Run 状态转移表 | 17 行合法转移，每行 event/guard/transition/terminal_reason/随行事件 |
| 携带物是否随 checkpoint 保存/恢复/重验 | I · Lifetime Matrix | 消息游标、compaction 版本、state_machine_version、approval、lease、credential 等 |
| 流的收尾判定 | O · Stream Terminal Table | 七种收尾×成功/失败×说明 |
| 四词对 run 的影响与转移 | P · Interaction Semantics | disconnect/cancel/interrupt/suspend×影响×转移×半轮归宿 |

## tb-99-13 · 99-appendix.md · 原 L225

| 图 | 档 | 它替你回答什么 | 接哪件 |
|---|---|---|---|
| 图 1.0 | 补充 | 入门卷行装与三桩开场怪事——部件都在，两份测量把病根钉在部件之外的约定上 | 1.0 命题（工程质量是独立变量） |
| 图 1.3 | 补充 | 四问从哪来：反馈环四处失守对上四原则，入门卷的设计问换向成本卷的检验问 | 1.3 四问／入门卷第九章 |
| 图 1.4a | 补充 | 为什么恰好是六份契约、八个组件——三个出厂设置怎么一路推出这两个数 | 1.1 三个失效的默认值／1.2／1.4 |
| 图 1.4b | 补充 | 九步落盘时序：顺利路径上哪一步写了什么、将来被谁读到；落盘点都握在谁手里 | 1.4 判断标准（机制要能在时序上标出位置） |
| 图 1.4c | 补充 | 业界三家在六契约矩阵上的厚区与空格——没有一家六格全实 | 1.4 业界对照／第四章 4.6 逐组件映射 |
| 图 1.5 | 核心 | 六契约 × 四个问题交出的检验矩阵，也是全卷的地图：哪一章住进哪几格 | 1.2 六契约 · 1.3 四问 |
| 图 1.A | 补充 | 入门卷 8 件＋控制面＋四原则在本卷的落位：同名直连、职责收进 run manager、拆分换形态 | 附录 A 术语对照表 |
| 图 2.4 | 核心 | 契约六要素每一格少了会怎样；哪两格填不满，设计就只做了一半 | 交付物 Assumption Register |
| 图 2.6 | 补充 | 判据自己怎么体检：三种失效配三项检验，落成报告的三个强制字段 | 交付物 判据体检三字段 |
| 图 3.4 | 核心 | 事故里那条消息在五个载体间的十帧轨迹——它一次都没碰过持久层 | 3.4 缺失证据清单 |
| 图 3.6 | 补充 | 同一张检验矩阵第二次用：六个缺口格格有名字，四个先倒在"看得见吗" | 3.6 契约缺口图／1.5 检验矩阵 |
| 图 4.8 | 核心 | 八个组件各主守哪份契约、L 级起步定在哪、负载长大时从哪一刀切出去 | 工作制品 G（Component Register） |
| 图 5.2 | 核心 | run 的七个状态怎么转；为什么"卡在 running"不是一个状态，是缺陷 | 工作制品 H（Run 状态转移表） |
| 图 5.11 | 补充 | 六个入口的后四列为什么只有一个去处——四种语义只在内核实现一次 | 工作制品 E（Routing Matrix） |
| 图 6.0 | 核心 | 六级实体链谁属于谁，各级落在十一张表的哪一张 | 工作制品 A（State Registry） |
| 图 6.11 | 补充 | 状态、执行、授权三条生命周期寿命不等；一次崩溃三种反应，resume 不是总开关 | 工作制品 I（Lifetime Matrix） |
| 图 7.1 | 补充 | 恢复时每一步分边只问账本：完整一行重放、半行对账、零记录重新执行 | 7.1 分边／第八章 8.6 四类处置 |
| 图 7.10 | 核心 | kill -9 之后的七步恢复，每步依据哪件、失败了去哪 | 工作制品 B／C／H／I |
| 图 8.2 | 核心 | 一次副作用在账本上的四段一生；两条来路不同的异常怎么汇进同一套调和 | 工作制品 B（Effect Ledger） |
| 图 8.3 | 补充 | 校验为什么要从入口搬到提交点——动手那一刻的凭据必须是活的 | 工作制品 B（committed_under） |
| 图 9.1 | 核心 | 断线之后 run、连接、屏幕三条钟各自怎么走，又怎么重新对上 | 工作制品 O／P |
| 图 10.2 | 补充 | 给窗口腾地方的四种手段各落哪类解空间、各担哪笔账 | 工作制品 Q（Context Assembly Spec） |
| 图 10.3 | 核心 | 压缩契约的四条纪律，各守事务的哪一刻 | 工作制品 R（Compaction Contract） |
| 图 11.2 | 补充 | 硬边界与软提示怎么分：失败时门是关着还是开着 | 工作制品 V（Common-mode Failure Matrix） |
| 图 11.7 | 核心 | 八个组件按"谁有权持有什么"分成的五个平面，与权力真正被行使的三个干预点 | 工作制品 F（Intervention Point Map） |
| 图 12.2 | 核心 | 自治的 loop 怎么嵌在编排的图里，两层各管什么、混层会坏在哪 | 12.2（与第八章 8.12 两种 graph 正交） |
| 图 12.7 | 补充 | 一次委派从 spawn 到采信，第十一章的四张欠条各钉在哪一刻 | 工作制品 W（Parent-Child Run Contract） |
| 图 13.2 | 核心 | 一条事件的解剖：唯一事实、八级 correlation 信封、四种投影 | 工作制品 C（Event Schema） |
| 图 13.6 | 补充 | 两种沉默的坍塌路径，与能自证的证据面该有的样子 | 工作制品 Y（Detector Test Record） |
| 图 13.8 | 补充 | 七条认识论边各在什么位置：三条建、两条溯源、两条回填成环 | 工作制品 X／Z |
| 图 14.2 | 核心 | 十四步构造序为什么不能倒置——依赖顺序就是构造纪律 | 14.6 标准故障包 |
| 图 15.2 | 补充 | Runtime Contract Matrix 三十格铺开：可测试性一行已被标准故障包填满 | 15.2 五件工具／14.6 标准故障包 |
| 图 15.3 | 核心 | 九十分钟八步，五件评审工具各接在哪一步上 | 工作制品 G／A／B／D |
| 图 附.1 | 核心 | 六条概念主线各自穿过哪几章，哪一章一条都不经过 | 附录一 概念主线索引 |
