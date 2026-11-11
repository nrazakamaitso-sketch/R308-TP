import random

from TP2_PartieA import Grille


def cases_libres(tab):
    #Renvoyer les coordonnées libres d'une grille 3 × 3 (liste de listes).
    return [(x, y) for x in range(3) for y in range(3) if tab[x][y] == " "]


class JoueurHumain:
    def prochain_coup(self, tab, symbole):
        #Demander une ligne et une colonne libres, puis renvoyer (x, y).
        
        if not cases_libres(tab):
            raise ValueError("La grille est pleine : aucun coup possible.")

        while True:
            print(f"Joueur {symbole}, coordonnées de 0 à 2.")
            try:
                x = int(input("Ligne : "))
                y = int(input("Colonne : "))
            except ValueError:
                print("Saisie invalide : entre des nombres entiers.")
                continue

            # Refuser -1 avant de consulter la liste : Python l'accepterait
            # comme indice de la dernière ligne ou colonne.
            if not (0 <= x < 3 and 0 <= y < 3):
                print("Coup hors grille : utilise des coordonnées de 0 à 2.")
                continue
            if tab[x][y] != " ":
                print("Case occupée : choisis une autre case.")
                continue
            return x, y


class JoueurIA:
    def prochain_coup(self, tab, symbole):
        #Choisir une case libre au hasard, sans modifier la grille.

        """Le paramètre symbole conserve la même interface que JoueurHumain.
        Cette IA aléatoire n'en a pas besoin pour choisir sa case.
        """
        libres = cases_libres(tab)
        if not libres:
            raise ValueError("La grille est pleine : aucun coup possible.")
        return random.choice(libres)


def demonstration():
    #Montrer un coup humain puis un coup IA ; la partie C gérera le jeu.
    grille = Grille()
    humain = JoueurHumain()
    ia = JoueurIA()
    grille.afficher()

    # Les deux objets possèdent la même méthode et renvoient un tuple.
    x, y = humain.prochain_coup(grille.tab, "X")
    grille.jouer(x, y, "X")
    x, y = ia.prochain_coup(grille.tab, "O")
    print(f"L'IA joue en ({x}, {y}).")
    grille.jouer(x, y, "O")
    grille.afficher()
    print("Fin de l'exemple : la boucle complète sera ajoutée en partie C.")


# TESTS AUTOMATISÉS DE LA PARTIE B — en bas du code

import io
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch


class TestsJoueurs(unittest.TestCase):
    def simuler_humain(self, grille, saisies):
        sortie = io.StringIO()
        with patch("builtins.input", side_effect=saisies):
            with redirect_stdout(sortie):
                coup = JoueurHumain().prochain_coup(grille.tab, "X")
        return coup, sortie.getvalue()

    def test_humain_renvoie_coordonnees_sans_jouer(self):
        grille = Grille()
        coup, _ = self.simuler_humain(grille, ["1", "2"])
        self.assertEqual(coup, (1, 2))
        self.assertEqual(grille.tab, [[" "] * 3 for _ in range(3)])

    def test_humain_redemande_apres_saisie_non_numerique(self):
        coup, sortie = self.simuler_humain(Grille(), ["abc", "1", "1"])
        self.assertEqual(coup, (1, 1))
        self.assertIn("Saisie invalide", sortie)

    def test_humain_redemande_apres_colonne_non_numerique(self):
        coup, sortie = self.simuler_humain(Grille(), ["1", "1.5", "0", "2"])
        self.assertEqual(coup, (0, 2))
        self.assertIn("Saisie invalide", sortie)

    def test_humain_refuse_coordonnees_hors_grille(self):
        for x, y in (("3", "0"), ("-1", "0"), ("0", "3"), ("0", "-1")):
            with self.subTest(x=x, y=y):
                coup, sortie = self.simuler_humain(Grille(), [x, y, "2", "2"])
                self.assertEqual(coup, (2, 2))
                self.assertIn("hors grille", sortie)

    def test_humain_refuse_case_occupee(self):
        grille = Grille()
        grille.jouer(0, 0, "O")
        coup, sortie = self.simuler_humain(grille, ["0", "0", "0", "1"])
        self.assertEqual(coup, (0, 1))
        self.assertIn("Case occupée", sortie)
        self.assertEqual(grille.tab[0][0], "O")

    def test_ia_choisit_uniquement_parmi_les_cases_libres(self):
        grille = Grille()
        grille.jouer(1, 1, "X")
        libres = cases_libres(grille.tab)
        # Vérifier la liste exacte donnée au tirage évite un test probabiliste.
        with patch.object(random, "choice", return_value=(2, 2)) as choix:
            self.assertEqual(JoueurIA().prochain_coup(grille.tab, "O"), (2, 2))
        choix.assert_called_once_with(libres)
        self.assertEqual(len(libres), 8)
        self.assertNotIn((1, 1), libres)
        self.assertEqual(grille.tab[2][2], " ")

    def test_ia_trouve_la_derniere_case_libre(self):
        grille = Grille()
        for x in range(3):
            for y in range(3):
                if (x, y) != (2, 1):
                    grille.jouer(x, y, "X")
        self.assertEqual(JoueurIA().prochain_coup(grille.tab, "O"), (2, 1))

    def test_grille_pleine_pour_les_deux_joueurs(self):
        grille = Grille()
        for x in range(3):
            for y in range(3):
                grille.jouer(x, y, "X")
        for joueur in (JoueurHumain(), JoueurIA()):
            with self.subTest(joueur=type(joueur).__name__):
                with patch("builtins.input") as saisie:
                    with self.assertRaises(ValueError):
                        joueur.prochain_coup(grille.tab, "O")
                saisie.assert_not_called()

    def test_les_deux_joueurs_fonctionnent_avec_grille_jouer(self):
        grille = Grille()
        coup, _ = self.simuler_humain(grille, ["1", "1"])
        self.assertTrue(grille.jouer(*coup, "X"))
        coup_ia = JoueurIA().prochain_coup(grille.tab, "O")
        self.assertNotEqual(coup_ia, coup)
        self.assertTrue(grille.jouer(*coup_ia, "O"))


if __name__ == "__main__":
    if "--test" in sys.argv[1:]:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    else:
        demonstration()
