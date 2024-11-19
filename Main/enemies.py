from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.screen = screen
        self.position = position
        self.idle_anim = Animation(test_enemy_idle_frames, 5)
        self.walk_anim = Animation(test_enemy_walk_frames, 5)
        self.run_anim = Animation(test_enemy_run_frames, 3)
        self.current_animation = self.idle_anim
        self.image = self.current_animation.get_frame()
        self.frame = frame_one
        self.rect = self.image.get_rect(midbottom=position)
        self.stats = Stats(100, 0, 0, 20)
        self.helth_bar = pygame.Surface([7, 10])
        self.helth_bar_bg = pygame.Surface([100, 10])
        self.vision_radius = 150



    def draw_hp(self):
        x, y = self.rect.topleft
        self.helth_bar_bg.fill("red")
        screen.blit(self.helth_bar_bg, [x, y - 10])
        for i in range(self.stats.helth // 10):
            self.helth_bar.fill("green")
            screen.blit(self.helth_bar, [x + i * 10 , y - 10])


    def draw(self):

        if self.stats.helth <= 50:
            # self.image = pygame.transform.flip(image, True, False)
            self.current_animation = self.run_anim
            self.position[0] += 1
            self.rect.midbottom = self.position

        self.current_animation.update()
        self.image = self.current_animation.get_frame()
        self.rect = self.image.get_rect(midbottom=self.position)
        screen.blit(self.image, self.rect.midbottom)
        # screen.blit(self.frame, [self.rect.topleft[0] - 8, self.rect.topleft[1] - 8])
        self.draw_hp()




