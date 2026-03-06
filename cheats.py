import pyxel

class Cheats:
    def __init__(self, game):
        self.game = game
        self.speedlvl = False
        self.noclip = False

        self.increased_speed = self.game.level.velocity_x*3

    def noclip_change(self):
        if pyxel.btnp(pyxel.KEY_N):
            if self.noclip:
                return False
            return True
        else:
            return self.noclip
    
    def speedlvl_change(self):
        if pyxel.btnp(pyxel.KEY_B):
            if not self.speedlvl:
                self.game.level.speed = self.increased_speed
                return True
            elif self.speedlvl:
                self.game.level.speed = self.game.level.velocity_x
                return False
        else:
            return self.speedlvl

    def cheats_update(self):
        self.noclip = self.noclip_change()
        self.speedlvl = self.speedlvl_change()
    def cheats_draw(self):
        if self.noclip:
            pyxel.text(self.game.screen_x-30,5,"NOCLIP",8)
        if self.speedlvl:
            pyxel.text(self.game.screen_x-80,5,"SPEED BOOST",8)