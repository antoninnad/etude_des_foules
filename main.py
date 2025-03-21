import tkinter as tk
import random

from affichage import *


# partie principale

tab_personne = []

arene = configuration()

for x in range(10):
    tab_personne.append(Personne( [80, x * 30 + 80]))



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

        for personne in tab_personne:
            personne.afficher(self.canvas)

    
    def start(self):
        """
            démarre le jeu
        """

        self.model()

    def model(self):

        """
            modélise le mouvement des personnes
        """
        for personne in tab_personne:
            personne.deplacer(1,1)

            x = personne.coordonnees[0]
            y = personne.coordonnees[1]

            if x < 70 or x > 580:
                personne.coordonnees[0] = random.randint(70,580)
            if y < 70 or y > 580:
                personne.coordonnees[1] = random.randint(70,580)


        self.afficher()
        self.root.after(15, self.model)
        
        

if __name__ == "__main__":
    app()