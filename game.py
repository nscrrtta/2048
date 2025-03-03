from constants import *
from tile import Tile
import pygame
import random


class Game:

    def __init__(self):
        self.rows = [0,1,2,3]
        self.cols = [0,1,2,3]
        self.new_game()

    
    def new_game(self):
        self.grid = [[Tile(row, col) for col in range(4)] for row in range(4)]

        for row in self.grid:
            for tile in row: tile.grid = self.grid
        
        self.game_over = False
        self.score = 0

        self.add_tile(True)
        self.add_tile(True)

        # For sliding animation
        self.slide_steps = 0

    
    def add_tile(self, first_tile=False):
        while True:
            row = random.randint(0, 3)
            col = random.randint(0, 3)

            tile = self.grid[row][col]
            if tile.value == 0: break
        
        tile.value = tile.slide_value = \
        random.choice([2] * 6 + [4] * 4)

        if not first_tile: self.check_game_over()

        # Animate new tile growing
        tile.tile_size = 0

    
    def check_game_over(self):
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if self.can_move(dr, dc): break
        else: self.game_over = True


    def move(self, dr: int, dc: int):
        # Make sure sliding animation from previous move is complete
        if self.slide_steps > 0: return
        
        # Make sure at least one tile can move this direction
        if self.can_move(dr, dc) is False:
            return
        
        # Change the order in which tiles are yielded
        self.rows = [3,2,1,0] if dr == 1 else [0,1,2,3]
        self.cols = [3,2,1,0] if dc == 1 else [0,1,2,3]

        for tile in self.yield_tiles():
            tile.slide_value = tile.value
            tile.tile_size = TILE_SIZE
            tile.move(dr, dc)

        # Animate tiles sliding
        self.slide_steps = 1


    def can_move(self, dr: int, dc: int) -> bool:
        for tile in self.yield_tiles():
            if tile.value == 0: continue
            if tile.can_move(dr, dc): return True
        return False

        
    def merge_tiles(self):
        for tile in self.yield_tiles():
            if tile.merged:
                self.score += tile.value
                tile.merged = False

                # Animate tiles merging
                tile.tile_size = TILE_SIZE + 1
    

    def yield_tiles(self):
        for row in self.rows:
            for col in self.cols:
                yield self.grid[row][col]

    
    def draw(self, screen: pygame.Surface):
        screen.fill((241, 243, 226))
        
        rect = pygame.Rect(LEFT, TOP, BOARD_SIZE, BOARD_SIZE)
        pygame.draw.rect(screen, (180, 170, 150), rect, border_radius=4)

        for tile in self.yield_tiles():
            rect = pygame.Rect(
                tile.center_x - TILE_SIZE // 2,
                tile.center_y - TILE_SIZE // 2,
                TILE_SIZE,
                TILE_SIZE)
            pygame.draw.rect(screen, (198, 190, 169), rect, border_radius=4)
            tile.draw(screen, self.slide_steps)

        # Last step in sliding animation
        if self.slide_steps == SLIDE_STEPS:
            self.slide_steps = 0
            self.merge_tiles()
            self.add_tile()
            
        elif self.slide_steps > 0:
            self.slide_steps += 1
