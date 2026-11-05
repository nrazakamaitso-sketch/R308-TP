# Importe le module random
import random


# Choisit un nombre aleatoire entre 1 et 100
nombre_secret = random.randint(1, 100)
# Initialise le nombre d'essais a 0
essais = 0
# Indique que le joueur n'a pas encore gagné
gagne = False


# Répète le jeu tant que le joueur a moins de 10 essais
while essais < 10:
    # Demande un nombre au joueur
    nombre_joueur = int(input("Entre ton nombre : "))

    # Ajoute 1 au nombre d'essais
    essais = essais + 1

    # Vérifie si le nombre proposé est trop petit
    if nombre_joueur < nombre_secret:
        print("Trop petit")

    # Vérifie si le nombre proposé est trop grand
    elif nombre_joueur > nombre_secret:
        print("Trop grand")

    # Sinon, le joueur a trouvé le nombre
    else:
        print("Gagné")
        # Indique que le joueur a gagné
        gagne = True
        # Arrête la boucle
        break


# Vérifie si le joueur n'a pas gagné après 10 essais
if not gagne:
    # Affiche le nombre secret
    print("Perdu ! Le nombre était", nombre_secret)