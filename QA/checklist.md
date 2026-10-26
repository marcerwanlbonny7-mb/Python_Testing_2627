# QA — Vérification finale

Date : **2026-10-26** — branche `QA` (**non fusionnée**, comme demandé).
Base vérifiée : branche `main`, dernier commit `9054d8d`.

## Exécution des vérifications

```bash
pip install -r requirements.txt
python -m pytest tests/ --cov=server --cov-report=term   # 71 passed, 100 %
python -m flake8 server.py conftest.py locustfile.py tests/   # 0 erreur
```

## Checklist

### Exigences du brief

| # | Exigence | Statut | Preuve |
|---|----------|--------|--------|
| 1 | Chaque bogue corrigé sur **sa propre branche**, un commit par bogue | ✅ | 12 branches listées dans [corrections.md](../reports/corrections.md) |
| 2 | Approche TDD (test rouge → fix → test vert) | ✅ | Chaque branche contient ses tests + le fix |
| 3 | Messages de commit explicites (ce qui a été debuggé) | ✅ | `git log` : `fix: ...` / `feat: ...` |
| 4 | Push **uniquement** sur le fork personnel | ✅ | `origin` = fork ; `upstream` = dépôt d'origine, jamais poussé |
| 5 | `flake8` : 0 erreur (norme PEP 8) | ✅ | [flake8.md](../reports/flake8.md), commit `241a175` |
| 6 | Couverture des tests ≥ 60 % | ✅ | **100 %** (124 instructions) |
| 7 | Tests séparés unit / intégration / fonctionnels | ✅ | `tests/unit` (6), `tests/integration` (61), `tests/functional` (4) |
| 8 | Rapport de test | ✅ | [tests.md](../reports/tests.md) |
| 9 | Rapport de performance Locust (6 users, load < 5 s, update < 2 s) | ✅ | [performance.md](../reports/performance.md) : 6 users, max 18,9 ms / 31 ms, **0 échec** |
| 10 | Rapport de corrections **daté** des pushes réels | ✅ | [corrections.md](../reports/corrections.md) |
| 11 | `requirements.txt` à jour (paquets installés) | ✅ | Versions réelles (Flask 3.1.3, pytest 9.1.1, flake8 7.4.1, locust 2.47.0) |
| 12 | Phase 2 : page `/points` publique lecture seule | ✅ | Route `GET` uniquement (POST → 405), sans connexion, triée |
| 13 | Branche QA à part, **non fusionnée** | ✅ | Cette branche |

### Règles métier (spécifications fonctionnelles)

| # | Règle | Statut | Test |
|---|-------|--------|------|
| 1 | 1 point = 1 place ; points réellement débités | ✅ | `test_points.py` |
| 2 | Message `Not enough points` si solde insuffisant | ✅ | `test_points.py` |
| 3 | Max 12 places cumulées par club **et** par compétition | ✅ | `test_book.py`, scénario functional |
| 4 | Ne jamais dépasser les places disponibles | ✅ | `test_place_validation.py` |
| 5 | Validation du nombre de places (entier, 1–12) | ✅ | `test_place_validation.py` |
| 6 | Messages conformes (`This competition is full`, `Great-booking complete! N places booked.`, etc.) | ✅ | `test_spec_messages.py` |
| 7 | Compétitions passées : masquées ET bloquées | ✅ | `test_past_competitions.py` |
| 8 | Connexion obligatoire avant réservation | ✅ | `test_session.py` |
| 9 | Impossible de réserver au nom d'un autre club | ✅ | `test_session.py` |
| 10 | Classement des points accessible **sans connexion** | ✅ | `test_points_board.py` |

## Écarts résiduels / limites connues

- Données en fichiers JSON (pas de base de données) — conforme au brief.
- Serveur de développement Flask (pas de serveur production) — hors périmètre.
- Après épuisement des points d'un club, les POST d'achat sont refusés par
  règle métier (réponse valide, pas une erreur technique).
