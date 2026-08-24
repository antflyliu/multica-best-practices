#!/bin/bash
# Shared credential resolution for multica platform skills
#
# Priority (highest first):
#   1. ATLASSIAN_USER / ATLASSIAN_PASS
#   2. ATLASSIAN_USER / ATLASSIAN_PASS (dev-workflow compatible)
#   3. JIRA_USER / JIRA_PASS, CONFLUENCE_USER / CONFLUENCE_PASS

load_skill_env() {
  local skill_dir="$1"
  if [ -f "$skill_dir/.env" ]; then
    set -a
    # shellcheck disable=SC1091
    . "$skill_dir/.env"
    set +a
  fi
}

resolve_credentials() {
  JIRA_USER="${ATLASSIAN_USER:-${JIRA_USER:-}}"
  JIRA_PASS="${ATLASSIAN_PASS:-${JIRA_PASS:-}}"
  CONFLUENCE_USER="${ATLASSIAN_USER:-${CONFLUENCE_USER:-${JIRA_USER:-}}}"
  CONFLUENCE_PASS="${ATLASSIAN_PASS:-${CONFLUENCE_PASS:-${JIRA_PASS:-}}}"
  export JIRA_USER JIRA_PASS CONFLUENCE_USER CONFLUENCE_PASS
}


