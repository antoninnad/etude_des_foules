import numpy as np


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
            "hauteur": 50,
        }

        self.obstacles = [
            {"x": 400, "y": 250, "longueur": 50, "hauteur": 30,"type": "rectangle", "couleur": "purple"},
        ]
    
    def dessiner_obstacles(self, canvas):
        """
        Dessine une liste d'obstacles sur un Canvas Tkinter.

        :param canvas: Le widget Canvas Tkinter
        :param obstacles: Liste de dictionnaires représentant les obstacles
        """
        for obstacle in self.obstacles:
            x, y = obstacle["x"], obstacle["y"]
            couleur = obstacle["couleur"]

            if obstacle["type"] == "rectangle":
                longueur, hauteur = obstacle["longueur"], obstacle["hauteur"]
                canvas.create_rectangle(x, y, x + longueur, y + hauteur, fill=couleur)


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

        self.dessiner_obstacles(canvas)
