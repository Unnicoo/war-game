import pygame

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CELL_SIZE = 40
MAP_WIDTH, MAP_HEIGHT = 50, 50  # 50x50 grid

# Map representation (2D list)
game_map = [[(x + y) % 2 for x in range(MAP_WIDTH)] for y in range(MAP_HEIGHT)]

# Camera position
camera_x, camera_y = 0, 0
dragging = False  # Is the user dragging the map?
last_mouse_pos = None

# Pygame setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                dragging = True
                last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                dx, dy = event.rel
                camera_x -= dx
                camera_y -= dy
                # Clamp camera to map boundaries
                camera_x = max(0, min(camera_x, MAP_WIDTH * CELL_SIZE - SCREEN_WIDTH))
                camera_y = max(0, min(camera_y, MAP_HEIGHT * CELL_SIZE - SCREEN_HEIGHT))

    # Draw the visible portion of the map
    screen.fill((0, 0, 0))
    for row in range(MAP_HEIGHT):
        for col in range(MAP_WIDTH):
            cell_x = col * CELL_SIZE - camera_x
            cell_y = row * CELL_SIZE - camera_y
            if 0 <= cell_x < SCREEN_WIDTH and 0 <= cell_y < SCREEN_HEIGHT:
                color = (200, 200, 200) if game_map[row][col] == 0 else (100, 100, 100)
                pygame.draw.rect(screen, color, (cell_x, cell_y, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
