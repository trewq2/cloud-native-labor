# Changelog

## v2.1 – Codespaces + Redis stabilizálás

- Javítva a GitHub Codespaces alatt tapasztalt `web -> redis:6379` timeout.
- Compose: `network_mode: "service:redis"`.
- Compose: `REDIS_HOST=127.0.0.1`.
- Redis healthcheck.
- Kibővített Flask diagnosztika.
- `/api/info` kibővítve `redis_configured`, `counter`, `redis_error` mezőkkel.
- Új `check-compose.sh`.
- Egyértelmű repository-root feltöltési utasítás.
- Dotmappák feltöltési útmutató.
- `.devcontainer` portok: 8080, 8081, 8082.
- Kubernetes Redis-viselkedés tisztázva.
- Volume reset és megőrzés egyértelműsítve.
- Tanári hibaelhárítás bővítve.
