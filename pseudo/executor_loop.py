"""Conditional Instruction Cache (CIC) executor-loop pseudocode.

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
                is_expired(instruction_branch, plan_bundle_loaded_at_ms)
                for instruction_branch in plan_bundle["cached_instruction_branches"]
            ):
                planner.request_replanning(
                    observation, reason="conditional instruction cache expired"
                )
                return

            instruction_branch = arbiter.highest_priority_match(
                plan_bundle["cached_instruction_branches"], observation
            )

            if instruction_branch is None:
                if fast_monitor.relevant_event_detected(observation):
                    planner.request_replanning(observation, reason="unknown event")
                    return
                continue

            if arbiter.valid_if_holds(instruction_branch["valid_if"], observation):
                executor.execute(instruction_branch["instruction"])
            else:
                executor.execute(instruction_branch["fallback"])
                planner.request_replanning(
                    observation, reason="cached instruction branch invalid"
                )
                return


def is_expired(instruction_branch, plan_bundle_loaded_at_ms):
    age_ms = monotonic_ms() - plan_bundle_loaded_at_ms
    return age_ms >= instruction_branch["expire_after_ms"]


# Placeholder interfaces used by the pseudocode:
# - load_plan_bundle(path)
# - monotonic_ms()
# - executor.execute(instruction), executor.step_is_active()
# - fast_monitor.observe()
# - fast_monitor.relevant_event_detected(observation)
# - risk_rules.detect_unknown_high_risk_event(observation)
# - external_fallback.enter_fallback_state(observation)
# - matches_replan_if(observation, conditions)
# - arbiter.highest_priority_match(entries, observation)
# - arbiter.valid_if_holds(condition, observation)
# - planner.request_replanning(observation, reason)
