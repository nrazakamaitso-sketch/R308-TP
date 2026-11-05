# R308 — Travaux pratiques Python

Un seul dépôt, avec un sous-dossier par TP. Les fichiers des parties sont
regroupés dans leur TP pour permettre les imports entre modules.

```text
TP1/
    TP1_PartieA.py
    TP1_PartieB.py
    TP1_PartieC.py
    TP1_PartieD.py
    mots.txt
TP3/
    TP3_PartieA.py
    TP3_PartieB.py
    TP3_PartieC.py
    TP3_PartieD.py
```

Le TP2 n'est pas inclus : aucun fichier correspondant n'était présent dans
le dossier source R308.

## Exécution

Python 3 suffit ; aucune dépendance externe n'est nécessaire.
Depuis la racine du dépôt, ouvrir le dossier du TP voulu avant l'exécution :

```powershell
cd TP1
python TP1_PartieA.py
python TP1_PartieB.py
```

Le fichier `TP1/mots.txt` contient un mot par ligne et sert aux parties C et D.
La partie C le cherche dans le dossier courant : l'exécuter depuis `TP1`.
La partie D le retrouve à côté de son fichier Python.

Pour jouer au pendu, depuis le dossier `TP1` :

```powershell
python TP1_PartieD.py
python TP1_PartieD.py --test
```

Sept erreurs entraînent la défaite. Chaque bonne lettre révèle toutes ses
positions. Une lettre déjà proposée ou une saisie invalide n'ajoute pas
d'erreur. Le masque, les erreurs et les lettres proposées sont affichés
à chaque tour. Les neuf tests automatisés sont placés en bas du code.
Les bonus facultatifs (dessin ASCII, mode deux joueurs) ne sont pas inclus.

Pour le menu de bibliothèque, depuis la racine du dépôt :

```powershell
cd TP3
python TP3_PartieD.py
```

Le menu charge `livres.csv` au démarrage et sauvegarde avec le choix 6.
Le CSV est créé dans le dossier courant. Les utilisateurs sans emprunt ne
sont pas conservés après un redémarrage avec le format de la partie C.

## Tests de la partie D

Depuis le dossier `TP3` :

```powershell
python TP3_PartieD.py --test
```

Les tests sont regroupés en bas de `TP3_PartieD.py`.
Les neuf tests couvrent le menu, les années et choix invalides, la sauvegarde,
le rechargement, le retour d'un livre après redémarrage et la limite de
persistance des utilisateurs sans emprunt. Les sauvegardes de test utilisent
un dossier temporaire.

## Historique

Chaque partie est ajoutée dans un commit distinct, nommé par exemple
`TP3 partie A`. Cet historique correspond à l'import des fichiers existants
dans le monorepo ; il ne reconstitue pas leurs dates de rédaction.
