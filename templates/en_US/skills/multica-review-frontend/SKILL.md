---
name: multica-review-frontend
description: Frontend implementation review framework covering code quality, maintainability, performance, accessibility, and test completeness.
category: methodology
owner: FrontendReviewer
version: 1.0
inputs:
  - implementation
  - acceptance_criteria
  - test_evidence
outputs:
  - frontend_review
side_effects: []
requires:
  - implementation_ready
forbidden:
  - modify_implementation
  - approve_leader_gate
idempotent: true
platform_dependent: false
---

# Frontend Review

## Responsibility
Review implementation from the frontend professional perspective. Do not modify implementation artifacts or execute the Leader Gate.

## Review dimensions
- UI/UX alignment with requirements and acceptance criteria
- API contract alignment
- Component quality and maintainability
- Performance and resource-loading risks
- Accessibility
- Error handling and edge cases
- Test coverage and regression risk

## Output
Report findings, severity, and recommendations to Leader. The Reviewer does not grant G1/G2/G2.5/G3 PASS.

If the third review round still FAILs, escalate to Human through Leader and stop the loop.
