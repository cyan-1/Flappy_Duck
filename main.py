import pygame
from sys import exit
from random import randint

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
        self.gravity += 0.5 # gravity speed
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

def display_score(score, obstacle_group):
    global screen, font, white_color

    # Count how many pipes the player has passed through
    passed_pipes = [pipe for pipe in obstacle_group.sprites() if pipe.rect.right < player.sprite.rect.left and not pipe.scored]
    num_passed_pipes = len(passed_pipes)

    # Update the score and mark the pipes as scored
    if num_passed_pipes > 0:
        score += 1
        for pipe in passed_pipes:
            pipe.scored = True

    # Render the score and number of pipes passed
    score_surface = test_font.render(f"Score: {score}", True, '#00ffff')
    screen.blit(score_surface, (10, 10))
    return score

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Flappy Duck')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf',50)
game_active = False
start_time = 0
score = 0

# Groups 
player = pygame.sprite.GroupSingle()
player.add(Player())

pipe1 = Obstacle('pipe_up')
pipe2 = Obstacle('pipe_down')
pipe2.rect.x = pipe1.rect.x
obstacle_group = pygame.sprite.Group()

# Background
bg_surface = pygame.image.load('imgs/background.png').convert()

#intro screen
player_stand = pygame.image.load('imgs/duck1.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center = (400, 200))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000) #pipe spawn speed

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active == False and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_active=True
            #start_time = int(pygame.time.get_ticks() / 1000)
            score = 0

        if game_active: 
            if event.type == obstacle_timer:
                pipe1 = Obstacle('pipe_down')
                pipe2 = Obstacle('pipe_up')
                distance_between_pipes = 150  # change if needed
                pipe1.rect.x = 800  # spawn pipe1 off the right edge of the screen
                pipe1.rect.y = randint(50, 200) - pipe1.rect.height # spawn pipe1 at a random height
                pipe2.rect.x = pipe1.rect.x
                pipe2.rect.y = pipe1.rect.y + pipe1.rect.height + distance_between_pipes  # spawn pipe2 below pipe1
                obstacle_group.add(pipe1, pipe2)

    if game_active:  
        screen.blit(bg_surface, (0,0))

        # Player
        player.draw(screen)
        player.update()

        # Obstacle
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision
        game_active = collision_sprite()

        # Score
        score = display_score(score, obstacle_group)

    else:
        screen.fill('#78adad')
        screen.blit(player_stand, player_stand_rect)

        game_name = test_font.render('Flappy Duck', False, '#00ffff')
        game_name_rect = game_name.get_rect(center = (400,80))

        game_message = test_font.render('Press space to start', False, '#00ffff')
        game_message_rect = game_message.get_rect(center=(400, 320))

        score_message = test_font.render(f'Your Score {score}', False, '#00ffff')
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name, game_name_rect)

        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)
            
    pygame.display.update()
    clock.tick(60)