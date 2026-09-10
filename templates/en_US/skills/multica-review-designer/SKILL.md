---
name: multica-review-designer
description: UI-design dedicated review framework. Called by DesignReviewer to professionally analyze Designer's UI/interaction design (interaction soundness/accessibility/design-system consistency/edge states), output a professional review conclusion and fix list, and report to Leader.
category: methodology
owner: DesignReviewer
version: 1.0
inputs:
  - ui_design_artifact
  - acceptance_criteria
  - previous_review_findings
outputs:
  - design_review
side_effects: []
requires:
  - ui_design_ready
forbidden:
  - modify_design_artifact
  - approve_leader_gate
  - notify_designer_directly
idempotent: true
platform_dependent: false
---

# UI Design Professional Review (DesignReviewer)

Structured professional review framework for **UI / interaction design artifacts**. Called by `DesignReviewer`; reviews the design artifact returned by `Designer` via `multica-artifact-ui-sync`.

## When to use
- DesignReviewer receives a "review UI design" dispatch from Leader.
- Entering a re-review round after design changes (check the previous round's fix list item by item).

## Review dimensions (conclusion per item)
1. **Interaction soundness**: flow smooth, matches user mental model, no redundant steps.
2. **Accessibility**: contrast, focus management, a11y annotations in place.
3. **Design-system consistency**: components, font, spacing, states aligned.
4. **Edge states**: empty / loading / error / overflow text covered.
5. **Technical feasibility**: no obviously unimplementable or high-cost interactions (mark and hand to Leader).

## Output format
```
【UI Review】<design artifact>
Conclusion: PASS / FAIL
Blocking items (required on FAIL, each: rationale / involved point / fix direction):
- ...
Suggestions (non-blocking):
- ...
Previous fix-list check (re-review): resolved X / unresolved Y
Round: N / 3
```

Conclusion + fix list **reported to Leader**. This skill performs professional review only; it does not execute the generic delivery gate, modify the design, or notify Designer directly.

## Boundaries
- Review only UI design, not architecture, requirements, code, or test cases.
- Don't replace Leader's generic gate (`multica-verification` skill).
- Still FAIL at round 3 → mark "escalate to human", hand to Leader, stop looping.
