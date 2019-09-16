# IMPORT MODULES + FILES
# pygame
import pygame
# settings file
from settings import *

# spritesheet setup
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        # loads the spritesheet and converts it to python format
        self.spritesheet = pygame.image.load(filename).convert()

    # get_image method to extract image from spritesheet utilizing coordinates and dimensions
    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pygame.Surface((width, height))
        # blit this image
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # scale the image to width and height of the dimension parameters
        image = pygame.transform.scale(image, (width , height))
        # return the image
        return image
