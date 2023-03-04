import pygame

def display_score(screen, score, obstacle_group, font, player):

    # Count how many pipes the player has passed through
    passed_pipes = [pipe for pipe in obstacle_group.sprites() if pipe.rect.right < player.sprite.rect.left and not pipe.scored]
    num_passed_pipes = len(passed_pipes)

    # Update the score and mark the pipes as scored
    if num_passed_pipes > 0:
        score += 1
        for pipe in passed_pipes:
            pipe.scored = True

    # Render the score and number of pipes passed
    score_surface = font.render(f"Score: {score}", True, '#00ffff')
    screen.blit(score_surface, (10, 10))
    return score


def collision_sprite(player, obstacle_group):
    if pygame.sprite.spritecollide(player.sprite, obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True
