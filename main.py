from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from game import Game
import pygame


pygame.init()
pygame.display.set_caption('2048 by Nick Sciarretta')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.Font(None, 50)

game_over_text = font.render('Game Over!', True, (20, 20, 20))
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (300, 30)

new_game_text = font.render('New Game', True, (20, 20, 20))
new_game_rect = new_game_text.get_rect()
new_game_rect.center = (300, 560)

game = Game()
running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT: running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if new_game_rect.collidepoint((x, y)): game.new_game()

        elif event.type == pygame.KEYDOWN and not game.game_over:
            if   event.key == pygame.K_UP:    game.move(-1, 0)
            elif event.key == pygame.K_DOWN:  game.move( 1, 0)
            elif event.key == pygame.K_LEFT:  game.move( 0,-1)
            elif event.key == pygame.K_RIGHT: game.move( 0, 1)
                    
    game.draw(screen)

    score_text = font.render(f'Score: {game.score}', True, (20, 20, 20))
    score_rect = score_text.get_rect()

    score_rect.center = (300, 75)
    screen.blit(score_text, score_rect)

    screen.blit(new_game_text, new_game_rect)

    if game.game_over: screen.blit(game_over_text, game_over_rect)

    pygame.display.update()

pygame.quit()