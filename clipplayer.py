import pygame


class ClipData:
    def __init__(
        self,
        frames,
        width,
        height,
        frame_count,
        cooldown,
        sound=None,
        sound_start_index=0,
    ):
        self.frames = frames
        self.width = width
        self.height = height
        self.frame_count = frame_count
        self.cooldown = cooldown

        # sound fx data
        self.sound = sound  # sound fx
        self.sound_start_index = sound_start_index


class ClipPlayer:
    def __init__(self, clips):
        self.clips = clips

        self.active_clip_index = 0
        self.active_clip = self.clips[self.active_clip_index]
        self.frame_index = 0
        self.active_frame = self.active_clip.frames[self.frame_index]
        self.update_time = pygame.time.get_ticks()

        # Active Clip Controls
        self.x = 0  # translation of frame
        self.y = 0
        self.scale = 1.0
        self.flip = False  # flip the image about the y axis
        self.play_in_reverse = False  # play the frames backwards
        self.is_visible = False  # surface is visible
        self.loop = False
        self.hold_final_frame = False

    def start_clip(
        self,
        clip_num,
        loop=False,
        hold_final_frame=False,
        starting_frame_index=None,
        play_in_reverse=False,
        flip=False,
    ):
        """call this when you want to change to a new clip, optionally provide the starting frame index"""
        # check if the new action is different to the previous one

        # storing clip playback settings
        print("starting clip")
        print(clip_num)
        self.loop = loop
        self.hold_final_frame = hold_final_frame
        self.play_in_reverse = play_in_reverse
        self.flip = flip

        self.active_clip_index = clip_num
        self.active_clip = self.clips[clip_num]
        if starting_frame_index is None:
            if play_in_reverse:
                starting_frame_index = self.active_clip.frame_count - 1
            else:
                starting_frame_index = 0

        self.update_frame(starting_frame_index)
        self.update_time = pygame.time.get_ticks()
        self.clip_is_finished = False
        self.is_visible = True

    def update(self):
        """performs active frame update per the cooldown rate and adjust frame index per the playback
        settings"""

        # check if enough time has passed since the last update
        frame_update_needed = False
        if pygame.time.get_ticks() - self.update_time > self.active_clip.cooldown:
            if self.play_in_reverse:
                self.frame_index -= 1
            else:
                self.frame_index += 1

            self.update_time = pygame.time.get_ticks()
            frame_update_needed = True

            # check if the animation has finished or frame index needs reset based on looping
            if (
                not self.play_in_reverse
                and self.frame_index >= self.active_clip.frame_count
            ):
                # if the clip is looping, reset to zero
                if self.loop:
                    self.frame_index = 0
                    self.clip_is_finished = False

                elif self.hold_final_frame:
                    self.frame_index = self.active_clip.frame_count - 1
                    self.clip_is_finished = True
                else:
                    self.clip_is_finished = True
                    frame_update_needed = False

            # check if the animation has finished
            elif self.play_in_reverse and self.frame_index < 0:
                # if the clip is looping, reset to the last frame
                if self.loop:
                    self.frame_index = self.active_clip.frame_count - 1
                    self.clip_is_finished = False

                elif self.hold_final_frame:
                    self.frame_index = 0
                    self.clip_is_finished = True
                else:
                    self.clip_is_finished = True
                    frame_update_needed = False

        if frame_update_needed:
            self.update_frame(self.frame_index)

    def update_frame(self, frame_num):
        self.frame_index = frame_num
        self.active_frame = self.active_clip.frames[self.frame_index]
        if (
            self.active_clip.sound is not None
            and frame_num == self.active_clip.sound_start_index
        ):
            self.active_clip.sound.play()

    def draw(self, surface: pygame.Surface):
        img = pygame.transform.flip(self.active_frame, self.flip, False)
        pygame.transform.scale_by(img, self.scale, img)
        surface.blit(img, (self.x, self.y))
