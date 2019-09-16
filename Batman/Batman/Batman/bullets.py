# IMPORT MODULES + PYGAME
# pygame
import pygame
# settings
from settings import *
# power-ups
from pow import *
# random
import random
# vector variable (measurement with direction; for two-dimensional motion)
vec = pygame.math.Vector2
# import path from os so files can be accessed regardless of operating system
from os import path

# bullet sprite class
class Bullet(pygame.sprite.Sprite):
    # initialize bullet class
    def __init__(self, game, x, y, type, shoot_direction):
        # groups to save bullet in
        self.groups = game.all_sprites
        # iniatilize sprite and save into specified groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        # game attribute
        self.game = game
        # direction of shot attribute
        self.shoot_direction = shoot_direction
        # type attribute
        self.type = type

        # SET IMAGE + PROPERTIES OF BULLET
        # check if type attribute is 'batarang'
        if self.type == "batarang":
            # set the image to image located at the specified position on the spritesheet
            self.image = self.game.player_spritesheet.get_image(356, 515, 15, 17)
            # check the direction of the shot
            if self.shoot_direction == "L":
                # flip the image 180 degrees (across y-axis)
                self.image = pygame.transform.flip(self.image, True, False)
            # scales them image to the specified dimension
            self.image = pygame.transform.scale(self.image, (15, 17))
            # removes color from background
            self.image.set_colorkey((3, 142, 187))
            # makes the image get a rectangle
            self.rect = self.image.get_rect()
            # sets the bottom of the rectangle to y-coordinate
            self.rect.bottom = y
            # sets the middle of the rectangle (x-axis) to the x-coordinate
            self.rect.centerx = x
        # checks if the type attribute is 'gun'
        elif self.type == "gun":
            # load the image of the gun bullet
            self.image = pygame.image.load(path.join(self.game.img_dir, "gunBullet.png")).convert()
            self.image.set_colorkey(BLACK)
            # checks the shoot_direction attribute
            if self.shoot_direction == "B":
                # flips the image 180 degrees (y-axis)
                self.image = pygame.transform.flip(self.image, True, False)
            # makes the image get a rectangle
            self.rect = self.image.get_rect()
            # sets the bottom of the rectangle to y-coordinate
            self.rect.bottom = y
            # sets the middle of the rectangle (x-axis) to the x-coordinate
            self.rect.centerx = x
        # checks if type attribute is 'explosion'
        elif type == "explosion":
            # set the image to image located at the specified position on the spritesheet
            self.image = self.game.powerUp2_spritesheet.get_image(7, 25, 21, 17)
            # scales the image to the specified dimensions
            self.image = pygame.transform.scale(self.image, (15, 17))
            # checks the shoot_direction attribute
            if self.shoot_direction == "L":
                # flips the image 180 degress (y-axis)
                self.image = pygame.transform.flip(self.image, True, False)
            # removes the specified color from the background of the image
            self.image.set_colorkey((163, 226, 255))
            # makes the image get a rectangle
            self.rect = self.image.get_rect()
            # sets the bottom of the rectangle to y-coordinate
            self.rect.bottom = y
            # sets the middle of the rectangle (x-axis) to the x-coordinate
            self.rect.centerx = x
        # checks if type attribute is 'boulder'
        elif type == "boulder":
            # set the image located at the specified position on the spritesheet
            self.image = self.game.boss_spritesheet.get_image(445, 615, 36, 34)
            # makes the image get a rectangle
            self.rect = self.image.get_rect()
            # set the bottom of the rectangle equal to the y-parameter
            self.rect.bottom = y
            # set the middle of the rectangle (x-axis) equal to x-parameter
            self.rect.centerx = x

            # POSITION + MOVEMENT VARIABLES
            # set the initial velocity
            self.vel = vec(0,0)
            # set the initial acceleration
            self.acc = vec(0,0)
            # set the initial position
            self.pos = (x,y)
            # ALTERED EQUATIONS OF MOTION
            # gravity projectile motion equation
            self.vel.y = ((self.game.player.rect.top - self.game.boss.rect.top) + (0.5 * GRAV)) * (30 / 1000)
            # x-direction constant motion equation
            self.vel.x = (self.game.player.rect.left - self.game.boss.rect.right) / 30

        # DIRECTION OF MOVEMENT SETTINGS
        # check direction attribute
        if self.shoot_direction == "F" or self.shoot_direction == "R":
            # speed in x is positive
            self.speedx = 10
        # if direction attribute is not "F" or "R"
        else:
            # speed in x is negative
            self.speedx = -10

    # update method
    def update(self):
        # if type attribute is "boulder"
        if self.type == "boulder":
            # vertical acceleration downward
            if self.game.boss.rect.centery >= self.game.player.rect.centery:
                self.acc = vec(0, 0.12)
            else:
                self.acc = vec(0, GRAV)

            # SPRITE COLLISIONS
            # if it collides with any walls
            if pygame.sprite.spritecollideany(self, self.game.walls):
                # check if random number is more than 0.7 (30% chance)
                if random.random() > 0.7:
                    # spawn a power-up
                    pow = Pow(self.game, "explosion", self.rect.right + 4, self.rect.centery)
                # kill the boulder
                self.kill()
            # if it collides with any platforms
            if pygame.sprite.spritecollideany(self, self.game.platforms):
                # checks if random number is more than 0.7 (30% chance)
                if random.random() > 0.7:
                    # spawn a power-up
                    pow = Pow(self.game, "explosion", self.rect.centerx, self.rect.top + 4)
                # kill the boulder
                self.kill()
                
            # increase the velocity by acceleration in y and x
            self.vel += self.acc
            # EQUATIONS OF MOTION
            # increase pos by vel and 1/2 of acc
            self.pos += self.vel + 0.5 * self.acc

            # set the midbottom of the boulder to pos variable
            self.rect.midbottom = self.pos
        # if type attribute is not a boulder
        else:
            # set the position in the x-axis equal to the speed in the x-axis
            self.rect.x += self.speedx

            # WHEN TO KILL
            # if the bullet is off screen
            if self.rect.centerx > self.game.player.rect.centerx + 500:
                # kill the bullet sprite
                self.kill()
            # if the bullet is off screen
            if self.rect.centerx < self.game.player.rect.centerx - 500:
                # kill the bullet sprite
                self.kill()
            # if the bullet sprite collides with any of the walls
            if pygame.sprite.spritecollideany(self, self.game.walls):
                # kill the bullet sprite
                self.kill()
            if pygame.sprite.spritecollideany(self, self.game.platforms):
                self.kill()
