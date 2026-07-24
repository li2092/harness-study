# research/volume2 · 第二卷调研原料

为《Harness 架构与工程化》（第二卷）写作收集的调研材料。综合结论见仓库根目录 `volume2-outline.md`。

## 来历

2026-07-10 用 opus workflow（run `wf_2e1f15b2-4aa`）并行跑 6 路调研。3 路完整返回；3 路（OpenAI / 框架 / 生产运维）因 WebFetch 网络请求僵死（无超时看门狗，30+ 分钟零写入）被断路器停止，从转录中抢救出半程检索材料；Anthropic 路提交结构化结果失败但完整成果自存盘获救。缺口随后由主会话用带超时的 curl 直连补齐（07）。这次故障本身将作为第二卷 §十二 的元案例。

## 文件

| 文件 | 内容 | 完整度 |
|---|---|---|
| 01-intro-coverage-map.md | 入门卷 22 章覆盖地图 + 可沿用术语 + 划界建议 | 完整 |
| 02-academic-verification.md | guide 引源逐条核对（含一处勘误）+ 2026 H1 新工作 | 完整 |
| 03-anthropic-route.md | Anthropic 官方工程文章与产品契约 16 条 | 完整 |
| 04-openai-route-raw.md | OpenAI/Codex/Assistants 退役/Temporal 集成检索原料 | 半程原始 |
| 05-frameworks-route-raw.md | LangGraph/Restate/Inngest/ADK/Vercel/Diagrid 检索原料 | 半程原始 |
| 06-production-route-raw.md | OTel/可观测性产品/$47K 复盘/guardrails/配额治理原料 | 半程原始 |
| 07-gap-fills.md | 四缺口补抓：Temporal×OpenAI 机制、Codex 仓库一手、OTel 现状、context anxiety 归因修正 | 完整 |
| 08-howpot-resilience-{audit,review}-2026-07-09.md | Howpot 韧性摸底与复审快照（§一事故一手源，原件在 Howpot 仓库 docs/） | 完整快照 |
| 09-harness-handbook-tencent.md | Tencent HY LLM Frontier《Harness Handbook》（arXiv:2607.13285）调研 + 各章借鉴映射 | 完整 |
| 10-schema-harness.md | Schema Harness：可执行 world model、Plan Lease、Evidence Graph 扩展、评测审计与适用边界 | 完整 |
| 11-howpot-vnext-2026-07-22.md | Howpot vNext 素材快照（07-10→07-22，154 commits）：run lease/ADR-007、SSE terminal 契约/ADR-006、Gate SSOT/ADR-008、第二次审计、evidence 治理、36 条素材按章归位＋暴露面标记＋两个结构裁决项（Attempt 层、lease 分层） | 完整快照 |

## 使用提醒

- 04-06 未经该路 agent 收尾综合，引用前按其中 URL 回核一手。
- 02 与 07 含对 harness-engineering-guide.md 的勘误，正式写作必须采纳（汇总见 volume2-outline.md 附录 B）。
