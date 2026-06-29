# Conditional Instruction Cache

[简体中文说明](README.zh-CN.md)

Conditional Instruction Cache (CIC) is a lightweight design pattern for agents that interact with changing environments. It pre-caches condition-bound instructions during execution so the agent can respond to expected state changes without waiting for a model call every time.

Examples of the situation CIC is meant to discuss:

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

> Can the agent prepare a few likely conditional responses while it is still executing the current step?

Conditional Instruction Cache (CIC) describes this bounded execution pattern:

```text
while acting -> prepare a few conditional instructions -> state changes -> match cached instruction branch -> act or replan
```

CIC stores a short `plan bundle` with a main path and a small number of `cached_instruction_branches`. Each branch has a `condition`, `trigger`, instruction, `valid_if`, expiration time, and fallback.

If an environmental change matches a branch, the system can try the cached instruction. If the cache is invalid, the change is unknown, or the situation is high-risk, it should reject the cache and use an `external fallback path` or request replanning.

This repository is still a design note / schema proposal. It is not a new planning algorithm, a complete agent framework, a real-time system, or a safety solution. It does not claim real-robot readiness or measured performance improvements.

## Quick Start

```bash
pip install -r requirements.txt
python demo/run_demo.py
python demo/run_demo.py examples/robotic_open_drawer.json
python -m unittest discover tests
```

The demo replays simulated events only. It does not control a robot or browser, call an API, read office files, or send email.

## What this is

CIC is a lightweight design note / schema proposal for describing one execution pattern that may reduce synchronous decision waiting after environmental changes.

This repository contains:

- a `plan bundle` JSON Schema;
- illustrative embodied-agent, browser-agent, and office-automation-agent examples;
- a minimal demo that replays simulated events; and
- short documents relating CIC to asynchronous planning, contingency planning, behavior trees, plan caching, event-triggered replanning, and world models.

## What this is not

CIC is not:

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

An agent may use a synchronous loop when the environment changes: observe an event, ask a planner or large model what to do, wait for a response, and only then act. For a small set of foreseeable events, some of that waiting may be avoided by preparing bounded responses in advance.

CIC focuses on the waiting that occurs *after* an environmental change. It does not make planning or model inference faster.

## Core Idea

A plan bundle contains:

- a short main plan;
- a small number of cached instruction branches, two to four in this schema;
- a `condition`, `trigger`, instruction, `valid_if`, expiration time, and fallback for each branch; and
- `replan_if` conditions that mark the plan bundle as invalid, unknown, or high-risk.

During execution, a monitor matches observed changes against cached triggers. A matching instruction may be used only while its `valid_if` and expiration constraints hold. CIC requests replanning when the plan bundle is invalid or expired, a change is unknown or unmatched, or a high-risk condition is observed. A safety fallback (an external fallback path) should be considered before replanning for high-risk conditions.

CIC is not limited to exception recovery. A branch may describe an expected object movement, page transition, API status, file-state change, user-input change, or other ordinary workflow condition. High-risk exceptions are one possible use case, not the defining use case.

## Repository Structure

- `docs/`: concept, architecture, limitations, related ideas, and scenarios.
- `schemas/`: JSON Schema for a CIC `plan bundle`.
- `examples/`: illustrative embodied-agent, browser-agent, and office-automation-agent plan bundles.
- `demo/`: simulated event replay for the CIC execution pattern.
- `tests/`: schema and demo checks using `unittest`.

For concrete JSON, start with [examples/robotic_pick_cup.json](examples/robotic_pick_cup.json) and [schemas/plan_bundle.schema.json](schemas/plan_bundle.schema.json).

## What This Does Not Solve

CIC does not provide world modeling, perception, low-level control, safety guarantees, or accurate probability estimation. It also does not solve API reliability, file availability, user intent disambiguation, or permission handling. It assumes that surrounding components can supply state estimates, detect events, execute instructions, and apply their own safety constraints or risk controls.

A cached instruction branch can be stale, incorrectly triggered, or inappropriate for the current state. Any practical experiment would need independent safety mechanisms and conservative rules for rejecting cached instructions.

## Status

This repository is a concept for open discussion. Its examples cover embodied-agent, browser-agent, and office-automation-agent tasks. The schema, examples, demo, and pseudocode are illustrative and are not validated for deployment or real-world control.
