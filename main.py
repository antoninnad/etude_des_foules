import tkinter as tk
import random

def dessiner_cercle(canvas, x, y, rayon, couleur):
    """Dessine un cercle sur le canevas."""
    canvas.create_oval(x - rayon, y - rayon, x + rayon, y + rayon, outline=couleur, width=2,fill=couleur)


class configuration:

    def __init__(self):

        self.sortie = {
            "x": 600,
            "y": 300,
            "hauteur": 40
        }

class Personne:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rayon = 10

    def afficher(self , canvas):

        dessiner_cercle(canvas, self.y, self.x, self.rayon, "blue")

tab_personne = []

arene = configuration()

for x in range(10):
    tab_personne.append(Personne(random.randint(0,600), random.randint(0,600)))

class app:

    def __init__(self):


        self.root = tk.Tk()
        self.root.title("Experience")

      
        self.root.geometry("1400x700")

        self.canvas = tk.Canvas(self.root, width=600 * 2, height=600, bg="white")

        self.button = tk.Button(self.root, text="Commencer", command=self.start)

        self.button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

           
        self.root.mainloop()


    def start(self):
        self.canvas.pack()
        self.button.destroy()

        for personne in tab_personne:
            personne.afficher(self.canvas)

        

if __name__ == "__main__":
    app()