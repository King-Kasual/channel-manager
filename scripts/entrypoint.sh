#!/usr/bin/env bash
set -euo pipefail

# Prefer .env in /app (when mounted in container), fallback to repo root .env
load_env_file() {
  local env_path="$1"
  # create a temp file with CR characters removed to avoid /bin/bash errors
  local tmpenv
  tmpenv=$(mktemp)
  tr -d '\r' < "$env_path" > "$tmpenv"
  set -a
  # shellcheck disable=SC1091
  . "$tmpenv"
  set +a
  rm -f "$tmpenv"
}

 # Only load a .env file if the DB_HOST variable is not already set by the environment
 if [ -z "${DB_HOST:-}" ]; then
  if [ -f "/app/.env" ]; then
    echo "[entrypoint] loading /app/.env (DB_HOST unset)"
    load_env_file "/app/.env"
  elif [ -f ".env" ]; then
    echo "[entrypoint] loading .env (DB_HOST unset)"
    load_env_file ".env"
  fi
 else
  echo "[entrypoint] DB_HOST already set in environment; skipping .env load"
 fi

echo "[entrypoint] environment for DB: DB_HOST=${DB_HOST:-<unset>} DB_PORT=${DB_PORT:-<unset>} DB_USER=${DB_USER:-<unset>} DB_NAME=${DB_NAME:-<unset>}"
echo "[entrypoint] running migrations..."
if ! python scripts/run_migrations.py; then
  echo "[entrypoint] migrations failed; exiting" >&2
  exit 1
fi
echo "[entrypoint] migrations complete"

echo "[entrypoint] starting bot"
# Use exec so the python process receives signals directly (PID 1 replacement)
exec python main.py
