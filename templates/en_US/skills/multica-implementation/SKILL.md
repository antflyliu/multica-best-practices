---
name: multica-implementation
description: Implement an approved technical plan with minimal unnecessary changes. Used for coding, adding tests, and running verification.
category: methodology
owner: BackendDev / FrontendDev
version: 1.0
inputs:
  - Approved Technical Design
  - Issue / Acceptance Criteria
  - Existing Code
outputs:
  - Implementation changes
  - Test changes
  - Execution evidence
side_effects:
  - Modifies source code and tests
requires:
  - Approved technical design
  - Clear Issue scope
forbidden:
  - Silent requirement changes
  - Declaring Gate PASS
  - Replacing Leader Verification
idempotent: false
platform_dependent: false
---

# Implementation

## Purpose

Implement the approved technical plan with the fewest unnecessary changes.

## Rules

1. Read before you change.
2. Follow existing conventions.
3. Keep the scope focused.
4. Don't silently modify requirements.
5. Add appropriate tests.
6. Run the existing verification.
7. Report actual evidence.

## Completion Evidence

- Changed files
- Notes on the important changes
- Commands actually executed
- Execution results
- Known limitations

## Why this works

The two rules "read before you change" and "report actual evidence" prevent the two most common incidents: changing things without knowing the current state, and claiming it passed without ever running the commands.
