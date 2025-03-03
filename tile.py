from constants import *
import pygame


class Tile:

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col

        self.value = 0
        self.merged = False

        self.grid: list[list[Tile]] = []

        # For drawing
        self.center_x = TILE_SIZE * (col + 0.5) + TILE_SPACING * (col + 1) + LEFT
        self.center_y = TILE_SIZE * (row + 0.5) + TILE_SPACING * (row + 1) + TOP

        # For growing animation
        self.tile_size = TILE_SIZE

        # For sliding animation
        self.dx = self.dy = 0
        self.slide_value = 0

    
    def move(self, dr: int, dc: int):
        val = self.value     
        curr_tile = self

        while val > 0 and curr_tile.can_move(dr, dc):
            prev_tile = curr_tile
            curr_tile = curr_tile.get_next(dr, dc)

            if curr_tile.value == prev_tile.value \
            and curr_tile.merged is False:
                curr_tile.merged = True

            if curr_tile.value == 0 or curr_tile.merged:
                curr_tile.value += prev_tile.value
                prev_tile.value = 0

            if curr_tile.merged: break

        self.dx = curr_tile.col - self.col
        self.dy = curr_tile.row - self.row

    
    def can_move(self, dr: int, dc: int):
        if self.row + dr not in range(4) \
        or self.col + dc not in range(4): return False

        next_tile = self.get_next(dr, dc)

        return next_tile.merged is False \
            and next_tile.value in [self.value, 0]
    

    def get_next(self, dr: int, dc: int):
        return self.grid[self.row + dr][self.col + dc]
    

    def draw(self, screen: pygame.Surface, slide_steps: int):
        # Center x, y coordinates
        x = self.center_x + self.dx * slide_steps * SLIDE_SPEED
        y = self.center_y + self.dy * slide_steps * SLIDE_SPEED

        # If tile is sliding, use self.slide_value
        value = self.slide_value if slide_steps > 0 else self.value
        tile_color, font_color, font_size = TILE_APPEARANCE[value]

        rect = pygame.Rect(
            x - self.tile_size // 2,
            y - self.tile_size // 2,
            self.tile_size,
            self.tile_size)
        pygame.draw.rect(screen, tile_color, rect, border_radius=4)

        font_size *= self.tile_size / TILE_SIZE
        font = pygame.font.Font(None, int(font_size))

        text_surf = font.render(str(value), True, font_color)
        text_rect = text_surf.get_rect()

        text_rect.center = (x, y)
        screen.blit(text_surf, text_rect)
        
        # Animate new tile growing
        if self.tile_size < TILE_SIZE:
            self.tile_size += 2

        # Animate tile merging
        elif TILE_SIZE < self.tile_size < TILE_SIZE + 20:
            self.tile_size += 1
        
        # Standard tile size
        else: self.tile_size = TILE_SIZE
