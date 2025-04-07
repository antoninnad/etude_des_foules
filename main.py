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



def initialiser_tab_personne():

    tab = []

    for y in range(3):
        for x in range(15):

            tab.append({
                "position": np.array([100 + 30 * y, 100 + 30 * x]),
                "masse": 10,
                "vitesse_desiree": 1.34 + random.randint(-1, 1) * random.randint(0, 25) * .01, 
                "vitesse": np.array([0, 0]),
                "to": .2,
                "rayon": 10 +  random.randint(-2, 2)

            })


    return tab

tab_personne = initialiser_tab_personne()


class app:

    def __init__(self):


        self.root = tk.Tk()
        self.root.title("Experience")


        self.root.geometry("1400x700")

        self.canvas = tk.Canvas(self.root, width=600 * 2, height=700, bg="white")

        #bouton lié à l'evt start
        self.button = tk.Button(self.root, text="Commencer simulation basique", command=self.start2)
        self.button.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

        self.button2 = tk.Button(self.root, text="Commencer simulation obsatcles", command=self.start)
        self.button2.place(relx=0.5, rely=0.55, anchor=tk.CENTER)


        self.temps = tk.Label(self.root, text="Temps 0.0 s", bg="white", fg="black", font=("Arial", 14))
        self.nombre = len(tab_personne)
        
        self.particule = tk.Label(self.root, text=f"Personnes {self.nombre}/{self.nombre}", bg="white", fg="black", font=("Arial", 14))
        self.restart = tk.Button(self.root, text="Restart", command=self.restart_action)

        self.stop = False
        self.stopBtn = tk.Button(self.root, text="Stop", command=self.stop_action)
           
        self.vitesse = 1

        self.slider = tk.Scale(self.root, from_=0, to=100, orient="horizontal", length=200, command=self.augmenter_vitesse)
        self.slider.set(53)  # Valeur initiale

        
        self.root.mainloop()

    def augmenter_vitesse(self, val):
        val = float(val)

        debut = .2
        fin = 30


        if val <= 50:
            # Appliquer une échelle de debut à 1
            display_val = debut + (val / 50) * (1 - debut)
        else:
            # Appliquer une échelle de 1 à fin
            display_val = 1 + ((val - 50) / 50) * (fin - 1)  

        self.vitesse = float(display_val)

    def restart_action(self):

        global tab_personne

        tab_personne = initialiser_tab_personne()
        self.debut = 0
        self.nombre = len(tab_personne)
        self.particule["text"] = f"Personnes {self.nombre}/{self.nombre}"


        self.model()


    def stop_action(self):
        self.stop = not self.stop

    def afficher(self):
        """
            dessine chaque persone
        """

        self.canvas.pack()
        self.canvas.delete("all")

        

        self.arene.afficher(self.canvas)

        for indice,personne in enumerate(tab_personne):
            
            
            dessiner_cercle(
                self.canvas, 
                personne["position"][0], # x
                personne["position"][1], # y
                personne["rayon"], 
                "blue"
            )

    def start2(self):
        """
            démarre la simulation
        """
        self.button.destroy()
        self.button2.destroy()

        self.temps.pack(side="left", padx=10, pady=5)
        self.particule.pack(side="left", padx=10, pady=25)
        self.stopBtn.place(x= 10,y= 10)
        self.restart.place(x= 10,y=50)
        self.slider.place(x=10,y=80)

        self.arene = configuration()

        self.arene.obstacles = []
        
        self.debut = 0
        self.model()
    
    def start(self):
        """
            démarre la simulation
        """
        self.button.destroy()
        self.button2.destroy()

        self.temps.pack(side="left", padx=10, pady=5)
        self.particule.pack(side="left", padx=10, pady=25)
        self.stopBtn.place(x= 10,y= 10)
        self.restart.place(x= 10,y=50)
        self.slider.place(x=10,y=80)

        self.arene = configuration()
        
        self.debut = 0
        self.model()
        

    def update(self, personne):
        personne.deplacer(1,1)

        x = personne.coordonnees[0]
        y = personne.coordonnees[1]
    def model(self):

        """
            modélise le mouvement des personnes
        """


        for indice in range(len(tab_personne)):
            
            personne = tab_personne[indice]
            # deplace une persoone

        if x < 70 or x > 580:
            personne.coordonnees[0] = random.randint(70,580)
        if y < 70 or y > 580:
            personne.coordonnees[1] = random.randint(70,580)
            tab_personne[indice]["x"] += 1
            tab_personne[indice]["y"] += 1

            x = personne["x"]
            y = personne["y"]

        



    def model(self):

        """
            modélise le mouvement des personnes
        """
        if self.stop:
            self.root.after(30, self.model)
            return

        for indice in range(len(tab_personne)):

            if indice <= (len(tab_personne) - 1):
            
                personne = tab_personne[indice]
            
                #application physique
                euler(tab_personne, personne, indice, self.arene.obstacles)

                if personne["position"][0] > 610:
                    tab_personne.pop(indice)

        self.particule["text"] = f"Personnes {len(tab_personne)}/{self.nombre}"

        if len(tab_personne) != 0:
    
            self.afficher()
            self.temps["text"] = f"Temps {self.debut:.2f} s"

            self.debut += 0.03
            self.root.after( int(30 / self.vitesse), self.model)
        
        else:
            self.temps["text"] = f"Temps {self.debut:.2f} s"
            messagebox.showinfo("Resultat", f"Fait en {self.debut:.2f} secondes")

            return
        
        

if __name__ == "__main__":
    app()