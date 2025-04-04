import numpy as np
import math


config = {
    "b0": 3
}


def normalize_vector(vector):
    """Normalise un vecteur en utilisant numpy."""
    norm = np.linalg.norm(vector)  # Calcul de la norme euclidienne
    
    if norm == 0:
        raise ValueError("Impossible de normaliser un vecteur nul.")
    
    return vector / norm  # Division de chaque élément par la norme

def orthogonal_vector(vector):
    """Retourne un vecteur orthogonal"""
    return np.array([-vector[1], vector[0]])



def calcul_ei0(personne):


    #position de la porte
    pt_souhaite = np.array([624, 335])
    vecteur_ei0 =  pt_souhaite - personne["position"]

    norm = np.linalg.norm(vecteur_ei0)

    

    vecteur_ei0 = vecteur_ei0 / norm

    assert( math.isclose(np.linalg.norm(vecteur_ei0), 1) )

    return vecteur_ei0
        

def force_motrice(personne):

    resultat = personne["vitesse_desiree"] * calcul_ei0(personne) - personne["vitesse"]

    resultat = resultat /  personne["to"]

    return resultat

def force_intercation_social(tab_personne, personne, indice, b0 = config["b0"]):

    resultat = 0

    for indice_personne, personne_autre  in enumerate(tab_personne):

        if indice_personne != indice:

            a = personne["position"]
            b = personne_autre["position"]

            norme_ab = np.linalg.norm(a - b) - personne_autre["rayon"] - personne["rayon"]

            if np.exp((- norme_ab / .08)) * (a - b)[0] > 1_000:
                print(f"norm {norme_ab}")
                print(f"\n vect {(a - b)}")

            resultat =  resultat + np.exp((- norme_ab / b0)) * (a - b)

            #print(f"norme: {norme_ab} force {np.exp((- norme_ab / .08)) * (a - b)}")
    return resultat


def angle_between_vectors(u, v):
    dot_product = np.dot(u, v)
    norm_u = np.linalg.norm(u)
    norm_v = np.linalg.norm(v)
    cos_theta = dot_product / (norm_u * norm_v)

    return np.arccos(np.clip(cos_theta, -1.0, 1.0)) 

def distance_mur_vect(coord_a, coord_b,  personne):

    coord_personne = personne["position"]

    AP = coord_personne - coord_a
    AB = coord_b - coord_a

    alpha = angle_between_vectors(AP,AB)

    
    PE = (np.linalg.norm(AP) * np.sin(alpha) - personne["rayon"]) 


    vecteur_normal = orthogonal_vector(AB)

    resultat = PE

    return resultat, vecteur_normal


def force_intercation_social_mur(personne, indice, b0 = config["b0"]):

    coord_a = np.array([50, 50])
    coord_b = np.array([600,50])
    coord_c = np.array([600,600])
    coord_d = np.array([50, 600])
    resultat = 0
    
    
    if not (personne["position"][1] > 310 and personne["position"][1] < 340) and personne["position"][0] < 600 - personne["rayon"]:
        mur_bc = distance_mur_vect(coord_b, coord_c, personne)
    
        resultat += np.exp(- mur_bc[0] / b0) * mur_bc[1]




    mur_ab = distance_mur_vect(coord_a, coord_b, personne)
    
    resultat += np.exp(- mur_ab[0] / b0) * mur_ab[1]

    mur_ad = distance_mur_vect(coord_a, coord_d, personne)

    
    resultat += np.exp(- mur_ad[0] / b0) * mur_ad[1] * -1

    mur_dc = distance_mur_vect(coord_d, coord_c, personne)

    resultat += np.exp(- mur_dc[0] / b0) * mur_dc[1] * -1

    return resultat


def euler(tab_personne, personne,indice, step=.02):

    f_m = force_motrice(personne)

    f_m += force_intercation_social_mur(personne , indice)

    
    
    f_m += force_intercation_social(tab_personne, personne, indice)

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
