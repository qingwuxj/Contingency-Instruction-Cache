"""Replay a simulated event stream to illustrate the CIC execution pattern."""

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


def run_demo(plan_bundle, events):
    cached_instruction_branches = {
        item["condition"]: item
        for item in plan_bundle["cached_instruction_branches"]
    }
    next_main_step = 0

    print("=" * 64)
    print("CIC LIGHTWEIGHT DEMO")
    print("=" * 64)
    print(f"TASK: {plan_bundle['task']}")
    print(
        "MODE: simulated event replay; no robot, browser, or office "
        "application is controlled"
    )
    print("MATCHING: event type to branch condition only")
    print(
        "NOTE: a real system would use a fast monitor to evaluate each "
        "cached trigger."
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

        # This demo matches event types to branch condition identifiers only.
        # A real system would use a fast monitor to evaluate the cached trigger
        # against current observations.
        cached_instruction_branch = cached_instruction_branches.get(event_type)
        if cached_instruction_branch is not None:
            if "expire_after_ms" not in cached_instruction_branch:
                print("CACHE INVALID: expire_after_ms is missing")
                print("REQUEST REPLANNING: cached instruction branch is invalid")
                continue

            print(
                "MATCHED CACHED INSTRUCTION BRANCH: "
                f"{cached_instruction_branch['condition']}"
            )
            print(
                "CACHE EXPIRY METADATA: "
                f"expire_after_ms={cached_instruction_branch['expire_after_ms']}"
            )
            print(
                f"CACHED INSTRUCTION: {cached_instruction_branch['instruction']}"
            )
            continue

        if risk == "high":
            print(f"NO CACHE HIT: {event_type}")
            print("EXTERNAL FALLBACK PATH: pause simulated execution")
            print("REQUEST REPLANNING: unknown high-risk event")
        else:
            print("NO CACHE HIT: continue or request background replanning")

    print("\n" + "=" * 64)
    print("DEMO COMPLETE: simulated events exhausted")
    print("=" * 64)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Replay simulated events against a CIC plan bundle."
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
