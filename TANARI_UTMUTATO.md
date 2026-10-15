# Cloud Native Labor v2.1 – tanári útmutató

## Javasolt időbeosztás

- 1. óra: GitHub repository + Codespaces + CloudLab első futtatása
- 2. óra: Docker alapok
- 3. óra: Dockerfile + Compose + Redis + volume + Docker Hub
- 4. óra: Kubernetes Deployment + Service
- 5. óra: scaling + self-healing + rollout
- 6. óra: GitHub Actions + Cloudflare Pages + záró kihívás

## A v2.1 legfontosabb tanári változása

A látogatásszámláló tényleges GitHub Codespaces teszt során hibásan működött a hagyományos Docker bridge hálózaton: a Redis önmagában `healthy` volt, a szolgáltatásnév feloldódott, de a `web` konténerből a `redis:6379` TCP kapcsolat timeoutolt.

A stabil tantermi megoldás:

```yaml
web:
  network_mode: "service:redis"
  environment:
    REDIS_HOST: "127.0.0.1"
```

A `web` és `redis` továbbra is két külön konténer, de közös hálózati névteret használnak. Emiatt a 8080-as port publikálása a `redis` szolgáltatásnál található. Ez elsőre szokatlan lehet, de technikailag a közös network namespace 8080-as portját tesszük elérhetővé.

## Modul 3 – kötelező ellenőrzési lánc

Ne csak azt ellenőrizd, hogy a konténerek `Up` állapotúak. A tanuló bizonyítsa a teljes kapcsolatot:

```bash
docker compose ps
docker compose exec -T redis redis-cli ping
docker compose exec -T web python -c "import redis; r=redis.Redis(host='127.0.0.1',port=6379,socket_connect_timeout=2,socket_timeout=2); print(r.ping())"
curl http://127.0.0.1:8080/api/info
```

Elvárt:

- Redis: `healthy`
- `redis-cli ping`: `PONG`
- Python teszt: `True`
- API: `"redis":true`

A `bash check-compose.sh` ugyanezt automatizálja, és a számlálót is növeli.

## Futási módok – ezt a tanulók is értsék

### `python app.py`
Nincs Redis. A web működik, a számláló nem aktív. Ez helyes.

### önálló `docker run`
Nincs Redis. A web működik, a számláló nem aktív. Ez helyes.

### `docker compose`
Redis aktív, a számlálónak működnie és növekednie kell.

### Kubernetes
A labor Kubernetes YAML-ja szándékosan csak a webalkalmazást telepíti. A Redis nincs benne; a modul fókusza Deployment, Service, scaling, self-healing és rollout.

## Repository-gyökér

A leggyakoribb kezdő hiba, hogy a tanuló az egész `cloudlab_starter` vagy `starter` mappát tölti fel. Ekkor a repository gyökerében nincs `Dockerfile`, és:

```bash
docker build -t cloudlab:1.0 .
```

`Dockerfile: no such file or directory` hibát ad.

A tanulónak ezt kell ellenőriznie:

```bash
pwd
ls -la
test -f Dockerfile && echo "OK: repository gyökér" || echo "HIBA: nincs itt Dockerfile"
```

## `.devcontainer`

A starter `.devcontainer/devcontainer.json` fájlja Docker-in-Docker és kubectl feature-t ad a Codespace-hez. Ha ezt a fájlt csak a Codespace létrehozása után teszik a repositoryba, az aktuális környezet nem feltétlenül épül újra automatikusan. Ilyenkor:

- VS Code Command Palette
- **Codespaces: Rebuild Container** / **Rebuild Container**

vagy a Codespace törlése és új létrehozása.

## Docker volume

A számláló a `redis-data` named volume-ban marad meg.

```bash
docker compose down
```

nem törli.

```bash
docker compose down -v
```

törli, ezért ezzel a számláló nullázódik.

## CI

A GitHub Actions workflow szándékosan önálló web containert tesztel a `/health` endpointtal. Ehhez Redis nem szükséges.

## Tipikus hibák

- `Dockerfile: no such file or directory` → rossz repository-könyvtár / plusz starter mappa.
- `port is already allocated` → korábbi container foglalja a portot.
- Compose alatt `redis:false` → futtasd a `check-compose.sh` scriptet; a starterben `REDIS_HOST=127.0.0.1` kell legyen.
- `docker push denied` → hibás Docker Hub név/login/tag.
- `ImagePullBackOff` → hibás vagy privát image/tag.
- `CrashLoopBackOff` → `kubectl logs` + `kubectl describe pod`.
- Cloudflare Pages 404 → output directory legyen `status-site`.

## Értékelés

A weboldal 100 pontos értékelése változatlan. A 6. bizonyítéknál külön kérjük a Redis kapcsolat és a számláló tényleges működésének bizonyítását.
