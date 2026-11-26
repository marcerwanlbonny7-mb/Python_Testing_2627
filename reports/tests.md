# Rapport de test

Exécution du **2026-11-26** sur le dépôt `main`.

## Comment lancer les tests

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python -m pytest tests/ -v --cov=server --cov-report=term
python -m flake8 server.py conftest.py tests/
```

## Résultat global

| Indicateur | Résultat | Exigence |
|------------|----------|----------|
| Tests exécutés | **81 — tous verts** | — |
| Couverture `server.py` | **100 %** (153 instructions, 0 manquantes) | ≥ 60 % |
| Erreurs flake8 | **0** | 0 (norme PEP 8) |

## Structure des tests

Les tests sont regroupés en trois dossiers séparés comme demandé :

### `tests/unit/` — logique pure, sans serveur (13 tests)

| Fichier | Ce qu'il vérifie |
|---------|------------------|
| `test_data_loading.py` | Chargement de `clubs.json` / `competitions.json` : fichier absent, corrompu, clé manquante → message d'erreur clair |
| `test_saving.py` | Sauvegarde roundtrip de clubs, compétitions et bookings ; `bookings.json` absent → `{}` ; fichier corrompu → message clair |
| `test_app_config.py` | `secret_key` configurée (variable d'env `SECRET_KEY` ou fallback) |

### `tests/integration/` — routes et interactions (64 tests)

| Fichier | Ce qu'il vérifie |
|---------|------------------|
| `test_show_summary.py` | Connexion par email (connu / inconnu) |
| `test_session.py` | Connexion obligatoire, isolation des clubs, logout |
| `test_book.py` | Page de réservation (existence, invente, passée, sans session) |
| `test_place_validation.py` | Nombre de places : entier, bornes 1–12, places restantes |
| `test_purchase_places.py` | Achat de places : succès, erreurs, messages |
| `test_points.py` | Débit des points et refus « Not enough points » |
| `test_points_board.py` | Page `/points` : publique, triée, lecture seule |
| `test_spec_messages.py` | Messages conformes aux spécifications |
| `test_past_competitions.py` | Compétitions passées : masquées et bloquées |
| `test_error_pages.py` | Pages 404/500 personnalisées, champs de formulaire manquants |
| `test_persistence.py` | Après achat : points, places et compteur écrits sur disque |

### `tests/functional/` — scénarios bout-en-bout (4 tests)

| Fichier | Scénario |
|---------|----------|
| `test_full_journey.py` | Accueil → connexion → réservation → confirmation → points/places mis à jour |
| `test_full_journey.py` | Refus du cumul > 12 : rien n'est modifié (points et places inchangés) |
| `test_full_journey.py` | Email erroné → message → nouvelle connexion réussie |
| `test_full_journey.py` | Visiteur : accueil → classement `/points` public → retour |

## Évolution

| Étape | Tests |
|-------|-------|
| Départ (tests de base) | 3 |
| Après les 7 premières corrections | 34 |
| Après compétitions passées | 40 |
| Après session/connexion | 48 |
| Après gestion des erreurs | 59 |
| Après classement `/points` | 65 |
| Après restructuration unit/integration/functional | 71 |
| Après persistance JSON | 79 |
| Après secret key env | **81** |
