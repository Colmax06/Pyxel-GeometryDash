import pyxel

class Cube:
    def __init__(self, game):
        self.game = game

        self.player_type = "cube"
        self.cube_x = 40
        self.cube_x_pourc = 0
        self.cube_y_min = 140
        self.cube_y = self.cube_y_min
        self.y_min = self.cube_y_min
        self.cube_rotation = 0
        self.cube_rot = False
        #cube falling
        self.going_down = 0
        self.cube_y_before = 0
        self.cube_y_now = 0


    def is_going_down(self):
        if not self.going_down:
            self.cube_y_before = self.cube_y
            self.going_down = True
        elif self.going_down:
            self.cube_y_now = self.cube_y
            self.going_down = False
            if not self.game.level.gravity_cube:
                if self.cube_y_before < self.cube_y_now:
                    self.game.level.jump = True
            if self.game.level.gravity_cube:
                if self.cube_y_before > self.cube_y_now:
                    self.game.level.jump = True

    def jump_rotation(self):
        #Saut du cube
        if self.player_type == "cube":
            if pyxel.btn(pyxel.KEY_SPACE) and self.game.level.jump==False:
                self.game.level.jumping()
        elif self.player_type == "ball":
            if pyxel.btnp(pyxel.KEY_SPACE) and self.game.level.jump==False:
                self.game.level.changing_gravity()


        if not self.game.level.gravity_cube:
            self.cube_y += self.game.level.velocity_y
            self.game.level.velocity_y += self.game.level.gravity
        if self.game.level.gravity_cube:
            self.cube_y -= self.game.level.velocity_y
            self.game.level.velocity_y += self.game.level.gravity
        self.is_going_down()
        self.game.level.end -= self.game.level.speed

        if self.game.level.velocity_y >= 20:
            self.game.level.velocity = 20
        if self.cube_rot:
            self.cube_rotation += 4
            if self.cube_rotation >= 80:
                self.cube_rotation = 0
        if self.game.level.jump==False:
            self.cube_rotation = 0
            self.cube_rot = False

        #Cube va au minimum au sol
        if not self.game.level.gravity_cube:
            if self.cube_y >= self.cube_y_min:
                self.cube_y = self.cube_y_min
                self.game.level.jump = False
                self.game.level.velocity_y = 0


    def draw_rotation_cube(self):
        if self.game.level.game_over:
            if self.player_type == "cube":
                pyxel.blt(self.cube_x, self.cube_y, 0, 80, 0, 16, 16, 0)
            elif self.player_type == "ball":
                pyxel.blt(self.cube_x, self.cube_y, 0, 96, 0, 16, 16, 0)
        elif not self.game.level.game_over:
            if self.player_type == "cube":
                if self.cube_rotation >= 0 and self.cube_rotation < 10:
                    pyxel.blt(self.cube_x, self.cube_y, self.game.pyxres.cube['basic']['image'], self.game.pyxres.cube['basic']['x'], self.game.pyxres.cube['basic']['y'], self.game.pyxres.cube['basic']['width'], self.game.pyxres.cube['basic']['height'], 0)
                elif self.cube_rotation >= 10 and self.cube_rotation < 40:
                    pyxel.blt(self.cube_x, self.cube_y, self.game.pyxres.cube['2']['image'], self.game.pyxres.cube['2']['x'], self.game.pyxres.cube['2']['y'], self.game.pyxres.cube['2']['width'], self.game.pyxres.cube['2']['height'], 0)
                elif self.cube_rotation >= 40 and self.cube_rotation < 50:
                    pyxel.blt(self.cube_x, self.cube_y, self.game.pyxres.cube['3']['image'], self.game.pyxres.cube['3']['x'], self.game.pyxres.cube['3']['y'], self.game.pyxres.cube['3']['width'], self.game.pyxres.cube['3']['height'], 0)
                elif self.cube_rotation >= 50 and self.cube_rotation <= 80:
                    pyxel.blt(self.cube_x, self.cube_y, self.game.pyxres.cube['4']['image'], self.game.pyxres.cube['4']['x'], self.game.pyxres.cube['4']['y'],  self.game.pyxres.cube['4']['width'], self.game.pyxres.cube['4']['height'], 0)
            elif self.player_type == "ball":
                pyxel.blt(self.cube_x, self.cube_y, 0, 64, 0,  16, 16, 0)        