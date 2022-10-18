import re
from Character import Character

class Player(Character):
    def __init__(self, width, height, image_path, x_max, y_max, position_increment, sound_path):
        super().__init__(width, height, image_path, x_max, y_max, position_increment, sound_path)
        self.life = 3
        self.level = 1
        
    def get_level(self): return self.level
    
    def get_life(self): return self.life
    
    def set_level(self): self.level += 1
    
    def set_life(self): self.life -= 1
    
    def is_dead(self): return self.life == 0
    
    def reset(self):
        self.life = 3
        self.level = 1
