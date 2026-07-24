# Harness Handbook（Tencent HY LLM Frontier）调研笔记

> 2026-07-18 · 主会话 curl 直连调研（GitHub API + 项目博客 + arXiv 摘要 + 中文 README）。
> 用途：第二卷 §二/§十/§十二/§十四、第三卷变更管理章的借鉴与引用底稿。

## 一、定性

- **是什么**：把 harness 代码库自动生成为"行为级手册"（behavior-centric representation）的开源工具 + 论文。两部分：①从源码生成三级手册（静态分析 + LLM 辅助结构化）；②把手册接到 code agent 的 planner 上，量化改动定位能力的提升。
- **谁做的**：署名机构 Tencent HY LLM Frontier（第一署名）+ Indiana University（通讯作者 Ruhan Wang）+ Maryland/Georgia/NUS。**注意**：仓库挂在个人账号 `Ruhan-Wang/Harness_Handbook`（69 star，2026-06-08 建，07-16 仍在推），非 Tencent org 官方仓库。称"腾讯开源"需带此限定。
- **论文**：arXiv:2607.13285《Harness Handbook: Making Evolving Agent Harnesses Readable, Navigable, and Editable》，2026-07-14 提交，v1。**来源等级：【预印】+【厂商实践】**，未经评审。
- **链接**：仓库 github.com/Ruhan-Wang/Harness_Handbook；博客 ruhan-wang.github.io/Harness-Handbook/（含中文版）；示例 Terminus 2 Handbook + Handbook Studio 交互演示。中英双语 README。

## 二、核心内容

### 2.1 问题定义（与本卷立论同源）

- 开场论断："一旦 agent 开始干真活，问题就从'模型能做什么'变成'系统允许它做什么'"——harness 决定行为边界，同一模型在不同 harness 下行为不同（厂商侧呼应 Harness-Bench 独立变量论）。
- **一行为多实现点**："删除文件前先问用户"由 prompt、tool wrapper、权限配置、状态管理、sandbox 执行、fallback 路径共同决定，没有一个 `confirmBeforeDelete()` 函数代表完整行为。理解/审计/修改都始于**行为定位（behavior localization）**——论文称其为 harness 演化的中心瓶颈。
- 规模数字：Codex 的相关实现散布在 **2,267 个文件、34,000+ 函数、约 160,000 条代码连接**里——文件树只说明代码在哪，说不出行为怎么产生。

### 2.2 三级手册结构 + BGPD

- L1 系统总览：跟一条请求走全程（怎么进、经过哪些 stage、状态怎么移、输出怎么变成动作）。
- L2 行为单元总览：把系统流拆成行为单元，记职责、输入输出、依赖、关键状态。
- L3 行为单元细节：触发、执行、状态变化、异常路径、代码证据（file:line）。
- **BGPD**（Behavior-Guided Progressive Disclosure）：行为问题 → L1 语境 → L2 定位单元 → L3 打开可验证细节 → 代码证据。一条证据路径三种用途：理解 / 审计 / 修改。
- **L3 行为单元模板字段**：Trigger / Permission rule / State change / Execution path / Edge cases / Evidence——与本卷 §2.4 契约六要素（owner、trigger、guard、action、outcome、evidence）高度同构，平行发明。

### 2.3 生成管线（facts-first）

1. 静态分析抽程序事实 → program graph（文件、函数、调用关系、状态读写、配置边界、外部 API）；
2. 按行为组织 → behavior map，proposer–reviewer 循环反复修正 stage/单元边界/证据对齐；
3. 渲染三级手册，**每个源链接、函数引用、代码片段必须来自抽取的程序事实**——"prose explains; facts anchor"（叙述解释行为，事实锚定声称）。

### 2.4 评测（定性结论，图表精确数字在论文正文，引用硬数字前读 PDF）

- 设置：NexAU 上构建的 coding agent，planner 用 DeepSeek-V4-Pro；两个真实 harness（Terminus-2、Codex）；唯一变量=planner 定位前是否读 Handbook；三个独立评审模型（GPT-5.5、Opus 4.8、DeepSeek-V4-Pro）；指标=win rate + planner token 成本；改动请求分三类：Q（调整既有行为）/ CF（跨文件加能力）/ SH（关键词搜不到——镜像实现、fallback、冷路径）。
- 结论一：两个 harness 上带手册的 planner 胜率更高**且** token 更少——收益来自更早命中相关代码，非喂更多上下文。
- 结论二：对照 Opus 4.8/GPT-5.5 参考方案，文件级与符号级 recall/precision/F1 几乎全面上升，"整个落错子系统"的 Wrong 案例大幅下降。
- 结论三：优势在 Q/CF/SH 三类与 Easy/Medium/Hard 三档上持续，SH（散点、冷路径、跨模块）收益最大。
- **自承边界**：只测定位与计划质量，不测最终代码一次通过；LLM-as-judge。

### 2.5 Handbook Studio（工作台形态）

读（三级手册+提问）/ 对照（行为描述⇄源码分屏，点行为单元开对应源码）/ 改（Co-Edit：选行为单元、描述改动，生成可审阅的 edit plan + diff，**用户确认前不写仓库、不更新手册**）。仓库始终是真相源。

## 三、对本书的借鉴映射

### 第二卷

| 章 | 借什么 | 怎么用 |
|---|---|---|
| §二 2.4 | L3 模板六字段 ≈ 契约六要素 | 脚注级印证："把隐式行为写成显式结构"已有业界平行发明；字段对照一句话即可 |
| §二 立论 | "模型能做什么→系统允许它做什么" | 厂商侧引语，与 Harness-Bench 23.8pp 互证【预印】 |
| §十 权限 | "删文件先问"行为链跨六类实现点；edge cases 点名 headless、auto-approval、fallback 绕过 | 不变量四"权力有边界不能只靠 prompt"的现成案例 + 审计路径清单 |
| §十二 证据 | ①facts-first 纪律与本卷"声称必须对账到事实"同构；②**术语防漂移**：他们的 evidence=代码证据（静态），本卷 Evidence Plane=运行证据（事件） | ①一句业界回声；②§三术语表加一行区分"行为证据（代码层）/运行证据（事件层）" |
| §十四 评审（**最大借鉴**） | ①审计立场："结论建立在全行为路径的可验证实现证据上，不建立在文档承诺上"；②Codex 规模数字作"评审为什么需要地图"；③应然 vs 实然对照框架：本卷契约/Boundary Map 是规范侧，Handbook 是实现测绘侧，评审=两者对照；④**局限即论点**：描述性工具测不出"缺失的行为"——Howpot Bug 2 那种"该有的持久化根本不存在"无处可映射，正是契约体系不可替代的地方 | 评审章可给 Handbook 一小节：作为行为测绘工具引入，再指出它与契约缺口图的互补关系 |
| §十三 构造 | 参考 runtime 可顺手给自己生成一份行为手册（工具开源、支持 Python/Rust/TS/Go） | 轻提，一句话+链接 |

### 第三卷

- 变更管理/维护章：论文核心命题"行为定位是 harness 演化的中心瓶颈"直接可引；resync 机制=文档随系统演化保持可审计。
- 企业线（onboarding/知识管理）：三级手册作为新成员与审计方的入口。
- 评测方法章：LLM-as-judge win-rate 的自承边界可作诚实标注的正面示例。

### 写作层（不入正文）

BGPD 三级披露与本卷章内结构同构：先系统语境、再行为单元、再 file:line 证据——与 §一开头返工得出的"先给所指再给标签"教训一致，佐证该原则不只是文风偏好。

## 四、不借/慎借

- 它解决"读懂并改对既有 harness 代码"，不解决"runtime 语义该是什么"——与本卷核心章（§四~§九 状态/转移/副作用语义）基本无交集，不要硬塞。
- 评测数字未经评审且为 LLM 评审制，只作方向性引用；硬数字引用前读 arXiv PDF 图表原文。
- "腾讯开源"表述统一为："Tencent HY LLM Frontier 与高校合作、以个人仓库形式开源"。
