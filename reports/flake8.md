# Rapport Flake8

## Commande exécutée

```bash
flake8 server.py conftest.py tests/
```

## Résultat

**0 erreur, 0 warning.**

```
0
```

## État avant nettoyage

**28 problèmes** détectés sur le code :

| Code | Signification | Nombre |
|------|---------------|--------|
| E231 | virgule sans espace après elle | 11 |
| E501 | ligne trop longue (> 79 caractères) | 7 |
| E111 / E117 | indentation fausse (5 espaces au lieu de 4) | 4 |
| E302 | moins de 2 lignes vides entre deux fonctions | 2 |
| W292 | fichier sans retour à la ligne final | 1 |
| Divers | lignes d'import et d'appels de fonctions | 3 |

## Correction

Tous les problèmes ont été corrigés **sans rien casser** : les 34 tests
passaient avant et passent toujours après.

## Commit concerné

| Commit | Message |
|--------|---------|
| `241a175` | style: fix all flake8 warnings to comply with PEP 8 |

## Fichiers vérifiés

- `server.py`
- `conftest.py`
- `tests/` (6 fichiers de tests)

## Configuration

Flake8 par défaut : norme **PEP 8**, lignes de 79 caractères maximum.
