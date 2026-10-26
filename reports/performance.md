# Rapport de performance — Locust

Exécution du **2026-10-26** contre l'application locale.

## Configuration

| Paramètre | Valeur |
|-----------|--------|
| Outil | Locust 2.47.0 (mode headless) |
| Utilisateurs simultanés | **6** (spawn 6/s, conformes au brief) |
| Durée | 60 secondes |
| Cible | `http://127.0.0.1:5000` (serveur Flask local, `flask run`) |
| Scénario | `locustfile.py` (fichier livré dans le dépôt) |
| Attente entre requêtes | 1 à 2 s par utilisateur |

**Scénario testé** : connexion par email au démarrage, puis mélange
realiste de chargements de pages (`/`, `/points`, `/book/...`) et
d'écritures (`POST /purchasePlaces` — la vraie « update » du site).

## Résultats

| Type de requête | Requêtes | Échecs | Médiane | Moyenne | P95 | Max |
|-----------------|----------|--------|---------|---------|-----|-----|
| `GET /` (load) | 134 | 0 | 7 ms | 6,7 ms | 9 ms | **18,9 ms** |
| `GET /book` (load) | 45 | 0 | 7 ms | 6,7 ms | 9 ms | 11,5 ms |
| `GET /points` (load) | 51 | 0 | 7 ms | 7,0 ms | 8 ms | 17,4 ms |
| `POST /purchasePlaces` (update) | 14 | 0 | 9 ms | 8,5 ms | 12 ms | 12,4 ms |
| `POST /showSummary` (login) | 6 | 0 | 27 ms | 26,0 ms | 31 ms | 30,9 ms |
| **Total** | **250** | **0 (0,00 %)** | 7 ms | 7,3 ms | 25 ms | 30,9 ms |

Débit : **4,21 requêtes/s**, 0 échec réseau sur toute la durée.

## Conformité aux exigences

| Exigence | Seuil | Relevé | Verdict |
|----------|-------|--------|---------|
| Utilisateurs simultanés | 6 | 6 | ✅ |
| Temps de chargement | < 5 000 ms | max **18,9 ms** | ✅ |
| Temps d'update | < 2 000 ms | max **31 ms** | ✅ |
| Erreurs | 0 | 0 | ✅ |

Les deux seuils sont respectés avec une marge très large (le chargement
le plus lent est ~260× sous la limite).

## Observations

- Le POST le plus lent est la connexion (`/showSummary`, 31 ms au pire),
  car elle compare l'email à chaque club — reste très largement sous 2 s.
- Après épuisement du solde de points du club testé, les achats sont
  refusés par la règle métier : c'est une réponse métier valide (page
  d'erreur affichée), pas une erreur technique — le taux d'échec reste 0.

## Reproduction

```bash
flask run --port 5000          # terminal 1
locust -f locustfile.py --headless -u 6 -r 6 -t 60s \
       --host http://127.0.0.1:5000
```
