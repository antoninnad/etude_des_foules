import tkinter as tk
from tkinter import messagebox

import random
import numpy as np
import math
import time


from physique import euler
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
                euler(tab_personne, personne, indice)

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