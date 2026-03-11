import pyxel

class Pyxres:
    def __init__(self, game):
        self.cube = {
            'basic': {
                'image': 0,
                'x': 0,
                'y': 0,
                'width': 16,
                'height': 16
            },
            '2': {
                'image': 0,
                'x': 16,
                'y': 0,
                'width': 16,
                'height': 16
            },
            '3': {
                'image': 0,
                'x': 32,
                'y': 0,
                'width': 16,
                'height': 16
            },
            '4': {
                'image': 0,
                'x': 48,
                'y': 0,
                'width': 16,
                'height': 16
            }
        }

        self.obstacles = {
            'coins': {
                'image': 2,
                'x': 0,
                'y': 32,
                'width': 16,
                'height': 16
            },
            'cube portal': {
                'image': 0,
                'x': 0,
                'y': 64,
                'width': 16,
                'height': 16
            },
            'ball portal': {
                'image': 0,
                'x': 16,
                'y': 64,
                'width': 16,
                'height': 16
            },
            'spike': {
                'image': 0,
                'x': 16,
                'y': 16,
                'width': 16,
                'height': 16
            },
            'turned spike': {
                'image': 0,
                'x': 16,
                'y': 32,
                'width': 16,
                'height': 16
            },
            'block': {
                'image': 0,
                'x': 32,
                'y': 16,
                'width': 16,
                'height': 16
            },
            'mur': {
                'image': 0,
                'x': 0,
                'y': 16,
                'width': 16,
                'height': 16
            },
            'orb': {
                'image': 0,
                'x': 48,
                'y': 16,
                'width': 16,
                'height': 16
            },
            'jump pad': {
                'image': 0,
                'x': 0,
                'y': 32,
                'width': 16,
                'height': 16
            },
            'gravity orb': {
                'image': 0,
                'x': 48,
                'y': 32,
                'width': 16,
                'height': 16
            },
            'small spike': {
                'image': 0,
                'x': 16,
                'y': 48,
                'width': 16,
                'height': 16
            },
            'small turned spike': {
                'image': 0,
                'x': 0,
                'y': 48,
                'width': 16,
                'height': 16
            },
            'gravity pad': {
                'image': 0,
                'x': 32,
                'y': 32,
                'width': 16,
                'height': 16
            },
        }

        self.difficulty = {
            'NA': {
                'image': 2,
                'x': 0,
                'y': 64,
                'width': 16,
                'height': 16
            },
            'normal': {
                'image': 2,
                'x': 0,
                'y': 48,
                'width': 16,
                'height': 16
            },
            'hard': {
                'image': 2,
                'x': 16,
                'y': 48,
                'width': 16,
                'height': 16
            },
            'insane': {
                'image': 2,
                'x': 32,
                'y': 48,
                'width': 16,
                'height': 16
            },
            'demon': {
                'image': 2,
                'x': 55,
                'y': 45,
                'width': 18,
                'height': 18
            }
        }