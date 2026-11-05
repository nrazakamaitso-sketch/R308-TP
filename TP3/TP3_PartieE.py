"""Partie E : recherche par auteur, limite d'emprunts et export JSON.

Lancer le menu : python TP3_PartieE.py
Lancer les tests en bas du fichier : python TP3_PartieE.py --test
"""

import json
import sys

from TP3_PartieA import Livre, Utilisateur
from TP3_PartieC import BibliothequeCSV


class BibliothequeEtendue(BibliothequeCSV):
    """Ajouter les extensions sans modifier les classes des parties A/B/C."""

    def __init__(self, limite_emprunts=3):
        super().__init__()
        # L'énoncé ne fixe pas de nombre : trois est une valeur configurable.
        if type(limite_emprunts) is not int or limite_emprunts < 1:
            raise ValueError("La limite doit être un entier strictement positif.")
        self.limite_emprunts = limite_emprunts

    def rechercher_par_auteur(self, auteur):
        """Renvoyer les livres dont l'auteur contient la recherche, sans casse."""
        recherche = auteur.strip().casefold()
        if not recherche:
            return []
        return [livre for livre in self.livres.values()
                if recherche in livre.auteur.casefold()]

    def emprunter(self, nom, titre):
        """Refuser un nouvel emprunt si l'utilisateur a atteint sa limite."""
        utilisateur = self.utilisateurs.get(nom)
        if utilisateur is not None and len(utilisateur.emprunts) >= self.limite_emprunts:
            print(f"Limite atteinte : {self.limite_emprunts} emprunts maximum.")
            return False
        # La partie B vérifie les noms, les titres et la disponibilité.
        return super().emprunter(nom, titre)

    def exporter_json(self, fichier_json="bibliotheque.json"):
        """Exporter un instantané lisible, incluant les utilisateurs sans emprunt.

        L'export JSON est indépendant du CSV : charger() continue de lire le CSV.
        Une erreur d'écriture est transmise à l'appelant pour qu'il la signale.
        """
        donnees = {
            "limite_emprunts": self.limite_emprunts,
            "livres": [
                {"titre": livre.titre, "auteur": livre.auteur,
                 "annee": livre.annee, "disponible": livre.disponible,
                 "emprunteur": livre.emprunteur}
                for livre in self.livres.values()
            ],
            "utilisateurs": [
                {"nom": utilisateur.nom,
                 "emprunts": [livre.titre for livre in utilisateur.emprunts]}
                for utilisateur in self.utilisateurs.values()
            ],
        }
        with open(fichier_json, "w", encoding="utf-8") as fichier:
            json.dump(donnees, fichier, ensure_ascii=False, indent=4)
        print("Export JSON effectué avec succès.")


def main():
    """Proposer le menu de la bibliothèque enrichi de deux nouveaux choix."""
    biblio = BibliothequeEtendue(limite_emprunts=3)
    try:
        biblio.charger()
    except OSError as erreur:
        # Ne pas démarrer vide après un échec de lecture : cela risquerait
        # d'écraser la sauvegarde existante lors de la sortie du programme.
        print(f"Chargement impossible : {erreur}")
        return
    print(f"Limite : {biblio.limite_emprunts} emprunts par utilisateur.")
    print("Le CSV ne conserve pas les utilisateurs sans emprunt.")

    while True:
        print("\n===== BIBLIOTHÈQUE — PARTIE E =====")
        print("1. Ajouter un livre")
        print("2. Ajouter un utilisateur")
        print("3. Emprunter un livre")
        print("4. Rendre un livre")
        print("5. Afficher les livres")
        print("6. Sauvegarder et quitter")
        print("7. Rechercher par auteur")
        print("8. Exporter en JSON")
        choix = input("Votre choix : ").strip()

        if choix == "1":
            titre = input("Titre : ").strip()
            auteur = input("Auteur : ").strip()
            try:
                annee = int(input("Année : "))
            except ValueError:
                print("Erreur : année invalide.")
                continue
            biblio.ajouter_livre(Livre(titre, auteur, annee))
        elif choix == "2":
            biblio.ajouter_utilisateur(Utilisateur(input("Nom : ").strip()))
        elif choix in ("3", "4"):
            nom = input("Nom : ").strip()
            titre = input("Titre : ").strip()
            if choix == "3":
                biblio.emprunter(nom, titre)
            else:
                biblio.rendre(nom, titre)
        elif choix == "5":
            biblio.afficher_livres()
        elif choix == "6":
            try:
                biblio.sauvegarder()
            except OSError as erreur:
                print(f"Sauvegarde impossible : {erreur}")
                continue
            print("Au revoir !")
            break
        elif choix == "7":
            livres = biblio.rechercher_par_auteur(input("Auteur recherché : "))
            if not livres:
                print("Aucun livre trouvé.")
            for livre in livres:
                livre.afficher()
        elif choix == "8":
            try:
                biblio.exporter_json()
            except OSError as erreur:
                print(f"Export impossible : {erreur}")
        else:
            print("Choix invalide. Veuillez saisir un nombre de 1 à 8.")


# ============================================================
# TESTS AUTOMATISÉS DE LA PARTIE E — en bas du code
# ============================================================
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch


class TestsExtensions(unittest.TestCase):
    def setUp(self):
        self.biblio = BibliothequeEtendue(limite_emprunts=2)
        self.livres = [Livre("1984", "George Orwell", 1949),
                       Livre("La Ferme des animaux", "George Orwell", 1945),
                       Livre("Le Petit Prince", "Saint-Exupéry", 1943)]
        for livre in self.livres:
            self.biblio.ajouter_livre(livre)
        self.biblio.ajouter_utilisateur(Utilisateur("Ana"))
        self.biblio.ajouter_utilisateur(Utilisateur("Léo"))
        self.sortie = redirect_stdout(io.StringIO())
        self.sortie.__enter__()
        self.addCleanup(self.sortie.__exit__, None, None, None)

    def test_recherche_partielle_sans_casse(self):
        self.assertEqual(self.biblio.rechercher_par_auteur(" ORWELL "), self.livres[:2])
        self.assertEqual(self.biblio.rechercher_par_auteur("exupéry"), [self.livres[2]])

    def test_recherche_absente_ou_vide(self):
        self.assertEqual(self.biblio.rechercher_par_auteur("inconnu"), [])
        self.assertEqual(self.biblio.rechercher_par_auteur("  "), [])

    def test_limite_et_absence_de_modification_apres_refus(self):
        self.assertTrue(self.biblio.emprunter("Ana", "1984"))
        self.assertTrue(self.biblio.emprunter("Ana", "La Ferme des animaux"))
        self.assertFalse(self.biblio.emprunter("Ana", "Le Petit Prince"))
        self.assertTrue(self.livres[2].disponible)
        self.assertIsNone(self.livres[2].emprunteur)
        self.assertEqual(len(self.biblio.utilisateurs["Ana"].emprunts), 2)

    def test_retour_libere_une_place(self):
        self.biblio.emprunter("Ana", "1984")
        self.biblio.emprunter("Ana", "La Ferme des animaux")
        self.assertTrue(self.biblio.rendre("Ana", "1984"))
        self.assertTrue(self.biblio.emprunter("Ana", "Le Petit Prince"))

    def test_limite_independante_par_utilisateur(self):
        self.biblio.emprunter("Ana", "1984")
        self.biblio.emprunter("Ana", "La Ferme des animaux")
        self.assertTrue(self.biblio.emprunter("Léo", "Le Petit Prince"))

    def test_cas_pieges_des_parties_precedentes(self):
        self.assertFalse(self.biblio.emprunter("Inconnu", "1984"))
        self.assertFalse(self.biblio.emprunter("Ana", "Inconnu"))
        self.assertTrue(self.biblio.emprunter("Ana", "1984"))
        self.assertFalse(self.biblio.emprunter("Léo", "1984"))
        self.assertFalse(self.biblio.rendre("Léo", "1984"))
        self.assertEqual(self.livres[0].emprunteur, "Ana")

    def test_limite_invalide(self):
        for limite in (0, -1, 1.5, "3", True):
            with self.subTest(limite=limite):
                with self.assertRaises(ValueError):
                    BibliothequeEtendue(limite)

    def test_export_json_complet_et_utf8(self):
        self.biblio.emprunter("Ana", "1984")
        with tempfile.TemporaryDirectory() as dossier:
            fichier = Path(dossier) / "export.json"
            self.biblio.exporter_json(fichier)
            texte = fichier.read_text(encoding="utf-8")
            donnees = json.loads(texte)
        self.assertEqual(donnees["limite_emprunts"], 2)
        self.assertEqual(len(donnees["livres"]), 3)
        self.assertEqual(donnees["livres"][0], {
            "titre": "1984", "auteur": "George Orwell", "annee": 1949,
            "disponible": False, "emprunteur": "Ana"})
        self.assertIsNone(donnees["livres"][1]["emprunteur"])
        self.assertEqual(donnees["utilisateurs"], [
            {"nom": "Ana", "emprunts": ["1984"]}, {"nom": "Léo", "emprunts": []}])
        self.assertIn("Saint-Exupéry", texte)

    def test_limite_apres_rechargement_csv(self):
        self.biblio.emprunter("Ana", "1984")
        self.biblio.emprunter("Ana", "La Ferme des animaux")
        with tempfile.TemporaryDirectory() as dossier:
            fichier = Path(dossier) / "livres.csv"
            self.biblio.sauvegarder(fichier)
            rechargee = BibliothequeEtendue(limite_emprunts=2)
            self.assertTrue(rechargee.charger(fichier))
        self.assertFalse(rechargee.emprunter("Ana", "Le Petit Prince"))
        self.assertTrue(rechargee.rendre("Ana", "1984"))
        self.assertTrue(rechargee.emprunter("Ana", "Le Petit Prince"))

    def test_erreur_export_transmise(self):
        with patch("builtins.open", side_effect=OSError("Accès refusé")):
            with self.assertRaises(OSError):
                self.biblio.exporter_json()

    def test_menu_recherche_export_et_saisies_invalides(self):
        # Remplacer seulement l'instance pour isoler les fichiers de travail.
        with patch.dict(main.__globals__, BibliothequeEtendue=lambda **kwargs: self.biblio):
            with patch.object(self.biblio, "charger") as charger:
                with patch.object(self.biblio, "sauvegarder") as sauvegarder:
                    with patch.object(self.biblio, "exporter_json") as exporter:
                        with patch("builtins.input", side_effect=[
                            "9", "1", "Rejeté", "Auteur", "abc", "7", "orwell", "8", "6"]):
                            sortie = io.StringIO()
                            with redirect_stdout(sortie):
                                main()
        charger.assert_called_once()
        sauvegarder.assert_called_once()
        exporter.assert_called_once()
        self.assertIn("Choix invalide", sortie.getvalue())
        self.assertIn("année invalide", sortie.getvalue())
        self.assertIn("1984", sortie.getvalue())
        self.assertNotIn("Rejeté", self.biblio.livres)


if __name__ == "__main__":
    if "--test" in sys.argv[1:]:
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    else:
        main()
