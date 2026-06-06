# Harness Study · The Engineering Practice for AI Agents · The Introductory Volume

> **What this volume is**: the introductory / entry-level explainer of the project, answering "what an agent harness is and which parts make it up." Its main axis is a platform-independent engineering-practice methodology, with concrete engineering cases used only as seasoning.
>
> **Where it sits in the whole of Harness Study**: this is the opening introductory volume — it **walks the full skeleton once** (8 runtime mechanisms + the Safety control plane + engineering patterns + the Harness Lab + the composability matrix + the four control-theory principles), giving each part a complete three-tier mental model: What / Why / How to start. **Per-chapter and per-module expansion volumes will follow** — each runtime part, each engineering pattern, each of the five Harness Lab layers will get its own deep volume, covering finer engineering discipline, industry cases, and landing pitfalls.

## Contents

This volume is split by chapter, one file per chapter; Chapter Five (the essential mechanisms) has one file per detail. Read in the order of the table below (file names 01 → 99).

| Section | File | Subject |
|---|---|---|
| §I | [01-why-harness.md](./01-why-harness.md) | What problem we are actually solving |
| §II | [02-prehistory.md](./02-prehistory.md) | Prehistory: when models were used as functions (2020–2022) |
| §III | [03-autogpt.md](./03-autogpt.md) | The first large-scale trial and error: the AutoGPT wave and its failure (2023) |
| §IV | [04-harness-emerges.md](./04-harness-emerges.md) | The emergence of the harness concept (mid-2023 – 2026) |
| §V · overview | [05-00-mechanisms-overview.md](./05-00-mechanisms-overview.md) | 8 runtime mechanisms + 1 Safety control plane · the cut, and part vs. implementation |
| §5.1 | [05-01-agent-loop.md](./05-01-agent-loop.md) | Agent Loop · Inner Loop · the agent's thinking structure · **P0** |
| §5.2 | [05-02-model-adapter.md](./05-02-model-adapter.md) | Model Adapter & Routing |
| §5.3 | [05-03-tool-registry.md](./05-03-tool-registry.md) | Tool Registry & ACI · **P0** |
| §5.4 | [05-04-context-memory-artifact.md](./05-04-context-memory-artifact.md) | Context / Memory / Artifact |
| §5.5 | [05-05-prompt-assets.md](./05-05-prompt-assets.md) | Prompt Assets · Instruction Layer · **P0** |
| §5.6 | [05-06-observation-surface.md](./05-06-observation-surface.md) | Observation Surface · the three-layer placement |
| §5.7 | [05-07-trajectory.md](./05-07-trajectory.md) | Trajectory · Event Stream · **P0** |
| §5.8 | [05-08-verifier.md](./05-08-verifier.md) | Verifier · three layers · **P0** |
| §5.9 | [05-09-safety.md](./05-09-safety.md) | Safety control plane · cross-cutting |
| §5.10 | [05-10-turn-walkthrough.md](./05-10-turn-walkthrough.md) | The micro-flow of a single turn |
| §5.11 | [05-11-end-to-end.md](./05-11-end-to-end.md) | A mid-size end-to-end example · 17 turns fixing a logging bug |
| §VI | [06-engineering-patterns.md](./06-engineering-patterns.md) | Engineering patterns · cross-part reusable engineering combinations |
| §VII | [07-harness-lab.md](./07-harness-lab.md) | Harness Lab · Outer Loop · systematically optimizing the harness itself |
| §VIII | [08-composability.md](./08-composability.md) | Composability matrix · encapsulation × topology × interaction boundary |
| §IX | [09-cybernetics.md](./09-cybernetics.md) | The four principles of control theory · the meta-rules that bind the whole tutorial |
| §X | [10-learning-path.md](./10-learning-path.md) | Learning paths · how three kinds of reader should use this tutorial |
| Companion · Prompt | [11-harness-prompt.md](./11-harness-prompt.md) | Harness Prompt · the executable landing spec for an agent (Phase 0–3 + a gate per step) |
| Companion · Prompt lite | [12-harness-prompt-lite.md](./12-harness-prompt-lite.md) | Harness Prompt · the generic TDD lite version (three instructions to feed a coding AI directly) |
| Appendix | [99-appendix.md](./99-appendix.md) | The 8-part quick-reference table + a roundup of primary sources |

> The deep volume on §5.1 is in the expansion volumes to follow (in planning). **The executable companion parts are already in this directory**: the landing spec → [`11-harness-prompt.md`](./11-harness-prompt.md); the TDD lite version → [`12-harness-prompt-lite.md`](./12-harness-prompt-lite.md); the quick-reference appendix → [`99-appendix.md`](./99-appendix.md).

## Figure index

The volume has 50 figures in all, in one unified jimi-ink visual style, with source files in the sibling [`../diagrams/`](../diagrams/). Each figure is embedded in the body of its chapter; the table below indexes them by chapter.

| Section | Figures |
|---|---|
| §I | the gap · opposition bridge `t1-comparison-1-gap-en` · the vibe-to-agentic spectrum `t2-comparison-1-spectrum-en` |
| §II | the limits of prompt-only `t1-comparison-2-prompt-en` |
| §III | the AutoGPT mechanism matrix `t1-matrix-3-autogpt-en` · the intern analogy 8+1 `t2-analogy-3-intern-en` |
| §IV | the harness naming timeline `t1-timeline-4-naming-en` · each algorithm generation's constraint layer `t2-matrix-4-generations-en` · the horse-gear metaphor `t2-analogy-4-bridle-en` |
| §V · overview | the eight mechanisms at a glance `sample-05-mechanisms-overview-en` · the abstraction levels `t1-layered-5.0-abstraction-en` |
| §5.1 | the ReAct evolution matrix `t1-matrix-5.1-react8-en` · the four-question design decision tree `t1-tree-5.1-choose-en` · fifteen converge to five `t2-cardgrid-5.1-five-en` · multi-agent cost 15x `t3-cardgrid-5.1-multiagent-en` |
| §5.2 | model routing `t1-cardgrid-5.2-routing-en` |
| §5.3 | the tool-call flow `t1-flow-5.3-toolcall-en` · the four tool-batching patterns `t3-cardgrid-5.3-toolbatch-en` |
| §5.4 | the three-layer state comparison `t1-comparison-5.4-state-en` · the five memory questions `t2-tree-5.4-memory-en` · the OS memory hierarchy `t2-analogy-5.4-osmem-en` · three compression strengths `t3-comparison-5.4-compress-en` |
| §5.5 | the prompt-asset matrix `t1-matrix-5.5-promptasset-en` · the P0-P5 pyramid `t3-layered-5.5-p0p5-en` |
| §5.6 | observation layering `t1-layered-5.6-observation-en` · observation vs logging `t2-comparison-5.6-obslog-en` · the five self-evolution paths `t3-cardgrid-5.6-selfevo-en` |
| §5.7 | the trajectory event types `t1-cardgrid-5.7-events-en` |
| §5.8 | the verifier matrix `t1-matrix-5.8-verifier-en` · the four classes of leakage defense `t2-cardgrid-5.8-leakage-en` |
| §5.9 | the Safety cross-cut `t2-layered-5.9-controlplane-en` · permission layering `t1-layered-5.9-permission-en` · the two HITL roads `t3-comparison-5.9-hitl-en` · the four OWASP risks that cut the plane `t2-cardgrid-5.9-owasp-en` · the four pitfall classes `t3-cardgrid-5.9-pitfalls-en` |
| §5.10 | the single-turn flow `t1-flow-5.10-turn-en` |
| §5.11 | the 17-turn timeline `t1-timeline-5.11-17turn-en` · the Turn 16 sequence `t1-sequence-5.11-turn16-en` |
| §VI | the engineering-pattern cards `t1-cardgrid-6-patterns-en` · the three isolation tiers `t2-comparison-6-isolation-en` · the six-pattern progression `t3-timeline-6-pattern-order-en` |
| §VII | the Harness Lab layering `t1-layered-7-harnesslab-en` · the workbench five-layer coverage `t2-matrix-7-workbench-en` · the three-phase ablation `t3-flow-7-ablation-en` |
| §VIII | the composability dimensions `t1-cardgrid-8-axes-en` · the sub-harness five dimensions `t2-cardgrid-8-subharness-en` · Lego plus shipping container `t3-comparison-8-lego-en` · the Evidence Graph ten edges `t3-cardgrid-8-evidence-en` |
| §IX | the thermostat analogy `t1-analogy-9-thermostat-en` · the four control-theory principles `t2-cardgrid-9-principles-en` |
| §X | the three reader paths `t1-comparison-10-readers-en` |

## What the tutorial is for

Most agent tutorials are about how to put together an agent that runs — pick a framework, write a prompt, add tools, run a demo. That layer is well covered online. But push an agent into a real B2B application and you find: **getting it running isn't hard; keeping it stable is.**

An agent that sails through a demo starts going wrong once it runs over and over on contract review, business-process approval, or office tasks: the same prompt gives different results at different times; running it five times and averaging looks fine, but the user just feels it's right only now and then; you hand it a document to consult and it fabricates details out of thin air and says "done"; you change how a single tool call is written and the whole main line stops converging.

Most of these problems **aren't a poorly written prompt** — they're a poorly designed layer of framework around the model. In the English literature that layer is called the harness. A harness is not LangChain / LangGraph / some SDK — those are frameworks. The harness is the whole structure you build on top of a framework for a particular task: how the model is mounted, how tools are managed, how context accumulates, how the trajectory is traced, what verification rests on, what safety rests on, how failures are backstopped.

## Six questions you should be able to answer after the introductory volume

1. **My agent is unstable — is the prompt poorly written?** Most likely not. The prompt is one part of the harness; tuning it past a point yields diminishing returns.
2. **Is ReAct still in use? Should I move to plan-execute?** It depends on the setting. Four of ReAct's eight original assumptions no longer hold, but invalidation doesn't mean ReAct is wholesale obsolete.
3. **I run N times and average the pass rate — is the statistic trustworthy?** Not necessarily. A prefix KV cache (as in DeepSeek-class models) can make the N runs non-independent — an apparent 80% pass rate may in fact be the same cached path replayed N times. This is called cache collusion.
4. **My verifier keeps passing outputs that look right but are wrong — what do I do?** Three typical pathologies: answer leakage, reward hacking, and artifact-claim mismatch. Each has a different remedy.
5. **How do I systematically optimize the harness instead of tuning by feel?** Observe → Score → Ablate → Tune → Iterate. This is an outer loop independent of the business loop; the volume calls it the Harness Lab.
6. **Which part of this is for me to read?** See "Who should read what" below.

## Who should read what

The introductory volume doesn't require reading cover to cover. Three kinds of reader each have a recommended path (the detailed paths are in [§X Learning paths](./10-learning-path.md)):

**AI PMs / AI business roles** — you select vendors, evaluate outside agent suppliers, set the harness direction for a team. Recommended path: §I → §5.3 Tool Registry → §5.5 Prompt Assets → the three common pitfalls of §VII Harness Lab → §VIII composability matrix.

**Learners** (studying agent engineering, doing research, preparing to enter the field) — you want a mental model that can converse with any agent paper or tutorial. Recommended path: §I–§II → §5.1 Agent Loop → §5.8 Verifier → §IX the four control-theory principles.

**For an AI to read** — an AI agent reading this volume to make downstream decisions. Recommended path: in the order of the contents (file names 01 → 99). Don't skip the mechanism-description passages — that is the prose body; skip it and only the names are left.

## What may be skipped

- **Continuity chapters** (§5.2 Model Adapter / §5.7 Trajectory) cover comparatively mature parts with lower methodological density and may be skimmed.
- **Don't skip the main chapters**: §5.1 Agent Loop / §5.4 Context-Memory-Artifact / §5.5 Prompt Assets / §5.6 Observation Surface / §5.8 Verifier / §VII Harness Lab / §VIII composability matrix / §IX control theory. These eight chapters are the load-bearing walls of the volume's thesis.
- **§5.6 upgrades a three-layer framing** — the observation surface isn't only a runtime-feedback part; it is the input-side infrastructure layer for cross-run self-evolution.

## Acceptance criterion · the Verify six

The acceptance criterion for the introductory volume = the reader can answer the six questions above after reading:

1. **How do the harness, prompt engineering, the agent runtime, and a workflow relate?** Answered jointly by §II + §III + §IV.
2. **Is ReAct still in use? Which to use in which setting?** The §5.1 Inner Loop decision tree.
3. **Why is verifier design so hard (Leakage + Reward Hacking + Artifact-Claim Mismatch)?** Answered jointly by §5.8 + the closing passage of §5.9.
4. **Why might the statistics of N reruns be fake (cache collusion)?** The §7.4 Ablate cache-collusion passage.
5. **How is the harness systematically tuned (Observe → Score → Ablate → Tune → Iterate)?** Answered jointly by the five layers of §VII Harness Lab.
6. **Is this book for me, and which chapter do I start from?** Answered jointly by §X Learning paths + the §I signposts.

**The next-tier acceptance criterion** (the per-chapter / per-module expansion volumes to follow): the reader can independently design and tune an agent harness, not merely answer the six questions.
