import pyxel
import json

class Level:
    def __init__(self, game):
        self.game = game

        #Phisique du jeu
        self.gravity = 1.12
        self.jump_strength = -8.15
        self.jump_pad_strength = -11
        self.velocity_x = 4.4
        self.speed = self.velocity_x
        self.velocity_y = 0
        self.jump = False
        self.jump_status = False
        self.game_over = False
        self.game_over_time = 0

        self.gravity_cube = False

        #Obstacles
        self.pourcentage = 0
        self.obstacle_liste = []
        self.initialisation = False
        self.finish = False
        self.end = 0
        self.end_pourc = 0

        
        self.collisions = {
            'cube portal': {
                'obs_gauche': 4,
                'obs_droit': 11,
                'obs_haut': 0,
                'obs_bas': 16
            },
            'ball portal': {
                'obs_gauche': 4,
                'obs_droit': 11,
                'obs_haut': 0,
                'obs_bas': 16
            },
            'spike': {
                'obs_gauche': 4,
                'obs_droit': 11,
                'obs_haut': 7,
                'obs_bas': 16
            },
            'turned spike': {
                'obs_gauche': 4,
                'obs_droit': 11,
                'obs_haut': 0,
                'obs_bas': 7
            },
            'block': {
                'obs_gauche': 0,
                'obs_droit': 16,
                'obs_haut': 0,
                'obs_bas': 16
            },
            'mur': {
                'obs_gauche': 0,
                'obs_droit': 16,
                'obs_haut': 0,
                'obs_bas': 16
            },
            'orb': {
                'obs_gauche': -2,
                'obs_droit': 18,
                'obs_haut': -2,
                'obs_bas': 18
            },
            'jump pad': {
                'obs_gauche': 0,
                'obs_droit': 16,
                'obs_haut': 14,
                'obs_bas': 16
            },
            'gravity orb': {
                'obs_gauche': -2,
                'obs_droit': 18,
                'obs_haut': -2,
                'obs_bas': 18
            },
            'small spike': {
                'obs_gauche': 4,
                'obs_droit': 11,
                'obs_haut': 11,
                'obs_bas': 16
            },
            'small turned spike': {
                'obs_gauche': 4,
                'obs_droit': 11,
                'obs_haut': 0,
                'obs_bas': 5
            },
            'gravity pad': {
                'obs_gauche': 0,
                'obs_droit': 16,
                'obs_haut': 14,
                'obs_bas': 16
            },
        }
        
        self.death_sound_var = False

        #Game
        self.in_level = False
        self.ESC_level = False
        self.current_level = 'lvl1'

        self.music_position = None
        self.sound = 0
        self.sec = 0
        self.sec_list = [0] * 64

    def default_var(self):
        #music
        self.game.menu.menu_song_var = False
        self.death_sound_var = False
        self.music_position = None
        self.sound = 0
        self.sec = 0
        self.sec_list = [0] * 64

        #cube
        self.game.cube.player_type = "cube"
        self.game.cube.cube_y = self.game.cube.cube_y_min
        self.velocity_y = 0
        self.speed = self.velocity_x
        self.jump = False
        self.game_over = False
        self.finish = False
        self.game_over_time = 0

        self.gravity_cube = False

        #game
        self.initialisation = False
        self.ESC_level = False
        #Pourcentage
        self.end_pourc = self.end
        self.game.cube.cube_x_pourc = 0

        #Cheats
        self.game.cheats.noclip = False
        self.game.cheats.speedlvl = False

    def get_lvl_data(self):
        if not self.current_level in self.game.levels:
            new_file = f"{self.game.folders['levels']}\\{self.current_level}.json"
            with open(new_file, 'w') as f:
                data = {"level_length": 0, "difficulty": "NA", "obstacles": {}}
                json.dump(data, f, indent=4)

        file = self.game.levels[self.current_level]
        with open(file, 'r') as f:
            data = json.load(f)
            level_length = data['level_length']
            obstacle_liste = data['obstacles']
            difficulty = data['difficulty']
        return obstacle_liste, level_length, difficulty

    def reset_obstacles(self):
        self.obstacle_liste, self.end, self.difficulty = self.get_lvl_data()

    

    def level_init(self):
        if not self.initialisation:
            pyxel.mouse(False)
            self.reset_obstacles()
            self.default_var()
            self.game.music.stop_allsongs()
            self.game.music.play_song()
            self.initialisation = True
    def jumping(self):
        self.jump = True
        self.velocity_y = self.jump_strength
        self.game.cube.cube_rot = True
    
    def changing_gravity(self):
        self.velocity_y = -self.jump_strength-3
        if not self.gravity_cube:
            self.gravity_cube = True
        elif self.gravity_cube:
            self.gravity_cube = False

    def deplacement_obstacles(self):
        for obstacle in self.obstacle_liste:
            obstacle['x'] -= self.speed
        for obstacle in self.obstacle_liste:
            if obstacle['x'] < -16:
                self.obstacle_liste.remove(obstacle)
    def obstacles_gestion(self):
        for obstacle in self.obstacle_liste:
            #Rester sur le bloc
            if not self.gravity_cube:
                if obstacle['type']=='block' or obstacle['type']=='mur':
                    cube_gauche = self.game.cube.cube_x
                    cube_droit = self.game.cube.cube_x + 16
                    cube_bas = self.game.cube.cube_y + 16
                    obs_gauche = obstacle['x']
                    obs_droite = obstacle['x'] + 16
                    obs_haut = obstacle['y']
                    
                    if (cube_droit > obs_gauche and cube_gauche < obs_droite and cube_bas <= obs_haut and cube_bas + self.velocity_y >= obs_haut):
                        self.game.cube.cube_y = obstacle['y'] - 16
                        self.velocity_y = 0
                        self.jump = False

            if self.gravity_cube:
                if obstacle['type']=='block' or obstacle['type']=='mur':
                    cube_gauche = self.game.cube.cube_x
                    cube_droit = self.game.cube.cube_x + 16
                    cube_haut = self.game.cube.cube_y
                    obs_gauche = obstacle['x']
                    obs_droite = obstacle['x'] + 16
                    obs_bas = obstacle['y'] + 16
                    
                    if (cube_droit > obs_gauche and cube_gauche < obs_droite and cube_haut >= obs_bas and cube_haut - self.velocity_y <= obs_bas):
                        self.game.cube.cube_y = obstacle['y'] + 16
                        self.velocity_y = 0
                        self.jump = False


            #Utilisation de l'orb
            if obstacle['type']=='orb':
                if self.collision(obstacle) and pyxel.btnp(pyxel.KEY_SPACE):
                    self.jumping()

            #Utilisation du gravity orb
            if obstacle['type']=='gravity orb':
                if self.collision(obstacle) and pyxel.btnp(pyxel.KEY_SPACE):
                    self.changing_gravity()
            
            #Utilisation du jump pad
            if obstacle['type']=='jump pad':
                if self.collision(obstacle):
                    self.jumping()
                    self.velocity_y = self.jump_pad_strength

            if obstacle['type']=='cube portal':
                if self.collision(obstacle):
                    self.game.cube.player_type = "cube"

            if obstacle['type']=='ball portal':
                if self.collision(obstacle):
                    self.game.cube.player_type = "ball"

            #Utilisation du gravity pad
            if obstacle['type']=='gravity pad':
                 if self.collision(obstacle):
                    self.changing_gravity()

            #Collisions
            if self.collision(obstacle) and not obstacle['type']=='ball portal' and not obstacle['type']=='cube portal' and not obstacle['type']=='orb' and not obstacle['type']=='jump pad' and not obstacle['type']=='gravity orb' and not obstacle['type']=='gravity pad' and self.game.cheats.noclip==False:
                self.game_over = True
                self.game_over_time += 2
                self.game.music.death_sound()
                self.stop()
                if self.game_over_time >= 40:
                    self.initialisation = False
    def collision(self, obstacle): #Utilisé dans obstacles_gestion()
        #obstacle hors écran
        if obstacle['x'] > self.game.screen_x:
            return False

        #Mise à jour de la position du cube
        self.collisions['cube'] = {
                'cube_gauche': self.game.cube.cube_x,
                'cube_droit': self.game.cube.cube_x+16,
                'cube_haut': self.game.cube.cube_y,
                'cube_bas': self.game.cube.cube_y+16
            }

        obs_gauche = obstacle['x']+self.collisions[obstacle['type']]['obs_gauche']
        obs_droit = obstacle['x']+self.collisions[obstacle['type']]['obs_droit']
        obs_haut = obstacle['y']+self.collisions[obstacle['type']]['obs_haut']
        obs_bas = obstacle['y']+self.collisions[obstacle['type']]['obs_bas']

        if (self.collisions['cube']['cube_droit'] > obs_gauche and self.collisions['cube']['cube_gauche'] < obs_droit and self.collisions['cube']['cube_bas'] > obs_haut and self.collisions['cube']['cube_haut'] < obs_bas):
            return True
        return False


    def level_pourc(self):
        self.game.cube.cube_x_pourc += self.speed
        self.pourcentage = int(self.game.cube.cube_x_pourc/(self.end_pourc-self.game.cube.cube_x)*10000)
        self.pourcentage = self.pourcentage/100
        if self.pourcentage >= 100:
            self.pourcentage = 100
    def is_end_level(self):
        if self.game.cube.cube_x>=self.end:
            self.finish = True
        if self.finish:
            pyxel.mouse(True)
            self.stop()
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 100+16 and pyxel.mouse_x > 100 and pyxel.mouse_y < 115+16 and pyxel.mouse_y > 115 or pyxel.btnp(pyxel.KEY_ESCAPE):
                self.QUIT_LEVEL()
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 170+16 and pyxel.mouse_x > 170 and pyxel.mouse_y < 115+16 and pyxel.mouse_y > 115 or pyxel.btnp(pyxel.KEY_R):
                #pyxel.blt(170, 115, 1, 64, 0, 16, 16, 0) #Recommencer
                self.initialisation = False
    def stop(self):
        self.speed = 0
        self.velocity_y = 0
        self.jump = True
        self.game.cube.cube_rot = False
    def QUIT_LEVEL(self):
        self.reset_obstacles()
        self.game.music.stop_allsongs()
        self.default_var()
        #game
        self.in_level = False
        self.game.menu.in_menu = True
        self.game.menu.game_menu = 2
    def ESC(self):
        if self.ESC_level:
            pyxel.mouse(True)
            self.game.music.stop_allsongs()
            self.speed = 0
            self.velocity_y = 0
            self.jump = True
            self.game.cube.cube_rot = False
            #comment mettre la musique en pause ?

            #Quitter le niveau
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
                self.QUIT_LEVEL()

            #Reprendre le niveau
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.game.screen_x/2+16 and pyxel.mouse_x > self.game.screen_x/2-16 and pyxel.mouse_y < self.game.screen_y/2+16 and pyxel.mouse_y > self.game.screen_y/2-16:
                self.game.music.resume_song()
                if self.game.cheats.speedlvl:
                    self.speed = self.game.cheats.increased_speed
                else:
                    self.speed = self.velocity_x
                self.jump = self.jump_status
                self.jump_status = False
                pyxel.mouse(False)
                self.ESC_level = False

        if self.in_level and pyxel.btnp(pyxel.KEY_ESCAPE):
            self.jump_status = self.jump
            self.ESC_level = True




    def niveau_update(self):
        if self.in_level:
            #Level initialization
            self.level_init()

            #Get song position
            self.game.music.get_song_pos()

            #Gestion d'obstacles
            self.obstacles_gestion()

            #Obstacles:
            self.deplacement_obstacles()

            #Pourcentage du niveau:
            self.level_pourc()

            #Gestion du cube
            self.game.cube.jump_rotation()

            #ESC
            self.ESC()

            #endlevel
            self.is_end_level()

    def niveau_draw(self):
        if self.in_level:
            pyxel.cls(1)
            #Sol blanc
            pyxel.rect(0, self.game.cube.cube_y_min+16, self.game.screen_x, self.game.screen_y, 7)

            #Cube
            self.game.cube.draw_rotation_cube()

            #Obstacles
            for obstacle in self.obstacle_liste:
                if obstacle['x'] < self.game.screen_x:
                    pyxel.blt(obstacle['x'], obstacle['y'], self.game.pyxres.obstacles[obstacle['type']]['image'], self.game.pyxres.obstacles[obstacle['type']]['x'], self.game.pyxres.obstacles[obstacle['type']]['y'], self.game.pyxres.obstacles[obstacle['type']]['width'], self.game.pyxres.obstacles[obstacle['type']]['height'], 0)

            if self.game_over:
                pyxel.text(70, 70, "GAME OVER", 8)

            if self.finish:
                pyxel.blt(self.game.screen_x//2-40, self.game.screen_y//2-20, 2, 0, 0, 64, 32 , 0) #Level complete
                pyxel.blt(100, 115, 1, 48, 0, 16, 16 , 0)   #Quitter
                pyxel.blt(170, 115, 1, 64, 0, 16, 16, 0) #Recommencer
            pyxel.text(self.game.screen_x//2-15, 5, f"{str(self.pourcentage)}%", 8)

            #ESC menu
            if self.ESC_level:
                pyxel.blt(5, 5, 1, 48, 0, 16, 16,0) #croix (quitter)
                pyxel.blt(self.game.screen_x/2-16, self.game.screen_y/2-16, 1, 0, 0, 32, 32,0) #bouton reprendre