# Limitations and Non-Goals

Conditional Instruction Cache (CIC) is a narrow design note / schema proposal. It only describes how a short plan bundle might hold and match a small number of cached instruction branches. It does not solve the following problems.

## World Modeling

CIC does not construct, update, or validate a world model or belief state. Incorrect state summaries can produce irrelevant plans and conditional branches.

## Perception

CIC does not detect objects, people, browser elements, motion, or hazards. It assumes that an external perception or observation layer provides events and state updates.

## Safety Guarantees

A cached instruction is not evidence or proof of safety. CIC provides no formal, statistical, or operational safety guarantee. An external fallback path, external constraints or risk controls, and fail-stop or review mechanisms remain necessary.

## Low-Level Control

CIC represents instructions at an abstract level. It does not generate motor commands, trajectories, browser automation primitives, or feedback-control policies.

## Accurate Probability Estimation

CIC does not estimate event probabilities accurately or prove that selected instruction branches are optimal. Ranking can be heuristic and may omit an important condition.

## External Services, Files, Intent, and Permissions

CIC does not solve API reliability, file availability, user intent disambiguation, or permission handling. Those concerns remain the responsibility of surrounding systems and user-facing workflows.

## Cache Failure Modes

A cached instruction branch can expire as the environment changes. Its `valid_if` condition may be incomplete, its `trigger` may be ambiguous, and monitoring may be delayed or incorrect. The plan bundle therefore needs explicit expiration and `replan_if` conditions.

An incorrect cached instruction can produce an incorrect response sooner than synchronous replanning would. Reduced waiting is not inherently beneficial when the cached instruction branch is wrong. Conservative arbitration, an external fallback path, and replanning for invalid, unknown, or high-risk situations remain necessary for any practical experiment.
