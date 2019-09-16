# IMPORT MODULES + FILES
# pygame
import pygame
# settings file 
from settings import *
# import path from os to find files regardless of operating system
from os import path

# Power-up sprite class
class Pow(pygame.sprite.Sprite):
    # initalize power-up with all attributes
    def __init__(self, game, type, x, y):
        # set the groups to store the sprite in
        self.groups = game.all_sprites, game.powerups
        # initalize the sprite as well as the group to place in
        pygame.sprite.Sprite.__init__(self, self.groups)
        # game attribute
        self.game = game
        # type attribute
        self.type = type
        # y-coordinate attibute
        self.y = y
        # checks if the the type attribute is 'explosion'
        if self.type == "explosion":
            # sets the image of the power-up to that of the bomb
            self.image = self.game.bomb
            # scales the image of the power-up to the specified dimensions
            self.image = pygame.transform.scale(self.image, (40, 40))
        # checks if the type attribute is 'shield'
        elif self.type == "shield":
            # sets the image of the power-up to that of the shield
            self.image = pygame.image.load(path.join(self.game.img_dir, 'shield.png'))
            # scales the image of the power-up to the specified dimensions
            self.image = pygame.transform.scale(self.image, (40, 40))
        # makes the image get a rectangle
        self.rect = self.image.get_rect()
        # set the image's center to the x and y parameters
        self.rect.center = (x, y)

    # update method for pow
    def update(self):
        # SET DIRECTION OF MOVEMENT
        # checks if the position of the pow is less (higher) or equal than what it started with
        if self.rect.centery <= self.y:
            # sets the direction equal to "D" (down)
            self.direction = "D"
        # checks if the position of pow is more (lower) or equal than the initial position + 4 down
        elif self.rect.centery >= self.y + 4:
            # sets the direction equal to "U" (up)
            self.direction = "U"

        # MOVEMENT
        # if the direction is "D" (down)
        if self.direction == "D":
            # move the power-up down
            self.rect.y += 1
        # if the direction is "U" (up)
        elif self.direction == "U":
            # move the power-up up
            self.rect.y -= 1