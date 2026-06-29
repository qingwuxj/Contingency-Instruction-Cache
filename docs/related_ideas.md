# Related Ideas

Contingency Instruction Cache (CIC) is not presented as original work. CIC does not invent these ideas. It is better understood as a modest attempt to organize several adjacent ideas into a lightweight schema and execution pattern.

The narrow goal is reducing synchronous decision latency after environmental changes. CIC asks whether a short-lived plan bundle with a small number of cached contingencies can sometimes provide a usable instruction before a fresh planning request completes. This document is a brief conceptual map, not a formal literature review.

## Asynchronous planning

Asynchronous planning overlaps planning work with ongoing execution instead of making every action wait for a new plan. CIC uses this general intuition when a planner prepares a short plan bundle while the current action is underway. It does not define a scheduler, concurrency model, or general asynchronous planning system.

## Contingency planning

Contingency planning prepares responses for possible departures from an expected path. CIC adopts a deliberately small version of this idea: each plan bundle contains only a few cached contingencies, each with a `trigger`, instruction, `valid_if` condition, expiration time, and fallback. It is not intended to represent a complete branching policy or an optimal contingency plan.

## Behavior trees

Behavior trees commonly organize reactive behavior through conditions, priorities, and action branches. A CIC executor could pass a cached instruction into a behavior-tree-based system, but CIC does not replace behavior trees or prescribe their runtime semantics. Its cached contingencies are temporary planner outputs rather than a complete behavior definition.

## Plan caching

Plan caching reuses previously computed planning results. CIC uses a narrower, short-lived cache: the cached contingencies belong to one plan bundle and are constrained by `valid_if` and expiration conditions. CIC does not assume that plans can be reused safely across tasks, sessions, or substantially changed world states.

## Event-triggered replanning

Event-triggered replanning requests a new plan when observations indicate that the current plan is no longer suitable. CIC first checks whether a known event matches a valid cached trigger. It requests replanning when the plan bundle or cached contingency is invalid or expired, the event is unknown or unmatched, or a high-risk `replan_if` condition holds.

## Safety fallback / external fallback path

In this proposal, safety fallback refers to an external fallback path used before or instead of continued task execution in a high-risk situation. CIC assumes such a path may exist, but does not design it and does not provide a safety guarantee. A cache hit must not override external constraints or risk controls.

## World models

World models or belief states can help a planner describe likely changes and generate useful contingencies. CIC only consumes a `world_state_summary`; it does not create, update, or validate a world model. Poor state information can therefore produce incorrect triggers, stale cached contingencies, or inappropriate instructions.
