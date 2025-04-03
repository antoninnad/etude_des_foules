import tkinter as tk
from tkinter import messagebox

import random
import numpy as np
import math
import time

from affichage import *


# partie principale

tab_personne = []

arene = configuration()


for x in range(15):

    tab_personne.append({
        "position": np.array([100, 70 + 30 * x]),
        "masse": 10,
        "vitesse_desiree": 1.34 + random.randint(-1, 1) * random.randint(0, 25) * .01, 
        "vitesse": np.array([0, 0]),
        "to": .2,
        "rayon": 10 +  random.randint(-2, 2)
    })



"""

    fonction pour le calcul du model social

"""

def calcul_ei0(personne):


    #position de la porte
    pt_souhaite = np.array([624, 335])
    vecteur_ei0 =  pt_souhaite - personne["position"]

    norm = np.linalg.norm(vecteur_ei0)

    

    vecteur_ei0 = vecteur_ei0 / norm

    assert( math.isclose(np.linalg.norm(vecteur_ei0), 1) )

    return vecteur_ei0
        

def force_motrice(personne):

    resultat = personne["vitesse_desiree"] * calcul_ei0(personne) - personne["vitesse"]

    resultat = resultat /  personne["to"]

    return resultat

def force_intercation_social(personne, indice, b0 = 0.8):

    resultat = 0

    for indice_personne, personne_autre  in enumerate(tab_personne):

        if indice_personne != indice:

            a = personne["position"]
            b = personne_autre["position"]

            norme_ab = np.linalg.norm(a - b) - personne_autre["rayon"] - personne["rayon"]

            if np.exp((- norme_ab / .08)) * (a - b)[0] > 1_000:
                print(f"norm {norme_ab}")
                print(f"\n vect {(a - b)}")

            resultat =  resultat + np.exp((- norme_ab / b0)) * (a - b)

            #print(f"norme: {norme_ab} force {np.exp((- norme_ab / .08)) * (a - b)}")
    return resultat


def angle_between_vectors(u, v):
    dot_product = np.dot(u, v)
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    cos_theta = dot_product / (norm_u * norm_v)

    return np.arccos(np.clip(cos_theta, -1.0, 1.0)) 

def distance_mur_vect(coord_a, coord_b,  coord_personne):

    AP = coord_personne - coord_a
    AB = coord_b - coord_a

    alpha = angle_between_vectors(AP,AB)

    
    PE = np.linalg.norm(AP) * np.sin(alpha)


def force_intercation_social_mur(personne, indice, b0 = 0.8):

    coord_a = np.array([50, 50])
    coord_b = np.array([600,50])
    coord_c = np.array([600,600])
    coord_d = np.array([50, 600])


    print(distance_mur_vect(coord_b, coord_c, personne["position"]))

    return 0


def euler(personne,indice, step=.02):

    f_m = force_motrice(personne)

    a = force_intercation_social(personne, indice)

    f_m += force_intercation_social_mur(personne , indice)

    
    
    f_m += a

    #projection sur Ux et Uy
    vitesse_x =  personne["vitesse"][0] + step * f_m[0]
    vitesse_y = personne["vitesse"][1] + step * f_m[1]

    
    #on actualise la position
    personne["position"] = np.array( [
        personne["position"][0] + vitesse_x,
        personne["position"][1] + vitesse_y 
    ])

    # v(t_n+&)
    personne["vitesse"] = np.array([
        vitesse_x,
        vitesse_y
    ])

    #print(personne["position"])

    #print(f"\n\nv= |{vitesse_x}|\n  |{vitesse_y}|")


    


class app:

    def __init__(self):


        self.root = tk.Tk()
        self.root.title("Experience")


        self.root.geometry("1400x700")

        self.canvas = tk.Canvas(self.root, width=600 * 2, height=700, bg="white")

        #bouton lié à l'evt start
        self.button = tk.Button(self.root, text="Commencer", command=self.start)
        self.button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


        self.temps = tk.Label(self.root, text="Temps 0.0 s", bg="white", fg="black", font=("Arial", 14))
        

           
        self.root.mainloop()

    def afficher(self):
        """
            dessine chaque persone
        """

        self.canvas.pack()
        self.canvas.delete("all")

        

        arene.afficher(self.canvas)

        for indice,personne in enumerate(tab_personne):
            
            
            dessiner_cercle(
                self.canvas, 
                personne["position"][0], # x
                personne["position"][1], # y
                personne["rayon"], 
                "blue"
            )

    
    def start(self):
        """
            démarre le jeu
        """
        self.button.destroy()
        self.temps.pack(side="left", padx=10, pady=5)


        self.debut = time.time()
        self.model()
        

    def model(self):

        """
            modélise le mouvement des personnes
        """

        

        for indice in range(len(tab_personne)):

            if indice <= (len(tab_personne) - 1):
            
                personne = tab_personne[indice]
            
                #application physique
                euler(personne, indice)

                if personne["position"][0] > 623.5:
                    tab_personne.pop(indice)

        if len(tab_personne) != 0:
    
            self.afficher()
            self.temps["text"] = f"Temps {time.time() - self.debut:.2f} s"
            self.root.after(30, self.model)
        
        else:
            self.temps["text"] = f"Temps {time.time() - self.debut:.2f} s"
            messagebox.showinfo("Resultat", f"Fait en {time.time() - self.debut} secondes")

            return
        
        

if __name__ == "__main__":
    app()