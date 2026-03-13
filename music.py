import pyxel

class Music:
    def __init__(self, game):
        self.game = game

        self.music_position = None
        self.sec = 0
        self.sec_list = [0] * 64
        self.sound = 0
        self.death_sound_var = False

    def resume_song(self):
        self.sec = 0
        for seconds in self.sec_list:
            self.sec += seconds
        if self.game.level.current_level == 'lvl1':
            pyxel.playm(1, sec=self.sec)
        if self.game.level.current_level == 'lvl2':
            pyxel.playm(2, sec=self.sec)

    def play_song(self):
        if self.game.level.current_level == 'lvl1':
            pyxel.playm(1)
        if self.game.level.current_level == 'lvl2':
            pyxel.playm(2)

    def stop_allsongs(self):
        pyxel.stop()

    def get_song_pos(self):
        self.music_position = pyxel.play_pos(0)
        if self.music_position is not None:
            self.sound, self.sec = self.music_position
            self.sec_list[self.sound] = self.sec


    def death_sound(self):
        if not self.death_sound_var:
            self.stop_allsongs()
            pyxel.play(0, 63)
            self.death_sound_var = True