class Grille:
    def __init__(self):
        # Chaque ligne est une liste différente ; une case libre vaut " ".
        self.tab = [[" " for colonne in range(3)] for ligne in range(3)]

    def afficher(self):
        #Afficher la grille avec des séparateurs lisibles.
        for x in range(3):
            print(" " + " | ".join(self.tab[x]))
            if x < 2:
                print("-----------")

    def jouer(self, x, y, joueur):
        #Placer X ou O ; renvoyer False si le coup est invalide. x représente la ligne et y la colonne, de 0 à 2 inclus.
        #Un refus ne modifie jamais la grille.
        # Vérifier les coordonnées avant de lire la case. En Python, -1
        # serait sinon interprété comme la dernière ligne ou colonne.
        if type(x) is not int or type(y) is not int:
            return False
        if not (0 <= x < 3 and 0 <= y < 3):
            return False
        if joueur not in ("X", "O"):
            return False
        if self.tab[x][y] != " ":
            return False

        self.tab[x][y] = joueur
        return True

    def est_gagnant(self, j):
        #Vérifier les trois lignes, trois colonnes et deux diagonales.
        if j not in ("X", "O"):
            return False

        for x in range(3):
            if all(self.tab[x][y] == j for y in range(3)):
                return True

        for y in range(3):
            if all(self.tab[x][y] == j for x in range(3)):
                return True

        # Diagonale principale : (0, 0), (1, 1), (2, 2).
        if all(self.tab[i][i] == j for i in range(3)):
            return True
        # Diagonale inverse : (0, 2), (1, 1), (2, 0).
        if all(self.tab[i][2 - i] == j for i in range(3)):
            return True
        return False

    def est_plein(self):
        #Renvoyer True lorsqu'il ne reste aucune case libre.
        for ligne in self.tab:
            if " " in ligne:
                return False
        return True


def demonstration():
    #Reproduire le jeu d'essai de la partie A de l'énoncé.
    g = Grille()
    g.jouer(0, 0, "X")
    g.jouer(0, 1, "O")
    g.jouer(1, 1, "X")
    g.afficher()
    print("Case occupée :", g.jouer(0, 0, "O"))
    print("Hors grille :", g.jouer(3, 0, "O"))
    print("X est gagnant :", g.est_gagnant("X"))
    g.jouer(2, 2, "X")
    print("Après le dernier coup :")
    g.afficher()
    print("X est gagnant :", g.est_gagnant("X"))


# TESTS AUTOMATISÉS DE LA PARTIE A — en bas du code
import io
import sys
import unittest
from contextlib import redirect_stdout


class TestsGrille(unittest.TestCase):
    def test_grille_vide(self):
        g = Grille()
        self.assertFalse(g.est_plein())
        self.assertFalse(g.est_gagnant("X"))
        self.assertFalse(g.est_gagnant("O"))

    def test_un_coup_ne_modifie_qu_une_case(self):
        g = Grille()
        self.assertTrue(g.jouer(0, 0, "X"))
        self.assertEqual(g.tab, [["X", " ", " "], [" ", " ", " "], [" ", " ", " "]])
        autre = Grille()
        self.assertEqual(autre.tab[0][0], " ")

    def test_case_occupee(self):
        g = Grille()
        g.jouer(0, 0, "X")
        self.assertFalse(g.jouer(0, 0, "O"))
        self.assertEqual(g.tab[0][0], "X")

    def test_coordonnees_invalides(self):
        g = Grille()
        for x, y in ((3, 0), (-1, 0), (0, 3), (0, -1), ("0", 0), (0, 1.5), (True, 0)):
            with self.subTest(x=x, y=y):
                self.assertFalse(g.jouer(x, y, "X"))
        self.assertEqual(g.tab, [[" "] * 3 for _ in range(3)])

    def test_symbole_invalide(self):
        g = Grille()
        for symbole in ("", " ", "A", "x", None):
            with self.subTest(symbole=symbole):
                self.assertFalse(g.jouer(0, 0, symbole))
                self.assertFalse(g.est_gagnant(symbole))

    def test_huit_alignements_pour_les_deux_joueurs(self):
        alignements = [
            [(x, y) for y in range(3)] for x in range(3)
        ] + [
            [(x, y) for x in range(3)] for y in range(3)
        ] + [[(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]
        for symbole in ("X", "O"):
            for cases in alignements:
                with self.subTest(symbole=symbole, cases=cases):
                    g = Grille()
                    for x, y in cases:
                        self.assertTrue(g.jouer(x, y, symbole))
                    self.assertTrue(g.est_gagnant(symbole))
                    self.assertFalse(g.est_gagnant("O" if symbole == "X" else "X"))

    def test_jeu_essai_enonce(self):
        g = Grille()
        g.jouer(0, 0, "X")
        g.jouer(0, 1, "O")
        g.jouer(1, 1, "X")
        self.assertFalse(g.est_gagnant("X"))
        g.jouer(2, 2, "X")
        self.assertTrue(g.est_gagnant("X"))

    def test_grille_pleine_sans_gagnant(self):
        g = Grille()
        cases = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]]
        for x in range(3):
            for y in range(3):
                if (x, y) == (2, 2):
                    self.assertFalse(g.est_plein())
                g.jouer(x, y, cases[x][y])
        self.assertTrue(g.est_plein())
        self.assertFalse(g.est_gagnant("X"))
        self.assertFalse(g.est_gagnant("O"))

    def test_affichage(self):
        g = Grille()
        g.jouer(0, 0, "X")
        sortie = io.StringIO()
        with redirect_stdout(sortie):
            g.afficher()
        self.assertEqual(sortie.getvalue().splitlines(), [
            " X |   |  ", "-----------", "   |   |  ", "-----------", "   |   |  "])


if __name__ == "__main__":
    if "--test" in sys.argv[1:]:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    else:
        demonstration()
