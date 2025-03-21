import tkinter as tk
import random

def dessiner_cercle(canvas, x, y, rayon, couleur):
    """Dessine un cercle sur le canevas."""
    canvas.create_oval(x - rayon, y - rayon, x + rayon, y + rayon, outline=couleur, width=2,fill=couleur)


class configuration:

    def __init__(self):

        
        # position de des contours
        self.x0, self.y0 = (50,50)
        self.x1, self.y1 = (600,600)

        #taille contours
        self.outlineTaille = 20
        
        #porte
        self.sortie = {
            "x": self.x1 - self.outlineTaille / 2,
            "y": self.y1 /2,
            "hauteur": 30,
        }

        

    def afficher(self, canvas):
        """
            affiche le cadre

            parametre: 
                le canevas sur lequel afficher le cadre
        """
        
        canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, outline="maroon", width=self.outlineTaille, fill="white")
        
        #sortie
        canvas.create_rectangle(
            self.sortie["x"], 
            self.sortie["y"], 
            self.sortie["x"] +  self.outlineTaille,
            self.sortie["y"] + self.sortie["hauteur"], 
            width=0, 
            fill="white"
        )


        return

class Personne:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rayon = 10

    def afficher(self , canvas):
        """
            affiche une personne

            parametre: 
                le canevas sur lequel afficher la personne
        """

        dessiner_cercle(canvas, self.y, self.x, self.rayon, "blue")


# partie principale

tab_personne = []

arene = configuration()

for x in range(10):
    tab_personne.append(Personne(random.randint(70,580), random.randint(70,580)))

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
        
        self.afficher()

        
        

if __name__ == "__main__":
    app()