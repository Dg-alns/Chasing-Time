# Chasing-Time

Python interpreter dans Pycharm ( Ctrl + Alt + s ):
- pygame-ce
- pyscroll
- PyTMX

Le fichier UncapFPS contient le même jeu sans les FPS cap à 60
Le jeu aura une grande vitesse car on ne gère pas les déplacements avec dt

Le saut est linéaire et nous n'avons pas pu lui mettre une vrai gravité :
ConstanteDeGravité * X² + Vitesse * X

ConstanteDeGravité = -9.81 ==> (en positif car y est inversé)
Vitesse = Vitesse de déplacement du joueur
