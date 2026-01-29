import pyxel
from obstacleslvls import *
from menu import *



class Game:
    def __init__(self):
        self.screen_x = 300
        self.screen_y = 200
        pyxel.init(self.screen_x, self.screen_y, quit_key=pyxel.KEY_P, title="GeometryDash")
        pyxel.mouse(True)
        pyxel.load("geometrydash.pyxres")


        #cube
        self.cube_x = 40
        self.cube_x_pourc = 0
        self.cube_y_min = 150
        self.cube_y = self.cube_y_min
        self.spike_y_min = self.cube_y_min
        self.cube_rotation = 0
        self.cube_rot = False
        #cube falling
        self.going_down = 0
        self.cube_y_before = 0
        self.cube_y_now = 0

        #Phisique du jeu
        self.gravity = 1.45
        self.jump_strength = -9.5
        self.velocity_x = 4.4
        self.speed = self.velocity_x
        self.velocity_y = 0
        self.jump = False
        self.is_jump = False
        self.game_over = False

        self.noclip = False

        #Game
        self.menu = True
        self.game_menu = 1
        self.in_level = False
        self.ESC_level = False
        self.current_level = None
        self.chosen_level = 1
        self.chosen_level_max = 2



        #Obstacles
        self.level_pourcentage = 0
        self.obstacle_liste = []
        self.level_initialisation = False
        self.finish_level = False
        self.end_level = 0
        self.end_level_pourc = 0



        pyxel.run(self.update, self.draw)

    def pause_song(self):
        pass

    def play_song(self):
        pass


    def stop_allsongs(self):
        pass


    #Variables souvent utilisés
    def reset_death(self):
        if self.current_level == 'level1':
            self.obstacle_liste, self.end_level = lvl1(self.spike_y_min)
            #Jouer la music du niveau 1
        elif self.current_level == 'level2':
            self.obstacle_liste, self.end_level = lvl2(self.spike_y_min)
            #Jouer la music du niveau 2

    def deplacement_obstacles(self):
        for obstacle in self.obstacle_liste:
            obstacle['x'] -= self.speed
        for obstacle in self.obstacle_liste:
            if obstacle['x'] < -16:
                self.obstacle_liste.remove(obstacle)

    def stop(self):
        self.speed = 0
        self.velocity_y = 0
        self.jump = True
        self.cube_rot = False

    def collision(self, obstacle):
        cube_gauche = self.cube_x
        cube_droit = self.cube_x+16
        cube_haut = self.cube_y
        cube_bas = self.cube_y+16

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

    def QUIT_LEVEL(self):
        self.reset_death()

        self.level_initialisation = False
        #game
        self.in_level = False
        self.menu = True
        self.game_menu = 2
        self.ESC_level = False
        self.finish_level = False

        #cube
        self.cube_y = self.cube_y_min
        self.velocity_y = 0
        self.speed = self.velocity_x
        self.jump = False
        self.game_over = False

    def noclip_change(self):
        if pyxel.btnp(pyxel.KEY_N):
            if self.noclip:
                return False
            return True
        else:
            return self.noclip

    def show_noclip(self):
        if self.noclip:
            pyxel.text(self.screen_x-30,5,"NOCLIP",8)

    def level_pourc(self):
        self.cube_x_pourc += self.speed
        self.level_pourcentage = int(self.cube_x_pourc/(self.end_level_pourc-self.cube_x)*10000)
        self.level_pourcentage = self.level_pourcentage/100
        if self.level_pourcentage >= 100:
            self.level_pourcentage = 100

    def is_going_down(self):
        if not self.going_down:
            self.cube_y_before = self.cube_y
            self.going_down = True
        elif self.going_down:
            self.cube_y_now = self.cube_y
            self.going_down = False
            if self.cube_y_before < self.cube_y_now:
                self.jump = True

    def restart_level(self):
        self.reset_death()
        #arrêter toutes les musics
        self.speed = self.velocity_x
        self.jump = False
        self.cube_y = self.cube_y_min
        self.game_over = False
        self.level_initialisation = False

    def level_init(self):
        if not self.level_initialisation:
            pyxel.mouse(False)
            self.reset_death()
            self.end_level_pourc = self.end_level
            self.cube_x_pourc = 0
            self.level_pourcentage = 0
            self.level_initialisation = True

    def cube_jump_rot(self):
        #Saut du cube
        if pyxel.btn(pyxel.KEY_SPACE) and self.jump==False:
            self.jump = True
            self.velocity_y = self.jump_strength
            self.cube_rot = True
        self.cube_y += self.velocity_y
        self.velocity_y += self.gravity
        self.is_going_down()
        self.end_level -= self.speed

        if self.cube_rot:
            self.cube_rotation += 4
            if self.cube_rotation >= 80:
                self.cube_rotation = 0
        if self.jump==False:
            self.cube_rotation = 0
            self.cube_rot = False

        #Cube va au minimum au sol
        if self.cube_y >= self.cube_y_min:
            self.cube_y = self.cube_y_min
            self.jump = False
            self.velocity_y = 0

    def obstacles_gestion(self):
        for obstacle in self.obstacle_liste:
            #Rester sur le bloc
            if obstacle['type']=='block' or obstacle['type']=='mur':
                cube_left = self.cube_x
                cube_right = self.cube_x + 16
                obs_left = obstacle['x']
                obs_right = obstacle['x'] + 16
                if (cube_right > obs_left and cube_left < obs_right and self.cube_y + 16 <= obstacle['y'] and self.cube_y + 16 + self.velocity_y >= obstacle['y']):
                    self.cube_y = obstacle['y'] - 16
                    self.velocity_y = 0
                    self.jump = False

            #Utilisation de l'orb
            if obstacle['type']=='orb':
                if obstacle['used']==False and self.collision(obstacle) and pyxel.btn(pyxel.KEY_SPACE): #A CONTINUER
                    self.jump = True
                    self.velocity_y = self.jump_strength
                    self.cube_rot = True
                    obstacle['used']=True

            #Collisions
            if self.collision(obstacle) and not obstacle['type']=='orb' and self.noclip==False:
                self.game_over = True
                #pause music
                #jouer music de mort
                self.stop()
                if pyxel.btnp(pyxel.KEY_R):
                    self.restart_level()

    def is_end_level(self):
        if self.cube_x>=self.end_level:
            self.finish_level = True
        if self.finish_level:
            self.stop()
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
                self.QUIT_LEVEL()
            if pyxel.btnp(pyxel.KEY_R):
                self.restart_level()

    def ESC(self):
        if self.ESC_level:
            pyxel.mouse(True)
            #pause music
            self.speed = 0
            self.velocity_y = 0
            self.jump = True
            self.cube_rot = False
            #comment mettre la musique en pause ?

            #Quitter le niveau
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
                self.QUIT_LEVEL()

            #Reprendre le niveau
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.screen_x/2+16 and pyxel.mouse_x > self.screen_x/2-16 and pyxel.mouse_y < self.screen_y/2+16 and pyxel.mouse_y > self.screen_y/2-16:
                #reprendre la music
                self.speed = self.velocity_x
                self.jump = self.is_jump
                self.is_jump = False
                pyxel.mouse(False)
                self.ESC_level = False

        if self.in_level and pyxel.btnp(pyxel.KEY_ESCAPE):
            self.is_jump = self.jump
            self.ESC_level = True

    #level update et draw
    def niveau_update(self):
        #Level initialization
        self.level_init()

        #Gestion d'obstacles
        self.obstacles_gestion()

        #Obstacles:
        self.deplacement_obstacles()

        #Pourcentage du niveau:
        self.level_pourc()

        #Gestion du cube
        self.cube_jump_rot()

        #endlevel
        self.is_end_level()

    def niveau_draw(self):
        pyxel.cls(1)
        #Sol blanc
        pyxel.rect(0, self.cube_y_min+16, self.screen_x, self.screen_y, 7)
        #Cube
        if self.cube_rotation >= 0 and self.cube_rotation < 10:
            pyxel.blt(self.cube_x, self.cube_y, 0, 0, 0, 16, 16, 0)
        elif self.cube_rotation >= 10 and self.cube_rotation < 40:
            pyxel.blt(self.cube_x, self.cube_y, 0, 16, 0, 16, 16, 0)
        elif self.cube_rotation >= 40 and self.cube_rotation < 50:
            pyxel.blt(self.cube_x, self.cube_y, 0, 32, 0, 16, 16, 0)
        elif self.cube_rotation >= 50 and self.cube_rotation <= 80:
            pyxel.blt(self.cube_x, self.cube_y, 0, 48, 0, 16, 16, 0)

        for obstacle in self.obstacle_liste:
            if obstacle['x'] < self.screen_x:
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

        if self.game_over:
            pyxel.text(70, 70, "GAME OVER", 8)
            pyxel.text(55, 80, "R pour recommencer", 7)

        if self.finish_level:
            pyxel.text(70, 70, "LEVEL FINISHED", 8)
            pyxel.text(55, 80, "R pour recommencer", 7)
            pyxel.text(55, 90, "ESC pour quitter", 7)
            #Quitter
            pyxel.blt(5, 5, 1, 48, 0, 16, 16,0)
        pyxel.text(self.screen_x//2-15, 5, f"{str(self.level_pourcentage)}%", 8)

    def update(self):
        if self.menu:
            menu_update(self)
            #arrêter toutes les musics

        #noclip
        self.noclip = self.noclip_change()

        #Niveau en cours
        if self.in_level:
            self.niveau_update()

        #ESC dans le niveau
        self.ESC()

    def draw(self):
        if self.menu: #menu
            menu_draw(self)

        if self.in_level: #dans le niveau
            self.niveau_draw() #chaque level dessine la même chose
        self.show_noclip()
        if self.ESC_level:
            pyxel.blt(5, 5, 1, 48, 0, 16, 16,0) #croix (quitter)
            pyxel.blt(self.screen_x/2-16, self.screen_y/2-16, 1, 0, 0, 32, 32,0) #bouton reprendre



Game()