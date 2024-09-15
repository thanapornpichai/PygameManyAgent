# Example file showing a basic pygame "game loop"
import pygame
import random

WIDTH = 1280
HEIGHT = 720
MAX_SPEED = 2

class Agent:
    def __init__(self, x, y) -> None:
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(1, 0)
        self.mass = 1

    def update(self):
        self.velocity = self.velocity + self.acceleration
        if self.velocity.length() > MAX_SPEED:
            self.velocity = self.velocity.normalize() * MAX_SPEED
        self.position = self.position + self.velocity
        self.acceleration = pygame.Vector2(0, 0)

    def apply_force(self, x, y):
        force = pygame.Vector2(x, y)
        self.acceleration = self.acceleration + (force/self.mass)

    def seek(self, x, y):
        d = pygame.Vector2(x, y) - self.position
        d = d.normalize() * 0.1
        seeking_force = d
        self.apply_force(seeking_force.x, seeking_force.y)

    def coherence(self, agents):
        
        center_of_mass = pygame.Vector2(0, 0)

        for agent in agents:
            if agent != self:
                center_of_mass += agent.position

        center_of_mass /= len(agents) - 1

        d = center_of_mass - self.position
        f = d.normalize() * 0.1
        self.apply_force(f.x, f.y)

    def separation(self, agents):

        d = pygame.Vector2(0, 0)
        for agent in agents:
            d += self.position - agent.position
        separation_force = d * 0.1

        self.apply_force(separation_force.x, separation_force.y)

    def draw(self):
        pygame.draw.circle(screen, "red", self.position, 10)

agents = []
for i in range(100):
    agents.append( Agent(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)))


# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("grey")

    for agent in agents:
        #agent.seek(400, 400)
        agent.coherence(agents)
        agent.separation(agents)
        agent.update()
        agent.draw()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()