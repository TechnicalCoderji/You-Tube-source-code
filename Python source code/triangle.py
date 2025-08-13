import pygame

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Infinite Triangle Zoom - Technical Coderji")

# Colors
BG_COLOR = (0, 0, 0)
LINE_COLOR = (0, 255, 0)

# Target apex position
APEX_TARGET = (300, 100)

# Initial zoom
zoom = 1.0

# Base triangle (before any zoom or shift)
base_p1 = (WIDTH / 2, HEIGHT * 0.3)  # apex
base_p2 = (WIDTH * 0.1, HEIGHT * 0.9)
base_p3 = (WIDTH * 0.9, HEIGHT * 0.9)

font = pygame.font.SysFont(None, 50)

def transform_point(p):
    """Scale and shift so apex is always at APEX_TARGET"""
    dx = APEX_TARGET[0] - base_p1[0] * zoom
    dy = APEX_TARGET[1] - base_p1[1] * zoom
    return (p[0] * zoom + dx, p[1] * zoom + dy)

def is_triangle_offscreen(p1, p2, p3):
    """Return True if triangle is completely outside the screen"""
    min_x = min(p1[0], p2[0], p3[0])
    max_x = max(p1[0], p2[0], p3[0])
    min_y = min(p1[1], p2[1], p3[1])
    max_y = max(p1[1], p2[1], p3[1])
    return max_x < 0 or min_x > WIDTH or max_y < 0 or min_y > (HEIGHT+100)

def draw_triangle(p1, p2, p3):
    """Recursive triangle drawing with off-screen and min-size checks"""
    # Skip if too small
    if max(
        abs(p1[0] - p2[0]), abs(p2[0] - p3[0]), abs(p3[0] - p1[0]),
        abs(p1[1] - p2[1]), abs(p2[1] - p3[1]), abs(p3[1] - p1[1])
    ) < 4:
        return

    # Skip if entirely off screen
    if is_triangle_offscreen(p1, p2, p3):
        return

    pygame.draw.polygon(screen, LINE_COLOR, [p1, p2, p3], 1)

    # Midpoints for Sierpinski-like division
    m12 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    m23 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
    m31 = ((p3[0] + p1[0]) / 2, (p3[1] + p1[1]) / 2)

    draw_triangle(p1, m12, m31)  # top subtriangle
    draw_triangle(m12, p2, m23)  # bottom-left
    draw_triangle(m31, m23, p3)  # bottom-right

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Zoom with mouse wheel
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:  # zoom in
                zoom *= 1.1
            elif event.y < 0:  # zoom out
                zoom /= 1.1

    screen.fill(BG_COLOR)

    # Transform and draw base triangle recursively
    tp1 = transform_point(base_p1)
    tp2 = transform_point(base_p2)
    tp3 = transform_point(base_p3)
    draw_triangle(tp1, tp2, tp3)

    # Draw zoom text
    zoom_text = font.render(f"Zoom: {zoom:.2f}x", True, (255, 255, 255))
    screen.blit(zoom_text, (10, 10))

    # Smooth infinite zoom
    zoom *= 1 + 0.01

    pygame.display.flip()
    clock.tick(60)

pygame.quit()