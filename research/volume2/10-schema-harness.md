# Schema Harness：可执行世界模型、反例驱动规划与评测审计

调研日期：2026-07-19  
对象：Schema Harness 发布页、公开 ARC-AGI-3 trajectories、项目仓库、ARC Prize 官方结果与相关论文  
用途：第二卷 §五、§七、§十二、§十三；第三卷 §十三、§十四、§十九

## 一、结论先行

Schema Harness 最值得借鉴的不是某个 ARC-AGI-3 技巧，而是把“agent 对世界的理解”从 prompt 中的隐式文字，变成一个可执行、可版本化、可反驳的中间工件：

1. agent 同时学习状态表示和转移机制，将当前信念写成 Python world model；
2. 每次规划前，用完整交互历史 backtest 当前模型；
3. 在模型内部搜索候选计划，只有 `commit_actions` 能触碰真实环境；
4. 每个真实动作后对比预测与观察；一旦不一致，立即废止剩余计划，把差异作为反例回到建模循环。

这仍然是 loop，不是“loop 被 graph 取代”。外层是 `observe → deliberate → execute → record`；内层是 `theorize/write code → certify/backtest → plan/search → commit`。`run_bfs` 搜索的是当前 world model 隐含的**世界状态转移图**，而 workflow graph 管的是任务、节点、分支、并行与 join。两种 graph 位于不同层，可以同时存在。[S1][S2]

对通用 Harness 的可迁移抽象是：

- `world_model.py` → 版本化 Belief/World Model；
- `run_backtest` → Model Certificate；
- `run_bfs` → planner/dry-run/sandbox search；
- `commit_actions` → 受控 Effect Gateway；
- prediction mismatch → Counterexample Event；
- “计划只对某个模型成立” → Plan Lease。

## 二、它特别在哪里

### 2.1 “Schema”不是 JSON Schema

项目借用的是 Kant 意义上的 schema：不是静态分类，也不是数据校验格式，而是“生成某类经验对象的构造规则”。在实现上，每个游戏的状态表示和动态规律由 agent 写进一个可执行 Python 程序。相比自然语言笔记，它同时具备四个性质：

- **可执行**：能给定状态和动作计算下一状态；
- **可反驳**：预测与真实 observation 可以逐步比较；
- **可搜索**：planner 能枚举模型中的状态转移；
- **可审计**：模型版本、差异和历史拟合结果可以保存。

这里真正重要的是“representation learning 与 mechanism discovery 联合发生”：新反例可能要求修改转移函数，也可能暴露原有 state representation 根本没有记录决定未来的变量。只修规则、不修状态表示，会得到一个永远靠补丁追赶的模型。[S1][S5][S6]

### 2.2 把思考与真实动作分账

Schema 将内部计算和外部环境动作分开：编辑模型、回放历史、运行 BFS 都不消耗环境动作；只有 `commit_actions` 会产生真实 interaction。这个边界有两层价值：

- 安全与可控：真实副作用集中通过单一 gateway；
- 经济性：当真实动作昂贵而内部仿真便宜时，可以先搜索再执行。

但“零环境动作”不等于“零成本”。模型 token、代码执行、BFS 节点扩展、CPU、wall-clock 和失败重跑仍应单独计量。Schema 的 RHAE 只奖励完成与 action efficiency，不覆盖内部计算成本。[S1][S4]

### 2.3 反例不是日志，而是控制流事件

Schema 不只是记录 prediction mismatch；它让 mismatch 直接改变控制流：丢弃尚未执行的动作队列，回到建模和验证。对公开 Claude/Fable FT09 `events.jsonl` 的逐行统计得到 78 个 `action_taken`、17 次 `run_backtest`、2 次 `run_bfs`、15 次 `commit_actions`、9 个 `model_mispredicted` 和 15 个 turn；多次误预测后均重新进入建模/提交流程。这说明“预测错误即 plan invalidation”不是发布文案中的抽象主张，而是轨迹里的实际机制。[S2]

这比一般“先计划、再执行”多一个关键约束：计划有适用前提，前提失效时计划也必须失效。通用化后可定义：

```text
PlanLease = {
  plan_id,
  model_version,
  history_cursor,
  policy_version,
  preconditions,
  expires_at
}
```

任一真实 observation 与预测不符、history cursor 前移但模型未重新认证、policy/authority 变化，均使 lease 失效。恢复、重试或 worker migration 不得只恢复动作队列而漏掉 lease 校验。

### 2.4 代码是信念工件，不是真相源

`world_model.py` 很容易被误读成 SSOT。正确分层是：

- 交互 timeline / event history：发生过什么，append-only ground truth；
- world model：agent 当前相信世界怎样运作，可变、可错；
- notes：工作记忆与假设，可变、非权威；
- plan：从某个 model version 派生的临时工件；
- environment outcome：外部世界实际发生了什么。

因此 world model 应进入 State Registry，但类型必须标成 `derived belief artifact`，不能覆盖原始 observation。它的 provenance 至少包含生成它的 history cursor、模型/提示/工具版本、backtest 范围和失败反例。

## 三、与 loop、workflow graph、Evidence Graph 的关系

### 3.1 三种控制结构不要混名

| 结构 | 节点/边是什么 | 解决什么问题 | Schema 中的位置 |
|---|---|---|---|
| Agent loop | observation、decision、action、feedback | 在线闭环适应 | 外层持续存在 |
| Workflow graph | task/node、branch、join、retry、handoff | 多步骤编排与全局控制流 | Schema 未以此为主要创新 |
| World-state graph | state、action、predicted transition | 在当前世界模型中搜索可行计划 | `run_bfs` 展开 |

所以，“工程从 loop 进化到 graph”只能描述编排层能力扩展。Schema 展示的是另一条演进：**loop 内新增可执行 belief model，并在其产生的状态图上规划**。一个生产系统完全可以由 workflow graph 调度多个 node，每个 node 内运行 Schema 式 model-based loop。

### 3.2 对现有 Evidence Graph 的扩展

Schema 适合补入以下认识论边，而不是另造一张平行图谱：

```text
observation    --grounds------> belief/model_version
model_version  --predicts-----> transition
history_set    --certifies----> model_version
counterexample --refutes------> model_version
plan           --derived_from-> model_version
commit         --realizes-----> plan
mismatch       --invalidates--> remaining_plan
```

Evidence Graph 原先主要回答“动作、结果、artifact、完成声明如何对账”；这些边补上“为什么系统相信当前模型，以及什么证据推翻了它”。注意 `certifies` 必须带 scope：完整历史 backtest 只证明 retrodictive consistency，不证明未见状态上的 generalization。

## 四、证据强度与可复用范围

### 4.1 公开材料能确认什么

- 发布页公开了过程说明、固定 fallback 规则、逐游戏结果和若干轨迹片段，并明确称 98.98% 与 95.35% 是 Public set 的 self-reported 结果，未获 ARC Prize 独立验证，也没有 Semi-Private、held-out 或 frozen-harness 结论。[S1]
- Hugging Face 数据集有 50 行，即 25 个 Claude/Fable 结果和 25 个 GPT-5.6 Sol 结果；目录包含 `events.jsonl`、清理后的 session、world-model snapshots、notes、run metadata 和 scorer，可复算公开工件中的分数与部分过程统计。[S2]
- GitHub 组织公开仓库截至 2026-07-19 只有 `.nojekyll`、README 和一个静态 `index.html`，没有 Schema runtime/harness 源码；Hugging Face dataset card metadata 为空，项目仓库也未声明 license。可研究不等于可直接复制进产品。[S2][S3]

### 4.2 结果数字怎样读

发布页报告：Claude Opus 4.8 与 Fable 5 的组合为 98.98% RHAE，GPT-5.6 Sol 组合为 95.35%。两组都采用固定 fallback：先跑 Opus 4.8 / Sol xhigh，低于 80 的游戏分别用 Fable 5 / Sol max 重跑，并保留较高的逐游戏结果。[S1]

因此该数字属于**自适应 portfolio / best-of-two 后处理结果**，不是单模型、单次运行的 pass@1。结合页面披露的 fallback 规则与数据集恰好 2×25 条记录，可以推断公开包只包含最终计分 trajectories，没有包含被 fallback 淘汰的全部运行；可以核算“已发布计分集”，不能从这些工件独立重放完整选择过程或证明 held-out 泛化。[S1][S2]

官方 ARC Prize 对 GPT-5.6 Sol Max 的最近参照是 Public 13.33%、Semi-Private 7.78%。这不是 matched harness comparison：模型 effort、运行策略、fallback、动作预算和 harness 均不同，因此只能证明 harness/protocol 对结果可能影响极大，不能把 82.02pp 差值全部归因为 Schema 的某个单一机制。[S4]

发布页还报告“Claude Code scratch snapshot 作为 baseline 为 42.83%，Schema 为 98.98%”。但公开的 50 条保留轨迹没有提供该 baseline 的等量完整 artifacts 和 matched protocol，故将其标为项目自述，而不是可独立复现的受控消融。[S1][S2]

### 4.3 `run_backtest` 的保证边界

对完整历史逐步回放能排除大量自洽幻觉，但只证明模型解释了已观察样本：

- 可能过拟合某个 level 的常量；
- 可读代码不自动等于简单、正确或可泛化；
- planner 可能主动寻找模型漏洞，得到现实中不可执行的“最优解”；
- BFS 的完备性只相对于当前状态表示、转移函数和搜索边界成立。

公开工件中存在很大的 final world model 和多份 level-specific candidate program，说明“代码化”带来 inspectability，却不会自动带来最小描述或泛化。[S2]

生产化时 Model Certificate 至少应并列记录：

1. full-history replay；
2. prospective next-step prediction；
3. held-out transition / leave-one-episode-out；
4. invariant 与 property-based tests；
5. planner-adversarial test：主动搜索会利用模型漏洞的计划；
6. certificate scope、history cursor、model version、测试覆盖与已知反例。

## 五、学术位置：组合很强，原语并非全新

Schema 的核心原语已有明确前史：

- **WorldCoder**（NeurIPS 2024）已经让 model-based LLM agent 用 Python program 表达世界知识，并通过环境交互与 planner 约束持续修正模型。[S5]
- **VIGA** 用 code-render-inspect loop 连接可执行 scene program、感知与符号交叉验证，支持“代码作为可检验中间表示”的一般性。[S6]
- **Executable World Models for ARC-AGI-3** 已经在同一 benchmark 上使用可执行 Python world model、历史验证、先规划后行动和近似 MDL 的重构；论文报告 GPT-5.5 high 在 25 个 Public games 上为 58.12%，且明确尚无 private validation 结果。[S7]
- **ARC-AGI-3** 本身要求 agent 探索陌生的抽象回合制环境、推断目标、建立动态模型并规划；benchmark 论文报告人类可解 100%，而 2026-03 的 frontier systems 低于 1%。[S8]

所以 Schema 的新意更准确地说是：把 executable world model、history-wide certification、search、guarded commit、mismatch-triggered invalidation 和 coding-agent workspace 组合成一套纪律明确的 harness，并公开了足够多的 retained trajectories 供审阅。不要写成“首次发明可执行世界模型”或“证明了 Public 分数能泛化到私有集”。

## 六、适用范围与生产映射

最适合 Schema 原型的环境具备：状态紧凑、动作离散、转移大体确定、真实动作昂贵、内部仿真便宜、结果可即时观察。企业 Agent 很少完全满足，但可以降维借鉴：

| Schema 原件 | 企业 Harness 映射 | 例子 |
|---|---|---|
| world model | contract/causal belief map | 订单状态机、航班保障约束、变更依赖 |
| backtest | replay + invariant + integration tests | 历史工单回放、状态转移验证 |
| BFS/search | dry-run、sandbox、what-if planner | 发布计划、恢复编排、资源调度 |
| commit_actions | Effect Gateway | 发消息、改数据库、调用生产 API |
| prediction mismatch | Counterexample Event | API outcome 与预期状态不一致 |
| discard plan | Plan Lease invalidation | 停止后续写操作并重新规划 |

不适合强行套用的情形：状态连续且高维、强随机、观察严重部分可见、其他主体会并发改变世界、仿真成本接近真实执行，或错误 world model 会制造高风险虚假确定性。此时仍可保留 Plan Lease 和 Counterexample Event，但不要承诺搜索完备性。

## 七、落入大纲的具体位置

- 第二卷 §五：将 Belief/World Model 定义为 derived mutable artifact，与 event history、notes、plan 和 outcome 分层。
- 第二卷 §七：增加 guarded commit 和 Plan Lease；每次真实动作都校验 lease，prediction/policy/authority mismatch 立即废止剩余计划。
- 第二卷 §十二：扩展 Evidence Graph 的 `grounds/predicts/certifies/refutes/derived_from/invalidates` 边；Model Certificate 必须带 scope。
- 第二卷 §十三：在一个可显式建模案例中实现最小 world model → replay certificate → search/dry-run → guarded commit → counterexample/replan 闭环。
- 第三卷 §十三：加入 prospective、held-out、property 和 planner-adversarial tests，防止把历史拟合当泛化。
- 第三卷 §十四：强制披露 pass@1、best-of-n、fallback/portfolio、保留/丢弃运行、public/held-out、frozen harness 和计算成本。
- 第三卷 §十九：环境动作、模型 token、搜索节点、CPU、wall-clock 分账。

## 八、来源

| 编号 | 来源 | 类型与本笔记用途 |
|---|---|---|
| S1 | [Schema Harness launch post](https://schema-harness.github.io/) | 【项目自述】架构、工具语义、fallback、分数、验证状态与案例片段；宣传性结论不自动视为独立证据 |
| S2 | [ARC-AGI-3 Schema Traces dataset](https://huggingface.co/datasets/schema-harness/arc-agi-3-schema-traces) | 【公开工件】50 条计分 trajectories、events、sessions、snapshots、artifacts、scorer；结合 fallback 规则推断未包含完整淘汰运行 |
| S3 | [schema-harness.github.io repository](https://github.com/schema-harness/schema-harness.github.io) | 【源码仓库】截至 2026-07-19 仅静态站点文件，无 runtime 源码与 license 声明 |
| S4 | [ARC Prize: GPT-5.6 Series verified results](https://arcprize.org/results/openai-gpt-5-6) | 【官方评测】Public 13.33%、Semi-Private 7.78% 的最近官方参照；不是 matched harness comparison |
| S5 | [WorldCoder](https://arxiv.org/abs/2402.12275) | 【评审论文】Python world model、planner 与交互修正的直接前史（NeurIPS 2024） |
| S6 | [Vision-as-Inverse-Graphics Agent](https://arxiv.org/abs/2601.11109) | 【预印本】code-render-inspect 与可执行中间表示的邻近工作 |
| S7 | [Executable World Models for ARC-AGI-3 in the Era of Coding Agents](https://arxiv.org/abs/2605.05138) | 【会议接收论文/预印本版本】ARC-AGI-3 上的可执行模型、验证与规划直接前史；AGI-2026 accepted |
| S8 | [ARC-AGI-3 benchmark paper](https://arxiv.org/abs/2603.24621) | 【基准论文】任务定义、RHAE 背景、人类/模型基线与外推边界 |

引用纪律：正文涉及 98.98%、95.35%、42.83% 时必须同时写“项目自述、Public、fallback portfolio、未获 ARC Prize 独立验证”；涉及“开源”时写“公开 retained trajectories 与静态站点”，不得写成“Schema runtime 已开源”；未出现明确 license 前，不复制代码进入参考实现。
