# IMPORT MODULES + PYGAME
# pygame
import pygame
# settings
from settings import *
# import path from os so all images can be loaded regardless of operating system
from os import path

# setup platforms
class Platform(pygame.sprite.Sprite):
    # initialize platform with all attributes
    def __init__(self, game, x, y, w, h):
        # sprite groups to include platform in
        self.groups = game.all_sprites
        # initalize sprite
        pygame.sprite.Sprite.__init__(self, self.groups)
        # game attribute
        self.game = game
        # set image of sprite
        self.image = self.game.jail_spritesheet.get_image(0, 416, 480, 33)
        # scale image to specified dimension
        self.image = pygame.transform.scale(self.image,((w, h)))
        # make image get a rectangle
        self.rect = self.image.get_rect()
        # set the x-value of rectangle to x parameter
        self.rect.x = x
        # set y-value of rectangle yo y parameter
        self.rect.y = y
        # set width of rectangle to w parameter
        self.rect.w = w
        # set height of rectangle to h parameter
        self.rect.h = h

# setup box objects
class Box(pygame.sprite.Sprite):
    # intialize spirte + attributes
    def __init__(self, game, x, y, w, h, type):
        # store sprite in specified groups
        self.groups = game.all_sprites, game.boxes
        # initalize sprite + store in specified groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        # game attribute
        self.game = game
        # type attribute
        self.type = type
        # check if type attribute is 'horizontal'
        if self.type == "horizontal":
            # get image for horizontal box
            self.image = self.game.jail_spritesheet.get_image(577, 161, 94, 91)
            # scale the image to specified dimensions
            self.image = pygame.transform.scale(self.image, ((w, h)))
        # check if type attribute is 'vertical'
        elif self.type == "vertical":
            # get image from spritesheet
            self.image = self.game.jail_spritesheet.get_image(0, 63, 65, 128)
            # scale image to specified dimensions
            self.image = pygame.transform.scale(self.image, ((w, h)))

        # make image get rectangle
        self.rect = self.image.get_rect()
        # set the x-position of the rectangle to x parameter
        self.rect.x = x
        # set the y-position of the rectangle to y parameter
        self.rect.y = y

# Miscellaneous class to store miscellaneous sprites
class Miscellaneous(pygame.sprite.Sprite):
    # initalize sprite
    def __init__(self, game, x, y, w, h, type):
        # sprite groups to store in
        self.groups = game.all_sprites
        # initalize sprite with groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        # type attribute
        self.type = type
        # current_frame attribute (for animation)
        self.current_frame = 0
        # game attribute
        self.game = game
        # last_update attribute (for animation)
        self.last_update = 0
        # w attribute (width)
        self.w = w
        # h attribute (height)
        self.h = h
        # load images method
        self.load_images()
        # check if type attribute is 'lightning'
        if self.type == "Lightning":
            # make image first image in lightning_list
            self.image = self.lightning_list[0]
        # check if type attribute is door
        elif self.type == "door":
            # make image first image in door_frames
            self.image = self.door_frames[0]
            # make the door open variable False (animation)
            self.open = False
        # check if type attribute is 'move'
        elif self.type == "move":
            # loads move keys image (WASD)
            self.image = pygame.image.load(path.join(self.game.img_dir, "MoveKeys.png")).convert()
            # remove background from image
            self.image.set_colorkey((BLACK))
            # scale image to specified dimensions
            self.image = pygame.transform.scale(self.image, (75, 75))
        # check if type attribute is 'combat'
        elif self.type == "combat":
            # load combat keys image (JK)
            self.image = pygame.image.load(path.join(self.game.img_dir, "combatKeys.png")).convert()
            # remove background from image
            self.image.set_colorkey((BLACK))
            # scale image to specified dimensions
            self.image = pygame.transform.scale(self.image, (75, 75))
        # check if type attribute is 'light'
        elif self.type == "light":
            # load light image
            self.image = pygame.image.load(path.join(self.game.img_dir, "light.png")).convert()
            # remove background from image
            self.image.set_colorkey((BLACK))
        # check if type attribute is 'speaker'
        elif self.type == "speaker":
            # load speaker image
            self.image = pygame.image.load(path.join(self.game.img_dir, "speaker.png")).convert()
            # remove background from image
            self.image.set_colorkey((BLACK))
            # scale image
            self.image = pygame.transform.scale(self.image, (w,h))
        # check if type attribute is 'vent'
        elif self.type == "vent":
            # load image
            self.image = pygame.image.load(path.join(self.game.img_dir, "vent.png")).convert()
            # remove background from image
            self.image.set_colorkey((BLACK))
            # scale image
            self.image = pygame.transform.scale(self.image, (w, h))

        # make image get a rectangle
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = ((x, y))

    def load_images(self):
        self.lightning_images = [pygame.image.load('img/lightning/0.png').convert(), pygame.image.load('img/lightning/1.png').convert(), pygame.image.load('img/lightning/2.png').convert(),
                                 pygame.image.load('img/lightning/3.png').convert(), pygame.image.load('img/lightning/4.png').convert(), pygame.image.load('img/lightning/5.png').convert(), 
                                 pygame.image.load('img/lightning/6.png').convert(), pygame.image.load('img/lightning/7.png').convert(), pygame.image.load('img/lightning/8.png').convert(), 
                                 pygame.image.load('img/lightning/9.png').convert(), pygame.image.load('img/lightning/10.png').convert()]

        self.lightning_list = []

        for frame in self.lightning_images:
            frame = pygame.transform.scale(frame, (self.w,self.h))
            frame.set_colorkey(BLACK)
            self.lightning_list.append(frame)

        self.door_images = [self.game.door_spritesheet.get_image(0, 60, 267, 340),
                            self.game.door_spritesheet.get_image(267, 60, 267, 340),
                            self.game.door_spritesheet.get_image(534, 60, 267, 340),
                            self.game.door_spritesheet.get_image(801, 60, 267, 340),
                            self.game.door_spritesheet.get_image(1068, 60, 267, 340),
                            self.game.door_spritesheet.get_image(1335, 60, 267, 340)]
        self.door_frames = []
        for frame in self.door_images:
            frame = pygame.transform.scale(frame, (self.w, self.h))
            frame.set_colorkey(BLACK)
            self.door_frames.append(frame)

    def animate(self):
       now = pygame.time.get_ticks()
       if self.type == "Lightning":
           if now - self.last_update > 75:
               self.last_update = now
               self.current_frame = (self.current_frame + 1) % len(self.lightning_list)
               bottom = self.rect.bottom
               self.image = self.lightning_list[self.current_frame]
               self.rect = self.image.get_rect()
               self.rect.bottom = bottom
       elif self.type == "door":
           if self.open == True:
               if now - self.last_update > 150:
                   self.last_update = now
                   bottom = self.rect.bottom
                   self.image = self.door_frames[self.current_frame]
                   self.rect = self.image.get_rect()
                   self.rect.bottom = bottom
                   if self.current_frame < 5:
                       self.current_frame += 1
                   if self.current_frame == 5:
                       if self.game.level == 1:
                           self.game.level = 2
                           self.game.levelClear = True
           else:
               self.current_frame = 0
               bottom = self.rect.bottom
               self.image = self.door_frames[self.current_frame]
               self.rect = self.image.get_rect()
               self.rect.bottom = bottom

    def update(self):
        if self.type == "Lightning":
            self.animate()
            self.rect.center = (self.x, self.y)
        elif self.type == "door":
            self.animate()
            self.rect.center = (self.x, self.y)

# setup walls
class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load(path.join(self.game.img_dir, "wall.jpg")).convert()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Pillar(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.pillars
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load(path.join(self.game.img_dir, "pillar.png")).convert()
        self.image = pygame.transform.scale(self.image, (30, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y