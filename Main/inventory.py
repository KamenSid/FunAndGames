from pygame.sprite import Sprite
from settings import *


class Inventory_slot(pygame.sprite.Sprite):
    def __init__(self, size, position, image=inventory_slot_bg):
        super().__init__()
        self.position = position
        self.size = size
        self.bg = image
        self.rect = self.bg.get_rect(topleft=position)

    def draw(self, item=None):
        if item == None:
            item = self.bg
            screen.blit(item, self.position)
        else:
            screen.blit(item.image, self.position)


class Inventory():
    def __init__(self,owner, slot_count, items):
        self.position = owner.position
        self.slot_count = slot_count
        self.slot_size = [60, 60]
        self.screen = screen
        self.slots = []
        self.items = items
        self.background_image = pygame.surface.Surface(
            [(self.slot_size[0] + 25) * self.slot_count, (self.slot_size[1] + 25) * self.slot_count])
        self.background = [self.background_image, [self.position[0] - 20, self.position[1] - 20]]

    def build(self):
        for row in range(self.slot_count):
            for col in range(self.slot_count):
                slot = Inventory_slot(self.slot_size, [self.position[0] + row * (self.slot_size[0] + 20),
                                                       self.position[1] + col * (self.slot_size[1] + 20)])
                self.slots.append(slot)

    def draw(self):
        self.screen.blit(*self.background)
        for i, slot in enumerate(self.slots):
            if i < len(self.items):
                item = self.items[i]
                slot.draw(item)
            else:
                slot.draw()

    def add_item(self, item):
        self.items.append(item)




class Item(pygame.sprite.Sprite):

    def __init__(self, image, stats, position=None):
        super().__init__()
        self.screen = screen
        self.position = position
        self.image = image
        self.stats = stats
        self.equpped = False
        if position:
            self.rect = self.image.get_rect(topleft=position)


    def draw(self):
        screen.blit(self.image, self.position)

    def pick(self):
        self.position[1] += 10
