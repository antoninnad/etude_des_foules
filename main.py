import tkinter as tk
from tkinter import messagebox

import random
import numpy as np
import math
import time


from physique import *
from affichage import *


# partie principale
global tab_personne
tab_personne = []



def initialiser_tab_personne():

	tab = []

	for y in range(3):
		for x in range(15):

			tab.append({
				"id": y*15+x,
				"position": np.array([100 + 30 * y, 100 + 30 * x]),
				"destination": np.array([100 + 30 * y, 100 + 30 * x]),
				"masse": 10,
				"vitesse_desiree": 1.34 + random.randint(-1, 1) * random.randint(0, 25) * .01, 
				"vitesse": np.array([0, 0]),
				"to": .2,
				"rayon": 10 +  random.randint(-2, 2)
				
			})


	return tab

def initialiser_tab_personne_pour_une_class():

	tab = []

	tab.append({
				"id": 0,
				"position": np.array([150, 90]),
				"destination": np.array([150, 90]),
				"masse": 10,
				"vitesse_desiree": 2 + random.randint(-1, 1) * random.randint(0, 25) * .01, 
				"vitesse": np.array([0, 0]),
				"to": .2,
				"rayon": 12
	})

	for y in range(5):
		for x in range(6):
			x_colunm_seperator = 60 if (x>2) else 0
			tab.append({
				"id": y*6+x+1,
				"position": np.array([120 + (70 * x) + x_colunm_seperator, 260 + (71* y)]),
				"destination": np.array([120 + (70 * x) + x_colunm_seperator, 260 + (71* y)]),
				"masse": 10,
				"vitesse_desiree": 2 + random.randint(0, 25) * .1, 
				"vitesse": np.array([0, 0]),
				"to": .2,
				"rayon": 10	+  random.randint(-2, 2)
			})
	return tab


class app:

	def __init__(self):

		# initialisation de window tkinter
		self.root = tk.Tk()
		self.root.title("Experience")
		self.root.geometry("1400x700")
		self.root.configure(bg='#e8e8e8')
		self.canvas = tk.Canvas(self.root, width=600 * 2, height=700, bg="white")

	# Interface de lancement

		# Texte "Simulation à lancer"
		self.explication_sim = tk.Label(self.root, text="Simulation à lancer :", font=("Arial", 14), bg='#e8e8e8')
		self.explication_sim.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

		#Bouttons de lancement de simulation
		self.button = tk.Button(self.root, text="Commencer simulation basique", width=27, command=self.start_basique, bg='#e8e8e8')
		self.button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

		self.button2 = tk.Button(self.root, text="Commencer simulation obsatcles", width=27, command=self.start_obstacles, bg='#e8e8e8')
		self.button2.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

		self.button3 = tk.Button(self.root, text="Commencer simulation cour", width=27, command=self.start_class, bg='#e8e8e8')
		self.button3.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

		# Texte "Mode de résolution des équations de vitesses"
		self.explication_mode = tk.Label(self.root, text="Mode de résolution des équations de vitesses :", font=("Arial", 14), bg='#e8e8e8')
		self.explication_mode.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

		# Variable qui contient le choix du mode de résolution
		self.mode_resolution = tk.StringVar()
		self.mode_resolution.set("euler")

		# Choix des modes
		self.radio1 = tk.Radiobutton(self.root, text="Euler", variable=self.mode_resolution, value="euler", bg='#e8e8e8')
		self.radio1.place(relx=0.3, rely=0.75, anchor=tk.CENTER)
		self.radio2 = tk.Radiobutton(self.root, text="Runge-Kutta 2", variable=self.mode_resolution, value="rk2", bg='#e8e8e8')
		self.radio2.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
		self.radio3 = tk.Radiobutton(self.root, text="Runge-Kutta 4", variable=self.mode_resolution, value="rk4", bg='#e8e8e8')
		self.radio3.place(relx=0.7, rely=0.75, anchor=tk.CENTER)

		# Informations sur l'etat actuel de la simulation
		self.particule = tk.Label(self.root, text=f"Personnes ", bg="white", fg="black", font=("Arial", 14))
		self.temps = tk.Label(self.root, text="Temps 0.0 s", bg="white", fg="black", font=("Arial", 14))

		
		# Bouton/slider de configuration de la simulation
		self.restart = tk.Button(self.root, text="Restart", command=self.restart_action)
		self.stopBtn = tk.Button(self.root, text="Stop", command=self.stop_action)
		self.slider = tk.Scale(self.root, from_=0, to=100, orient="horizontal", length=200, command=self.augmenter_vitesse)
		self.menuBtn = tk.Button(self.root, text=">> Menu <<", command=self.restart_app)

		# Initialisation de valeurs
		self.vitesse = 1
		self.stop = False
		self.nombre = 1
		self.slider.set(53)
		self.porte = []

		# mainloop
		self.root.mainloop()

	def start(self):
		"""
			Initialisation basique de comencement
		"""
		self.explication_sim.destroy()
		self.button.destroy()
		self.button2.destroy()
		self.button3.destroy()
		
		self.explication_mode.destroy()		
		self.radio1.destroy()
		self.radio2.destroy()
		self.radio3.destroy()

		global fichier_coords,followed
		fileName = 'coords_' + self.type + '_' + time.asctime(time.localtime(time.time())) + '.txt'
		fichier_coords = open('coordonnee/'+fileName, 'w')
		fichier_coords.write('x1;y1;x2;y2;x3;y3;x4;y4;x5;y5;x6;y6\n')
		self.nombre = len(tab_personne)

		followed = random.choices(list(range(self.nombre)),k=6)
		print(followed)

		self.temps.pack(side="left", padx=10, pady=5)
		self.particule.pack(side="left", padx=10, pady=25)
		self.stopBtn.place(x= 10,y= 10)
		self.restart.place(x= 10,y=50)
		self.slider.place(x=10,y=80)

		self.trouvePorte()
		self.arene = configuration()
		self.arene.placeporte(self.portes)
		
		self.debut = 0


	def start_basique(self):
		"""
			start la simulation dans une salle vide
		"""
		self.type = 'basique'

		global tab_personne
		tab_personne = initialiser_tab_personne()
		self.portes = [[600, 300, 50]]
		self.nombre=45
		self.start()
		self.model()

	def start_class(self):
		"""
			start la simulation dans une salle de classe
		"""
		self.type = 'class'

		global tab_personne
		tab_personne = initialiser_tab_personne_pour_une_class()

		self.portes = [[600, 100, 40], [600, 500, 60]]
		self.nombre=31
		self.start()
		self.arene.ajout_class()
		self.model()

	def start_obstacles(self):
		"""
			start la simulation dans une salle avec un obstacle
		"""
		self.type = 'obstacle'

		global tab_personne
		tab_personne = initialiser_tab_personne()

		self.portes = [[600, 300, 50]]
		self.nombre=45
		self.start()
		self.arene.ajout_obstacles()
		self.model()

	def trouvePorte(self):
		for personne in tab_personne:
			closest = self.portes[0]
			closestDist = np.sqrt( (personne["position"][0] + closest[0])**2 + (personne["position"][1] + closest[1])**2 )
			for porte in self.portes:
				distancePorte = np.sqrt( (personne["position"][0] + porte[0])**2 + (personne["position"][1] + porte[1])**2 )
				if closestDist < distancePorte:
					closest = porte
					closestDist = distancePorte 
			personne["destination"] = np.array([closest[0] + 35, closest[1] + 35])


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
		global tab_personne, fichier_coords

		fileName = 'coords_' + self.type + '_' + time.asctime(time.localtime(time.time())) + '.txt'
		fichier_coords.close()
		fichier_coords = open('coordonnee/'+fileName, 'w')
		fichier_coords.write('x1;y1;x2;y2;x3;y3;x4;y4;x5;y5;x6;y6\n')
		
		wasEmpty = (len(tab_personne) == 0)
		tab_personne_len_type = self.nombre
		tab_personne.clear()
		if (not self.type == 'class'):
			tab_personne = initialiser_tab_personne()
		else:
			tab_personne = initialiser_tab_personne_pour_une_class()

		self.debut = 0
		self.trouvePorte()
		if (wasEmpty):
			self.model()
		self.stop = False

	def stop_action(self):
		self.stop = not self.stop

	def restart_app(self):
		self.root.destroy()
		self.__init__()

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
		

	def update(self, personne):
		personne.deplacer(1,1)
		x = personne.coordonnees[0]
		y = personne.coordonnees[1]

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

				if self.mode_resolution.get() == "euler":
					euler(tab_personne, personne, indice, self.arene.obstacles, self.portes)

				elif self.mode_resolution.get() == "rk2":
					runge_kutta_2(tab_personne, personne, indice, self.arene.obstacles, self.portes)
					
				else:	# mode_resolution.get() == "rk4":
					runge_kutta_4(tab_personne, personne, indice, self.arene.obstacles, self.portes)

				if personne["position"][0] > 610:
					tab_personne.pop(indice)

		#personnes_id = [i['id'] for i in tab_personne]


		for i in followed:
			boolean = 0
			
			for p in tab_personne:
				if p['id']==i:

					boolean=1
					fichier_coords.write(f"{p['position'][0]};{550-p['position'][1]};")
					
			if not boolean:
				
				fichier_coords.write(f"nan;nan;")

		fichier_coords.write("\n")

		self.particule["text"] = f"Personnes {len(tab_personne)}/{self.nombre}"

		if len(tab_personne) != 0 and self.debut<150:
	
			self.afficher()
			self.temps["text"] = f"Temps {self.debut:.2f} s"

			self.debut += 0.03
			self.root.after( int(30 / self.vitesse), self.model)
		
		else:
			self.temps["text"] = f"Temps {self.debut:.2f} s"
			messagebox.showinfo("Resultat", f"Fait en {self.debut:.2f} secondes")

			fileName = fichier_coords.name
			fichier_coords.close()
			plot_graphs(fileName)

			return
		
		

if __name__ == "__main__":
	app()
	# ~ plot_graphs()
