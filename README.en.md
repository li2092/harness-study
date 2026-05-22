# Harness Study · The Engineering Practice for AI Agents

> 中文版（主版本）: [README.md](README.md)

> Current status: **the introductory volume is under review.** The manuscript is complete and undergoing final review; it will be pushed to [`intro/`](intro/) once review is finished. This README sets out the purpose, audience, structure, and acceptance criteria of the volume.

---

## 1. What This Volume Addresses

Most existing material on agents stops at how to build one that runs — pick a framework, write a prompt, add a few tools, run a demo. That layer is well covered on the public internet.

What appears once an agent is actually deployed to office work, contract review, or business process automation is a different class of problem: the same prompt produces different outputs at different times; the headline pass rate looks high but users report inconsistent behaviour in practice; given a document to consult, the agent fabricates details that are not in it and then declares the task complete; a change to a single tool-call convention — leaving the model untouched — causes the entire main loop to stop converging.

In most of these cases, the cause is not in the prompt. Past a certain point, further investment in prompt iteration yields rapidly diminishing returns. What actually determines whether an agent is stable is the layer around the model — in English, the **harness**. A harness is not LangChain or any particular SDK — those are frameworks. The harness is the structure you build on top of a framework for a particular task: how the model is mounted, how tools are managed, how context accumulates, where artifacts land, how things are verified, how safety is enforced, what happens when something fails.

This volume — the introductory one — extracts that layer around the model and treats it as an engineering object in its own right, going through what it is composed of, why each part must be there, how to choose, and how to recognise when you have chosen wrongly.

## 2. What the Introductory Volume Delivers

The volume decomposes an agent harness into **eight runtime mechanisms + one cross-cutting control plane + engineering patterns + a workbench + a composability matrix + four principles from control theory**, and walks through this skeleton in full. Each item is given a complete three-tier mental model: What / Why / How to start.

By the end, the reader should have a complete mental model of an agent harness, and be able to locate any agent engineering problem to a specific component and a specific anti-pattern.

Further volumes — **per-chapter / per-module expansions** — are planned. Each runtime component, each engineering pattern, and each layer of the workbench will get its own deeper volume, covering finer engineering discipline, real-world cases, and deployment pitfalls. After those, the reader should be able to design and tune an agent harness independently.

There is a further objective: **any AI coding assistant that reads this volume should be able to take a user's specific requirement or scenario and produce a deployable agent of reasonably high accuracy**. The volume is written on the assumption that some of its readers are AI themselves; for those readers, the downstream action is not to *understand the concepts*, but to *construct a usable engineering artifact* on behalf of the user.

## 3. Six Questions Answerable After Reading

1. **My agent is unstable — is it because the prompt is poorly written?** Most likely not. The prompt is one piece of the harness; tuning it past a certain point yields diminishing returns.
2. **Is ReAct still relevant? Should I move to plan-execute?** It depends on the setting. Four of ReAct's eight original assumptions no longer hold, but invalidation of assumptions does not mean ReAct is wholesale obsolete.
3. **I run N trials and take the average pass rate — is the statistic trustworthy?** Not necessarily. Prefix KV caches (as in DeepSeek-class models) can make those N trials non-independent — an apparent 80% pass rate may in fact be the same cached path replayed N times. This is what is called *cache collusion*.
4. **My verifier keeps passing outputs that look correct but are actually wrong — what do I do?** Three typical pathologies: answer leakage (the verifier has seen the ground truth), reward hacking (the model has learned to game the verifier), and artifact-claim mismatch (the agent claims to have done something the artifacts do not corroborate). Each calls for a different remedy.
5. **How do I systematically optimise the harness rather than tune by feel?** Observe trajectories, Score them, Ablate mechanisms, Tune parameters, Iterate. This is an outer loop independent of the business loop; the volume calls it the **Harness Lab**.
6. **Which part of this is for me?** See *Who Should Read What* below.

## 4. Who Should Read What

The introductory volume does not require linear reading. Three reader types have recommended paths.

**AI PMs / AI business roles** — for those evaluating vendors, selecting frameworks, setting the harness direction for a team. The most useful question for you is: *what are the parts, what fits which setting, what are the common errors?* Path:

§I Why harness (build mental model in five minutes) → §5.3 Tool Registry & ACI (tools are the crucial part of B2B agent deployment) → §5.5 Prompt Assets (how the instruction layer is managed) → §VII Harness Lab anti-patterns (cache collusion / leakage / reward hacking) → §VIII Composability Matrix (see clearly which combination you are actually putting together).

**Learners** — students of agent engineering, researchers, those preparing to enter the field. The point is to build a mental model that converses with any agent paper or tutorial — to understand why the line from ReAct to Reflexion to plan-execute has evolved the way it has. Path:

§I-§II (naming and history) → §5.1 Agent Loop (evolution of reasoning paradigms) → §5.8 Verifier (the hardest piece of agent engineering) → §IX Four Principles of Control Theory (where the volume's thesis comes together).

**For AI to read** — an agent reading this volume itself, in order to make downstream decisions (for example, an agent tuning its own harness configuration after reading). Path:

Follow the `depends_on` chain in each chapter's frontmatter. The entry hook and cognitive-node definitions in each chapter are sufficient for modelling. Do not skip the mechanism-description sections — that is the prose body; skipping leaves only the names behind.

## 5. Structure

| Section | Subject |
|---|---|
| §I | Why harness — why the layer around the model must be extracted |
| §II | Naming and history — from prompt to harness engineering |
| §III | Three layers of span |
| §IV | Key tensions |
| §V | Eight runtime mechanisms + Safety control plane + end-to-end examples |
| §5.1 | Agent Loop |
| §5.2 | Model Adapter & Routing |
| §5.3 | Tool Registry & ACI |
| §5.4 | Context / Memory / Artifact |
| §5.5 | Prompt Assets |
| §5.6 | Observation Surface |
| §5.7 | Trajectory |
| §5.8 | Verifier |
| §5.9 | Safety |
| §5.10 | Micro-flows |
| §5.11 | End-to-end 17 turns |
| §VI | Engineering patterns |
| §VII | Harness Lab — the outer optimisation loop |
| §VIII | Composability matrix |
| §IX | Four principles of control theory |
| §X | Learning paths |
| Appendix | K1-K7 / primary sources / EG10 / OWASP / naming map / SPIFFE-biscuit / AP01-AP19 / arxiv index |

The volume runs to roughly 250,000 Chinese characters, prose-dominant. That scale is set by the introductory positioning — *walk the full skeleton once, give a complete mental model*; later expansion volumes will be more focused and more detailed.

## 6. What May Be Skipped

- **The appendix is reference material, not required reading** — consult on demand.
- **Continuity sections** (§5.2 Model Adapter / §5.7 Trajectory) cover comparatively mature components and have lower methodological density than the main chapters; may be skimmed.
- **The main chapters should not be skipped**: §5.1 Agent Loop / §5.4 Context-Memory-Artifact / §5.5 Prompt Assets / §5.6 Observation Surface / §5.8 Verifier / §VII Harness Lab / §VIII Composability Matrix / §IX Control Theory. These eight chapters carry the volume's thesis.

## 7. Relation to the Workbench Project

The tutorial side — this repository — defines the object of study and the method. The engineering implementation side is carried by an independent project, [Harness · Lab](https://github.com/li2092/Harness-Lab), which puts this method onto a workbench specification. The two projects share the same vocabulary, the same node definitions, the same signal conventions.

Order of use:

- First-time readers of this tutorial: the workbench is not needed; start directly from `intro/01-introduction.md`.
- After finishing the introductory volume, when deploying an actual harness: use the workbench specification as the visual language of the evidence graph.

## 8. Acceptance Criteria

**Introductory volume completion** = the reader can answer the six questions above after reading.

**Next-tier completion** (per-chapter / per-module expansion volumes): the reader can independently design and tune an agent harness — not merely answer the six questions.

## 9. License

[Apache License 2.0](LICENSE) © 2026 Jinming Li

## 10. Contact

- Issues and Discussions welcome.
- Email: li2092@qq.com
- GitHub: [@li2092](https://github.com/li2092)
