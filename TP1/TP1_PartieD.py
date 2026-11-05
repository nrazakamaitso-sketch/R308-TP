"""TP1, partie D : jeu du pendu, avec sept erreurs maximum.

Lancer le jeu : python TP1_PartieD.py
Lancer les tests placés en bas du fichier : python TP1_PartieD.py --test
"""

import random
import sys
from pathlib import Path


def charger_mots(fichier):
    """Lire un mot par ligne et ignorer les lignes vides ou non alphabétiques."""
    with open(fichier, encoding="utf-8") as source:
        mots = []
        for ligne in source:
            mot = ligne.strip().upper()
            if mot and mot.isalpha():
                mots.append(mot)
    return mots


def jouer(mot):
    """Jouer avec le mot fourni ; renvoyer True pour une victoire, sinon False."""
    mot = mot.strip().upper()
    if not mot or not mot.isalpha():
        raise ValueError("Le mot doit contenir uniquement des lettres.")

    # Comme dans la partie C, une liste représente les positions du masque.
    masque = ["_"] * len(mot)
    lettres_proposees = []
    erreurs = 0
    maximum_erreurs = 7

    def afficher_etat():
        print("\nMot :", " ".join(masque))
        print(f"Erreurs : {erreurs}/{maximum_erreurs}")
        print("Lettres déjà proposées :", " ".join(lettres_proposees) or "aucune")

    afficher_etat()
    # Arrêter dès la septième erreur, conformément au jeu d'essai de l'énoncé.
    while "_" in masque and erreurs < maximum_erreurs:
        lettre = input("Propose une lettre : ").strip().upper()

        # Une saisie incorrecte ne consomme pas d'erreur.
        if len(lettre) != 1 or not lettre.isalpha():
            print("Saisie invalide : entre une seule lettre.")
            afficher_etat()
            continue

        # Une lettre répétée ne doit jamais être comptée deux fois.
        if lettre in lettres_proposees:
            print("Lettre déjà proposée : pas d'erreur de plus.")
            afficher_etat()
            continue

        lettres_proposees.append(lettre)
        if lettre in mot:
            # Révéler toutes les positions, y compris les lettres répétées.
            for position in range(len(mot)):
                if mot[position] == lettre:
                    masque[position] = lettre
        else:
            erreurs += 1

        afficher_etat()

    if "_" not in masque:
        print("Gagné ! Le mot était", mot)
        return True

    print("Perdu, le mot était", mot)
    return False


def main():
    """Choisir un mot dans mots.txt et démarrer une partie sans le révéler."""
    # Retrouver le fichier même si le jeu est lancé depuis un autre dossier.
    fichier = Path(__file__).resolve().with_name("mots.txt")
    try:
        mots = charger_mots(fichier)
    except OSError as erreur:
        print(f"Impossible de charger mots.txt : {erreur}")
        return

    if not mots:
        print("Aucun mot valide dans mots.txt.")
        return

    print("=== JEU DU PENDU ===")
    print("Trouve le mot avec 7 erreurs maximum.")
    jouer(random.choice(mots))


# ============================================================
# TESTS DE LA PARTIE D — placés en bas du code
# ============================================================
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch


class TestsPendu(unittest.TestCase):
    def simuler(self, mot, lettres):
        """Fournir les saisies automatiquement et récupérer les messages."""
        sortie = io.StringIO()
        with patch("builtins.input", side_effect=lettres) as saisie:
            with redirect_stdout(sortie):
                gagne = jouer(mot)
        return gagne, sortie.getvalue(), saisie.call_count

    def test_victoire_python_en_minuscules(self):
        gagne, sortie, nombre = self.simuler("PYTHON", list("python"))
        self.assertTrue(gagne)
        self.assertEqual(nombre, 6)
        self.assertIn("P Y T H O N", sortie)
        self.assertIn("Gagné !", sortie)
        self.assertNotIn("Perdu", sortie)

    def test_defaite_apres_exactement_sept_erreurs(self):
        gagne, sortie, nombre = self.simuler("PYTHON", list("abcdefg"))
        self.assertFalse(gagne)
        self.assertEqual(nombre, 7)
        self.assertIn("Erreurs : 7/7", sortie)
        self.assertIn("Perdu, le mot était PYTHON", sortie)

    def test_lettre_absente_repetee_sans_erreur_supplementaire(self):
        gagne, sortie, nombre = self.simuler("PYTHON", ["a", "A"] + list("python"))
        self.assertTrue(gagne)
        self.assertEqual(nombre, 8)
        self.assertIn("Lettre déjà proposée", sortie)
        self.assertIn("Erreurs : 1/7", sortie)
        self.assertNotIn("Erreurs : 2/7", sortie)

    def test_revele_toutes_les_positions(self):
        gagne, sortie, _ = self.simuler("PAPA", ["p", "a"])
        self.assertTrue(gagne)
        self.assertIn("P _ P _", sortie)
        self.assertIn("P A P A", sortie)

    def test_saisies_invalides_et_lettre_presente_repetee(self):
        gagne, sortie, _ = self.simuler("AB", ["", "12", "1", "ab", "a", "A", "b"])
        self.assertTrue(gagne)
        self.assertEqual(sortie.count("Saisie invalide"), 4)
        self.assertIn("Lettre déjà proposée", sortie)
        self.assertNotIn("Erreurs : 1/7", sortie)
        self.assertIn("Lettres déjà proposées : A B", sortie)

    def test_refuse_un_mot_vide_ou_invalide(self):
        for mot in ("", "   ", "PY-THON", "123"):
            with self.subTest(mot=mot):
                with self.assertRaises(ValueError):
                    jouer(mot)

    def test_chargement_des_mots(self):
        with tempfile.TemporaryDirectory() as dossier:
            fichier = Path(dossier) / "mots.txt"
            fichier.write_text("python\n\n lettre \n123\n", encoding="utf-8")
            self.assertEqual(charger_mots(fichier), ["PYTHON", "LETTRE"])

    def test_fichier_absent(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            sortie = io.StringIO()
            with redirect_stdout(sortie):
                main()
        self.assertIn("Impossible de charger mots.txt", sortie.getvalue())

    def test_liste_vide(self):
        with patch.dict(main.__globals__, charger_mots=lambda fichier: []):
            sortie = io.StringIO()
            with redirect_stdout(sortie):
                main()
        self.assertIn("Aucun mot valide", sortie.getvalue())


if __name__ == "__main__":
    if "--test" in sys.argv[1:]:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    else:
        main()
