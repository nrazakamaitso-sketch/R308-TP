# Réutiliser la grille, les joueurs et la boucle du jeu complet.
from TP2_PartieA import Grille
from TP2_PartieB import JoueurHumain, JoueurIA, cases_libres
from TP2_PartieC import jouer_partie


class JoueurIAMalin(JoueurIA):
    def trouver_coup_gagnant(self, tab, symbole):
        # Tester chaque case libre dans l'ordre des lignes et des colonnes.
        # S'il existe plusieurs victoires possibles, la première est retenue.
        for x, y in cases_libres(tab):
            simulation = Grille()
            # Copier CHAQUE ligne : tab[:] seul partagerait les listes internes.
            # Un essai sur la copie ne doit jamais modifier la vraie partie.
            simulation.tab = [ligne[:] for ligne in tab]
            simulation.jouer(x, y, symbole)
            if simulation.est_gagnant(symbole):
                return x, y
        return None

    def prochain_coup(self, tab, symbole):
        if symbole not in ("X", "O"):
            raise ValueError("Le symbole doit être X ou O.")
        if not cases_libres(tab):
            raise ValueError("La grille est pleine : aucun coup possible.")

        # Priorité 1 : terminer immédiatement la partie par une victoire.
        coup = self.trouver_coup_gagnant(tab, symbole)
        # Un couple (0, 0) est une réponse valide : on compare explicitement à None.
        if coup is not None:
            return coup

        # Priorité 2 : simuler les coups de l'autre symbole. Une case qui ferait
        # gagner l'adversaire doit être occupée par notre IA pour le bloquer.
        adversaire = "O" if symbole == "X" else "X"
        coup = self.trouver_coup_gagnant(tab, adversaire)
        if coup is not None:
            return coup

        # Priorité 3 : aucune menace immédiate. super() appelle l'IA aléatoire
        # de la partie B, qui choisit uniquement parmi les cases encore libres.
        return super().prochain_coup(tab, symbole)


def main():
    print("=== MORPION — IA QUI GAGNE OU BLOQUE ===")
    while True:
        print("\n1. Humain (X) contre IA maligne (O)")
        print("2. IA aléatoire (X) contre IA maligne (O)")
        print("3. Deux IA malignes")
        print("0. Quitter")
        choix = input("Votre choix : ").strip()
        if choix == "0":
            break
        if choix == "1":
            joueur_x, joueur_o = JoueurHumain(), JoueurIAMalin()
        elif choix == "2":
            joueur_x, joueur_o = JoueurIA(), JoueurIAMalin()
        elif choix == "3":
            joueur_x, joueur_o = JoueurIAMalin(), JoueurIAMalin()
        else:
            print("Choix invalide : entre 0, 1, 2 ou 3.")
            continue
        # Grâce à la même méthode prochain_coup(), le moteur existant peut
        # utiliser le nouveau joueur sans aucune modification de la partie C.
        jouer_partie(joueur_x, joueur_o)



# TESTS AUTOMATISÉS DU BONUS 1 — en bas du code

import io
import random
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch


class TestsIAMalin(unittest.TestCase):
    def test_blocage_exemple_enonce(self):
        # X X _ / _ O _ / _ _ _ : O doit bloquer la première ligne.
        tab = [["X", "X", " "], [" ", "O", " "], [" ", " ", " "]]
        self.assertEqual(JoueurIAMalin().prochain_coup(tab, "O"), (0, 2))

    def test_victoire_prioritaire_sur_blocage(self):
        # O peut gagner sur la première ligne : il ne doit pas se contenter
        # de bloquer les deux X de la deuxième ligne.
        tab = [["O", "O", " "], ["X", "X", " "], [" ", " ", " "]]
        self.assertEqual(JoueurIAMalin().prochain_coup(tab, "O"), (0, 2))

    def alignements(self):
        # Les huit façons d'aligner trois cases, réutilisées dans deux tests.
        return ([[(x, y) for y in range(3)] for x in range(3)]
                + [[(x, y) for x in range(3)] for y in range(3)]
                + [[(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]])

    def test_gagne_sur_tous_les_alignements_avec_x_et_o(self):
        for symbole in ("X", "O"):
            for cases in self.alignements():
                with self.subTest(symbole=symbole, cases=cases):
                    g = Grille()
                    for x, y in cases[:2]:
                        g.jouer(x, y, symbole)
                    self.assertEqual(JoueurIAMalin().prochain_coup(g.tab, symbole), cases[2])

    def test_bloque_sur_tous_les_alignements_avec_x_et_o(self):
        for symbole in ("X", "O"):
            adversaire = "O" if symbole == "X" else "X"
            for cases in self.alignements():
                with self.subTest(symbole=symbole, cases=cases):
                    g = Grille()
                    for x, y in cases[:2]:
                        g.jouer(x, y, adversaire)
                    self.assertEqual(JoueurIAMalin().prochain_coup(g.tab, symbole), cases[2])

    def test_simulation_ne_modifie_pas_la_vraie_grille(self):
        g = Grille()
        g.jouer(0, 0, "X")
        g.jouer(1, 1, "O")
        avant = [ligne[:] for ligne in g.tab]
        coup = JoueurIAMalin().prochain_coup(g.tab, "X")
        self.assertEqual(g.tab, avant)
        self.assertIn(coup, cases_libres(avant))

    def test_hasard_sans_victoire_ni_menace(self):
        g = Grille()
        g.jouer(1, 1, "X")
        # Imposer le tirage permet de vérifier exactement sa liste de choix,
        # sans dépendre d'un résultat aléatoire susceptible de varier.
        with patch.object(random, "choice", return_value=(0, 0)) as choix:
            self.assertEqual(JoueurIAMalin().prochain_coup(g.tab, "O"), (0, 0))
        choix.assert_called_once_with(cases_libres(g.tab))

    def test_grille_pleine(self):
        tab = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]]
        with self.assertRaises(ValueError):
            JoueurIAMalin().prochain_coup(tab, "O")

    def test_symbole_invalide(self):
        with self.assertRaises(ValueError):
            JoueurIAMalin().prochain_coup(Grille().tab, "A")

    def test_integration_vingt_parties_contre_ia_aleatoire(self):
        # Vérifier de vraies parties contre l'IA aléatoire, avec une graine
        # reproductible. Aucune saisie ni grille affichée n'est nécessaire.
        for graine in range(20):
            with self.subTest(graine=graine):
                tirage = random.Random(graine)
                with patch.object(random, "choice", side_effect=tirage.choice):
                    resultat = jouer_partie(JoueurIA(), JoueurIAMalin(), afficher=False)
                self.assertIn(resultat, ("X", "O", None))

    def test_menu_et_choix_invalide(self):
        # Remplacer les parties par une fonction qui mémorise les joueurs
        # pour vérifier le branchement du menu sans interaction réelle.
        parties = []
        with patch.dict(main.__globals__, jouer_partie=lambda x, o: parties.append((x, o))):
            with patch("builtins.input", side_effect=["9", "1", "2", "3", "0"]):
                sortie = io.StringIO()
                with redirect_stdout(sortie):
                    main()
        self.assertIn("Choix invalide", sortie.getvalue())
        self.assertEqual(len(parties), 3)
        self.assertIsInstance(parties[0][0], JoueurHumain)
        self.assertIsInstance(parties[1][0], JoueurIA)
        self.assertIsInstance(parties[2][0], JoueurIAMalin)
        self.assertTrue(all(isinstance(o, JoueurIAMalin) for x, o in parties))


if __name__ == "__main__":
    # Un import permet de réutiliser la classe sans ouvrir le menu.
    # --test sélectionne les tests ; sinon on démarre le jeu interactif.
    if "--test" in sys.argv[1:]:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    else:
        main()
