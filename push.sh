#!/usr/bin/env bash
# One-click push for Mac/Linux. Usage:  ./push.sh "your message"
set -e
echo "=== Running tests ==="
python -m pytest -q || { echo "*** TESTS FAILED - nothing pushed. ***"; exit 1; }
MSG="${1:-Update site}"
git add -A
git commit -m "$MSG" || echo "(Nothing new to commit.)"
git push origin main
echo "=== Done. ==="
