import pygame
from random import randint

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        self.pipe_up = pygame.image.load('imgs/long_pipe.png')
        self.pipe_down = pygame.transform.rotozoom(self.pipe_up, 180, 2)

        if type == 'pipe_down': 
            self.frame = self.pipe_down
        else:
            self.pipe_up = pygame.transform.scale2x(self.pipe_up)  
            self.frame = self.pipe_up 

        self.animation_index = 0
        self.image = self.frame
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), 0))
        self.scored = False
    def animation_state(self):
        self.image = self.frame

    def update(self):
        self.animation_state() 
        self.rect.x -= 10 # pipe speed
        self.destroy()

    def destroy(self):
        if self.rect.x < -100:
            self.kill()