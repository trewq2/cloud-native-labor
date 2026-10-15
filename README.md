# Cloud Native Labor v2.1 – GitHub Pages

Komplex, **6 × 45 perces** oktatói weboldal a **Szerverek és felhőszolgáltatások** tantárgyhoz.

## Mi változott a v2.1 kiadásban?

A csomag a tényleges GitHub Codespaces teszt alapján frissült. A legfontosabb javítás a Docker Compose + Redis látogatásszámláló.

- Codespaces / Docker-in-Docker környezetben nem támaszkodunk a `web -> redis:6379` bridge routingra.
- A `web` szolgáltatás `network_mode: "service:redis"` beállítást használ.
- A Flask alkalmazás Compose módban a `127.0.0.1:6379` címen éri el a Redist.
- A `compose.yaml` Redis healthchecket tartalmaz.
- Az `app.py` különbséget tesz a **Redis nincs konfigurálva** és a **Redis kapcsolati hiba** között.
- Az `/api/info` diagnosztikai adatokat is visszaad.
- Új `check-compose.sh` ellenőrző script készült.
- Egyértelmű lett, hogy a starter ZIP **tartalma a tanulói repository gyökerébe** kerül.
- A `.github` és `.devcontainer` ponttal kezdődő mappák feltöltésére külön útmutató került az oldalra.
- A Kubernetes-rész külön jelzi, hogy ott a Redis hiánya szándékos.

## Témák

- GitHub Codespaces
- Docker image és container
- Dockerfile
- Docker Compose + Redis
- volume és hálózat
- Docker Hub
- Kubernetes Deployment és Service
- skálázás, self-healing, rollout
- GitHub Actions CI
- Cloudflare Pages

## A tanári weboldal fájljai

- `index.html`
- `styles.css`
- `script.js`
- `downloads/cloudlab_starter.zip` – ezt kapják a tanulók
- `starter/` – ugyanennek a kibontott, ellenőrizhető változata
- `TANARI_UTMUTATO.md`
- `FRISSITES_MEGLEVO_REPOHOZ.md`
- `CHANGELOG.md`

## GitHub Pages publikálás

1. Hozz létre egy külön repositoryt az **oktatói weboldalnak**.
2. A csomag teljes tartalmát töltsd fel ebbe a repositoryba.
3. GitHub → **Settings → Pages**.
4. Source: **Deploy from a branch**.
5. Branch: `main`.
6. Folder: `/(root)`.
7. Save.

> Az oktatói weboldal repositoryja és a tanulói `cloud-native-labor` repository két külön dolog. A tanulók a weboldalról letöltött `cloudlab_starter.zip` tartalmát teszik a saját repositoryjuk gyökerébe.

## Tanulói repository helyes szerkezete

```text
cloud-native-labor/
├── app.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── k8s.yaml
├── check-compose.sh
├── status-site/
├── .devcontainer/
└── .github/
```

Nem helyes:

```text
cloud-native-labor/
└── starter/
    ├── Dockerfile
    └── ...
```

## Gyors Compose teszt

A tanulói repository gyökerében:

```bash
docker compose down --remove-orphans
docker compose up -d --build --force-recreate
bash check-compose.sh
```

A helyes ellenőrzések között megjelenik:

```text
PONG
Redis PING: True
```

és az `/api/info` válaszban:

```json
"redis": true
```

## Megjegyzés

A külső szolgáltatások ingyenes keretei és felületei idővel változhatnak.
