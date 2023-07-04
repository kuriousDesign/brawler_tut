import pygame
from pygame import mixer
from fighter import Fighter
from bird import *
from water import *
from gato import *
import os

mixer.init()
pygame.init()

# create game window
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]
BIRD_LANDING_SIZE = [456, 1528]
BIRD_LANDING_SCALE = 0.5
BIRD_LANDING_OFFSET = [-500, 600]
BIRD_LANDING_DATA = [BIRD_LANDING_SIZE, BIRD_LANDING_SCALE, BIRD_LANDING_OFFSET]

# load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.005)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.05)


# other variables


# replace color in image
def color_replace(image, search_color, replace_color):
    pygame.transform.threshold(
        image, image, search_color, (0, 0, 0, 0), replace_color, 1, None, True
    )
    return image


# function for colorizing images
def colorize(image, newColor):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
    original).
    :param image: Surface to create a colorized copy of
    :param newColor: RGB color to use (original alpha values are preserved)
    :return: New colorized Surface instance
    """
    # image = self.image.copy()

    # zero out RGB values
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

    return image


# load background image


def load_bg_images():
    merged = None

    # assign directory
    directory = "assets/images/background/"
    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)

        # checking if it is a file
        if os.path.isfile(f):
            print(f)
            image = pygame.image.load(f)
            if merged == None:
                merged = image
            else:
                merged.blit(image, (0, 0))

    # assign directory
    directory = "assets/images/background/outlines/"
    # iterate over files in
    # the outlines directory
    outline_merged = None
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)

        # checking if it is a file
        if os.path.isfile(f):
            print(f)
            image = pygame.image.load(f)
            if outline_merged == None:
                outline_merged = image
            else:
                outline_merged.blit(image, (0, 0))
    # merged.set_colorkey((255, 255, 255))
    newColor = (255, 192, 203)
    # colorize the outline to be some new color
    outline_merged = colorize(outline_merged, newColor)

    # replace outline black with outline white
    # outline_merged.convert_alpha().set_colorkey((0, 0, 0))
    # outline_merged = color_replace(outline_merged, (0, 0, 0, 1), (255, 0, 0, 1))
    merged.blit(outline_merged, (0, 0))
    return merged.convert_alpha()


bg_image = load_bg_images()

# load spritesheets
warrior_sheet = pygame.image.load(
    "assets/images/warrior/Sprites/warrior.png"
).convert_alpha()
wizard_sheet = pygame.image.load(
    "assets/images/wizard/Sprites/wizard.png"
).convert_alpha()


# define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]
BIRD_ANIMATION_STEPS = [9]

# define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)


# function for drawing text


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# function for drawing background


def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill((100, 100, 100))
    screen.blit(scaled_bg, (0, 0))


# function for drawing fighter health bars


def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


# create two instances of fighters
fighter_1 = Fighter(
    1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx
)
fighter_2 = Fighter(
    2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx
)

# create instance of objects
bird = Bird()
water = Water()
gato = Gato()

# game setup
water.clip_player.start_clip(WaterClipNames.LOOP, loop=True)

# game loop
run = True
while run:
    clock.tick(FPS)

    # draw background
    draw_bg()
    draw_text("gon world", score_font, RED, 20, 60)

    # update objects
    bird.clip_player.update()
    water.clip_player.update()
    gato.clip_player.update()

    # draw objects
    if bird.get_visibility():
        bird.clip_player.draw(screen)

    water.clip_player.draw(screen)

    if gato.get_visibility():
        gato.clip_player.draw(screen)

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                bird.clip_player.start_clip(
                    BirdClipNames.LEAVING_HOME, loop=False, play_in_reverse=False
                )

            elif event.key == pygame.K_h:
                bird.clip_player.start_clip(
                    BirdClipNames.LEAVING_HOME, loop=False, play_in_reverse=True
                )
            elif event.key == pygame.K_LEFT:
                bird.clip_player.start_clip(
                    BirdClipNames.FOLLOWING, loop=True, play_in_reverse=True, flip=True
                )
            elif event.key == pygame.K_RIGHT:
                bird.clip_player.start_clip(
                    BirdClipNames.FOLLOWING,
                    loop=True,
                    play_in_reverse=False,
                    flip=False,
                )
            elif event.key == pygame.K_DOWN:
                bird.clip_player.start_clip(BirdClipNames.LANDING)
                print("keydown down arrow")
            elif event.key == pygame.K_k:
                bird.clip_player.start_clip(
                    BirdClipNames.KISSING, loop=False, hold_final_frame=True
                )
                print("keydown k")
            elif event.key == pygame.K_c:
                gato.clip_player.start_clip(
                    GatoClipNames.WALK, loop=False, hold_final_frame=True
                )
                print("keydown k")

    # update display
    pygame.display.update()

# exit pygame
pygame.quit()
