# This file contains the Game class.
class Game:
    def __init__(self, grid_size, difficulty, score, lives):
        self.id = None
        self.grid_size = grid_size
        self.difficulty = difficulty
        self.score = score
        self.lives = lives
        self.life_orb = None
        self.life_orb_active = None
        self.player = None
        self.guards = []
        self.door = None
        self.game_over = False
        self.was_paused = False
