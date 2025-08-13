import pygame
import random
import math

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Text Animation - Technical Coderji")
clock = pygame.time.Clock()

# Particle class
class Particle:
    def __init__(self):
        self.x = random.uniform(0, WIDTH)
        self.y = random.uniform(0, HEIGHT)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.tx, self.ty = None, None  # target coords

    def update(self):
        if self.tx is not None and self.ty is not None:
            dx = self.tx - self.x
            dy = self.ty - self.y
            dist = math.hypot(dx, dy)
            if dist > 0.5:
                self.x += dx * 0.05
                self.y += dy * 0.05
        else:
            self.x += self.vx
            self.y += self.vy
            if self.x < 0 or self.x > WIDTH:
                self.vx *= -1
            if self.y < 0 or self.y > HEIGHT:
                self.vy *= -1

    def draw(self):
        pygame.draw.circle(screen, (0, 255, 0), (int(self.x), int(self.y)), 2)

# Create particles
particles = [Particle() for _ in range(10000)]

# Function to generate targets for multiline text
def generate_text_targets(lines):
    font = pygame.font.SysFont("Arial", 80, bold=True)
    total_height = len(lines) * font.get_height()
    start_y = HEIGHT // 2 - total_height // 2
    targets = []

    for i, text in enumerate(lines):
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH//2, start_y + i * font.get_height()))

        surface_locked = pygame.Surface(text_surface.get_size())
        surface_locked.blit(text_surface, (0, 0))
        pixels = pygame.PixelArray(surface_locked)

        for y in range(surface_locked.get_height()):
            for x in range(surface_locked.get_width()):
                if pixels[x, y] != surface_locked.map_rgb((0, 0, 0)):
                    targets.append((x + text_rect.left, y + text_rect.top))

        del pixels

    return targets

# Main loop
running = True
text_targets = None
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            text_targets = generate_text_targets(["Python + Code","Technical Coderji"])
            for p in particles:
                tx, ty = random.choice(text_targets)
                p.tx, p.ty = tx, ty

    for p in particles:
        p.update()
        p.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()