import pyxel
import os

#Class
from editlvls import LevelEditor
from menu import Menu
from cube import Cube
from cheats import Cheats
from level import Level
from music import Music
from pyxres import Pyxres


class Game:
    def __init__(self):
        self.screen_x = 300
        self.screen_y = 200
        pyxel.init(self.screen_x, self.screen_y, quit_key=pyxel.KEY_P, title="GeometryDash")
        pyxel.mouse(True)
        pyxel.load("geometrydash.pyxres")

        self.folders = {
            "default": os.getcwd(),
            "levels": f"{os.getcwd()}\\levels",
            "editlevels": f"{os.getcwd()}\\editlevels"
        }

        #Class
        self.pyxres = Pyxres(self)
        self.level_editor = LevelEditor(self)
        self.menu = Menu(self)
        self.cube = Cube(self)
        self.level = Level(self)
        self.cheats = Cheats(self)
        self.music = Music(self)


        self.levels_json()


        pyxel.run(self.update, self.draw)




    def levels_json(self):
        #Fichiers où se trouvent les niveaux
        levels_folder = self.folders["levels"]
        self.levels = {}
        for filename in os.listdir(levels_folder):
            if filename.endswith(".json") and filename.startswith("lvl"):
                #Créer une variable avec l'emplacement du fichier.json
                var_name = filename.replace(".json", "")
                self.levels[var_name] = f"{levels_folder}\\{filename}"
                self.menu.chosen_level_max += 1







    #Game
    def update(self):
        #Menu
        self.menu.menu_update()

        #Niveau en cours
        self.level.niveau_update()

        #Lvl editor
        self.level_editor.editor_update()

        #Cheats
        self.cheats.cheats_update()



    def draw(self):
        #Menu
        self.menu.menu_draw()

        #Lvl editor
        self.level_editor.editor_draw()

        #Niveau
        self.level.niveau_draw()

        #Cheats
        self.cheats.cheats_draw()



Game()