import random
from camera import Camera
import pygame.sprite
from settings import *

tileset = [tile_1, tile_2, tile_3, tile_4, tile_5, tile_6]


class Tile(pygame.sprite.Sprite):
    def __init__(self, position, solid=True):
        super().__init__()
        self.image = tileset[random.randint(0, 5)]
        self.rect = self.image.get_rect(topleft=position)
        self.solid = solid
        self.blocks_light = True

    def draw(self, screen, rect):
        screen.blit(self.image, rect)


class Surface(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.screen = screen
        self.level_layout = level1_layout
        self.tile_grid = [[None for _ in range(self.level_layout[0].__len__())] for _ in
                          range(self.level_layout.__len__())]
        self.dark_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.camera = Camera(300, 300)

    def build(self):
        for row_index, row in enumerate(self.level_layout):
            for col_index, tile_type in enumerate(row):
                if tile_type == '1':
                    position = (col_index * TILE_SIZE, row_index * TILE_SIZE)
                    tile = Tile(position)
                    self.tile_grid[row_index][col_index] = tile

    def draw(self, players):

        self.camera.update(players[0])
        for row in self.tile_grid:
            for tile in row:
                if tile:
                    adjust_rect = self.camera.apply_rect(tile.rect)
                    tile.draw(self.screen, adjust_rect)

        self.dark_overlay.fill((0, 0, 0, 200))

        for player in players:
            radius = player.vision_radius
            player_rect = self.camera.apply(player)
            self.cast_light(player, radius, self.camera)
            player.draw(player_rect)

        screen.blit(self.dark_overlay, [0, 0])

    def cast_light(self, source, radius, camera):
        MAX_ALFA = 280


        for angle in range(0, 360, 5):  # Calculating the amount of rays
            dx = math.cos(math.radians(angle))
            dy = math.sin(math.radians(angle))
            x, y = [source.position[0] + 25 , source.position[1] + 25 ]

            for i in range(0, radius, 12):
                x += dx * 12
                y += dy * 12
                point = (int(x) + random.randint(-1, 1), int(y) + random.randint(-1, 1))
                # Calculate grid coordinates
                grid_x = int(x // TILE_SIZE)
                grid_y = int(y // TILE_SIZE)
                # Check if the grid coordinates are within bounds
                if 0 <= grid_x < len(self.tile_grid[0]) and 0 <= grid_y < len(self.tile_grid):
                    tile = self.tile_grid[grid_y][grid_x]
                    if tile and tile.blocks_light:  # Stop the ray if a blocking tile is hit
                        break

                distance_from_source = math.sqrt(
                    (x - (source.position[0] + 25)) ** 2 + (y - (source.position[1] + 25)) ** 2)
                alpha = max(50, min(MAX_ALFA, int(MAX_ALFA * (1.3 - distance_from_source / radius))))

                adjusted_point = (point[0] - self.camera.camera.topleft[0], point[1] - self.camera.camera.topleft[1])
                # Draw the light point with gradient
                pygame.draw.circle(self.dark_overlay, (0, 0, 0, MAX_ALFA - alpha), adjusted_point, 15)

    def create_gradient(self, radius):
        surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        center = radius
        for r in range(0, radius + 20):  # Loop from 0 to radius
            alpha = int(150 * (r / radius))  # Alpha increases as `r` increases
            pygame.draw.circle(surface, (0, 0, 0, 170 - alpha), (center + 35, center + 35), radius - r)
        return surface

    def remove_tile(self, tile):
        tile.kill()
