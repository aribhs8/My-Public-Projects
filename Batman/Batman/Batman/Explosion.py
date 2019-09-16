# import pygame + files
import pygame
from settings import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, game, center):
        self.groups = game.all_sprites, game.explosions
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.frame = 0
        self.frame_rate = 75
        self.last_update = pygame.time.get_ticks()
        self.rect.center = center

    def load_images(self):
        self.frames = [self.game.powerUp2_spritesheet.get_image(28, 12, 32, 28),
                  self.game.powerUp2_spritesheet.get_image(63, 12, 32, 28),
                  self.game.powerUp2_spritesheet.get_image(97, 9, 37, 32),
                  self.game.powerUp2_spritesheet.get_image(142, 8, 38, 36),
                  self.game.powerUp2_spritesheet.get_image(190, 8, 42, 37),
                  self.game.powerUp2_spritesheet.get_image(243, 5, 47, 39),
                  self.game.powerUp2_spritesheet.get_image(5, 53, 49, 44),
                  self.game.powerUp2_spritesheet.get_image(66, 54, 52, 44),
                  self.game.powerUp2_spritesheet.get_image(128, 55, 55, 46)]

        for frame in self.frames:
            frame.set_colorkey((163, 226, 255))

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.frames):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.frames[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
