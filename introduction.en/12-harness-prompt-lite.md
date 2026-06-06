# A Generic TDD Prompt for an Agent Harness

Three generic instructions you can feed a coding AI directly to build and land an agent runtime.
The three are upstream-to-downstream: first build a generic runtime, then narrow it to the scenario, then allocate resources by cost structure.

---

## Part one: A generic agent runtime (language-agnostic)

```
Build an agent runtime — Python is fastest (two days to running), TypeScript
is handy for wiring a frontend (four days), Rust is solid but more work (about
a week). Split it into three core modules plus two supporting: engine runs the
loop, llm does the multi-provider abstraction, tools handles registration and
execution; storage holds sessions and checkpoints, types is the central place
for message and tool signatures.

The engine's main loop is one ReAct: send the message → receive the reply →
execute any tool call → write the result back → decide whether to stop. Add a
state machine for multi-turn: awaiting user input, awaiting user confirmation,
done, errored. Check the cancellation signal at the top of every turn; stop
must take effect immediately.

Abstract llm into one unified interface and handle each vendor's differences
in an adapter layer. The thinking parameter is written differently by each
vendor, so configure it through an extra field. The assistant-message protocol
is strict: a tool_result must follow immediately after tool_calls with nothing
in between, or the next request returns a 400 outright. Domestic APIs must
explicitly bypass the proxy, with a dedicated no_proxy — the uppercase variable
alone won't stop the lowercase one.

Two layers of context compression. When messages pile up, first clear old tool
results (micro); when the token estimate exceeds 60–70% of the window, trigger
a small-model summary (auto). After compression you must re-inject the task
goal and the system identity, or after dozens of turns the agent drifts off
topic and thinks it is doing something else.

The tool layer reloads the list every step — do not cache it, because a tool
registered in a POST hook has to be visible next turn. Give each single tool
output its own hard cap (file read 20k, search 10k, shell 15k to start); over
the cap, send it to external storage and return an ID. Route shell and git
commands through execFile with array arguments; reject string concatenation, to
prevent injection.

Tool results never enter the main conversation as raw text. After a batch runs,
the raw text lands in external storage (returning a ref), and only a trimmed
summary — a stub, carrying size and a truncated marker — goes into context; for
the raw text, the model itself sends read_observation to fetch on demand:
extract in full, inject on demand, never truncate, never skip pages. Error
returns must be actionable (say what went wrong and how to fix it, don't dump a
raw stack trace), and errors from tools that reach external data sources are
sanitized first, to prevent injection.

When the model should call a tool but emits only a stretch of text, rule out
three things in order before editing the prompt or swapping the model. First,
response parsing: the model may have written the call as a text tag instead of
into the structured tool_calls field, so have the parsing layer also catch it
with a regex. Second, request parameters: on a turn that must use a tool, set
tool_choice to required — per turn, not globally on. Third, prompt assembly: an
overlong Chinese prompt makes the model too lazy to call a tool, so keep the
trigger instruction short and near the front.

Instrument observability from the first line. Instrument at decision points,
not execution points — where the mechanism judges "should this be done." Four
states: triggered and executed, condition unmet and not executed, triggered
but blocked, executed and errored. No event is the most dangerous signal — it
means the code path was never reached.

Loop detection catches repeated tool calls; queue any intervention message and
push it after the tool_result is processed, all at once, instead of breaking
the message protocol mid-stream.

For concurrency, do not wait synchronously on a long task while holding the
lock. Inside the lock, only take the engine out and release immediately, then
run async and listen for the cancellation signal, guaranteeing the engine is
returned on all three paths — success, cancellation, error.

When a frontend integrates, the backend is the single source of truth; do not
keep a frontend state snapshot. On a session switch, pull last_messages and
is_running from the backend.

Estimate the build time for a single agent from the three language timings above, then add a week
for observability instrumentation, loop detection, and multi-agent isolation.
Build on a strong model — a weak one cannot carry multi-turn tool calling.
```

---

## Part two: Narrowing from generic to a scenario (industry-agnostic)

```
Once the generic runtime runs, narrow it to a concrete business scenario.
Whether it is customer service, tendering, quality inspection, operations,
translation, or data analysis, the method is the same; do the eight steps.

Step one: build the eval set. Start with 3–5 typical tasks, each with an
automatable pass/fail decision, an expected tool-call sequence, and a final
database state. The eval set evolves with the code; do not "build first, test
later."

Step two: narrow the tools. The generic runtime may carry 40–50 tools, while a
business scenario usually uses 8–15. Explicitly disable the rest in a
disabledTools whitelist — it is not enough to just not call them; left in
context they scatter the model's attention and raise the odds of a wrong pick.

Step three: strengthen tool descriptions. Each business tool's description
lists the required field names, types, and enum values directly. Whether a
field is user_id or userId, an array or an object, what the enum values are —
do not let the model guess. One wrong guess wastes a turn; this is the
highest-ROI single-point optimization, an order of magnitude more effective
than editing the system prompt.

Step four: a policy rule engine. Do not pile business rules into the system
prompt — the model forgets them after dozens of turns. Make them "inject a
structured reminder before calling tool X": an eligibility check before a
cancellation, a second confirmation before a deletion, the preconditions before
a refund. A reminder at the point of use beats stating the rule once up front.

Step five: layer the prompt. The system layer writes the role and capability
boundary, the scenario layer writes the business rules and forbidden behaviors,
the execution layer writes the output format (must report the number, must
reply in the same language, must wait for user confirmation). Keeping the three
separate makes them easy to tune and A/B individually.

Step six: turn on reasoning mode (if the model supports it). For scenarios
dense in multi-step judgment, numeric computation, or rule checking, reasoning
mode can add ten points outright. Leave it off for simple Q&A — a waste of
tokens.

Step seven: run ablation experiments. For each mechanism added, turn it off and
rerun the eval set, and see how far the score drops. Keep the positive
contributors, cut the negative ones, weigh the near-zero ones against
maintenance cost. This step is the crux — some "looks-right" mechanisms raise
the score when turned off, and a unit test cannot see it at all.

Step eight: attribute failures by dimension. Do not look only at the pass rate;
also look at whether the tool-call parameters were right, whether the final
database state was right, whether the reply said the numbers and clauses it
should have, whether the required flow ran to the end. A single-dimension eval
hides the real problem: the database was right but the number went unsaid, which
to the customer is a job not done.

With this narrowing done, the generic runtime gains 10–20 points in a specific
scenario. Cheaper than swapping the model, faster than rewriting the framework.
```

---

## Part three: Cost structure (what to spend on first, what last)

```
Do not spread resources evenly across every mechanism. Hit the bottleneck where
it is. Get the order wrong and the same money buys a worse result.

Spend on the eval set first. With no eval set you are tuning blind, and every
later change becomes "did it actually help?" — unanswerable. An eval set crude
enough to look only at the pass rate still beats nothing. Three to five
auto-judged typical tasks, up and running, is enough. Run it on every change,
and fill in edge cases over time.

Then spend on tool descriptions. This is the highest single-point ROI — one
wrong field-name guess wastes a turn, and over dozens of turns may waste half of
them. Spelling out the required fields, types, and enum values beats editing the
system prompt ten times over.

Then spend on the policy rule engine. Make business rules "inject before the
call." After dozens of turns the model forgets the rules in the system prompt;
the ones injected on the spot it does not forget. Doing this before reaching for
a new model is far cheaper.

Whether to turn on reasoning mode depends on whether the task is multi-step.
Turn it on for scenarios dense in rule checking, numeric computation, and
multi-condition judgment — it can add ten points. Leave it off for simple Q&A:
expensive, slow, no payoff.

Put model upgrades last. Start from a cheap model and swap only when you hit the
bottleneck. A model is expensive, irreversible (a swap means rerunning the eval
set), and limited in gain for most scenarios — what usually caps the pass rate
is not model capability but a poorly tuned outer mechanism. Most teams' mistake
is to swap the model first — you spend the money and the score does not move.

Infrastructure (compression, observability, loop detection, locking and
cancellation) is table stakes, not an investment. Nothing works without it. But
"good enough to run" is enough, and over-engineering it only slows iteration.

Allocation by scenario type:
  Customer service / rule execution   tool descriptions + policy rules first, then reasoning mode
  Code / complex planning             reasoning mode + a strong model first, descriptions and rules second
  Long conversation / multi-turn      compression + observability first, or it collapses after dozens of turns
  High-concurrency / low-latency      a cheap model + tool-output caching + a simplified tool set

The most counterintuitive point comes last: cut negative-contribution
mechanisms promptly. Some mechanisms lose points when added, and keeping one
costs you twice — it burns resources and drags the pass rate down. One ablation
shows it. Being unwilling to cut "code that looks right" is a common mistake.

The other direction: for a mechanism to enter the default profile, it passes
four tests — it changes real behavior (not just adding a DTO/schema/log field),
it has on/off ablation data, it has a machine-readable trace, and it passes a
stability check (N reruns plus a perturbed prompt, the gain not resting on a
lucky pass). One that falls short stays an experimental flag, out of the default
profile.
```

---

## The order to use the three parts

1. Use Part one to build the generic runtime first. This step ignores the
   concrete business and just gets the frame running.
2. Once the generic runtime can start a ReAct loop against any tool set, use
   Part two to narrow it to the scenario. This step evolves with the business;
   do not wait for "the generic version to be perfect" before narrowing.
3. Part three can be consulted at any stage — it decides not "what to do" but
   "which to do first" and "which money to spend." Get the order wrong and the
   generic runtime, however well built, still produces no results in the
   business.

The whole logic of the three parts: **build something that runs, then sharpen it
for the scenario, then spend where it counts.**
