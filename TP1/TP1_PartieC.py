# Importe le module random
import random


# 1. Charger la liste de mots
try:
    # Ouvre le fichier mots.txt en lecture
    with open("mots.txt", "r") as fichier:

        # Récupère chaque ligne dans une liste
        mots = fichier.read().splitlines()

except FileNotFoundError:
    # Affiche un message si le fichier n'existe pas
    print("Le fichier mots.txt est introuvable")

    # Crée une liste vide
    mots = []

# 2. Fonction pour choisir un mot
def choisir_mot(liste):
    # Vérifie que la liste n'est pas vide
    if len(liste) == 0:
        return None
    # Choisit un mot au hasard
    mot = random.choice(liste)
    # Transforme le mot en majuscules
    return mot.upper()


def masque(mot):
    # Crée une liste de "_" de la même longueur que le mot
    resultat = ["_"] * len(mot)

    # Renvoie le masque
    return resultat


# Choisit un mot
mot = choisir_mot(mots)

# Affiche le mot choisi
print("Mot choisi :", mot)

# Crée le masque du mot
print("Masque :", masque(mot))

