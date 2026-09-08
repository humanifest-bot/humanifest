from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
from pathlib import Path
import tempfile
import unittest

from humanifest.cli import main
from tests.test_models import opportunity


class CliTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def run_cli(self, *args):
        stdout, stderr = StringIO(), StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = main(list(args))
        return status, stdout.getvalue(), stderr.getvalue()

    def write_record(self, name, record):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(record), encoding="utf-8")
        return path

    def seed_portfolio(self):
        project = {
            "id": "sample-project", "name": "Sample", "repository": "https://example.test/repo",
            "homepage": "https://example.test", "license": "MIT", "humanitarian_domain": "Health",
            "maintenance": {}, "contribution": {}, "impact_evidence": [],
            "sources": opportunity()["sources"],
        }
        self.write_record("portfolio/projects/sample.json", project)
        self.write_record("portfolio/opportunities/sample.json", opportunity())

    def test_missing_root_fails_instead_of_reporting_success(self):
        for command in ["validate", "report"]:
            status, out, err = self.run_cli(command, "--root", str(self.root / "missing"))
            self.assertEqual(status, 1)
            self.assertEqual(out, "")
            self.assertIn("required record directory is missing", err)

    def test_valid_portfolio_and_json_score(self):
        self.seed_portfolio()
        for command in ["validate", "report"]:
            status, out, err = self.run_cli(command, "--root", str(self.root))
            self.assertEqual((status, err), (0, ""))
            self.assertTrue(out)
        status, out, err = self.run_cli("score", str(self.root / "portfolio/opportunities/sample.json"))
        self.assertEqual((status, err), (0, ""))
        self.assertEqual(json.loads(out)["score"], 2.7)

    def test_bad_inputs_have_diagnostics_without_tracebacks(self):
        for content in ["{", "[]", '{"id": "a", "id": "b"}', '{"score": NaN}', '{}']:
            path = self.root / "bad.json"
            path.write_text(content)
            for command in ["score", "brief", "handoff"]:
                args = [command, str(path)]
                if command == "handoff":
                    args.extend(["--target", "codex"])
                with self.subTest(content=content, command=command):
                    status, out, err = self.run_cli(*args)
                    self.assertEqual(status, 1)
                    self.assertEqual(out, "")
                    self.assertTrue(err)
                    self.assertNotIn("Traceback", err)
        status, out, err = self.run_cli("brief", str(self.root / "missing.json"))
        self.assertEqual((status, out), (1, ""))
        self.assertIn("missing.json", err)

    def test_portfolio_collects_errors_and_blocks_report(self):
        self.seed_portfolio()
        bad = opportunity()
        bad["project_id"] = "missing-project"
        self.write_record("portfolio/opportunities/duplicate.json", bad)
        (self.root / "portfolio/projects/bad.json").write_text("{")
        for command in ["validate", "report"]:
            status, out, err = self.run_cli(command, "--root", str(self.root))
            self.assertEqual((status, out), (1, ""))
            self.assertIn("bad.json", err)
            self.assertIn("duplicate opportunities id", err)
            self.assertIn("unknown project: missing-project", err)

    def test_duplicate_project_ids_are_rejected(self):
        self.seed_portfolio()
        project = json.loads((self.root / "portfolio/projects/sample.json").read_text())
        self.write_record("portfolio/projects/duplicate.json", project)
        status, _, err = self.run_cli("validate", "--root", str(self.root))
        self.assertEqual(status, 1)
        self.assertIn("duplicate projects id", err)

    def test_invalid_advanced_state_cannot_produce_a_handoff(self):
        record = opportunity()
        record["pipeline_state"] = "BUILDING"
        record["gates"]["maintainer_interest_confirmed"]["passed"] = False
        path = self.write_record("blocked.json", record)
        status, out, err = self.run_cli("handoff", str(path), "--target", "codex")
        self.assertEqual((status, out), (1, ""))
        self.assertIn("requires every hard gate", err)
