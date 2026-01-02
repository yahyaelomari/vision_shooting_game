import pygame
import random
import math
import time

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 8)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.lifetime = random.uniform(0.5, 1.0)
        self.spawn_time = time.time()
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.size = max(0, self.size - 0.1)
        
    def is_alive(self):
        return time.time() - self.spawn_time < self.lifetime and self.size > 0
        
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))

class GameObject:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = random.randint(100, screen_width - 100)
        self.y = random.randint(100, screen_height - 100)
        self.spawn_time = time.time()
        self.lifetime = 5.0
        self.score = 10
        self.size = 50
        self.color = (255, 255, 255)
        
    def update(self):
        pass
        
    def is_expired(self):
        return time.time() - self.spawn_time > self.lifetime
        
    def draw(self, surface):
        pass

class Drone(GameObject):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.score = 50
        self.size = 40
        self.color = (0, 255, 255) # Cyan
        self.angle = 0
        self.speed_x = random.choice([-2, 2])
        self.speed_y = random.choice([-1, 1])
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.angle += 5
        
        # Bounce
        if self.x < 50 or self.x > self.screen_width - 50: self.speed_x *= -1
        if self.y < 50 or self.y > self.screen_height - 50: self.speed_y *= -1
        
    def draw(self, surface):
        # Draw central body
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 15)
        # Draw rotating blades
        rad = math.radians(self.angle)
        for i in range(4):
            offset = math.radians(i * 90)
            bx = self.x + math.cos(rad + offset) * 25
            by = self.y + math.sin(rad + offset) * 25
            pygame.draw.circle(surface, (100, 100, 100), (int(bx), int(by)), 8)
            pygame.draw.line(surface, (50, 50, 50), (int(self.x), int(self.y)), (int(bx), int(by)), 2)

class Orb(GameObject):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.score = 30
        self.size = 35
        self.color = (255, 0, 255) # Magenta
        self.pulse_speed = 5
        
    def update(self):
        # Pulse size
        self.current_size = self.size + math.sin(time.time() * self.pulse_speed) * 10
        
    def draw(self, surface):
        s = int(getattr(self, 'current_size', self.size))
        # Glow
        pygame.draw.circle(surface, (*self.color, 100), (int(self.x), int(self.y)), s + 10)
        # Core
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), s)
        pygame.draw.circle(surface, (255, 255, 255), (int(self.x), int(self.y)), s // 2)

class HexTarget(GameObject):
    def __init__(self, w, h):
        super().__init__(w, h)
        self.score = 20
        self.size = 45
        self.color = (255, 165, 0) # Orange
        self.rotation = 0
        
    def update(self):
        self.rotation += 2
        
    def draw(self, surface):
        points = []
        for i in range(6):
            angle_deg = 60 * i + self.rotation
            angle_rad = math.radians(angle_deg)
            px = self.x + self.size * math.cos(angle_rad)
            py = self.y + self.size * math.sin(angle_rad)
            points.append((px, py))
            
        pygame.draw.polygon(surface, self.color, points, 3)
        pygame.draw.polygon(surface, (255, 255, 0), points, 1)
        # Center dot
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 5)

# Factory to create random objects
def create_random_object(w, h):
    r = random.random()
    if r < 0.3: return Drone(w, h)
    elif r < 0.6: return Orb(w, h)
    else: return HexTarget(w, h)
