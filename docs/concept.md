# Concept

Action Branch Cache (ABC) is a design pattern / schema proposal for embodied, browser, and office automation agents whose environment may change while an action is underway. Its scope is narrow: reducing agent decision-to-action latency after an environmental change by preparing a small number of condition-bound action branches in advance.

## The Latency Problem

A simplified synchronous decision flow is:

```text
state changes -> update state -> decide or replan -> validate action -> act
```

Even when a change is foreseeable, the agent may repeat the whole synchronous path before it can act. A model call can contribute to that latency, but state handling, branch formation, validation, and execution handoff may contribute as well.

ABC moves a small amount of branch formation earlier and overlaps it with current execution:

```text
execute current plan -> precompute action branches -> state changes -> match trigger -> validate and switch branch
```

The intended target is a shorter decision-to-action path after an environmental change, not faster model inference, guaranteed real-time behavior, or better plan quality. A bounded action branch may already be available in the plan bundle, but surrounding systems still decide whether it remains applicable and allowed.

## Plan Bundles

A planner produces a short-lived ABC plan bundle containing:

1. a short main plan for the expected path;
2. a small number of cached action branches, two to four in this schema;
3. a `condition`, structured `trigger`, and structured `action` for each branch;
4. a `valid_if` condition and expiration time for each branch; and
5. `replan_if` conditions for invalid, unknown, or high-risk situations.

The plan bundle should remain selective and short-lived. Caching many speculative branches increases monitoring cost, ambiguity, and the chance of using stale actions. A useful cached action branch describes a foreseeable state change with a specific trigger and a bounded action that the surrounding system can validate.

ABC is not limited to exception recovery. A branch can represent an ordinary object movement, page transition, API status, file-state change, user-input change, or workflow switch. High-risk exceptions can also be represented, but they are one use case rather than the organizing definition.

The schema separates human-readable text from adapter-oriented fields. `trigger.description` and `action.description` explain intent, but real systems would need monitor adapters for `trigger.detector`, `trigger.signals`, and `trigger.rule`, plus executor adapters for `action.command`, `action.args`, and `action.executor`.

## Progressive Bundles

ABC does not require the full main plan and branch cache to be generated before the first action. A `bootstrap_only` bundle may contain a low-risk `bootstrap_action` and an `async_branch_request`, allowing the first bounded action to begin while the fuller branch cache is hydrated asynchronously.

This optional mode can reduce initial planning latency, but it is constrained: the bootstrap action must be interruptible, short-lived, externally validated, and rejected when its `valid_if` or expiration metadata no longer holds. If no hydrated branch is ready and an unknown or high-risk event appears, the system should use an external fallback path or request replanning.

## Runtime Behavior

During execution, a fast monitor compares observed changes with cached triggers. The arbiter considers a cached action branch only when its `trigger` matches, its `valid_if` condition holds, and its expiration deadline has not passed. The branch must still pass external action validation before the executor can switch to its action.

ABC requests replanning when the plan bundle or matching cached action branch is expired or invalid, when an observed change is unknown or unmatched, or when a high-risk `replan_if` condition holds. High-risk conditions should be routed to an external fallback path before task execution continues.

ABC therefore complements a planner; it does not replace one. It proposes a small data structure and execution pattern, not a complete agent architecture.
