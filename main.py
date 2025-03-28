import tkinter as tk
import random

from affichage import *


# partie principale

tab_personne = []

arene = configuration()

for x in range(10):
    tab_personne.append({
        "x": 100 + 20 * x,
        "y": 60,
        "masse": 10
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

           
        self.root.mainloop()

    def afficher(self):
        """
            dessine chaque persone
        """
        self.canvas.pack()
        self.button.destroy()

        arene.afficher(self.canvas)

        for indice,personne in enumerate(tab_personne):
            
            
            dessiner_cercle(self.canvas, personne["x"], personne["y"], 10, "blue")

    
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

            tab_personne[indice]["x"] += 1
            tab_personne[indice]["y"] += 1

            x = personne["x"]
            y = personne["y"]

        


        self.afficher()
        self.root.after(30, self.model)
        
        

if __name__ == "__main__":
    app()