import pygame
import sys

class EventHandler:
    def __init__(self, game):
        self.game = game

    def get_and_handle_events(self):
        self.ManualController()
        # self.EEGController()


    # manual controls to pursue - implemented for testing purposes
    def ManualController(self):
        events = pygame.event.get()
        self.exit_if_time_to_quit(events)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[pygame.K_LEFT] and self.game.pursuePos[0] > self.game.velocity:
            self.game.pursuePos[0] -= self.game.velocity
        if pressed_keys[pygame.K_RIGHT] and self.game.pursuePos[0] < 1000 - self.game.width - self.game.velocity:
            self.game.pursuePos[0] += self.game.velocity
        if pressed_keys[pygame.K_UP] and self.game.pursuePos[1] > self.game.velocity:
            self.game.pursuePos[1] -= self.game.velocity
        if pressed_keys[pygame.K_DOWN] and self.game.pursuePos[1] < 1000 - self.game.height - self.game.velocity:
            self.game.pursuePos[1] += self.game.velocity

        mousex, mousey = pygame.mouse.get_pos()
        if self.game.close_button.isOver((mousex, mousey)):
            self.game.close_button.outline = 20
            for event in events:
                if event.type == pygame.MOUSEBUTTONUP:
                    sys.exit()
        else:
            self.game.close_button.outline = 0


    # controls given to pursuer
    def EEGController(self):
        action = self.game.pursuer.streamLineData()
        # left
        if action == "left" and self.game.pursuePos[0] > self.game.velocity:
            self.game.pursuePos[0] -= self.game.velocity
        # right
        if action == "right" and self.game.pursuePos[0] < 1000 - self.game.width - self.game.velocity:
            self.game.pursuePos[0] += self.game.velocity
        # up
        if action == "lift" and self.game.pursuePos[1] > self.game.velocity:
            self.game.pursuePos[1] -= self.game.velocity
        # down
        if action == "drop" and self.game.pursuePos[1] < 1000 - self.game.height - self.game.velocity:
            self.game.pursuePos[1] += self.game.velocity


    @staticmethod
    def exit_if_time_to_quit(events):
        for event in events:
            if event.type == pygame.QUIT:
                # need to close BCI connection
                sys.exit()

    @staticmethod
    def key_was_pressed_on_this_cycle(key, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == key:
                return True
        return False