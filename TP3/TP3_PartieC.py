# Module pour lire et écrire les fichiers CSV
import csv

# Importer les classes des parties précédentes
from TP3_PartieA import Livre, Utilisateur
from TP3_PartieB import Bibliotheque


# Classe qui ajoute la sauvegarde à la bibliothèque
class BibliothequeCSV(Bibliotheque):
    # Méthode pour sauvegarder les livres dans un CSV
    def sauvegarder(self, fichier_csv="livres.csv"):
        # Ouvrir le fichier en écriture
        with open(fichier_csv, "w", newline="", encoding="utf-8") as fichier:
            # Créer un objet pour écrire dans le CSV
            writer = csv.writer(fichier)
            # Écrire les noms des colonnes
            writer.writerow([
                "titre", "auteur", "annee",
                "disponible", "emprunteur"
            ])

            # Parcourir tous les livres
            for livre in self.livres.values():
                # Écrire les informations du livre
                writer.writerow([
                    livre.titre,
                    livre.auteur,
                    livre.annee,
                    livre.disponible,
                    livre.emprunteur or ""
                ])
        print("Bibliothèque sauvegardée avec succès")

    # Méthode pour charger les livres depuis le CSV
    def charger(self, fichier_csv="livres.csv"):
        try:
            # Ouvrir le fichier en lecture
            with open(fichier_csv, "r", newline="", encoding="utf-8") as fichier:
                # Créer un lecteur CSV
                lecteur = csv.reader(fichier)
                # Ignorer la première ligne (en-têtes)
                next(lecteur, None)
                # Préparer une nouvelle collection de livres
                nouveaux_livres = {}
                # Parcourir chaque ligne du fichier
                for ligne in lecteur:
                    # Ignorer les lignes vides
                    if not ligne:
                        continue
                    # Vérifier le nombre de colonnes
                    if len(ligne) != 5:
                        print("Ligne CSV invalide :", ligne)
                        continue
                    # Récupérer les informations
                    titre = ligne[0]
                    auteur = ligne[1]
                    # Convertir l'année en entier
                    try:
                        annee = int(ligne[2])
                    except ValueError:
                        print("Année invalide pour :", titre)
                        continue
                    # Vérifier la disponibilité
                    if ligne[3] not in ("True", "False"):
                        print("Disponibilité invalide :", titre)
                        continue
                    disponible = (ligne[3] == "True")
                    # Récupérer l'emprunteur
                    emprunteur = ligne[4]
                    # Vérifier la cohérence de l'emprunt
                    if not disponible and not emprunteur:
                        print("Emprunteur manquant :", titre)
                        continue
                    # Créer le livre
                    livre = Livre(titre, auteur, annee)
                    # Restaurer son état
                    livre.disponible = disponible
                    livre.emprunteur = (
                        emprunteur if not disponible else None
                    )
                    # Enregistrer le livre
                    nouveaux_livres[titre] = livre
                # Remplacer les livres par ceux du CSV
                self.livres = nouveaux_livres
                # Vider les anciennes listes d'emprunts
                for utilisateur in self.utilisateurs.values():
                    utilisateur.emprunts = []
                # Reconstruire les emprunts
                for livre in self.livres.values():
                    # Vérifier si le livre est emprunté
                    if not livre.disponible:
                        nom = livre.emprunteur
                        # Recréer l'utilisateur si nécessaire
                        if nom not in self.utilisateurs:
                            self.utilisateurs[nom] = Utilisateur(nom)
                        # Récupérer l'utilisateur
                        utilisateur = self.utilisateurs[nom]
                        # Ajouter le livre à ses emprunts
                        utilisateur.emprunts.append(livre)
            print("Bibliothèque chargée avec succès")
            return True
        # Le fichier n'existe pas encore
        except FileNotFoundError:
            print("Aucune sauvegarde trouvée")
            return False



# TESTS DE LA PARTIE C
if __name__ == "__main__":
    # Créer une première bibliothèque
    biblio = BibliothequeCSV()

    # Ajouter un livre
    livre1 = Livre("1984", "Orwell", 1949)
    biblio.ajouter_livre(livre1)

    # Ajouter un utilisateur
    ana = Utilisateur("Ana")
    biblio.ajouter_utilisateur(ana)

    # Ana emprunte le livre
    print("\nTEST 1 - Emprunt")
    assert biblio.emprunter("Ana", "1984") is True

    # Sauvegarder les informations
    print("\nTEST 2 - Sauvegarde")
    biblio.sauvegarder()

    # Créer une nouvelle bibliothèque vide
    print("\nTEST 3 - Chargement")
    nouvelle_biblio = BibliothequeCSV()

    # Charger les informations sauvegardées
    assert nouvelle_biblio.charger() is True

    # Vérifier que le livre a été restauré
    livre_recharge = nouvelle_biblio.livres["1984"]

    assert livre_recharge.disponible is False
    assert livre_recharge.emprunteur == "Ana"

    # Vérifier qu'Ana a retrouvé son emprunt
    ana_rechargee = nouvelle_biblio.utilisateurs["Ana"]

    assert livre_recharge in ana_rechargee.emprunts

    # Ana rend son livre après le rechargement
    print("\nTEST 4 - Retour après chargement")
    assert nouvelle_biblio.rendre("Ana", "1984") is True

    # Vérifier que le livre est disponible
    assert livre_recharge.disponible is True
    assert livre_recharge.emprunteur is None

  
