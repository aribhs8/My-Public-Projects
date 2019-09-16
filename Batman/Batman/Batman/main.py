# BATMAN GAME
# 1800+ lines of code
# Attempted to add comments to every single line of code
# Credits
    # creator of game: Arib Hussain
    # batman sprites: SNES Batman Returns - (http://spritedatabase.net/file/7419/Batman)
    # bane sprites: Batman Brave and the bold - (http://spritedatabase.net/files/ds/2647/Sprite/Bane.png)
    # lightning sprites: Calinou - (https://opengameart.org/content/lightning-animation)
    # meleeEnemy sprites: Vendetta - (https://www.spriters-resource.com/arcade/vendetta/sheet/59916/)
    # shootrEnemy sprites: Halo - (https://www.codeproject.com/Articles/756189/Master-Chief-CreateJS-TypeScript)
    # Reference Code: Jumpy! A platformer game - kidcancode (http://kidscancode.org/lessons/)
    # Reference Code: SHMUP! - kidscancode (http://kidscancode.org/lessons/)
    # Reference Code: TileMap Demo - kidscancode (http://kidscancode.org/lessons/)

# IMPORT MODULES + FILES
# pygame
import pygame
# import functions of random
import random
# settings file
from settings import *
# player sprite
from player import *
# boss sprite
from boss import *
# obstacles (platforms, lightining, boxes, etc.) file
from obstacles import *
# enemy sprites
from levelEnemies import *
# collision detection file
from collisions import *
# explosion sprit 
from Explosion import *
# file to access sprites in spritesheets
from spritesheet import *
# file that spawns powerups
from pow import *
# import path from os to find files regardless of operating system
from os import path

# main game class
class Game:
    # initialize the class
    def __init__(self):
        # PYGAME + LOOP SETUP
        # initializes pygame
        pygame.init()
        # initializes the mixer in pygame
        pygame.mixer.init()
        # sets the screen resolution
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # sets the title of the game window
        pygame.display.set_caption(TITLE)
        # keeps track of time in pygame (Used for frame rate)
        self.clock = pygame.time.Clock()
        # set the running variable to true (used to control run method)
        self.running = True

        # COUNTERS
        # variable to check the difference between time elapsed and certain instances of the program
        self.updateLast = pygame.time.get_ticks()
        # used to check the total time elapsed since the program began to run
        self.totalTime = pygame.time.get_ticks()
        # variable used to control stun duration
        self.batarangStun = pygame.time.get_ticks()
        # variable used to control death animation
        self.deathTime = pygame.time.get_ticks()
        # initalizes combo variable
        self.comboCounter = 0
        # initalizes score variable
        self.score = 0
        # initialize level of game
        self.level = 1

        # initalizes levelClear variable (used to see if level should change)
        self.levelClear = False

        # FONTS
        # font used for combo count
        self.combo_font_name = pygame.font.match_font('impact')
        # font used for SCORE Heading on top of score
        self.scoreHeading_font_name = pygame.font.match_font("algerian")
        # font used for the score
        self.score_font_name = pygame.font.match_font('arial')
        # font used for the title on the title screen
        self.mainTitle_font_name = pygame.font.match_font('arial black')
        # font used on button on title and gameOver screens
        self.button_font_name = pygame.font.match_font('copperplate gothic bold')

        # calls load data method
        self.load_data()

    def draw_shield_bar(self, surf, x, y, pct, type):
        if pct < 0:
            pct = 0
        if pct > 100:
            pct = 100
        if type == "player":
            if pct > 30:
                fillColor = LIGHTBLUEFILL
            else:
                fillColor = RED
            BAR_LENGTH = 100
            BAR_HEIGHT = 20
            fill = (pct / 100) * BAR_LENGTH
            fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
            behind_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
            outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
            pygame.draw.rect(surf, BLACK, behind_rect)
            pygame.draw.rect(surf, fillColor, fill_rect)
            pygame.draw.rect(surf, LIGHTBLUEOUTLINE, outline_rect, 2)
            
        elif type == "boss":
            if pct > 30: 
                fillColor = (255, 60, 60)
            else:
                fillColor = WHITE
            BAR_LENGTH = 600
            BAR_HEIGHT = 20
            fill = (pct / 100) * BAR_LENGTH
            fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
            behind_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
            pygame.draw.rect(surf, BLACK, behind_rect)
            pygame.draw.rect(surf, fillColor, fill_rect)
            outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
            pygame.draw.rect(surf, YELLOW, outline_rect, 2)

    # load images + spritesheets
    def load_data(self):
        # DIRECTORIES
        # checks current folder
        self.dir = path.dirname(__file__)
        # HIGHSCORE
        # load HS_File and read line inside file
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            # python will try to read the contents of the file
            try:
                self.highscore = float(f.read())
            # if no integer exists in the file, highscore will be equal to 0
            except:
                self.highscore = 0 
        # looks for image folder in current folder
        self.img_dir = path.join(self.dir, 'img')
        # looks for sound folder in curent folder
        self.snd_dir = path.join(self.dir, 'snd')


        # SPRITESHEETS
        # calls spritesheet class on the player's spritesheet
        self.player_spritesheet = Spritesheet(path.join(self.img_dir, 'BatmanReturns.gif'))
        # calls spritesheet class on boss's spritesheet
        self.boss_spritesheet = Spritesheet(path.join(self.img_dir, 'Bane.png'))
        # calls spritesheet class on explosive disk spritesheet
        self.powerUp2_spritesheet = Spritesheet(path.join(self.img_dir, 'diskPowerup.png'))
        # calls spritesheet class on 'jail' spritesheet (includes platforms and boxes)
        self.jail_spritesheet = Spritesheet(path.join(self.img_dir, 'level.png'))
        # calls spritesheet class on melee enemy's spritesheet (enemies with knives)
        self.meleeEnemy_spritesheet = Spritesheet(path.join(self.img_dir, 'thug1.png'))
        # calls spritesheet class on shooter enemy's spritesheet (Halo enemies - with guns) 
        self.shooterEnemy_spritesheet = Spritesheet(path.join(self.img_dir, 'shooter.png'))
        # calls spritesheet class on door spritesheet (opening and closing door animation
        self.door_spritesheet = Spritesheet(path.join(self.img_dir, 'doorSpritesheet.png'))

        # BACKGROUNDS
        # LEVEL BACKGROUND
        # loads the background and converts it to python format
        self.background = pygame.image.load(path.join(self.img_dir, 'bg.jpg')).convert()
        # scales the background to match the size of the screen
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        # gives the background a rectangle
        self.background_rect = self.background.get_rect()
        # TITLE BACKGROUND
        # loads the background and converts it to python format
        self.titleBackground = pygame.image.load(path.join(self.img_dir, "titleWallpaper.jpg")).convert()
        # scales the background to match the size of the screen
        self.titleBackground = pygame.transform.scale(self.titleBackground, (WIDTH, HEIGHT))
        # gives the background a rectangle
        self.titleBackground_rect = self.titleBackground.get_rect()
        # GAME OVER SCREEN BACKGROUND
        # loads the background and converts it to python format
        self.endLossBackground = pygame.image.load(path.join(self.img_dir, 'endWallpaper.jpg')).convert()
        # scales the background to match the size of the screen
        self.endLossBackground = pygame.transform.scale(self.endLossBackground, (WIDTH, HEIGHT))
        # gives the background a rectangle
        self.endLossBackground_rect = self.endLossBackground.get_rect()
        # WIN SCREEN BACKGROUND
        # loads the background and converts it to python format
        self.winBackground = pygame.image.load(path.join(self.img_dir, 'winWallpaper.jpg')).convert()
        self.winBackground = pygame.transform.scale(self.winBackground, (WIDTH, HEIGHT))
        self.winBackground_rect = self.winBackground.get_rect()

        # BASIC IMAGES (NOT SPRITES USED IN GAME)
        # BOMB IMAGE
        # loads image of bomb and convert it to python format
        self.bomb = pygame.image.load(path.join(self.img_dir, 'disks.png')).convert()
        # removes the black background around the image
        self.bomb.set_colorkey((BLACK))
        # scales the image to a certain size
        self.bomb_image = pygame.transform.scale(self.bomb, (40, 40))
        # gives the image a rectangle
        self.bomb_rect = self.bomb_image.get_rect()
        # moves the image to a particular location
        self.bomb_rect = self.bomb_rect.move(150, 40)
        # BATARANG IMAGE
        # loads the image and converts it to python format
        self.batarang_image = pygame.image.load(path.join(self.img_dir, 'batarang.jpg')).convert()
        # removes the white background around the image
        self.batarang_image.set_colorkey(WHITE)
        # scales the image to a particular size
        self.batarang_image = pygame.transform.scale(self.batarang_image, (40, 40))
        # gives the image a rectangle
        self.batarang_rect = self.batarang_image.get_rect()
        # moves the image to a particular location
        self.batarang_rect = self.batarang_rect.move(150, 40)

        # SOUND FILES
        # sound when getting bomb powerup 
        self.attackPowerUp_sound = pygame.mixer.Sound(path.join(self.snd_dir, 'attackPowerUp.wav'))
        # sound when getting shield powerup
        self.healSound = pygame.mixer.Sound(path.join(self.snd_dir, 'healthHeal.wav'))
        # sound when explosive disk makes contact with enemy
        self.explosionSound = pygame.mixer.Sound(path.join(self.snd_dir, 'explosionSound.wav'))
        # punching enemy sound
        self.punchSound = pygame.mixer.Sound(path.join(self.snd_dir, 'punchSound.wav'))

    # setup sprite groups + camera
    def new(self):
        # SPRITE GROUPS
        # stores every single sprite
        self.all_sprites = pygame.sprite.Group()
        # stores all platform sprites
        self.platforms = pygame.sprite.Group()
        # stores all wall sprites
        self.walls = pygame.sprite.Group()
        # stores all 'roof' sprites
        self.top = pygame.sprite.Group()
        # stores all batarang sprites
        self.batarangs = pygame.sprite.Group()
        # stores all explosion sprites
        self.explosions = pygame.sprite.Group()
        # stores all box sprites
        self.boxes = pygame.sprite.Group()
        # stores all meleeEnemy sprites
        self.meleeEnemies = pygame.sprite.Group()
        # stores all gunWielding enemy sprites
        self.shooterEnemies = pygame.sprite.Group()
        # stores bullets shot by gunWielding sprites
        self.gunShots = pygame.sprite.Group()
        # stores lightning sprites
        self.lightning = pygame.sprite.Group()
        # stores the power-up sprites
        self.powerups = pygame.sprite.Group()
        # stores the door sprites
        self.doors = pygame.sprite.Group()
        # stores the boulders thrown by Bane spries
        self.boulders = pygame.sprite.Group()
        # stores the pillar spirtes used in level 2
        self.pillars = pygame.sprite.Group()
        
        # checks if the game's level is 1
        if self.level == 1:
            # LOAD SPRITES
            # creates the Miscellaneous class on the PA sprite
            Miscellaneous(self, 400, 150, 64, 64, "speaker")
            # checks each vent in the VENT_LIST
            for vent in VENT_LIST:
                # calls the Miscellaneous class on the vent sprites
                Miscellaneous(self, *vent)
            # checks each light in the LIGHT_LIST
            for light in LIGHT_LIST:
                # calls the Miscellaneous class on the light sprites
                Miscellaneous(self, *light)
            # checks each key in the KEY_LIST
            for key in KEY_LIST:
                # calls the Miscellaneous class on the key sprites
                Miscellaneous(self, *key)
            # calls the Miscellaneous class on the door sprite
            d = Miscellaneous(self, 150, 1080, 60, 100, "door")
            # adds the door to the 'doors' sprite group
            self.doors.add(d)
            # creates a player sprite and specifies coordinates (x, y parameters)
            self.player = Player(self, WIDTH / 10, HEIGHT / 4)
            # calls the Miscellaneous class on the lightning sprite
            l = Miscellaneous(self, 855, 625, 200, 75, "Lightning")
            # adds the lightning sprite to the 'lightning' sprite group
            self.lightning.add(l)
            # checks each box in the PLATFORM_LIST
            for plat in PLATFORM_LIST:
                # calls the Platform class on the item
                p = Platform(self, *plat)
                # adds the platform sprite to the platforms sprite group
                self.platforms.add(p)
            # checks each box in the BOX_LIST
            for box in BOX_LIST:
                # calls the box class on the item
                Box(self, *box)
            # checks each item in the POWERUPS_LIST
            for item in POWERUPS_LIST:
                # calls the Pow class on the item
                Pow(self, *item)
            # checks each enemy in the MELEE_ENEMY_LIST
            for enemy in MELEE_ENEMY_LIST:
                # calls the meleeEnemy class on the enemy
                meleeEnemy(self, *enemy)
            # checks each enemy in the SHOOTER_ENEMY_LIST
            for enemy in SHOOTER_ENEMY_LIST:
                # calls the shooterEnemy class on the enemy
                shooterEnemy(self, *enemy)
            # checks each wall in WALLS (list)
            for wall in WALLS:
                # calls Wall class on wall
                w = Wall(self, *wall)
                # add wall sprite to walls
                self.walls.add(w)

            # LEVEL 1 SOUNDTRACK
            # loads the soundtrack
            pygame.mixer.music.load(path.join(self.snd_dir, 'levelTrack.ogg'))
            # lowers the volume of the soundtrack
            pygame.mixer.music.set_volume(0.4)

            # setup camera
            self.camera = Camera(MAPWIDTH, MAPHEIGHT)

        # if the level is the boss level
        else:
            # LEVEL 2 SOUNDTRACK 
            # loads the soundtrack
            pygame.mixer.music.load(path.join(self.snd_dir, 'bossTrack.ogg'))
            # lowers the volume of the soundtrack
            pygame.mixer.music.set_volume(0.4)

            # LOAD SPRITES
            # calls the Miscellaneous class on the door
            Miscellaneous(self, 100, 250, 60, 100, "door")
            # creates a player sprite
            self.player = Player(self, 100, 290)
            # creates a boss sprite
            self.boss = Boss(self, 700, 300)
            # checks each pillar in the PILLAR_LIST_LEVEL2
            for pillar in PILLAR_LIST_LEVEL2:
                # calls Pillar class on the pillar
                Pillar(self, *pillar)
            # checks each plat in PLATFORM_LIST_LEVEL2
            for plat in PLATFORM_LIST_LEVEL2:
                # calls the Platform class on the plat
                p = Platform(self, *plat)
                # adds the platform sprite to the platforms sprite group
                self.platforms.add(p)
            # checks each item in the WALLS_LEVEL2 (list)
            for wall in WALLS_LEVEL2:
                # calls Wall class on wall
                w = Wall(self, *wall)
                # adds the wall to the walls sprite group
                self.walls.add(w)

            # sets up camera for level 2
            self.camera = Camera(800, 900)
                        
        # adds the roof to both levels
        for block in TOPBLOCK:
            b = Wall(self, *block)
            self.top.add(b)

        # calls the run method
        self.run()

    # game loop
    def run(self):
        # plays whatever sountrack is loaded
        pygame.mixer.music.play(loops = -1)
        # sets the playing variable to True
        self.playing = True
        # loop that keeps going as long as self.playing is True
        while self.playing:
            # controls the frame rate of the game
            self.clock.tick(FPS)
            # checks each event in the game
            self.events()
            # updates the game
            self.update()
            # draws each sprite/image in the game
            self.draw()

    # check if user exits window + if key is pressed
    def events(self):
        # checks each event in all of the events taken place since the game started
        for event in pygame.event.get():
            # checks if window is closed
            if event.type == pygame.QUIT:
                # checks if user is playing
                if self.playing:
                    # sets playing variable to False
                    self.playing = False
                # sets the running variable to False (stops loop)
                self.running = False
            # checks if a key is pressed and the user is still alive
            if event.type == pygame.KEYDOWN and not self.player.death:
                # checks if the user presses w
                if event.key == pygame.K_w:
                    # calls the jump method on the player sprite stored in the Player class
                    self.player.jump()
                # checks if the user presses j
                if event.key == pygame.K_j:
                    # sets the player's attacking variable to True (used to control animation + see if opponent should take damage)
                    self.player.attacking = True
                # checks if user presses k
                if event.key == pygame.K_k:
                    # calls the shoot method on the player sprite stored in the Player class
                    self.player.shoot()
                    # sets the plauer's batarang variable to True (used to control animation)
                    self.player.batarang = True
    
    # update sprites + window
    def update(self):
        # updates all sprites store in all_sprites group
        self.all_sprites.update()
        # checks time elapsed (gathers milliseconds since start; stopwatch)
        updateNow = pygame.time.get_ticks()
        # calculates score using specially created equation
        self.score += self.comboCounter - (self.comboCounter * (self.totalTime / 100000000))

        # CLEARING LEVELS
        # checks if all contents of level should be erased
        if self.levelClear:
            # checks each sprite in platform sprite group
            for sprite in self.platforms:
                # kills all the sprites
                sprite.kill()
            # checks each sprite in the lightning sprite group
            for sprite in self.lightning:
                # kills all the sprites
                sprite.kill()
            # checks each sprite in the powerups sprite group
            for sprite in self.powerups:
                # kills all the sprites
                sprite.kill()
            # checks each sprite in the meleeEnemies sprite group
            for sprite in self.meleeEnemies:
                # kills all the sprites
                sprite.kill()
            # checks each sprite in the shooterEnemies sprite group
            for sprite in self.shooterEnemies:
                # kills all the sprites
                sprite.kill()
            # checks each sprite in the all_sprites group
            for sprite in self.all_sprites:
                # kills all the sprites
                sprite.kill()
            # sets levelClear variable to False
            self.levelClear = False
            # calls the new method
            self.new()

        # updates deathTime variable as long as the player is not dead (used for animation)
        if not self.player.death:
            # sets deathTime equal to timeElapsed
            self.deathTime = updateNow

        # calls the collisionCheck method from the collision file
        collisionCheck(self)

        # scan for death
        if self.player.shield <= 0:
            # sets the player's death variable equal to true
            self.player.death = True
            # checks the difference between the current time and the deathTime
            if updateNow - self.deathTime > 1500:
                # decreases the score by a certain amount (depending on how much time elapsed)
                self.score = self.score - (self.score * self.totalTime / 100000)
                # decreases the score by 25%
                self.score = self.score - (self.score * 0.25)
                # checks if the score is less than 0
                if self.score < 0:
                    # prevent score from going below 0
                    self.score = 0
                # sets playing variable to False
                self.playing = False
                # makes the music fadeout
                pygame.mixer.music.fadeout(500)

        # update camera
        self.camera.update(self.player)

    # draw images
    def draw(self):
        # blits the level background
        self.screen.blit(self.background, self.background_rect)

        # checks each sprite in the all_sprites group
        for sprite in self.all_sprites:
            # if the sprite (player) has ever attacked any of the melee enemy sprites
            if isinstance(sprite, meleeEnemy):
                # draws the sprite's health
                sprite.draw_health()
            # if the sprite (player) has ever attacked any of the shooter enemy sprites
            if isinstance(sprite, shooterEnemy):
                # draws the sprite's health
                sprite.draw_health()
            # blits the sprite's image and calls the apply method from the camera object on the sprite
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        # HEALTH BAR
        # draws the player's health bar
        self.draw_shield_bar(self.screen, 40, 50, self.player.shield, "player")
        # checks if the level is equal to two
        if self.level == 2:
            # draws the boss's health bar
            self.draw_shield_bar(self.screen, 40, 550, self.boss.health, "boss")
            # calls the draw_text method and writes Bane next to health bar
            self.draw_text(self.screen, self.score_font_name, "BANE", 28, 700, 542, WHITE)

        # SCORE + COMBOS
        # calls the draw_text method and writes SCORE in the top right
        self.draw_text(self.screen, self.scoreHeading_font_name, "SCORE", 32, 730, 30, WHITE)
        # calls the draw_text method and writes the score underneath the SCORE
        self.draw_text(self.screen, self.score_font_name, str("%.2f" % self.score), 28, 725, 60, WHITE)
        # checks if the comboCounter is more than 0
        if self.comboCounter > 0:
            # calls the draw_text method and writes the comboCounter value under the player's health bar
            self.draw_text(self.screen, self.combo_font_name, "x" + str(self.comboCounter), 36, 75, 100, WHITE)

        # DRAWS POWER UP NEXT TO HEALTH BAR
        # checks if the player has batarangs
        if self.player.power == 1 or self.player.quantity - 1 <= 0:
            # draws the batarang image
            self.screen.blit(self.batarang_image, self.batarang_rect)
            # writes quantity of batarangs next to batarang image
            self.draw_text(self.screen, self.combo_font_name, "∞", 28, 190, 50, WHITE)
        # checks if player has explosive disks (bombs)
        if self.player.power == 2 and self.player.quantity - 1 > 0:
            # draws the bomb image
            self.screen.blit(self.bomb_image, self.bomb_rect)
            # writes quantity of bombs next to bomb image
            self.draw_text(self.screen, self.combo_font_name, "x" + str(self.player.quantity - 1), 28, 190, 80, WHITE)

        # *after* drawing everything, flip the screen
        pygame.display.flip()

    # win screen
    def show_win_screen(self):
        pygame.mixer.music.fadeout(500)
        self.screen.blit(self.winBackground, self.winBackground_rect)
        # calls the draw_text method and writes the score at the specified position
        self.draw_text(self.screen, self.score_font_name, "SCORE: " + str("%.2f" % self.score), 30, 590, 190, WHITE)
        # checks if the value of the score variable is greater than the highscore
        if self.score > self.highscore:
            # assigns highscore to score
            self.highscore = self.score
            # calls the draw_text method and writes 'NEW HIGH SCORE!' at the specified position
            self.draw_text(self.screen, self.score_font_name, "NEW HIGH SCORE!", 30, 530, 230, WHITE)
            # opens the HS_FILE and writes the new score as the high score
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        # if the value of score is less than or equal to the highscore
        else:
            # calls the draw_text method and writes the high score at the specified position
            self.draw_text(self.screen, self.score_font_name, "HIGH SCORE: " + str("%.2f" % self.highscore), 30, 550, 230, WHITE)
        self.draw_text(self.screen, self.score_font_name, "Please close the window to continue", 36, 400, 50, WHITE)
        self.draw_text(self.screen, self.mainTitle_font_name, "YOU WIN!", 48, WIDTH / 2, 100, WHITE)
        # *after* drawing everything flip the display
        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
        if not waiting:
            pygame.quit()

    # title screen
    def show_start_screen(self):
        # SOUNDTRACK
        # loads soundtrack
        pygame.mixer.music.load(path.join(self.snd_dir, 'titleTrack.ogg'))
        # plays soundtrack
        pygame.mixer.music.play(loops = -1)
        # variable to control loop
        waiting = True
        # while loop that runs as long as waiting is True
        while waiting:
            # blits titleBackground
            self.screen.blit(self.titleBackground, self.titleBackground_rect)
            # call draw_text method to write 'THE BATMAN' at a specified portion of the screen
            self.draw_text(self.screen, self.mainTitle_font_name, "THE BATMAN", 48, 200, 80, WHITE)

            # MOUSE CONTORLS
            # gets position of mouse
            mouse = pygame.mouse.get_pos()
            # checks if mouse is clicked
            click = pygame.mouse.get_pressed()
            # checks if location of mouse is inside a button
            if 0 + 250 > mouse[0] > 0 and 250 + 50 > mouse[1] > 250:
                # draws a rectangle and makes it color DIMGREY
                pygame.draw.rect(self.screen, DIMGREY, (0, 250, 250, 50))
                # checks if the mouse is clicked
                if click[0] == True:
                    # sets the waiting variable to false (loop ends)
                    waiting = False
            # if the mouse is not in the specified position
            else:
                # draws a rectangle and makes it colork WHITE
                pygame.draw.rect(self.screen, WHITE, (0, 250, 250, 50))

            # calls the draw_text method and writes 'PLAY' at the specified location
            self.draw_text(self.screen, self.button_font_name, "PLAY", 48, 120, 260, BLACK)
            # controls the frame rate of the game
            self.clock.tick(FPS)
            # checks each event in all of the events in the game
            for event in pygame.event.get():
                # checks if the window is closed
                if event.type == pygame.QUIT:
                    # sets the running variable to False (stops run loop)
                    self.running = False
                    # sets the waiting variable to False (stops start screen)
                    waiting = False
            # *after* drawing everything, flip the display
            pygame.display.flip()
        # fades out title music in 500 ms
        pygame.mixer.music.fadeout(1000)

    # game over screen
    def show_go_screen(self):
        # checks if program is running
        if not self.running:
            # if not running, return to the title screen
            return
        # blits the game over background
        self.screen.blit(self.endLossBackground, self.endLossBackground_rect)
        # calls the draw_text method and writes 'GAME OVER' at the specified position
        self.draw_text(self.screen, self.scoreHeading_font_name, "GAME OVER", 100, 400, 50, WHITE)
        # calls the draw_text method and writes the score at the specified position
        self.draw_text(self.screen, self.score_font_name, "SCORE: " + str("%.2f" % self.score), 30, 610, 150, WHITE)
        # checks if the value of the score variable is greater than the highscore
        if self.score > self.highscore:
            # assigns highscore to score
            self.highscore = self.score
            # calls the draw_text method and writes 'NEW HIGH SCORE!' at the specified position
            self.draw_text(self.screen, self.score_font_name, "NEW HIGH SCORE!", 30, 600, 190, WHITE)
            # opens the HS_FILE and writes the new score as the high score
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        # if the value of score is less than or equal to the highscore
        else:
            # calls the draw_text method and writes the high score at the specified position
            self.draw_text(self.screen, self.score_font_name, "HIGH SCORE: " + str("%.2f" % self.highscore), 30, 573, 190, WHITE)
        # variable to control loop
        waiting = True
        # while loop that runs as long as waiting is True
        while waiting:
            # checks each event in all pygame events
            for event in pygame.event.get():
                # if window is closed
                if event.type == pygame.QUIT:
                    # set running variable to control loop to False
                    self.running = False
                    # set waiting variable to False (stop game over screen)
                    waiting = False
            # MOUSE SETTINGS
            # gets mouse position
            mouse = pygame.mouse.get_pos()
            # checks if mouse is clicked
            click = pygame.mouse.get_pressed()

            # RETRY BUTTON
            # if mouse is in a specified position (in area of rectangle)
            if 550 + 250 > mouse[0] > 550 and 250 + 50 > mouse[1] > 250:
                # draws rectangle (button) w/ color change
                pygame.draw.rect(self.screen, DIMGREY, (550, 250, 250, 50))
                # checks if mouse is clicked
                if click[0] == True:
                    # sets the score to 0
                    self.score = 0
                    # sets the waiting variable (loop in game over screen) to False
                    waiting = False
            # if the mouse is not in the specified position
            else:
                # draw the original rectangle (button)
                pygame.draw.rect(self.screen, WHITE, (550, 250, 250, 50))

            # calls the draw_text method and writes 'PLAY' in the specified position
            self.draw_text(self.screen, self.button_font_name, "RETRY", 48, 680, 260, BLACK)

            # MAIN MENU BUTTON
            # if mouse is in a specified position (in area of rectangle)
            if 550 + 250 > mouse[0] > 550 and 300 + 50 > mouse[1] > 300:
                # draw rectangle (button) w/ color change
                pygame.draw.rect(self.screen, DIMGREY, (550, 300, 250, 50))
                # if the mouse is pressed
                if click[0] == True:
                    # set the score to 0
                    self.score = 0
                    # change the waiting variable (to control game over screen) to False
                    waiting = False
                    # calls the show_start_screen() method
                    self.show_start_screen()
            # if mouse is not in the specified position (not in area of rectangle)
            else:
                # draw the original rectangle (button)
                pygame.draw.rect(self.screen, WHITE, (550, 300, 250, 50))

            # calls the draw_text method and writes 'MAIN MENU' in the specified position
            self.draw_text(self.screen, self.button_font_name, "MAIN MENU", 48, 680, 310, BLACK)

            # draw a BLACK line seperating the two buttons
            pygame.draw.line(self.screen, BLACK, (550, 300), (800, 300), 4)
            
            # sets the frame rate
            self.clock.tick(FPS)
            # *after* drawing everything flip the image
            pygame.display.flip()

    # FUNCTION TAKEN FROM: SHMUP! (VIEW TOP FOR MORE INFORMATION)
    def draw_text(self, surf, style, text, size, x, y, color):
        font = pygame.font.Font(style, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

# CAMERA TAKEN FROM: TileMap Demo (VIEW TOP FOR MORE INFORMATION)
# camera setup
class Camera:
    # initalizes camer
    def __init__(self, width, height):
        # creates a rectangle the size of the width and height parameters
        self.camera = pygame.Rect(0, 0, width, height)
        # creates a width attribute for the class
        self.width = width
        # creates a height attibute for the class
        self.height = height

    # apply method, used to apply camera on sprites
    def apply(self, entity):
        # moves camera
        return entity.rect.move(self.camera.topleft)

    # update method
    def update(self, target):
        # changes the x-pos of the sprites
        x = -target.pos.x + int(WIDTH / 2)
        # changes the y-pos of the sprites
        y = -target.pos.y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x) # left
        y = min(0, y) # top
        x = max(-(self.width - WIDTH), x) # right
        y = max(-(self.height - HEIGHT), y) # bottom
        self.camera = pygame.Rect(x, y, self.width, self.height) # draws the updated camera rect

# call game class 
g = Game()
# show the title screen
g.show_start_screen()
# checks if the game is running
while g.running:
    # call the new method in the game class
    g.new()
    # call the gamer over method in the game class
    g.show_go_screen()

# quit pygame
pygame.quit()
