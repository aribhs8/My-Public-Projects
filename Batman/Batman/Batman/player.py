# import other files + pygame
import pygame
from settings import *
from bullets import *
vec = pygame.math.Vector2

# main player
class Player(pygame.sprite.Sprite):
    # initialize player with all attributes
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        # counters
        self.current_frame = 0
        self.shield = 100
        self.attack_frame = 0
        self.death_frame = 0
        self.last_update = 0
        self.quantity = 0
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 1000
        self.power = 1

        # setup image
        self.load_images()
        self.image = self.standing_frame_r
        self.rect = self.image.get_rect()
        self.direction = "R"

        # setup location
        self.rect.center = (x, y)
        self.pos = (x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0,0)

        # animation variables
        self.walking = False
        self.jumping = False
        self.attacking = False
        self.batarang = False
        self.damage = False
        self.death = False

    # load all images from spritesheet
    def load_images(self):
        # standstill image
        self.standing_frame_r = self.game.player_spritesheet.get_image(10, 20, 75, 90)
        self.standing_frame_r.set_colorkey((3, 142, 187))
        self.standing_frame_r = pygame.transform.scale(self.standing_frame_r, (45, 70))
        self.standing_frame_l = pygame.transform.flip(self.standing_frame_r, True, False)

        # air attack
        self.air_attack_frame_r = self.game.player_spritesheet.get_image(426, 260, 79, 91)
        self.air_attack_frame_r.set_colorkey((3, 142, 187))
        self.air_attack_frame_r = pygame.transform.scale(self.air_attack_frame_r, (45, 70))
        self.air_attack_frame_l = pygame.transform.flip(self.air_attack_frame_r, True, False)

        # damage image
        self.damage_frame_r = self.game.player_spritesheet.get_image(21, 838, 69, 90)
        self.damage_frame_r.set_colorkey((3, 142, 187))
        self.damage_frame_r = pygame.transform.scale(self.damage_frame_r, (45, 70))
        self.damage_frame_l = pygame.transform.flip(self.damage_frame_r, True, False)

        # death image
        self.death_frames_r = [self.game.player_spritesheet.get_image(108, 837, 78, 80),
                               self.game.player_spritesheet.get_image(203, 885, 99, 38)]
        self.death_frames_r[0] = pygame.transform.scale(self.death_frames_r[0], (45, 70))
        self.death_frames_r[1] = pygame.transform.scale(self.death_frames_r[1], (70, 45))
        self.death_frames_l = []
        for frame in self.death_frames_r:
            frame.set_colorkey((3, 142, 187))
            self.death_frames_l.append(pygame.transform.flip(frame, True, False))

        # walk images
        self.walk_images_r = [self.game.player_spritesheet.get_image(353, 11, 56, 94),
                              self.game.player_spritesheet.get_image(419, 11, 54, 94),
                              self.game.player_spritesheet.get_image(484, 12, 69, 92),
                              self.game.player_spritesheet.get_image(558, 16, 54, 91),
                              self.game.player_spritesheet.get_image(635, 15, 54, 95),
                              self.game.player_spritesheet.get_image(710, 15, 64, 92)]
        self.walk_frames_l = []
        self.walk_frames_r = []
        for frame in self.walk_images_r:
            frame.set_colorkey((3, 142, 187))
            frame = pygame.transform.scale(frame, (45, 70))
            self.walk_frames_r.append(frame)
            self.walk_frames_l.append(pygame.transform.flip(frame, True, False))

        # jump images
        self.jump_images_r = [self.game.player_spritesheet.get_image(82, 254, 54, 98),
                            self.game.player_spritesheet.get_image(157, 246, 75, 97),
                            self.game.player_spritesheet.get_image(243, 253, 73, 97)]
        self.jump_frames_l = []
        self.jump_frames_r = []
        for frame in self.jump_images_r:
            frame.set_colorkey((3, 142, 187))
            frame = pygame.transform.scale(frame, (45, 70))
            self.jump_frames_r.append(frame)
            self.jump_frames_l.append(pygame.transform.flip(frame, True, False))

        # attack images
        self.attack_images_r = [self.game.player_spritesheet.get_image(7, 128, 74, 95),
                                self.game.player_spritesheet.get_image(90, 128, 88, 94),
                                self.game.player_spritesheet.get_image(190, 128, 72, 96),
                                self.game.player_spritesheet.get_image(277, 128, 63, 91),
                                self.game.player_spritesheet.get_image(360, 137, 64, 83),
                                self.game.player_spritesheet.get_image(438, 137, 65, 83),
                                self.game.player_spritesheet.get_image(515, 137, 55, 85),
                                self.game.player_spritesheet.get_image(578, 137, 86, 85)]
        self.attack_frames_r = []
        self.attack_frames_l = []
        for frame in self.attack_images_r:
            frame.set_colorkey((3, 142, 187))
            frame = pygame.transform.scale(frame, (45, 70))
            self.attack_frames_r.append(frame)
            self.attack_frames_l.append(pygame.transform.flip(frame, True, False))

        # shoot images
        self.batarang_frame_r = self.game.player_spritesheet.get_image(255, 500, 84, 82)
        self.batarang_frame_r.set_colorkey((3, 142, 187))
        self.batarang_frame_r = pygame.transform.scale(self.batarang_frame_r, (45, 70))
        self.batarang_frame_l = pygame.transform.flip(self.batarang_frame_r, True, False)

    # control jumping
    def jump(self):
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        box_hits = pygame.sprite.spritecollide(self, self.game.boxes, False)
        self.rect.x -= 1
        if hits and not (self.rect.y > hits[0].rect.y) or box_hits:
            self.vel.y = PLAYER_JUMP
    
    # control player movement
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pygame.K_d]:
            self.acc.x = PLAYER_ACC
        return self.acc.x

    # switch between pictures in spritesheet
    def animate(self):
        # get current time
        now = pygame.time.get_ticks()

        meleeEnemyHits = pygame.sprite.spritecollide(self, self.game.meleeEnemies, False)
        shooterEnemyHits = pygame.sprite.spritecollide(self, self.game.shooterEnemies, False)
        if self.game.level == 2:
            try:
                bossHits = pygame.sprite.collide_rect(self, self.game.boss)
            except:
                None
        # show death animation
        if self.death:
            if now - self.last_update > 250:
                self.last_update = now
                if self.death_frame < 2:
                    bottom = self.rect.bottom
                    if self.direction == "R":
                        self.image = self.death_frames_r[self.death_frame]
                    else:
                        self.image = self.death_frames_l[self.death_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
                    self.death_frame += 1

        # show damage picture
        if self.damage and not self.walking and not self.jumping and not self.attacking and not self.batarang and not self.death:
            self.last_update = now
            self.current_frame = 0
            bottom = self.rect.bottom
            if self.direction == "R":
                self.image = self.damage_frame_r
            else:
                self.image = self.damage_frame_l
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

        # show jump animation
        if self.jumping and not self.death and not self.batarang and not self.attacking:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jump_frames_r)
                top = self.rect.top
                if self.vel.x > 0 or self.direction == "R":
                    self.image = self.jump_frames_r[self.current_frame]
                else:
                    self.image = self.jump_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.top = top

        # show walk animation
        if self.walking and not self.death and not self.attacking:
            self.batarang = False
            self.attacking = False
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_r)
                bottom = self.rect.bottom
                if self.vel. x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]

                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # standstill
        if not self.jumping and not self.walking and not self.attacking and not self.batarang and not self.damage and not self.death:
            self.last_update = now
            self.current_frame = 0
            bottom = self.rect.bottom
            if self.direction == "R":
                self.image = self.standing_frame_r
            else:
                self.image = self.standing_frame_l
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

        # show attack animation
        if self.attacking:
            if now - self.last_update > 200 and self.attack_frame < 3:
                self.attacking = False
                self.last_update = now
                if meleeEnemyHits or shooterEnemyHits and not self.jumping:
                    self.game.punchSound.play()
                    self.attack_frame += 1
                if self.game.level == 2:
                    if bossHits and not self.jumping:
                        self.game.punchSound.play()
                        self.attack_frame += 1

            if self.attack_frame >= 3 and self.attack_frame <=  7:
                if now - self.last_update > 60:
                    self.last_update = now
                    self.attack_frame += 1

            if self.attack_frame > 7:
                self.attack_frame = 0

            if self.jumping:
                bottom = self.rect.bottom
                if self.direction == "R":
                    self.image = self.air_attack_frame_r
                if self.direction == "L":
                    self.image = self.air_attack_frame_l
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

            else:
                bottom = self.rect.bottom
                if self.direction == "R":
                    self.image = self.attack_frames_r[self.attack_frame]
                else:
                    self.image = self.attack_frames_l[self.attack_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # batarang
        if self.batarang and not self.walking:
            if now - self.last_shot > self.shoot_delay - 150:
                self.last_update = now
                self.batarang = False
            self.current_frame = 0
            bottom = self.rect.bottom
            if self.direction == "R":
                self.image = self.batarang_frame_r
            else:
                self.image = self.batarang_frame_l

            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                if self.direction == "R":
                    bullet = Bullet(self.game, self.rect.right, self.rect.centery, "batarang", "R")
                    self.game.batarangs.add(bullet)
                else:
                    bullet = Bullet(self.game, self.rect.left, self.rect.centery, "batarang", "L")
                    self.game.batarangs.add(bullet)
            elif self.power == 2:
                if self.direction == "R":
                    bullet = Bullet(self.game, self.rect.right, self.rect.centery, "explosion", "R")
                    self.game.batarangs.add(bullet)
                    self.quantity -= 1
                else:
                    bullet = Bullet(self.game, self.rect.left, self.rect.centery, "explosion", "L")
                    self.game.batarangs.add(bullet)
                    self.quantity -=1
                if self.quantity < 1:
                    self.power = 1
       
    def update(self):
        # get player status
        # walking
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False

        # jumping
        if self.vel.y > 0 or self.vel.y < 0:
            self.jumping = True
        else:
            self.jumping = False

        # set player direction
        if self.vel.x > 0:
            self.direction = "R"
        elif self.vel.x < 0:
            self.direction = "L"
        
        # call player functions
        self.animate()
        self.acc = vec(0, GRAV)
        if not self.death:
            self.move()

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        if abs(self.vel.x) < 0.5:
            self.vel.x = 0

        self.rect.midbottom = self.pos