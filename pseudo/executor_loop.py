"""Action Branch Cache (ABC) executor-loop pseudocode.

This file illustrates control flow only. The referenced interfaces are placeholders;
it does not connect to a robot, browser, office application, model, or safety system.
"""


def run(plan_bundle_path):
    plan_bundle = load_plan_bundle(plan_bundle_path)
    plan_bundle_loaded_at_ms = monotonic_ms()

    if plan_bundle["mode"] == "bootstrap_only":
        run_bootstrap_only(plan_bundle, plan_bundle_loaded_at_ms)
        return

    run_hydrated_bundle(plan_bundle, plan_bundle_loaded_at_ms)


def run_bootstrap_only(plan_bundle, plan_bundle_loaded_at_ms):
    bootstrap_action = plan_bundle["bootstrap_action"]

    if is_expired(bootstrap_action, plan_bundle_loaded_at_ms):
        planner.request_replanning(None, reason="bootstrap action expired")
        return

    if not external_action_validator.allows(bootstrap_action):
        external_fallback.enter_fallback_state(None)
        planner.request_replanning(None, reason="bootstrap action rejected")
        return

    executor.execute_command(
        command=bootstrap_action["command"],
        args=bootstrap_action["args"],
    )
    planner.request_async_branch_hydration(plan_bundle["async_branch_request"])

    while executor.step_is_active():
        observation = fast_monitor.observe()

        if risk_rules.detect_unknown_high_risk_event(observation):
            external_fallback.enter_fallback_state(observation)
            planner.request_replanning(
                observation, reason="no hydrated cache for high-risk event"
            )
            return

        if is_expired(bootstrap_action, plan_bundle_loaded_at_ms):
            planner.request_replanning(observation, reason="bootstrap action expired")
            return

        hydrated_bundle = planner.poll_hydrated_bundle()
        if hydrated_bundle is not None:
            run_hydrated_bundle(hydrated_bundle, monotonic_ms())
            return


def run_hydrated_bundle(plan_bundle, plan_bundle_loaded_at_ms):
    for main_step in plan_bundle["main_plan"]:
        executor.execute(main_step["instruction"])

        while executor.step_is_active():
            observation = fast_monitor.observe()

            if risk_rules.detect_unknown_high_risk_event(observation):
                external_fallback.enter_fallback_state(observation)
                planner.request_replanning(observation, reason="unknown high-risk event")
                return

            if matches_replan_if(observation, plan_bundle["replan_if"]):
                planner.request_replanning(observation, reason="replan condition matched")
                return

            if any(
                is_expired(action_branch, plan_bundle_loaded_at_ms)
                for action_branch in plan_bundle["cached_action_branches"]
            ):
                planner.request_replanning(
                    observation, reason="action branch cache expired"
                )
                return

            action_branch = arbiter.highest_priority_match(
                plan_bundle["cached_action_branches"], observation
            )

            if action_branch is None:
                if fast_monitor.relevant_event_detected(observation):
                    planner.request_replanning(observation, reason="unknown event")
                    return
                continue

            if not arbiter.valid_if_holds(action_branch["valid_if"], observation):
                executor.execute_fallback(action_branch["fallback"])
                planner.request_replanning(
                    observation, reason="cached action branch invalid"
                )
                return

            action = action_branch["action"]
            if external_action_validator.allows(action):
                executor.execute_command(
                    command=action["command"],
                    args=action["args"],
                    executor=action["executor"],
                )
            else:
                executor.execute_fallback(action_branch["fallback"])
                planner.request_replanning(
                    observation, reason="cached action branch rejected"
                )
                return


def is_expired(action_branch, plan_bundle_loaded_at_ms):
    age_ms = monotonic_ms() - plan_bundle_loaded_at_ms
    return age_ms >= action_branch["expire_after_ms"]


# Placeholder interfaces used by the pseudocode:
# - load_plan_bundle(path)
# - monotonic_ms()
# - executor.execute(step_instruction), executor.step_is_active()
# - executor.execute_command(command, args, executor=None)
# - executor.execute_fallback(fallback_description)
# - fast_monitor.observe()
# - fast_monitor.relevant_event_detected(observation)
# - risk_rules.detect_unknown_high_risk_event(observation)
# - external_fallback.enter_fallback_state(observation)
# - matches_replan_if(observation, conditions)
# - arbiter.highest_priority_match(entries, observation)
# - arbiter.valid_if_holds(condition, observation)
# - external_action_validator.allows(action)
# - planner.request_async_branch_hydration(request)
# - planner.poll_hydrated_bundle()
# - planner.request_replanning(observation, reason)
