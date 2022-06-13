import pygame


# GLOBAL VARIABLES FOR RGB COLORS
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

class Viewer:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game

    def update(self):
        self.screen.fill(WHITE)
        # draw pursuer
        pygame.draw.rect(self.screen, RED, (self.game.pursuePos[0], self.game.pursuePos[1], self.game.width, self.game.height))
        # draw evader
        pygame.draw.rect(self.screen, BLUE, (self.game.evadePos[0], self.game.evadePos[1], self.game.width, self.game.height))
        # draw targets
        pygame.draw.circle(self.screen, GREY, self.game.realTarget, self.game.targetRadius)
        pygame.draw.circle(self.screen, GREY, self.game.falseTarget, self.game.targetRadius)
        # draw exit button
        self.game.close_button.draw(self.screen)
        # draw images
        for image in self.game.images:
            image.draw(self.screen)
        # update display
        pygame.display.update()
