"""Action Branch Cache (ABC) executor-loop pseudocode.

This file illustrates control flow only. The referenced interfaces are placeholders;
it does not connect to a robot, browser, office application, model, or safety system.
"""


def run(plan_bundle_path):
    plan_bundle = load_plan_bundle(plan_bundle_path)
    plan_bundle_loaded_at_ms = monotonic_ms()

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

            if arbiter.valid_if_holds(action_branch["valid_if"], observation):
                executor.execute(action_branch["action"])
            else:
                executor.execute(action_branch["fallback"])
                planner.request_replanning(
                    observation, reason="cached action branch invalid"
                )
                return


def is_expired(action_branch, plan_bundle_loaded_at_ms):
    age_ms = monotonic_ms() - plan_bundle_loaded_at_ms
    return age_ms >= action_branch["expire_after_ms"]


# Placeholder interfaces used by the pseudocode:
# - load_plan_bundle(path)
# - monotonic_ms()
# - executor.execute(action_or_step), executor.step_is_active()
# - fast_monitor.observe()
# - fast_monitor.relevant_event_detected(observation)
# - risk_rules.detect_unknown_high_risk_event(observation)
# - external_fallback.enter_fallback_state(observation)
# - matches_replan_if(observation, conditions)
# - arbiter.highest_priority_match(entries, observation)
# - arbiter.valid_if_holds(condition, observation)
# - planner.request_replanning(observation, reason)
