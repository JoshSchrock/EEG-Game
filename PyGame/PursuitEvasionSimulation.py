import pygame
import random
import math
from userSession import userSession

"""
Pygame Pursuit-Evader Simulation
"""

"""
Stage 1: One human, one robot. Human is the pursuer and robot is the evader who aims to get a target from two possibilities. 

Experiment set up: Record the EEG signals of the human pursuer under different conditions. The conditions include (rank by priority): 
1. Different types of trajectories, e.g., staying ambiguous, zig-zagging, etc. 
2. Different distances between the real target and the misleading target. 
3. Different initial locations of the evader. 
4. Different initial locations of the pursuer. 
5. How important is the target. For example, the human is told a score related to each target before they start the chasing. 
"""

# GLOBAL VARIABLES FOR RGB COLORS
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

class pursuitEvasionSimulation():
    def __init__(self):
        # initilializes the pygame
        pygame.init()
        # title on top of game window
        pygame.display.set_caption("Pursuit-Evasion Simulation")
        # window size
        self.window = pygame.display.set_mode((1000,1000))
        # create user session class for pursuer and set up
        self.pursuer = userSession()
        # initial conditions
        self.pursuePos = [random.randint(75,125), random.randint(875,925)]
        self.evadePos = [random.randint(175,225), random.randint(775,825)]
        self.realTarget = [random.randint(700,900), 125]
        self.falseTarget = [random.randint(200,400), 125]
        self.slope = (self.realTarget[1]-self.evadePos[1])/(self.realTarget[0]-self.evadePos[0])
        self.midpoint = [((self.realTarget[0]+self.falseTarget[0])//2), 125]
        self.verticalSpeed = 30
        self.targetRadius = 20
        self.width = 16
        self.height = 24
        self.velocity = 10
        self.run = True
    
    # simulates pursuit-evasion game
    def simulation(self):
        # initialize pursuer session and mark
        self.pursuer.openSession()
        # begin recording
        self.pursuer.beginRecord()
        # pick random strategy for evader
        evadeStrat = random.randint(0,2)
        while self.run:
            pygame.time.delay(50)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            self.updateDisplay()
            self.pursuerEEGController()
            self.chooseEvadeStrat(evadeStrat)
            if self.verticalSpeed != 0:
                self.verticalSpeed -= 1 
        self.quit()   

    # sets up graphical interface
    def updateDisplay(self):
        self.window.fill(WHITE)
        # draw pursuer
        pygame.draw.rect(self.window, RED, (self.pursuePos[0], self.pursuePos[1], self.width, self.height))
        # draw evader
        pygame.draw.rect(self.window, BLUE, (self.evadePos[0], self.evadePos[1], self.width, self.height))
        # draw targets
        pygame.draw.circle(self.window, GREY, self.realTarget, self.targetRadius)
        pygame.draw.circle(self.window, GREY, self.falseTarget, self.targetRadius)
        # update display
        pygame.display.update()

    def quit(self):
        pygame.quit()
        # close pursuer session
        self.pursuer.close()

    # choose evade strategy
    def chooseEvadeStrat(self, strat):
        if strat == 0:
            self.exaggeratingPath()
        elif strat == 1:
            self.switchingPath()
        else:
            self.ambiguousPath()

    # exaggerating evasion technique
    def exaggeratingPath(self):
        if (self.evadePos[0] < self.realTarget[0]) and (self.evadePos[1] > self.realTarget[1]):
            self.evadePos[0] += 5 # x = x + 5
            self.evadePos[1] += (2.5*self.slope - self.verticalSpeed) # y = 2.5m + verticalSpeed (non-constant)
        # go directly towards target once target x-pos or y-pos is reached
        else:
            if self.evadePos[0] < self.realTarget[0]:
                self.evadePos[0] += self.velocity
            if self.evadePos[1] > self.realTarget[1]:
                self.evadePos[1] -= self.velocity

    # switching evasion technique
    def switchingPath(self):
        timeElapsed = pygame.time.get_ticks() // 1000
        # travel in sinusoidal trajectory towards target
        if (self.evadePos[0] < self.realTarget[0]) and (self.evadePos[1] > self.realTarget[1]):
            if timeElapsed == 0:
                self.evadePos[0] += self.velocity
                self.evadePos[1] += self.velocity*self.slope
            else:    
                self.evadePos[0] += (25*math.sin(timeElapsed*self.velocity) + 2.5) #  x = x + 25sin(velocity*t) + 1
                self.evadePos[1] += (self.slope - timeElapsed) # y = m - t
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
    
    # controls given to pursuer
    def pursuerEEGController(self):
        action = self.pursuer.streamLineData()
        # left
        if action == "left" and self.pursuePos[0] > self.velocity:
            self.pursuePos[0] -= self.velocity
        # right
        if action == "right" and self.pursuePos[0] < 1000 - self.width - self.velocity:
            self.pursuePos[0] += self.velocity
        # up
        if action == "lift" and self.pursuePos[1] > self.velocity: 
            self.pursuePos[1] -= self.velocity
        # down
        if action == "drop" and self.pursuePos[1] < 1000 - self.height - self.velocity:
            self.pursuePos[1] += self.velocity

    # manual controls to pursue - implemented for testing purposes
    def pursuerManualController(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.pursuePos[0] > self.velocity:
            self.pursuePos[0] -= self.velocity
        if keys[pygame.K_RIGHT] and self.pursuePos[0] < 1000 - self.width - self.velocity:
            self.pursuePos[0] += self.velocity
        if keys[pygame.K_UP] and self.pursuePos[1] > self.velocity: 
            self.pursuePos[1] -= self.velocity
        if keys[pygame.K_DOWN] and self.pursuePos[1] < 1000 - self.height - self.velocity:
            self.pursuePos[1] += self.velocity
        
if __name__ == "__main__":
    sim = pursuitEvasionSimulation()
    sim.simulation()