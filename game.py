import pygame
from random import randint, choice
import math


def lerp(a, b, t):
    return ((1 - t)* a + (t*b))

def pointCircle(x, y, cx, cy, r):
    return ((x-cx)**2 + (y-cy)**2 <= r ** 2)

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
        self.acc = pygame.Vector2(0, 150)
        
        self.radius = 20
        self.fuel = 1
        
    def update(self, deltaTime: float):
        
        self.rot = lerp(self.rot, 0, 0.99 * deltaTime)
        self.HandleInput(deltaTime)
        self.vel += self.acc * deltaTime
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
            
         
def linepoint(line: Line, point: pygame.Vector2):
    d1 = point.distance_to(line.start)
    d2 = point.distance_to(line.end)
    
    lineLen = (line.end - line.start).length()
    buffer = 0.1
    if (d1 + d2) >= lineLen - buffer and (d1 + d2) <= lineLen - buffer:
        return True
    return False

def checkCollision(line: Line, player: Rocket):
    inside1 = pointCircle(line.start.x, line.start.y, player.pos.x, player.pos.y, player.radius)
    inside2 = pointCircle(line.end.x, line.end.y, player.pos.x, player.pos.y, player.radius)
    
    if inside1 or inside2:
        return True
    
    len_sq = (line.end - line.start).length_squared()
    dot = pygame.Vector2.dot(player.pos - line.start, line.end-line.start) / len_sq
    closest = line.start + (dot * (line.end - line.start))
    
    onSegment = linepoint(line, closest)
    if not onSegment:
        return False
    
    distance = (closest - player.pos).length_squared()
    if distance <= player.radius**2:
        return True
    return False
            
        
            
        
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
    
    # calculate position of propeller
    propellerPos = pygame.Vector2(0, player.radius)
    propellerPos.x = propellerPos.y * math.sin(player.rot)
    propellerPos.y = propellerPos.y * math.cos(player.rot)
    pygame.draw.circle(screen, (217,113,22), player.pos, player.radius)
    pygame.draw.circle(screen, "red", pygame.Vector2(player.pos + propellerPos), player.radius / 2)
    
    for line in lines:
        
        if checkCollision(line, player):
            dot = pygame.Vector2.dot(player.vel, line.normal) * line.normal  
            perp = player.vel - dot
            player.vel = perp
                
            print("Collision detected")
            if line == lines[safe]:
                print("You win")
        #pygame.draw.line(screen, "blue", line.GetMidpoint(), line.GetMidpoint() + (line.normal * 20))
        pygame.draw.polygon(screen, "white", [line.start, line.end, (line.end.x, 500), (line.start.x, 500)])
        if line == lines[safe]:
            pygame.draw.line(screen, "green", line.start, line.end, 4)
            
    
    player.update(deltaTime)
    # display fuel
    pygame.draw.rect(screen, "black", pygame.Rect(590, 20, 25, 150))
    pygame.draw.polygon(screen, "green", ([590, 170], [615, 170], [615, 20 + (1 - player.fuel) * 150], [590, 20 + (1 - player.fuel) * 150]))
        
    
    pygame.display.flip() #double buffer rendering, render back buffer
    
pygame.quit()