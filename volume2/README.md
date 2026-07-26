# Harness Study · 第二卷《架构与工程卷》· 正文

> **本卷定位**：怎样构造一个语义正确、可中断、可恢复、可验证的 Agent Harness runtime。入门卷（`../introduction/`）讲部件学；本卷讲这些部件怎样组成一个正确的运行时。生产工程（数据库运维、安全治理、发布、SRE、成本）在第三卷。
>
> **规格文件**：`../volume2-outline.md`（大纲 v5.4）是本卷的 spec——章节结构、每章模板、事实修正纪律、素材指针都以它为准。正文与 spec 冲突时，先改 spec 再改正文。逻辑框架与写作流程见 `SPEC.md`。

## 目录与写作状态

2026-07-17 起按阅读顺序逐章写、一章一审。**2026-07-19 三章用户审回（叙述散、无自上而下推理主线、需脱敏），流程改 spec 先行：卷级论证树与十四章问题链见 [`SPEC.md`](./SPEC.md)，每章先审章 spec 再写正文**；语言与审稿纪律仍在 `WRITING-PLAN.md`。**2026-07-20 大纲 v5.4 手术**：§一瘦身为一条主线（章级判据 12 新概念/10 前向引用/2 表）；下沉件归属（编号已按 v5.5 顺移）：实体链→§六、Routing Matrix→§五、五平面＋干预点→§十一、双层控制流→§十二、部署→§十四、两种 graph→§八；"六不变量"并入六契约承诺句、术语退役。**2026-07-21 大纲 v5.5 手术**：新增"§四 参考架构蓝图"为第二部分开篇（用户裁决方案 A），原 §四–§十四 顺移为 §五–§十五，全卷 15 章；手术前文件里的旧编号按大纲读法规则映射。

| 章 | 文件 | 状态 |
|---|---|---|
| §一 参考架构与检验坐标系 | [`01-architecture-v4.0.md`](./01-architecture-v4.0.md) | **v4.0 用户过审（2026-07-21，"质量大幅提高"；含用户增补反格言段与 STAR 完备性回扫）**；章名已回写大纲；v3.0（瘦身版）与 v2.1 留档对照 |
| §二 什么叫"正确的 runtime" | [`02-correct-runtime-v1.0.md`](./02-correct-runtime-v1.0.md) | **v1.0 用户过审（2026-07-21；开场按 STAR＋指向裁决改写，SPEC §七.9 由此确立）**；四维评审 technical B+/style A-/cybernetic A-（方法论比例 64%）/business B+ 已落实；v0.4 留档对照 |
| §三 一次"数据丢失"事故：判据的反向验证 | [`03-incident-v2.0.md`](./03-incident-v2.0.md) | **v2.0 用户过审（2026-07-21，"继续下一章"；含庭审修辞收掉与锚链正式化两批语域增量）**；四维评审 technical A-/style A-/cybernetic A-（方法论比例 55%）/business B+ 已落实；章名副题已回写大纲；v1.0 留档对照 |
| §四 参考架构蓝图 | [`04-blueprint.md`](./04-blueprint.md) | **v1.0 用户过审（2026-07-21，"继续下一章"；含语域清理与两张"八件"清单接线两批用户初审增量）**；四维评审 technical A-/style B+/cybernetic A-（设计空间占比 78%）/business A- 已落实；Component Register 入 90-artifacts G 节并列入 §十五 工具清单；章 spec 见 SPEC §十一 |
| §五 Run 生命周期状态机 | [`05-run-lifecycle.md`](./05-run-lifecycle.md) | **v1.0 用户过审（2026-07-23，"进 §六"；含 STAR 跨章回指回扫增量）**；四维评审 technical A-/style A-/cybernetic A-（方法论比例 60%）/business B+ 已落实；交付 90-artifacts H 转移表 17 行＋E Routing Matrix v1 |
| §六 状态、事件与持久化 | [`06-state-persistence.md`](./06-state-persistence.md) | **v1.0 用户过审（2026-07-23，"继续"；Attempt 不设实体、lease 分层两项结构裁决随过审确认）**；四维评审 technical A-/style A-/cybernetic A-（方法论比例 60%）/business B+ 已落实；交付 A v2＋I/J/K；悬案留档：model-based harness 项目是否实名（终稿裁决，涉 6.12 与第十三章） |
| §七 Durable Execution 与重放 | [`07-durable-execution.md`](./07-durable-execution.md) | **v1.0 用户过审（2026-07-23，"过审，进入下一章"）**；四维评审 technical A-/style A-/cybernetic A-（方法论比例 62%）/business A- 已落实；交付 90-artifacts L 节（恢复语义表＋durability 选型记录） |
| §八 工具执行与副作用 | [`08-tools-effects.md`](./08-tools-effects.md) | **v1.0 用户过审（2026-07-23，"继续第九章"）**；四维评审 technical A-/style A-/cybernetic A-（方法论比例约 80%）/business A- 已落实；交付 90-artifacts B v2＋M（Tool Contract）＋N（Plan Lease 与 Counterexample Event） |
| §九 Streaming、中断与人机挂起 | [`09-interaction.md`](./09-interaction.md) | **v1.0 用户认可推进（2026-07-23，"继续写正文"）**；四维评审 technical A-/style A-/cybernetic A-（方法论比例约 78%）/business 合规达标 已落实；交付 90-artifacts O（流终结真值表）＋P（交互语义表） |
| §十 Context、Memory 与 Artifact 的连续性 | [`10-context-continuity.md`](./10-context-continuity.md) | **v1.0 用户过审（2026-07-23，"继续"）**；四维评审 technical A-/style A-/cybernetic A-（方法论比例约 80%）/business 合规达标 已落实；交付 90-artifacts Q/R/S |
| §十一 权限、身份与运行时隔离 | [`11-permissions.md`](./11-permissions.md) | **v1.0 用户过审（2026-07-24，"继续"）**；四维评审四路已落实（technical A-/style A-/cybernetic A- 方法论比例约 76%/business 合规达标，零 P0）；交付 90-artifacts T/U/V＋D/F 填充。**待终稿：第一章"六类契约表"节号 1.7→1.2（v4.0 无 1.7，§十二评审查出的全书 drift，L83/L125）** |
| §十二 多 Agent 协调 | [`12-multi-agent.md`](./12-multi-agent.md) | **v1.0 用户过审（2026-07-24，"继续"）**；含用户加调研的 SOTA（Codex 桌面端 worktree＋子继承收窄沙箱、Devin verifier agent、Cursor 3.0、Claude Code dynamic workflow、框架四家双层控制流、MAST）；四维评审已落实（technical A-/style 达标/cybernetic A- 77%、代价末环七点全落/business 合规达标，零 P0）；交付 90-artifacts W |
| §十三 Evidence Plane | [`13-evidence.md`](./13-evidence.md) | **v1.0 用户过审（2026-07-24，"继续"）**；evidence plane＝只追加＋全量关联链＋事实/解释分账＋correlation 八级兑付第十二章＋两类沉默失败（absence/sabotage validation）收口第二章＋content 敏感（tracing≠telemetry）＋认识论七边与 Model Certificate scope；四维评审已落实（technical B+→A-（四纪律补全＋session→conversation）/style A-/cyber A- 约 80%、代价末环八点全落/business 合规达标 Schema 引用铁律全守，零 P0）；交付 90-artifacts C 升 v2＋X/Y/Z |
| §十四 从零构造一个最小但完整的 Runtime | [`14-build.md`](./14-build.md) | **v1.0 用户过审（2026-07-24，"继续"）**；可运行骨架逐步点亮六契约＋依赖顺序＝构造纪律＋点亮判据＝失败 trajectory 非 happy path＋标准故障包＝九 fixture 汇编验收 SSOT＋executable spec 底线/reference impl 加分＋部署基线切换信号；收口全卷主线"部件正确加不出系统正确"于集成正确性；四维评审已落实（technical B+→A-/style B+→A-/cyber A- 约 85% 代价末环 8/8/business 合规达标，零 P0）；交付 executable spec＋标准故障包（不新增 A-Z 工作制品） |
| §十五 Runtime 架构评审 | [`15-review.md`](./15-review.md) | **v1.0：按 SPEC §二十二 spec 首写（卷级出口：评审＝拿全卷登记表逐项提问、产出残余风险清单＋owner 非判决＋五件工具复用工作制品 G/A/B/D＋Runtime Contract Matrix＋90 分钟八步流程（首步「对组件图」系 2026-07-26 用户裁决补入）＋两条文化判定线 harness vs framework 思维/敢不敢动 core＋收束"模型可以不确定 runtime 不能不知道自己发生了什么"回扣全卷）。四维评审四路已落实（technical A- 零 P0/style B+→A-/cybernetic A- 方法论比例约 78%、代价末环补齐 5/5＋收束尺易主/business 合规达标 脱敏纠误＋Diagrid 竞争方标注，零 P0），待用户审**；不新增 A-Z 工作制品 |
| 工作制品（State Registry / Effect Ledger / Event Schema / Runtime Trust Boundary） | [`90-artifacts.md`](./90-artifacts.md) | **v2.7，随各章升级（A–Z）** |
| 参考附录（概念主线索引 / 术语速查 / 探针与观测点 / 字段字典导览 / 图表清单） | [`99-appendix.md`](./99-appendix.md) | **v1 骨架（2026-07-23）：主线索引＋图表清单已做全第一至九章；术语/探针/字段导览立形态＋样张，待用户审形态后批量填满** |

## 写作纪律（每章开工前过一遍）

- 每章固定模板：症状/事故 → 契约归属 → 传统 CS 根基 → Agent 增加的变量 → 轻量/标准/重型三档 → 进入贯穿实现 → 主动破坏一次 → 可复用 artifact。
- 来源五级标注（【评审】【预印】【规范/官方文档】【厂商实践】【经验/推导】）；"唯一/空白/收敛"必附检索范围与日期。
- 事实修正纪律 8 条见大纲第四节；MCP 2026-07-28 定稿后回核三处。
- 术语以 §三 冻结的词汇表为准；与入门卷冲突时以 §3.6 对照表为准。
- 配图沿用 jimi-ink 视觉，正文用"（配图占位：…）"标注，成稿后统一补图并清除占位注中的"jimi-ink"字样（脱敏 checklist 项，不依赖逐处记忆）。
- 案例真实性与脱敏声明走卷级：出版前在卷首"关于案例"说明统一声明（案例真实、可识别信息已隐去、数字与时间线未改）；正文不放裸声明句（2026-07-21 用户裁决，撤回 §三 内联声明；§二 首现处括注保留，终稿随卷首说明一并复核）。脱敏标准：关键名字脱敏、产品功能与作用照实说清即可，不设暴露面台账（2026-07-22 用户裁决，SPEC §七.6）。
- 章节引用文字化（2026-07-23 用户裁决，SPEC §七.10.5）：正文用"第五章""第一章 1.4 节"，不用"§"符号。第六章起执行；**第一至五章与 90-artifacts 的既有 §N 表述终稿前统一替换**（与 jimi-ink 占位清除同批的机械手术项；含 v2.2-v2.5 新增/填充的 B/M/N/O/P/Q/R/S/T/U/V 节与 D/F/A 行的 §N）。
