# Limitations and Non-Goals

Contingency Instruction Cache (CIC) is a narrow design note / schema proposal. It only describes how a short plan bundle might hold and match a small number of cached contingencies. It does not solve the following problems.

## World Modeling

CIC does not construct, update, or validate a world model or belief state. Incorrect state summaries can produce irrelevant plans and contingencies.

## Perception

CIC does not detect objects, people, browser elements, motion, or hazards. It assumes that an external perception or observation layer provides events and state updates.

## Safety Guarantees

A cached instruction is not evidence or proof of safety. CIC provides no formal, statistical, or operational safety guarantee. An external fallback path, external constraints or risk controls, and fail-stop or review mechanisms remain necessary.

## Low-Level Control

CIC represents instructions at an abstract level. It does not generate motor commands, trajectories, browser automation primitives, or feedback-control policies.

## Accurate Probability Estimation

CIC does not estimate event probabilities accurately or prove that selected contingencies are optimal. Ranking can be heuristic and may omit an important event.

## Cache Failure Modes

A cached contingency can expire as the environment changes. Its `valid_if` condition may be incomplete, its `trigger` may be ambiguous, and monitoring may be delayed or incorrect. The plan bundle therefore needs explicit expiration and `replan_if` conditions.

An incorrect cached instruction can produce an incorrect response sooner than synchronous replanning would. Reduced waiting is not inherently beneficial when the cached contingency is wrong. Conservative arbitration, an external fallback path, and replanning for invalid, unknown, or high-risk situations remain necessary for any practical experiment.
