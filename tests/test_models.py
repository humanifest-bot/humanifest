import unittest

from humanifest.models import (
    BUILDING_STATES,
    HARD_GATES,
    MAINTAINER_CONFIRMED_STATES,
    failed_gates,
    generate_handoff,
    score_opportunity,
    validate_opportunity,
)


def opportunity():
    gates = {
        gate: {"passed": True, "rationale": "supported by fixture"}
        for gate in [
            "humanitarian_relevance_supported",
            "repository_active",
            "external_contributions_accepted",
            "contribution_policy_understood",
            "ai_policy_understood",
            "problem_current_and_consequential",
            "behavior_reproducible_or_verifiable",
            "code_and_tests_located",
            "change_bounded",
            "regression_strategy_credible",
            "no_private_data_required",
            "security_and_licensing_risk_acceptable",
            "environment_feasible",
            "maintainer_interest_confirmed",
            "probable_reviewer_identified",
            "benefit_justifies_review_cost",
            "user_can_explain_line_by_line",
        ]
    }
    return {
        "id": "sample",
        "project_id": "sample-project",
        "title": "Sample opportunity",
        "pipeline_state": "SHORTLISTED",
        "problem": "A real problem",
        "humanitarian_relevance": "Relevant",
        "evidence": [{"type": "measured", "claim": "Observed", "source_id": "s1"}],
        "code_surface": "one module",
        "proposed_change": "small patch",
        "tests": "unit test",
        "environment": "local",
        "maintainer": "named reviewer",
        "risks": "low",
        "gates": gates,
        "score_inputs": {
            "humanitarian_benefit": 4,
            "acceptance_probability": 3,
            "technical_confidence": 4,
            "review_burden": 1,
            "deployment_probability": 3,
        },
        "sources": [{"id": "s1", "url": "https://example.test", "accessed": "2026-09-06"}],
    }


class ModelTests(unittest.TestCase):
    def test_evidence_must_reference_a_unique_source(self):
        record = opportunity()
        record["evidence"][0]["source_id"] = "unknown"
        self.assertTrue(any("unknown source" in issue.message for issue in validate_opportunity(record, "sample")))
        record = opportunity()
        record["sources"].append(dict(record["sources"][0]))
        self.assertTrue(any("duplicate source id" in issue.message for issue in validate_opportunity(record, "sample")))

    def test_source_dates_and_urls_are_validated(self):
        for field, values in {"accessed": ["2026-02-30", "20260906", "", None],
                              "url": ["relative/path", "https://", "https://[", "https://bad host", None]}.items():
            for value in values:
                record = opportunity()
                record["sources"][0][field] = value
                self.assertTrue(validate_opportunity(record, "sample"), (field, value))
        record = opportunity()
        record["sources"][0]["url"] = "file:///private/tmp/inspected-repo"
        self.assertEqual(validate_opportunity(record, "sample"), [])

    def test_malformed_nested_data_returns_issues(self):
        for field, values in {"evidence": [None, [None], [{"type": []}]],
                              "sources": [None, [None], [{"id": []}]],
                              "title": [None, "", []], "pipeline_state": [None, [], {}]}.items():
            for value in values:
                record = opportunity()
                record[field] = value
                self.assertTrue(validate_opportunity(record, "sample"), (field, value))

    def test_advanced_states_require_maintainer_confirmation(self):
        for state in MAINTAINER_CONFIRMED_STATES:
            with self.subTest(state=state):
                record = opportunity()
                record["pipeline_state"] = state
                record["gates"]["maintainer_interest_confirmed"]["passed"] = False
                self.assertTrue(validate_opportunity(record, "sample"))

    def test_building_and_later_require_every_gate(self):
        for state in BUILDING_STATES:
            for gate in HARD_GATES:
                with self.subTest(state=state, gate=gate):
                    record = opportunity()
                    record["pipeline_state"] = state
                    record["gates"][gate]["passed"] = False
                    self.assertTrue(validate_opportunity(record, "sample"))

    def test_early_and_stopped_states_can_retain_failed_gates(self):
        for state in ["MAINTAINER-CHECK", "PARKED", "DECLINED"]:
            record = opportunity()
            record["pipeline_state"] = state
            record["gates"]["maintainer_interest_confirmed"]["passed"] = False
            self.assertEqual(validate_opportunity(record, "sample"), [])

    def test_invalid_gate_shapes_fail_closed(self):
        for value in [None, [], True, "yes"]:
            record = opportunity()
            record["gates"] = value
            self.assertTrue(validate_opportunity(record, "sample"))
            self.assertEqual(len(failed_gates(record)), len(HARD_GATES))
        record = opportunity()
        record["gates"][HARD_GATES[0]] = None
        self.assertTrue(validate_opportunity(record, "sample"))
        self.assertEqual(len(failed_gates(record)), 1)

    def test_gate_values_require_boolean_and_explanation(self):
        for value in [1, "true", None]:
            record = opportunity()
            record["gates"][HARD_GATES[0]]["passed"] = value
            self.assertTrue(validate_opportunity(record, "sample"))
        for value in ["", "  ", None]:
            record = opportunity()
            record["gates"][HARD_GATES[0]]["rationale"] = value
            self.assertTrue(validate_opportunity(record, "sample"))

    def test_invalid_scores_are_rejected(self):
        for value in [True, float("nan"), float("inf"), -1, 6, "3"]:
            record = opportunity()
            record["score_inputs"]["humanitarian_benefit"] = value
            self.assertTrue(validate_opportunity(record, "sample"))

    def test_handoff_exposes_blockers_for_every_target(self):
        record = opportunity()
        record["gates"]["maintainer_interest_confirmed"] = {"passed": False, "rationale": "not yet asked"}
        for target in ["codex", "spark", "cursor-red-team"]:
            text = generate_handoff(record, target)
            self.assertIn("Implementation blocked. Do not implement", text)
            self.assertIn("maintainer_interest_confirmed: not yet asked", text)

    def test_validation_accepts_complete_opportunity(self):
        self.assertEqual(validate_opportunity(opportunity(), "sample"), [])

    def test_score_is_zero_when_hard_gate_fails(self):
        record = opportunity()
        record["gates"]["maintainer_interest_confirmed"] = {"passed": False, "rationale": "not yet asked"}
        result = score_opportunity(record)
        self.assertEqual(result["score"], 0.0)
        self.assertFalse(result["eligible_for_building"])
        self.assertEqual(failed_gates(record)[0]["gate"], "maintainer_interest_confirmed")

    def test_score_rewards_benefit_confidence_and_penalizes_review_burden(self):
        result = score_opportunity(opportunity())
        self.assertEqual(result["raw_score"], 2.7)
        self.assertEqual(result["score"], 2.7)

    def test_handoff_generation_is_bounded(self):
        text = generate_handoff(opportunity(), "cursor-red-team")
        self.assertIn("Do not implement", text)
        self.assertIn("no external writes", text)


if __name__ == "__main__":
    unittest.main()
