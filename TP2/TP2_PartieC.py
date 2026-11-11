"""TP2, partie C : jeu complet de morpion.

Jouer : python TP2_PartieC.py
Tests en bas du code : python TP2_PartieC.py --test
"""

from TP2_PartieA import Grille
from TP2_PartieB import JoueurHumain, JoueurIA


def jouer_partie(joueur_x, joueur_o, afficher=True):
    """Jouer sur une nouvelle grille ; renvoyer X, O, ou None pour un nul."""
    grille = Grille()
    joueurs = {"X": joueur_x, "O": joueur_o}
    symbole = "X"

    if afficher:
        grille.afficher()

    while True:
        if afficher:
            print(f"\nAu tour de {symbole}.")
        try:
            x, y = joueurs[symbole].prochain_coup(grille.tab, symbole)
        except (TypeError, ValueError):
            # Le joueur doit renvoyer deux coordonnées. Une proposition
            # mal formée n'entraîne ni modification ni changement de tour.
            if afficher:
                print("Coup invalide : le même joueur rejoue.")
            continue

        # Même si le joueur humain vérifie déjà ses saisies en partie B,
        # le jeu valide aussi le coup avec la méthode de la partie A.
        if not grille.jouer(x, y, symbole):
            if afficher:
                print("Coup invalide : le même joueur rejoue.")
            continue

        if afficher:
            print(f"{symbole} joue en ({x}, {y}).")
            grille.afficher()

        # Une victoire au dernier coup est prioritaire sur le match nul.
        if grille.est_gagnant(symbole):
            if afficher:
                print(f"Victoire de {symbole} !")
            return symbole
        if grille.est_plein():
            if afficher:
                print("Match nul !")
            return None

        # Changer de joueur seulement après un coup valide non terminal.
        symbole = "O" if symbole == "X" else "X"


def main():
    """Choisir un mode et conserver les scores pendant cette exécution."""
    scores = {"X": 0, "O": 0, "nuls": 0}
    print("=== JEU DU MORPION ===")
    print("Coordonnées : ligne puis colonne, de 0 à 2. X commence.")

    while True:
        print("\n1. Humain (X) contre IA (O)")
        print("2. Deux humains")
        print("3. IA contre IA")
        print("0. Quitter")
        choix = input("Votre choix : ").strip()

        if choix == "0":
            print("Au revoir !")
            break
        if choix == "1":
            joueur_x, joueur_o = JoueurHumain(), JoueurIA()
        elif choix == "2":
            joueur_x, joueur_o = JoueurHumain(), JoueurHumain()
        elif choix == "3":
            joueur_x, joueur_o = JoueurIA(), JoueurIA()
        else:
            print("Choix invalide : entre 0, 1, 2 ou 3.")
            continue

        resultat = jouer_partie(joueur_x, joueur_o)
        if resultat is None:
            scores["nuls"] += 1
        else:
            scores[resultat] += 1
        print(f"Scores : X = {scores['X']} | O = {scores['O']} | Nuls = {scores['nuls']}")
        # Retour au choix du mode : chaque partie crée une grille vide.
        # Les scores sont attachés aux symboles, même si le mode change.


# ============================================================
# TESTS AUTOMATISÉS DE LA PARTIE C — en bas du code
# ============================================================
import io
import random
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch


class JoueurProgramme:
    """Doublure de test : proposer une suite de coups connue à l'avance."""
    def __init__(self, coups):
        self.coups = iter(coups)
        self.symboles = []
        self.tab = None

    def prochain_coup(self, tab, symbole):
        self.tab = tab
        self.symboles.append(symbole)
        return next(self.coups)


class TestsJeuComplet(unittest.TestCase):
    def test_victoire_x_et_alternance(self):
        x = JoueurProgramme([(0, 0), (0, 1), (0, 2)])
        o = JoueurProgramme([(1, 0), (1, 1)])
        self.assertEqual(jouer_partie(x, o, afficher=False), "X")
        self.assertEqual(x.symboles, ["X"] * 3)
        self.assertEqual(o.symboles, ["O"] * 2)
        self.assertEqual(x.tab[0], ["X", "X", "X"])

    def test_victoire_o(self):
        x = JoueurProgramme([(0, 0), (0, 1), (2, 2)])
        o = JoueurProgramme([(1, 0), (1, 1), (1, 2)])
        self.assertEqual(jouer_partie(x, o, afficher=False), "O")

    def test_match_nul(self):
        x = JoueurProgramme([(0, 0), (0, 2), (1, 0), (2, 1), (2, 2)])
        o = JoueurProgramme([(0, 1), (1, 1), (1, 2), (2, 0)])
        self.assertIsNone(jouer_partie(x, o, afficher=False))
        self.assertTrue(all(case != " " for ligne in x.tab for case in ligne))

    def test_coups_invalides_ne_changent_pas_de_joueur(self):
        x = JoueurProgramme([(3, 0), (-1, 0), (0, 0), (0, 1), (0, 2)])
        o = JoueurProgramme([(0, 0), (1, 0), (1, 1)])
        sortie = io.StringIO()
        with redirect_stdout(sortie):
            self.assertEqual(jouer_partie(x, o), "X")
        self.assertEqual(sortie.getvalue().count("Coup invalide"), 3)
        self.assertEqual(x.tab[0], ["X", "X", "X"])
        self.assertEqual(x.tab[1], ["O", "O", " "])

    def test_coup_mal_forme_puis_reprise(self):
        x = JoueurProgramme([None, (0,), (0, 0), (0, 1), (0, 2)])
        o = JoueurProgramme([(1, 0), (1, 1)])
        self.assertEqual(jouer_partie(x, o, afficher=False), "X")

    def test_victoire_sur_la_derniere_case_prioritaire_sur_nul(self):
        x = JoueurProgramme([(0, 0), (0, 2), (1, 1), (2, 1), (2, 2)])
        o = JoueurProgramme([(0, 1), (1, 0), (1, 2), (2, 0)])
        self.assertEqual(jouer_partie(x, o, afficher=False), "X")
        self.assertTrue(all(case != " " for ligne in x.tab for case in ligne))

    def test_vingt_parties_ia_contre_ia(self):
        # Une graine par partie rend les tirages reproductibles et conserve
        # l'état aléatoire global. Les vraies IA des parties B sont utilisées.
        for graine in range(20):
            with self.subTest(graine=graine):
                grille = Grille()
                tirage = random.Random(graine)
                with patch.dict(jouer_partie.__globals__, Grille=lambda: grille):
                    with patch.object(random, "choice", side_effect=tirage.choice):
                        resultat = jouer_partie(JoueurIA(), JoueurIA(), afficher=False)
                nb_x = sum(ligne.count("X") for ligne in grille.tab)
                nb_o = sum(ligne.count("O") for ligne in grille.tab)
                self.assertLessEqual(nb_x + nb_o, 9)
                self.assertIn(nb_x - nb_o, (0, 1))
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
        grilles = []
        for _ in range(2):
            x = JoueurProgramme([(0, 0), (0, 1), (0, 2)])
            o = JoueurProgramme([(1, 0), (1, 1)])
            self.assertEqual(jouer_partie(x, o, afficher=False), "X")
            grilles.append(x.tab)
        self.assertIsNot(grilles[0], grilles[1])

    def test_menu_modes_scores_et_choix_invalide(self):
        sortie = io.StringIO()
        with patch("builtins.input", side_effect=["9", "1", "2", "3", "0"]):
            with patch.dict(main.__globals__, jouer_partie=lambda x, o: next(resultats)):
                resultats = iter(["X", None, "O"])
                with redirect_stdout(sortie):
                    main()
        self.assertIn("Choix invalide", sortie.getvalue())
        self.assertIn("Scores : X = 1 | O = 1 | Nuls = 1", sortie.getvalue())
        self.assertIn("Au revoir !", sortie.getvalue())


if __name__ == "__main__":
    if "--test" in sys.argv[1:]:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    else:
        main()
