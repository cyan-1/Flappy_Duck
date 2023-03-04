import pygame
from sys import exit
from random import randint
from player import Player
from obstacle import Obstacle
from functions import display_score
from functions import collision_sprite

pygame.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Flappy Duck')
clock = pygame.time.Clock()
font = pygame.font.Font('font/Pixeltype.ttf',50)
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
        game_active = collision_sprite(player, obstacle_group)

        # Score
        score = display_score(screen, score, obstacle_group, font, player)

    else:
        screen.fill('#78adad')
        screen.blit(player_stand, player_stand_rect)

        game_name = font.render('Flappy Duck', False, '#00ffff')
        game_name_rect = game_name.get_rect(center = (400,80))

        game_message = font.render('Press space to start', False, '#00ffff')
        game_message_rect = game_message.get_rect(center=(400, 320))

        score_message = font.render(f'Your Score {score}', False, '#00ffff')
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name, game_name_rect)

        if score == 0: screen.blit(game_message, game_message_rect)
        else: screen.blit(score_message, score_message_rect)
            
    pygame.display.update()
    clock.tick(60)