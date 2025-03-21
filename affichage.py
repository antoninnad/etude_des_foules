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

        self.obstacle = [
            {"x": 100, "y": 100, "taille": 30,"type": "rectangle"},
            {"x": 500, "y": 500, "rayon": 40, "type": "cercle"},
            {"x": 300, "y": 300, "rayon": 20, "type": "cercle"},
            {"x": 200, "y": 600, "rayon": 10, "type": "cercle"},
            {"x": 400, "y": 200, "rayon": 50, "type": "cercle"}
        ]
        

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