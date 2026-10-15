# CloudLab starter – Codespaces kompatibilis változat

A projektet a repository **gyökerébe** töltsd fel. Ne legyen egy plusz `starter/` vagy `cloudlab_starter/` könyvtár a repository gyökerében.

Helyes szerkezet:

```text
cloud-native-labor/
├── app.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── k8s.yaml
├── status-site/
├── .devcontainer/
└── .github/
```

## 1. Gyors ellenőrzés Codespaces-ben

```bash
pwd
ls -la
```

A `Dockerfile` és a `compose.yaml` legyen az aktuális könyvtárban.

## 2. Python mód

```bash
python -m pip install -r requirements.txt
python app.py
```

Ebben a módban nincs Redis. Ez **nem hiba**. A `/health` működik, a számláló csak Compose módban aktív.

## 3. Önálló Docker container

```bash
docker build -t cloudlab:1.0 .
docker run --rm -p 8080:8080 cloudlab:1.0
```

Itt sincs Redis, ezért a számláló nem aktív.

## 4. Docker Compose + Redis

A Compose fájl Codespaces / Docker-in-Docker kompatibilis. A `web` container a `redis` hálózati névterét használja:

```yaml
network_mode: "service:redis"
```

A Flask alkalmazás így a Redist ezen éri el:

```text
127.0.0.1:6379
```

Indítás:

```bash
docker compose down --remove-orphans
docker compose up -d --build --force-recreate
docker compose ps
```

Redis teszt:

```bash
docker compose exec -T redis redis-cli ping
```

Elvárt: `PONG`.

Python → Redis kapcsolat:

```bash
docker compose exec -T web python -c "import redis; r=redis.Redis(host='127.0.0.1',port=6379,socket_connect_timeout=2,socket_timeout=2); print(r.ping())"
```

Elvárt: `True`.

API:

```bash
curl http://127.0.0.1:8080/api/info
```

Elvárt: `"redis":true`.

Számláló teszt:

```bash
curl -s http://127.0.0.1:8080/ >/dev/null
curl -s http://127.0.0.1:8080/ >/dev/null
docker compose exec -T redis redis-cli GET cloudlab_visits
```

A számnak növekednie kell.

## 5. Volume

A sima:

```bash
docker compose down
```

nem törli a `redis-data` volume-ot. A számláló újraindítás után folytatódik.

Csak akkor használd ezt, ha szándékosan nullázni akarod:

```bash
docker compose down -v
```

## 6. Kubernetes

A `k8s.yaml` ebben a laborban csak a webalkalmazást telepíti. Redist nem telepít, ezért Kubernetesben a számláló nem aktív. Ez szándékos: a modul fókusza a Deployment, Service, scaling, self-healing és rollout.
