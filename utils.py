import pygame

def draw_text(screen, text, pos, size=36, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, pos)