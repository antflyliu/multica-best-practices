---
name: multica-test-automation
description: "Test-automation skill (placeholder shell): Tester phase-3 automation — after G2.5 the deploy environment is ready, run the team's automation tool against the scenario cases and produce G3 input. Concrete tool (Apifox / Postman / Playwright / pytest / etc.) onboarded by the team; credentials injected via runtime env, never in role prompts."
metadata:
  layer: automation
  runtime:
    python: ">=3.10"
    external:
      - <team-test-cli>  # team automation-test CLI
---

# Test Automation (placeholder shell · T3)

> This is a **placeholder shell**. The public multica-best-practices binds to no specific company's internal URLs or test tools.
> To onboard your own automation tool, only edit this skill's `scripts/` and `config.yaml`; the upstream Tester role stays untouched.

## Purpose

Tester **T3**: after G2.5 gives `deploy_base_url`, run cases with the team's automation tool and produce G3 input (test report).

> Cross-platform: wrap config + subprocess calls to the underlying CLI in Python, consistent on Windows / Linux.

## Install

```bash
pip install -r scripts/requirements.txt
# install the team automation-test CLI (team-specific, e.g. apifox-cli / newman / playwright)
```

## Workflow

```bash
set TEST_TOOL_TOKEN=<token>   # runtime env, never in role prompts

python scripts/run_tests.py \
  --issue <ISSUE-KEY> \
  --base-url "<deploy_base_url>" \
  --scenario-id <scenario> \
  --environment-id <env> \
  --json
```

Or specify only the Issue (scenario / environment read from `config.yaml`):

```bash
python scripts/run_tests.py --issue <ISSUE-KEY> --base-url "<deploy_base_url>" --json
```

## Why it works

Python owns config and the subprocess call to the underlying test CLI, isolating the "Tester role" from the "concrete test tool" — swap tools by editing only this skill, keeping the Tester prompt "use the multica-test-automation skill to run T3" unchanged.
