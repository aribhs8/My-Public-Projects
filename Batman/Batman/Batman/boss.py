import pygame
from settings import *
from bullets import *
vec = pygame.math.Vector2

class Boss(pygame.sprite.Sprite):
    # initialize boss with all attributes
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.load_images()
        
        # counters
        self.shield = 100
        self.spawnCounter = 0
        self.currentFrame = 0
        self.hitCount = 0
        self.health = 100
        self.throwFrame = 0
        self.spawnUpdate = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 3300

        # setup image
        self.image = self.spawnFrames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = (x, y)

        # setup movement + gravity
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        # animation variables
        self.direction = "L"
        self.jumping = False
        self.throwing = False
        self.dazed = False
        
    def load_images(self):
        # images that appear when level 2 starts
        self.spawnImages = [self.game.boss_spritesheet.get_image(282, 384, 105, 53),
                            self.game.boss_spritesheet.get_image(372, 972, 73, 63),
                            self.game.boss_spritesheet.get_image(450, 965, 60, 68),
                            self.game.boss_spritesheet.get_image(511, 957, 72, 78)]
        self.spawnFrames = []
        for frame in self.spawnImages:
            frame.set_colorkey((82, 134, 120))
            frame = pygame.transform.flip(frame, True, False)
            self.spawnFrames.append(frame)

        # throwing image
        self.throwImages = [self.game.boss_spritesheet.get_image(610, 385, 101, 51),
                            self.game.boss_spritesheet.get_image(715, 345, 76, 89),
                            self.game.boss_spritesheet.get_image(800, 320, 66, 114),
                            self.game.boss_spritesheet.get_image(875, 310, 66, 124),
                            self.game.boss_spritesheet.get_image(315, 467, 70, 108),
                            self.game.boss_spritesheet.get_image(390, 460, 66, 114),
                            self.game.boss_spritesheet.get_image(465, 460, 77, 114),
                            self.game.boss_spritesheet.get_image(550, 460, 70, 115),
                            self.game.boss_spritesheet.get_image(628, 510, 108, 65),
                            self.game.boss_spritesheet.get_image(740, 510, 98, 66),
                            self.game.boss_spritesheet.get_image(845, 512, 75, 65)]
        self.throwFrames_r = []
        self.throwFrames_l = []
        for frame in self.throwImages:
            frame.set_colorkey((82, 134, 120))
            self.throwFrames_l.append(frame)
            frame = pygame.transform.flip(frame, True, False)
            self.throwFrames_r.append(frame)

        # dazed image
        self.dazedImage = self.game.boss_spritesheet.get_image(82, 860, 58, 71)
        self.dazedImage.set_colorkey((82, 134, 120))
        self.dazedImage = pygame.transform.flip(self.dazedImage, True, False)

        # standstill image
        self.standingFrame_r = self.game.boss_spritesheet.get_image(10, 10, 67, 73)
        self.standingFrame_r.set_colorkey((82, 134, 120))
        self.standingFrame_l = pygame.transform.flip(self.standingFrame_r, True, False)

    def animate(self):
        now = pygame.time.get_ticks()
        if self.spawnCounter < 4:
            self.lastUpdate = pygame.time.get_ticks()
            if now - self.spawnUpdate > 400:
                self.spawnUpdate = now
                bottom = self.rect.bottom
                self.image = self.spawnFrames[self.spawnCounter]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                self.spawnCounter += 1
        else:
            if self.throwing:
                if now - self.lastUpdate > 300:
                    if self.throwFrame > 10:
                        self.throwFrame = 0
                    self.lastUpdate = now
                    bottom = self.rect.bottom
                    if self.direction == "R":
                        self.image = self.throwFrames_r[self.throwFrame]
                    elif self.direction == "L":
                        self.image = self.throwFrames_l[self.throwFrame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
                    self.throwFrame += 1

            elif self.dazed:
                if now - self.lastUpdate > 5000:
                    self.last_shot = now
                    self.lastUpdate = now
                    self.dazed = False

                bottom = self.rect.bottom
                self.image = self.dazedImage
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                

    def shoot(self, direction):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.game, self.rect.left, self.rect.top, "boulder", direction)
            self.game.boulders.add(bullet)

    def update(self):
        # apply gravity
        self.acc = vec(0, GRAV)
        # call animation method
        self.animate()

        # check for death
        if self.health <= 0:
            self.kill()
            self.game.show_win_screen()

        # attack/movement
        if self.spawnCounter >= 4:
            if self.rect.centerx > self.game.player.rect.centerx and not self.dazed:
                self.throwing = True
                self.shoot("L")
            else:
                self.throwing = False
        else:
            self.last_shot = pygame.time.get_ticks()

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0

        self.rect.midbottom = self.pos
