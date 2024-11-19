import pygame
import math


#UTILITY
def load_frames(sprite_sheet, frame_width, frame_height, num_frames):
    frames = []
    for i in range(num_frames):
        frame = sprite_sheet.subsurface(pygame.Rect(i * frame_width, 0, frame_width, frame_height))
        frames.append(frame)
    return frames



SCR_WIDE = 1820
SCR_HEIGHT = 900
screen = pygame.display.set_mode((SCR_WIDE, SCR_HEIGHT))


test_spell_pic = pygame.image.load("../.venv/assets/kya.png").convert_alpha()
test_spell_pic = pygame.transform.scale(test_spell_pic, (115, 115))
test_projectile = pygame.image.load("../.venv/assets/Arcane_Effect_1.png").convert_alpha()
test_projectile = pygame.transform.scale(test_projectile, (50, 50))



inventory_slot_bg = pygame.Surface([20, 20])
inventory_slot_bg.fill("white")
inventory_slot_bg = pygame.transform.scale(inventory_slot_bg, (60, 60))



# MAIN CHARACTER
main_char_image = pygame.image.load("../.venv/assets/hero_wizard.png").convert_alpha()
main_char_image = pygame.transform.scale(main_char_image, (100, 100))
frame_one =  pygame.image.load("../.venv/assets/readyframes_assets_one.png").convert_alpha()
frame_one = pygame.transform.scale(frame_one, (115, 115))

sprite_sheet_walk = pygame.image.load("../.venv/assets/cat/walk.png").convert_alpha()
sprite_sheet_idle = pygame.image.load("../.venv/assets/cat/idle.png").convert_alpha()
sprite_sheet_jump = pygame.image.load("../.venv/assets/cat/jump.png").convert_alpha()
sprite_sheet_hit = pygame.image.load("../.venv/assets/cat/attack.png").convert_alpha()

idle_frames = load_frames(sprite_sheet_idle, 64, 50, 7)
walk_frames = load_frames(sprite_sheet_walk, 64, 50, 7)
jump_frames = load_frames(sprite_sheet_jump, 64, 50, 7)
hit_frames = load_frames(sprite_sheet_hit, 64, 50, 3)

#ENEMIES
test_enemy_idle = pygame.image.load("../.venv/assets/rabit/Rabbit_Idle.png").convert_alpha()
test_enemy_walk = pygame.image.load("../.venv/assets/rabit/Rabbit_Hop.png").convert_alpha()
test_enemy_run = pygame.image.load("../.venv/assets/rabit/Rabbit_Run.png").convert_alpha()
test_enemy_idle_frames = load_frames(test_enemy_idle, 32, 26, 10)
test_enemy_walk_frames = load_frames(test_enemy_walk, 32, 26, 10)
test_enemy_run_frames = load_frames(test_enemy_run, 32, 26, 6)

#ITEMS
item_coin = pygame.image.load("../.venv/assets/items/coin.png").convert_alpha()
item_tome = pygame.image.load("../.venv/assets/items/tome.png").convert_alpha()
item_envelope = pygame.image.load("../.venv/assets/items/envelope.png").convert_alpha()
item_potion_green = pygame.image.load("../.venv/assets/items/potionGreen.png").convert_alpha()
item_potion_blue = pygame.image.load("../.venv/assets/items/potionBlue.png").convert_alpha()

test_item_1_image = item_coin


#Level STUFF

#Tiles

tile_1 =  pygame.image.load("../.venv/assets/tileset/first_tile.png").convert_alpha()
tile_2 =  pygame.image.load("../.venv/assets/tileset/tile_2.png").convert_alpha()
tile_3 =  pygame.image.load("../.venv/assets/tileset/tile_3.png").convert_alpha()
tile_4 =  pygame.image.load("../.venv/assets/tileset/tile_4.png").convert_alpha()
tile_5 =  pygame.image.load("../.venv/assets/tileset/tile_5.png").convert_alpha()
tile_6 =  pygame.image.load("../.venv/assets/tileset/tile_6.png").convert_alpha()
tile_1 = pygame.transform.scale(tile_1, (32, 32))
tile_2 = pygame.transform.scale(tile_2, (32, 32))
tile_3 = pygame.transform.scale(tile_3, (32, 32))
tile_4 = pygame.transform.scale(tile_4, (32, 32))
tile_5 = pygame.transform.scale(tile_5, (32, 32))
tile_6 = pygame.transform.scale(tile_6, (32, 32))

TILE_SIZE = 32
level1_layout = [
    "111111111111111111111111111111111111111111111111111111111",
    "1                                                       1",
    "1                                                       1",
    "1                                                       1",
    "1                                                       1",
    "1                                                       1",
    "1                                                       1",
    "1                                                       1",
    "1                                        111111         1",
    "1                                                       1",
    "1          111111                                       1",
    "1                                                       1",
    "1                         1111111                       1",
    "1                                                       1",
    "1                                                       1",
    "1           111111                                      1",
    "1                                                       1",
    "1                                    1111111            1",
    "1                                                       1",
    "1                                                       1",
    "1                11111111                               1",
    "1                                                       1",
    "1                                111111                 1",
    "1                                                       1",
    "1                     11111111                          1",
    "1                                                       1",
    "1                                                       1",
    "111111111111111111111111111111111111111111111111111111111"
]


class Animation:
    def __init__(self, frames, speed, loop=True):
        self.frames = frames
        self.speed = speed
        self.loop = loop
        self.index = 0
        self.counter = 0
        self.finished = False

    def update(self):
        if self.finished and not self.loop:
            return

        self.counter += 1
        if self.counter >= self.speed:
            self.counter = 0
            self.index += 1


            if self.index >= len(self.frames):
                if self.loop:
                    self.index = 0
                else:
                    self.index = len(self.frames) - 1
                    self.finished = True


    def get_frame(self):
        return self.frames[self.index]


class Stats:
    def __init__(self, helth, mana, speed, gold):
        self.helth = helth
        self.mana = mana
        self.speed = speed
        self.gold = gold


