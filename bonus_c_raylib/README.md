Une version écrit en C uniquement utilisant raylib comme librairie graphique (https://www.raylib.com/)

// build :
make so_release
// launch :
make so_release_exe

ou utilisé la version déjà complié :
./so_release.out

l'interface se découpe en 4 partie :
 
 I-  en haut les sliders pour changer les variables (listé de gauche à droite) :
     1. time : le nombre de tick de temps se déroulant par frame (avec 60 fps) affiché en puissance de dix
     2. particule : le nombre de particule, modifiable seulement au début de la simulation, de 4 à 800
     3. door : la largeur de la porte
     4. tau : le tau utilisé dans la simulation physique de chaque particule, affiché en puissance de dix (il représente la vitesse les particules approche la vitesse désiré)
     5. fild : la norme du champ vectoriel dictant la vitesse désiré de chaque particule
     6. radius : le rayons approximatif (+ ou - 5%) de chaque particule, modifiable seulement au début de la simulation 
     7. obstacle : la position de l'obstacle sur l'axe X seulement
     8. wish : la distance désiré de chaque particule dans la simulation physique, affiché en puissance de dix (Bi dans le cour)
II-  à gauche les boutons (listé de gauche à droite) : 
     1. le boutons play/pause
     2. le boutons stop : remet la simulation dans l'état initial
     3. le boutons cible : change le champ vectoriel dictant la vitesse désiré pour que les particules se dirige vers la sortie
     4. le boutons rotation 1 : change le champ vectoriel dictant la vitesse désiré pour que les particules tourne en rond autour du centre 
     5. le boutons souris : change le champ vectoriel dictant la vitesse désiré pour que les particules se dirige vers le curseur
     6. le boutons tête de mort : met en mode débug. Cela affiche la direction champ vectoriel pour chaque particule en plus leur vitesse (un trait rouge sur la direction) et la grille de hashage si en mode hash map
     7. le boutons rotation 2 : change le champ vectoriels dictant la vitesse désiré pour que les particules tourne en rond autour et vers le centre
     8. le boutons grille : passe change en mode hash map et normal, le mode hash map et une optimisation permettant de ne prendre en compte que les particules réellement proche les unes des autres. Ce mode est expérimental et ne prend pas en compte la taille de particules, il permet cependant de très bonnes performances si nous avons un grand nombre de particules.
     9. le boutons triangle/cercle : change l'obstacle en cercle ou un triangle
III- la zone du milieu :
    c'est la simulation en elle-même composé de :
     - cinq ligne entourant les particules en rouge
     - un obstacle qui peut-être un cercle ou triangle au choix (II-9.)
     - les particules apparaisse aligné avec de petits décalages aléatoires 
     - une "porte" dont la largeur peut-être modifier (I-3.)
IV - en bas des informations sur les performances 
     - le temps pour afficher l'ui en milliseconde
     - le temps pour simuler en milliseconde
     - le nombre de frame afficher par seconde (fps)
