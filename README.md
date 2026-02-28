#  Projet BlackJack
import random

paquet = 4*["As","2","3","4","5","6","7","8","9","10","Valet","Reinne","Roi"]

def tirer_cartes(liste):
    a = random.randint(0,len(liste)-1)
    carte = liste.pop(a)
    return carte

def creer_main(liste):
    main  = []
    main.append(tirer_cartes(liste))
    main.append(tirer_cartes(liste))
    return main

def calculer_score(joueur):
    score = 0
    for carte in joueur:
        if carte == "As":
            a = int(input("Vous avez",score," ,voulez-vous misez 1 ou 11?  (1/11) "))
            score += a
        elif carte in ["Valet","Reine","Roi"]:
            score += 10
        else:
            score += int(carte)
    return score

def brule(joueur):
    est_brule = False
    if calculer_score(joueur) > 21:
        est_brule = True
    return est_brule

def tour_joueur(joueur,liste):
    actions = ["Hit","Stand","Double Down","Surrender"]
    est_vrai = True
    while est_vrai == True:
        a = input("Que voulez vous faire? (Hit/Stand/Double Down/Surrender) ")
        if a in actions:
            est_vrai = False
    if a == "Double Down":
        if len(joueur) != 2 and (calculer_score(joueur) != 9 or calculer_score(joueur) != 10 or calculer_score(joueur) != 11):
            print("Vous ne pouvez pas faire cette action")
            a = "Hit"
#A completer avec les mises
    if a == "Hit":
        continuer = True
        while continuer == True:
            joueur.append(tirer_cartes(liste))
            if brule(joueur) == True:
                print("Vous avez trop de points, fin du tour ")
                return None
            else: 
                continuer = bool(input("Voulez-vous continuer? (True/False) "))
        return None
    if a == "Stand":
        return None
#if a == "Surrender":
#A completer avec les mises      



#Verrification

nb_joueurs = int(input("Combien de joueurs?  "))
joueurs = []
for i in range (nb_joueurs):
    joueur = creer_main(paquet)
    joueurs.append(joueur)
print(joueurs)
print(joueur)
print(calculer_score(joueur))
