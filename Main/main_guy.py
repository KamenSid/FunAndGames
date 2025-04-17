from settings import *
from particle_effects import *
from spells import *
from inventory import Inventory, Item


class Main_guy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.screen = screen
        self.position = position
        # Animation
        self.idle_frames = Animation(idle_frames, 5)
        self.walk_frames = Animation(walk_frames, 3)
        self.jump_frames = Animation(jump_frames, 5)
        self.hit_frames = Animation(hit_frames, 4)
        self.current_animation = self.idle_frames
        self.image = self.current_animation.get_frame()
        self.state = "idile"
        # Collision
        self.rect = self.image.get_rect(topleft=position)
        # Movement
        self.direction = [0, 0]
        self.acceleration = 0.8
        self.friction = 0.8
        self.velocity = [0, 0]
        self.gravity = 1.5
        self.on_ground = False
        self.been_on_ground = False
        self.right = True
        self.hitting = False
        # Visuals
        self.frame = frame_one
        self.circles_list = []
        self.spells_list = []
        # Stats
        self.stats = Stats(200, 100, 0, 0)
        self.hit_speed = 60
        self.equipped = []
        self.invent = []
        self.inventory = Inventory(self, 5, self.invent)
        self.inventory.build()
        self.vision_radius = 250


    # def check_collision(self, level):
    #     left = int(self.rect.left // TILE_SIZE)
    #     right = int(self.rect.right // TILE_SIZE)
    #     top = int(self.rect.top // TILE_SIZE)
    #     bottom = int(self.rect.bottom // TILE_SIZE)
    #
    #     # Iterate only through the relevant tiles
    #     self.on_ground = False
    #     for row in range(top, bottom + 1):
    #         for col in range(left, right + 1):
    #             # Ensure grid indices are within bounds
    #             if 0 <= row < len(level.tile_grid) and 0 <= col < len(level.tile_grid[row]):
    #                 tile = level.tile_grid[row][col]
    #                 if tile and tile.solid:
    #                     # Check for collision
    #                     if pygame.sprite.collide_rect(self, tile):
    #                         self.on_ground = True
    #                         self.velocity[1] = 0  # Stop vertical velocity
    #                         self.position[1] = tile.rect.top - self.rect.height + 4
    #                         return
    def check_collision(self, level):
        left = int(self.rect.left // TILE_SIZE)
        right = int(self.rect.right // TILE_SIZE)
        top = int(self.rect.top // TILE_SIZE)
        bottom = int(self.rect.bottom // TILE_SIZE)

        self.on_ground = False

        for row in range(top, bottom + 1):
            for col in range(left, right + 1):
                if 0 <= row < len(level.tile_grid) and 0 <= col < len(level.tile_grid[row]):
                    tile = level.tile_grid[row][col]
                    if tile and tile.solid:
                        if self.rect.colliderect(tile.rect) and not self.on_ground:
                            # Simple bottom collision check (falling onto a tile)
                            if self.velocity[1] >= 0 and self.rect.bottom >= tile.rect.top:
                                self.on_ground = True
                                self.velocity[1] = 0  # Stop vertical velocity
                                self.position[1] = tile.rect.top - self.rect.height + 4
                                return
                            # Hitting head on a tile
                            elif self.velocity[1] < 0 and self.rect.top >= tile.rect.bottom - 20:
                                self.rect.top = tile.rect.bottom
                                self.position[1] = self.rect.y + 5
                                self.velocity[1] = 0



    def update(self, keys, level, enemies):
        acceleration_vector = [0, 0]

        # Handle input
        if keys[pygame.K_LEFT]:
            acceleration_vector[0] = -self.acceleration
        if keys[pygame.K_RIGHT]:
            acceleration_vector[0] = self.acceleration
        if keys[pygame.K_UP] and self.on_ground:
            self.on_ground = False
            acceleration_vector[1] = -self.acceleration * 20

        if keys[pygame.K_DOWN] and not self.on_ground:
            acceleration_vector[1] = self.acceleration
        if keys[pygame.K_g]:
            self.hit()

        if keys[pygame.K_i]:
            self.inventory.draw()


        self.check_collision(level)
        # for land in lands:
        #     if pygame.sprite.collide_rect(self, land):
        #         self.on_ground = True
        #         self.velocity[1] = 0  # Stop downward movement when landing
        #         self.position[1] = land.rect.top - self.rect.height + 4
        #         break
        #     else:
        #         self.on_ground = False


        self.been_on_ground = self.on_ground

        # Handle animation
        if abs(self.velocity[0]) > 0.1 and self.on_ground:
            self.state = "walk"
        elif not self.on_ground:
            self.state = "jump"
        else:
            self.state = "idle"

        if self.state == "walk":
            self.current_animation = self.walk_frames
        elif self.state == "jump":
            self.current_animation = self.jump_frames
        else:
            self.current_animation = self.idle_frames

        if self.velocity[0] > 0:
            self.right = True
        elif self.velocity[0] < 0:
            self.right = False

        self.current_animation.update()
        self.image = self.current_animation.get_frame()

        if not self.right:
            self.image = pygame.transform.flip(self.image, True, False)

        if not self.on_ground:
            acceleration_vector[1] += self.gravity
        else:
            self.velocity[1] = 0

        self.velocity[0] += acceleration_vector[0]
        self.velocity[1] += acceleration_vector[1]

        self.velocity[0] *= self.friction
        self.velocity[1] *= self.friction

        # Update position based on velocity
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.rect.topleft = self.position


    def draw(self, rect):
        self.rect = rect
        screen.blit(self.image, self.rect.topleft)


    def effect(self):
        if self.circles_list.__len__() <= 10:
            if random.random() < 0.4:
                for _ in range(10):
                    circle = Water_drop([self.position[0] + 50, self.position[1] + 125], screen)
                    self.circles_list.append(circle)

        for item in self.inventory.items:
            for k, v in item.stats.items():
                if k == "speed":
                    self.acceleration += v


    def hit(self):

        if not self.spells_list:
            self.current_animation = self.hit_frames
            teleport = Spell([self.position[0], self.position[1] - 130])
            self.spells_list.append(teleport)
            for _ in range(500):
                if random.random() < 0.2:
                    effect = Snow_flake([(self.position[0] + 40) + random.randint(-50, 50), self.position[1] + 10],
                                        self.screen)
                    self.circles_list.append(effect)

