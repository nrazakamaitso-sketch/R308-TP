# Réutiliser la grille et les joueurs déjà écrits : on ne recopie pas
# leurs classes ici. Ces deux fichiers doivent rester dans le même dossier.
from TP2_PartieA import Grille
from TP2_PartieB import JoueurHumain, JoueurIA


def jouer_partie(joueur_x, joueur_o, afficher=True):
    #Jouer sur une nouvelle grille ; renvoyer X, O, ou None pour un nul.
    # Une nouvelle instance donne neuf cases vides à chaque nouvelle partie.
    grille = Grille()
    
    # Ce dictionnaire associe chaque symbole à l'objet qui choisit ses coups.
    # Cet objet peut être un humain ou une IA : leur méthode porte le même nom.
    joueurs = {"X": joueur_x, "O": joueur_o}
    # Cette variable indique à qui appartient le tour actuel. X commence.
    symbole = "X"

    # afficher=False permet aux tests de jouer sans remplir le terminal.
    if afficher:
        grille.afficher()

    # La boucle continue jusqu'à ce qu'un return annonce une victoire ou un nul.
    while True:
        if afficher:
            print(f"\nAu tour de {symbole}.")
        try:
            # joueurs[symbole] retrouve le joueur du tour actuel.
            # grille.tab est la liste de listes contenant les neuf cases.
            # L'affectation x, y sépare le couple renvoyé en deux coordonnées :
            # x = ligne, y = colonne, avec des indices allant de 0 à 2.
            x, y = joueurs[symbole].prochain_coup(grille.tab, symbole)
        except (TypeError, ValueError):
            # Par exemple, None ne peut pas être séparé en deux coordonnées
            # Le joueur doit renvoyer deux coordonnées. Une proposition
            # mal formée n'entraîne ni modification ni changement de tour.
            if afficher:
                print("Coup invalide : le même joueur rejoue.")
            # continue remonte au début de while sans atteindre le changement
            continue

        # Même si le joueur humain vérifie déjà ses saisies en partie B,
        # le jeu valide aussi le coup avec la méthode de la partie A.
        if not grille.jouer(x, y, symbole):
            # jouer() renvoie False si la case est occupée, les coordonnées
            # hors grille ou le symbole invalide ; elle laisse la grille intacte.
            if afficher:
                print("Coup invalide : le même joueur rejoue.")
            continue

        if afficher:
            # Ce bloc n'est atteint qu'après l'enregistrement d'un coup valide.
            print(f"{symbole} joue en ({x}, {y}).")
            grille.afficher()

        # Une victoire au dernier coup est prioritaire sur le match nul.
        if grille.est_gagnant(symbole):
            if afficher:
                print(f"Victoire de {symbole} !")
            # return termine toute la fonction et transmet le vainqueur à main().
            return symbole
        if grille.est_plein():
            if afficher:
                print("Match nul !")
            # None représente ici l'absence de vainqueur, donc le match nul.
            return None

        # Changer de joueur seulement après un coup valide non terminal.
        # Lecture : choisir O si le symbole actuel est X ; sinon choisir X.
        symbole = "O" if symbole == "X" else "X"


def main():
    # Initialiser les compteurs une seule fois, AVANT la boucle du menu.
    # Les recréer dans la boucle remettrait les scores à zéro à chaque partie.
    scores = {"X": 0, "O": 0, "nuls": 0}
    print("=== JEU DU MORPION ===")
    print("Coordonnées : ligne puis colonne, de 0 à 2. X commence.")

    # Cette seconde boucle sert à enchaîner plusieurs parties ou à quitter.
    # Elle est indépendante de la boucle qui gère les tours dans jouer_partie().
    while True:
        print("\n1. Humain (X) contre IA (O)")
        print("2. Deux humains")
        print("3. IA contre IA")
        print("0. Quitter")
        # input() renvoie du texte ; on compare donc avec "1", pas avec 1.
        # strip() enlève les espaces accidentels au début et à la fin.
        choix = input("Votre choix : ").strip()

        if choix == "0":
            print("Au revoir !")
            # break quitte la boucle du menu ; main() arrive ensuite à sa fin.
            break
        if choix == "1":
            # Deux instances différentes reçoivent les rôles X et O.
            joueur_x, joueur_o = JoueurHumain(), JoueurIA()
        elif choix == "2":
            joueur_x, joueur_o = JoueurHumain(), JoueurHumain()
        elif choix == "3":
            joueur_x, joueur_o = JoueurIA(), JoueurIA()
        else:
            print("Choix invalide : entre 0, 1, 2 ou 3.")
            # Ne pas lancer de partie si le mode saisi n'existe pas.
            continue

        # Cet appel ne rend la main qu'une fois la partie terminée.
        # Son résultat est le symbole gagnant, ou None si la partie est nulle.
        resultat = jouer_partie(joueur_x, joueur_o)
        if resultat is None:
            # += 1 signifie : reprendre la valeur actuelle et lui ajouter un.
            scores["nuls"] += 1
        else:
            # resultat vaut "X" ou "O" : il sert directement de clé au dictionnaire.
            scores[resultat] += 1
        # La lettre f permet d'insérer dans le texte les valeurs entre accolades.
        print(f"Scores : X = {scores['X']} | O = {scores['O']} | Nuls = {scores['nuls']}")
        # Retour au choix du mode : chaque partie crée une grille vide.
        # Les scores sont attachés aux symboles, même si le mode change.



# TESTS AUTOMATISÉS DE LA PARTIE C — en bas du code

import io  # Capturer les messages imprimés dans une chaîne de caractères.
import random
import sys  # Lire les options données après le nom du fichier, dont --test.
import unittest  # Organiser les tests et signaler leurs réussites ou leurs échecs.
from contextlib import redirect_stdout  # Rediriger temporairement les print().
from unittest.mock import patch  # Remplacer une fonction pendant un test seulement.


class JoueurProgramme:
    """Doublure de test : proposer une suite de coups connue à l'avance."""
    def __init__(self, coups):
        # iter() prépare un parcours des coups : chaque next() fournira le suivant.
        self.coups = iter(coups)
        # Garder une trace des tours pour vérifier que le bon joueur est appelé.
        self.symboles = []
        self.tab = None

    def prochain_coup(self, tab, symbole):
        # Conserver la référence de la grille permet de lire son état final.
        self.tab = tab
        self.symboles.append(symbole)
        # Aucun input ni hasard : on connaît exactement les coups de ce test.
        return next(self.coups)


# unittest découvre automatiquement les méthodes dont le nom commence par test_.
class TestsJeuComplet(unittest.TestCase):
    def test_victoire_x_et_alternance(self):
        # X remplit la première ligne pendant que O joue sur la deuxième.
        x = JoueurProgramme([(0, 0), (0, 1), (0, 2)])
        o = JoueurProgramme([(1, 0), (1, 1)])
        # assertEqual compare le résultat obtenu avec le résultat attendu.
        self.assertEqual(jouer_partie(x, o, afficher=False), "X")
        self.assertEqual(x.symboles, ["X"] * 3)
        self.assertEqual(o.symboles, ["O"] * 2)
        self.assertEqual(x.tab[0], ["X", "X", "X"])

    def test_victoire_o(self):
        # Cette fois, X ne s'aligne pas et O remplit toute la deuxième ligne.
        x = JoueurProgramme([(0, 0), (0, 1), (2, 2)])
        o = JoueurProgramme([(1, 0), (1, 1), (1, 2)])
        self.assertEqual(jouer_partie(x, o, afficher=False), "O")

    def test_match_nul(self):
        # Ces neuf coups remplissent la grille sans aligner trois symboles identiques.
        x = JoueurProgramme([(0, 0), (0, 2), (1, 0), (2, 1), (2, 2)])
        o = JoueurProgramme([(0, 1), (1, 1), (1, 2), (2, 0)])
        # assertIsNone vérifie le résultat prévu pour un match nul.
        self.assertIsNone(jouer_partie(x, o, afficher=False))
        # all() vaut True si chaque case examinée est différente d'un espace.
        self.assertTrue(all(case != " " for ligne in x.tab for case in ligne))

    def test_coups_invalides_ne_changent_pas_de_joueur(self):
        # X propose d'abord deux lignes hors grille ; O tente ensuite de prendre
        # la case déjà occupée par X. Chacun doit pouvoir rejouer immédiatement.
        x = JoueurProgramme([(3, 0), (-1, 0), (0, 0), (0, 1), (0, 2)])
        o = JoueurProgramme([(0, 0), (1, 0), (1, 1)])
        # StringIO joue le rôle d'un terminal en mémoire pour lire les messages.
        sortie = io.StringIO()
        with redirect_stdout(sortie):
            self.assertEqual(jouer_partie(x, o), "X")
        self.assertEqual(sortie.getvalue().count("Coup invalide"), 3)
        self.assertEqual(x.tab[0], ["X", "X", "X"])
        self.assertEqual(x.tab[1], ["O", "O", " "])

    def test_coup_mal_forme_puis_reprise(self):
        # Tester les deux erreurs de décomposition traitées par le bloc except.
        x = JoueurProgramme([None, (0,), (0, 0), (0, 1), (0, 2)])
        o = JoueurProgramme([(1, 0), (1, 1)])
        self.assertEqual(jouer_partie(x, o, afficher=False), "X")

    def test_victoire_sur_la_derniere_case_prioritaire_sur_nul(self):
        # X complète la diagonale au neuvième coup : la grille pleine n'annule
        # pas cette victoire. Ce test vérifie l'ordre des deux contrôles de fin.
        x = JoueurProgramme([(0, 0), (0, 2), (1, 1), (2, 1), (2, 2)])
        o = JoueurProgramme([(0, 1), (1, 0), (1, 2), (2, 0)])
        self.assertEqual(jouer_partie(x, o, afficher=False), "X")
        self.assertTrue(all(case != " " for ligne in x.tab for case in ligne))

    def test_vingt_parties_ia_contre_ia(self):
        # Une graine par partie rend les tirages reproductibles et conserve
        # l'état aléatoire global. Les vraies IA des parties B sont utilisées.
        for graine in range(20):
            # subTest identifie la partie précise si une vérification échoue.
            with self.subTest(graine=graine):
                grille = Grille()
                tirage = random.Random(graine)
                # Faire utiliser cette grille au jeu pour pouvoir l'inspecter.
                # lambda: grille est une fonction qui renvoie notre instance.
                with patch.dict(jouer_partie.__globals__, Grille=lambda: grille):
                    # Remplacer le tirage pendant ce bloc uniquement ; à la sortie,
                    # patch rétablit la fonction random.choice d'origine.
                    with patch.object(random, "choice", side_effect=tirage.choice):
                        resultat = jouer_partie(JoueurIA(), JoueurIA(), afficher=False)
                # Compter les coups réellement inscrits pour contrôler l'alternance.
                nb_x = sum(ligne.count("X") for ligne in grille.tab)
                nb_o = sum(ligne.count("O") for ligne in grille.tab)
                self.assertLessEqual(nb_x + nb_o, 9)
                self.assertIn(nb_x - nb_o, (0, 1))
                # Une partie nulle doit être pleine sans vainqueur ; sinon le
                # symbole renvoyé doit correspondre à un véritable alignement.
                if resultat is None:
                    self.assertTrue(grille.est_plein())
                    self.assertFalse(grille.est_gagnant("X"))
                    self.assertFalse(grille.est_gagnant("O"))
                else:
                    self.assertIn(resultat, ("X", "O"))
                    self.assertTrue(grille.est_gagnant(resultat))
                    self.assertFalse(grille.est_gagnant("O" if resultat == "X" else "X"))
                    self.assertEqual(nb_x - nb_o, 1 if resultat == "X" else 0)

    def test_nouvelle_grille_pour_chaque_partie(self):
        # Deux parties identiques doivent réussir sur deux grilles indépendantes.
        grilles = []
        for _ in range(2):
            x = JoueurProgramme([(0, 0), (0, 1), (0, 2)])
            o = JoueurProgramme([(1, 0), (1, 1)])
            self.assertEqual(jouer_partie(x, o, afficher=False), "X")
            grilles.append(x.tab)
        # assertIsNot vérifie qu'il s'agit bien de deux objets distincts.
        self.assertIsNot(grilles[0], grilles[1])

    def test_menu_modes_scores_et_choix_invalide(self):
        # Simuler les touches saisies : erreur, trois modes, puis sortie.
        sortie = io.StringIO()
        with patch("builtins.input", side_effect=["9", "1", "2", "3", "0"]):
            with patch.dict(main.__globals__, jouer_partie=lambda x, o: next(resultats)):
                # Éviter de jouer réellement : les trois résultats imposés servent
                # à vérifier uniquement le menu et l'addition des scores.
                resultats = iter(["X", None, "O"])
                with redirect_stdout(sortie):
                    main()
        self.assertIn("Choix invalide", sortie.getvalue())
        self.assertIn("Scores : X = 1 | O = 1 | Nuls = 1", sortie.getvalue())
        self.assertIn("Au revoir !", sortie.getvalue())


# Ce bloc est exécuté quand on lance le fichier directement, pas quand une
# autre partie l'importe. L'import n'ouvre donc pas de menu et ne lance aucun test.
if __name__ == "__main__":
    if "--test" in sys.argv[1:]:
        # Retirer notre option --test avant de transmettre les arguments à unittest.
        # verbosity=2 affiche le nom de chaque test et son résultat.
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    else:
        # Sans l'option --test, démarrer normalement le menu interactif.
        main()
