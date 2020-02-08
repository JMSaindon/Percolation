<img align="left" height="150" src=img/logotrans.png>

Le contenu de ce dépôt correspond à un rendu de TP dans le cadre de l'option IA enseignée à l'Enseirb-Matmeca. Cela vaut pour le module d'Intelligence distribuée / SMA. Le TP choisi porte sur les automates cellulaires et présente la Percolation sur feu de forêts (et en bonus le Jeu de la vie).   

Auteur : Jean-Marie Saindon      
Encadrant : Laurent Simon   

---

# Percolation

## Quickstart
- modules nécessaires: pygame, numpy et matplotlib
- dé-commenter la ligne correspondant à ce que vous voulez obtenir en bas du fichier `Percolation.py`: plot de graphique ou fenêtre pygame
- Réglez la densité de la forêt avec la variable density également en bas du fichier `Percolation.py`
- commande : `$ python Percolation.py`

## Description
L'objectif est ici de modéliser simplement la propagation d'un feu de forêt.
Le TP est implémenté en Python avec pygame sur la base du code pygame fourni pour d'autres TP.
La forêt est modélisée par une Classe Grid utilisant une matrice.
Les arbres sont représentés par des 1, les terrains vides par des 0 et le feu par des -1.

La première approche pour propager l'incendie a été de procéder étape par étape en calculant entièrement, à chacune de celles-ci, la matrice de l'état suivant.

Dans un second temps, pour accélérer le calcul, une méthode récursive de propagation a été envisagée. Cela permettait de parcourir la matrice une fois seulement, mais pour les propagation assez importantes, cela entraînait un dépassement de la limite de récursion.
Enfin, le problème a été corrigé grâce à une méthode itérative utilisant une pile.

En bas du fichier, plusieurs lignes sont à dé-commenter pour lancer, soit les graphiques, soit la fenêtre pygame:

<p align="center">
  <img src=img/PercoCode.PNG>
</p>

L'affichage de la fenêtre pygame donne le rendu ci-dessous:

<p align="center">
  <img width="650" src=img/Perco.PNG>
</p>

L'incendie est lancé sur une grille de taille (153, 83) pour tous les tests. On observe le seuil de percolation aux alentours d'une densité de 0.6 pour des forêts générées aléatoirement de manière uniforme. 

<p align="center">
  <img src=img/graph_50_100_2.png>
</p>



# Bonus : Game of life

## Quickstart

- modules nécessaires: pygame, numpy
- Réglez la densité de vie initiale avec la variable LifeDensity en bas du fichier `GameOfLife.py`
- commande : `$ python GameOfLife.py`

## Description
Le jeu de la vie est également implémenté en Python avec pygame et suis le même principe que la première approche étape par étape de la partie précédente.


<p align="center">
  <img src=img/GameOfLifeCode.PNG>
</p>

<p align="center">
  <img width="650" src=img/GameOfLife.PNG>
</p>


