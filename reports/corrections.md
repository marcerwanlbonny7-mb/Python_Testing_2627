# Rapport des corrections

Chaque correction a été faite sur **sa propre branche**, testée (rouge →
vert), fusionnée sur `main`, puis poussée sur le fork.
Les dates et heures ci-dessous sont celles des pushes réels.

## Récapitulatif

| Date et heure (push) | Branche | Commit | Problème corrigé |
|----------------------|---------|--------|------------------|
| 2026-10-24 21:40:46 | `bug/gitignore-tests` | `5beba20` | Les tests étaient ignorés par git |
| 2026-10-24 21:41:31 | `bug/crash-email-inconnu` | `4e8c212` | Page qui plantait sur un email inconnu |
| 2026-10-26 11:32:03 | `bug/club-competition-introuvable` | `ab3ad69` | Plantage sur un nom de club/compétition inventé |
| 2026-10-26 11:58:13 | `bug/validation-places` | `7c7be38` | Réservations sans aucun contrôle du nombre de places |
| 2026-10-26 16:19:15 | `bug/gestion-points` | `12ed013` | Points jamais retirés, solde jamais vérifié |
| 2026-10-26 16:44:55 | `bug/limite-12-cumulee` | `d2036f6` | Limite de 12 places contournable en réservant deux fois |
| 2026-10-26 16:46:51 | `bug/messages-specs` | `b69e9d4` | Messages non conformes aux spécifications |
| 2026-10-26 17:18:51 | `style/flake8-cleanup` | `241a175` | 28 erreurs de style (voir rapport flake8) |
| 2026-10-26 17:36:41 | `bug/competitions-passees` | `782308c` | Réservations encore possibles dans des compétitions passées |
| 2026-10-26 18:53:32 | `bug/session-club` | `10aca08` | Réservation possible sans connexion, et au nom d'un autre club |
| 2026-10-26 19:02:42 | `bug/gestion-erreurs` | `e558f97` | Erreurs brutales (404/500, champs manquants, JSON cassé) |
| 2026-10-26 19:04:27 | `feature/points-board` | `594eaf3` | Nouveauté : tableau public des points sur `/points` |

---

## Détail de chaque correction (langage simple)

### 1. Les tests étaient ignorés git — `bug/gitignore-tests`

**Le problème :** le fichier qui décide ce que git ignore contenait la ligne
`tests/` : aucun test n'aurait jamais été enregistré dans le dépôt. Le QA
n'aurait trouvé aucun test.

**La correction :** `tests/` retiré de la liste des ignorés ; le dossier
`venv/` (installation locale) ajouté à la place.

---

### 2. Un email inconnu plantait la page — `bug/crash-email-inconnu`

**Le problème :** si le secrétaire tapait un email qui n'existe pas, l'application
plantait (écran d'erreur 500) au lieu de répondre.

**La correction :** un message « email inconnu, réessayez » s'affiche et on
retourne à la page d'accueil. Les messages d'erreur s'affichent désormais sur
la page d'accueil.

**Tests :** 3 tests (happy path + 2 cas d'erreur).

---

### 3. Un nom inventé dans l'adresse plantait l'application — `bug/club-competition-introuvable`

**Le problème :** en changeant le nom du club ou de la compétition dans
l'adresse du navigateur (ex. `/book/Fake/Fake`), l'application plantait.
Un bloc mort de code risquait un deuxième plantage.

**La correction :** message « quelque chose s'est mal passé » + retour à
la page d'accueil. Le bloc mort a été supprimé.

**Tests :** 10 tests (happy paths + adresses inventées).

---

### 4. Réservations sans aucun contrôle — `bug/validation-places`

**Le problème :** le champ « combien de places ? » acceptait tout :
`-5` donnait **plus** de places au club, `100` sur 13 places restantes
faisait tomber le compteur sous zéro, un texte plantait l'application.

**La correction :** le serveur vérifie que c'est un nombre entier, entre 1
et 12, et jamais plus que ce qu'il reste. Le formulaire a aussi des limites
visibles (`min`/`max`), et la page de réservation affiche les messages
d'erreur.

**Tests :** 7 tests, dont la preuve du bug (25 → **30** places avec -5).

---

### 5. Les points ne servaient à rien — `bug/gestion-points`

**Le problème :** les points affichés n'étaient jamais retirés quand on
réservait : c'était gratuit et illimité. Personne ne vérifiait si le club
avait assez de points.

**La correction :** chaque place coûte 1 point, le solde diminue vraiment.
Si le club n'a pas assez, il reçoit « pas assez de points » et la
réservation est refusée — sans rien changer.

**Tests :** 5 tests (débit, solde à zéro, refus, solde et places inchangés).

---

### 6. La limite de 12 places contournable — `bug/limite-12-cumulee`

**Le problème :** la règle « max 12 par club » ne s'appliquait que par
envoi : 8 puis encore 8 faisait 16 places pour le même club.

**La correction :** l'application compte le cumul des réservations de chaque
club **par compétition** : 8 + 4 = 12 passe, la moindre chose de plus est
refusée. 12 au Spring Festival n'empêche rien au Fall Classic.

**Tests :** 4 tests (cumul refusé, frontière 12 acceptée, limite par compétition).

---

### 7. Messages non conformes aux spécifications — `bug/messages-specs`

**Le problème :** quand une compétition était complète, aucun message ne le
disait (et un POST direct passait encore). La confirmation de réservation ne
disait pas combien de places avaient été achetées.

**La correction :** « This competition is full » quand il ne reste plus rien
(bloqué aussi côté serveur), et la confirmation affiche le nombre :
« Great-booking complete! 3 places booked. ».

**Tests :** 5 tests, dont le lien de réservation qui disparaît bien de la
page d'accueil quand c'est complet.

---

### 8. 28 erreurs de style — `style/flake8-cleanup`

**Le problème :** le code ne respectait pas la norme PEP 8 (espaces manquants,
lignes trop longues, indentation fausse). Le QA reproche déjà le
non-respect des normes.

**La correction :** tout le code reformatté — **0 erreur flake8** désormais.
Voir [flake8.md](flake8.md).

**Tests :** les 34 tests passent toujours (rien n'a été cassé).

---

### 9. Réservations dans des compétitions passées — `bug/competitions-passees`

**Le problème :** le site affichait des compétitions déjà terminées (dates de
2020) et permettait d'y réserver, alors que les specs n'autorisent que les
compétitions **à venir**.

**La correction :** une seule fonction vérifie la date. Les compétitions
passées n'apparaissent plus sur la page d'accueil, la page de réservation les
refuse avec « This competition has already taken place », et un envoi direct
du formulaire est bloqué pareil. Les dates de démonstration ont été mises à
jour en 2027.

**Tests :** 6 tests (liste filtrée, page de réservation bloquée, POST bloqué,
places et points inchangés en cas de refus).

---

### 10. Réservation sans connexion et au nom d'un autre club — `bug/session-club`

**Le problème :** n'importe qui pouvait réserver sans jamais se connecter, et
en modifiant le formulaire pouvait réserver **au nom d'un autre club** — un
club pouvait dépenser les points d'un autre.

**La correction :** une connexion par email est obligatoire avant toute
réservation : « Please log in first ». Chaque réservation est vérifiée contre
le club de la session : « You can only make bookings for your own club » —
et rien n'est modifié si le club ne correspond pas. La déconnexion efface
bien la session.

**Tests :** 8 nouveaux tests de sécurité (accès sans session, club différent,
POST direct sans connexion, changement de session après logout).

---

### 11. Erreurs brutales de l'application — `bug/gestion-erreurs`

**Le problème :** une URL inconnue montrait la page technique de Flask, une
erreur interne aussi, un champ manquant dans un formulaire plantait la page,
et un fichier `clubs.json`/`competitions.json` cassé faisait planter le
démarrage sans explication.

**La correction :** pages 404 et 500 personnalisées avec un lien vers
l'accueil, tous les champs de formulaire sont lus sans planter (message
d'erreur à la place), et le chargement des JSON échoue proprement avec un
message clair du type « ERROR: clubs.json is not valid JSON. ».

**Tests :** 11 nouveaux (page 404, page 500, champs manquants, fichiers
absents/corrompus).

---

### 12. Nouveauté : tableau public des points — `feature/points-board`

**Le besoin (spec) :** les specs demandent un classement public en lecture
seule des points de tous les clubs, consultable **sans connexion** pour
déterminer le club gagnant.

**La réalisation :** nouvelle route `GET /points` (aucune modification
possible — un POST renvoie 405), qui affiche les clubs **triés du plus de
points au moins de points**, avec le rang de chaque club. Un lien « View the
club leaderboard » a été ajouté sur la page d'accueil.

**Tests :** 6 tests (accès sans connexion, tous les clubs, points affichés,
ordre décroissant, méthode POST refusée, lien depuis l'accueil).

---

## Évolution du nombre de tests

| Étape | Tests |
|-------|-------|
| Après correction 1 | 3 |
| Après correction 2 | 13 |
| Après correction 3 | 20 |
| Après correction 4 | 25 |
| Après correction 5 | 29 |
| Après correction 6 | 34 |
| Après nettoyage flake8 | 34 (inchangé, tous verts) |
| Après correction 9 (compétitions passées) | 40 |
| Après correction 10 (session) | 48 |
| Après correction 11 (erreurs) | 59 |
| Après nouveauté `/points` | 65 |
