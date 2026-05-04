import tkinter as tk
import random
import os



paquet = []
valeurs = ["As", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Valet", "Reine", "Roi"]                                #modification des paquets en couleurs et valeurs pour uafficher les cartes de manière différentes 
couleurs = ["pique", "coeur", "trefle", "carreau"]

for cartes in valeurs:
    for c in couleurs:
        paquet.append(f"{cartes}_{c}")    #affichage chaque carte pour sa "famille"

def paquet_melange(paquet):
    paquet_copie = paquet.copy()            #assignation pour ne pas faire de modifications dans 2 fois le même paquet et pour ne pas supprimer les cartes precedemment mis dans le paquet 
    nouveau_paquet = []
    while len(paquet_copie) > 0:
        numero_carte = random.randint(0, len(paquet_copie) - 1)                                
        nouveau_paquet.append(paquet_copie.pop(numero_carte))
    return nouveau_paquet


def tirer_cartes(liste):
    carte = liste.pop()                            #liste = nouveau_paquet
    return carte


def creer_main(liste):
    main = []
    main.append(tirer_cartes(liste))                                #on va ajouter à la main les cartes tirées precedemment
    main.append(tirer_cartes(liste))
    return main


def calculer_score(joueur):                                         #tout les compteurs sont à zero pour la règle de l'As
    score = 0
    nombre_as = 0

    for carte in joueur:
        valeur = carte.split("_")[0] 

        if valeur == "As":
            score += 11
            nombre_as += 1
        elif valeur in ["2", "3", "4", "5", "6", "7", "8", "9", "10"]:
            score += int(valeur)
        elif valeur in ["Valet", "Reine", "Roi"]:
            score += 10
    while score > 21 and nombre_as > 0:
        score -= 10
        nombre_as -= 1
    return score


def brule(joueur):
    est_brule = False
    if calculer_score(joueur) > 21:                            # tant que c'est inferieur à 21 ca joue 
        est_brule = True                                       #respect des regles du blackjack
    return est_brule                                           #

def comparer_score(joueur,croupier):
    global mise
    score_joueur = calculer_score(joueur)
    score_croupier = calculer_score(croupier)
    if score_croupier > score_joueur:
        afficher_message("Score croupier : " + str(score_croupier) + ". Votre score : " + str(score_joueur) + ". Vous avez perdu")
        mise = mise - 10
        afficher_etat()
    elif score_joueur == score_croupier:
        afficher_message("Score croupier : " + str(score_croupier) + ". Votre score : " + str(score_joueur) + ". Il y a égalité")
    else:
        afficher_message("Score croupier : " + str(score_croupier) + ". Votre score : " + str(score_joueur) + ". Vous avez gagné")
        mise = mise + 10
        afficher_etat()

#-----------------------------------------------------------------INTERFACE---------------------------------------------------------------------#


racine = tk.Tk()
racine.title("Blackjack - Interface joueur")                        
racine.geometry("780x500")
racine.config(bg="darkgreen")


paquet_carte = []
joueur = []
croupier = []
tour_en_cours = False
mise = 50

images_cartes = {} #création d'un dictionnaire pour ne pas faire de conditions à chaque cartes#

def charger_cartes():
    for cartes in valeurs:
        for c in couleurs:
            nom_carte = f"{cartes}_{c}"
            #route = f"cartes/{nom_carte}.png" cela aurait du être le chemin utilisé pour trouver les images

            BASE_DIR = os.path.dirname(__file__)
            route = os.path.join(BASE_DIR, "cartes", nom_carte + ".png")                        
            images_cartes[nom_carte] = tk.PhotoImage(file=route).subsample(7,7)


BASE_DIR = os.path.dirname(__file__)

route_dos = os.path.join(BASE_DIR, "cartes", "dos.png")
image_dos = tk.PhotoImage(file=route_dos).subsample(5,5)

charger_cartes() #on appelle la fonction pour pouvoir afficher les cartes tirées plus tard 

frame_croupier = tk.Frame(racine, bg="darkgreen")
frame_croupier.grid(row=2, column=1, columnspan=3)

frame_joueur = tk.Frame(racine, bg="darkgreen")
frame_joueur.grid(row=5, column=1, columnspan=3)



def afficher_main_graphique(main, frame):
    # Vide le conteneur pour chaque nouvelle partie
    for widget in frame.winfo_children():
        widget.destroy()

    #garder les réf d'images
    frame.images = []

    for carte in main:
        img = images_cartes[carte]

        label = tk.Label(frame, image=img, bg="darkgreen")
        label.pack(side="left", padx=5)

        #garder la carte affichée
        frame.images.append(img)
        label.image = img

def afficher_main_croupier(main, frame, cacher_deuxieme=True):
    for widget in frame.winfo_children():
        widget.destroy()

    frame.images = []

    for i, carte in enumerate(main):
        if cacher_deuxieme and i == 1:
            img = image_dos  
        else:
            img = images_cartes[carte]

        label = tk.Label(frame, image=img, bg="darkgreen")
        label.pack(side="left", padx=5)

        frame.images.append(img)


def texte_mise():
    global mise
    return str(mise)


def afficher_etat():
    afficher_main_graphique(joueur, frame_joueur)
    label_score_joueur.config(text="Score joueur : " + str(calculer_score(joueur)))
    afficher_main_graphique(croupier, frame_croupier)
    afficher_main_croupier(croupier, frame_croupier, cacher_deuxieme=tour_en_cours)
    dessiner_pile_jetons()


def afficher_message(message):
    label_message.config(text=message)


def nouvelle_partie():
    global paquet_carte, joueur, croupier, tour_en_cours, mise
    paquet_carte = paquet_melange(paquet)
    joueur = creer_main(paquet_carte)
    croupier = creer_main(paquet_carte)
    tour_en_cours = True
    mise = 50
    afficher_etat()
    afficher_message("Nouvelle partie commencée. Choisissez une action.")
    bouton_hit.config(state="normal")
    bouton_stand.config(state="normal")
    bouton_dd.config(state = "normal")
    bouton_surrender.config(state = "normal")
    bouton_nouvelle.config(text ="Prochain Tour",state="disabled")


def action_hit():
    global tour_en_cours, mise
    if tour_en_cours == False:
        return
    carte = tirer_cartes(paquet_carte)
    joueur.append(carte)
    afficher_etat()
    if brule(joueur):
        afficher_message("Vous avez tiré " + carte + ". Vous avez trop de points, fin du tour.")
        bouton_hit.config(state="disabled")
        bouton_stand.config(state="disabled")
        bouton_dd.config(state = "disabled")
        bouton_nouvelle.config(state="normal")
        bouton_surrender.config(state="disabled")
        tour_en_cours = False
        mise = mise - 10
        afficher_etat()
        return
    if calculer_score(joueur) == 21:
        afficher_message("Vous avez 21 points. Vous avez gagné")
        bouton_hit.config(state="disabled")
        bouton_stand.config(state="disabled")
        bouton_dd.config(state ="disabled")
        bouton_surrender.config(state = "disabled")
        bouton_nouvelle.config(state = "normal")
        tour_en_cours = False
        mise = mise + 10
        afficher_etat()
        return
    afficher_message("Vous avez tiré " + carte + ". Voulez-vous continuer ou vous arrêter ? (Hit/Stand)")


def action_stand():
    global tour_en_cours
    if tour_en_cours == False:
        return
    afficher_message("Votre tour est terminé.")
    bouton_hit.config(state="disabled")
    bouton_stand.config(state="disabled")
    bouton_dd.config(state="disabled")
    bouton_surrender.config(state="disabled")
    bouton_nouvelle.config(state ="normal")
    if calculer_score(joueur) == 21:
        afficher_message("Vous avez 21 points. Vous avez gagné")        
        bouton_hit.config(state="disabled")
        bouton_stand.config(state="disabled")
        bouton_dd.config(state="disabled")
        bouton_surrender.config(state="disabled")
        bouton_nouvelle.config(state = "normal")
        tour_en_cours = False
        return
    elif not brule(joueur):
        return comparer_score(joueur,croupier)

def dessiner_pile_jetons():
    canvas_jetons.delete("all")

    # 5 jetons noirs fixes
    for i in range(5):
        y_decalage = 60 - i * 8
        canvas_jetons.create_oval(20, y_decalage,100, y_decalage + 30,fill="black",outline="white",width=2)

    # texte sur le jeton du dessus
    y_haut = 60 - 4 * 8
    canvas_jetons.create_text(60, y_haut + 15,text=str(mise),fill="white",font=("Helvetica", 11, "bold"))

def action_dd():
    global tour_en_cours, mise, paquet_carte
    if len(joueur) == 2 and calculer_score(joueur) in [9,10,11]:
        bouton_hit.config(state="disabled")
        bouton_stand.config(state="disabled")
        bouton_dd.config(state = "disabled")
        bouton_surrender.config(state = "disabled")
        bouton_nouvelle(state = "normal")
        mise = mise * 2
        carte = tirer_cartes(paquet_carte)
        joueur.append(carte)
        afficher_etat()
        return comparer_score(joueur,croupier)
    else:
        afficher_message("Vous ne pouvez pas faire cette action, vous devez faire une autre action")
        bouton_dd.config(state = "disabled")
        return




def action_surrender():
    global tour_en_cours, mise, paquet_carte
    mise = mise//2                                                
    afficher_message("Vous avez abandonné")
    bouton_hit.config(state="disabled")
    bouton_stand.config(state="disabled")
    bouton_dd.config(state="disabled")
    bouton_surrender.config(state="disabled")
    bouton_nouvelle.config(state="normal")
    afficher_etat()
    tour_en_cours = False
    return





label_titre = tk.Label(racine, text="BLACKJACK", font=("Helvetica", 22, "bold"), bg="darkgreen", fg="white")
label_titre.grid(row=0, column=1, columnspan=3, pady=20)

label_main_croupier = tk.Label(racine, text="Main croupier : ", font=("Helvetica", 14), bg="darkgreen", fg="white")
label_main_croupier.grid(row=1, column=1, columnspan=3, pady=10)

label_main_joueur = tk.Label(racine, text="Main joueur : ", font=("Helvetica", 14), bg="darkgreen", fg="white")
label_main_joueur.grid(row=4, column=1, columnspan=3, pady=20)

canvas_jetons = tk.Canvas(racine, width=120, height=100, bg="darkgreen", highlightthickness=0)
canvas_jetons.grid(row=1, column=0, rowspan=2, pady=10)

label_mise = tk.Label(racine, text="Mise", bg="darkgreen", fg="white", font=("Helvetica", 12))
label_mise.grid(row=1, column=0, pady=30)

label_score_joueur = tk.Label(racine, text="Score joueur : ", font=("Helvetica", 12), bg="darkgreen", fg="white")
label_score_joueur.grid(row=6, column=1, columnspan=3)

label_message = tk.Label(racine, text="Cliquez sur Nouvelle partie", font=("Helvetica", 12, "italic"), bg="darkgreen", fg="yellow")
label_message.grid(row=7, column=1, columnspan=3, pady=20)

bouton_hit = tk.Button(racine, text="Hit", width=12, font=("Helvetica", 12), command=action_hit)
bouton_hit.grid(row=8, column=0, padx=10, pady=20)

bouton_stand = tk.Button(racine, text="Stand", width=12, font=("Helvetica", 12), command=action_stand)
bouton_stand.grid(row=8, column=1, padx=10, pady=20)

bouton_dd = tk.Button(racine, text= "Double Down", width = 12, font=("Helvetica",12), command = action_dd)
bouton_dd.grid(row = 8, column = 2, padx=10, pady = 20)

bouton_surrender = tk.Button(racine, text = "Surrender", width = 12, font = ("Helvetica", 12), command = action_surrender)
bouton_surrender.grid(row = 8, column = 3, padx= 10, pady = 20)

bouton_nouvelle = tk.Button(racine, text="Nouvelle partie", width=18, font=("Helvetica", 12), command=nouvelle_partie)
bouton_nouvelle.grid(row=8, column=4, padx=10, pady=20)


bouton_hit.config(state="disabled")
bouton_stand.config(state="disabled")
bouton_dd.config(state ="disabled")
bouton_surrender.config(state = "disabled")

racine.mainloop()
