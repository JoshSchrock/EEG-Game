import pygame
import random
import math
from button import Button
from event_handler import EventHandler

class Game:
    def __init__(self, eegInterface, frame_rate):
        self.pursuePos = [random.randint(75, 125), random.randint(875, 925)]
        startx = random.randint(175, 225)
        starty = random.randint(775, 825)
        self.evadeStart = [startx, starty]
        self.evadePos = [startx, starty]
        self.realTarget = [random.randint(700, 900), 125]
        self.falseTarget = [random.randint(200, 400), 125]
        self.slope = (self.realTarget[1] - self.evadePos[1]) / (self.realTarget[0] - self.evadePos[0])
        self.midpoint = [((self.realTarget[0] + self.falseTarget[0]) // 2), 125]
        self.verticalSpeed = 30
        self.targetRadius = 20
        self.width = 16
        self.height = 24
        desired_velocity = 10  # velocity without respect to frame rate
        self.velocity = desired_velocity * (20 / frame_rate)
        self.close_button = Button(pygame.Color("red"), 1000, 50, 50, 50, "X",
                                   font='comicsans', size=50)
        self.strat = random.randint(0, 2)
        self.eventHandler = EventHandler(self)  # events that control the game
        self.eegInterface = eegInterface

    def run_one_cycle(self):
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
        timeElapsed = pygame.time.get_ticks() // 1000
        # travel in sinusoidal trajectory towards target
        if (self.evadePos[0] < self.realTarget[0]) and (self.evadePos[1] > self.realTarget[1]):
            if timeElapsed == 0:
                self.evadePos[0] += self.velocity
                self.evadePos[1] += self.velocity * self.slope
            else:
                self.evadePos[0] += (25 * math.sin(timeElapsed * self.velocity) + 2.5)  # x = x + 25sin(velocity*t) + 1
                self.evadePos[1] += (self.slope - timeElapsed)  # y = m - t
        # go directly towards target once target x-pos or y-pos is reached
        else:
            if self.evadePos[0] < self.realTarget[0]:
                self.evadePos[0] += self.velocity
            if self.evadePos[1] > self.realTarget[1]:
                self.evadePos[1] -= self.velocity

    # ambigious evasion technique - needs to be edited
    def ambiguousPath(self):
        if self.evadePos[0] < self.midpoint[0]:
            self.evadePos[0] += self.velocity
            self.evadePos[1] += self.slope
        elif self.evadePos[1] > self.realTarget[1]:
            self.evadePos[1] -= self.velocity
        # go directly towards target once target x-pos or y-pos is reached
        else:
            if self.evadePos[0] < self.realTarget[0]:
                self.evadePos[0] += self.velocity
            if self.evadePos[1] > self.realTarget[1]:
                self.evadePos[1] -= self.velocity

