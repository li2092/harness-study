# Harness Study · The Engineering Practice for AI Agents · The Introductory Volume

This volume was revised in September 2026. If you read the earlier edition, start with the [revision notes](../introduction/00-revision-notes.md) (in Chinese).

> **What this volume is**: the **entry-level introduction** to the Harness Study project, answering "what an agent harness is and which parts make it up." Its main axis is a **platform-independent engineering-practice methodology**, with the companion implementation projects serving as engineering cases that back it up.
>
> **Where it sits in the whole of Harness Study**: this is the opening introductory volume, and it **walks through the full skeleton once**: the 8 runtime mechanisms, the Safety control plane, engineering patterns, the Harness Lab, the composability matrix, and the four cybernetic principles. Each part gets a complete mental model at three levels: What, Why, and How to start. **Chapter-by-chapter and module-by-module expansion volumes will follow.** Each runtime mechanism, each engineering pattern, the five layers of the Harness Lab, and more will get a deep volume of its own, covering finer engineering practices, industry cases, and the pitfalls met in practice.

## Contents

This volume is split by chapter, one file per chapter; §V (the essential mechanisms) has one file per detail. Read in the order of the table below (file names 01 → 99).

| Section | File | Subject |
|---|---|---|
| Revision notes | [00-revision-notes.md](../introduction/00-revision-notes.md) (in Chinese) | What changed in the September 2026 revision |
| §I | [01-why-harness.md](./01-why-harness.md) | What problem we are actually solving |
| §II | [02-prehistory.md](./02-prehistory.md) | Prehistory: when models were used as functions (2020–2022) |
| §III | [03-autogpt.md](./03-autogpt.md) | The first large-scale trial and error: the AutoGPT wave and its failure (2023) |
| §IV | [04-harness-emerges.md](./04-harness-emerges.md) | The emergence of the harness concept (mid-2023 – 2026) |
| §5.0 | [05-00-mechanisms-overview.md](./05-00-mechanisms-overview.md) | 8 runtime mechanisms + 1 Safety control plane · the cut, and abstract function vs. implementation |
| §5.1 | [05-01-agent-loop.md](./05-01-agent-loop.md) | Agent Loop · Inner Loop · the agent's thinking structure · **P0** |
| §5.2 | [05-02-model-adapter.md](./05-02-model-adapter.md) | Model Adapter & Routing |
| §5.3 | [05-03-tool-registry.md](./05-03-tool-registry.md) | Tool Registry & ACI · **P0** |
| §5.4 | [05-04-context-memory-artifact.md](./05-04-context-memory-artifact.md) | Context / Memory / Artifact |
| §5.5 | [05-05-prompt-assets.md](./05-05-prompt-assets.md) | Prompt Assets · Instruction Layer · **P0** |
| §5.6 | [05-06-observation-surface.md](./05-06-observation-surface.md) | Observation Surface |
| §5.7 | [05-07-trajectory.md](./05-07-trajectory.md) | Trajectory · Event Stream · **P0** |
| §5.8 | [05-08-verifier.md](./05-08-verifier.md) | Verifier · three layers · **P0** |
| §5.9 | [05-09-safety.md](./05-09-safety.md) | Safety control plane · cross-cutting |
| §5.10 | [05-10-turn-walkthrough.md](./05-10-turn-walkthrough.md) | The micro-flow of a single turn |
| §5.11 | [05-11-end-to-end.md](./05-11-end-to-end.md) | A mid-size end-to-end example · 17 steps fixing a logging bug |
| §VI | [06-engineering-patterns.md](./06-engineering-patterns.md) | Engineering patterns · cross-mechanism reusable engineering combinations |
| §VII | [07-harness-lab.md](./07-harness-lab.md) | Harness Lab · Outer Loop · systematically optimizing the harness itself |
| §VIII | [08-composability.md](./08-composability.md) | Composability matrix · encapsulation × topology × interaction boundary |
| §IX | [09-cybernetics.md](./09-cybernetics.md) | Four cybernetic principles · the meta-rules that bind the whole tutorial |
| §X | [10-learning-path.md](./10-learning-path.md) | Learning paths · how three kinds of reader should use this tutorial |
| Companion · Prompt | [11-harness-prompt.md](./11-harness-prompt.md) | Harness Prompt · the executable implementation spec for an agent (Phase 0–3 + a gate per step) |
| Companion · Prompt lite | [12-harness-prompt-lite.md](./12-harness-prompt-lite.md) | The generic implementation prompt (eval-first), lite version: three instructions handed straight to a coding AI |
| Appendix | [99-appendix.md](./99-appendix.md) | A primary source index · B the Evidence Graph ten edges · C OWASP LLM Top 10 · D mechanisms mapped to industry products · E identity and authorization · F anti-pattern quick reference · G citation index |

> Mechanisms marked **P0** in the contents have the highest priority: skip one and the harness either won't run or can't be relied on when it does (for what the three levels P0, P1, and P2 mean, see the [§V overview](./05-00-mechanisms-overview.md)).
>
> The deep volume on §5.1 is in the expansion volumes to follow (in planning). **The executable companion files are already in this directory**: the implementation spec → [`11-harness-prompt.md`](./11-harness-prompt.md); the implementation prompt, lite version (eval-first) → [`12-harness-prompt-lite.md`](./12-harness-prompt-lite.md); the quick-reference appendix → [`99-appendix.md`](./99-appendix.md).

## Figure index

The volume has 49 figures in all, in one unified jimi-ink visual style, with source files in the sibling [`../diagrams/`](../diagrams/). Each figure is embedded in the body of its chapter; the table below indexes them by chapter.

| Section | Figures |
|---|---|
| §I | the engineering layer the harness adds `t1-comparison-1-gap-en` · the agent productization spectrum `t2-comparison-1-spectrum-en` |
| §II | the three techniques of prompt engineering `t1-comparison-2-prompt-en` |
| §III | AutoGPT's five typical failures `t1-matrix-3-autogpt-en` · the intern analogy `t2-analogy-3-intern-en` |
| §IV | the 2026 naming convergence `t1-timeline-4-naming-en` · five generations of algorithms, their sources of uncontrollability, and the matching constraint layer `t2-matrix-4-generations-en` |
| §5.0 | the mechanism overview `sample-05-mechanisms-overview-en` · abstract function vs. implementation `t1-layered-5.0-abstraction-en` |
| §5.1 | ReAct's eight implicit assumptions and their decay `t1-matrix-5.1-react8-en` · the four-question decision flow for choosing an Agent Loop `t1-tree-5.1-choose-en` · sixteen evolution directions converge on five mainstream Agent Loops `t2-cardgrid-5.1-five-en` · five sources of multi-agent orchestration overhead `t3-cardgrid-5.1-multiagent-en` |
| §5.2 | the four kinds of decision the Routing layer makes `t1-cardgrid-5.2-routing-en` |
| §5.3 | the three things done in order on every tool_call `t1-flow-5.3-toolcall-en` · the four scheduling modes of Tool Batch `t3-cardgrid-5.3-toolbatch-en` |
| §5.4 | the three time scales of Context / Memory / Artifact `t1-comparison-5.4-state-en` · the five-question test for whether to build Memory `t2-tree-5.4-memory-en` · the cross-domain analogy to the OS memory hierarchy `t2-analogy-5.4-osmem-en` · the three strengths of Context compression `t3-comparison-5.4-compress-en` |
| §5.5 | the five physical forms of Prompt Assets across four dimensions `t1-matrix-5.5-promptasset-en` · the system prompt's six trimming levels `t3-layered-5.5-p0p5-en` |
| §5.6 | how the three layers of the Observation Surface relate `t1-layered-5.6-observation-en` · the essential difference between observation and logging `t2-comparison-5.6-obslog-en` · the five self-evolution paths built on observation `t3-cardgrid-5.6-selfevo-en` |
| §5.7 | the nine event classes of a trajectory `t1-cardgrid-5.7-events-en` |
| §5.8 | what each of the three verifier layers can and cannot do `t1-matrix-5.8-verifier-en` · the four forms of verifier leakage and their defenses `t2-cardgrid-5.8-leakage-en` |
| §5.9 | Safety cuts across the eight runtime mechanisms `t2-layered-5.9-controlplane-en` · the four-layer permission decision model `t1-layered-5.9-permission-en` · the two engineering roads of HITL `t3-comparison-5.9-hitl-en` · OWASP LLM Top 10 v2025: the four that cut the control plane `t2-cardgrid-5.9-owasp-en` · the four anti-pattern classes of the Safety control plane `t3-cardgrid-5.9-pitfalls-en` |
| §5.10 | the Step 0→7 five-phase flow of one agent turn `t1-flow-5.10-turn-en` |
| §5.11 | 17 steps end to end `t1-timeline-5.11-17turn-en` · git push: Safety's four layers, crossed one by one `t1-sequence-5.11-turn16-en` |
| §VI | the six cross-mechanism reusable engineering patterns `t1-cardgrid-6-patterns-en` · the three isolation modes for sub-agent execution `t2-comparison-6-isolation-en` · the progressive adoption order of the six engineering patterns `t3-timeline-6-pattern-order-en` |
| §VII | the Harness Lab five-layer framework `t1-layered-7-harnesslab-en` · five classes of industry workbench compared `t2-matrix-7-workbench-en` · three-phase ablation `t3-flow-7-ablation-en` |
| §VIII | the three composability axes `t1-cardgrid-8-axes-en` · the five-dimension ontology of a sub-harness cell `t2-cardgrid-8-subharness-en` · Lego and the shipping container `t3-comparison-8-lego-en` · the ten relational edges of the Evidence Graph `t3-cardgrid-8-evidence-en` |
| §IX | the thermostat analogy `t1-analogy-9-thermostat-en` · the four cybernetic principles `t2-cardgrid-9-principles-en` |
| §X | three kinds of reader, three learning paths `t1-comparison-10-readers-en` |

## What the tutorial is for

Most agent tutorials are about how to put together an agent that runs: pick a framework, write a prompt, add tools, run a demo. That layer is well covered online. But push an agent into a real B2B application and you find: **getting it running isn't hard; keeping it stable is.**

An agent that sails through a demo starts going wrong once it runs over and over on contract review, business-process approval, or office tasks: the same prompt gives different results at different times; running it five times and averaging looks fine, but the user just feels it's right only now and then; you hand it a document to consult and it fabricates details out of thin air and says "done"; you change how a single tool call is written and the whole main line stops converging.

Most of these problems **aren't a poorly written prompt**; they come from a poorly designed layer outside the agent. In the English literature that layer is called the harness: the layer of software wrapped around the model that handles context, tools, execution, permissions, and the audit trail. This book keeps that name. A harness is not LangChain, LangGraph, or some SDK; those are agent frameworks for development. The harness is the whole structure you build on top of a framework for a particular task: how the model is connected, how tools are managed, how context accumulates, how the trajectory is recorded, what verification rests on, what safety rests on, and how failures are backstopped.

## Six questions you should be able to answer after the Introductory Volume

If you can answer the six questions below, you have finished the Introductory Volume. Each question comes with a short answer and the chapters that cover it.

1. **My agent is unstable. Is the prompt poorly written? And how does the harness relate to prompt engineering, the agent runtime, and a workflow?** Most likely the prompt isn't the problem. The prompt is only one component of the harness; tune it as far as it goes and the gains plateau. §II, §III, and §IV take up these relationships in turn.
2. **Is ReAct still in use? Should I move to Plan-Execute?** It depends on the setting. This book distills ReAct's original design into eight assumptions (the distillation is the book's own; the paper itself gives no such list). Four of them no longer hold, but that doesn't make ReAct obsolete as a whole. For which loop fits which setting, see the decision tree in §5.1 Inner Loop.
3. **I run N times and average the pass rate. Is that statistic trustworthy? And if the evaluation scores are high, why are there still so many problems after launch?** These are two different problems (both covered in §7.4 Ablate):
   - **Non-Independent Reruns (AP01, see Appendix F)**: N reruns are not N independent samples if they share a response cache, a fixed random seed, or the same files, memory, or workspace. The same holds if cache hits at temperature 0 make them reproduce one output verbatim. An apparent 80% pass rate may then be one result counted several times over. Prefix caching in the model service only reuses the computation for the input prefix. A hit or a miss does not change the output, so it is not the source of this problem.
   - **Overfitting to a Fixed Test Set (AP20, see Appendix F)**: you tune prompts and rules against the same test set again and again. The evaluation score keeps rising, and then problems appear as soon as the live inputs change. Keep the test set used for development separate from a held-out set, and feed live failures back in as new test cases.
4. **My verifier keeps passing outputs that look right but are wrong. What do I do?** There are three typical defects: answer leakage, reward hacking, and Artifact Claim Mismatch, and each has its own remedy. §5.8 answers this, and the closing passage of §5.9 adds to it.
5. **How do I optimize the harness systematically instead of tuning by feel?** Follow five steps: Observe → Score → Ablate → Tune → Iterate. This is an outer loop independent of the business loop. The volume calls it the Harness Lab, the book's name for the outer workbench that improves a harness iteratively through evaluation, ablation, and tuning. See §VII.
6. **Is this book for me, and which chapter should I start from?** See "Who should read what" below and §X Learning paths.

**The next goal** (the chapter-by-chapter and module-by-module expansion volumes to follow): the reader can independently design and tune an agent harness, and not just answer these six questions.

## Who should read what

The Introductory Volume doesn't require reading cover to cover. Three kinds of reader each have a recommended path (the detailed paths are in [§X Learning paths](./10-learning-path.md)):

**AI PMs and AI business roles**: you make technology choices, evaluate outside agent vendors, or set the harness direction for a team. Recommended path: §I → §5.3 Tool Registry → §5.5 Prompt Assets → the anti-patterns subsection of §VII Harness Lab (7.8) → §VIII composability matrix.

**Learners** (studying agent engineering, doing research, preparing to enter the field): you want a mental model that can converse with any agent paper or tutorial. Recommended path: §I, §II → §5.1 Agent Loop → §5.8 Verifier → §IX Four cybernetic principles.

**For an AI to read**: an AI agent reads this volume itself to make downstream decisions. Recommended path: in the order of the contents (file names 01 → 99). Don't skip the passages that describe the mechanisms. They are the main body of the text; skip them and only the names are left.

## What may be skipped

- **Chapters on the more mature mechanisms** (§5.2 Model Adapter, §5.7 Trajectory) carry less methodology and may be skimmed.
- **Don't skip the key chapters**: §5.1 Agent Loop, §5.4 Context-Memory-Artifact, §5.5 Prompt Assets, §5.6 Observation Surface, §5.8 Verifier, §VII Harness Lab, §VIII composability matrix, and §IX Four cybernetic principles. These eight chapters are the main support for the volume's argument.
- **§5.6 covers the two roles of the observation surface**: it is not only runtime feedback to the model; it is also the input-side infrastructure for cross-run self-evolution.
