import pygame
import random

class Obstacle():
    def __init__(self, screen):
        self.screen = screen
        self.car1_sprite = spr("Sprites/car1.png")
        self.van1_sprite = spr("Sprites/van1.png")
        self.van2_sprite = spr("Sprites/van2.png")
        self.traffic_cone_sprite = spr("Sprites/traffic_cone.png")
        self.sprites = [self.car1_sprite, self.van1_sprite, self.van2_sprite, self.traffic_cone_sprite]

        self.chosen_sprite = random.randint(0, len(self.sprites) - 1)
        self.sprite = self.sprites[self.chosen_sprite].sprite
        self.mask = self.sprites[self.chosen_sprite].mask
        self.rect = self.sprite.get_frect()

        self.x, self.y = (176 + random.randint(160, 320),122)
    
    def update(self):
        if self.x < 0 - self.rect.width:
            self.x = 176 + random.randint(0, 320)

            self.chosen_sprite = random.randint(0, len(self.sprites) - 1)
            self.sprite = self.sprites[self.chosen_sprite].sprite
            self.mask = self.sprites[self.chosen_sprite].mask
            self.rect = self.sprite.get_frect()
        
        # Set Position
        self.rect.midbottom = (self.x, self.y)
        self.screen.blit(self.sprite, self.rect)

class spr():
    def __init__(self, spritePath):
        self.sprite = pygame.image.load(spritePath).convert_alpha()
        self.mask = pygame.mask.from_surface(self.sprite)
