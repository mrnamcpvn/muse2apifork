#!/bin/bash
echo "Starting muse2api server on Codespaces (0.0.0.0:10000)..."
export PORT=10000
export MUSE2API_HOST=0.0.0.0
export MUSE2API_KEY=m2a_orca_muse_1b_tokens

# Keep-alive heartbeat to prevent idle sleep
(while true; do date > /tmp/.keepalive 2>/dev/null; sleep 120; done) &

if command -v python3 &>/dev/null; then
    PY_BIN=python3
else
    PY_BIN=python
fi

# Tự động phục hồi account nếu chưa có
$PY_BIN restore_accounts.py 2>/dev/null || true

exec $PY_BIN -m uvicorn app:app --host 0.0.0.0 --port 10000
