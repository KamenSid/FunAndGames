from settings import *
import math
import random

colors = ["white", "yellow", "green", "blue", "purple", "lightblue"]


class Particle:
    def __init__(self, position, max_r, lifetime, color, speed, direction, gravity, screen):
        self.screen = screen
        self.lifetime = lifetime
        self.max_r = max_r
        self.color = color
        self.speed = speed
        self.vx = math.cos(direction[0]) * speed
        self.vy = math.sin(direction[1]) * speed
        self.position = position
        self.gravity = gravity


    def update(self):
        self.position[1] += self.gravity
        self.position[0] += self.vx
        self.position[1] += self.vy
        self.lifetime -= 1



    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.position, self.max_r)

    def light(self):
        if self.position[0] > 800:
            pygame.draw.circle(self.screen, "lightyellow", self.position, self.max_r+0.3)



class Snow_flake(Particle):
    def __init__(self, position, screen):
        super().__init__(position=position, max_r=1, lifetime=400, color=colors[random.randint(0, 5)], speed=1, direction=[0, random.uniform(-0.2,0.2)], gravity=0.2, screen=screen)


    def update(self):

        if self.lifetime < 150:
            self.gravity += random.uniform(-0.01, -0.1)
        elif self.lifetime < 290:
            self.gravity += random.uniform(-0.1, 0.1)
            self.max_r += 0.02
        self.position[0] += random.uniform(-1, 1)  # Simulate gentle drifting
        self.position[1] += self.gravity
        self.lifetime -= 1
        self.draw()




class Water_drop(Particle):
    def __init__(selfself, position, screen):
        super().__init__(position=position, max_r=3, lifetime=50, color="aquamarine", speed=3, direction=[random.uniform(0, -2 * math.pi), random.uniform(-300, -200 * math.pi)], gravity=0.2, screen=screen)

    def update(self):
        self.position[0] += random.uniform(-1, 1)
        self.max_r += 0.01
        super().update()

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.position, self.max_r)
        pygame.draw.circle(self.screen, "aqua", [self.position[0], self.position[1] - 3], self.max_r - 1)

    def light(self):
        if self.position[0] < 400:
            pygame.draw.circle(self.screen, "lightyellow", self.position, self.max_r+3)