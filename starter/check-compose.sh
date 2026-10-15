#!/usr/bin/env bash
set -euo pipefail

echo "=== CloudLab Compose ellenőrzés ==="

docker compose ps

echo
echo "[1/4] Redis PING"
docker compose exec -T redis redis-cli ping

echo
echo "[2/4] Python -> Redis"
docker compose exec -T web python -c "import redis; r=redis.Redis(host='127.0.0.1',port=6379,socket_connect_timeout=2,socket_timeout=2); print('Redis PING:', r.ping())"

echo
echo "[3/4] API"
curl --fail --silent http://127.0.0.1:8080/api/info
echo

echo
echo "[4/4] Számláló"
curl --fail --silent http://127.0.0.1:8080/ >/dev/null
curl --fail --silent http://127.0.0.1:8080/ >/dev/null
printf "cloudlab_visits = "
docker compose exec -T redis redis-cli GET cloudlab_visits

echo
echo "=== Ellenőrzés vége ==="
