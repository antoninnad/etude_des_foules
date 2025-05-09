import numpy as np
import math

import csv
import matplotlib.pyplot as plt


config = {
	"b0": 5
}

"""Normalise un vecteur"""
def normalize_vector(vector):
	"""Normalise un vecteur"""
	norm = np.linalg.norm(vector)  # Calcul de la norme euclidienne
	
	if norm == 0:
		raise ValueError("Impossible de normaliser un vecteur nul.")
	
	return vector / norm  # Division de chaque élément par la norme

"""Retourne un vecteur orthogonal"""
def orthogonal_vector(vector):
	return np.array([-vector[1], vector[0]])



"""
	Calcule le vecteur de direction normalisé d'une personne à un point souhaité (porte).

	Cette fonction calcule le vecteur unitaire pointant à partir de la position actuelle de la personne
	à un point fixe souhaité, qui représente l'emplacement de la porte.

	Paramètres :
	personne (dict) : dico de personne

	Retours :
	numpy.ndarray : Un vecteur 2D normalisé (ei0) représentant la direction
				   de la position de la personne jusqu'au point souhaité (porte).
				   Le vecteur a une norme de 1.

	AssertionError : Si le vecteur résultant n'est pas un vecteur unitaire (magnitude ≠ 1).
"""
def calcul_ei0(personne):
	
	#position desiree
	pt_souhaite = personne["destination"]
	#direction 
	vecteur_ei0 =  pt_souhaite - personne["position"]
	vecteur_ei0 = [0, 1] if all(vecteur_ei0 == [0, 0]) else vecteur_ei0
	# normalisation du vecteur
	norm = np.linalg.norm(vecteur_ei0)
	vecteur_ei0 = vecteur_ei0 / norm

	assert( math.isclose(np.linalg.norm(vecteur_ei0), 1) )

	return vecteur_ei0


"""
	Calcule la force motrice d'une personne.

	Cette fonction calcule la force motrice agissant sur une personne en fonction de la vitesse souhaitée,
	vitesse du courant et un temps de relaxation.

	Paramètres :
	personne (dict) : Un dictionnaire contenant des informations sur la personne, notamment :
		- 'vitesse_desiree' (float ou numpy.ndarray) : La vitesse souhaitée de la personne.
		- 'vitesse' (numpy.ndarray) : La vitesse actuelle de la personne.
		- 'to' (float) : Le temps de relaxation, représentant la rapidité avec laquelle la personne s'adapte à la vitesse souhaitée.

	Retours :
	numpy.ndarray : Le vecteur de force motrice résultant agissant sur la personne.
"""   

def force_motrice(personne):
	
	resultat = personne["vitesse_desiree"] * calcul_ei0(personne) - personne["vitesse"]

	resultat = resultat /  personne["to"]

	return resultat


"""
	Calcule la force d'interaction sociale entre une personne et les autres personnes dans la foule.

	Cette fonction calcule la force d'interaction sociale ressentie par une personne
	en raison de la présence d’autres individus dans un seuil d’interaction spécifié.

	Paramètres :
		tab_personne (list) : Une liste de dictionnaires, chacun représentant une personne dans la foule.
		personne (dict) : Le dictionnaire représentant la personne pour laquelle la force est calculée.
		indice (int) : L'index de 'personne' dans la liste 'tab_personne'.
		b0 (float) : paramètre contrôlant la force de la force d’interaction. La valeur par défaut est config["b0"].
		seuil_interaction (float) : La distance maximale pour considérer les interactions sociales. La valeur par défaut est 50.

	Retours :
	numpy.ndarray : le vecteur de force d'interaction sociale résultant agissant sur la personne.
"""
def force_intercation_social(tab_personne, personne, indice, b0=config["b0"], seuil_interaction=50):
	

	resultat = 0

	for indice_personne, personne_autre in enumerate(tab_personne):
		if indice_personne != indice and np.linalg.norm(personne_autre["position"] - personne["position"]) < seuil_interaction:

			a = personne["position"]
			b = personne_autre["position"]

			norme_ab = np.linalg.norm(a - b) - personne_autre["rayon"] - personne["rayon"]

			# if np.exp((- norme_ab / .08)) * (a - b)[0] > 1_000:
			#	 print(f"norm {norme_ab}")
			#	 print(f"\n vect {(a - b)}")

			resultat = resultat + np.exp((- norme_ab / b0)) * (a - b)

	return resultat

""" angle entre deux vecteurs """
def angle_entre_vecteur(u, v):
	dot_product = np.dot(u, v)
	norm_u = np.linalg.norm(u)
	norm_v = np.linalg.norm(v)
	cos_theta = dot_product / (norm_u * norm_v)

	return np.arccos(np.clip(cos_theta, -1.0, 1.0)) 


"""
	Calcule la distance entre une personne et un segment de mur et renvoyez le vecteur normal au mur.

	Cette fonction calcule la distance perpendiculaire d'une personne à un segment de mur
	défini par deux points, et calcule également le vecteur normal à ce segment de mur.

	Paramètres :
	coord_a (numpy.ndarray) : Les coordonnées du premier point du segment de mur.
	coord_b (numpy.ndarray) : Les coordonnées du deuxième point du segment de mur.
	personne (dict) : Un dictionnaire contenant des informations sur la personne, notamment :
		- 'position' (numpy.ndarray) : La position actuelle de la personne.
		- 'rayon' (flotteur) : Le rayon de la personne (considéré comme un cercle).

	Retours :
	tuple : Un tuple contenant deux éléments :
		- resultat (float) : La distance perpendiculaire de la personne au segment de mur,
		  ajusté en soustrayant le rayon de la personne.
		- vecteur_normal (numpy.ndarray) : Le vecteur normal au segment de mur.
		- AE (float) : Distance sur l'axe AB pour l'évitement

"""

def distance_mur_vect(coord_a, coord_b, personne):
	
	coord_personne = personne["position"]

	AP = coord_personne - coord_a
	AB = coord_b - coord_a

	alpha = angle_entre_vecteur(AP, AB)


	PE = (np.linalg.norm(AP) * np.sin(alpha) - personne["rayon"]) 


	vecteur_normal = orthogonal_vector(AB)

	resultat = PE


	AE = math.sqrt(np.linalg.norm(AP) ** 2 -  np.linalg.norm(PE) ** 2)

	return resultat, vecteur_normal, AE

def _distance_mur_vect(mur_pos1 : np.array, mur_pos2 : np.array, personne : dict):
	coord_personne = personne["position"]
	
	mur_len = mur_pos2 - mur_pos1
	
	vec_pers_mur = coord_personne - mur_pos1
	
	mur_longueur = np.linalg.norm(mur_len)
	if (mur_longueur == 0):
		return (mur_pos1)
	
	mur_len_normaliser = mur_len / mur_longueur
	
	k = np.dot(vec_pers_mur, mur_len_normaliser)
	print(k)
	
	if (k <= 0):
		return (mur_pos1)
	if (k >= np.linalg.norm(mur_len)):
		return mur_pos1 + mur_len

	return mur_pos1 + k * mur_len_normaliser
	
	
   
def normalize(v):
	norm = np.linalg.norm(v)
	if norm == 0: 
	   return v
	return v / norm


def force_intercation_social_mur(personne, indice, portes, b0 = config["b0"]):

    coord_a = np.array([50, 50])
    coord_b = np.array([600,50])
    coord_c = np.array([600,600])
    coord_d = np.array([50, 600])
    
    resultat = 0
    
    inAdoor = False
    for porte in portes:
        if (personne["position"][1] > porte[1] and personne["position"][1] < (porte[1] + 40)) and personne["position"][0] < porte[0] + 20:
           inAdoor = True 
    
    mur_bc = distance_mur_vect(coord_b, coord_c, personne)
    
    resultat += (np.exp(- mur_bc[0] / b0) * mur_bc[1]) if not inAdoor else resultat
    
    mur_ab = distance_mur_vect(coord_a, coord_b, personne)
	
    resultat += np.exp(- mur_ab[0] / b0) * mur_ab[1]
    
    mur_ad = distance_mur_vect(coord_a, coord_d, personne)
    
    resultat += np.exp(- mur_ad[0] / b0) * mur_ad[1] * -1
    
    mur_dc = distance_mur_vect(coord_d, coord_c, personne)
    
    resultat += np.exp(- mur_dc[0] / b0) * mur_dc[1] * -1
    
    return resultat


def point_le_plus_proche_rectangle(personne : dict, rectangle : dict) -> np.array:
	# vecteur mur (un sommet) -> personne
	pers_mur = personne["position"] - np.array([rectangle["x"], rectangle["y"]])
	
	# le vecteur pour désigner la longeur du mur 
	# pourra dans le future, ne pas être aligner aux axes x y
	vecteur_mur1 = np.array([rectangle["longueur"], 0.])
	
	# le vecteur pour désigner la largeur du mur 
	vecteur_mur2 = np.array([0., rectangle["hauteur"]])
	
	# vérifie si personne n'est pas dans le mur
	est_pas_dans_mur = False
	
	
	k1 = np.dot(pers_mur, normalize(vecteur_mur1))
	if (k1 < 0.):
		k1 = 0.
		est_pas_dans_mur = True
	
	vecteur_mur1_longeur = np.linalg.norm(vecteur_mur1)
	if (k1 > vecteur_mur1_longeur):
		k1 = vecteur_mur1_longeur
		est_pas_dans_mur = True
	
	k2 = np.dot(pers_mur, normalize(vecteur_mur2))
	if (k2 < 0.):
		k2 = 0.
		est_pas_dans_mur = True
	
	vecteur_mur2_longeur = np.linalg.norm(vecteur_mur2)
	if (k2 > vecteur_mur2_longeur):
		k2 = vecteur_mur2_longeur
		est_pas_dans_mur = True
		
	return (
		np.array([rectangle["x"], rectangle["y"]])
	  + k1 * (vecteur_mur1)/ vecteur_mur1_longeur
	  + k2 * (vecteur_mur2)/ vecteur_mur2_longeur
	)
		
# donne le vecteur de répulsion d'un rectangle sur une personne
# facilement modifible pour prendre n'importe quel forme de rectangle (rotation)
def force_intercation_rectangle(personne, rectangle, b0=config["b0"]):
	point = point_le_plus_proche_rectangle(personne, rectangle)
	
	
	distance_mur = np.linalg.norm(point - personne["position"]) - personne["rayon"]

	return 15. * np.exp(- distance_mur / b0) * normalize(personne["position"] - point)

# antienne méthode de calcule
def _force_intercation_rectangle(personne, rectangle, b0=config["b0"]):

	x = rectangle["x"]
	y = rectangle["y"]
	h = rectangle["hauteur"]
	l = rectangle["longueur"]

	rayon   = personne["rayon"] 
	coord_x = personne["position"][0] + rayon
	coord_y = personne["position"][1] + rayon


	coord_a = np.array([x, y])
	coord_b = np.array([x + l,y])
	coord_c = np.array([x + l,y + h])
	coord_d = np.array([x , y + h])
	resultat = 0
	

	if coord_y > y and coord_y < y + h + 2 * rayon and coord_x < x:
		
		mur_ad = distance_mur_vect(coord_a, coord_d, personne)
		resultat += np.exp(- mur_ad[0] / b0) * mur_ad[1]

		# ajout force contournement
		if mur_ad[0] < 20:
			ad = coord_a - coord_d

			signe = 1

			
			#pour de faire aller la force vers le haut ou vers le vas
			if mur_ad[2] > h/2:
				signe = -1

			ad = normalize_vector(ad) * 10 * signe

			resultat += ad

	if coord_x - 2 * rayon > x and coord_x - 2 * rayon < x + l and coord_y > y:

		mur_ab = distance_mur_vect(coord_a, coord_b, personne)
		
		resultat += np.exp(- mur_ab[0] / b0) * mur_ab[1] * -1

	if coord_x - 2 * rayon > x and coord_x < x + l and coord_y > y:

		mur_dc = distance_mur_vect(coord_d, coord_c, personne)

		resultat += np.exp(- mur_dc[0] / b0) * mur_dc[1] 

	

	return resultat


def force_interaction_cercle(personne, cercle, b0=config["b0"]):
	
	resultat = np.array([0, 0])
	
	o = np.array([cercle["x"], cercle["y"]])
	i = personne["position"]
	
	distance = np.linalg.norm(o - i) - cercle["rayon"] - personne["rayon"]
	
	resultat = resultat + np.exp((- distance / b0)) * 1.3*(i - o)
		
	return resultat


def force_interaction_cercle(personne, cercle, b0=config["b0"]):
	
	resultat = np.array([0, 0])
	
	o = np.array([cercle["x"], cercle["y"]])
	i = personne["position"]
	
	distance = np.linalg.norm(o - i) - cercle["rayon"] - personne["rayon"]
	
	resultat = resultat + np.exp((- distance / b0)) * 1.3*(i - o)
		
	return resultat

def force_interaction_obstacle(personne, obstacles):
	accumulateur = 0
	for obstacle in obstacles:
		if obstacle["type"] == "rectangle":

			accumulateur += force_intercation_rectangle(personne, obstacle)
			
		elif obstacle["type"] == "cercle":

			accumulateur += force_interaction_cercle(personne, obstacle)


	return accumulateur


"""
resoud l'equation et actualise la position

"""
def euler(tab_personne, personne,indice,obstacles, portes, step=.02):
	"""
	pb physique 
	"""
	#cacul de la force motrice
	f_m = force_motrice(personne)

	#force des murs de la simulation
	f_m += force_intercation_social_mur(personne , indice, portes)

	#force interaction personnes
	f_m += force_intercation_social(tab_personne, personne, indice)

	#forces obstacles
	f_m += force_interaction_obstacle(personne, obstacles)

	#projection sur Ux et Uy
	vitesse_x =  personne["vitesse"][0] + step * f_m[0]
	vitesse_y = personne["vitesse"][1] + step * f_m[1]

	
	#on actualise la position
	personne["position"] = np.array( [
		personne["position"][0] + vitesse_x,
		personne["position"][1] + vitesse_y 
	])

	# v(t_n+&)
	personne["vitesse"] = np.array([
		vitesse_x,
		vitesse_y
	])



def plot_graphs():

	f = open('fichier_coords.txt', 'r')
	coords = csv.DictReader(f, delimiter=';')
	
	x1, x2, x3 = [], [], []
	y1, y2, y3 = [], [], []

	for row in coords:
		
		x1.append(float(row['x1'])*0.01)
		x2.append(float(row['x2'])*0.01)
		x3.append(float(row['x3'])*0.01)
		y1.append(float(row['y1'])*0.01)
		y2.append(float(row['y2'])*0.01)
		y3.append(float(row['y3'])*0.01)

	x1, x2, x3 = np.array(x1), np.array(x2), np.array(x3)
	y1, y2, y3 = np.array(y1), np.array(y2), np.array(y3)

	plt.title("Trajectoire d'individus selon le modèle de Helbing")
	plt.xlabel('x (m)')
	plt.ylabel('y (m)')
	plt.plot(x1, y1, color='r')
	plt.plot(x2, y2, color='b')
	plt.plot(x3, y3, color='g')

	plt.xlim(0, 6)
	plt.ylim(0, 6)
	
	plt.show()
