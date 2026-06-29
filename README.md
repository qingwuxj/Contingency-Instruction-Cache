# Action Branch Cache

[简体中文说明](README.zh-CN.md)

Action Branch Cache is a lightweight design pattern for agents operating in changing environments. The core idea is to precompute a small set of condition-bound action branches while the agent is executing its current plan, so that when an expected state change occurs, the agent can switch to a cached branch instead of performing a full decision cycle from scratch.

Examples of the situation ABC is meant to discuss:

- a robot arm is reaching for a cup, but the cup shifts;
- a browser agent is filling a form, but a modal blocks the submit button;
- an office automation agent calls an API, but the request fails;
- a required spreadsheet is missing or unreadable; or
- user input conflicts with expected values or workflow assumptions.

In each case, waiting begins when the environment changes and the agent asks a model, for the first time, what to do next. A common synchronous flow is:

```text
event happens -> ask model -> wait -> decide -> act
```

The core question is:

> Can the agent prepare a few likely action branches while it is still executing the current step?

Action Branch Cache (ABC) describes this bounded execution pattern:

```text
while acting -> precompute a few action branches -> state changes -> match cached action branch -> validate and switch
```

ABC stores a short `plan bundle` with a main path and a small number of `cached_action_branches`. Each branch has a `condition`, `trigger`, action, `valid_if`, expiration time, and fallback.

If an environmental change matches a branch, the system can consider switching to its cached action. If the cache is invalid, the change is unknown, or the situation is high-risk, it should reject the cache and use an `external fallback path` or request replanning.

This repository is an idea-first design pattern / schema proposal. It is not a new planning algorithm, a complete agent framework, a real-time system, or a safety solution. It does not claim real-robot readiness or measured performance improvements.

## Quick Start

```bash
pip install -r requirements.txt
python demo/run_demo.py
python demo/run_demo.py examples/robotic_open_drawer.json
python -m unittest discover tests
```

The demo replays simulated events only. It does not control a robot or browser, call an API, read office files, or send email.

## What this is

ABC is a lightweight design note / schema proposal for describing one execution pattern that may reduce agent decision-to-action latency after environmental changes.

This repository contains:

- a `plan bundle` JSON Schema;
- illustrative embodied-agent, browser-agent, and office-automation-agent examples;
- a minimal demo that replays simulated events; and
- short documents relating ABC to asynchronous planning, contingency planning, behavior trees, plan caching, event-triggered replanning, and world models.

## What this is not

ABC is not:

- a new planning algorithm;
- a complete agent framework;
- a real-time robotics system;
- a safety solution;
- a world model; or
- a perception or low-level control module.

## Docs and Examples

- Concept and boundaries: [Concept](docs/concept.md), [Architecture](docs/architecture.md), [Limitations](docs/limitations.md)
- Context: [Related Ideas](docs/related_ideas.md), [Scenarios](docs/scenarios.md)
- Examples: [robotic_pick_cup](examples/robotic_pick_cup.json), [robotic_open_drawer](examples/robotic_open_drawer.json), [browser_agent_form](examples/browser_agent_form.json), [browser_checkout_recovery](examples/browser_checkout_recovery.json), [office_automation_agent](examples/office_automation_agent.json)
- Schema and demo: [plan_bundle.schema.json](schemas/plan_bundle.schema.json), [run_demo.py](demo/run_demo.py)

## Motivation

An agent may use a synchronous loop when the environment changes: update state, ask a planner or model what to do, form a new action branch, validate it, and only then act. For a small set of foreseeable changes, part of this decision path may be prepared in advance.

ABC focuses on decision-to-action latency after an environmental change. Model waiting can be one part of that latency, but it is not the whole problem. ABC does not make planning, inference, validation, or execution inherently faster; it only proposes reusing a bounded branch that was prepared earlier.

## Core Idea

A plan bundle contains:

- a short main plan;
- a small number of cached action branches, two to four in this schema;
- a `condition`, `trigger`, action, `valid_if`, expiration time, and fallback for each branch; and
- `replan_if` conditions that mark the plan bundle as invalid, unknown, or high-risk.

During execution, a monitor matches observed changes against cached triggers. A matching branch may be considered only while its `valid_if` and expiration constraints hold, and external action validation still applies. ABC requests replanning when the plan bundle is invalid or expired, a change is unknown or unmatched, or a high-risk condition is observed. A safety fallback (an external fallback path) should be considered before replanning for high-risk conditions.

ABC is not limited to exception recovery. A branch may describe an expected object movement, page transition, API status, file-state change, user-input change, or other ordinary workflow condition. High-risk exceptions are one possible use case, not the defining use case.

## Repository Structure

- `docs/`: concept, architecture, limitations, related ideas, and scenarios.
- `schemas/`: JSON Schema for an ABC `plan bundle`.
- `examples/`: illustrative embodied-agent, browser-agent, and office-automation-agent plan bundles.
- `demo/`: simulated event replay for the ABC execution pattern.
- `tests/`: schema and demo checks using `unittest`.

For concrete JSON, start with [examples/robotic_pick_cup.json](examples/robotic_pick_cup.json) and [schemas/plan_bundle.schema.json](schemas/plan_bundle.schema.json).

## What This Does Not Solve

ABC does not provide world modeling, perception, low-level control, safety guarantees, or accurate probability estimation. It also does not solve API reliability, file availability, user intent disambiguation, or permission handling. It assumes that surrounding components can supply state estimates, detect changes, validate actions, execute them, and apply their own safety constraints or risk controls.

A cached action branch can be stale, incorrectly triggered, or inappropriate for the current state. Any practical experiment would need independent safety mechanisms and conservative rules for rejecting cached branches.

## Status

This repository is a concept for open discussion. Its examples cover embodied-agent, browser-agent, and office-automation-agent tasks. The schema, examples, demo, and pseudocode are illustrative and are not validated for deployment or real-world control.
