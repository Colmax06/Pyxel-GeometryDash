import pyxel
from obstacleslvls import *
from menu import *

x = 300
y = 200
pyxel.init(x, y, quit_key=pyxel.KEY_P)
pyxel.load("geometrydash.pyxres")
pyxel.mouse(True)

#cube
cube_x = 40
cube_x_pourc = 0
cube_y_min = 150
cube_y = cube_y_min
spike_y_min = cube_y_min
cube_rotation = 0
cube_rot = False

#Phisique du jeu
gravity = 1.45
jump_strength = -9.5
velocity_x = 4.4
speed = velocity_x
velocity_y = 0
jump = False
is_jump = False
game_over = False

noclip = False

#Game
menu = True
game_menu = 1
in_level = False
ESC_level = False
current_level = None
chosen_level = 1
chosen_level_max = 2
level1 = False
level2 = False

#Obstacles
level_pourcentage = 0
obstacle_liste = []
obstacle_level_bool = False
obstacle_liste_temp = []
finish_level = False

#Sons
son_game_over = False
level1_song = False

#is cube falling ?
going_down = 0

#Variables souvent utilisés
def reset_death():
    if current_level == 'level1':
        return lvl1(spike_y_min)
    elif current_level == 'level2':
        return lvl2(spike_y_min)
def deplacement_obstacles(obstacle_liste):
    for obstacle in obstacle_liste:
        obstacle['x'] -= speed
    for obstacle in obstacle_liste:
        if obstacle['x'] < -16:
            obstacle_liste.remove(obstacle)
    return obstacle_liste
def stop():
    global speed, velocity_y, jump, cube_rot
    speed = 0
    velocity_y = 0
    jump = True
    cube_rot = False
def collision(obstacle):
    cube_gauche = cube_x
    cube_droit = cube_x+16
    cube_haut = cube_y
    cube_bas = cube_y+16


    #Hitbox spike:
    if obstacle['type']=='spike':
        obs_gauche = obstacle['x']+4
        obs_droit = obstacle['x']+11
        obs_haut = obstacle['y']+7
        obs_bas = obstacle['y']+16

    #Hitbox block et mur:
    elif obstacle['type']=='block' or obstacle['type']=='mur' or obstacle['type']=='orb':
        obs_gauche = obstacle['x']
        obs_droit = obstacle['x'] + 16
        obs_haut = obstacle['y']
        obs_bas = obstacle['y'] + 16
    if (cube_droit > obs_gauche and cube_gauche < obs_droit and cube_bas > obs_haut and cube_haut < obs_bas):
        return True
    return False
def QUIT_LEVEL():
    global finish_level, end_level, current_level, obstacle_liste, level1, level1_song, obstacle_level_bool
    global level2, in_level, menu, game_menu, ESC_level, son_game_over, cube_y, velocity_y, speed, jump, game_over
    if current_level == 'level1':
        obstacle_liste, end_level = lvl1(spike_y_min)
        level1 = False


    elif current_level == 'level2':
        obstacle_liste, end_level = lvl2(spike_y_min)
        level2 = False

    level1_song = False
    obstacle_level_bool = False
    #game
    in_level = False
    menu = True
    game_menu = 2
    ESC_level = False
    son_game_over = False
    finish_level = False
    pyxel.stop()

    #cube
    cube_y = cube_y_min
    velocity_y = 0
    speed = velocity_x
    jump = False
    game_over = False

def noclip_change():
    if pyxel.btnp(pyxel.KEY_N):
        if noclip:
            return False
        return True
    else:
        return noclip
def show_noclip():
    if noclip:
        pyxel.text(x-30,5,"NOCLIP",8)
def level_pourc():
    global cube_x_pourc, level_pourcentage
    cube_x_pourc += speed
    level_pourcentage = int(cube_x_pourc/(end_level_pourc-cube_x)*10000)
    level_pourcentage = level_pourcentage/100
    if level_pourcentage >= 100:
        level_pourcentage = 100

def is_going_down():
    global going_down, y_before, y_now, jump
    if not going_down:
        y_before = cube_y
        going_down = True
    elif going_down:
        y_now = cube_y
        going_down = False
        if y_before < y_now:
            jump = True


#level update et draw
def niveau_update(): #a faire: les songs
    global obstacle_level_bool, obstacle_liste, level1_song, jump, velocity_y, cube_y, cube_rotation, cube_rot, game_over, speed, son_game_over, end_level, finish_level, level_pourcentage, end_level_pourc, cube_x_pourc
    if not obstacle_level_bool:
        pyxel.mouse(False)
        obstacle_liste, end_level = reset_death()
        end_level_pourc = end_level
        cube_x_pourc = 0
        level_pourcentage = 0
        obstacle_level_bool = True
    #Obstacles:
    deplacement_obstacles(obstacle_liste)

    #Pourcentage du niveau:
    level_pourc()

    if not level1_song:
        pyxel.playm(0,0,True)
        level1_song = True

    #Saut du cube
    if pyxel.btn(pyxel.KEY_SPACE) and jump==False:
        jump = True
        velocity_y = jump_strength
        cube_rot = True
    cube_y += velocity_y
    velocity_y += gravity
    is_going_down()
    end_level -= speed
    for obstacle in obstacle_liste:
        if obstacle['type']=='orb':
            if obstacle['used']==False and collision(obstacle) and pyxel.btn(pyxel.KEY_SPACE): #A CONTINUER
                jump = True
                velocity_y = jump_strength
                cube_rot = True
                obstacle['used']=True

    if cube_rot:
        cube_rotation += 4
        if cube_rotation >= 80:
            cube_rotation = 0
    if jump==False:
        cube_rotation = 0
        cube_rot = False


    for obstacle in obstacle_liste:
        if obstacle['type']=='block' or obstacle['type']=='mur':
            cube_left = cube_x
            cube_right = cube_x + 16
            obs_left = obstacle['x']
            obs_right = obstacle['x'] + 16
            if (cube_right > obs_left and cube_left < obs_right and cube_y + 16 <= obstacle['y'] and cube_y + 16 + velocity_y >= obstacle['y']):
                cube_y = obstacle['y'] - 16
                velocity_y = 0
                jump = False


    #cube va au minimum au sol
    if cube_y >= cube_y_min:
        cube_y = cube_y_min
        jump = False
        velocity_y = 0

    for obstacle in obstacle_liste:
        if collision(obstacle) and not obstacle['type']=='orb' and noclip==False:
            game_over = True
            stop()

            if not son_game_over:
                pyxel.stop()
                pyxel.play(0, 63)
                son_game_over = True
            if pyxel.btnp(pyxel.KEY_R):
                obstacle_liste, end_level = reset_death()
                speed = velocity_x
                jump = False
                cube_y = cube_y_min
                pyxel.playm(0,0,True)
                son_game_over = False
                game_over = False
                level1_song = False
                obstacle_level_bool = False

    #endlevel
    if cube_x>=end_level:
        finish_level = True
    if finish_level:
        stop()
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
            QUIT_LEVEL()
        if pyxel.btnp(pyxel.KEY_R):
            obstacle_liste, end_level = reset_death()
            speed = velocity_x
            jump = False
            cube_y = cube_y_min
            pyxel.playm(0,0,True)
            son_game_over = False
            game_over = False
            level1_song = False
            finish_level = False
            obstacle_level_bool = False

def niveau_draw():
    pyxel.cls(1)
    #Sol blanc
    pyxel.rect(0, cube_y_min+16, x, y, 7)
    #Cube
    if cube_rotation >= 0 and cube_rotation < 10:
        pyxel.blt(cube_x, cube_y, 0, 0, 0, 16, 16, 0)
    elif cube_rotation >= 10 and cube_rotation < 40:
        pyxel.blt(cube_x, cube_y, 0, 16, 0, 16, 16, 0)
    elif cube_rotation >= 40 and cube_rotation < 50:
        pyxel.blt(cube_x, cube_y, 0, 32, 0, 16, 16, 0)
    elif cube_rotation >= 50 and cube_rotation <= 80:
        pyxel.blt(cube_x, cube_y, 0, 48, 0, 16, 16, 0)

    for obstacle in obstacle_liste:
        if obstacle['x'] < x:
            if obstacle['type']=='spike' and obstacle['turned']==False:
                pyxel.blt(obstacle['x'], obstacle['y'], 0, 16, 16, 16, 16, 0)
            if obstacle['type']=='spike' and obstacle['turned']==True:
                pyxel.blt(obstacle['x'], obstacle['y'], 0, 16, 32, 16, 16, 0)
            if obstacle['type']=='block':
                pyxel.blt(obstacle['x'], obstacle['y'], 0, 32, 16, 16, 16)
            if obstacle['type']=='mur':
                pyxel.blt(obstacle['x'], obstacle['y'], 0, 0, 16, 16, 16)
            if obstacle['type']=='orb':
                pyxel.blt(obstacle['x'], obstacle['y'], 0, 48, 16, 16, 16, 0)

    if game_over:
        pyxel.text(70, 70, "GAME OVER", 8)
        pyxel.text(55, 80, "R pour recommencer", 7)

    if finish_level:
        pyxel.text(70, 70, "LEVEL FINISHED", 8)
        pyxel.text(55, 80, "R pour recommencer", 7)
        pyxel.text(55, 90, "ESC pour quitter", 7)
        #Quitter
        pyxel.blt(5, 5, 1, 48, 0, 16, 16,0)
    pyxel.text(x//2-15, 5, f"{str(level_pourcentage)}%", 8)


def update():
    global cube_y, velocity_y, velocity_x, jump, game_over, speed, son_game_over
    global cube_rotation, cube_rot, game_menu, menu, level1_song, ESC_level
    global obstacle_level_bool, in_level, chosen_level, current_level, is_jump
    global noclip, level1, level2

    if menu:
        game_menu, chosen_level, level1, level2, current_level, menu, in_level = menu_update(game_menu, chosen_level, level1, level2, current_level, menu, in_level, chosen_level_max, x, y)

    #noclip
    noclip = noclip_change()

    #différents obstacles pour chaques niveaux
    if level1:
        niveau_update()

    if level2:
        niveau_update()

    #ESC dans le niveau
    if ESC_level:
        pyxel.mouse(True)

        speed = 0
        velocity_y = 0
        jump = True
        cube_rot = False
        #comment mettre la musique en pause ?

        #Quitter le niveau
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
            QUIT_LEVEL()

        #Reprendre le niveau
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < x/2+16 and pyxel.mouse_x > x/2-16 and pyxel.mouse_y < y/2+16 and pyxel.mouse_y > y/2-16:
            speed = velocity_x
            jump = is_jump
            is_jump = False
            pyxel.mouse(False)
            ESC_level = False

    if in_level and pyxel.btnp(pyxel.KEY_ESCAPE):
        is_jump = jump
        ESC_level = True


def draw():

    if menu: #menu
        menu_draw(game_menu, chosen_level, x, y)


    if in_level: #dans le niveau
        niveau_draw() #chaque level dessine la même chose
    show_noclip()
    if ESC_level:
        pyxel.blt(5, 5, 1, 48, 0, 16, 16,0) #croix (quitter)
        pyxel.blt(x/2-16, y/2-16, 1, 0, 0, 32, 32,0) #bouton reprendre



pyxel.run(update, draw)