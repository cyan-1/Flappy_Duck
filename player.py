import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk_1 = pygame.image.load('imgs/duck1.png').convert_alpha()
        player_walk_2 = pygame.image.load('imgs/duck2.png').convert_alpha()
        player_walk_1 = pygame.transform.scale2x(player_walk_1)
        player_walk_2 = pygame.transform.scale2x(player_walk_2)

        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0;

        self.player_jump = pygame.image.load('imgs/duck_jump.png').convert_alpha()
        self.player_jump = pygame.transform.scale2x(self.player_jump)
    
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and self.rect.top >= 0: 
            self.gravity = -5 # player gravity
            keys = [0]

    def apply_gravity(self):
        self.gravity += 0.5 # gravity speed; amount of time for player to fall down
        self.rect.y += self.gravity
        if self.rect.top <=0: self.rect.top = 0
        if self.rect.bottom >= 400: self.rect.bottom = 400

    def animation_state(self):
        if self.rect.bottom < 400:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()