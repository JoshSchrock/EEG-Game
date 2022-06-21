import pygame
import random
import math
from button import Button
from event_handler import EventHandler
from image_handler import ImageHandler


class Game:
    def __init__(self, eegInterfaces, frame_rate):
        self.images = None
        self.timer = None
        self.endVec = None
        self.strat = None
        self.midpoint = None
        self.slope = None
        self.falseTarget = None
        self.realTarget = None
        self.evadePos = None
        self.evadeStart = None
        self.pursuePos = None
        self.eegInterfaces = eegInterfaces
        
        desired_velocity = 10  # velocity without respect to frame rate
        self.velocity = desired_velocity * (20 / frame_rate)
        
        self.verticalSpeed = 30
        self.targetRadius = 20
        self.width = 16
        self.height = 24
        
        self.eventHandler = EventHandler(self)  # events that control the game
        self.close_button = Button(pygame.Color("red"), 1000, 50, 50, 50, "X",
                                   font='comicsans', size=50)
        self.win_image = ImageHandler("GreatJob.jpg", (100, 300), (1000, 300))

        self.settup()

        
    def settup(self):
        self.pursuePos = [random.randint(75, 125), random.randint(875, 925)]
        startx = random.randint(175, 225)
        starty = random.randint(775, 825)
        self.evadeStart = [startx, starty]
        self.evadePos = [startx, starty]
        self.realTarget = [random.randint(700, 900), 125]
        self.falseTarget = [random.randint(200, 400), 125]
        self.midpoint = [((self.realTarget[0] + self.falseTarget[0]) // 2), 125]
        self.endVec = self.getunittoend()
        self.strat = random.randint(0, 2)
        self.images = []

        self.timer = 0
        for eeg in self.eegInterfaces:
            eeg.add_game_marker()
        
        
    def run_one_cycle(self):
        if self.checkloss() is True:
            self.settup()
        elif self.checkwin() is True:
            if self.win_image not in self.images:
                self.images.append(self.win_image)
                self.timer = pygame.time.get_ticks()
            if pygame.time.get_ticks() - self.timer > 2000:
                self.settup()
        else:
            self.performEvadeStrat()
            self.eventHandler.get_and_handle_events()
            if self.verticalSpeed != 0:
                self.verticalSpeed -= 1


    # choose evade strategy
    def performEvadeStrat(self):
        if self.strat == 0:
            self.exaggeratingPath()
        elif self.strat == 1:
            self.switchingPath()
        else:
            self.ambiguousPath()

    # exaggerating evasion technique
    def exaggeratingPath(self):
        falseVec = [self.falseTarget[0] - self.evadePos[0], self.falseTarget[1] - self.evadePos[1]]
        falseVecMag = math.sqrt(falseVec[0] ** 2 + falseVec[1] ** 2)
        trueVec = [self.realTarget[0] - self.evadePos[0], self.realTarget[1] - self.evadePos[1]]
        trueVecMag = math.sqrt(trueVec[0] ** 2 + trueVec[1] ** 2)

        weightFalse = ((self.evadePos[1] - 125) / (self.evadeStart[1] - 125)) ** \
                      (1 - ((self.evadePos[1] - 125) / (self.evadeStart[1] - 125)))
        weightTrue = 1 - weightFalse

        if self.evadePos[0] < self.realTarget[0]:
            self.evadePos[0] += ((falseVec[0] / falseVecMag) * weightFalse +
                                 (trueVec[0] / trueVecMag) * weightTrue) * self.velocity
        if self.evadePos[1] > self.realTarget[1]:
            self.evadePos[1] += ((falseVec[1] / falseVecMag) * weightFalse +
                                 (trueVec[1] / trueVecMag) * weightTrue) * self.velocity

    # switching evasion technique
    def switchingPath(self):
        timeElapsed = pygame.time.get_ticks() / 1000
        # travel in straight line towards target
        vecx, vecy = self.getunittoend()
        self.evadePos = [self.evadePos[0] + vecx, self.evadePos[1] + vecy]
        # travel in sinusoidal trajectory towards target
        # <-1/slope * sin(wt), -1/slope * sin(xt)>
        self.evadePos = [(-self.endVec[0]/self.endVec[1]) * math.sin(timeElapsed * 1) * self.velocity + self.evadePos[0],
                         (-self.endVec[0]/self.endVec[1]) * math.sin(timeElapsed * 1) * self.velocity + self.evadePos[1]]

    # ambigious evasion technique - needs to be edited
    def ambiguousPath(self):
        if self.evadePos[0] < self.midpoint[0] and self.evadePos[1] > self.midpoint[1]:
            vecx, vecy = self.getunittoend()
            self.evadePos = [self.evadePos[0] + vecx * self.velocity, self.evadePos[1] + vecy * self.velocity]
        elif self.evadePos[0] >= self.midpoint[0] and self.evadePos[1] > self.midpoint[1]:
            self.evadePos[1] -= self.velocity
        else:
            self.evadePos[0] += self.velocity

    def checkloss(self):
        if (self.realTarget[0] - self.targetRadius < self.evadePos[0] < self.realTarget[0] + self.targetRadius
                and self.realTarget[1] - self.targetRadius < self.evadePos[1] < self.realTarget[1] + self.targetRadius):
            return True

    def checkwin(self):
        if (self.pursuePos[0] - self.targetRadius < self.evadePos[0] < self.pursuePos[0] + self.targetRadius
                and self.pursuePos[1] - self.targetRadius < self.evadePos[1] < self.pursuePos[1] + self.targetRadius):
            return True

    def getunittoend(self):
        deltay = self.realTarget[1] - self.evadePos[1]
        deltax = self.realTarget[0] - self.evadePos[0]
        mag = math.sqrt((deltax ** 2) + (deltay ** 2))
        return deltax/mag, deltay/mag




