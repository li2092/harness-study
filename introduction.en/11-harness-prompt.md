# Harness Prompt · The executable landing spec for an agent

This file is the **executable companion** to the main text, *Harness Study*. The main text covers "which mechanisms there are and why they are designed this way"; this file covers "what order to build them in, and how to verify that each step was done right."

**How to use it**: hand this file, together with your concrete scenario ("build me an agent for scenario X"), to a coding agent. The agent works through Phase 0 → 1 → 2 → 3 in order, and **the completion gate at the end of each Phase must pass before the next Phase begins**. A gate answers "how do you verify it was done right," not "what was done." Without verifiable evidence, treat the step as unfinished.

**Global conventions**:

- Every concrete number in this file (token-usage thresholds, single-tool output caps, tool counts, pass-rate thresholds, and so on) is a **starting default**, to be tuned by measuring in your own scenario, not a universal constant. Numbers that come from the literature say so.
- Each Phase marks the main-text sections it corresponds to (`↪`); go back there when you need the underlying reasoning. The P0, P1, and P2 in the `↪` lines are the priorities §V of the main text assigns to the mechanisms: P0 is required for a minimum viable version, P1 is what to add before going to production, and P2 can wait until you scale.
- Build on a **strong model**. A weak model can't run multi-turn tool calling reliably and will fail the Phase 1 gate over and over.
- Wherever possible, back each Phase's completion gate with a **runnable check**: a script, an assertion, a comparison that actually runs, not just a written description. The one executing this spec is an agent, and a written criterion is exactly what an agent can most easily wave through with a one-line "satisfied" (the breeding ground for Artifact Claim Mismatch, AP04 in Appendix F). A gate that runs leaves no room to fudge. Example: the Phase 1 gate should at minimum include a hard check like "complete one full ReAct loop against a fake model service (a fake provider), and assert that every tool call has a matching tool result."
- The coverage of this spec is a middle ground: three parts distilled from practice (a generic runtime, scenario narrowing, and cost structure), plus behavioral probing, the four-principle self-check, and the mechanism admission check. Two advanced topics, the Harness Lab's five layers and the three composability axes, get only their decision criteria here, not a full treatment; go back to the main text when you need them.

---

## Phase 0 · Behavioral probing · get to know the model's quirks before you build

**Goal**: before building the runtime, run a set of diagnostics against the model endpoint you will use. This is behavioral probing, which the book also calls "taking the model's pulse." It produces a profile: which mechanisms this model needs, which it doesn't, and which are traps for it. The value lies less in "understanding the model" for its own sake than in **narrowing the range of mechanisms you will have to try later** and **flagging in advance the traps that would backfire**.

**Method core: the three-part probe.** Every probe consists of three parts:

1. **Stimulus**: a minimal task designed to expose one behavior (not hard, just enough to force the behavior out).
2. **Behavior classification**: judge *how* it did it, not *whether* it was right. Prefer programmatic judgment (did it crash, did it translate, how many times did it read: each of these is binary or countable), and let a model act as judge only on fuzzy dimensions.
3. **Mechanism implication**: given the behavior class, output **one configuration decision plus one prediction that later ablation can falsify**. A probe ends in a configuration decision and a testable prediction, never in a score.

**Four probe families** (graded hard to soft by the consequence of an error, run A through D):

- **Family A, protocol layer**: an error crashes the harness outright instead of merely degrading results. Highest priority, with a binary hard judgment. Typical probe: give the model a tool with a complex strict schema containing nested objects and arrays, and see whether it fails outright at the request layer or registers and calls the tool normally. If it fails outright, you must build a schema-normalization layer.
- **Family B, tool-use layer**: results degrade, but nothing crashes. Typical probe: give it a multi-file task that requires using tools first, and count how many times it reads before it acts. If it keeps reading and keeps putting off acting, add a check along the lines of "read completeness" or "evidence sufficiency."
- **Family C, instruction-following layer**: for a typical probe, use an English heading in the task and see whether the model, working in a Chinese context, translates the heading into Chinese. If it does, the verifier can't accept only the fixed English string; turn on multi-alias matching.
- **Family D, self-correction layer**: the deepest family, and the one that best tells models apart. Typical probe: give it an operation that will fail with an error, and see whether the model retries blindly or reads the error message and tries a different approach.

**✅ Completion gate**:

- [ ] Families A, B, C, and D each ran a few probes, and every probe was assigned to one behavior class (for programmatic judgments, keep the raw observation: crashed, translated, read N times).
- [ ] Every probe produced both a configuration decision and a falsifiable prediction, not just a score.
- [ ] You have a profile table: which mechanisms this model **must** turn on, which it **does not need**, which are **traps**. This table directly narrows the mechanism set for Phases 1–3.

**Note**: behavioral probing gives only **qualitative priors**, not quantitative conclusions. Take a finding like "turning on X recovers some of the missed tool calls." How much "some" really is has to wait until the Phase 3 ablation produces clean data. What probing can settle at a glance are facts such as "did it crash" and "did it translate," which don't depend on a precise comparison between configurations.

`↪ Main text: behavioral probing ("taking the model's pulse"), the first of the Harness Lab's three steps`

---

## Phase 1 · A generic agent runtime · no language binding, no scenario binding

**Goal**: build a generic runtime that can run a ReAct loop against any tool set. This step touches no concrete business; it just gets the frame running.

### 1.1 Module split: five modules

Three core modules plus two supporting:

- **engine**: runs the loop. The main loop is a single ReAct loop: send the message → receive the reply → execute any tool call → write the result back → decide whether to stop. Add a state machine to manage multiple turns, with the states awaiting user input, awaiting user confirmation, done, and errored. Check the cancellation signal at the start of every turn, and make a stop take effect immediately.
- **llm**: the multi-provider abstraction. Abstract a single unified interface and handle each vendor's differences in an adapter layer. Parameters such as `thinking` and reasoning are written differently by each vendor, so configure them per vendor through an `extra` field. **Requests to domestic model services should bypass the proxy explicitly, by domain, in code.** Don't rely on environment variables alone: some libraries read the uppercase `NO_PROXY` and others the lowercase `no_proxy`, so if you do use environment variables, set both.
- **tools**: handles tool registration and execution. Reload the tool list at every step and **do not cache it**: a tool newly registered in a POST hook must be visible on the next turn.
- **storage**: stores sessions and checkpoints.
- **types**: the central place for message and tool signatures.

`↪ Main text: Agent Loop (§5.1, P0) / Model Adapter & Routing (§5.2, the P0 boundary)`

### 1.2 Three protocols and runtime red lines

- **The message protocol**: once an assistant message issues tool calls (the `tool_calls` field in the OpenAI protocol, `tool_use` blocks in the Anthropic protocol), the next message must carry the matching tool results (in OpenAI, messages with role `tool`; in Anthropic, `tool_result` blocks inside a user message). Insert no other message in between, or the API will reject the next request with a 400.
- **Strict-schema normalization** (if Phase 0's Family A probes show the model is sensitive to strict schemas): normalize each schema before registering the tool, and convert schemas that contain nested objects or arrays into a form the model accepts.
- **The cancellation signal**: check it at the start of every turn. While holding the lock, do nothing but take the engine out, and release the lock as soon as you have it. Then run asynchronously while listening for the cancellation signal, and make sure the engine is returned on all three paths: success, cancellation, and error. Never wait synchronously on a long task inside the lock.

`↪ Main text: Model Adapter & Routing (§5.2)`

### 1.3 The tool layer

The tool layer does more than "register and execute." **Tool-call quality** (whether the model actually makes the call, makes it correctly, gets a clean result written back, and corrects itself after a failure) is decided jointly by the groups of practices below.

**Interface and guards**

- Define the Tool abstraction with the main text's five fields (`name`, `description`, `input_schema`, `execute`, and `policy`, where policy is the ToolPolicy, covering allowed_paths, timeout, requires_confirmation, and so on). For every tool call, the Registry does three things: schema validation → policy decision (allow, human approval, or deny) → execution, with an audit record written into the trajectory.
- Give every single tool output a **hard cap** (starting defaults: 20k for file reads, 10k for search, 15k for shell). Output over the cap goes through "result roll-up" below.
- Always invoke shell and git commands with an argument array, never through shell parsing: `execFile` in Node, `subprocess.run([...])` without `shell=True` in Python, `exec.Command` in Go. **Reject string concatenation**, to prevent command injection.

**Scheduling: the four tool-batch modes** (whether a batch of tools should run concurrently, run serially, or stop)

- **parallel_read**: read-only, no side effects, no path conflicts; concurrent by default (read_file, grep, glob, list_dir, web_search, web_fetch).
- **sequential_write**: writing files, changing the workspace, or changing state; serial by default (write_file, edit_file, shell_exec, git_*, and any tool marked DANGEROUS).
- **barrier**: when the next step needs permission confirmation, involves a dangerous operation, switches batches, or calls for a new decision based on the previous batch's observations, stop explicitly and make the decision at that switch point.
- **background_sidecar**: hand the work to a lightweight side agent that runs without interfering with the main line.
- **Main-line principle**: a single agent executes tools in batches → rolls up the results and writes them back → brings in a side agent only when needed. Don't start out with a sub-agent: the costs in three areas (the safety boundary, context isolation, and result aggregation) are more than most tasks can bear.

**Result roll-up: tool results never enter the main conversation as raw text**

- When a batch of tools finishes, it produces two things: the raw text goes into the **ArtifactStore** (which returns a reference), plus an **observation stub** (a trimmed summary, starting default around 200 characters, which enters the context). The main thread reads only the stub. When it needs the raw text, the model itself calls `read_observation(obs_id)` or `read_artifact` to fetch it on demand. The rule of thumb: **extract in full, inject on demand, never truncate, never skip pages**.
- The stub must carry the metadata `truncated:true`, `size`, and `preview_truncated_at`, to avoid two opposite failure modes. One is **overload**: everything goes into the context, triggering the lost-in-the-middle effect, so you pay for tokens the model never attends to. The other is **distortion**: a crude truncation drops information, and the agent doesn't even know it is looking at a truncated version. **The raw text must be stored persistently and be retrievable by reference**; truncating without keeping the raw text is still distortion.
- The three lines of prompt that go with it: ① when the feedback is large, look only at the stub, and use `read_observation` to fetch the full content; ② when the stub carries a `truncated` marker, check `size` to decide whether to fetch the full text; ③ errors like `PreprocessError` are preprocessing failures on multimodal content, not tool-call failures, so you can retry or try a different approach.

**Error returns: they decide whether the agent can correct itself**

- **Actionable**: say what went wrong and how to fix it, but don't throw away the useful information in the original stack trace. Example: `file_path 'data/output.txt' does not exist; did you mean 'data/input.txt'? list data/ first` is far better than throwing a raw `FileNotFoundError`. In the author's experience, this is a key piece of ACI (agent-computer interface) design for raising tool-call accuracy. The accuracy gain, though, comes from the whole Tool Registry and ACI design working together, not from this one rule alone.
- **Raw or sanitized errors, depending on the tool's origin**: a tool implemented in internal code, whose execution is fully under your control, returns the raw error (with details, so the agent can correct itself). A tool that reaches an external data source, whose results contain external content, returns a sanitized error (with the stack trace, internal paths, and sensitive fields removed). You can also split by environment: raw errors in development, sanitized errors in production. **Error returns are one of the most common injection points for prompt injection.**

**Recommended: equip web_search and web_fetch by default**

- The model's weights are frozen, and its knowledge has a cutoff date. The model can only guess at facts from after the cutoff (a new version number, a just-changed API, the current docs), and a wrong guess turns into a hallucination. These two tools connect the model to "the world after training" so it can look things up and check them live, which often improves quality more than another round of prompt tuning would.
- Two requirements go with them: ① when a return is large (dozens of results at once, or one article of tens of thousands of characters), it must go through "result roll-up" above; don't let the raw text flood the main conversation; ② fetched content is external input, so judge the credibility of its source first or hand it to a verifier; don't treat incorrect information that a search turns up as a factual basis.

**Diagnosis: a tool that should have been called but wasn't**

When the model should call a tool but outputs only text, there are three possible causes, one at each of three layers, and the fixes are completely different. Rule them out in the order response parsing → request parameters → prompt assembly; that is much faster than repeatedly editing the prompt or swapping the model:

1. **The response-parsing layer (false negative)**: the model may have written the call as a text tag in the body (e.g. `<tool_call>…</tool_call>`) instead of in the structured tool-call field (`tool_calls` in OpenAI, `tool_use` blocks in Anthropic). An Adapter that reads only the structured field then drops it as ordinary text. Fix: beyond the structured field, have the parsing layer extract text tags with a regex as a fallback.
2. **The request-parameter layer**: the default `tool_choice: auto` means the model may or may not call a tool. When an exchange must use a tool (it must query the database, it must write to disk), set `tool_choice` to require a tool call (`required` in OpenAI, `any` in Anthropic), or name a specific tool. **Turn this on per exchange and per scenario, never globally** (forcing calls all the time pushes the model to call tools when it shouldn't, which creates noise).
3. **The prompt-assembly layer**: an overlong Chinese prompt makes some models skip the tool call and answer in text instead. Keep the instruction to call a tool short and near the front, and split long explanations out.

`↪ Main text: Tool Registry & ACI (§5.3, P0) / ObservationPack · Observation Surface (§5.6) / the Model Adapter three causes (§5.2 last subsection) / Artifact (§5.4, P2)`

### 1.4 Context compression: three strengths

- **micro**: the lightest of the three, a local roll-up of one large tool result (the stub goes into the context, the raw text is stored externally, and `read_observation` fetches it on demand). The mechanism itself is described under "result roll-up" in 1.3; this entry only marks where it sits among the three compression strengths.
- **auto**: when the token estimate reaches 60–70% of the window (starting default, commonly 70%), use a small model to summarize the whole history. The summary **must keep four kinds of information**: any open `tool_call_id` and its state; each turn's key decisions and their reasons; artifact reference ids; and verifier failure information. Drop any one of them and the agent will make things up later on (inventing a fake observation or a fake id, or running into the same error again).
- **rolling window**: the crudest fallback; when the history runs too long, drop the earliest turns outright.
- **After compression you must re-inject the task goal and the system identity**, or after dozens of turns the agent drifts off topic and thinks it is doing something else.

`↪ Main text: Context (§5.4, P0) / Prompt Assets identity re-injection (§5.5, P0)`

### 1.5 Observability: instrument from the first line of code

- Put the instrumentation at **decision points**, not execution points: the places where a mechanism judges "should this be done."
- Record all four states: triggered and executed; condition unmet, so not executed; triggered but blocked; executed with an error.
- **No event is the most dangerous signal**: it means the code path was never reached.
- Loop detection blocks repeated tool calls. Queue any intervention messages and push them all at once after this turn's tool results have been processed; don't break the message protocol midway.

`↪ Main text: Observation Surface (§5.6) / Trajectory (§5.7, P0)`

### 1.6 The Safety control plane, to start: cutting across all mechanisms, not a ninth mechanism

Safety is not one more runtime mechanism. It is a control plane that cuts across all of them: every tool call, state change, and artifact write must pass through it, like the system-call gate of an operating system, with no exceptions. Its full form is a **four-layer permission decision model**:

- **permission mode**: the agent's overall run mode (read-only, workspace-write, and a few other levels).
- **allow, deny, and ask rules**: fine-grained rules configured per tool and per parameter pattern, following **default deny plus explicit allow** (allow `git status`, deny `git push`, ask on `git commit`).
- **hooks**: user scripts that run before and after a call, for complex decisions the rules cannot express. **Match on whole command words and normalized intent, not on a prefix of the raw command string.** Otherwise, allowing `cargo check` also lets `cargo checkpoint` through (cargo runs it as the external program `cargo-checkpoint` on the PATH).
- **sandbox**: an OS-level sandbox (Seatbelt, bubblewrap, containers) that bounds which files can be read and written and where network traffic can go. When the logical checks of the first three layers are bypassed, it is the last line of defense.

To start, get at least these two in place:

- **Critical safety decisions live in code, not with the model** (the Hard Gate): the decision to intercept a dangerous operation (deleting files, pushing code, making network requests, spending money) is written at the code layer, not left to the model's discretion through a prompt. The model assists only with soft judgments (whether content is harmful) and never serves as the last line of defense.
- **A human-in-the-loop approval gate (HITL approval gate)**: mark high-impact operations (deleting data, transferring money, deploying, sending email) with `requires_confirmation`. Before calling one, the agent hands it to a human for confirmation and only then executes it; the agent does not decide on its own whether to go ahead. The approval mode propagates down the parent-child agent chain (a sub-agent inherits its parent's setting by default and can never be looser).

`↪ Main text: the Safety control plane · the four-layer permission decision model + HITL (§5.9, cross-cutting)`

### 1.7 The verifier, to start: the Hard Gate only

Start with the cheapest of the three verifier layers, the **Hard Gate**: a program rules PASS or FAIL (pytest passes, the build succeeds, a file hash matches). The Outcome Judge (model review) and the PRM (process reward model) wait until Phase 2.

`↪ Main text: the three-layer verifier (§5.8, P0)`

### 1.8 Frontend integration (if any)

The backend is the **single source of truth**; don't keep a separate copy of the state in the frontend. When switching sessions, pull `last_messages` and `is_running` from the backend.

**✅ Phase 1 completion gate**:

- [ ] The runtime can start a ReAct loop against **any tool set** and run at least one task to completion.
- [ ] The trajectory has a complete event stream, instrumented at decision points and covering the four states.
- [ ] Dangerous commands (delete, push, spend money) are stopped at the **code layer**: write a task that triggers the interception and verify that it really fires, rather than relying on a line in the prompt that says "don't delete."
- [ ] High-impact operations (deleting data, transferring money, deploying) trigger human approval, and the agent really stops before the call to wait for human confirmation.
- [ ] The Hard Gate can rule PASS or FAIL on a task.
- [ ] Tool results go through roll-up: run a tool that returns a large amount of content (say 5000 lines) and confirm that only the stub entered the main conversation, the raw text can be fetched back with `read_observation`, and the stub carries `size` and `truncated`.
- [ ] Running dozens of turns in a row stays on topic (re-injecting identity and goal after compression works).

---

## Phase 2 · From generic to scenario, narrowing down · not industry-bound

**Goal**: once the generic runtime runs, narrow it to a concrete business scenario (customer service, tendering, quality inspection, operations, translation, data analysis, and so on). The method is the same for every industry and has eight steps.

1. **Build the eval set**: start with 3–5 typical tasks, each with a pass-or-fail criterion that can be judged automatically, an expected tool-call sequence, and a final database state. The eval set evolves with the code; don't "build first, test later." Split the eval set into a development set and a held-out set. Day-to-day tuning of prompts and rules looks only at the development set. The held-out set takes no part in tuning: run it before and after every change, only to check whether the gains on the development set still hold, so you avoid Overfitting to a Fixed Test Set (AP20, see Appendix F). Failed inputs you meet after launch should flow back into the eval set as new case records.
2. **Narrow the tools**: the generic runtime may carry dozens of tools, while a business scenario usually uses only a small subset (starting default 8–15). Use an allowlist that admits only those tools, or put the rest on a denylist to **disable them explicitly**. Don't just leave them there uncalled: tools left in the context scatter the model's attention and raise the odds of picking the wrong one.
3. **Strengthen tool descriptions**: in each business tool's description, list the required field names, types, and enum values directly. Whether a field is `user_id` or `userId`, whether it is an array or an object, how many values the enum has: don't make the model guess any of it. **In the author's experience, this is the single optimization with the highest return on investment**, usually far more effective than editing the system prompt again and again.
4. **A policy rule engine**: don't pile all the business rules into the system prompt (the model forgets them after dozens of turns). Turn them into "**inject a structured reminder before calling tool X**": pop up an eligibility check before a cancellation, and a second confirmation before a deletion. A reminder at the point of use is far more effective than a global statement.
5. **Layer the prompt**: the system layer writes the role and capability boundary, the scenario layer writes the business rules and forbidden behaviors, the execution layer writes the output format. Keeping the three separate makes them easy to tune and A/B individually.
6. **Turn on reasoning mode** (if the model supports it and Phase 0 showed a payoff): turn it on for scenarios dense in multi-step judgment, numeric computation, or rule checking; leave it off for simple Q&A (expensive, slow, no payoff).
7. **Run ablation experiments**: for each mechanism you add, turn it off and rerun the eval set to see how far the score drops. Keep the positive contributors, cut the negative ones, and decide on the near-zero ones by their maintenance cost. This step is the crux: some mechanisms that "look correct" give better results when turned off, and a unit test cannot see it. A concrete counter-example from tool-call quality is **lenient parameter handling**: when a tool's parameters fail to parse or don't match the schema, the harness patches over the problem and calls the tool anyway. It looks like it saves the model trouble, but it actually masks the error signal the model should have received. It is locally correct and globally harmful. Unit tests can't see it; it takes an ablation of that single mechanism, or a dedicated audit, to catch it. Ablate down to a single mechanism switched on and off; don't switch a whole group at once.
8. **Attribute failures by dimension**: don't look only at the pass rate. Also check **whether the tools that should have been called were called** (if not, go back to "a tool that should have been called but wasn't" in 1.3 and run the three checks), whether the tool-call parameters were right, whether the final database state was right, whether the reply stated the numbers and clauses it should have, and whether the required flow ran to the end. A single-dimension eval hides real problems (the database was right but the number went unsaid, which to the customer means the job wasn't done).

### 2.1 When narrowing graduates to an independent sub-harness

A sub-harness is a child harness, called up dynamically per task, that carries its own domain rules. If cramming a scenario's domain knowledge into the main agent's context would blow the context up, or the scenario needs to evolve and iterate independently, make it an **independent sub-harness**. The criterion is **whether the domain model is complete across five dimensions** (the main text borrows the word "ontology" and calls this the "five-dimension ontology"; here it means a domain-model schema):

1. **Domain entities**: what "things" the domain has (for a PPT sub-harness, slide, layout, and content_block).
2. **Entity attributes**: the fields each entity has, and each field's type and constraints.
3. **Relationships**: the logical constraints between entities (for example, layout determines the type of content_block).
4. **State machine**: an entity's legal states and transition paths (draft → review → approved → exported).
5. **Operations**: the tool set the sub-harness exposes.

**Criterion**: the design is complete only when all five dimensions are present. The more dimensions are missing, the further it is from a real sub-harness; with three or more missing, it is still at the "catch-all prompt" stage and does not count as a sub-harness. Writing one 5,000-character system prompt and letting the model improvise is not a sub-harness.

`↪ Main text: the sub-harness cell's five-dimension ontology (§8.5)`

### 2.2 Extend the verifier from the Hard Gate to three layers

Phase 1 ran only the Hard Gate. Here, add the other two layers as needed:

- **Layer two, the Outcome Judge**: use **another model** to score the final output semantically. The judge model and the agent's model should come **from different vendors or different model families**, to reduce preference leakage (a judge model favors content generated by models from its own family or models it is related to by inheritance). Only open-ended tasks need this layer.
- **Layer three, PRM (process scoring)**: score the reasoning process step by step. Add it once long tasks run stably, to give ablation experiments a step-by-step signal.
- **Combination rule**: if the Hard Gate fails, the whole result fails outright; the model doesn't get to scrape through a failed task on its process score.

`↪ Main text: the three-layer verifier + the three-layer combination strategy (§5.8)`

**✅ Phase 2 completion gate**:

- [ ] Every task in the eval set can be **judged automatically** as pass or fail, and the development and held-out sets are already separated.
- [ ] After narrowing, the eval-set score is higher than the generic version's, and **an ablation experiment proves** that the narrowing is what did it, not an illusion; the score on the held-out set is not noticeably lower than on the development set.
- [ ] Failures are attributed along multiple dimensions (parameters, database state, what should have been said, flow), not by pass rate alone.
- [ ] If you built a sub-harness: all five dimensions are present. If you only narrowed: the tool allowlist contains only the tools the scenario uses, and key rules are injected before the call.
- [ ] If you added an Outcome Judge: the judge model and the agent's model come from different families.

---

## Phase 3 · Cost structure + mechanism admission · spend where it counts

**Goal**: don't spread resources evenly; put them where the bottleneck is. Get the order wrong, and the same money won't buy the same result.

### 3.1 The order of investment

1. **Invest in the eval set first**: without evals you are tuning blind, and for every later change you can't say whether it actually helped. Even a crude eval that looks only at the pass rate beats having none.
2. **Then invest in tool descriptions**: in the author's experience, this is the single spot with the highest return on investment. Each wrong guess at a field name wastes a turn, and over dozens of turns the wasted turns can add up considerably.
3. **Next, invest in the policy rule engine**: turn business rules into "inject before the call," and the model won't forget them. Finishing this step and then checking performance is far cheaper than swapping the model straight away.
4. **Reasoning mode depends on the task**: turn it on for scenarios dense in multi-step judgment, rule checking, or numeric computation; leave it off for simple Q&A.
5. **Model upgrade last**: expensive, irreversible (a new model means rerunning the evals), and of limited gain for most scenarios. What usually holds the pass rate back is not model capability but outer mechanisms that aren't tuned well. **Swapping the model as the first step is the most common mistake**: the money is spent and the score doesn't rise.

**Infrastructure (compression, observability, loop detection, locking and cancellation) is the price of admission, not an investment**: without it nothing else is possible, but "good enough to run" is enough, and over-engineering it only slows iteration down.

### 3.2 Allocate by scenario type

| Scenario type | Invest here first |
|---|---|
| Customer service / rule-execution | Tool descriptions + policy rules, then consider reasoning mode |
| Code / complex planning | Reasoning mode + a strong model, tool descriptions and rules second |
| Long conversation / multi-turn | Compression + observability, or it collapses on its own after dozens of turns |
| High-concurrency / low-latency | A cheap model + tool-output caching + a simplified tool set |

### 3.3 The mechanism admission check: every mechanism in the default configuration must pass it

You cannot enable a mechanism by default just because it "looks reasonable." Before a mechanism enters the main harness's default path, it must meet at least these four:

1. **It changes real behavior**: not just adding a DTO, a schema, or a log field.
2. **It has on/off ablation data**: turning it off shows a change in pass rate, cost, latency, or reliability.
3. **It has a machine-readable trace**: recording the trigger reason, the rule ID, an input summary, and the result.
4. **It passes a stability check**: the gain must not rest on lucky passes. There are three practices. First, rerun the eval several times, each time from a clean state (response caching off, no fixed seed, no shared files, memory, or workspace); otherwise the reruns are not independent and stability gets overestimated (Non-Independent Reruns, AP01, see Appendix F). Second, run an input perturbation test: make small changes to the input that leave the task's meaning intact (for example, a random nonce added to each run, a paraphrase, shuffled irrelevant fields) and see whether the result stays stable. Third, report both pass@1 and pass^k (the fraction of tasks that pass all k times).

A mechanism that falls short of these four stays an **experimental flag** and stays out of the default configuration. **Cut negative-contribution mechanisms promptly**: keeping one means a double loss (it takes up resources and drags the pass rate down). Being reluctant to cut "code that looks correct" is a common mistake, and one ablation run exposes it.

**✅ Phase 3 completion gate**:

- [ ] Spending went in the order above, and the eval set was built **before** the model upgrade.
- [ ] Every mechanism in the default configuration passed the four admission conditions (above all, it has on/off ablation data).
- [ ] Negative-contribution and near-zero-contribution mechanisms have been cut or demoted to experimental flags.

`↪ Main text: the four getting-started dimensions (at each chapter's end) / mechanism admission rules (§VII Harness Lab)`

---

## Cross-cutting · the four-principle self-check · run it at the end of every Phase

When a Phase finishes, check it once against each of the four principles of control theory (the book borrows these concepts from control theory as an analogy; see §IX). If any one of them doesn't hold, go back and fix it; don't carry the problem into the next Phase. Whenever you hit a bug, first assign it to one of these four as well.

- **Observable**: any silent failures (an error swallowed by try/catch, producing no event)? Any hidden state (internal agent state with no corresponding event)? A persistently high "claimed-versus-actual gap" (the declared_vs_executed gap: the difference between what the agent claims it did and what the tools or the verifier actually observed) is a warning signal.
- **Controllable**: can a control point be bypassed (Hook / Allowlist Bypass, AP13, see Appendix F)? Is the tool granularity so fine that the model can't choose well? Any "fake landing," where a mechanism is in the repo but does nothing on the production path?
- **Stable**: does each mechanism have a bound (max_turn, max_token, max_depth, max_retry)? Can those bounds be monitored? Any loop blind spot, context bloat, or reward hacking?
- **Closed-loop feedback**: does every change have ablation data behind it? "I think this is better" without data means closed-loop feedback has not held.

`↪ Main text: how the four principles of control theory map to the anti-patterns (§9.2)`

---

## Advanced decision criteria · when to adopt (not expanded; go back to the main text when needed)

The advanced capabilities below are **off by default**; adopt one only when its criteria are met. Apart from those with a cited source, the numbers here are starting defaults, to be tuned to your scenario.

- **Multi-agent / sub-agent fork-join**: first answer "what is the single agent's pass rate over 10 runs on this task?" If you haven't run it, run the single agent first. If the pass rate is already 80% or higher, don't add multi-agent; optimizing the single agent pays off better. According to Anthropic's article on its multi-agent research system (2025-06), a single agent uses about 4x the tokens of an ordinary chat, and a multi-agent system about 15x. Avoid it especially in scenarios like coding, where the subtasks depend heavily on one another and little can run in parallel.
  - **If you judge that you must adopt it** (the task runs past 60 turns, and the subtasks are genuinely independent and can each be verified): then ask whether the control flow can be fixed in advance. Which substeps run in parallel, who cross-checks whom, how the results are aggregated: is all of that clear before the run starts? **If it can be fixed in advance**, write that orchestration as a **deterministic script** and let the runtime run it in the background (a dynamic workflow). Model inference then happens only when the leaf agents do their work, and the main agent's context ends up holding just one aggregated answer. You save the overhead of the main agent improvising the orchestration, and the orchestration itself can be rerun and audited. **If it can't be fixed in advance** (an exploratory task, where the next step depends on the result of the last one), the main agent has to improvise the orchestration, and you are back to expecting roughly 15x the cost. Gate: the orchestration script can be rerun independently of any particular run, and every step's `hands_off` and `calls_tool` are recorded in the trajectory.
  - **Boundary**: a dynamic workflow lowers the cost of orchestration; it does not lower the admission bar. These rules still hold: single agent first; don't adopt at a 10-run pass rate of 80% or higher; don't adopt for tightly coupled tasks like coding.
  `↪ Main text: Multi-Agent Over-Decomposition (AP09) + dynamic workflow (§5.1.5 last passage + footnote / §5.1.6) / fork-join concurrency (§6.6) / the topology axis (§VIII)`
- **Dynamic harness, the runtime routing of sub-harnesses**: this is the next step after §2.1's question, "should I build a sub-harness?" Once the harness is running, it **chooses dynamically among several sub-harnesses per task**. Answer two questions first: ① do you really have two or more sub-harnesses that are complete in all five dimensions (if not, first complete a single one; go back to §2.1)? ② can you decide which one to take by "entity features" rather than "fuzzy text" (if you can't, it isn't yet time for routing; run a single harness)? Once routing is on, it must satisfy 3 verifiable rules: routing is based on the task's entity features; the main harness can invoke only sub-harnesses already mounted and cannot conjure one up; and every routing decision is written into the trajectory (write a task and verify that the trajectory shows "why it went to A and not B"). A dynamic harness and the dynamic workflow above are two independent things: the former governs which tools, policies, and verifiers are mounted, and the latter governs who holds the control flow. The combination **ReAct + dynamic harness + dynamic workflow** is a direction the main text's author is actively practicing and still evolving; it is given here as a direction based on current practice, not as a settled conclusion. Choosing between the two depends mainly on the strength of the reward signal. Open-ended, weak-reward tasks with no standard answer lean toward the dynamic workflow (cross-checking built into the orchestration stands in for the missing hard verifier). Standardized, recurring, strong-reward tasks that a Hard Gate can judge (the typical shape of core B2B delivery) lean toward the dynamic harness (fix the mechanisms in place and close out with hard verification). `↪ Main text: the main-to-sub harness routing rules (§8.7 "What prompts to write") / dynamic harness (§5.1.6)`
- **The Harness Lab workbench (the five layers Observe-Score-Ablate-Tune-Iterate)**: first answer "of the 8 runtime mechanisms plus Safety, how many are already stable in the project?" Consider it only at 6 or more. If the harness's own pass rate still swings by more than 10 percentage points from week to week, hold off on Ablate (ablation): most of the differences it turns up would be drowned out by noise, so stabilize the evals first. `↪ Main text: Harness Lab (§VII)`
- **Cross-vendor protocols (A2A and the like)**: at this stage, define your own JSON-RPC schema and document it as an internal standard; do not bind the architecture to an external spec that is still evolving. `↪ Main text: the interaction-boundary axis (§VIII)`

---

## The order to use this

1. **Run Phase 0, behavioral probing, first**: a cheap qualitative diagnostic that marks out the range of mechanisms to try later, and the traps, before you start.
2. **Phase 1** builds the generic runtime, with no business in mind, just getting the frame running. Pass the gate before moving on.
3. **Phase 2** narrows it alongside the business; do not wait for "the generic version to be perfect" before narrowing.
4. **Phase 3** can be consulted at any stage: it decides not "what to do" but "what to do first" and "where to spend the money."
5. **The four-principle self-check** runs once at the end of each Phase.

The whole logic in one line: **get to know the model's quirks first, then build something that runs, sharpen it for the scenario, and spend where it counts. At every step, confirm with a verifiable gate that it was done right; without gate evidence, treat it as unfinished.**
