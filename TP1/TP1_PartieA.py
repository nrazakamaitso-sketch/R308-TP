# 1. Création du dictionnaire
etudiants = {}

# Ajout des étudiants
etudiants["Alice"] = 12.0
etudiants["Bob"] = 15.0
etudiants["Claire"] = 9.5


# 2. Fonction pour ajouter un étudiant
def ajouter_etudiant(d, nom, note):
    # Ajoute ou modifie l'étudiant
    d[nom] = note


# 3. Fonction pour calculer la moyenne
def moyenne_classe(d):
    # Vérifie si le dictionnaire est vide
    if len(d) == 0:
        return None

    # Initialise la somme
    somme = 0

    # Parcourt toutes les notes
    for note in d.values():
        somme = somme + note

    # Calcule la moyenne
    moyenne = somme / len(d)

    # Renvoie la moyenne
    return moyenne


# 4. Fonction pour trouver le meilleur étudiant
def meilleur_etudiant(d):
    # Vérifie si le dictionnaire est vide
    if len(d) == 0:
        return None

    # Initialise la meilleure note
    meilleure_note = 0
    meilleur_nom = None

    # Parcourt les étudiants
    for nom, note in d.items():

        # Compare les notes
        if note > meilleure_note:
            meilleure_note = note
            meilleur_nom = nom

    # Renvoie le nom et la note
    return (meilleur_nom, meilleure_note)


# 5. Fonction pour sauvegarder les étudiants
def sauvegarder_etudiants(d, nom_fichier):
    try:
        # Ouvre le fichier en écriture
        with open(nom_fichier, "w") as fichier:

            # Parcourt le dictionnaire
            for nom, note in d.items():

                # Écrit nom:note dans le fichier
                fichier.write(f"{nom}:{note}\n")

    except OSError:
        # Gère les erreurs de fichier
        print("Erreur lors de la sauvegarde")


# 6. Fonction pour charger les étudiants
def charger_etudiants(nom_fichier):
    # Crée un dictionnaire vide
    etudiants = {}

    try:
        # Ouvre le fichier en lecture
        with open(nom_fichier, "r") as fichier:

            # Parcourt chaque ligne
            for ligne in fichier:

                try:
                    # Sépare le nom et la note
                    nom, note = ligne.strip().split(":")

                    # Convertit la note en nombre décimal
                    note = float(note)

                    # Ajoute l'étudiant au dictionnaire
                    etudiants[nom] = note

                except ValueError:
                    # Gère les lignes mal formées
                    print("Ligne mal formée")

    except FileNotFoundError:
        # Gère le fichier inexistant
        print("Fichier absent")

    # Renvoie le dictionnaire
    return etudiants



# Affiche la moyenne
print("Moyenne :", moyenne_classe(etudiants))


# Affiche le meilleur étudiant
print("Meilleur étudiant :", meilleur_etudiant(etudiants))


# Sauvegarde dans un fichier
sauvegarder_etudiants(etudiants, "etudiants.txt")


# Recharge les étudiants depuis le fichier
etudiants_charges = charger_etudiants("etudiants.txt")


# Affiche les étudiants rechargés
print("Étudiants chargés :", etudiants_charges)