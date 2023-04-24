import pygame
import math

pygame.init()
WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Draw with the Mouse")

points = []
dragging = False
thickness = 5
center = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2)

font = pygame.font.Font(None, 30)
start_time = pygame.time.get_ticks()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if len(points) > 1:
                points = []
            points.append(event.pos)
            dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            points.append(event.pos)

    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, (255, 255, 255), center, 5)

    distances = []
    for i in range(len(points) - 1):
        p1, p2 = points[i:i+2]
        distance = abs((p2[1] - p1[1]) * center[0] - (p2[0] - p1[0]) * center[1] + p2[0] * p1[1] - p2[1] * p1[0]) / math.hypot(p2[1] - p1[1], p2[0] - p1[0])
        distances.append(distance)

    if distances:
        constant_percentage = round(sum(d == distances[0] for d in distances) / len(distances) * 100)
    else:
        constant_percentage = 0

    if constant_percentage >= 85:
        color = (0, 255, 0) 
    elif constant_percentage >= 65:
        color = (255, 255, 0)  
    else:
        color = (255, 0, 0) 

    too_close = any(math.hypot(point[0] - center[0], point[1] - center[1]) < 50 for point in points)

    if len(points) > 1:
        pygame.draw.lines(screen, color, False, points, thickness)

    text = font.render(str(constant_percentage) + "%", True, color)
    screen.blit(text, (10, 10))

    if too_close:
        text = font.render("Too close", True, (255, 0, 0))
        screen.blit(text, (WINDOW_SIZE[0] - text.get_width() - 10, 10))

    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time > 10000:
        text = font.render("Too slow", True, (255, 0, 0))
        screen.blit(text, (WINDOW_SIZE[0] // 2 - text.get_width() // 2, 10))

    pygame.display.flip()

pygame.quit()
