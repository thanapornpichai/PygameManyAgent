# Example file showing a basic pygame "game loop"
import pygame
import random
import math

WIDTH = 1280
HEIGHT = 720
MAX_SPEED = 5

COHERENCE_FACTOR = 0.01
ALIGNMENT_FACTOR = 0.1
SEPARATION_FACTOR = 0.05
SEPARATION_DISTANCE = 25

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
        agent_in_range_count = 0

        for agent in agents:
            if agent != self:
                dist = math.sqrt((self.position.x - agent.position.x)**2 + (self.position.y - agent.position.y)**2)
                if dist < 100:
                    center_of_mass += agent.position
                    agent_in_range_count += 1

        if agent_in_range_count > 0:
            center_of_mass /= agent_in_range_count

        d = center_of_mass - self.position
        f = d * COHERENCE_FACTOR
        self.apply_force(f.x, f.y)

    def separation(self, agents):

        d = pygame.Vector2(0, 0)
        for agent in agents:
            dist = math.sqrt((self.position.x - agent.position.x)**2 + (self.position.y - agent.position.y)**2)
            #dist = pygame.math.Vector2.distance_to(self.position,agent.position)
            if dist < SEPARATION_DISTANCE:
                d += self.position - agent.position

        separation_force = d * SEPARATION_FACTOR

        self.apply_force(separation_force.x, separation_force.y)

    def alignment(self, agents):
        v = pygame.Vector2(0, 0)
        for agent in agents:
            if agent != self:
                v += agent.velocity
        
        v /= len(agents) - 1
        alignmen_f = (v - self.velocity) * ALIGNMENT_FACTOR
        self.apply_force(alignmen_f.x, alignmen_f.y)


    def draw(self):
        pygame.draw.circle(screen, "red", self.position, 10)

agents = []
for i in range(100):
    agents.append( Agent(random.uniform(0, WIDTH), random.uniform(0, HEIGHT)))

agents[4].apply_force(-5, -5)

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
        agent.alignment(agents)
        agent.update()
        agent.draw()

    for agent in agents:
        if agent.position.x > WIDTH + 1:
            agent.position.x = 1
        elif agent.position.x < 0:
            agent.position.x = WIDTH
        if agent.position.y > HEIGHT + 1:
            agent.position.y = 1
        elif agent.position.y < 0:
            agent.position.y = HEIGHT

    pygame.display.flip()

    clock.tick(60)

pygame.quit()