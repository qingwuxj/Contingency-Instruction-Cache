import json
import subprocess
import sys
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "plan_bundle.schema.json"
EXAMPLES_DIR = ROOT / "examples"


def load_json(path):
    with path.open(encoding="utf-8") as file:
        return json.load(file)


class SchemaExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schema = load_json(SCHEMA_PATH)
        Draft202012Validator.check_schema(schema)
        cls.validator = Draft202012Validator(schema)

    def test_all_examples_match_schema(self):
        example_paths = sorted(EXAMPLES_DIR.glob("*.json"))
        self.assertTrue(example_paths, "No JSON examples were found.")

        for example_path in example_paths:
            with self.subTest(example=example_path.name):
                self.validator.validate(load_json(example_path))

    def test_demo_exercises_cache_and_fallback_paths(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "demo" / "run_demo.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("MAIN PLAN STEP 1: Approach the cup.", result.stdout)
        self.assertIn("MATCHED CACHED CONTINGENCY: cup_shifted", result.stdout)
        self.assertIn("CACHED INSTRUCTION:", result.stdout)
        self.assertIn("EXTERNAL FALLBACK PATH:", result.stdout)
        self.assertIn("REQUEST REPLANNING", result.stdout)
        self.assertIn(
            "MATCHED CACHED CONTINGENCY: human_hand_near_workspace",
            result.stdout,
        )

    def test_demo_accepts_a_plan_bundle_path(self):
        example_path = Path("examples") / "robotic_open_drawer.json"
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "demo" / "run_demo.py"),
                str(example_path),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PLAN BUNDLE FILE: robotic_open_drawer.json", result.stdout)


if __name__ == "__main__":
    unittest.main()
