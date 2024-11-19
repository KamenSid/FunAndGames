from settings import *
from particle_effects import Water_drop


class Spell(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.projectile_position = [position[0], position[1]+120]
        self.image = test_spell_pic
        self.projectile = test_projectile
        self.cooldown = 360
        self.position_words = position[:]
        self.rect = self.projectile.get_rect(topleft=self.projectile_position)
        self.effects = []
        self.did_hit = False
        self.name = "teleport"



    def update(self):
        self.projectile_position[0] += 5
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.cooldown < 60:
            self.position_words[1] -= 2
        self.rect.topleft = self.projectile_position

    def hit(self):

        self.did_hit = True
        # for _ in range(20):
        #     effect = Water_drop(self.position, screen)
        #     self.effects.append(effect)


    def draw(self):
        screen.blit(self.image, self.position_words)
        screen.blit(self.projectile, self.projectile_position)
