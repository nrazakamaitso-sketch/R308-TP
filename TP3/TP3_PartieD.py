"""Menu du TP3 : exécuter ce fichier dans le dossier des parties A, B et C.

La partie C conserve les livres et leurs emprunteurs dans livres.csv.
Les utilisateurs sans emprunt ne sont donc pas conservés au redémarrage.
"""

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


# Un import depuis les tests ne doit pas lancer les questions du menu.
if __name__ == "__main__":
    main()
