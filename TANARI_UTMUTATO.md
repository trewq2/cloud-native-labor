# Cloud Native Labor – tanári útmutató

## Javasolt időbeosztás
- 1. óra: GitHub Codespaces + a CloudLab első futtatása
- 2. óra: Docker alapok
- 3. óra: Dockerfile + Compose + Redis + Docker Hub
- 4. óra: Kubernetes Deployment + Service
- 5. óra: scaling + self-healing + rollout
- 6. óra: GitHub Actions + Cloudflare Pages + záró kihívás indítása

## Fontos előkészület
A tanulóknak GitHub, Docker Hub és a Cloudflare-modulhoz Cloudflare fiók szükséges.
A Kubernetes-modul böngészős laborban is végrehajtható.

## Két tanóra közötti folytatás
A Codespaces újranyitható a repositoryból.
A Docker konténerállapot nem tekintendő beadandó állapotnak: szükség esetén újraépíthető.
Az online Kubernetes-labor munkamenete lejárhat; ilyenkor a tanuló új klaszteren újra alkalmazza a k8s.yaml fájlt.

## Tipikus hibák
- Docker push denied: hibás felhasználónév/login/tag.
- ImagePullBackOff: hibás vagy privát Docker Hub image/tag.
- CrashLoopBackOff: `kubectl logs` és `kubectl describe pod`.
- Port foglalt: `docker ps`, majd másik host port vagy régi container törlése.
- Cloudflare Pages 404: hibás output directory; a laborban `status-site`.

## Értékelés
A weboldal végén lévő 100 pontos értékelés használható. A képernyőképek célja nem a mennyiség, hanem az állapot hiteles bizonyítása.
