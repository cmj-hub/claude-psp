#!/usr/bin/env bash
set -euo pipefail
PASSED=0; FAILED=0
check() { local n="$1"; shift; if "$@"; then echo "  ✓ $n"; PASSED=$((PASSED+1)); else echo "  ✗ $n"; FAILED=$((FAILED+1)); fi; }

echo "=== score_psp.py ==="
# Strong PSP (score >=70 → exit 0)
check "strong PSP" \
  bash -c 'python3 scripts/score_psp.py --stdin --format text <<EOF
{"signal":"Posted Senior Demand Gen Lead role on LinkedIn 4 days ago","pain":"Pipeline gap; demand-gen motion isn'\''t producing enough SQLs","timing_trigger":"new-exec","felt_pain_role":"VP Demand Gen","vocabulary":["pipeline gap","SDR ramp","demand-gen motion isn'\''t producing","we keep closing wrong-fit logos"]}
EOF'

# Weak PSP (score <70 → exit 1) — invert
echo "  (testing inverse — abstract PSP should exit non-zero)"
if bash -c 'python3 scripts/score_psp.py --stdin --format text <<EOF
{"signal":"Series B SaaS company with 50 employees","pain":"They need to scale growth","timing_trigger":"soon","felt_pain_role":"CEO","vocabulary":["scale","growth"]}
EOF' > /dev/null 2>&1; then
  echo "  ✗ abstract PSP should have failed but passed"
  FAILED=$((FAILED+1))
else
  echo "  ✓ abstract PSP correctly rejected"
  PASSED=$((PASSED+1))
fi

echo ""; echo "Passed: $PASSED, Failed: $FAILED"
[ "$FAILED" -eq 0 ]
