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
TP2/
    TP2_PartieA.py
    TP2_PartieB.py
    TP2_PartieC.py
TP3/
    TP3_PartieA.py
    TP3_PartieB.py
    TP3_PartieC.py
    TP3_PartieD.py
    TP3_PartieE.py
```

Les trois parties du TP2 sont disponibles : A (grille), B (joueurs)
et C (jeu complet).

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

## Partie E du TP3 : extensions facultatives

Depuis `TP3`, lancer `python TP3_PartieE.py` pour ouvrir le menu enrichi.
Les choix 1 à 6 restent ceux de la partie D ; 7 recherche les livres par
auteur (recherche partielle, sans distinction majuscules/minuscules),
8 exporte la bibliothèque vers `bibliotheque.json` dans le dossier courant.
Le défi supplémentaire des statistiques est distinct de cette partie E.

La classe `BibliothequeEtendue` hérite de `BibliothequeCSV`. Sa limite est
de trois emprunts par utilisateur par défaut, car l'énoncé ne fixe pas de
nombre. Elle peut être changée avec `BibliothequeEtendue(limite_emprunts=5)`.
Dans le menu, modifier la valeur passée au constructeur dans `main()`.
Rendre un livre libère une place ; les emprunts rechargés du CSV comptent
également dans la limite. La limite est un réglage du programme, non du CSV.

L'export JSON contient les livres, les utilisateurs (y compris sans emprunt)
et la limite configurée. Il n'est pas rechargé automatiquement : le menu
continue de charger et sauvegarder le CSV, avec sa limite de persistance
des utilisateurs sans emprunt.

Les onze tests sont en bas de `TP3_PartieE.py` :

```powershell
python TP3_PartieE.py --test
```

## TP2 : morpion, étape 1 — la grille

La classe `Grille` de `TP2/TP2_PartieA.py` utilise une liste de trois listes.
Les coordonnées commencent à 0 : `x` est la ligne, `y` la colonne.
`jouer(x, y, joueur)` renvoie True si X ou O est placé dans une case libre,
False pour un coup invalide, sans modifier la grille. `est_gagnant(j)`
vérifie lignes, colonnes et diagonales. `est_plein()` indique si la grille
ne contient plus de case libre.

Depuis la racine du dépôt :

```powershell
cd TP2
python TP2_PartieA.py
python TP2_PartieA.py --test
```

Le premier lancement affiche le jeu d'essai de l'énoncé ; il ne lance pas
encore de partie interactive. Les neuf tests sont en bas du code.

## TP2 : morpion, étape 2 — les joueurs

`JoueurHumain` et `JoueurIA` possèdent la même méthode
`prochain_coup(tab, symbole)`. Passer `grille.tab` comme premier argument.
La méthode renvoie un tuple (ligne, colonne) sans modifier la grille ;
le programme appelant applique ensuite le coup avec `grille.jouer()`.

Le joueur humain redemande les coordonnées après une saisie non numérique,
un coup hors grille ou une case occupée. L'IA tire au hasard parmi les
cases libres. Sur une grille pleine, les deux lèvent ValueError ;
la partie C détecte donc la fin de partie avant de demander un coup.

Depuis le dossier `TP2` :

```powershell
python TP2_PartieB.py
python TP2_PartieB.py --test
```

Le lancement normal montre un coup humain puis un coup IA, sans boucle
de partie complète. Les neuf tests sont placés en bas du fichier.

## TP2 : morpion, étape 3 — le jeu complet

Depuis le dossier `TP2` :

```powershell
python TP2_PartieC.py
python TP2_PartieC.py --test
```

Le menu propose humain contre IA, deux humains et IA contre IA ; 0 quitte.
X commence et les coordonnées vont de 0 à 2 (ligne puis colonne).
La fonction `jouer_partie(joueur_x, joueur_o)` crée une grille vide, alterne
les joueurs après un coup valide et renvoie "X", "O", ou None pour un nul.
Un coup invalide fait rejouer le même joueur. Une victoire sur la neuvième
case est reconnue avant le test de match nul.

Les scores de X, O et des matchs nuls sont conservés entre les parties
pendant cette exécution, même si le mode change. Ils ne sont pas sauvegardés
sur disque. Chaque nouvelle partie repart sur une grille vide.

Les neuf tests sont en bas du code, dont vingt parties IA contre IA
reproductibles, la reprise après coups invalides, les victoires et le nul.
Le bonus de l'IA qui gagne ou bloque sera traité séparément.

## Historique des commits

Chaque partie est ajoutée dans un commit distinct, nommé par exemple
`TP3 partie A`. Cet historique correspond à l'import des fichiers existants
dans le monorepo ; il ne reconstitue pas leurs dates de rédaction.
