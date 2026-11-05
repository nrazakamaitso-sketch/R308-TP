from TP3_PartieA import Livre, Utilisateur
from TP3_PartieC import BibliothequeCSV


def main():
    """Charger les données, traiter les choix, puis sauvegarder avant de sortir."""
    biblio = BibliothequeCSV()
    try:
        biblio.charger()
    except FileNotFoundError:
        # Premier lancement : aucun fichier n'a encore été enregistré.
        print("Aucune sauvegarde : démarrage avec une bibliothèque vide.")
    print("Attention : les utilisateurs sans emprunt ne sont pas sauvegardés.")

    while True:
        print("\n===== GESTION DE LA BIBLIOTHÈQUE =====")
        print("1. Ajouter un livre")
        print("2. Ajouter un utilisateur")
        print("3. Emprunter un livre")
        print("4. Rendre un livre")
        print("5. Afficher les livres")
        print("6. Sauvegarder et quitter")
        choix = input("Votre choix : ").strip()

        if choix == "1":
            titre = input("Titre : ").strip()
            auteur = input("Auteur : ").strip()
            try:
                # input renvoie du texte ; int exige un entier (ex. : 1949).
                annee = int(input("Année : "))
            except ValueError:
                print("Erreur : année invalide. Veuillez saisir un entier.")
                # Aucun livre n'est créé ; on affiche à nouveau le menu.
                continue
            biblio.ajouter_livre(Livre(titre, auteur, annee))

        elif choix == "2":
            nom = input("Nom de l'utilisateur : ").strip()
            biblio.ajouter_utilisateur(Utilisateur(nom))
        elif choix == "3":
            nom = input("Nom de l'utilisateur : ").strip()
            titre = input("Titre du livre : ").strip()
            # La bibliothèque retrouve elle-même les objets concernés.
            biblio.emprunter(nom, titre)
        elif choix == "4":
            nom = input("Nom de l'utilisateur : ").strip()
            titre = input("Titre du livre : ").strip()
            biblio.rendre(nom, titre)
        elif choix == "5":
            biblio.afficher_livres()
        elif choix == "6":
            try:
                biblio.sauvegarder()
            except OSError as erreur:
                # Si l'écriture échoue, rester dans le menu pour réessayer.
                print(f"Sauvegarde impossible : {erreur}")
                continue
            print("Au revoir !")
            break  # Sortir uniquement après une sauvegarde réussie.

        else:
            print("Choix invalide. Veuillez saisir un nombre de 1 à 6.")



# TESTS DE LA PARTIE D
import importlib
import importlib.util
import io
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock, call, patch


DOSSIER = Path(__file__).resolve().parent

def charger_menu_simule():
    """Importer le vrai fichier D en remplaçant seulement ses dépendances."""
    partie_a = types.ModuleType("TP3_PartieA")
    partie_a.Livre = Mock(name="Livre")
    partie_a.Utilisateur = Mock(name="Utilisateur")
    partie_c = types.ModuleType("TP3_PartieC")
    partie_c.BibliothequeCSV = Mock(name="BibliothequeCSV")
    specification = importlib.util.spec_from_file_location(
        "menu_simule", DOSSIER / "TP3_PartieD.py"
    )
    module = importlib.util.module_from_spec(specification)
    with patch.dict(sys.modules, {"TP3_PartieA": partie_a, "TP3_PartieC": partie_c}):
        specification.loader.exec_module(module)
    return module


def executer_menu(module, saisies):
    """Simuler input et capturer les messages, sans interaction humaine."""
    sortie = io.StringIO()
    with patch("builtins.input", side_effect=saisies) as lecture:
        with redirect_stdout(sortie):
            module.main()
    return sortie.getvalue(), lecture


class TestsMenu(unittest.TestCase):
    def setUp(self):
        self.menu = charger_menu_simule()
        self.biblio = self.menu.BibliothequeCSV.return_value

    def test_import_ne_lance_pas_le_menu(self):
        self.menu.BibliothequeCSV.assert_not_called()

    def test_six_choix_chargement_et_sortie(self):
        sortie, lecture = executer_menu(self.menu, ["6"])
        for libelle in (
            "1. Ajouter un livre", "2. Ajouter un utilisateur",
            "3. Emprunter un livre", "4. Rendre un livre",
            "5. Afficher les livres", "6. Sauvegarder et quitter",
        ):
            self.assertIn(libelle, sortie)
        self.assertEqual(self.biblio.method_calls, [call.charger(), call.sauvegarder()])
        self.assertEqual(lecture.call_count, 1)
        self.assertIn("Au revoir !", sortie)

    def test_toutes_les_actions_et_ordre_des_arguments(self):
        executer_menu(self.menu, [
            "1", "1984", "Orwell", "1949", "2", "Ana",
            "3", "Ana", "1984", "4", "Ana", "1984", "5", "6",
        ])
        self.menu.Livre.assert_called_once_with("1984", "Orwell", 1949)
        self.menu.Utilisateur.assert_called_once_with("Ana")
        self.assertEqual(self.biblio.method_calls, [
            call.charger(), call.ajouter_livre(self.menu.Livre.return_value),
            call.ajouter_utilisateur(self.menu.Utilisateur.return_value),
            call.emprunter("Ana", "1984"), call.rendre("Ana", "1984"),
            call.afficher_livres(), call.sauvegarder(),
        ])

    def test_annees_invalides_puis_ajout_valide(self):
        for annee in ("bonjour", "", "19.5"):
            with self.subTest(annee=annee):
                menu = charger_menu_simule()
                sortie, _ = executer_menu(menu, [
                    "1", "Rejete", "Auteur", annee,
                    "1", "Valide", "Auteur", "2000", "6",
                ])
                self.assertIn("année invalide", sortie)
                menu.Livre.assert_called_once_with("Valide", "Auteur", 2000)
                menu.BibliothequeCSV.return_value.ajouter_livre.assert_called_once()

    def test_choix_invalides_puis_affichage(self):
        sortie, _ = executer_menu(self.menu, ["9", "abc", "", "5", "6"])
        self.assertEqual(sortie.count("Choix invalide"), 3)
        self.biblio.afficher_livres.assert_called_once()

    def test_premier_lancement_sans_csv(self):
        self.biblio.charger.side_effect = FileNotFoundError("livres.csv")
        sortie, _ = executer_menu(self.menu, ["6"])
        self.assertIn("bibliothèque vide", sortie)
        self.biblio.sauvegarder.assert_called_once()

    def test_echec_sauvegarde_permet_de_reessayer(self):
        self.biblio.sauvegarder.side_effect = [OSError("Accès refusé"), None]
        sortie, _ = executer_menu(self.menu, ["6", "5", "6"])
        self.assertIn("Sauvegarde impossible", sortie)
        self.assertEqual(self.biblio.sauvegarder.call_count, 2)
        self.biblio.afficher_livres.assert_called_once()
        self.assertEqual(sortie.count("Au revoir !"), 1)


class TestsIntegrationCSV(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Seule l'absence des fichiers autorise à ignorer ces tests.
        # Une erreur d'import interne aux parties A/B/C reste un échec visible.
        manquants = [nom for nom in ("TP3_PartieA", "TP3_PartieB", "TP3_PartieC")
                     if not (DOSSIER / f"{nom}.py").is_file()]
        if manquants:
            raise unittest.SkipTest("Fichiers requis absents : " + ", ".join(manquants))
        cls.menu = importlib.import_module("TP3_PartieD")

    def setUp(self):
        # La partie C utilise livres.csv relativement au dossier courant.
        self.temporaire = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporaire.cleanup)
        ancien = Path.cwd()
        os.chdir(self.temporaire.name)
        self.addCleanup(os.chdir, ancien)

    def affichage(self, biblio):
        sortie = io.StringIO()
        with redirect_stdout(sortie):
            biblio.afficher_livres()
        return sortie.getvalue()

    def test_menu_sauvegarde_rechargement_et_retour(self):
        # Session 1 : les vrais objets sont créés et l'emprunt est sauvegardé.
        executer_menu(self.menu, [
            "1", "1984", "Orwell", "1949", "2", "Ana",
            "3", "Ana", "1984", "6",
        ])
        csv = Path("livres.csv")
        self.assertTrue(csv.is_file())
        contenu_emprunte = csv.read_bytes()
        self.assertIn(b"1984", contenu_emprunte)
        self.assertIn(b"1949", contenu_emprunte)
        self.assertIn(b"Ana", contenu_emprunte)

        # Une nouvelle instance doit restaurer le livre ET son emprunteur.
        chargee = self.menu.BibliothequeCSV()
        with redirect_stdout(io.StringIO()):
            chargee.charger()
        emprunte = self.affichage(chargee)
        self.assertIn("1984", emprunte)

        # Rendre le livre sans recréer Ana vérifie sa restauration.
        executer_menu(self.menu, ["4", "Ana", "1984", "6"])
        self.assertNotEqual(csv.read_bytes(), contenu_emprunte)
        rendue = self.menu.BibliothequeCSV()
        with redirect_stdout(io.StringIO()):
            rendue.charger()
        disponible = self.affichage(rendue)
        self.assertIn("1984", disponible)
        self.assertNotEqual(disponible, emprunte)

        # Comparer à un livre neuf, disponible, sans supposer les attributs A/B.
        reference = self.menu.BibliothequeCSV()
        with redirect_stdout(io.StringIO()):
            reference.ajouter_livre(self.menu.Livre("1984", "Orwell", 1949))
        self.assertEqual(disponible, self.affichage(reference))

    def test_utilisateur_sans_emprunt_non_sauvegarde(self):
        executer_menu(self.menu, ["1", "1984", "Orwell", "1949", "6"])
        avant = Path("livres.csv").read_bytes()
        executer_menu(self.menu, ["2", "SansEmpruntXYZ", "6"])
        apres = Path("livres.csv").read_bytes()
        self.assertEqual(avant, apres)
        self.assertNotIn(b"SansEmpruntXYZ", apres)

# Lancement : le menu par défaut, ou les tests avec l'option --test.
if __name__ == "__main__":
    if "--test" in sys.argv[1:]:
        # Ne pas transmettre notre option personnalisée à unittest.
        unittest.main(argv=[sys.argv[0]], verbosity=2)
    else:
        main()
