#!/usr/bin/env bash
# Wiki Ingest wrapper: raw → wiki compile
# Usage: ./wiki-ingest.sh <raw-file> [--type concept|entity|source]

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/wiki-ingest.py" "$@"
