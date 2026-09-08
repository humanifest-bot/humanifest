"""Data loading, validation, gates, scoring, and report generation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import json
from typing import Any
from urllib.parse import urlsplit


PIPELINE_STATES = [
    "QUEUED",
    "PROJECT-AUDIT",
    "OPPORTUNITY-RESEARCH",
    "SHORTLISTED",
    "MAINTAINER-CHECK",
    "ENVIRONMENT-READY",
    "REPRODUCED",
    "BUILDING",
    "ADVERSARIAL-REVIEW",
    "HUMAN-REVIEW",
    "PR-OPEN",
    "MERGED",
    "RELEASED",
    "PARKED",
    "DECLINED",
]

EVIDENCE_TYPES = {"measured", "modeled", "self_reported", "inferred"}
MAINTAINER_CONFIRMED_STATES = PIPELINE_STATES[5:13]
BUILDING_STATES = PIPELINE_STATES[7:13]

HARD_GATES = [
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

SCORE_WEIGHTS = {
    "humanitarian_benefit": 0.30,
    "acceptance_probability": 0.20,
    "technical_confidence": 0.20,
    "review_burden": -0.20,
    "deployment_probability": 0.10,
}

REQUIRED_PROJECT_FIELDS = [
    "id",
    "name",
    "repository",
    "homepage",
    "license",
    "humanitarian_domain",
    "impact_evidence",
    "maintenance",
    "contribution",
    "sources",
]

REQUIRED_OPPORTUNITY_FIELDS = [
    "id",
    "project_id",
    "title",
    "pipeline_state",
    "problem",
    "humanitarian_relevance",
    "evidence",
    "code_surface",
    "proposed_change",
    "tests",
    "environment",
    "maintainer",
    "risks",
    "gates",
    "score_inputs",
    "sources",
]


@dataclass(frozen=True)
class ValidationIssue:
    record: str
    message: str


def load_json(path: Path) -> dict[str, Any]:
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    def reject_constant(value):
        raise ValueError(f"invalid JSON constant: {value}")

    with path.open(encoding="utf-8") as handle:
        data = json.load(handle, object_pairs_hook=unique_object, parse_constant=reject_constant)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def iter_records(directory: Path) -> list[tuple[Path, dict[str, Any]]]:
    records: list[tuple[Path, dict[str, Any]]] = []
    if not directory.exists():
        return records
    for path in sorted(directory.glob("*.json")):
        records.append((path, load_json(path)))
    return records


def validate_project(record: dict[str, Any], record_name: str) -> list[ValidationIssue]:
    issues = _require_fields(record, REQUIRED_PROJECT_FIELDS, record_name)
    issues.extend(_validate_text_fields(record, REQUIRED_PROJECT_FIELDS[:6], record_name))
    for field in ["maintenance", "contribution"]:
        if not isinstance(record.get(field), dict):
            issues.append(ValidationIssue(record_name, f"{field} must be an object"))
    issues.extend(_validate_sources(record, record_name))
    issues.extend(_validate_evidence_list(record.get("impact_evidence", []), record_name, "impact_evidence", _source_ids(record)))
    return issues


def validate_opportunity(record: dict[str, Any], record_name: str) -> list[ValidationIssue]:
    issues = _require_fields(record, REQUIRED_OPPORTUNITY_FIELDS, record_name)
    issues.extend(_validate_text_fields(record, [field for field in REQUIRED_OPPORTUNITY_FIELDS
                                               if field not in {"evidence", "gates", "score_inputs", "sources"}], record_name))
    state = record.get("pipeline_state")
    if state not in PIPELINE_STATES:
        issues.append(ValidationIssue(record_name, f"pipeline_state must be one of {', '.join(PIPELINE_STATES)}"))
    gates = record.get("gates", {})
    if not isinstance(gates, dict):
        issues.append(ValidationIssue(record_name, "gates must be an object"))
    else:
        for gate in HARD_GATES:
            item = gates.get(gate)
            if not isinstance(item, dict) or "passed" not in item or "rationale" not in item:
                issues.append(ValidationIssue(record_name, f"gate {gate} must include passed and rationale"))
                continue
            if not isinstance(item["passed"], bool):
                issues.append(ValidationIssue(record_name, f"gate {gate}.passed must be a boolean"))
            if not isinstance(item["rationale"], str) or not item["rationale"].strip():
                issues.append(ValidationIssue(record_name, f"gate {gate}.rationale must be a non-empty string"))
    failures = failed_gates(record)
    if state in MAINTAINER_CONFIRMED_STATES and any(
        item["gate"] == "maintainer_interest_confirmed" for item in failures
    ):
        issues.append(ValidationIssue(record_name, f"{state} requires maintainer_interest_confirmed to pass"))
    if state in BUILDING_STATES and failures:
        issues.append(ValidationIssue(record_name, f"{state} requires every hard gate to pass"))
    score_inputs = record.get("score_inputs", {})
    if not isinstance(score_inputs, dict):
        issues.append(ValidationIssue(record_name, "score_inputs must be an object"))
    else:
        for key in SCORE_WEIGHTS:
            value = score_inputs.get(key)
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 5:
                issues.append(ValidationIssue(record_name, f"score_inputs.{key} must be a number from 0 to 5"))
    issues.extend(_validate_sources(record, record_name))
    issues.extend(_validate_evidence_list(record.get("evidence", []), record_name, "evidence", _source_ids(record)))
    return issues


def failed_gates(record: dict[str, Any]) -> list[dict[str, str]]:
    failures = []
    gates = record.get("gates")
    if not isinstance(gates, dict):
        gates = {}
    for gate in HARD_GATES:
        item = gates.get(gate)
        if not isinstance(item, dict):
            item = {}
        if item.get("passed") is not True:
            failures.append({"gate": gate, "rationale": str(item.get("rationale", "missing rationale"))})
    return failures


def score_opportunity(record: dict[str, Any], weights: dict[str, float] | None = None) -> dict[str, Any]:
    weights = weights or SCORE_WEIGHTS
    inputs = record["score_inputs"]
    weighted_total = 0.0
    details = {}
    for key, weight in weights.items():
        contribution = float(inputs[key]) * weight
        details[key] = {"value": inputs[key], "weight": weight, "contribution": round(contribution, 3)}
        weighted_total += contribution

    failures = failed_gates(record)
    eligible = not failures
    return {
        "eligible_for_building": eligible,
        "score": round(max(0.0, weighted_total), 3) if eligible else 0.0,
        "raw_score": round(weighted_total, 3),
        "failed_gates": failures,
        "details": details,
    }


def generate_candidate_brief(record: dict[str, Any]) -> str:
    score = score_opportunity(record)
    evidence_lines = [
        f"- {item['type']}: {item['claim']} ({item['source_id']})"
        for item in record.get("evidence", [])
    ]
    failed = score["failed_gates"]
    gate_lines = ["- none"] if not failed else [f"- {item['gate']}: {item['rationale']}" for item in failed]
    return "\n".join(
        [
            f"# {record['title']}",
            "",
            f"Project: {record['project_id']}",
            f"Pipeline state: {record['pipeline_state']}",
            f"Score: {score['score']} (raw {score['raw_score']})",
            "",
            "## Problem",
            record["problem"],
            "",
            "## Evidence",
            *evidence_lines,
            "",
            "## Proposed smallest safe change",
            record["proposed_change"],
            "",
            "## Failed gates",
            *gate_lines,
        ]
    )


def generate_handoff(record: dict[str, Any], target: str) -> str:
    if target not in {"codex", "spark", "cursor-red-team"}:
        raise ValueError("target must be codex, spark, or cursor-red-team")
    base = [
        f"Objective: evaluate and prepare the opportunity `{record['id']}` for {record['project_id']}.",
        f"Title: {record['title']}",
        f"Scope: {record['code_surface']}",
        f"Problem: {record['problem']}",
        f"Proposed bounded change: {record['proposed_change']}",
        f"Acceptance criteria: {record['tests']}",
        "Constraints: no external writes, no maintainer contact, no private data, stop if evidence contradicts the gate rationale.",
        "Return format: findings, changed files if any, commands run, remaining blockers, and confidence.",
    ]
    failures = failed_gates(record)
    base.insert(2, f"Pipeline state: {record['pipeline_state']}.")
    if failures or record["pipeline_state"] in {"PARKED", "DECLINED"}:
        base.append("Implementation blocked. Do not implement; limit work to read-only inspection and resolving the blockers below.")
    else:
        base.append("All hard gates pass. Implementation still requires an approved scope and inspected environment.")
    base.extend(f"Blocker: {item['gate']}: {item['rationale']}" for item in failures)
    if target == "spark":
        base.insert(0, "Use a fast Codex model only for bounded inspection or mechanical verification.")
    elif target == "cursor-red-team":
        base.insert(0, "Act as an independent adversarial reviewer. Do not implement the fix.")
        base.append("Focus on hidden scope, security, environment risk, test gaps, and maintainer burden.")
    else:
        base.insert(0, "Use full-reasoning Codex for synthesis, integration, and final go/no-go.")
    return "\n".join(base)


def portfolio_report(projects: list[dict[str, Any]], opportunities: list[dict[str, Any]]) -> str:
    rows = ["# Portfolio Status", ""]
    rows.append(f"Projects: {len(projects)}")
    rows.append(f"Opportunities: {len(opportunities)}")
    rows.append("")
    for opportunity in sorted(opportunities, key=lambda item: score_opportunity(item)["raw_score"], reverse=True):
        score = score_opportunity(opportunity)
        rows.append(f"- {opportunity['id']}: {opportunity['pipeline_state']}; score={score['score']}; failed_gates={len(score['failed_gates'])}")
    return "\n".join(rows)


def _require_fields(record: dict[str, Any], fields: list[str], record_name: str) -> list[ValidationIssue]:
    return [ValidationIssue(record_name, f"missing required field: {field}") for field in fields if field not in record]


def _validate_text_fields(record: dict[str, Any], fields: list[str], record_name: str) -> list[ValidationIssue]:
    return [ValidationIssue(record_name, f"{field} must be a non-empty string")
            for field in fields if not isinstance(record.get(field), str) or not record[field].strip()]


def _source_ids(record: dict[str, Any]) -> set[str]:
    sources = record.get("sources")
    if not isinstance(sources, list):
        return set()
    return {source["id"] for source in sources if isinstance(source, dict) and isinstance(source.get("id"), str)}


def _validate_sources(record: dict[str, Any], record_name: str) -> list[ValidationIssue]:
    issues = []
    sources = record.get("sources", [])
    if not isinstance(sources, list) or not sources:
        return [ValidationIssue(record_name, "sources must be a non-empty list")]
    seen = set()
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            issues.append(ValidationIssue(record_name, f"sources[{index}] must be an object"))
            continue
        issues.extend(_validate_text_fields(source, ["id", "url", "accessed"], f"{record_name}: sources[{index}]"))
        source_id = source.get("id")
        if isinstance(source_id, str):
            if source_id in seen:
                issues.append(ValidationIssue(record_name, f"duplicate source id: {source_id}"))
            seen.add(source_id)
        try:
            accessed = source.get("accessed")
            if not isinstance(accessed, str) or date.fromisoformat(accessed).isoformat() != accessed:
                raise ValueError
        except ValueError:
            issues.append(ValidationIssue(record_name, f"sources[{index}].accessed must be a valid YYYY-MM-DD date"))
        try:
            url = source.get("url")
            parsed = urlsplit(url) if isinstance(url, str) else None
            web_url = parsed is not None and parsed.scheme in {"https", "http"} and bool(parsed.hostname)
            local_url = parsed is not None and parsed.scheme == "file" and parsed.netloc in {"", "localhost"} and parsed.path.startswith("/")
            if not (web_url or local_url) or any(c.isspace() for c in url):
                raise ValueError
        except ValueError:
            issues.append(ValidationIssue(record_name, f"sources[{index}].url must be an absolute HTTP(S) or local file URL"))
    return issues


def _validate_evidence_list(items: Any, record_name: str, field: str, source_ids: set[str]) -> list[ValidationIssue]:
    issues = []
    if not isinstance(items, list):
        return [ValidationIssue(record_name, f"{field} must be a list")]
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            issues.append(ValidationIssue(record_name, f"{field}[{index}] must be an object"))
            continue
        evidence_type = item.get("type")
        if not isinstance(evidence_type, str) or evidence_type not in EVIDENCE_TYPES:
            issues.append(ValidationIssue(record_name, f"{field}[{index}].type must be measured, modeled, self_reported, or inferred"))
        issues.extend(_validate_text_fields(item, ["claim", "source_id"], f"{record_name}: {field}[{index}]"))
        source_id = item.get("source_id")
        if isinstance(source_id, str) and source_id not in source_ids:
            issues.append(ValidationIssue(record_name, f"{field}[{index}].source_id references unknown source: {source_id}"))
    return issues


def load_portfolio(root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[ValidationIssue]]:
    """Collect diagnostics across the portfolio before any report is rendered."""
    issues = []
    collections = []
    for kind, validator in [("projects", validate_project), ("opportunities", validate_opportunity)]:
        directory = root / "portfolio" / kind
        records = []
        seen = set()
        if not directory.is_dir():
            issues.append(ValidationIssue(str(directory), "required record directory is missing"))
        else:
            for path in sorted(directory.glob("*.json")):
                try:
                    record = load_json(path)
                except (OSError, ValueError) as error:
                    issues.append(ValidationIssue(str(path), str(error)))
                    continue
                issues.extend(validator(record, str(path)))
                record_id = record.get("id")
                if isinstance(record_id, str):
                    if record_id in seen:
                        issues.append(ValidationIssue(str(path), f"duplicate {kind} id: {record_id}"))
                    seen.add(record_id)
                records.append((path, record))
        collections.append(records)
    projects, opportunities = collections
    project_ids = {record["id"] for _, record in projects if isinstance(record.get("id"), str)}
    for path, record in opportunities:
        project_id = record.get("project_id")
        if isinstance(project_id, str) and project_id not in project_ids:
            issues.append(ValidationIssue(str(path), f"project_id references unknown project: {project_id}"))
    return [record for _, record in projects], [record for _, record in opportunities], issues
