import random

import pygame.sprite
from enemies import Enemy
from main_guy import *
from surfaces import Surface


pygame.init()

clock = pygame.time.Clock()
running = True
colors_list = ["green", "orange", "red", "purple"]
player = Main_guy([250, 300])
enemies = []
effects = []
ground_items = []
# land = Surface([100, 400])
# land2 = Surface([600, 400])
# land3 = Surface([300, 500])
# main_land = Surface([0, 850])
# main_land2 = Surface([300, 850])
# main_land3 = Surface([600, 850])
# lands.extend([land, land2, land3, main_land, main_land2, main_land3])
enemy = Enemy([620, 300])
enemies.append(enemy)
test_item = Item(test_item_1_image, {"speed": 0.5}, [500, 800])
ground_items.append(test_item)
players = [player]
level = Surface()
level.build()
while running:

    screen.fill("blue")
    keys = pygame.key.get_pressed()

    player_pos_x = pygame.mouse.get_pos()[0]
    player_pos_y = pygame.mouse.get_pos()[1]


    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    for item in ground_items:
        item.draw()
        if pygame.sprite.collide_rect(item, player):
            player.inventory.add_item(item)
            ground_items.remove(item)
            player.effect()

    for spell in player.spells_list:
        if spell.cooldown > 2:
            spell.update()
            spell.draw()
        else:
            if spell.name == "teleport":
                player.position[0] = 50
                player.position[1] = 50
            player.spells_list.remove(spell)


    if not enemies:
        enemy = Enemy([random.randint(400, 600), random.randint(250, 500)])
        enemies.append(enemy)


    for enemy in enemies:
        if player.spells_list:
                if pygame.sprite.collide_rect(enemy, spell):
                    if not spell.did_hit:
                        spell.hit()
                        effects.extend(spell.effects)
                        enemy.stats.helth -= 30
        if pygame.sprite.collide_rect(player, enemy):
            enemy.stats.helth -= 25
        if enemy.stats.helth > 0:
            enemy.draw()
        else:
            enemies.remove(enemy)
            player.stats.gold += enemy.stats.gold
            print(player.stats.gold)

    player.update(keys, level, enemies)
    player.draw()

    effects.extend(player.circles_list)
    player.circles_list = []
    for effect in effects:
        effect.update()
    effects = [effect for effect in effects if effect.lifetime > 1]

    level.draw(players)
    pygame.display.flip()


    clock.tick(60)

pygame.quit()
