"""Replay a simulated event stream to illustrate the ABC execution pattern."""

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError, ValidationError


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN_BUNDLE_PATH = ROOT / "examples" / "robotic_pick_cup.json"
EVENTS_PATH = ROOT / "demo" / "simulated_events.json"
SCHEMA_PATH = ROOT / "schemas" / "plan_bundle.schema.json"


def load_json(path):
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def resolve_plan_bundle_path(argument):
    path = Path(argument)
    if path.is_absolute():
        return path
    return ROOT / path


def print_header(plan_bundle):
    print("=" * 64)
    print("ABC LIGHTWEIGHT DEMO")
    print("=" * 64)
    print(f"TASK: {plan_bundle['task']}")
    print(f"BUNDLE MODE: {plan_bundle['mode']}")
    print(
        "MODE: simulated event replay; no robot, browser, or office "
        "application is controlled"
    )


def run_bootstrap_demo(plan_bundle, events):
    bootstrap_action = plan_bundle["bootstrap_action"]
    async_request = plan_bundle["async_branch_request"]

    print(f"BOOTSTRAP ACTION: {bootstrap_action['description']}")
    print(f"BOOTSTRAP COMMAND: {bootstrap_action['command']}")
    print(
        "BOOTSTRAP ARGS: "
        f"{json.dumps(bootstrap_action['args'], sort_keys=True)}"
    )
    print(f"BOOTSTRAP VALID IF: {bootstrap_action['valid_if']}")
    print(
        "BOOTSTRAP EXPIRY: "
        f"expire_after_ms={bootstrap_action['expire_after_ms']}"
    )
    print(
        "BOOTSTRAP REQUIRES VALIDATION: "
        f"{bootstrap_action['requires_validation']}"
    )
    print(f"ASYNC BRANCH REQUEST: {json.dumps(async_request, sort_keys=True)}")
    print(
        "NOTE: no hydrated branch cache is available in this example; "
        "unknown or high-risk events require fallback or replanning."
    )

    for position, event in enumerate(events, start=1):
        event_type = event["type"]
        risk = event["risk"]

        print("\n" + "-" * 64)
        print(f"EVENT {position}/{len(events)}: {event_type} (risk={risk})")
        print(f"DESCRIPTION: {event['description']}")
        print(f"SIGNALS: {json.dumps(event['signals'], sort_keys=True)}")

        if event_type == "normal_tick":
            print("BOOTSTRAP ACTION: continue only while externally validated")
            continue

        print(f"NO HYDRATED CACHE: {event_type}")
        if risk == "high":
            print("EXTERNAL FALLBACK PATH: pause simulated bootstrap execution")
        print("REQUEST REPLANNING: no hydrated cache")


def run_hydrated_demo(plan_bundle, events):
    branch_matches = {}
    for branch in plan_bundle["cached_action_branches"]:
        branch_matches[branch["condition"]] = branch
        branch_matches[branch["trigger"]["detector"]] = branch

    next_main_step = 0
    print("MATCHING: event type to branch condition or detector only")
    print(
        "NOTE: trigger rules are illustrative. A real system needs a monitor "
        "adapter that evaluates detector signals and rule semantics."
    )

    for position, event in enumerate(events, start=1):
        event_type = event["type"]
        risk = event["risk"]

        print("\n" + "-" * 64)
        print(f"EVENT {position}/{len(events)}: {event_type} (risk={risk})")
        print(f"DESCRIPTION: {event['description']}")
        print(f"SIGNALS: {json.dumps(event['signals'], sort_keys=True)}")

        if event_type == "normal_tick":
            if next_main_step < len(plan_bundle["main_plan"]):
                step = plan_bundle["main_plan"][next_main_step]
                print(f"MAIN PLAN STEP {step['step']}: {step['instruction']}")
                next_main_step += 1
            else:
                print("MAIN PLAN: no remaining step in this demonstration")
            continue

        # This demo does not parse trigger.rule. It only matches the simulated
        # event type to a stable condition or detector identifier.
        cached_action_branch = branch_matches.get(event_type)
        if cached_action_branch is not None:
            if "expire_after_ms" not in cached_action_branch:
                print("CACHE INVALID: expire_after_ms is missing")
                print("REQUEST REPLANNING: cached action branch is invalid")
                continue

            trigger = cached_action_branch["trigger"]
            action = cached_action_branch["action"]
            print(
                "MATCHED CACHED ACTION BRANCH: "
                f"{cached_action_branch['condition']}"
            )
            print(f"TRIGGER DETECTOR: {trigger['detector']}")
            print(f"TRIGGER RULE (illustrative): {trigger['rule']}")
            print(
                "CACHE EXPIRY METADATA: "
                f"expire_after_ms={cached_action_branch['expire_after_ms']}"
            )
            print(f"CACHED ACTION: {action['description']}")
            print(f"SELECTED EXECUTOR: {action['executor']}")
            print(f"SELECTED COMMAND: {action['command']}")
            print(f"COMMAND ARGS: {json.dumps(action['args'], sort_keys=True)}")
            print(f"REQUIRES VALIDATION: {action['requires_validation']}")
            continue

        if risk == "high":
            print(f"NO CACHE HIT: {event_type}")
            print("EXTERNAL FALLBACK PATH: pause simulated execution")
            print("REQUEST REPLANNING: unknown high-risk event")
        else:
            print("NO CACHE HIT: continue or request background replanning")


def run_demo(plan_bundle, events):
    print_header(plan_bundle)

    if plan_bundle["mode"] == "bootstrap_only":
        run_bootstrap_demo(plan_bundle, events)
    else:
        run_hydrated_demo(plan_bundle, events)

    print("\n" + "=" * 64)
    print("DEMO COMPLETE: simulated events exhausted")
    print("=" * 64)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Replay simulated events against an ABC plan bundle."
    )
    parser.add_argument(
        "plan_bundle",
        nargs="?",
        default=str(DEFAULT_PLAN_BUNDLE_PATH),
        help=(
            "Path to a plan bundle JSON file. Defaults to "
            "examples/robotic_pick_cup.json."
        ),
    )
    args = parser.parse_args(argv)
    plan_bundle_path = resolve_plan_bundle_path(args.plan_bundle)

    try:
        schema = load_json(SCHEMA_PATH)
        plan_bundle = load_json(plan_bundle_path)
        events = load_json(EVENTS_PATH)

        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(plan_bundle)
        print(f"PLAN BUNDLE FILE: {plan_bundle_path.name}")
        print("PLAN BUNDLE VALIDATION: passed")
        run_demo(plan_bundle, events)
    except (OSError, json.JSONDecodeError, SchemaError, ValidationError) as error:
        print(f"DEMO ERROR: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
