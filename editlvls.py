import pyxel
import json
import os

class LevelEditor:
    def __init__(self, game):
        pyxel.mouse(True)
        self.game = game
        #init all variables
        self.in_editor = False
        self.new_json_file = 1
        self.custum_level = f"{self.game.folders['levels']}\\custum_level.json"

        self.initialisation = False
        self.camera_x = 0
        self.camera_y = 0

        #Level choosing
        self.choosing_level = 1
        self.choosen_obstacles = 'spike'
        self.choosen_placement = 'place'
        self.mouse_x = 0
        self.mouse_y = 0


        self.no_place_obstacle = 0

        self.obstacles_temp = []
        self.end_of_level = None
        self.lvl_name = ""
        self.lvl_name_text = ""
        self.save_as_text = False
        self.lvl_already_exists = False
        self.exists_timer = 0

        self.obstacles_pos = {
            'place': {'x': 1, 'y': self.game.screen_y-40},
            'delete': {'x': 1, 'y': self.game.screen_y-20},
            'cube portal': {'x': 120, 'y': self.game.screen_y-20},
            'ball portal': {'x': 140, 'y': self.game.screen_y-20},
            'spike': {'x': 20, 'y': self.game.screen_y-40},
            'turned spike': {'x': 20, 'y': self.game.screen_y-20},
            'block': {'x': 60, 'y': self.game.screen_y-40},
            'mur': {'x': 60, 'y': self.game.screen_y-20},
            'orb': {'x': 80, 'y': self.game.screen_y-40},
            'jump pad': {'x': 80, 'y': self.game.screen_y-20},
            'gravity orb': {'x': 100, 'y': self.game.screen_y-40},
            'small spike': {'x': 40, 'y': self.game.screen_y-40},
            'small turned spike': {'x': 40, 'y': self.game.screen_y-20},
            'gravity pad': {'x': 100, 'y': self.game.screen_y-20},
        }
      
        self.difficulty_pos = {
            'NA': {'x': self.game.screen_x/2-58, 'y': self.game.screen_y/2-58},
            'normal': {'x': self.game.screen_x/2-58+18, 'y': self.game.screen_y/2-58},
            'hard': {'x': self.game.screen_x/2-58+18+18, 'y': self.game.screen_y/2-58},
            'insane': {'x': self.game.screen_x/2-58+18+18+18, 'y': self.game.screen_y/2-58},
            'demon': {'x': self.game.screen_x/2-58+18+18+18+18, 'y': self.game.screen_y/2-58}
        }

        self.in_choosing_difficulty = False

                



    def save_as(self):
        if self.save_as_text:
            if pyxel.input_text:
                self.lvl_name_text += pyxel.input_text
            if pyxel.btnp(pyxel.KEY_BACKSPACE) and len(self.lvl_name_text) > 0:
                self.lvl_name_text = self.lvl_name_text[:-1]
            if pyxel.btnp(pyxel.KEY_KP_ENTER) or pyxel.btnp(pyxel.KEY_RETURN):
                self.lvl_name = f"{self.game.folders['levels']}\\{self.lvl_name_text}.json"
                print(self.lvl_name)
                if os.path.exists(self.lvl_name):
                    self.lvl_already_exists = True
                    return
                
                if self.lvl_name == "":
                    self.lvl_name = self.custum_level
                    while os.path.exists(self.lvl_name):
                        self.lvl_name = f"levels\\custum_level{self.new_json_file}.json"
                        self.new_json_file += 1
                
                self.write_json(self.lvl_name, self.obstacles_temp)
                self.new_json_file = 1
                self.save_as_text = False
                self.lvl_name_text = ""
        
        if self.lvl_already_exists:
            self.exists_timer +=1
            if self. exists_timer >= 50:
                self.lvl_already_exists = False
    def draw_save_as(self):
        if self.save_as_text:
            pyxel.text(self.game.screen_x/2-80, self.game.screen_y/2-63, "Level name:", 7)
            pyxel.text(self.game.screen_x/2-80, self.game.screen_y/2-55, f"{self.lvl_name_text}_", 7)
            if self.lvl_already_exists:
                pyxel.text(self.game.screen_x/2-80, self.game.screen_y/2-47, "Level already exists", 2)

    def quit_editor(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < 5+16 and pyxel.mouse_x > 5 and pyxel.mouse_y < 5+16 and pyxel.mouse_y > 5 or pyxel.btnp(pyxel.KEY_ESCAPE):
            self.in_editor = False
            self.game.menu.in_menu = True
            self.no_place_obstacle = 0
            self.initialisation = False
            self.camera_x = 0
            self.camera_y = 0
            self.choosen_placement = 'place'
            self.game.menu.menu_song_var = False
            self.save_as_text = False
            self.lvl_already_exists = False
            self.in_choosing_difficulty = False

    def mouse_pos(self):
        self.mouse_x = pyxel.mouse_x
        self.mouse_y = pyxel.mouse_y
        if self.mouse_y >= self.game.cube.cube_y_min+8:
            self.mouse_y = self.game.cube.cube_y_min+8
    def choose_placement(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['place']['x']+16 and pyxel.mouse_x > self.obstacles_pos['place']['x'] and pyxel.mouse_y < self.obstacles_pos['place']['y']+16 and pyxel.mouse_y > self.obstacles_pos['place']['y']:
            self.choosen_placement = 'place'
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos['delete']['x']+16 and pyxel.mouse_x > self.obstacles_pos['delete']['x'] and pyxel.mouse_y < self.obstacles_pos['delete']['y']+16 and pyxel.mouse_y > self.obstacles_pos['delete']['y']:
            self.choosen_placement = 'delete'  
    def choose_obstacle(self):
        if self.choosen_placement == 'place':
            for obs in self.obstacles_pos:
                if (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.obstacles_pos[obs]['x']+16 and pyxel.mouse_x > self.obstacles_pos[obs]['x'] and pyxel.mouse_y < self.obstacles_pos[obs]['y']+16 and pyxel.mouse_y > self.obstacles_pos[obs]['y']):
                    if (not obs == 'place') and (not obs == 'delete'):
                        self.choosen_obstacles = obs


    def editor_init(self):
        if not self.initialisation:
            self.obstacles_temp, self.end_of_level, self.difficulty = self.game.level.get_lvl_data()
            self.initialisation = True
    def place_obstacle(self):
        if self.no_place_obstacle < 2:
            return
        if not self.in_choosing_difficulty and self.choosen_placement == 'place' and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_y-16 <= self.game.cube.cube_y_min and not (pyxel.mouse_x < self.game.screen_x-11+8 and pyxel.mouse_x > self.game.screen_x-43-8 and pyxel.mouse_y < 20+10+8 and pyxel.mouse_y > 20-8) and not (pyxel.mouse_x < self.game.screen_x-4+8 and pyxel.mouse_x > self.game.screen_x-48-8 and pyxel.mouse_y < 8+10+8 and pyxel.mouse_y > 10-8):
            self.obstacles_temp.append({"x": self.mouse_x-8+self.camera_x, "y": self.mouse_y-8, "type": self.choosen_obstacles})
    def remove_obstacle(self):
        if self.choosen_placement == 'delete' and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for obstacle in self.obstacles_temp:
                obstacle_x = obstacle['x']-self.camera_x
                obstacle_y = obstacle['y']-self.camera_y
                if pyxel.mouse_x >= obstacle_x and pyxel.mouse_x <= obstacle_x + 16 and pyxel.mouse_y >= obstacle_y and pyxel.mouse_y <= obstacle_y + 16:
                    self.obstacles_temp.remove(obstacle)
                    return
                    

    def write_json(self, file, data):
        with open (file, "w") as f:
            data = {"level_length": self.end_of_level, 'difficulty': self.difficulty, "obstacles": data}
            json.dump(data, f, indent=4)

    def saving(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.game.screen_x-4 and pyxel.mouse_x > self.game.screen_x-48 and pyxel.mouse_y < 8+10 and pyxel.mouse_y > 10:
            self.write_json(self.game.levels[self.game.level.current_level], self.obstacles_temp)
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.game.screen_x-11 and pyxel.mouse_x > self.game.screen_x-43 and pyxel.mouse_y < 20+10 and pyxel.mouse_y > 20:
            self.save_as_text = True


    #Difficulty
    def choose_difficulty(self):
        if not self.in_choosing_difficulty:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.game.screen_x-1 and pyxel.mouse_x > self.game.screen_x-19 and pyxel.mouse_y < self.game.screen_y-1 and pyxel.mouse_y > self.game.screen_y-19:
                self.in_choosing_difficulty = True
        if self.in_choosing_difficulty:
            for diff in self.difficulty_pos:
                if (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.difficulty_pos[diff]['x']+16 and pyxel.mouse_x > self.difficulty_pos[diff]['x'] and pyxel.mouse_y < self.difficulty_pos[diff]['y']+16 and pyxel.mouse_y > self.difficulty_pos[diff]['y']):
                    self.difficulty = diff

            #Quit
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and pyxel.mouse_x < self.game.screen_x/2-60+16 and pyxel.mouse_x > self.game.screen_x/2-60 and pyxel.mouse_y < self.game.screen_y/2-77+16 and pyxel.mouse_y > self.game.screen_y/2-77:
                self.in_choosing_difficulty = False

    def draw_choose_difficulty(self):
        if self.in_choosing_difficulty:
            pyxel.rect(self.game.screen_x/2-60, self.game.screen_y/2-60, 120, 80, 5)
            pyxel.rectb(self.game.screen_x/2-60, self.game.screen_y/2-60, 120, 80, 10)


            pyxel.rect(self.difficulty_pos[self.difficulty]['x']-1, self.difficulty_pos[self.difficulty]['y']-1, 18, 18, 2)
            for diff in self.difficulty_pos:
                pyxel.blt(self.difficulty_pos[diff]['x'], self.difficulty_pos[diff]['y'], self.game.pyxres.difficulty[diff]['image'], self.game.pyxres.difficulty[diff]['x'], self.game.pyxres.difficulty[diff]['y'], self.game.pyxres.difficulty[diff]['width'], self.game.pyxres.difficulty[diff]['height'], 0)

            #Quit
            pyxel.blt(self.game.screen_x/2-60, self.game.screen_y/2-77, 1, 48, 0, 16, 16,0)




    def move_camera(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.camera_x = self.end_of_level-self.game.screen_x+50
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.camera_x = 0
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.camera_x += 10
        if pyxel.btn(pyxel.KEY_LEFT):
            if not self.camera_x == 0:
                self.camera_x -= 10


    def draw_obstacles(self):
        for obstacle in self.obstacles_temp:
            if obstacle['x']-self.camera_x < self.game.screen_x:
                pyxel.blt(obstacle['x']-self.camera_x, obstacle['y'], self.game.pyxres.obstacles[obstacle['type']]['image'], self.game.pyxres.obstacles[obstacle['type']]['x'], self.game.pyxres.obstacles[obstacle['type']]['y'], self.game.pyxres.obstacles[obstacle['type']]['width'], self.game.pyxres.obstacles[obstacle['type']]['height'], 0)
                

        #Finish line
        if len(self.obstacles_temp) > 0:
            self.end_of_level = max(obstacle['x'] for obstacle in self.obstacles_temp)+25
            if self.end_of_level-self.camera_x < self.game.screen_x:
                pyxel.line(self.end_of_level-self.camera_x, 0, self.end_of_level-self.camera_x, self.game.cube.cube_y_min+16, 4)
    
    def draw_placement_to_choose(self):
        pyxel.blt(self.obstacles_pos['place']['x'], self.obstacles_pos['place']['y'], 1, 104, 0, 16, 16, 0)
        pyxel.blt(self.obstacles_pos['delete']['x'], self.obstacles_pos['delete']['y'], 1, 120, 0, 16, 16, 0)
        pyxel.rectb(self.obstacles_pos[self.choosen_placement]['x']-1, self.obstacles_pos[self.choosen_placement]['y']-1, 18, 18,2)
    
    def draw_obstacles_to_choose(self):
        for obstacle in self.game.pyxres.obstacles:
            pyxel.blt(self.obstacles_pos[obstacle]['x'], self.obstacles_pos[obstacle]['y'], self.game.pyxres.obstacles[obstacle]['image'], self.game.pyxres.obstacles[obstacle]['x'], self.game.pyxres.obstacles[obstacle]['y'], self.game.pyxres.obstacles[obstacle]['width'], self.game.pyxres.obstacles[obstacle]['height'], 0)

        #Choosen
        if self.choosen_placement == 'place' :
            pyxel.rectb(self.obstacles_pos[self.choosen_obstacles]['x']-2, self.obstacles_pos[self.choosen_obstacles]['y']-2, 20, 20, 10)

    def editor_update(self):
        if self.in_editor:
            self.editor_init()
            self.no_place_obstacle += 1
            self.choose_placement()
            self.choose_obstacle()
            #Save
            self.saving()
            self.save_as()

            self.mouse_pos()
            self.move_camera()
            self.place_obstacle()
            self.remove_obstacle()

            #Difficulty
            self.choose_difficulty()

            #Quit editor
            self.quit_editor()

    def editor_draw(self):
        if self.in_editor:
            pyxel.cls(1)
            
            #Sol blanc
            pyxel.rect(0, self.game.cube.cube_y_min+16, self.game.screen_x, self.game.screen_y, 7)

            self.draw_obstacles_to_choose()
            self.draw_placement_to_choose()
            self.draw_obstacles()
            
            #Save Level
            pyxel.rect(self.game.screen_x-48, 8, 44, 10, 10)
            pyxel.text(self.game.screen_x-45, 10, "Save Level", 0)
            #Save As
            pyxel.rect(self.game.screen_x-43, 20, 32, 10, 10)
            pyxel.text(self.game.screen_x-40, 22, "Save As", 0)
            #Camera
            pyxel.text(self.game.screen_x/2+50, 5, f"Camera: {self.camera_x}",7)

            pyxel.text(30, 5, f"Obstacle choisis: {self.choosen_obstacles}", 7)
            pyxel.text(self.game.screen_x-65, self.game.cube.cube_y_min+22, "Fleches: Camera", 0)

            #Difficulty
            self.draw_choose_difficulty()

            #Obstacle on mouse
            if self.choosen_placement == 'place' and not self.in_choosing_difficulty:
                pyxel.blt(self.mouse_x-8, self.mouse_y-8, self.game.pyxres.obstacles[self.choosen_obstacles]['image'], self.game.pyxres.obstacles[self.choosen_obstacles]['x'], self.game.pyxres.obstacles[self.choosen_obstacles]['y'], self.game.pyxres.obstacles[self.choosen_obstacles]['width'], self.game.pyxres.obstacles[self.choosen_obstacles]['height'], 0)

            self.draw_save_as()

            #Difficulté du niveau
            diff = self.difficulty if self.difficulty in self.game.pyxres.difficulty else 'NA'
            pyxel.rect(self.game.screen_x-19, self.game.screen_y-19, 18, 18, 1)
            pyxel.blt(self.game.screen_x-18, self.game.screen_y-18, self.game.pyxres.difficulty[diff]['image'], self.game.pyxres.difficulty[diff]['x'], self.game.pyxres.difficulty[diff]['y'], self.game.pyxres.difficulty[diff]['width'], self.game.pyxres.difficulty[diff]['height'], 0)  

            #Bouton pour revenir au menu
            pyxel.blt(5, 5, 1, 48, 0, 16, 16,0)
