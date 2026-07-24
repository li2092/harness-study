# 素材索引 · Agent-Z learn-harness 库 → 第二卷章节映射

> 2026-07-17 · 扫描产出（Explore agent，通读 `/Users/jimi/ClaudeCode/Agent-Z/docs/learn-harness/`）。
> 定性：learn-harness 是另一本书（Agent-Z harness 工程方法论）的工作库，与本卷主题重叠但视角不同；对本卷的价值是**一手工程细节**。引用前按各文件可信度分级回核。

## 一、可信度分级导览

- `_facts/`：**事实库，已核对到源码/日志**，最高可信度；每条 F-* 编号带 Source 行号。
- `chapters/`：canonical 成稿/半成稿；`_legacy/` 低可信。
- `_chapters/draft/2026-05-03-ch01-*`：草稿 + 四路评审全流程（technical/business/cybernetic/style）。
- `_scan-results/`：原始扫描 raw，README 明示"写章节前必须重核"。
- `extraction-cards/`：已核对证据卡（review_status: checked）。
- `explainers/what-is-harness/`：入门卷草稿演进史，非本卷正文素材。
- `_review-notes/`：169 份旧素材池，多数待重抽取，低优先。

## 二、素材 → 章节映射（写到对应章时精读）

### §二 什么叫"正确的 runtime"
- `chapters/ch10-anti-self-deception.md`（约 8500 字成稿）——**§2.8 四层自欺框架的原稿**（commit/eval/strategy/position 四层 + 各层真相检测动作），大纲标"作者观点内化"，此文可直接搬运改写。
- 同文 1.1：Agent-Z P0 Spine 假落地实证——11 commit 合并、cargo test 287/287 全过，审计后真验收 29/44，`set_hook_registry` 从未被调用——"写了错误处理 ≠ 故障有归宿"的一手案例。
- `_facts/2026-05-03-artifact-claim-mismatch-facts.md` F-K01/F-K06："report.pass=true 不能作为通过证据""会污染 reward"——直接引语。

### §四 Run 生命周期
- `_facts/2026-05-07-deepseek-p0-p1-review.md` F-T02/F-T04：RuntimeStateManager / SQLite lock poison-safe（`poisoned.into_inner()` 恢复）——锁中毒收敛实例。
- `_scan-results/agent-c-git-history.md`：Agent-Z `66a41fd` Take-Run-Return + select! cancel（P0 mutex/cancel/blocking）、`9009826` StrictMode double-invoke 双根因——并发/抢占语料。
- `_scan-results/agent-b-conversation-cases.md` case 15/13（停止按钮后台还在跑）、case 45（last_response 未重置致 MaxTurnsExceeded）。

### §五 持久化
- `_scan-results/agent-c-git-history.md` `099372c`：RAII txn + WAL restore + CASCADE。
- `chapters/ch04-seven-mechanisms-detail.md`（58KB）：七机制详解，作五平面的旧版对照。

### §七 工具与副作用
- `_facts/2026-05-03-artifact-claim-mismatch-facts.md`（**本库最高价值文件**）：F-T01→F-T12 完整 v3-v10 迭代时间线——模型 final JSON 声称创建文件但真实 diff 不含（F-T10），硬门写入 `failure_taxonomy=artifact_claim_mismatch:1`（F-T12）。
- 代码坐标 F-C02/F-C03：`crates/engine/src/harness.rs:2137` 八类硬门、`:2463` 用 `git diff --name-status` 对账语言声称。
- `chapters/ch01-artifact-claim-mismatch.md`（24KB 成稿叙事版，含四路评审）——改写省力。

### §八 Streaming/中断/挂起
- `_scan-results/agent-b-conversation-cases.md` case 23（双 SSE 流交错：finish→persist→finish→suggestions 等 5s→[DONE]，可重入窗口）、case 24（abort 抛 AbortError 时当前 step 的 stepText 永不 push 到 messages——**与 Howpot Bug 2 同构的 partial-not-saved，另一项目独立复现**）、case 27/28（Stop hook 类型约束）、case 41（切会话丢数据）。

### §九 Context 连续性
- `chapters/chapter-context-management.md`（成稿，钦定样章）：CC 5 层压缩（Tool Result Budget→MicroCompact→ContextCollapse→AutoCompact→SessionMemoryCompact）逐层触发 + 前缀稳定约束；AutoCompact 触发 `context>(window-13000)`、3 次失败 circuit breaker、post-compact 重注入最近 5 文件+Plan+Skill；Howpot 双轨消息+qwen-flash 语义摘要作轻档对照。

### §十 权限/隔离
- `_facts/2026-05-07-deepseek-p0-p1-review.md` F-T01：SubAgentTool 子引擎继承 parent safety_policy，workspace escape 触发 `Escalate→Ask→"child agents restricted to read-only"`——subagent 权限收窄的直接实现；F-T05：shell allowlist token-boundary（`cargo checkpoint` 不再被 `cargo check` 放行）。

### §十一 多 Agent
- `_scan-results/agent-a-code-scan.md`：Howpot `H-Relay/provider-queue.ts` 两层并发（Provider 级 + Tier 级 FIFO + 30s reject）、AGWA SubAgentToolkit（run_parallel_subtasks 120-300s 超时分层）。

### §十二 Evidence Plane
- `_facts/2026-05-10-fixture-classifier-bug-facts.md`（**独家**）：路径分类 bug 把 fixture 误判 → baseline 60% 假象、真实 75-87%，"几乎全部来自 manifest 设计 bug 不来自模型"；F-M03/F-M05"failure_taxonomy 不能直接当结论""classifier bug 通常 silent"；F-M06"第一次 baseline 必须 deep dive ≥3 个 fail case"。
- artifact-claim-mismatch facts 的 F-I01/F-I02：三路证据交叉（trace+audit log+snapshot）；Claw-Eval（F-A01-A04，Pass³ Opus4.6 70.4%，trajectory-opaque 漏 44% safety）。
- `extraction-cards/v4-batch-a-2026-05-01.md` lh-card-006：Reference Parity 必须看 evidence_quality（缺 workspace_commit/diff/tests 显示 incomplete）。
- deepseek facts F-K03：用执行计数而非返回值证明工具未执行——detector test 方法论。

### §十四 评审
- fixture-classifier facts 全文——"用错统计口径"经典案例 + 评审流程处方。

## 三、与 harness-study 已有素材的关系

**重叠（不重复搬）**：学术立论以 `research/volume2/02` 为权威版；context 压缩机制入门卷 §5.4 已有框架（chapter-context-management.md 是增量深化）；Bug 2 三域映射 guide §六已有。

**纯增量（harness-study 没有）**：artifact_claim_mismatch 硬门 v3-v10 完整迭代；四层自欺框架成稿；fixture classifier 沉默 bug 反转 baseline；subagent safety / lock-poison Rust 实现；50 条会话 case + 9 项目 git 语料。

## 四、§一 事故素材（最高优先）

**learn-harness 内没有 Bug 2 事故正文**。一手源在 Howpot 仓库，已快照进本仓库：

- `../research/volume2/08-howpot-resilience-review-2026-07-09.md`（**§一金矿**）：§二"确认问题与修复映射"三批表格——Bug 2 直系素材在第二批（原 L29-34）：`tryStart 同会话并发抢占 TOCTOU`（双标签页/双击→后到者静默 abort 先到者新 run，整轮跳过持久化，占位行永久卡"生成中"）、`外链拦截只覆盖 Thread 一处`、`10s 抢占等待兜底放行后占位行卡死`；§四"经验沉淀"5 条是 §一→§二 过渡论点；§三 10 条验收清单可作 §十三故障包。
- `../research/volume2/08-howpot-resilience-audit-2026-07-09.md`：四阶段方案，与 review 互补。
- `/Users/jimi/ClaudeCode/Howpot/H-Relay/docs/resilience-hardening-2026-07-09.md`：H-Relay 侧 4 路摸底（500 消息墙/断路器/first-token 延迟）。
- `../harness-engineering-guide.md` §六：三域交叉因果链——§一叙事骨架的现成版本。

完整度：因果链、三域归属、逐条失败场景、修法、验收清单齐全，支撑 §1.1-1.6 全部小节；唯一需补：1.4 的 state-event-effect 逐帧时间线需据 review 第二批表格重构（现有素材是问题清单式）。
