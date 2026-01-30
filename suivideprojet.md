# 📝 <span style="color:red">Suidi de Projet</span>

---

## 📅 <span style="color:orange">18/12/2025 et 08/01/2026:</span>
### ✅ Ajouts / Changements:
Pendant ces deux jours, Elvis (Maxime absent) a travaillé sur le début des graphismes et le premier spike qui revient tout le temps pour que le jeu dure plus longtemps.
### 📝 À faire:
Ajouter d'autres mécaniques pour rendre le jeu plus intérésant.

---
<br></br>

## 📅 <span style="color:orange">22/12/2025 - 27/12/2025 (vancance de Noël):</span>
### ✅ Ajouts / Changements:
- Nous avons crée plusieurs fichiers .py pour chaques parties du jeu:
    - app.py: la carte mère du jeu qui rassemble tous les fichiers.py pour faire tourner le jeu
    - level.py: il devrait y avoir normalement niveau_draw() --> ce qui va être dessiner et niveau_update() --> pour gérer le déplacement des obstacles et du cube. Il n'y a que le niveau_draw() pour le moment et le niveau_update() devrait arriver bientot dedans mais il y a des erreurs que je n arrive pas a fix (il se trouve actuellement dans le app.py)
    - menu.py: menu principal du jeu pour choisir le niveau. menu_update() pour update les variables et menu_draw() pour dessier le menu
    - obstacleslvls.py: une fonction par niveau et chaque fonction contient des dictionnaires pour chaque obstacles dans le jeu
### ⚠️ Problèmes Rencontrés:
Problèmes level_update() devait changer les variables mais il fallait juste return les variables
### 📝 À faire:
- Continuer les niveaux
- Ajouter des orbs

---
<br></br>

## 📅 <span style="color:orange">12/01/2026:</span>
### ✅ Ajouts / Changements:
- Continué de faire les niveaux
- Orbs (jaune)
- Modifier la gravité et augmenter un peu la vitesse du joueur
### ⚠️ Problèmes Rencontrés:
- Lorsqu'on sautait sur l'orb, le cube montais vers le haut à l'infini
### 📝 À faire:
Modifier encore un peu la gravité du joueur

---
<br></br>

## 📅 <span style="color:orange">15/01/2026:</span>
### ✅ Ajouts / Changements:
- Terminé de faire le niveau et un peu commencé le niveau 2
- Commencé à faire la fin du niveau (+ dessins) (bientot fini)
### 📝 À faire:
- Régler la musique: nous allons créer un .mp3 et jouer cette musique (ou supprimer la musique nous allons voir). 

---
<br></br>

## 📅 <span style="color:orange">17/01/2026:</span>
### ✅ Ajouts / Changements:
- Maxime a remis level.py dans app.py car cela complique les choses même si c est un peu moins bien organisé mais c est mieux visible (). Fix des bugs sur la fin du niveau + petite optimisation du code. optimisation (variables qui ne servent a rien dans le global + variables répétés)
### 📝 À faire:
- Quand le cube tombe, il peut quand même sauter dans les airs
- A voir si on mets aussi, dans app.py, menu.py (pas obstacleslvls.py)

---
<br></br>

## 📅 <span style="color:orange">19/01/2026:</span>
### ✅ Ajouts / Changements:
- Noclip pour pouvoir aller à la fin du niveau sans mourir
- Pourcentage du niveau où l'utilisateur est
### ⚠️ Problèmes Rencontrés:
noclip = noclip() <--TypeError: 'NoneType' object is not callable --> Il fallait juste change le nom de la fonction car le code bug lorsque qu'une variable a le même nom qu'un fonction

---
<br></br>

## 📅 <span style="color:orange">26/01/2026:</span>
### ✅ Ajouts / Changements:
Fix bug où le joueur pouvait sauter dans le vide lorsqu'il tombé d'un cube/mur
### ⚠️ Problèmes Rencontrés:
J'ai fais en sorte que le programme regarde le y du cube et regarde que si il a diminué, il fallait tomber faire que jump=True mais il faut en fait voir si il a augmenté (y=0 <-- en haut de la fenêtre)

---
<br></br>

## 📅 <span style="color:orange">28/01/2026:</span>
### ✅ Ajouts / Changements:
- Ajouts de la class Game (pour enlever les global + meilleurs organisation + moins d'erreurs)
- Optimisation du code (comme des variables qui ne servent à rien)
- Enlever la musique pyxelstudio et la remplacer par une music.mp3 grâce à la lib vlc
### ⚠️ Problèmes Rencontrés:
- Mise en pause, arrêt, lancer la musique (c'est une nouvelle lib que je n'avais jamais utlisé)
### 📝 À faire:
- Continuer l'optimisation du code
- Faire un dictionnaire pour les variables de bases (en regroupement)
- Mettre les musiques dans un autre dossier

---
<br></br>

## 📅 <span style="color:orange">29/01/2026:</span>
### ✅ Ajouts / Changements:
- Plus de vlc
### 📝 À faire:
- Mettre la music de PyxelStudio

---
<br></br>

## 📅 <span style="color:orange">30/01/2026:</span>
### ✅ Ajouts / Changements:
- Musique de PyxelStudio ajouté, avec aussi le fait que lorsqu'on mets le niveau en pause et qu'on reprend, la musique reprend aussi --> j'ai donc du stocker le moment où en est la musique lorsqu'elle est mise en pause
- Un petit peu d'optimisation + organisation
- Meilleur esthétique à la fin du niveau + boutons (à programmer)
### ⚠️ Problèmes Rencontrés:
- La musique reprennait mais s'arrêter au bout d'un moment
- Proplème de récupération là où en était la musique
- Je voulais récupérer les données du tuple mais j'avais une erreur qui me disait que le tuple = None donc je ne pouvais pas récupérer la position de la musique. C'est juste que si aucune musique ne joue, play_pos(ch) renvoie None
### 📝 À faire:
- Fonction qui reset toutes les variables qu'il faut après chaque reset et chaque quit de niveau (pour éviter le désordre des variables)
- Finir les boutons lors de la fin du niveau