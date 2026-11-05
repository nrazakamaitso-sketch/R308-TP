# Importer les classes créées dans la partie A
from TP3_PartieA import Livre, Utilisateur

class Bibliotheque:
    # Constructeur de la bibliothèque
    def __init__(self):
        # Dictionnaire des livres : titre -> objet Livre
        self.livres = {}
        # Dictionnaire des utilisateurs : nom -> objet Utilisateur
        self.utilisateurs = {}

    # Méthode pour ajouter un livre
    def ajouter_livre(self, livre):
        # Vérifier que le titre n'existe pas déjà
        if livre.titre not in self.livres:
            self.livres[livre.titre] = livre
            return True
        print("Ce livre existe déjà")
        return False

    # Méthode pour ajouter un utilisateur
    def ajouter_utilisateur(self, utilisateur):
        # Vérifier que le nom n'existe pas déjà
        if utilisateur.nom not in self.utilisateurs:
            self.utilisateurs[utilisateur.nom] = utilisateur
            return True
        print("Cet utilisateur existe déjà")
        return False

    # Méthode pour emprunter un livre
    def emprunter(self, nom, titre):
        # Vérifier que l'utilisateur existe
        if nom not in self.utilisateurs:
            print("Utilisateur inconnu")
            return False
        # Vérifier que le livre existe
        if titre not in self.livres:
            print("Livre inconnu")
            return False
        # Récupérer l'utilisateur et le livre
        utilisateur = self.utilisateurs[nom]
        livre = self.livres[titre]
        # Essayer d'emprunter le livre
        if utilisateur.emprunter_livre(livre):
            print("Emprunt effectué avec succès")
            return True
        print("Ce livre est déjà emprunté")
        return False

    # Méthode pour rendre un livre
    def rendre(self, nom, titre):
        # Vérifier que l'utilisateur existe
        if nom not in self.utilisateurs:
            print("Utilisateur inconnu")
            return False
        # Vérifier que le livre existe
        if titre not in self.livres:
            print("Livre inconnu")
            return False
        # Récupérer l'utilisateur et le livre
        utilisateur = self.utilisateurs[nom]
        livre = self.livres[titre]
        # Vérifier que cet utilisateur a emprunté le livre
        if utilisateur.rendre_livre(livre):
            print("Livre rendu avec succès")
            return True
        print("Cet utilisateur n'a pas emprunté ce livre")
        return False

    # Méthode pour afficher tous les livres
    def afficher_livres(self):
        # Vérifier si la bibliothèque est vide
        if len(self.livres) == 0:
            print("Aucun livre dans la bibliothèque")
            return
        # Parcourir tous les livres
        for livre in self.livres.values():
            # Afficher les informations du livre
            livre.afficher()
            # Séparer les livres pour faciliter la lecture
            print("--------------------")



# TESTS DE LA PARTIE B
if __name__ == "__main__":

    # Créer une bibliothèque
    biblio = Bibliotheque()

    # Créer deux livres
    livre1 = Livre("1984", "Orwell", 1949)
    livre2 = Livre("Le Petit Prince", "Saint-Exupéry", 1943)

    # Créer deux utilisateurs
    ana = Utilisateur("Ana")
    leo = Utilisateur("Léo")

    # Ajouter les livres à la bibliothèque
    biblio.ajouter_livre(livre1)
    biblio.ajouter_livre(livre2)

    # Ajouter les utilisateurs
    biblio.ajouter_utilisateur(ana)
    biblio.ajouter_utilisateur(leo)

    # Test 1 : Ana emprunte le livre 1984
    print("\nTEST 1 - Emprunt par Ana")
    assert biblio.emprunter("Ana", "1984") is True

    # Test 2 : Léo essaie d'emprunter le même livre
    print("\nTEST 2 - Livre déjà emprunté")
    assert biblio.emprunter("Léo", "1984") is False

    # Test 3 : Utilisateur inconnu
    print("\nTEST 3 - Utilisateur inconnu")
    assert biblio.emprunter("Paul", "1984") is False

    # Test 4 : Livre inconnu
    print("\nTEST 4 - Livre inconnu")
    assert biblio.emprunter("Ana", "Harry Potter") is False

    # Test 5 : Léo essaie de rendre le livre d'Ana
    print("\nTEST 5 - Mauvais emprunteur")
    assert biblio.rendre("Léo", "1984") is False

    # Vérifier qu'Ana reste l'emprunteuse
    assert livre1.emprunteur == "Ana"
    assert livre1.disponible is False

    # Test 6 : Ana rend son livre
    print("\nTEST 6 - Retour par Ana")
    assert biblio.rendre("Ana", "1984") is True

    # Vérifier que le livre est disponible
    assert livre1.disponible is True
    assert livre1.emprunteur is None

    # Test 7 : Afficher les livres
    print("\nTEST 7 - Affichage des livres")
    biblio.afficher_livres()


