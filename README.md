# Harness Study · 智能体的工程实践

*The Engineering Practice for AI Agents*

> English version: [README.en.md](README.en.md)

> 当前状态：**入门卷正在审稿**——稿件已写完，正在终审；审稿完成后推到 [`intro/`](intro/) 目录。本 README 描述本卷的目的、读者、章节、判据。

---

## 一、这一卷想解决的事

大多数关于智能体（agent）的资料停在"怎么搭一个能跑的 agent"——选框架、写提示词、加几件工具、跑通示例。这一层网上够多了。

真正把智能体放到 To B 办公、合同审核、业务流程审批这类任务上反复运行之后，会出现另一类问题：同一份提示词在不同时段产出不同的结果；表面通过率高但用户实际感到时对时错；明明给了文档让它查，仍然伪造细节并宣称完成；只改了一处工具调用的写法，整条主线就不再收敛。

这些问题里大多数原因不在提示词。把希望寄托在反复迭代提示词上，到一定阶段之后边际收益迅速衰减。真正决定智能体稳定与否的，是围绕模型的那一层结构——在英文文献里叫 **harness**。harness 不是 LangChain 或某个 SDK——那是 framework。harness 是你在 framework 之上为某个具体任务搭起来的整套结构：模型怎么挂、工具怎么管、上下文怎么累积、产物怎么落地、验证靠什么、安全靠什么、出错怎么兜底。

本卷（入门卷）的目的，是把围绕模型的这一层抽出来作为独立的工程对象，逐件讲清楚它由什么构成、为什么必须有、怎么选、怎么发现选错了。

## 二、入门卷完成什么

入门卷把 agent harness 拆成 **八件 runtime 机制 + 一件横切控制面 + 工程模式 + 工作台 + 可组合性矩阵 + 控制论四原则**，把整套骨架走一遍。每一件给出 What / Why / How to start 三档完整 mental model。

读完本卷，你应能建起完整的 agent harness mental model，拿到任何 agent 工程问题能定位到具体件 + 具体反模式。

后续会有**逐章 / 逐模块展开卷**——每件 runtime 件 / 每件工程模式 / 工作台五层等都会有独立深度卷，覆盖更细的工程纪律、业界案例、落地踩坑。读完展开卷后，你应能独立设计 + 独立调优一个 agent harness。

另有一件目标——**任何一个 AI coding 工具读完本卷之后，应当能够依据使用者给出的具体需求或场景，落地一个可投入使用且准确性较高的 agent**。本卷在写作上即假定读者中包括 AI 本身：它读完之后的下游动作不是停在"理解概念"，而是为使用者构造可用的工程产物。

## 三、读完入门卷应能回答的六个问题

1. **我的 agent 不稳定 · 是不是 prompt 写得不好？** 多半不是。prompt 只是 harness 的一件零件，调到极限收益会到顶。
2. **ReAct 还在用吗？我该升级到 plan-execute 吗？** 看场景。ReAct 八条原始假设里四条已经失效，但失效不等于 ReAct 整体过时。
3. **我跑 N 次取平均看通过率 · 统计可信吗？** 不一定。DeepSeek 之类的 prefix KV cache 会让 N 次之间不独立——表面 80% 通过率可能其实是同一份缓存复用 N 次。这叫 cache 共谋。
4. **我的 verifier 总放过看似对实际错的输出 · 怎么办？** 三种典型病：答案泄漏（verifier 见过 ground truth）、reward hacking（模型学会糊弄 verifier）、artifact-claim mismatch（agent 声称做了但产物里没有）。三种各有不同对策。
5. **我应该怎么系统优化 harness 而不是凭感觉调？** Observe（观察轨迹）→ Score（打分）→ Ablate（消融）→ Tune（调参）→ Iterate（迭代）。这是一个独立于业务循环的外循环，本卷称之为 Harness Lab。
6. **这教程哪段是给我读的？** 见下文"谁该读哪段"。

## 四、谁该读哪段

入门卷不要求从头读到尾。三类读者各有推荐路径：

**AI PM / AI 业务人员**——你要选型、评估外部 agent 厂商、给团队定 harness 方向。最需要"有哪些零件、什么场景该选什么、什么是常见误区"。推荐路径：

§一 Why harness（5 分钟先建心智）→ §5.3 Tool Registry & ACI（工具是 To B agent 落地的关键）→ §5.5 Prompt Assets（指令层怎么管）→ §七 Harness Lab 三块反模式（cache 共谋 / leakage / reward hacking）→ §八 可组合性矩阵（看清自己手里在拼哪一组合）。

**学习者**（在学 agent 工程、做研究、准备入行）——你要建一套能跟任何 agent 论文 / 教程对话的 mental model，知道 ReAct 到 Reflexion 到 plan-execute 这条线为什么会这么演化。推荐路径：

§一-§二（命名与历史）→ §5.1 Agent Loop（思维范式的进化）→ §5.8 Verifier（agent 工程最难的一件）→ §九 控制论四原则（整本教程 thesis 收束）。

**给 AI 看**——AI agent 自己读本卷做下游决策（例如读完本卷之后调自己 harness 配置）。推荐路径：

按 frontmatter `depends_on` 链表依次读。每章 entry hook + 认知节点定义足够建模。不要跳读机制描述段——那是 prose 主体，跳了就只剩名字。

## 五、章节规划

| 章 | 主题 |
|---|---|
| §一 | Why harness · 为什么必须把围绕模型的那一层抽出来 |
| §二 | 命名与历史 · prompt → harness engineering |
| §三 | 跨度三层 |
| §四 | 关键张力 |
| §五 | 八件 runtime 机制 + Safety 控制面 + 端到端示例 |
| §5.1 | Agent Loop |
| §5.2 | Model Adapter & Routing |
| §5.3 | Tool Registry & ACI |
| §5.4 | Context / Memory / Artifact |
| §5.5 | Prompt Assets |
| §5.6 | Observation Surface |
| §5.7 | Trajectory |
| §5.8 | Verifier |
| §5.9 | Safety |
| §5.10 | 微型流程 |
| §5.11 | 端到端 17 turn |
| §六 | 工程模式 |
| §七 | Harness Lab · 调优外循环 |
| §八 | 可组合性矩阵 |
| §九 | 控制论四原则 |
| §十 | 学习路径 |
| 附录 | K1-K7 / 一手 source / EG10 / OWASP / 命名映射 / SPIFFE-biscuit / AP01-AP19 / arxiv 全表 |

入门卷整本规模约二十五万中文字，prose 主导。这件规模由"一次走完全骨架 + 给完整 mental model"的入门版定位决定；后续展开卷会更聚焦、更详细。

## 六、跳读建议

- **附录是参考资料不是必读**——查到再读。
- **沿用章节**（§5.2 Model Adapter / §5.7 Trajectory）讲的是相对成熟的零件，方法论密度低于重头戏章，可跳读。
- **重头戏章不要跳**：§5.1 Agent Loop / §5.4 Context-Memory-Artifact / §5.5 Prompt Assets / §5.6 Observation Surface / §5.8 Verifier / §七 Harness Lab / §八 可组合性矩阵 / §九 控制论。这八章是本卷的 thesis 承重墙。

## 七、跟工作台项目的关系

教程一侧定义研究的对象与方法；工程实现一侧由独立项目 [Harness · Lab](https://github.com/li2092/Harness-Lab) 承担——把这套方法承担在可视化工作台规范上。教程项目（本仓库）跟工作台项目共享同一套术语、节点、信号定义。

两者使用顺序：

- 第一次读本教程：不需要工作台 · 直接读 `intro/01-introduction.md` 起。
- 已读完入门卷、要落地某个具体 harness：把工作台规范当作 evidence graph 的视觉语言来用。

## 八、完成判据

**入门卷完成判据** = 上述六个问题读者读完能回答。

**下一档完成判据**（后续逐章 / 逐模块展开卷）：读者能独立设计 + 独立调优一个 agent harness——不只是回答六问。

## 九、协议

[Apache License 2.0](LICENSE) © 2026 Jinming Li

## 十、联系

- Issues 与 Discussions 欢迎
- 邮箱：li2092@qq.com
- GitHub：[@li2092](https://github.com/li2092)
