# Concept

Contingency Instruction Cache (CIC) is a design note / schema proposal for embodied, browser, and office automation agents whose environment may change while an action is underway. Its scope is narrow: reducing synchronous decision latency after an environmental change by preparing a small number of contingency instructions in advance.

## The Latency Problem

A common synchronous decision flow is:

```text
event happens -> ask model -> wait -> decide -> act
```

Even when an event is foreseeable, the agent remains blocked while a planner or large model produces a fresh response.

CIC moves a small amount of planning work earlier and overlaps it with current execution:

```text
execute current action -> precompute cached contingencies -> event happens -> match cached trigger -> use cached instruction
```

The intended gain is not faster model inference, guaranteed real-time behavior, or better plan quality. It is less synchronous waiting *after* an environmental change, because a bounded instruction may already be available in the plan bundle.

## Plan Bundles

A planner produces a short-lived CIC plan bundle containing:

1. a short main plan for the expected path;
2. a small number of cached contingencies, two to four in this schema;
3. a `trigger` and instruction for each cached contingency;
4. a `valid_if` condition and expiration time for each cached contingency; and
5. `replan_if` conditions for invalid, unknown, or high-risk situations.

The plan bundle should remain selective and short-lived. Caching many speculative branches increases monitoring cost, ambiguity, and the chance of using stale instructions. A useful cached contingency describes a foreseeable event with a specific trigger and a bounded response that the surrounding system is willing to authorize.

## Runtime Behavior

During execution, a fast monitor compares observed events with cached triggers. The arbiter accepts a cached contingency only when its `trigger` matches, its `valid_if` condition holds, and its expiration deadline has not passed. The executor can then use the cached instruction without waiting for a fresh planner response.

CIC requests replanning when the plan bundle or matching cached contingency is expired or invalid, when an observed event is unknown or unmatched, or when a high-risk `replan_if` condition holds. High-risk conditions should be routed to an external fallback path before task execution continues.

CIC therefore complements a planner; it does not replace one. It proposes a small data structure and execution pattern, not a complete agent architecture.
