#!/usr/bin/env bash
set -euo pipefail

##
# Generates .env from 1Password "Developer Projects" vault.
#
# Usage:
#   ./scripts/generate-env.sh          # write .env to project root
#   ./scripts/generate-env.sh --stdout  # print to stdout
#   ./scripts/generate-env.sh --check   # diff against current .env
##

VAULT="Developer Projects"
ITEM="sbu-seedgrant-llm-grantreviewer-env"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_ROOT/.env"

# All fields to fetch, in order. Format: FIELD_NAME:section
FIELDS=(
  "OPENAI_API_KEY:Secrets"
  "OPENAI_MODEL:Config"
  "GEMINI_API_KEY:Secrets"
  "GEMINI_MODEL:Config"
  "ANTHROPIC_API_KEY:Secrets"
  "ANTHROPIC_MODEL:Config"
  "GROK_API_KEY:Secrets"
  "GROK_MODEL:Config"
  "FLASK_SECRET_KEY:Secrets"
  "FLASK_DEBUG:Config"
  "PORT:Config"
  "DB_TYPE:Config"
  "DB_PATH:Config"
)

# --- Auth check ---
check_auth() {
  if ! command -v op &>/dev/null; then
    echo "Error: 1Password CLI (op) is not installed." >&2
    echo "Install it: https://developer.1password.com/docs/cli/get-started/" >&2
    exit 1
  fi

  if ! op vault list &>/dev/null 2>&1; then
    echo "Error: Not authenticated with 1Password CLI." >&2
    echo "Unlock the 1Password desktop app or run: eval \$(op signin)" >&2
    exit 1
  fi
}

# --- Fetch a single field value ---
fetch_field() {
  local field_name="$1"
  op item get "$ITEM" --vault "$VAULT" --fields "label=$field_name" --reveal 2>/dev/null
}

# --- Generate .env content ---
generate_env() {
  local output=""
  output+="# Auto-generated from 1Password ($VAULT / $ITEM)"$'\n'
  output+="# Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"$'\n'
  output+=$'\n'

  local current_section=""
  for entry in "${FIELDS[@]}"; do
    local field_name="${entry%%:*}"
    local section="${entry##*:}"

    # Add section header on change
    if [[ "$section" != "$current_section" ]]; then
      if [[ -n "$current_section" ]]; then
        output+=$'\n'
      fi
      output+="# $section"$'\n'
      current_section="$section"
    fi

    local value
    value="$(fetch_field "$field_name")"
    if [[ -z "$value" ]]; then
      echo "Warning: empty value for $field_name" >&2
    fi
    output+="$field_name=$value"$'\n'
  done

  printf '%s' "$output"
}

# --- Main ---
check_auth

MODE="${1:-write}"

case "$MODE" in
  --stdout)
    generate_env
    ;;
  --check)
    if [[ ! -f "$ENV_FILE" ]]; then
      echo "No .env file found at $ENV_FILE" >&2
      exit 1
    fi
    TMPFILE=$(mktemp)
    trap 'rm -f "$TMPFILE"' EXIT
    generate_env > "$TMPFILE"
    # Strip comments and blank lines for comparison
    diff <(grep -v '^#' "$ENV_FILE" | grep -v '^$' | sort) \
         <(grep -v '^#' "$TMPFILE" | grep -v '^$' | sort) \
      && echo "No differences found." \
      || echo -e "\nDifferences detected (left: current .env, right: 1Password)."
    ;;
  --help|-h)
    echo "Usage: $0 [--stdout | --check | --help]"
    echo ""
    echo "  (no args)   Write .env to project root"
    echo "  --stdout    Print .env content to stdout"
    echo "  --check     Diff current .env against 1Password values"
    echo "  --help      Show this help"
    ;;
  write|"")
    # Default: write .env
    generate_env > "$ENV_FILE"
    chmod 600 "$ENV_FILE"
    echo "Wrote $ENV_FILE (chmod 600)"
    ;;
  *)
    echo "Unknown option: $MODE" >&2
    echo "Usage: $0 [--stdout | --check | --help]" >&2
    exit 1
    ;;
esac
