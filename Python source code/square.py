import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Infinite Fractal Zoom - Technical Coderji")
clock = pygame.time.Clock()

zoom = 1.0
zoom_speed = 0.005
FPS = 10  # starting FPS

# Colors
BG = (50, 50, 50)
LINE = (255, 255, 255)

font = pygame.font.SysFont(None, 50)  # for FPS display

def draw_zoomed_fractal(x, y, size, view_size, depth=0, max_depth=10):
    if depth > max_depth or size < 2 / zoom:
        return

    # Convert fractal coords → screen coords (bottom-left origin)
    sx = (x / view_size) * WIDTH
    sy = HEIGHT - (y + size) / view_size * HEIGHT
    s_size = (size / view_size) * WIDTH

    # Outer square (thin line)
    pygame.draw.rect(screen, LINE, (sx, sy, s_size, s_size), 1)

    # Vertical split
    mid_x = x + size / 2
    pygame.draw.line(screen, LINE,
                     ((mid_x / view_size) * WIDTH, sy),
                     ((mid_x / view_size) * WIDTH, sy + s_size), 1)

    # Horizontal split in left rectangle
    square_size = size / 2
    mid_y = y + square_size
    pygame.draw.line(screen, LINE,
                     ((x / view_size) * WIDTH,
                      HEIGHT - mid_y / view_size * HEIGHT),
                     ((mid_x / view_size) * WIDTH,
                      HEIGHT - mid_y / view_size * HEIGHT), 1)

    # Recursive bottom-left
    draw_zoomed_fractal(x, y, square_size, view_size, depth + 1, max_depth)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                FPS = min(500, FPS + 10)
            elif event.key == pygame.K_DOWN:
                FPS = max(10, FPS - 10)

    screen.fill(BG)  # Black background

    base_size = WIDTH
    view_size = base_size / zoom

    draw_zoomed_fractal(0, 0, base_size, view_size)

    # Draw FPS text in white
    fps_text = font.render(f"Speed: {FPS}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    # Smooth infinite zoom
    zoom *= 1 + zoom_speed
    if zoom > 2:
        zoom /= 2

    pygame.display.flip()
    clock.tick(FPS)