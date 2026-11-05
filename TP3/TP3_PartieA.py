# Classe qui représente un livre
class Livre:

    # Constructeur : initialise les informations du livre
    def __init__(self, titre, auteur, annee):
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.disponible = True  # Le livre est disponible au départ
        self.emprunteur = None  # Personne n'a encore emprunté le livre

    # Méthode pour afficher les informations du livre
    def afficher(self):
        print("Titre :", self.titre)
        print("Auteur :", self.auteur)
        print("Année :", self.annee)
        # Vérifier si le livre est disponible
        if self.disponible:
            print("Statut : Disponible")
        else:
            print("Statut : Emprunté par", self.emprunteur)

    # Méthode pour emprunter un livre
    def emprunter(self, nom):
        # Vérifier si le livre est disponible
        if self.disponible:
            self.disponible = False  # Le livre devient indisponible
            self.emprunteur = nom    # Enregistrer le nom de l'emprunteur
            return True
        # Si le livre est déjà emprunté
        return False

    # Méthode pour rendre un livre
    def rendre(self):
        # Vérifier si le livre est actuellement emprunté
        if not self.disponible:
            self.disponible = True   # Le livre redevient disponible
            self.emprunteur = None   # Effacer le nom de l'emprunteur
            return True
        # Si le livre est déjà disponible
        return False

# Classe qui représente un utilisateur
class Utilisateur:
    # Constructeur : initialise le nom et les emprunts
    def __init__(self, nom):
        self.nom = nom
        self.emprunts = []  # Liste des livres empruntés
    # Méthode pour emprunter un livre
    def emprunter_livre(self, livre):
        # Essayer d'emprunter le livre
        if livre.emprunter(self.nom):
            # Ajouter le livre à la liste des emprunts
            self.emprunts.append(livre)
            return True
        # Si l'emprunt a échoué
        return False

    # Méthode pour rendre un livre
    def rendre_livre(self, livre):
        # Vérifier que le livre appartient aux emprunts
        if livre in self.emprunts:
            # Essayer de rendre le livre
            if livre.rendre():
                # Retirer le livre de la liste
                self.emprunts.remove(livre)
                return True
        # Si le retour a échoué
        return False

    # Méthode pour afficher les livres empruntés
    def afficher_emprunts(self):
        # Vérifier si la liste est vide
        if len(self.emprunts) == 0:
            print("Aucun livre emprunté")
        else:
            print("Livres empruntés par", self.nom, ":")
            # Parcourir la liste des livres empruntés
            for livre in self.emprunts:
                print("-", livre.titre)


# TESTS DE LA PARTIE A
if __name__ == "__main__":

    # Créer un livre
    livre1 = Livre("1984", "Orwell", 1949)

    # Créer deux utilisateurs
    ana = Utilisateur("Ana")
    leo = Utilisateur("Léo")

    # Afficher le livre avant l'emprunt
    livre1.afficher()

    # Ana emprunte le livre
    print("Emprunt par Ana :", ana.emprunter_livre(livre1))

    # Léo essaie d'emprunter le même livre
    print("Emprunt par Léo :", leo.emprunter_livre(livre1))

    # Afficher les emprunts d'Ana
    ana.afficher_emprunts()

    # Ana rend le livre
    print("Retour par Ana :", ana.rendre_livre(livre1))

    # Vérifier que le livre est de nouveau disponible
    livre1.afficher()
