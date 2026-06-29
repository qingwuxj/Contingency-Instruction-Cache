# Scenarios

These scenarios are illustrative only. They show how a CIC plan bundle might describe a short main plan, a small number of cached contingencies, and conditions for replanning. They do not implement robot control, browser control, office automation, perception, safety guarantees, or production execution.

## robotic_open_drawer

### Why this scenario is useful

Opening a drawer has a clear expected path, but it also has foreseeable interruptions: the handle pose may be uncertain, the drawer may not move as expected, force readings may exceed a conservative threshold, or a person may enter the workspace. This makes it a compact example for separating a main plan from cached contingencies.

The scenario is still only a schema example. The CIC plan bundle does not estimate handle pose, measure force, identify hands, or decide that any motion is acceptable.

### Main plan

The main plan is intentionally short:

1. locate drawer handle;
2. approach handle;
3. align gripper;
4. pull drawer; and
5. verify drawer opened.

These steps assume some external controller and state estimator exist outside CIC.

### Cached contingencies

The cached contingencies cover a few likely deviations:

- `handle_pose_uncertain`: pause and request a refreshed handle estimate before continuing;
- `drawer_stuck`: pause the pull and avoid increasing force from a cached instruction;
- `excessive_force_detected`: stop the pull request and route to the external risk-control path; and
- `human_hand_near_workspace`: pause execution and route to the external fallback path.

High-risk cases are phrased conservatively. The cached instruction does not claim to fully handle the condition; it routes the example toward an external fallback path and replanning.

### When replanning is needed

Replanning is needed when the drawer handle is no longer visible, the drawer geometry no longer matches the state summary, an unknown high-risk event appears, or no cached contingency remains valid.

### What the example intentionally omits

The example omits world modeling, handle detection, hand detection, force control, motion planning, collision checking, and risk validation. It only illustrates how a plan bundle could carry short-lived contingency instructions.

## browser_checkout_recovery

### Why this scenario is useful

A checkout flow has a predictable sequence and several common page-level interruptions: a login session may expire, a button may be disabled, an address may fail validation, or a modal may block the page. CIC can also be illustrated with browser-agent workflows.

The scenario is written as an illustrative browser-agent workflow. It intentionally stops before final confirmation and does not execute payment or submit an order.

### Main plan

The main plan is:

1. open checkout page;
2. verify cart;
3. fill shipping details;
4. choose shipping method; and
5. prepare final confirmation, then stop before submitting the order.

The last step is bounded to avoid implying real payment execution.

### Cached contingencies

The cached contingencies cover:

- `login_session_expired`: stop checkout progression and request approved session recovery;
- `payment_button_disabled`: avoid clicking the disabled control and inspect required-field indicators;
- `address_validation_error`: pause progression and surface the validation message; and
- `modal_popup_blocks_page`: close only a recognized non-critical modal, then verify state.

These instructions are deliberately narrow. They do not authorize payment, consent, or security decisions.

### When replanning is needed

Replanning is needed if the cart total changes unexpectedly, the page origin changes, a payment or consent prompt appears, final order confirmation would be required, or an unknown high-risk event is observed.

### What the example intentionally omits

The example omits browser automation, authentication handling, data validation policy, purchase authorization, and security guarantees. It only illustrates event matching and conservative replanning boundaries inside a plan bundle.

## Office automation agents

### Why this scenario is useful

An office automation workflow may have a predictable sequence while still depending on external services, files, and user instructions that can change or conflict. The [office automation example](../examples/office_automation_agent.json) uses report preparation and draft-email creation to show how a plan bundle can represent a few foreseeable interruptions without performing the work itself.

### Main plan

The illustrative main plan is:

1. locate the spreadsheet;
2. read the required fields;
3. generate a report summary; and
4. create a draft email without sending it.

### Cached contingencies

These cached contingencies are structured fallback instructions, not final solutions:

- `api_failure`: retry with bounded backoff, use cached data only when it is still valid, otherwise pause and request replanning;
- `missing_file`: search the expected non-sensitive working directory, ask the user for a replacement file, and stop before generating the report; and
- `conflicting_user_input`: pause, summarize the conflict, and request clarification before continuing.

The instructions do not establish that a retry is appropriate, that a replacement file is trustworthy, or that one conflicting input should override another. Those judgments remain outside CIC.

### When replanning is needed

Replanning is needed when retries are exhausted, cached data is stale, the required file remains unavailable, user intent is ambiguous, permissions are missing, or no cached contingency remains applicable. An external fallback path may pause the workflow before replanning or user review.

### What the example intentionally omits

The example does not call an API, read a file, generate a real report, access an address book, or send an email. It also omits authentication, permission handling, data classification, recipient validation, and user-intent resolution.
