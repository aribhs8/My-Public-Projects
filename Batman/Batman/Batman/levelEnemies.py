# import files + pygame
import pygame
from settings import *
from bullets import *
vec = pygame.math.Vector2

# setup non-gun wielding enemies
class meleeEnemy(pygame.sprite.Sprite):
    # initialize enemy attributes
    def __init__(self, game, x, y, range):
        self.groups = game.all_sprites, game.meleeEnemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # counters
        self.last_update = 0
        self.current_frame = 0
        self.last_attack = pygame.time.get_ticks()
        self.attack_frame = 0
        self.shield = 100
        self.health = 100

        # setup image
        self.load_images()
        self.image = self.standing_frame_r
        self.rect = self.image.get_rect()

        # setup location
        self.rect.center = ((x, y))
        self.pos = ((x, y))
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.range = range
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        # animation variables
        self.direction = None
        self.walking = False
        self.attacking = False
        self.attacked = False

    # load enemy images from spritesheet
    def load_images(self):
        self.standing_frame_r = self.game.meleeEnemy_spritesheet.get_image(1, 0, 44, 88)
        self.standing_frame_r.set_colorkey((0, 64, 128))
        self.standing_frame_r = pygame.transform.scale(self.standing_frame_r, (45, 70))
        self.standing_frame_l = pygame.transform.flip(self.standing_frame_r, True, False)

        self.walking_images_r = [(self.game.meleeEnemy_spritesheet.get_image(3, 93, 57, 79)),
                                 (self.game.meleeEnemy_spritesheet.get_image(63, 91, 54, 79)),
                                 (self.game.meleeEnemy_spritesheet.get_image(119, 89, 49, 82)),
                                 (self.game.meleeEnemy_spritesheet.get_image(168, 87, 47, 86)),
                                 (self.game.meleeEnemy_spritesheet.get_image(214, 86, 50, 89)),
                                 (self.game.meleeEnemy_spritesheet.get_image(268, 89, 50, 85)),
                                 (self.game.meleeEnemy_spritesheet.get_image(317, 89, 56, 82))]

        self.walking_frames_l = []
        self.walking_frames_r = []
        for frame in self.walking_images_r:
            frame.set_colorkey((0, 64, 128))
            frame = pygame.transform.scale(frame, (45, 70))
            self.walking_frames_r.append(frame)
            self.walking_frames_l.append(pygame.transform.flip(frame, True, False))

        self.attacking_images_r = [self.game.meleeEnemy_spritesheet.get_image(1, 172, 53, 89),
                                  self.game.meleeEnemy_spritesheet.get_image(51, 167, 59, 94),
                                  self.game.meleeEnemy_spritesheet.get_image(136, 256, 68, 82),
                                  self.game.meleeEnemy_spritesheet.get_image(204, 258, 45, 81)]
        self.attacking_frames_l = []
        self.attacking_frames_r = []
        for frame in self.attacking_images_r:
            frame.set_colorkey((0, 64, 128))
            frame = pygame.transform.scale(frame, (45, 70))
            self.attacking_frames_r.append(frame)
            self.attacking_frames_l.append(pygame.transform.flip(frame, True, False))

        self.damage_frame_r = self.game.meleeEnemy_spritesheet.get_image(46, 308, 34, 90)
        self.damage_frame_r = pygame.transform.scale(self.damage_frame_r, (30, 70))
        self.damage_frame_r.set_colorkey((0, 64, 128))
        self.damage_frame_l = pygame.transform.flip(self.damage_frame_r, True, False)

    # control enemy movement
    def move(self):
        if self.rect.centerx >= self.range and self.x != self.range:
            self.direction = "B";
        if self.rect.centerx <= self.x and self.x != self.range:
            self.direction = "F"
        
        if self.direction == "F":
            self.acc.x = ENEMY_ACC
        if self.direction == "B":
            self.acc.x = -ENEMY_ACC
        return self.acc.x
    
    # switch between enemy pictures from spritesheet
    def animate(self):
        # get current time
        now = pygame.time.get_ticks()

        # show walk animation
        if self.walking:
            self.attack_frame = 0
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_r)
                bottom = self.rect.bottom
                if self.direction == "F":
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.attacking and not self.walking and not self.attacked:
            if self.game.player.rect.x > self.rect.x:
                self.direction = "F"
            else:
                self.direction = "B"

            if now - self.last_update > 150:
                self.last_update = now
                if self.attack_frame < 4:
                    self.attack_frame += 1
                else:
                    self.attack_frame = 0
                bottom = self.rect.bottom
                if self.direction == "F":
                    self.image = self.attacking_frames_r[self.attack_frame - 1]
                else:
                    self.image = self.attacking_frames_l[self.attack_frame - 1]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if self.attacked:
             self.last_update = now
             bottom = self.rect.bottom
             if self.game.player.rect.centerx > self.rect.centerx:
                 self.image = self.damage_frame_r
             elif self.game.player.rect.centerx < self.rect.centerx:
                 self.image = self.damage_frame_l

             self.rect = self.image.get_rect()
             self.rect.bottom = bottom

    def update(self):
        # timer
        attackNow = pygame.time.get_ticks()
        self.acc = vec(0, 0)
        if not self.attacking and not self.attacked:
            self.move()
        self.animate()

        if self.health <= 0:
            self.kill()

        # set enemy state
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if abs(self.vel.x) < 0.5:
            self.vel.x = 0

        self.rect.midbottom = self.pos

    def draw_health(self):
        if self.health > 60:
            fillColor = GREEN
        elif self.health > 30:
            fillColor = YELLOW
        else:
            fillColor = RED
        width = int(self.rect.width * self.health / 100)
        self.health_bar = pygame.Rect(0, 0, width, 7)
        if self.health < 100:
            pygame.draw.rect(self.image, fillColor, self.health_bar)

class shooterEnemy(pygame.sprite.Sprite):
    # initialize enemy attributes
    def __init__(self, game, x, y, range):
        self.groups = game.all_sprites, game.shooterEnemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # counters
        self.last_update = 0
        self.current_frame = 0
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 2000
        self.attackRange = 500
        self.last_time = pygame.time.get_ticks()
        self.attack_frame = 0
        self.health = 100

        # setup image
        self.load_images()
        self.image = self.standing_frame_r
        self.rect = self.image.get_rect()

        # setup location
        self.rect.center = ((x, y))
        self.pos = ((x, y))
        self.rect.x = x
        self.rect.y = y
        self.x = x
        self.range = range
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        # animation variables
        self.direction = "F"
        self.walking = False
        self.attacking = False
        self.attacked = False

    def load_images(self):
        self.standing_frame_r = self.game.shooterEnemy_spritesheet.get_image(0, 1, 48, 69)
        self.standing_frame_r.set_colorkey(BLACK)
        self.standing_frame_r = pygame.transform.scale(self.standing_frame_r, (45, 70))
        self.standing_frame_l = pygame.transform.flip(self.standing_frame_r, True, False)

        self.walking_images_r = [self.game.shooterEnemy_spritesheet.get_image(117, 150, 45, 61),
                                 self.game.shooterEnemy_spritesheet.get_image(165, 147, 42, 65),
                                 self.game.shooterEnemy_spritesheet.get_image(215, 147, 41, 62),
                                 self.game.shooterEnemy_spritesheet.get_image(263, 148, 48, 61),
                                 self.game.shooterEnemy_spritesheet.get_image(317, 149, 48, 61),
                                 self.game.shooterEnemy_spritesheet.get_image(370, 149, 45, 62),
                                 self.game.shooterEnemy_spritesheet.get_image(420, 148, 41, 62),
                                 self.game.shooterEnemy_spritesheet.get_image(467, 147, 41, 63),
                                 self.game.shooterEnemy_spritesheet.get_image(510, 148, 47, 63),
                                 self.game.shooterEnemy_spritesheet.get_image(568, 150, 47, 62)]
        self.walking_frames_l = []
        self.walking_frames_r = []
        for frame in self.walking_images_r:
            frame.set_colorkey(BLACK)
            frame = pygame.transform.scale(frame, (45, 70))
            self.walking_frames_r.append(frame)
            self.walking_frames_l.append(pygame.transform.flip(frame, True, False))

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.direction == "F":
                bullet = Bullet(self.game, self.rect.right, self.rect.centery, "gun", "F")
                self.game.gunShots.add(bullet)
            else:
                bullet = Bullet(self.game, self.rect.left, self.rect.centery, "gun", "B")
                self.game.gunShots.add(bullet)

    # control enemy movement
    def move(self):
        if self.rect.centerx >= self.range and self.x != self.range and not self.attacking:
            self.direction = "B";
        if self.rect.centerx <= self.x and self.x != self.range and not self.attacking:
            self.direction = "F"
        
        if self.direction == "F":
            self.acc.x = ENEMY_ACC
        if self.direction == "B":
            self.acc.x = -ENEMY_ACC
        return self.acc.x

    def draw_health(self):
        if self.health > 60:
            fillColor = GREEN
        elif self.health > 30:
            fillColor = YELLOW
        else:
            fillColor = RED
        width = int(self.rect.width * self.health / 100)
        self.health_bar = pygame.Rect(0, 0, width, 7)
        if self.health < 100:
            pygame.draw.rect(self.image, fillColor, self.health_bar)

    def update(self):
        self.acc = vec(0, 0)

        if self.health <= 0:
            self.kill()
        
        # shooting
        if self.game.player.rect.centery <= self.rect.bottom and self.game.player.rect.bottom >= self.rect.top:
            if self.game.player.rect.centerx > self.x - self.attackRange and self.game.player.rect.centerx < self.range + self.attackRange:
                if self.game.player.rect.centerx < self.rect.centerx:
                    self.direction = "B"
                    self.attacking = True
                    self.walking = False
                    self.image = self.standing_frame_l
                    self.shoot()
                elif self.game.player.rect.centerx > self.rect.centerx:
                    self.direction = "F"
                    self.image = self.standing_frame_r
                    self.attacking = True
                    self.walking = False
                    self.shoot()

        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if abs(self.vel.x) < 0.5:
            self.vel.x = 0

