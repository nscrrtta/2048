from random import randint, choice
import pygame


pygame.init()
font = pygame.font.Font(None, 50)
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('2048 by Nick Sciarretta')

# Game Over text
go_surf = font.render('Game Over!', True, (20, 20, 20))
go_rect = go_surf.get_rect()
go_rect.center = (300, 30)

# New Game text
ng_surf = font.render('New Game', True, (20, 20, 20))
ng_rect = ng_surf.get_rect()
ng_rect.center = (300, 560)

tiles = [[0 for _ in range(4)] for _ in range(4)]

# tile colour, font colour, font size
tile_appearance = {
    2:     [(238, 228, 218), (119, 110, 101), 75],
    4:     [(237, 224, 200), (119, 110, 101), 75],
    8:     [(242, 177, 121), (249, 246, 242), 75],
    16:    [(245, 149,  99), (249, 246, 242), 75],
    32:    [(246, 124,  95), (249, 246, 242), 75],
    64:    [(246,  94,  59), (249, 246, 242), 75],
    128:   [(237, 207, 114), (249, 246, 242), 65],
    256:   [(237, 204,  97), (249, 246, 242), 65],
    512:   [(237, 200,  80), (249, 246, 242), 65],
    1024:  [(237, 197,  63), (249, 246, 242), 50],
    2048:  [(237, 194,  46), (249, 246, 242), 50],
    4096:  [(243, 119, 137), (249, 246, 242), 50],
    8192:  [(236,  89, 107), (249, 246, 242), 50],
    16384: [(243,  84,  81), (249, 246, 242), 40],
    32768: [(124, 191, 225), (249, 246, 242), 40],
    65536: [(109, 174, 234), (249, 246, 242), 40],
    131072:[(49,  142, 201), (249, 246, 242), 35]
}


def move_tiles(dir: str, mtype: str, i=0) -> bool:

    if mtype == 'shift' and i > 2: return False

    row_vals, col_vals = {
        'up':    ([1,  4,  1, -1], [0,  4,  1,  0]),
        'down':  ([2, -1, -1,  1], [0,  4,  1,  0]),
        'left':  ([0,  4,  1,  0], [1,  4,  1, -1]),
        'right': ([0,  4,  1,  0], [2, -1, -1,  1]) 
    }[dir]

    row_start, row_stop, row_step, dr = row_vals
    col_start, col_stop, col_step, dc = col_vals

    for row in range(row_start, row_stop, row_step):
        for col in range(col_start, col_stop, col_step):
        
            curr_tile = tiles[row][col]
            next_tile = tiles[row+dr][col+dc]

            if mtype == 'valid':
                if curr_tile == 0: continue
                if next_tile == 0: return True
                if next_tile == curr_tile: return True

            elif mtype == 'shift':
                if next_tile > 0: continue
                tiles[row][col] = 0
                tiles[row+dr][col+dc] = curr_tile

            elif mtype == 'merge':
                if curr_tile != next_tile: continue
                tiles[row][col] = 0
                tiles[row+dr][col+dc] = curr_tile*2
                global score; score += curr_tile*2

    if mtype == 'valid': return False
    elif mtype == 'shift': move_tiles(dir, mtype, i+1)


def check_game_over():

    global game_over

    game_over = not(
        move_tiles('up',   'valid') or
        move_tiles('down', 'valid') or
        move_tiles('left', 'valid') or
        move_tiles('right','valid')
    )


def add_tile():

    # Randomly pick a 2 or 4 (weighted)
    rand_tiles = [2]*6 + [4]*4

    # Randomly pick a spot on board
    while True:
        i,j = randint(0,3), randint(0,3)
        if tiles[i][j] == 0: break

    tiles[i][j] = choice(rand_tiles)


def new_game():

    global score, game_over

    # Reset all tiles to 0
    for i in range(4): tiles[i] = [0,0,0,0]

    # Add two random tiles
    add_tile(); add_tile()

    score = 0
    game_over = False


def draw():

    screen.fill((241, 243, 226))

    # Draw board background
    rect = pygame.Rect(90, 100, 420, 420)
    pygame.draw.rect(screen, (180,170,150), rect, border_radius=4)

    # Draw tiles and numbers
    for row in range(4):
        for col in range(4):

            tile_val = tiles[row][col]
            if tile_val == 0: tile_colour = (198, 190, 169)
            else: tile_colour, font_colour, font_size = tile_appearance[tile_val]

            left = 102*(col+1)
            top  = 102*(row+1)+10

            rect = pygame.Rect(left, top, 90, 90)
            pygame.draw.rect(screen, tile_colour, rect, border_radius=4)

            if tile_val == 0: continue

            font = pygame.font.Font(None, font_size)
            text_surf = font.render(f'{tile_val}', True, font_colour)
            text_rect = text_surf.get_rect()
            text_rect.center = (left+45, top+45)
            screen.blit(text_surf, text_rect)

    # Draw score
    font = pygame.font.Font(None, 50)
    score_surf = font.render(f'Score: {score}', True, (20, 20, 20))
    score_rect = score_surf.get_rect()
    score_rect.center = (300, 75)
    screen.blit(score_surf, score_rect)

    # Draw game over
    if game_over: screen.blit(go_surf, go_rect)

    # Draw new game button
    screen.blit(ng_surf, ng_rect)


new_game()
running = True

while running:

    x,y = pygame.mouse.get_pos()

    for event in pygame.event.get():

        if event.type == pygame.QUIT: running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if ng_rect.collidepoint((x,y)): new_game()

        elif event.type == pygame.KEYDOWN and not game_over:

            if   event.key == pygame.K_UP:    dir = 'up'
            elif event.key == pygame.K_DOWN:  dir = 'down'
            elif event.key == pygame.K_LEFT:  dir = 'left'
            elif event.key == pygame.K_RIGHT: dir = 'right'
            else: continue

            if not move_tiles(dir, 'valid'): continue

            for m in ['shift', 'merge', 'shift']: move_tiles(dir, m)
            add_tile(); check_game_over()
                    
    draw()
    pygame.display.update()

pygame.quit()
