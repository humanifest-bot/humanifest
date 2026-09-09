"""Offline work selection from validated portfolio records."""

from datetime import date

from .models import ACTIVE_IMPLEMENTATION_STATES, PIPELINE_STATES, next_action


def work_plan(opportunities: list[dict], *, as_of: date) -> dict:
    """List recorded work without interpreting prose as executable instructions.

    Callers validate the full portfolio first. A date is a review reminder, not
    evidence of a reply or permission to implement. Ordering is by ID, not impact.
    """
    plan = {"as_of": as_of.isoformat(), "active_work": [], "due_reviews": [],
            "independent_research": [], "unscheduled_reviews": [], "waiting": []}
    research_states = set(PIPELINE_STATES[:7]) | {"PR-OPEN"}
    active_states = set(ACTIVE_IMPLEMENTATION_STATES) | {"ENVIRONMENT-READY", "REPRODUCED"}
    for record in sorted(opportunities, key=lambda item: item["id"]):
        state = record["pipeline_state"]
        if state in {"PARKED", "DECLINED"}:
            continue
        item = {"id": record["id"], "title": record["title"], "state": state}
        if state in active_states:
            plan["active_work"].append({**item, "action": next_action(record)})
        if state in research_states and record.get("research_next_step"):
            plan["independent_research"].append({**item, "action": record["research_next_step"]})
        review_date = record.get("next_external_status_check")
        if review_date:
            bucket = "due_reviews" if date.fromisoformat(review_date) <= as_of else "waiting"
            plan[bucket].append({**item, "review_on": review_date})
        elif state in {"MAINTAINER-CHECK", "PR-OPEN"}:
            plan["unscheduled_reviews"].append(item)
    plan["refill_suggested"] = not (plan["active_work"] or plan["independent_research"])
    return plan


def render_work_plan(plan: dict) -> str:
    lines = [f"# Work options as of {plan['as_of']}", "",
             "Offline record view; no upstream check, state change, or authorization is implied.",
             "Items are ordered by ID, not ranked by impact. Act on relevant new feedback when it arrives."]
    for key, title in [("active_work", "Work in progress"), ("due_reviews", "Reviews due"),
                       ("independent_research", "Independent research available now"),
                       ("unscheduled_reviews", "Review date not recorded"),
                       ("waiting", "Reviews scheduled for later")]:
        if not plan[key]:
            continue
        lines.extend(["", f"## {title}", ""])
        for item in plan[key]:
            detail = item.get("action") or (
                f"Review on {item['review_on']}" if "review_on" in item
                else "Record a review date; missing dates do not mean poll on every run."
            )
            lines.append(f"- {item['id']}: {item['title']} — {detail}")
    if plan["refill_suggested"]:
        lines.extend(["", "No independent research step or active work is recorded. After due reviews, "
                      "find and verify another bounded opportunity; waiting reviews do not exhaust the queue."])
    return "\n".join(lines)
