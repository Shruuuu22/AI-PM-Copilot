from jinja2 import Template
from datetime import datetime

PRD_TEMPLATE = '''# {{title}}

Generated: {{ts}}

## Problem Statement

{{problem}}

## Customer Evidence

{% for q in quotes %}- {{q}}
{% endfor %}

## Target Users

{{target_users}}

## User Need / JTBD

{{jtbd}}

## Proposed Solution Direction

{{solution}}

## Goals

{{goals}}

## Non-Goals

{{non_goals}}

## Success Metrics

{{metrics}}

## Risks

{{risks}}

## Open Questions

{{questions}}

## Evidence References

{{references}}
'''


def export_prd_md(theme_label, prd_text):
    ts = datetime.utcnow().isoformat()
    md = f"# PRD: {theme_label}\n\nGenerated: {ts}\n\n" + prd_text
    return md

