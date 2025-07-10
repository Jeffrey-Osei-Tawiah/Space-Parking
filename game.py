import pygame
from random import randint, choice
import math


def lerp(a, b, t):
    return ((1 - t)* a + (t*b))

class Line:
    def __init__(self, start: pygame.Vector2, end: pygame.Vector2):
        self.start = start
        self.end = end
        self.normal = self.CalculateNormal()
        
    def CalculateNormal(self):
        normal = pygame.Vector2(0)
        normal = self.end - self.start
        normal = pygame.Vector2(normal.y, -normal.x).normalize()
        return normal
    
    def GetMidpoint(self) -> pygame.Vector2:
        return 0.5 * (self.start + self.end)
    
class Rocket:
    def __init__(self, position: pygame.Vector2, rotation: float, velocity: pygame.Vector2):
        self.pos = position
        self.rot = rotation
        self.vel = velocity
        
        self.radius = 20
        self.fuel = 1
        
    def update(self, deltaTime: float):
        
        self.rot = lerp(self.rot, 0, 0.99 * deltaTime)
        self.HandleInput(deltaTime)
        self.vel += pygame.Vector2(0, 150) * deltaTime
        self.pos += self.vel * deltaTime
        
            
    def HandleInput(self, deltaTime: float):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.fuel > 0:
                self.fuel -= 0.15 * deltaTime
                self.vel += -pygame.Vector2(math.sin(self.rot), math.cos(self.rot)) * 200 * deltaTime
                
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rot = lerp(self.rot, math.pi / 3, 0.99 * deltaTime)
            
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rot = lerp(self.rot, -math.pi / 3, 0.99 * deltaTime)
            
        
            
        
pygame.init()
screen = pygame.display.set_mode((650, 500))
clock = pygame.time.Clock()
running = True

player = Rocket(pygame.Vector2(250, 0), 0, pygame.Vector2(0, 20))
lines = []
lines.append(Line(pygame.Vector2(0, randint(300, 400)), pygame.Vector2(50, randint(300, 400))))

for i in range(50, 600 + 1, 50):
    line = Line(pygame.Vector2(i, lines[-1].end.y), pygame.Vector2(i + 50, randint(300, 400)))
    
    lines.append(line)
    
safe = randint(0, len(lines) - 1)
lines[safe].end.y = lines[safe].start.y
lines[safe].normal = lines[safe].CalculateNormal()

if safe < len(lines) - 1:
    lines[safe + 1].start.y =lines[safe].end.y
    
while running:
    deltaTime = clock.tick(60) / 1000 # limit fps to 60 and get elapsed time since last frame in seconds
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill("cyan")
    player.update(deltaTime)
    
    # calculate position of propeller
    propellerPos = pygame.Vector2(0, player.radius)
    propellerPos.x = propellerPos.y * math.sin(player.rot)
    propellerPos.y = propellerPos.y * math.cos(player.rot)
    pygame.draw.circle(screen, (217,113,22), player.pos, player.radius)
    pygame.draw.circle(screen, "red", pygame.Vector2(player.pos + propellerPos), player.radius / 2)
    
    for line in lines:
        #pygame.draw.line(screen, "blue", line.GetMidpoint(), line.GetMidpoint() + (line.normal * 20))
        pygame.draw.polygon(screen, "white", [line.start, line.end, (line.end.x, 500), (line.start.x, 500)])
        if line == lines[safe]:
            pygame.draw.line(screen, "green", line.start, line.end, 4)
            
    
    # display fuel
    pygame.draw.rect(screen, "black", pygame.Rect(590, 20, 25, 150))
    pygame.draw.polygon(screen, "green", ([590, 170], [615, 170], [615, 20 + (1 - player.fuel) * 150], [590, 20 + (1 - player.fuel) * 150]))
        
    
    pygame.display.flip() #double buffer rendering, render back buffer
    
pygame.quit()