# Batman Game
#import modules + setup files
import pygame
import random
import time
from settings import *
from player import *
from obstacles import *
from levelEnemies import *
from collisions import *
from Explosion import *
from spritesheet import *
from pow import *
from os import path

# main game class
class Game:
    # initialize the class
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.updateLast = pygame.time.get_ticks()
        self.totalTime = pygame.time.get_ticks()
        self.batarangStun = pygame.time.get_ticks()
        self.deathTime = pygame.time.get_ticks()
        self.comboCounter = 0
        self.score = 0
        self.levelClear = False

        self.combo_font_name = pygame.font.match_font('impact')
        self.scoreHeading_font_name = pygame.font.match_font("algerian")
        self.score_font_name = pygame.font.match_font('arial')
        self.mainTitle_font_name = pygame.font.match_font('arial black')
        self.title_font_name = pygame.font.match_font('copperplate gothic bold')

        self.load_data()

    def draw_shield_bar(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        if pct > 100:
            pct = 100
        if pct > 30:
            fillColor = LIGHTBLUEFILL
        else:
            fillColor = RED
        BAR_LENGTH = 100
        BAR_HEIGHT = 20
        fill = (pct / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        behind_rect = pygame.Rect(x, y, 100, BAR_HEIGHT)
        pygame.draw.rect(surf, BLACK, behind_rect)
        pygame.draw.rect(surf, fillColor, fill_rect)
        pygame.draw.rect(surf, LIGHTBLUEOUTLINE, outline_rect, 2)

    # load images + spritesheets
    def load_data(self):
        # directories
        self.dir = path.dirname(__file__) 
        # load high score
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0 

        self.img_dir = path.join(self.dir, 'img')
        self.snd_dir = path.join(self.dir, 'snd')

        
        # spritesheets
        self.player_spritesheet = Spritesheet(path.join(self.img_dir, 'BatmanReturns.gif'))
        self.powerUp2_spritesheet = Spritesheet(path.join(self.img_dir, 'diskPowerup.png'))
        self.jail_spritesheet = Spritesheet(path.join(self.img_dir, 'level.png'))
        self.meleeEnemy_spritesheet = Spritesheet(path.join(self.img_dir, 'thug1.png'))
        self.shooterEnemy_spritesheet = Spritesheet(path.join(self.img_dir, 'shooter.png'))
        self.door_spritesheet = Spritesheet(path.join(self.img_dir, 'doorSpritesheet.png'))
        self.control_spritesheet = Spritesheet(path.join(self.img_dir, 'KeySample.png'))

        # backgrounds
        self.background = pygame.image.load(path.join(self.img_dir, 'bg.jpg')).convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.background_rect = self.background.get_rect()

        self.titleBackground = pygame.image.load(path.join(self.img_dir, "titleWallpaper.jpg")).convert()
        self.titleBackground = pygame.transform.scale(self.titleBackground, (WIDTH, HEIGHT))
        self.titleBackground_rect = self.titleBackground.get_rect()

        self.endLossBackground = pygame.image.load(path.join(self.img_dir, 'endWallpaper.jpg')).convert()
        self.endLossBackground = pygame.transform.scale(self.endLossBackground, (WIDTH, HEIGHT))
        self.endLossBackground_rect = self.endLossBackground.get_rect()

        # sound files
        self.attackPowerUp_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'attackPowerUp.wav'))
        self.healSound = pygame.mixer.Sound(path.join(self.snd_dir, 'healthHeal.wav'))

    # setup sprite groups + camera
    def new(self):
        # all sprites
        if self.level == 1:
            self.boxes = pygame.sprite.Group()
            self.lowPlatforms = pygame.sprite.Group()
            self.meleeEnemies = pygame.sprite.Group()
            self.shooterEnemies = pygame.sprite.Group()
            self.gunShots = pygame.sprite.Group()

        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()

        
        self.walls = pygame.sprite.Group()
        self.top = pygame.sprite.Group()

        self.batarangs = pygame.sprite.Group()

        self.lightning = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()

        # load sprites
        for door in DOOR_LIST:
            d = Miscellaneous(self, *door)
            self.doors.add(d)
            
        self.player = Player(self)

        for item in POWERUPS_LIST:
            p = Pow(self, *item)

        for light in LIGHTNING_LIST:
            l = Miscellaneous(self, *light)
            self.lightning.add(l)

        for plat in PLATFORM_LIST:
            p = Platform(self, *plat)
            self.platforms.add(p)

        for low_plat in LOW_PLATFORM_LIST:
            p = Platform(self, *low_plat)
            self.lowPlatforms.add(p)

        for box in BOX_LIST:
            b = Box(self, *box)

        for wall in WALLS:
            w = Wall(self, *wall)
            self.walls.add(w)

        for block in TOPBLOCK:
            b = Wall(self, *block)
            self.top.add(b)

        for enemy in MELEE_ENEMY_LIST:
            e = meleeEnemy(self, *enemy)

        for enemy in SHOOTER_ENEMY_LIST:
            e = shooterEnemy(self, *enemy)

        # setup camera
        self.camera = Camera(MAPWIDTH, MAPHEIGHT)

        # soundtrack
        pygame.mixer.music.load(path.join(self.snd_dir, 'levelTrack.ogg'))
        pygame.mixer.music.set_volume(0.4)

        self.run()

    # game loop
    def run(self):
        pygame.mixer.music.play(loops = -1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    # check if user exits window + if key is pressed
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN and not self.player.death:
                if event.key == pygame.K_w:
                    self.player.jump()
                if event.key == pygame.K_j:
                    self.player.attacking = True
                if event.key == pygame.K_k:
                    self.player.shoot()
                    self.player.batarang = True
    
    # update sprites + window
    def update(self):
        self.all_sprites.update()
        updateNow = pygame.time.get_ticks()

        collisionCheck(self)
        self.score += self.comboCounter - (self.comboCounter * (self.totalTime / 100000000))

        if not self.player.death:
            self.deathTime = updateNow

        # scan for death
        if self.player.shield <= 0:
            self.player.death = True
            if updateNow - self.deathTime > 1500:
                self.score = self.score - (self.score * self.totalTime / 100000)
                self.score = self.score - (self.score * 0.25)
                if self.score < 0:
                    self.score = 0
                self.playing = False
                pygame.mixer.music.fadeout(500)

        # update camera
        self.camera.update(self.player)

    # draw images
    def draw(self):
        self.screen.blit(self.background, self.background_rect)
        for sprite in self.all_sprites:
            if isinstance(sprite, meleeEnemy):
                sprite.draw_health()
            if isinstance(sprite, shooterEnemy):
                sprite.draw_health()

            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.draw_shield_bar(self.screen, 40, 50, self.player.shield)
        self.draw_text(self.screen, self.scoreHeading_font_name, "SCORE", 32, 730, 30, WHITE)
        self.draw_text(self.screen, self.score_font_name, str("%.2f" % self.score), 28, 725, 60, WHITE)
        if self.comboCounter > 0:
            self.draw_text(self.screen, self.combo_font_name, "x" + str(self.comboCounter), 36, 75, 100, WHITE)

        pygame.display.flip()

    def show_start_screen(self):
        pygame.mixer.music.load(path.join(self.snd_dir, 'titleTrack.ogg'))
        pygame.mixer.music.play(loops = -1)
        waiting = True
        while waiting:
            self.screen.blit(self.titleBackground, self.titleBackground_rect)
            self.draw_text(self.screen, self.mainTitle_font_name, "THE BATMAN", 48, 200, 80, WHITE)
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            
            if 0 + 250 > mouse[0] > 0 and 250 + 50 > mouse[1] > 250:
                pygame.draw.rect(self.screen, DIMGREY, (0, 250, 250, 50))
                if click[0] == True:
                    waiting = False
            else:
                pygame.draw.rect(self.screen, WHITE, (0, 250, 250, 50))

            self.draw_text(self.screen, self.title_font_name, "PLAY", 48, 120, 260, BLACK)
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
            pygame.display.flip()
        pygame.mixer.music.fadeout(1000)

    def show_go_screen(self):
        if not self.running:
            return
        self.screen.blit(self.endLossBackground, self.endLossBackground_rect)
        self.draw_text(self.screen, self.scoreHeading_font_name, "GAME OVER", 100, 400, 50, WHITE)
        self.draw_text(self.screen, self.score_font_name, "SCORE: " + str("%.2f" % self.score), 30, 610, 150, WHITE)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text(self.screen, self.score_font_name, "NEW HIGH SCORE!", 30, 600, 190, WHITE)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text(self.screen, self.score_font_name, "HIGH SCORE: " + str("%.2f" % self.highscore), 30, 573, 190, WHITE)
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if 550 + 250 > mouse[0] > 550 and 250 + 50 > mouse[1] > 250:
                pygame.draw.rect(self.screen, DIMGREY, (550, 250, 250, 50))
                if click[0] == True:
                    self.score = 0
                    waiting = False
            else:
                pygame.draw.rect(self.screen, WHITE, (550, 250, 250, 50))
            if 550 + 250 > mouse[0] > 550 and 300 + 50 > mouse[1] > 300:
                pygame.draw.rect(self.screen, DIMGREY, (550, 300, 250, 50))
                if click[0] == True:
                    self.score = 0
                    waiting = False
                    self.show_start_screen()
            else:
                pygame.draw.rect(self.screen, WHITE, (550, 300, 250, 50))
            pygame.draw.line(self.screen, BLACK, (550, 300), (800, 300), 4)
            self.draw_text(self.screen, self.title_font_name, "RETRY", 48, 680, 260, BLACK)
            self.draw_text(self.screen, self.title_font_name, "MAIN MENU", 48, 680, 310, BLACK)
            self.clock.tick(FPS)
            pygame.display.flip()

    def draw_text(self, surf, style, text, size, x, y, color):
        font = pygame.font.Font(style, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

# camera setup 
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.pos.x + int(WIDTH / 2)
        y = -target.pos.y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x) # left
        y = min(0, y) # top
        x = max(-(self.width - WIDTH), x) # right
        y = max(-(self.height - HEIGHT), y) # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height)

# call game class 
g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pygame.quit()
