from settings import *

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0,0, width, height)
        self.width = width
        self.height = height


    def apply(self, entity):
        return entity.rect.move(-self.camera.topleft[0], -self.camera.topleft[1])


    def apply_rect(self, rect):
        return rect.move(-self.camera.topleft[0], -self.camera.topleft[1])

    def update(self, target):

        x = target.rect.centerx - self.camera.width // 2
        y = target.rect.centery - self.camera.height // 2

        # Clamp camera to level boundaries
        x = max(0, min(x, self.width - self.camera.width))
        y = max(0, min(y, self.height - self.camera.height))

        self.camera.topleft = (x, y)