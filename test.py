import pygame

WIDTH, HEIGHT = 300, 200

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
