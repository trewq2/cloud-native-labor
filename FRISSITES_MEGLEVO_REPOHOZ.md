# Meglévő cloud-labor repository frissítése v2.1-re

Ha már korábbi starterből dolgozol, nem kell új repositoryt készíteni.

## 1. Biztonsági mentés

```bash
git status
git add .
git commit -m "Mentés a CloudLab v2.1 frissítés előtt"
git push
```

Ha nincs módosítás, a commit lépés kihagyható.

## 2. Cserélendő fájlok

A friss starterből másold át:

- `app.py`
- `compose.yaml`
- `requirements.txt`
- `.devcontainer/devcontainer.json`
- `check-compose.sh`

A `Dockerfile`, `k8s.yaml`, workflow és `status-site` csak akkor cserélendő, ha a saját változatod nem tartalmaz fontos egyedi módosítást.

## 3. Compose újraindítás

```bash
docker compose down --remove-orphans
docker rm -f cloudlab cloudlab-web cloudlab-redis 2>/dev/null || true
docker compose up -d --build --force-recreate
```

## 4. Ellenőrzés

```bash
bash check-compose.sh
```

Helyes eredmények:

```text
PONG
Redis PING: True
```

és az API-ban:

```json
"redis": true
```

## 5. Böngésző

Codespaces → **PORTS** → **8080** → **Open in Browser**.

F5-re a számlálónak növekednie kell.

## 6. Commit

```bash
git add app.py compose.yaml requirements.txt .devcontainer/devcontainer.json check-compose.sh
git commit -m "Fix Codespaces Redis visitor counter"
git push origin main
```

## 7. Dev container újraépítés

Ha a `.devcontainer/devcontainer.json` változott, a Command Palette-ben futtasd a **Rebuild Container** műveletet, vagy készíts új Codespace-et.
