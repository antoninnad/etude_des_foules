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

        self.obstacles = []
    
    def placeporte(self, portes):
        for porte in portes:
            self.sortie = {
                "x": porte[0] - 34,
                "y": porte[1] - 35,
                "hauteur": 50,
            }

    def ajout_obstacles(self):
        self.obstacles = [
            {"x": 400, "y": 250, "longueur": 50, "hauteur": 90,"type": "rectangle", "couleur": "purple"},
        ]

    def ajout_class(self):
        self.obstacles = [
            {"x": 100, "y": 110, "longueur": 100, "hauteur": 35,"type": "rectangle", "couleur": "purple"},
            {"x": 180, "y": 60, "longueur": 300, "hauteur": 10,"type": "rectangle", "couleur": "black"},

            {"x": 90 , "y": 220, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 160, "y": 220, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 230, "y": 220, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 360, "y": 220, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 430, "y": 220, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 500, "y": 220, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},

            {"x": 90 , "y": 290, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 160, "y": 290, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 230, "y": 290, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 360, "y": 290, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 430, "y": 290, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 500, "y": 290, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},

            {"x": 90 , "y": 360, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 160, "y": 360, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 230, "y": 360, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 360, "y": 360, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 430, "y": 360, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 500, "y": 360, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},

            {"x": 90 , "y": 430, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 160, "y": 430, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 230, "y": 430, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 360, "y": 430, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 430, "y": 430, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 500, "y": 430, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},

            {"x": 90 , "y": 500, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 160, "y": 500, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 230, "y": 500, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 360, "y": 500, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 430, "y": 500, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            {"x": 500, "y": 500, "longueur": 60, "hauteur": 25,"type": "rectangle", "couleur": "brown"},
            
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
