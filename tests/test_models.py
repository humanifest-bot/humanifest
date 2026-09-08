import unittest

from humanifest.models import (
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
