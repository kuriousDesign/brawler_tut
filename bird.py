import pygame
from spritesheet import *
from typing import List
from clipplayer import *


class BirdClipNames(enumerate):
    LEAVING_HOME = 0
    FOLLOWING = 1
    LANDING = 2
    KISSING = 3
    GOING_HOME = 4


class Bird:
    def __init__(
        self,
    ):
        self._is_visible = True
        # frame kinematics and scaling

        self.scale = 1.0
        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.ax = 0
        self.ay = 0

        self.clip_player = ClipPlayer(self.load_clips())

        self.clip_is_finished = False
        self.rect = pygame.Rect((self.x, self.y, 80, 180))
        self.vel_y = 0

    def set_visibility(self, is_visible):
        self._is_visible = is_visible
        self.clip_player.is_visible = self._is_visible

    def get_visibility(self):
        self._is_visible = self.clip_player.is_visible
        return self._is_visible

    def load_clips(self):
        # create clip list

        """
        LEAVING_HOME = 0
        FOLLOWING = 1
        LANDING = 2
        KISSING = 3
        GOING_HOME = 4
        """

        clips: List[ClipData] = list()

        path = "assets/images/bird/spritesheet_bird_leavinghome_F4.png"
        sprite_sheet = SpriteSheet(path, 1920 * 2, 1080 * 2, 4, 0.5)
        clips.append(
            ClipData(
                sprite_sheet.frames,
                sprite_sheet.width,
                sprite_sheet.height,
                sprite_sheet.frame_count,
                100,
            )
        )

        path = "assets/images/bird/bird_flying_W3508H2612_F3.png"
        sprite_sheet = SpriteSheet(path, 3508, 2612, 3, 0.1)
        clips.append(
            ClipData(
                sprite_sheet.frames,
                sprite_sheet.width,
                sprite_sheet.height,
                sprite_sheet.frame_count,
                100,
            )
        )

        path = "assets/images/bird/spritesheet_bird_landing_W456H1528F9.png"
        sprite_sheet = SpriteSheet(path, 456, 1528, 9, 0.5)
        clips.append(
            ClipData(
                sprite_sheet.frames,
                sprite_sheet.width,
                sprite_sheet.height,
                sprite_sheet.frame_count,
                100,
            )
        )

        path = "assets/images/bird/spritesheet_bird_kiss_F5.png"
        sprite_sheet = SpriteSheet(path, 1920 * 2, 1080 * 2, 5, 0.5)
        kiss_fx = pygame.mixer.Sound("assets/audio/kiss.wav")
        kiss_fx.set_volume(0.5)
        clips.append(
            ClipData(
                sprite_sheet.frames,
                sprite_sheet.width,
                sprite_sheet.height,
                sprite_sheet.frame_count,
                100,
            )
        )

        path = "assets/images/bird/spritesheet_bird_landing_W456H1528F9.png"
        sprite_sheet = SpriteSheet(path, 456, 1528, 9, 0.5)
        clips.append(
            ClipData(
                sprite_sheet.frames,
                sprite_sheet.width,
                sprite_sheet.height,
                sprite_sheet.frame_count,
                100,
            )
        )

        return clips

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # get keypresses
        key = pygame.key.get_pressed()

        # can only perform other actions if not currently attacking
        if self.attacking == False and self.alive == True and round_over == False:
            # check player 1 controls
            if self.player == 1:
                # movement
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                # jump
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                # attack
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)
                    # determine which attack type was used
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2

            # check player 2 controls
            if self.player == 2:
                # movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                # jump
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                # attack
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(target)
                    # determine which attack type was used
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2

        # apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        # ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # apply attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # update player position
        self.rect.x += dx
        self.rect.y += dy

    # handle animation updates
