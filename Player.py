import pygame

vec = pygame.math.Vector2

class Player:
    def __init__(self, sprite, screen):
        self.screen = screen

        self.sprite = pygame.image.load("Sprites/" + sprite + ".png").convert_alpha()
        self.sprite_idle = self.sprite
        self.mask = pygame.mask.from_surface(self.sprite)
        self.sprite_accelerating = pygame.image.load("Sprites/Player/accelerating.png").convert_alpha()
        self.sprite_jump = pygame.image.load("Sprites/Player/jump.png").convert_alpha()
        self.sprite_fall = pygame.image.load("Sprites/Player/fall.png").convert_alpha()
        self.rect = self.sprite.get_frect()
    
        self.x, self.y = (32,112)
        self.rect.center = (self.x, self.y)
        self.isJumping = False

        self.vel = 0
        self.acc = 0

        self.accelerating = False
    
    def update(self):
        self.spriteUpdate()
        self.gravity()
        
        self.vel += self.acc
        self.y += self.vel + 0.5 * self.acc
        if self.y > 112:
            self.isJumping = False
            self.vel = 0
            self.y = 112
        self.rect.center = (self.x, self.y)
        self.screen.blit(self.sprite, self.rect)

    def spriteUpdate(self):
        if self.accelerating:
            self.sprite = self.sprite_accelerating
        else:
            self.sprite = self.sprite_idle
        
        if self.vel < 0:
            self.sprite = self.sprite_jump
        elif self.vel > 0:
            self.sprite = self.sprite_fall
    
    def gravity(self):
        if self.y < 112:
            self.isJumping = True
            if self.vel < 0:
                self.acc = 0.2
            elif self.vel > 0:
                self.acc = 0.3
    
    def jump(self, speed):
        if self.isJumping == False: self.vel = -speed