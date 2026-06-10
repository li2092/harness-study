# Harness Prompt · The executable landing spec for an agent

This file is the **executable companion** to the main text, *Harness Study*. The main text covers "what the parts are and why they are designed this way"; this file covers "what order to build them in, and how to verify each step is right."

**How to use it**: hand this file, together with your concrete scenario ("build me an agent for scenario X"), to a coding agent. The agent works through Phase 0 → 1 → 2 → 3 in order, and **the completion gate at the end of each Phase must pass before the next Phase begins**. A gate is "how you verify the step was done right," not "what was done" — with no verifiable evidence, treat the step as unfinished.

**Global conventions**:

- Every concrete number in this file (token-usage thresholds, single-tool output caps, tool counts) is a **starting default**, to be tuned against your scenario, not a universal constant.
- Each Phase marks its corresponding main-text chapter (`↪`); drill down there when you need the underlying reasoning.
- Build on a **strong model**. A weak model cannot carry multi-turn tool calling and will fail the Phase 1 gate over and over.
- Wherever possible, give each Phase's completion gate a **runnable check** — a script, an assertion, a comparison that executes — not just a written description. The one executing this spec is an agent, and written criteria are exactly what an agent finds easiest to "declare satisfied" (the incubator of artifact-claim mismatch); a gate that runs leaves no room to fudge. Example: the Phase 1 gate should at minimum include a hard check like "one full ReAct loop completed on a fake provider + a tool_call/tool_result pairing assertion."
- This spec runs the **middle-coverage tier**: a generic runtime + scenario narrowing + cost structure (the three parts distilled from practice) + the Model Probe + the four-principle self-check + the mechanism admission gate. The two advanced topics — the Harness Lab five layers and the composability three axes — get only their judgment lines here, not a full treatment; go back to the main text when you need them.

---

## Phase 0 · Model Probe · take the model's pulse before you build

**Goal**: before building the runtime, run a diagnostic against the exact LLM endpoint you will use, and produce a profile — which mechanisms this model needs, which it does not, and which are traps for it. The value is not "understanding the model"; it is **cutting down the space of mechanisms you will later have to try**, and **flagging negative-contribution traps in advance**.

**Method core · the three-part probe**: every probe is a triple —

1. **Stimulus**: a minimal task designed to expose one behavior (not hard, just enough to force the behavior out).
2. **Behavior classification**: judge *how* it did it, not *whether* it was right. Prefer programmatic judgment (did it crash, did it translate, how many times did it read — all binary or countable), and use a model-as-judge only on fuzzy dimensions.
3. **Mechanism implication**: given the behavior class, output **one configuration decision plus one prediction that later ablation can falsify**. A probe ends in a configuration decision and a testable prediction, never in a score.

**Four probe families** (graded hard to soft by the consequence of an error, run A through D):

- **Family A · protocol layer**: an error crashes the harness, not degrades it. Highest priority, binary hard judgment. Typical — feed a complex strict-schema tool with nested objects and arrays, and watch whether the model fails at the request layer or registers and calls it cleanly. Outright failure → a schema-normalization layer is mandatory.
- **Family B · tool-use layer**: degrades, does not crash. Typical — give a tool-first multi-file task and count how many times it reads before acting. Reading over and over without acting → add a read-complete / evidence-sufficiency guard.
- **Family C · instruction-following layer**: typical — put an English heading in the task and see whether the model translates it into Chinese in a Chinese context. If it translates → the verifier cannot match a fixed English string; turn on multi-alias matching.
- **Family D · self-healing and calibration layer**: the deepest and most differentiating. Typical — give an operation that will error, and see whether the model retries blindly or reads the error message and changes approach.

**✅ Completion gate**:

- [ ] Each of families A/B/C/D ran a few probes, and every probe landed in one behavior class (keep the raw observation for the programmatic ones: crashed / translated / read N times).
- [ ] Every probe produced both a configuration decision and a falsifiable prediction, not just a score.
- [ ] You have a profile table: which mechanisms this model **must** turn on, which it **does not need**, which are **traps**. This table directly narrows the mechanism set for Phases 1–3.

**Note**: the Model Probe gives only **qualitative priors**, not quantitative conclusions. "Turning on X recovers some of the dropped tool calls" — how much "some" is waits for Phase 3 ablation to answer with clean data. What you can read off at a glance is a binary fact — did it crash, did it translate — and that does not depend on a precise cross-config comparison.

`↪ Main text: Model Probe · the first of the Harness Lab's three steps`

---

## Phase 1 · A generic agent runtime · no language binding, no scenario binding

**Goal**: build a generic runtime that can run a ReAct loop against any tool set. This step touches no concrete business; it just gets the frame running.

### 1.1 Module split · five modules

Three core modules plus two supporting:

- **engine**: runs the loop. The main loop is one ReAct — send the message → receive the reply → execute any tool call → write the result back → decide whether to stop. Add a state machine for multi-turn: awaiting user input / awaiting user confirmation / done / errored. Check the cancellation signal at the top of every turn; stop must take effect immediately.
- **llm**: the multi-provider abstraction. Abstract one unified interface and handle each vendor's differences in an adapter layer. `thinking` / reasoning parameters are written differently by each vendor, so configure them through an `extra` field. **Domestic APIs must explicitly bypass the proxy**, with a dedicated `no_proxy` — setting only the uppercase variable will not stop the lowercase one.
- **tools**: handles registration and execution. Reload the tool list every step — **do not cache it** — because a tool registered in a POST hook has to be visible on the next turn.
- **storage**: stores sessions and checkpoints.
- **types**: the central place for message and tool signatures.

`↪ Main text: Agent Loop (§5.1, P0) / Model Adapter & Routing (§5.2, the P0 boundary)`

### 1.2 Three protocols / runtime red lines

- **The assistant-message protocol**: a `tool_result` must follow **immediately** after `tool_calls`, with nothing inserted between them, or the next request returns a 400 outright.
- **strict-schema normalization** (if the Family A probes in Phase 0 show the model is sensitive to strict schemas): normalize the schema before registering a tool, and handle nested objects / arrays until the model accepts them.
- **The cancellation signal**: check it at the top of every turn; release the lock the instant you take the engine out, run async and listen for cancellation, and guarantee the engine is returned on all three paths — success, cancellation, error. Do not wait synchronously on a long task while holding the lock.

`↪ Main text: Model Adapter & Routing (§5.2)`

### 1.3 The tool layer

The tool layer is not only "register and execute" — **tool-call quality** (does the model actually call, call correctly, get a clean result written back, and self-repair on failure) is decided by the groups below together.

**Interface and guards**

- Define the Tool abstraction by the main text's five fields (`name` / `description` / `input_schema` / `execute` / `policy`, where policy is the ToolPolicy: allowed_paths / timeout / requires_confirmation, and so on). On every tool_call the Registry does three things: schema validation → policy decision (allow / ask / deny) → execute + audit into the trajectory.
- Give every single tool output a **hard cap** (starting defaults: file read 20k / search 10k / shell 15k); over the cap, go through "result roll-up" below.
- Route shell and git commands through `execFile` + array arguments; **reject string concatenation**, to prevent injection.

**Scheduling · the four Tool Batch modes** (whether a batch should run concurrently, serially, or stop)

- **parallel_read**: read-only, no side effects, no path conflicts → concurrent by default (read_file / grep / glob / list_dir / web_search / web_fetch).
- **sequential_write**: writing files / changing the workspace / changing state → serial by default (write_file / edit_file / shell_exec / git_* and anything marked DANGEROUS).
- **barrier**: permission confirmation / a dangerous operation / a batch switch / a decision that must be reconsidered against the previous batch's observation → stop explicitly and decide where to switch.
- **background_sidecar**: hand off to a lightweight side agent, independent of the main line.
- **Main-line discipline**: a single agent executes a batch of tools → rolls the results up and writes them back → spins up a sidecar only when needed. Do not reach for a sub-agent up front (the three costs — the safety boundary, context isolation, result aggregation — are more than most tasks can bear).

**Result roll-up · tool results never enter the main conversation as raw text**

- After a batch executes, it produces two kinds of artifact: the raw text lands in the **ArtifactStore** (returning a ref) plus an **observation stub** (a trimmed summary, starting default around 200 characters, which enters context). The main thread consumes only the stub; for the raw text, the model itself sends `read_observation(obs_id)` / `read_artifact` to fetch on demand. The rule: **extract in full, inject on demand, never truncate, never skip pages**.
- The stub must carry the metadata `truncated:true / size / preview_truncated_at` — to sidestep two opposite failure modes: **overload** (everything stuffed into context, triggering lost-in-the-middle, paying tokens without getting attention) and **distortion** (a crude truncate drops information and the agent does not know it was cut). **The body must be in addressable persistent storage**; truncating without storing the body is still distortion.
- The three lines of prompt that go with it: ① when the feedback is large, look only at the stub, and use `read_observation` to fetch the full content; ② when the stub carries a `truncated` marker, check `size` to decide whether to fetch the full text; ③ a `PreprocessError` is a modal-processing failure, not a tool-call failure, and can be retried or routed around.

**Error returns · they decide whether the agent can self-repair**

- **actionable**: say "what went wrong and how to fix it," not a raw stack trace. Example: `file_path 'data/output.txt' does not exist — did you mean 'data/input.txt'? list data/ first` — far better than throwing a raw `FileNotFoundError`. It is one key piece of the ACI design that pushes the tool-call success rate from 60–70% to 95%+ (the number is the whole Tool Registry + ACI working together, not this one piece alone).
- **raw vs sanitized, split by the tool's origin**: tools whose `execute` is fully under your control, implemented in internal code → raw error (with details, easy to self-repair); tools that reach an external data source, whose `execute` result contains external content → sanitized error (strip the stack trace / internal paths / sensitive fields). You can also split by environment: raw in development, sanitized in production. **The error return is one of the most common injection points for prompt injection.**

**Recommended default: web_search + web_fetch**

- The model's weights are frozen and its knowledge has a cutoff; facts after the cutoff (a new version number, a just-changed API, the current docs) can only be guessed at, and a bad guess is a hallucination — these two tools wire "the world after training" back in for live lookup and checking, often raising quality more than another round of prompt tuning would.
- Two disciplines that go with them: ① a large return (dozens of results at once, or one article of tens of thousands of characters) → must go through "result roll-up" above; do not let the raw text flood the main conversation; ② the fetched content is external input → run it through a source-credibility check or hand it to a verifier; do not take a found source as ground truth.

**Diagnosis · a tool that should have been called but wasn't**

When the model should call a tool but emits only a stretch of text, there are three causes, sitting at three layers, with completely different fixes. Rule them out in order — response parsing → request parameters → prompt assembly. That is faster than repeatedly editing the prompt or swapping the model:

1. **The response-parsing layer (false negative)**: the model may have written the call as a text tag in the body (e.g. `<tool_call>…</tool_call>`) instead of into the structured `tool_calls` field, and an Adapter that only reads the structured field drops it as ordinary text. Fix: have the parsing layer also catch text-tag calls with a regex, beyond the structured field.
2. **The request-parameter layer**: the default `tool_choice:auto` makes a call optional. On a turn that must use a tool (must query the database, must write to disk), set `tool_choice` to `required` / `any` or name a specific tool — **per turn and per scenario, not globally on** (a permanent `required` forces the model to call when it shouldn't, manufacturing noise).
3. **The prompt-assembly layer**: an overlong Chinese prompt makes some models "too lazy" to call a tool and answer in text instead. Keep the instruction that triggers a tool call short and near the front, and split the long explanation out.

`↪ Main text: Tool Registry & ACI (§5.3, P0) / ObservationPack · Observation Surface (§5.6) / the Model Adapter three causes (§5.2 last subsection) / Artifact (§5.4, P2)`

### 1.4 Context compression · three strengths

- **micro**: the lightest notch on the compression spectrum — the local roll-up of one large tool result (the stub enters context / the raw lands externally / `read_observation` fetches on demand); the mechanism is the "result roll-up" in 1.3, marked here only for its place among the three strengths.
- **auto**: when the token estimate exceeds the window (starting default 60–70%, commonly 70%) it triggers a small-model summary of the whole history. The summary **must keep four classes** — any open `tool_call_id` and its state / each turn's key decision and reasoning / artifact-reference ids / verifier failure information. Drop any one and the agent will hallucinate afterward (fabricate an observation, fabricate an id, hit the same error again).
- **rolling window**: the crudest fallback — when it runs too long, roll off the oldest turns.
- **After compression you must re-inject the task goal and the system identity**, or after dozens of turns the agent drifts off topic and thinks it is doing something else.

`↪ Main text: Context (§5.4, P0) / Prompt Assets identity re-injection (§5.5, P0)`

### 1.5 Observability · instrument it from the first line

- Instrument at **decision points**, not execution points — where the mechanism judges "should this be done."
- Record all four states: triggered and executed / condition unmet and not executed / triggered but blocked / executed and errored.
- **No event is the most dangerous signal** — it means the code path was never reached.
- Loop detection catches repeated tool calls; queue any intervention message and push it after the `tool_result` is processed, all at once, instead of breaking the message protocol mid-stream.

`↪ Main text: Observation Surface (§5.6) / Trajectory (§5.7, P0)`

### 1.6 The Safety control plane, to start · cross-cutting, not a ninth part

Safety is not another runtime part; it is a control plane cutting across all the parts — every tool call, state change, and artifact write passes through it, like an OS syscall gate, with no exceptions. The full thing is a **four-layer permission decision model**:

- **permission mode**: the agent's overall run mode (read-only / workspace-write / and a few other tiers).
- **allow-deny-ask rules**: fine-grained rules by tool and by parameter pattern, running **default deny + explicit allow** (allow `git status` / deny `git push` / ask on `git commit`).
- **Hooks**: user scripts run before and after a call, for decisions the rules cannot express. Run on **normalized intent, not the raw string** — otherwise a deny on `cargo check` gets bypassed by an alias like `cargo c`.
- **sandbox**: the physical isolation layer (Seatbelt / bubblewrap / container), bounding the file read-write range and network egress. When the first three logical layers are bypassed, it is the last line of defense.

To start, land at least these two:

- **Critical safety goes through code, not the LLM** (a hard gate): the interception for dangerous operations (deleting files, pushing code, making network requests, spending money) is written at the code layer, not left to the model's discretion via a prompt. The LLM assists only at the soft gate (judging benign vs harmful) and is never the last line of defense.
- **A HITL approval gate**: high-impact operations (deleting data / transferring money / deploying / sending email) are marked `requires_confirmation`, and the agent sends them for human confirmation before executing rather than deciding on its own. The approval mode propagates down the parent-child agent chain (a sub-agent inherits the parent by default, never looser).

`↪ Main text: the Safety control plane · the four-layer permission decision model + HITL (§5.9, cross-cutting)`

### 1.7 The verifier, to start · the hard gate only

Start with the cheapest of the three verifier layers — the **hard gate**: a programmatic PASS/FAIL (pytest passes / build succeeds / file hash matches). The outcome judge and the PRM come in Phase 2.

`↪ Main text: the three-layer verifier (§5.8, P0)`

### 1.8 Frontend integration (if any)

The backend is the **single source of truth**; do not keep a frontend state snapshot. On a session switch, pull `last_messages` and `is_running` from the backend.

**✅ Phase 1 completion gate**:

- [ ] The runtime can start a ReAct loop against **any tool set** and run at least one task to completion.
- [ ] The trajectory has a complete event stream, instrumented at decision points and covering the four states.
- [ ] A dangerous command (delete / push / spend money) is stopped at the **code layer** — write a task that triggers one and verify the interception actually fires, not a prompt that says "don't delete."
- [ ] A high-impact operation (deleting data / transferring money / deploying) triggers HITL, and the agent really stops to wait for human confirmation before the call.
- [ ] The hard gate can rule PASS/FAIL on a task.
- [ ] Tool results go through the roll-up — run a tool that returns a large amount of content (say 5000 lines) and confirm that only the stub enters the main conversation, the body can be fetched back with `read_observation`, and the stub carries `size` / `truncated`.
- [ ] Running dozens of turns in a row stays on topic (post-compression identity + goal re-injection works).

---

## Phase 2 · From generic to scenario, narrowing down · not industry-bound

**Goal**: once the generic runtime runs, narrow it to a concrete business scenario (customer service / tendering / quality inspection / operations / translation / data analysis, and so on). The method is the same for every industry; do the eight steps.

1. **Build the eval set**: start with 3–5 typical tasks, each with an automatable pass/fail decision, an expected tool-call sequence, and a final database state. The eval set evolves with the code; do not "build first, test later."
2. **Narrow the tools**: the generic runtime may carry dozens of tools, while a business scenario usually uses a small handful (starting default 8–15). **Explicitly disable** the rest in a whitelist — leaving them in context scatters attention and raises the odds of a wrong pick; it is not enough to just not call them.
3. **Strengthen tool descriptions**: each business tool's description lists the required field names, types, and enum values directly. Whether a field is `user_id` or `userId`, an array or an object, what the enum values are — do not let the model guess. **This is the single highest-ROI optimization**, an order of magnitude more effective than editing the system prompt.
4. **A policy rule engine**: do not pile business rules into the system prompt (the model forgets them after dozens of turns). Make them "**inject a structured reminder before calling tool X**" — an eligibility check before a cancellation, a second confirmation before a deletion. A reminder at the point of use beats stating the rule once up front.
5. **Layer the prompt**: the system layer writes the role and capability boundary, the scenario layer writes the business rules and forbidden behaviors, the execution layer writes the output format. Keeping the three separate makes them easy to tune and A/B individually.
6. **Turn on reasoning mode** (if the model supports it and Phase 0 showed a payoff): turn it on for scenarios dense in multi-step judgment / numeric computation / rule checking; leave it off for simple Q&A (expensive, slow, no payoff).
7. **Run ablation experiments**: for each mechanism added, turn it off and rerun the eval set, and see how far the score drops. Keep the positive contributors, cut the negative ones, weigh the near-zero ones against maintenance cost. This step is the crux — some plausible-looking mechanisms raise the score when turned off, and a unit test cannot see it. A concrete counter-example from the tool-call-quality domain: **parameter auto-completion** (the harness fills in a missing tool parameter for the model) looks like a convenience but may measure as a negative contributor — locally correct, globally harmful, caught by single-point ablation, invisible to a unit test. Ablate down to a single mechanism on/off; do not switch a whole group.
8. **Attribute failures by dimension**: do not look only at the pass rate; also look at — **a tool that should have been called but wasn't** (if so → re-run the three checks in §1.3) / whether the tool-call parameters were right / whether the final database state was right / whether the reply said the numbers and clauses it should have / whether the required flow ran to the end. A single-dimension eval hides the real problem (the database was right but the number went unsaid, which to the customer is a job not done).

### 2.1 When narrowing graduates to an independent sub-harness

If cramming a scenario's domain knowledge into the main agent's context would blow it up, or it needs to evolve and iterate independently, make it an **independent sub-harness**. The criterion is whether the **five-dimension ontology** is complete —

1. **Domain entities**: what "things" the domain has (for a PPT sub-harness, slide / layout / content_block).
2. **Entity attributes**: each entity's fields + types + constraints.
3. **Relationships**: the logical constraints between entities (layout determines content_block type, and so on).
4. **State machine**: an entity's legal states + transition paths (draft → review → approved → exported).
5. **Operations**: the tool set the sub-harness exposes.

**Judgment line**: all five dimensions present = design complete; missing one is 80%; missing two is 40%; missing three = still at the "catch-all prompt" stage, not a sub-harness. Writing one 5,000-word system prompt and letting the model improvise ≠ a sub-harness.

`↪ Main text: the sub-harness cell's five-dimension ontology (§8.5)`

### 2.2 Extend the verifier from the hard gate to three layers

Phase 1 ran only the hard gate. Here, add the other two as needed:

- **Layer two · outcome judge**: use **another LLM** to score the final output semantically. The judge LLM is **cross-vendor / cross-family** from the agent LLM, to prevent preference leakage (same-family self-grading is biased toward itself). Needed only for open-ended tasks.
- **Layer three · PRM (process scoring)**: step-level scoring of the reasoning process. Add it once long tasks run stably, to give ablation a step-level signal.
- **Combining them**: a failed hard gate fails the whole thing — do not let the model scrape by on a process score on a failed task.

`↪ Main text: the three-layer verifier + the three-layer combination strategy (§5.8)`

**✅ Phase 2 completion gate**:

- [ ] Every task in the eval set can be **judged automatically** pass/fail.
- [ ] After narrowing, the eval-set score is higher than the generic version, and **ablation proves** it was the narrowing that did it (not an illusion).
- [ ] Failures are attributed by multiple dimensions (parameters / database state / things that should have been said / flow), not by pass rate alone.
- [ ] If a sub-harness was added: the five-dimension ontology is complete. If it was only narrowing: disabled tools are in the whitelist, and key rules are injected before the call.
- [ ] If an outcome judge was added: the judge is cross-family from the agent.

---

## Phase 3 · Cost structure + mechanism admission · spend where it counts

**Goal**: do not spread resources evenly. Hit the bottleneck where it is. Get the order wrong and the same money buys a worse result.

### 3.1 The order to spend

1. **Spend on the eval set first**: with no eval set you are tuning blind, and every later change becomes "did it actually help?" — unanswerable. Even a crude pass-rate-only set beats nothing.
2. **Then on tool descriptions**: the highest single-point ROI. A wrong field-name guess wastes a turn, and over dozens of turns may waste half of them.
3. **Then on the policy rule engine**: make business rules "inject before the call" and the model will not forget them. Doing this before reaching for a new model is far cheaper.
4. **Reasoning mode by task**: turn it on for the multi-step-judgment / rule-checking / numeric-computation-dense ones, off for simple Q&A.
5. **Model upgrade last**: expensive, irreversible (a swap means rerunning the eval set), and limited gain for most scenarios. What usually caps the pass rate is not model capability but a poorly tuned outer mechanism. **Swapping the model first is the most common mistake** — you spend the money and the score does not move.

**Infrastructure (compression / observability / loop detection / locking and cancellation) is admission, not investment**: nothing works without it, but "good enough to run" is enough, and over-engineering it only slows iteration.

### 3.2 Allocate by scenario type

| Scenario type | Spend here first |
|---|---|
| Customer service / rule-execution | Tool descriptions + policy rules, then consider reasoning mode |
| Code / complex planning | Reasoning mode + a strong model, tool descriptions and rules second |
| Long conversation / multi-turn | Compression + observability, or it collapses on its own after dozens of turns |
| High-concurrency / low-latency | A cheap model + tool-output caching + a simplified tool set |

### 3.3 The mechanism admission gate · every mechanism in the default profile must pass it

You cannot enable a mechanism by default just because it "looks reasonable." Before a mechanism enters the main harness's default path, it must meet at least these four:

1. **It changes real behavior**: not just adding a DTO, a schema, or a log field.
2. **It has an on/off ablation**: turning it off shows a change in pass_rate / cost / latency / reliability.
3. **It has a machine-readable trace**: recording the trigger reason, the rule ID, an input summary, and the result.
4. **It passes a stability check**: across N reruns, a perturbed prompt, and shuffled irrelevant fields, the gain cannot rest on a lucky pass.

A mechanism that falls short of the four stays an **experimental flag**, out of the default profile. **Cut negative-contribution mechanisms promptly** — keeping one **costs you twice** — it burns resources and drags the pass rate down. Being unwilling to cut code that looks right is a common mistake; one ablation shows it.

**✅ Phase 3 completion gate**:

- [ ] Spending went in the order above, and the eval set was built **before** the model upgrade.
- [ ] Every mechanism in the default profile passed the four admission rules (especially the on/off ablation data).
- [ ] Negative-contribution and near-zero-contribution mechanisms have been cut or demoted to experimental flags.

`↪ Main text: the four getting-started dimensions (at each chapter's end) / mechanism admission discipline (§VII Harness Lab)`

---

## Cross-cutting · the four-principle self-check · run it at the end of every Phase

When a Phase finishes, run it once against each of the four principles of control theory — if any one is breached, go back and fix it; do not carry a breach into the next Phase. Any bug you hit, place it into one of these four first.

- **Observable**: any silent failure (an error swallowed by try/catch, producing no event)? Any hidden state (an internal agent state with no corresponding event)? A persistently high `declared_vs_executed gap` (what the agent claims it did vs what the tool/verifier actually observed) is the early warning.
- **Controllable**: can a control point be bypassed (a hook bypass)? Is the tool granularity so fine the model cannot choose well? Any "fake landing" — a mechanism in the repo but a noop on the production path?
- **Stable**: does each mechanism have a bound (max_turn / max_token / max_depth / max_retry)? Can those bounds be monitored? Any loop blind spot, context bloat, reward hacking?
- **Closed-loop feedback**: does every change have ablation data behind it? "I think this is better" with no data = a broken loop.

`↪ Main text: the four principles of control theory + the common-pitfall mapping (§IX)`

---

## Advanced judgment lines · when to adopt (not expanded — go back to the main text when needed)

These two advanced capabilities are **off by default**; adopt them once the judgment line is met:

- **multi-agent / sub-agent fork-join**: first answer "what is the single agent's pass rate over N=10 runs on this task?" Never run → run the single agent first; ≥80% → don't add multi-agent, optimizing the single agent is worth more. Multi-agent burns about 15x the tokens of an ordinary chat (an agent is ~4x a chat, multi-agent ~15x), and the worst fit of all is a domain with few parallelizable subtasks and strong dependencies between them — coding above all.
  - **If the judgment is that you must adopt it** (>60 turns, the subtasks genuinely independent and verifiable): then ask whether the control flow is predictable — which substeps run in parallel, who cross-checks whom, how the results aggregate, all known before the run starts? **Predictable** → write that orchestration as a **deterministic script** that the runtime runs in the background (a dynamic workflow); the model's reasoning happens only when a leaf agent does its work, the lead's context is left with just one aggregated answer, and you save the most expensive tokens of the run — the lead improvising the orchestration — while the orchestration itself becomes re-runnable and auditable. **Unpredictable** (exploratory, the next step depends on the last) → the lead can only improvise the orchestration, and you are back to the 15x cost. Gate: the orchestration script can rerun detached from any one run, and every step's `hands_off` / `calls_tool` enters the trajectory.
  - **Boundary**: a dynamic workflow lowers orchestration cost, it does not loosen the admission bar — single agent first, N=10 ≥80% don't adopt, coding strong-coupling don't adopt, all still hold.
  `↪ Main text: Multi-Agent over-decomposition + dynamic workflow (§5.1.5 last passage + footnote / §5.1.6) / fork-join concurrency (§6.6) / the topology axis (§VIII)`
- **dynamic harness · sub-harness runtime routing**: the next notch up from §2.1's "should I build a sub-harness" — once the harness is running, **routing each task dynamically among several sub-harnesses**. Answer two things first: ① do you genuinely have ≥2 sub-harnesses with a complete five-dimension ontology (if not → finish a single one first, back to §2.1); ② can the task be judged by "entity features" rather than "fuzzy text" to decide which one to take (if not → it is not yet time to route, run a single harness). Once routing is on, meet three verifiable disciplines: routing is based on the task's entity features / the main harness can only invoke an already-mounted sub-harness and cannot conjure one / every routing decision enters the trajectory (write a task and verify the trajectory can answer "why it went to A and not B"). A dynamic harness and the dynamic workflow above are two orthogonal things: the former governs which tools/policy/verifier are mounted, the latter governs how control flow is held. **ReAct + dynamic harness + dynamic workflow** as a combination is a direction the main text's author is actively practicing and still evolving — treat it as a working direction, not a settled conclusion. The dominant dimension for picking sides is reward-signal strength — open-ended, unlabeled weak-reward tasks lean dynamic workflow (cross-checking built into the orchestration stands in for the missing hard verifier); standardized, recurring strong-reward tasks that a Hard Gate can judge (the typical shape of core To B delivery) lean dynamic harness (frozen mechanisms + hard verification to close out). `↪ Main text: main↔sub routing discipline (§8.7) / dynamic harness (§5.1.6)`
- **The Harness Lab workbench (the five layers Observe-Score-Ablate-Tune-Iterate)**: first answer "of the 8 runtime parts + Safety, how many are stable in my project?" Consider it only at ≥6; while the harness's own pass rate still swings >10pp week to week, running Ablate produces signal that is 95% noise. `↪ Main text: Harness Lab (§VII)`
- **Cross-vendor protocols (A2A and the like)**: at this stage, define your own JSON-RPC schema and document it as an internal standard; do not bind the architecture to an external spec that is still evolving. `↪ Main text: the interaction-boundary axis (§VIII)`

---

## The order to use this

1. **Run Phase 0, the Model Probe, first** — a cheap qualitative diagnostic that flags the mechanism search space and the traps before you try them.
2. **Phase 1** builds the generic runtime, with no business in mind, just getting the frame running. Pass the gate before moving on.
3. **Phase 2** narrows it alongside the business; do not wait for "the generic version to be perfect" before narrowing.
4. **Phase 3** can be consulted at any stage — it decides not "what to do" but "which to do first" and "which money to spend."
5. **The four-principle self-check** runs once at the end of each Phase.

The whole logic in one line: **take the model's pulse first, then build something that runs, then sharpen it for the scenario, then spend where it counts — and at every step confirm with a verifiable gate that it was done right; with no gate evidence, treat it as unfinished.**
