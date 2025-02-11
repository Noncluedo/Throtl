import pygame

class Scrollable:
    def __init__(self, sprite, screen, x ,y):
        self.screen = screen
        self.sprite = pygame.image.load("Sprites/" + sprite + ".png").convert_alpha()
        self.rect = self.sprite.get_rect()
        self.x, self.y = (x,y)
    
    def update(self):
        if self.x < -self.rect.width / 2:
            self.x = 0
        self.rect.topleft = (self.x, self.y)
        self.screen.blit(self.sprite, self.rect)