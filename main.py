import tkinter as tk
import random
import numpy as np
import math
from affichage import *


# partie principale

tab_personne = []

arene = configuration()


for x in range(3):

    tab_personne.append({
        "position": np.array([100 + 30 * x, 70]),
        "masse": 10,
        "vitesse_desiree": 1.34 ,#+ random.randint(-1, 1) * random.randint(0, 25) * .01, 
        "vitesse": np.array([0, 0]),
        "to": .2,
        "rayon": 10 + random.randint(-1, 1) * random.randint(0, 2)
    })



"""

    fonction pour le calcul du model social

"""

def calcul_ei0(personne):


    #position de la porte
    pt_souhaite = np.array([620, 370])
    vecteur_ei0 =  pt_souhaite - personne["position"]

    norm = np.linalg.norm(vecteur_ei0)

    

    vecteur_ei0 = vecteur_ei0 / norm

    assert( math.isclose(np.linalg.norm(vecteur_ei0), 1) )

    return vecteur_ei0
        

def force_motrice(personne):

    resultat = personne["vitesse_desiree"] * calcul_ei0(personne) - personne["vitesse"]

    resultat = resultat /  personne["to"]

    return resultat





def euler(personne, step=.02):

    f_m = force_motrice(personne)

    vitesse_x =  personne["vitesse"][0] + step * f_m[0]
    vitesse_y = personne["vitesse"][1] + step * f_m[1]

    

    personne["position"][0] = personne["position"][0] + vitesse_x 
    personne["position"][1] = personne["position"][1] + vitesse_y 
    



    personne["vitesse"] = np.array([
        vitesse_x,
        vitesse_y
    ])

    print(personne["position"])

    print(f"\n\nv= |{vitesse_x}|\n  |{vitesse_y}|")

    #projection sur Ux
    


class app:

    def __init__(self):


        self.root = tk.Tk()
        self.root.title("Experience")


        self.root.geometry("1400x700")

        self.canvas = tk.Canvas(self.root, width=600 * 2, height=700, bg="white")

        #bouton lié à l'evt start
        self.button = tk.Button(self.root, text="Commencer", command=self.start)
        self.button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

           
        self.root.mainloop()

    def afficher(self):
        """
            dessine chaque persone
        """
        self.canvas.pack()
        self.button.destroy()

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

        self.model()

    def model(self):

        """
            modélise le mouvement des personnes
        """


        for indice in range(len(tab_personne)):
            
            personne = tab_personne[indice]
            # deplace une persoone

            euler(personne)


        


        self.afficher()
        self.root.after(30, self.model)
        
        

if __name__ == "__main__":
    app()