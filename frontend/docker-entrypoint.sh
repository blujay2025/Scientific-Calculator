#!/bin/sh
set -eu

cat > /app/dist/env-config.js <<CONFIG
window.__APP_CONFIG__ = {
  VITE_API_BASE_URL: "${VITE_API_BASE_URL:-http://localhost:5001/api}"
};
CONFIG

exec serve -s /app/dist -l 3000
