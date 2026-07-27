# Harness Study · 第二卷《架构与工程卷》

> **本卷定位**：怎样构造一个语义正确、可中断、可恢复、可验证的 Agent Harness runtime。入门卷（[`../introduction/`](../introduction/)）讲部件学；本卷讲这些部件怎样组成一个正确的运行时。生产工程（数据库运维、安全治理、发布、SRE、成本）在第三卷。

## 目录

| 章 | 文件 |
|---|---|
| 一、参考架构与检验坐标系 | [`01-architecture.md`](./01-architecture.md) |
| 二、什么叫"正确的 runtime" | [`02-correct-runtime.md`](./02-correct-runtime.md) |
| 三、一次"数据丢失"事故：判据的反向验证 | [`03-incident.md`](./03-incident.md) |
| 四、参考架构蓝图 | [`04-blueprint.md`](./04-blueprint.md) |
| 五、Run 生命周期状态机 | [`05-run-lifecycle.md`](./05-run-lifecycle.md) |
| 六、状态、事件与持久化 | [`06-state-persistence.md`](./06-state-persistence.md) |
| 七、Durable Execution 与重放 | [`07-durable-execution.md`](./07-durable-execution.md) |
| 八、工具执行与副作用 | [`08-tools-effects.md`](./08-tools-effects.md) |
| 九、Streaming、中断与人机挂起 | [`09-interaction.md`](./09-interaction.md) |
| 十、Context、Memory 与 Artifact 的连续性 | [`10-context-continuity.md`](./10-context-continuity.md) |
| 十一、权限、身份与运行时隔离 | [`11-permissions.md`](./11-permissions.md) |
| 十二、多 Agent 协调 | [`12-multi-agent.md`](./12-multi-agent.md) |
| 十三、Evidence Plane | [`13-evidence.md`](./13-evidence.md) |
| 十四、从零构造一个最小但完整的 Runtime | [`14-build.md`](./14-build.md) |
| 十五、Runtime 架构评审 | [`15-review.md`](./15-review.md) |
| 工作制品汇编 · 全卷登记表的单一真相源 | [`90-artifacts.md`](./90-artifacts.md) |
| 附录 · 第二卷速查与图解 | [`99-appendix.md`](./99-appendix.md) |

## 配图

全卷 34 张编号配图与 80 张排版替换图（表格与 ASCII 图的图片化）统一存放在仓库根 [`../diagrams/`](../diagrams/)，与入门卷共用一个图库，正文以 `../diagrams/*.png` 引用。图源（html）、出图脚本与表格内容 SSOT 维护在配套工程仓，不入本仓；改表走 SSOT 重渲，不手改 PNG。

## 编辑区说明

各章文末的「审稿日志」「引用来源」「变更记录」是写作过程工作区，出版时由构建管线剥离。写作规范、审稿记录与 PDF 出版管线维护在配套工程仓，不入本仓。
