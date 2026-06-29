# Limitations and Non-Goals

Action Branch Cache (ABC) is a narrow design pattern / schema proposal. It only describes how a short plan bundle might hold and match a small number of cached action branches. It does not solve the following problems.

## World Modeling

ABC does not construct, update, or validate a world model or belief state. Incorrect state summaries can produce irrelevant plans and action branches.

## Perception

ABC does not detect objects, people, browser elements, motion, or hazards. It assumes that an external perception or observation layer provides events and state updates.

## Safety Guarantees

A cached action branch is not evidence or proof of safety. ABC provides no formal, statistical, or operational safety guarantee. An external fallback path, external constraints or risk controls, and fail-stop or review mechanisms remain necessary.

## Low-Level Control

ABC represents actions at an abstract level. It does not generate motor commands, trajectories, browser automation primitives, or feedback-control policies.

## Accurate Probability Estimation

ABC does not estimate event probabilities accurately or prove that selected action branches are optimal. Ranking can be heuristic and may omit an important condition.

## External Services, Files, Intent, and Permissions

ABC does not solve API reliability, file availability, user intent disambiguation, or permission handling. Those concerns remain the responsibility of surrounding systems and user-facing workflows.

## Cache Failure Modes

A cached action branch can expire as the environment changes. Its `valid_if` condition may be incomplete, its `trigger` may be ambiguous, and monitoring may be delayed or incorrect. The plan bundle therefore needs explicit expiration and `replan_if` conditions.

ABC reduces decision-execution latency only when cached branches are valid and correctly matched.

An incorrect cached action can produce an incorrect response sooner than synchronous replanning would. Reduced decision-to-action latency is not inherently beneficial when the cached action branch is wrong. Conservative arbitration, independent action validation, an external fallback path, and replanning for invalid, unknown, or high-risk situations remain necessary for any practical experiment.
