# Related Ideas

Action Branch Cache (ABC) is not presented as original work. ABC does not invent these ideas. It is better understood as a modest attempt to organize several adjacent ideas into a lightweight schema and execution pattern.

The narrow goal is reducing agent decision-to-action latency after environmental changes. ABC asks whether a short-lived plan bundle with a small number of cached action branches can sometimes avoid rebuilding the full decision path from scratch. Model waiting may be part of that path, but it is not the complete target. This document is a brief conceptual map, not a formal literature review.

## Asynchronous planning

Asynchronous planning overlaps planning work with ongoing execution instead of making every action wait for a new plan. ABC uses this general intuition when a planner prepares a short plan bundle while the current action is underway. It does not define a scheduler, concurrency model, or general asynchronous planning system.

## Contingency planning

Contingency planning prepares responses for possible departures from an expected path. ABC borrows a deliberately small part of this idea, while also covering ordinary state changes and workflow branches: each plan bundle contains only a few cached action branches, each with a `condition`, `trigger`, action, `valid_if` condition, expiration time, and fallback. It is not intended to represent a complete branching policy or an optimal contingency plan.

## Behavior trees

Behavior trees commonly organize reactive behavior through conditions, priorities, and action branches. An ABC executor could pass a cached action into a behavior-tree-based system, but ABC does not replace behavior trees or prescribe their runtime semantics. Its cached action branches are temporary planner outputs rather than a complete behavior definition.

## Plan caching

Plan caching reuses previously computed planning results. ABC uses a narrower, short-lived cache: the cached action branches belong to one plan bundle and are constrained by `valid_if` and expiration conditions. ABC does not assume that plans can be reused safely across tasks, sessions, or substantially changed world states.

## Event-triggered replanning

Event-triggered replanning requests a new plan when observations indicate that the current plan is no longer suitable. ABC first checks whether a known state change matches a valid cached trigger. It requests replanning when the plan bundle or cached action branch is invalid or expired, the change is unknown or unmatched, or a high-risk `replan_if` condition holds.

## Safety fallback / external fallback path

In this proposal, safety fallback refers to an external fallback path used before or instead of continued task execution in a high-risk situation. ABC assumes such a path may exist, but does not design it and does not provide a safety guarantee. A cache hit must not override external constraints, action validation, or risk controls.

## World models

World models or belief states can help a planner describe likely changes and generate useful action branches. ABC only consumes a `world_state_summary`; it does not create, update, or validate a world model. Poor state information can therefore produce incorrect triggers, stale cached action branches, or inappropriate actions.
