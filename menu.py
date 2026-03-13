import pyxel
import json

class Menu:
    def __init__(self, game):
        self.game = game

        self.in_menu = True
        self.menu_song_var = False
        self.game_menu = 1
        self.chosen_level  = 1
        self.chosen_level_max = 0

        
        


    def get_lvl_difficulty(self):
        _, _, self.difficulty = self.game.level.get_lvl_data()


    def menu_update(self):
        if self.in_menu:
            if not self.menu_song_var:
                pyxel.playm(0, 0, True) #menu song
                self.get_lvl_difficulty()
                self.menu_song_var = True
                
            pyxel.mouse(True)
            if self.game_menu == 1: #menu principale
                #Quitter
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
                    pyxel.quit()
                    #A FAIRE (SUR DE QUITTER)

                #Bouton pour game_menu = 2
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.game.screen_x/2+16 and pyxel.mouse_x > self.game.screen_x/2-16 and pyxel.mouse_y < self.game.screen_y/2+16 and pyxel.mouse_y > self.game.screen_y/2-16:
                    self.game_menu = 2
                    self.chosen_level = 1
            

            elif self.game_menu == 2:
                #Retour game_menu (croix)
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
                    self.game_menu = 1

                #Choix niveau
                elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 10+16 and pyxel.mouse_x > 10 and pyxel.mouse_y < self.game.screen_y/2+16 and pyxel.mouse_y > self.game.screen_y/2 or pyxel.btnp(pyxel.KEY_LEFT): #gauche
                    if self.chosen_level == 1:
                        self.chosen_level = self.chosen_level_max
                    else:
                        self.chosen_level -= 1
                    self.game.level.current_level = f'lvl{self.chosen_level}'
                    self.get_lvl_difficulty()
                elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.game.screen_x-10 and pyxel.mouse_x > self.game.screen_x-10-16 and pyxel.mouse_y < self.game.screen_y/2+16 and pyxel.mouse_y > self.game.screen_y/2 or pyxel.btnp(pyxel.KEY_RIGHT): #droit
                    if self.chosen_level == self.chosen_level_max:
                        self.chosen_level = 1
                    else:
                        self.chosen_level += 1
                    self.game.level.current_level = f'lvl{self.chosen_level}'
                    self.get_lvl_difficulty()

                #Bouton cliqué ? JOUER
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.game.screen_x/2-64+128 and pyxel.mouse_x > self.game.screen_x/2-64 and pyxel.mouse_y < self.game.screen_y/2-16+32 and pyxel.mouse_y > self.game.screen_y/2-16 or pyxel.btnp(pyxel.KEY_RETURN):
                    self.in_menu = False
                    self.game.level.in_level = True

                #Bouton edit lvls
                if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.game.screen_x/2-90+16 and pyxel.mouse_x > self.game.screen_x/2-90 and pyxel.mouse_y < self.game.screen_y/2-5+16 and pyxel.mouse_y > self.game.screen_y/2-5:
                    #SAVOIR QUELLE NIVEAU A EDITER
                    pyxel.stop()
                    self.game.level_editor.in_editor = True
                    self.game.level_editor.choosing_level = self.chosen_level
                    self.in_menu = False


    def menu_draw(self):
        if self.in_menu:
            pyxel.cls(1)
            if self.game_menu == 1: #menu principale
                #Quitter
                pyxel.blt(5, 5, 1, 48, 0, 16, 16,0)

                #Bouton pour game_menu = 2
                pyxel.blt(self.game.screen_x/2-16, self.game.screen_y/2-16, 1, 0, 0, 32, 32,0)


            elif self.game_menu == 2: #Sélection niveaux
                #Retour game_menu (croix)
                pyxel.blt(5, 5, 1, 48, 0, 16, 16,0)


                #Edit lvls
                pyxel.blt(self.game.screen_x/2-90, self.game.screen_y/2-5, 1, 88, 0, 16, 16,0)


                #Choix niveau
                pyxel.blt(10, self.game.screen_y/2, 1, 32, 16, 16, 16,0) #gauche
                pyxel.blt(self.game.screen_x-10-16, self.game.screen_y/2, 1, 32, 0, 16, 16,0) #droit
                
                #Bouton Jouer
                pyxel.bltm(self.game.screen_x/2-64, self.game.screen_y/2-16, 0, 0, self.chosen_level*32, 128, 32, 0)

                #Difficulté Niveau
                pyxel.blt(self.game.screen_x/2-8, self.game.screen_y/2+25, self.game.pyxres.difficulty[self.difficulty]['image'], self.game.pyxres.difficulty[self.difficulty]['x'], self.game.pyxres.difficulty[self.difficulty]['y'], self.game.pyxres.difficulty[self.difficulty]['width'], self.game.pyxres.difficulty[self.difficulty]['height'], 0)
        