# Progressive ABC

Action Branch Cache (ABC) does not require a complete `main_plan + cached_action_branches` bundle before the agent starts every task. In some settings, generating the full bundle up front may increase the first decision latency. Progressive ABC is an optional pattern for starting with a small, low-risk action while the rest of the bundle is hydrated asynchronously.

This document is conceptual. It does not add a runtime scheduler, background planner, executor, monitor, or provider call path.

## Motivation

A fully hydrated plan bundle can be useful when the agent already has enough context to prepare the main path and a few likely branches. But sometimes the first useful step is simple while the surrounding branches still need more planning time.

For example, an embodied agent might first move slowly to an observation pose, a browser agent might first open a page and inspect the DOM state, or an office automation agent might first locate a non-sensitive working directory. These bootstrap actions can be useful because they give the system a low-risk starting point while branch hydration happens in the background.

Progressive ABC addresses a narrow concern: precomputing all branches up front can delay the first action. It does not claim real-time behavior, better planning quality, or safety guarantees.

## Phase 1: Generate a bootstrap action

The planner may first return a `bootstrap_only` bundle. This bundle contains a `bootstrap_action` and an `async_branch_request`, but not a hydrated `main_plan` or `cached_action_branches`.

The bootstrap action must be:

- low-risk;
- interruptible;
- short-lived;
- externally validated; and
- bounded by `valid_if` and `expire_after_ms`.

The bootstrap action is not a shortcut around action validation. It is only a small initial action that surrounding systems may reject or pause.

## Phase 2: Execute while hydrating branches

While the bootstrap action is active, an asynchronous branch request can ask for:

- a short continuation horizon for the main plan;
- a small number of cached action branches; and
- a branch-selection policy for likely short-horizon changes.

If no hydrated cache is ready yet, unknown or high-risk events must go to the `external fallback path` or request replanning. The bootstrap bundle should not pretend that it can handle events it has not prepared for.

## Phase 3: Switch to a hydrated bundle

When the continuation and cached branches become available, the system can switch from `bootstrap_only` to `hydrated_bundle`.

A hydrated bundle contains:

- a short `main_plan`;
- `cached_action_branches`;
- structured `trigger` objects with detector-oriented fields; and
- structured `action` objects with executor-oriented fields.

The switch should still be explicit. The hydrated bundle must be validated, its branches must remain current, and external action validation must still apply.

## Structured triggers and actions

Progressive ABC does not make natural-language descriptions executable. Human-readable descriptions are useful for inspection, but real systems need adapter fields.

In the schema:

- `trigger.description` explains the condition for humans;
- `trigger.detector`, `trigger.signals`, `trigger.rule`, and `trigger.debounce_ms` are intended for monitor integration;
- `action.description` explains the response for humans; and
- `action.command`, `action.args`, `action.executor`, and `action.requires_validation` are intended for executor integration.

The demo only matches simulated event names to branch identifiers. It does not parse rules or execute commands.

## Boundary

Progressive ABC is optional. It is only a mitigation for first-decision latency when full branch generation would be too slow or unnecessary before a first bounded action.

It does not replace the core ABC boundary:

```text
observe state -> match structured trigger -> validate branch -> execute mapped action or fallback -> replan when invalid, unknown, or high-risk
```

If no hydrated branch is available, or if the available branch is expired, invalid, unknown, or high-risk, the system should use an `external fallback path` or request replanning.
