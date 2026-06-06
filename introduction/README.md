# Harness Study · 智能体的工程实践 · 入门版

*Harness Study · The Engineering Practice for AI Agents · Intro*

> **本卷定位**：Harness Study 项目的**导论级 / 入门版** explainer · 回答"什么是智能体的 harness 以及它由哪几件组成"。**平台无关的工程实践方法论**主轴 · 配套实现项目作为工程案例点缀。
>
> **在 Harness Study 全集中的位置**：本卷是开篇导论卷——把 8 件 runtime + Safety 控制面 + 工程模式 + Harness Lab + 可组合性矩阵 + 控制论四原则**全骨架走一遍** · 每件件给出 What / Why / How to start 三档完整 mental model。**后续会有逐章 / 逐模块展开版**——每件 runtime 件 / 每件工程模式 / Harness Lab 五层等都会有独立深度卷 · 覆盖更细的工程纪律 / 业界 case / 落地踩坑。

## 目录

本卷按章节拆分，每章一个文件；第五章（必备机制）每个细节一个文件。建议按下表顺序（文件名 01 → 99）依次读。

| 章 | 文件 | 主题 |
|---|---|---|
| §一 | [01-why-harness.md](./01-why-harness.md) | 我们究竟在解决什么问题 |
| §二 | [02-prehistory.md](./02-prehistory.md) | 前世：模型当函数用的时代（2020–2022） |
| §三 | [03-autogpt.md](./03-autogpt.md) | 第一次大规模试错：AutoGPT 浪潮和它的翻车（2023） |
| §四 | [04-harness-emerges.md](./04-harness-emerges.md) | Harness 概念的浮现（2023 中–2026） |
| §五 · 总述 | [05-00-mechanisms-overview.md](./05-00-mechanisms-overview.md) | 8 件 runtime + 1 件 Safety 控制面 · 切法与件 vs 实现 |
| §5.1 | [05-01-agent-loop.md](./05-01-agent-loop.md) | Agent Loop · Inner Loop · agent 的思考结构 · **P0** |
| §5.2 | [05-02-model-adapter.md](./05-02-model-adapter.md) | Model Adapter & Routing |
| §5.3 | [05-03-tool-registry.md](./05-03-tool-registry.md) | Tool Registry & ACI · **P0** |
| §5.4 | [05-04-context-memory-artifact.md](./05-04-context-memory-artifact.md) | Context / Memory / Artifact |
| §5.5 | [05-05-prompt-assets.md](./05-05-prompt-assets.md) | Prompt Assets · Instruction Layer · **P0** |
| §5.6 | [05-06-observation-surface.md](./05-06-observation-surface.md) | Observation Surface · 三层定位 |
| §5.7 | [05-07-trajectory.md](./05-07-trajectory.md) | Trajectory · Event Stream · **P0** |
| §5.8 | [05-08-verifier.md](./05-08-verifier.md) | Verifier 三层 · **P0** |
| §5.9 | [05-09-safety.md](./05-09-safety.md) | Safety 控制面 · cross-cutting |
| §5.10 | [05-10-turn-walkthrough.md](./05-10-turn-walkthrough.md) | 一次 turn 的微型流程 |
| §5.11 | [05-11-end-to-end.md](./05-11-end-to-end.md) | 中型端到端流程示例 · 17 turn 修 logging bug |
| §六 | [06-engineering-patterns.md](./06-engineering-patterns.md) | 工程模式 · 跨件复用的工程组合 pattern |
| §七 | [07-harness-lab.md](./07-harness-lab.md) | Harness Lab · Outer Loop · 系统化优化 harness 自身 |
| §八 | [08-composability.md](./08-composability.md) | 可组合性矩阵 · 封装 × 拓扑 × 交互边界 |
| §九 | [09-cybernetics.md](./09-cybernetics.md) | 控制论四原则 · 整本教程的元规则收束 |
| §十 | [10-learning-path.md](./10-learning-path.md) | 学习路径 · 三类读者怎么用这本教程 |
| 配套 · Prompt | [11-harness-prompt.md](./11-harness-prompt.md) | Harness Prompt · 给 agent 的可执行落地 Spec（Phase 0–3 + 每步 gate）|
| 配套 · Prompt lite | [12-harness-prompt-lite.md](./12-harness-prompt-lite.md) | Harness Prompt · 通用 TDD lite 版（三段指令直接喂编码 AI）|
| 附录 | [99-appendix.md](./99-appendix.md) | 8 件速查表 + 一手引源汇总 |

> §5.1 的深讲卷在后续展开卷（规划中）。**可执行配套件已收进本目录**：落地 Spec → [`11-harness-prompt.md`](./11-harness-prompt.md)；TDD lite 版 → [`12-harness-prompt-lite.md`](./12-harness-prompt-lite.md)；速查附录 → [`99-appendix.md`](./99-appendix.md)。

## 配图目录

全卷共 50 张配图，统一 jimi-ink 视觉，源文件在同级 [`../diagrams/`](../diagrams/)。各图已嵌入对应章节正文，下表按章索引。

| 章 | 配图 |
|---|---|
| §一 | 鸿沟·对立桥 `t1-comparison-1-gap` · 从 vibe 到 agentic 光谱 `t2-comparison-1-spectrum` |
| §二 | prompt-only 局限 `t1-comparison-2-prompt` |
| §三 | AutoGPT 机制矩阵 `t1-matrix-3-autogpt` · 实习生类比 8+1 `t2-analogy-3-intern` |
| §四 | harness 命名时间线 `t1-timeline-4-naming` · 每代算法对应约束层 `t2-matrix-4-generations` · 马具隐喻 `t2-analogy-4-bridle` |
| §五·总述 | 八大机制总览 `sample-05-mechanisms-overview` · 抽象层次 `t1-layered-5.0-abstraction` |
| §5.1 | ReAct 演化矩阵 `t1-matrix-5.1-react8` · 设计四问决策树 `t1-tree-5.1-choose` · 十五条收敛五条 `t2-cardgrid-5.1-five` · 多 agent 成本 15x `t3-cardgrid-5.1-multiagent` |
| §5.2 | 模型路由 `t1-cardgrid-5.2-routing` |
| §5.3 | tool call 流程 `t1-flow-5.3-toolcall` · 工具批处理四模式 `t3-cardgrid-5.3-toolbatch` |
| §5.4 | 三层状态对比 `t1-comparison-5.4-state` · Memory 五问 `t2-tree-5.4-memory` · OS 内存层次 `t2-analogy-5.4-osmem` · 压缩三力度 `t3-comparison-5.4-compress` |
| §5.5 | prompt 资产矩阵 `t1-matrix-5.5-promptasset` · P0-P5 金字塔 `t3-layered-5.5-p0p5` |
| §5.6 | observation 分层 `t1-layered-5.6-observation` · observation vs logging `t2-comparison-5.6-obslog` · 自进化五路径 `t3-cardgrid-5.6-selfevo` |
| §5.7 | trajectory 事件类型 `t1-cardgrid-5.7-events` |
| §5.8 | verifier 矩阵 `t1-matrix-5.8-verifier` · leakage 四类防御 `t2-cardgrid-5.8-leakage` |
| §5.9 | Safety 横切 `t2-layered-5.9-controlplane` · permission 分层 `t1-layered-5.9-permission` · HITL 两路径 `t3-comparison-5.9-hitl` · OWASP 四项 `t2-cardgrid-5.9-owasp` · 四类误区 `t3-cardgrid-5.9-pitfalls` |
| §5.10 | 一次 turn 流程 `t1-flow-5.10-turn` |
| §5.11 | 17 turn 时间线 `t1-timeline-5.11-17turn` · Turn 16 时序 `t1-sequence-5.11-turn16` |
| §六 | 工程模式卡片 `t1-cardgrid-6-patterns` · Isolation 三档 `t2-comparison-6-isolation` · 六 pattern 渐进 `t3-timeline-6-pattern-order` |
| §七 | Harness Lab 分层 `t1-layered-7-harnesslab` · 工作台五层覆盖 `t2-matrix-7-workbench` · 三 Phase 消融 `t3-flow-7-ablation` |
| §八 | 可组合性维度 `t1-cardgrid-8-axes` · 副 harness 五维度 `t2-cardgrid-8-subharness` · 乐高加集装箱 `t3-comparison-8-lego` · Evidence Graph 十边 `t3-cardgrid-8-evidence` |
| §九 | 恒温器类比 `t1-analogy-9-thermostat` · 控制论四原则 `t2-cardgrid-9-principles` |
| §十 | 三类读者路径 `t1-comparison-10-readers` |

## 教程在解决什么问题

大多数 agent 教程在讲怎么搭一个能跑的 agent——选 framework、写 prompt、加工具、跑 demo。这一层网上资料很多。但真把 agent 推到 To B 应用里就会发现：**跑通不难，跑稳难**。

演示时一切顺利的 agent，放到合同审核、业务流程审批、OA 任务上反复跑，开始出各种岔子：同一个 prompt 不同时间结果不一致；跑 5 次取平均看着挺好，用户实际用着只觉得偶尔答对；明明给了文档让它查，它却凭空伪造细节然后说"已完成"；改了一个工具调用的写法，整条主线就不收敛了。

这些问题里大部分**不是 prompt 没写好**——是 agent 外面那一层框架没设计好。这层框架在英文文献里叫 harness · 中文一般翻译成"智能体框架"。harness 不是 LangChain / LangGraph / 某个 SDK · 那是 framework。harness 是你在 framework 之上为某个具体任务搭起来的整套结构：模型怎么挂、工具怎么管、上下文怎么累积、轨迹怎么留痕、验证靠什么、安全靠什么、出错怎么兜底。

## 读完入门版应该能回答的六个问题

1. **我的 agent 不稳定 · 是不是 prompt 写得不好？** —— 多半不是。prompt 只是 harness 一件零件 · prompt 调到极限收益就到顶了。
2. **ReAct 还在用吗？我该升级到 plan-execute 吗？** —— 看场景。ReAct 八条原始假设里四条已经失效 · 但失效不等于 ReAct 整体过时。
3. **我跑 N 次取平均看通过率 · 统计可信吗？** —— 不一定。DeepSeek 之类的 prefix KV cache 会让 N 次之间不是独立的——表面 80% 通过率可能其实是同一份缓存复用 N 次。这叫 cache 共谋。
4. **我的 verifier 总放过看似对实际错的输出 · 怎么办？** —— 三种典型病：答案泄漏、reward hacking、artifact-claim mismatch。各有不同对策。
5. **我应该怎么系统优化 harness 而不是凭感觉调？** —— Observe → Score → Ablate → Tune → Iterate。这是一个独立于业务循环的外循环 · 本卷叫 Harness Lab。
6. **这教程哪段是给我读的？** —— 见下文"谁该读哪段"。

## 谁该读哪段

入门版不要求从头读到尾。三类读者各有推荐路径（详细路径见 [§十 学习路径](./10-learning-path.md)）：

**AI PM / AI 业务人员**——你要选型 / 评估外部 agent 厂商 / 给团队定 harness 方向。推荐路径：§一 → §5.3 Tool Registry → §5.5 Prompt Assets → §七 Harness Lab 三块常见误区 → §八 可组合性矩阵。

**学习者**（学 agent 工程、做研究、准备入行）——你要建一套能跟任何 agent 论文 / 教程对话的 mental model。推荐路径：§一-§二 → §5.1 Agent Loop → §5.8 Verifier → §九 控制论四原则。

**给 AI 看**——AI agent 自己读本卷做下游决策。推荐路径：按目录顺序（文件名 01 → 99）依次读。不要跳读机制描述段——那是 prose 主体，跳了就只剩名字。

## 跳读建议

- **沿用章节**（§5.2 Model Adapter / §5.7 Trajectory）讲相对成熟的零件 · 方法论密度低 · 可跳读。
- **重头戏章不要跳**：§5.1 Agent Loop / §5.4 Context-Memory-Artifact / §5.5 Prompt Assets / §5.6 Observation Surface / §5.8 Verifier / §七 Harness Lab / §八 可组合性矩阵 / §九 控制论。这八章是本卷的 thesis 承重墙。
- **§5.6 升级了三层 framing**——observation surface 不只是 runtime feedback 件 · 更是 cross-run self-evolution 的输入侧基础设施层。

## 完成判据 · Verify 六问

入门版完成判据 = 上面六个问题读者读完能回答：

1. **harness 跟 prompt engineering / agent runtime / workflow 各是什么关系？** —— §二 + §三 + §四 联合回答。
2. **ReAct 还在不在用？什么场景该用哪个？** —— §5.1 Inner Loop 决策树。
3. **为什么 verifier 设计这么难（Leakage + Reward Hacking + Artifact Claim Mismatch）？** —— §5.8 + §5.9 末段联合回答。
4. **为什么 N 次复跑统计可能是假的（Cache 共谋）？** —— §7.4 Ablate Cache 共谋段。
5. **harness 怎么被系统调优（Observe → Score → Ablate → Tune → Iterate）？** —— §七 Harness Lab 五层联合回答。
6. **这本书是给我看的吗 · 从哪一章开始读？** —— §十 学习路径 + §一 阅读路标联合回答。

**下一档完成判据**（后续逐章 / 逐模块展开版）：读者能独立设计 + 独立调优一个 agent harness · 不是只回答六问。
