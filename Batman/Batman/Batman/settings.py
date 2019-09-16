# GAME OPTIONS AND SETTINGS

# DEFINE COLORS
# white
WHITE = (255, 255, 255)
# black
BLACK = (0, 0, 0)
# red
RED = (255, 0, 0)
# green
GREEN = (0, 255, 0)
# blue
BLUE = (0, 0, 255)
# yellow
YELLOW = (255, 255, 0)
# grey
DIMGREY = (105, 105, 105)
# brown
LIGHTBROWN = (181, 101, 29)
# lightBlue (player health bar outline)
LIGHTBLUEOUTLINE = (134, 200, 216)
# lightBlue (player health bar fill)
LIGHTBLUEFILL = (205, 255, 255)

# SCREEN SETTINGS
# title of game
TITLE = "THE BATMAN"
# width of screen
WIDTH = 800
# height of screen
HEIGHT = 600
# frame rate
FPS = 30
# width of map
MAPWIDTH = 1920
# height of map
MAPHEIGHT = 1140

# high score
HS_FILE = "highscore.txt"

# PLAYER PROPERTIES
# gravity
GRAV = 0.5
# friction on player
PLAYER_FRICTION = -0.12
# acceleration of player
PLAYER_ACC = 0.75
# player jumping velocity
PLAYER_JUMP = -10

# LEVEL 1
# player powerups
POWERUPS_LIST = [("explosion", 1400, 450),
                 ("shield", 1195, 750)]

# GAME OBSTACLES
# list of platforms
PLATFORM_LIST = [(20, 300, 480, 80),
                 (500, 300, 480, 80),
                 (980, 368, 300, 10),
                 (1280, 300, 440, 80),
                 (200, 570, 530, 80),
                 (730, 638, 250, 10),
                 (980, 570, 480, 80),
                 (1460, 570, 275, 80),
                 (1350, 490, 100, 10),
                 (1735, 638, 185, 10),
                 (25, 680, 80, 25),
                 (20, 860, 600, 80),
                 (620, 928, 200, 10),
                 (820, 860, 900, 80),
                 (25, 1130, 1880, 10)]

# list of boxes
BOX_LIST = [(150, 220, 90, 80, "horizontal"),
            (1640, 160, 85, 140, "vertical"),
            (1500, 490, 90, 80, "horizontal"),
            (150, 800, 90, 60, "horizontal"),
            (1150, 800, 90, 60, "horizontal")]

# list of lights
LIGHT_LIST = [(600, 150, 64, 64, "light"),
              (900, 150, 64, 64, "light"),
              (1200, 150, 64, 64, "light"),
              (1500, 150, 64, 64, "light"),
              (600, 800, 64, 64, "light")]

# list of vents
VENT_LIST = [(1800, 100, 64, 64, "vent"),
             (100, 500, 64, 64, "vent")]

# list of keys
KEY_LIST = [(100, 150, 100, 100, "move"),
            (200, 150, 100, 100, "combat")]

# ENEMIES
# list of melee enemies
MELEE_ENEMY_LIST = [(330, 302, 600),
              (1320, 302, 1540),
              (1380, 492, 1430),
              (1625, 572, 1700),
              (1100, 572, 1400),
              (330, 572, 600),
              (270, 572, 500),
              (240, 572, 560),
              (1400, 865, 1630),
              (1380, 865, 1600),
              (1420, 865, 1620),
              (1450, 865, 1625)]

# list of shooter enemies
SHOOTER_ENEMY_LIST = [(1500, 302, 1600),
                      (400, 860, 600),
                      (900, 860, 1100)]

# WALL SETUP
# y_coord of wall
y_coord = 0
# x_coord of wall
x_coord = 0
# list of walls
WALLS = []
# list of topblocks
TOPBLOCK = []
# loop to make sure all walls are added
while y_coord < MAPHEIGHT:
    # adds coordinates to walls list
    WALLS += [(0, y_coord)]
    # increments y_coord by 20
    y_coord += 20

# y_coord of wall 
y_coord = 0
# loop to make sure all the walls are added
while y_coord < MAPHEIGHT:
    # added coordinates to walls list
    WALLS += [(1900, y_coord)]
    # increments y_coord by 20
    y_coord += 20

# ENEMY PROPERTIES
# acceleration of all enemies
ENEMY_ACC = 0.5
# knockback speed when player attacks enemies
KNOCKBACK = 0.75

# LEVEL 2
# OBSTACLES
# setup platforms
PLATFORM_LIST_LEVEL2 = [(20, 300, 200, 30),
                        (500, 370, 50, 30),
                        (330, 370, 30, 30),
                        (400, 500, 100, 30),
                        (20, 500, 200, 30),
                        (580, 300, 200, 30),
                        (300, 650, 190, 30),
                        (580, 750, 200, 30),
                        (20, 750, 200, 30),
                        (20, 850, 755, 50)]


# setup pillars
PILLAR_LIST_LEVEL2 = [(195, 330),
                      (195, 530)]

# setup walls
WALLS_LEVEL2 = []
# set y_coord to 0
y_coord = 0
# loop to make sure all walls added
while y_coord < 900:
    # adds coordinates to WALLS_LEVEL2 list
    WALLS_LEVEL2 += [(780, y_coord)]
    # increments y_coord by 20
    y_coord += 20

# resets y_coord to 0
y_coord = 0
# loop to make sure all walls are added
while y_coord < 900:
    # add coordinates to WALLS_LEVEL2 list
    WALLS_LEVEL2 += [(0, y_coord)]
    # increments y_coord by 20
    y_coord += 20

# loop to make sure all roof blocks are added  
while x_coord < MAPWIDTH:
    # adds coordinates to TOPBLOCK list
    TOPBLOCK += [(x_coord, 0)]
    # incements x_coord by 20 
    x_coord += 20