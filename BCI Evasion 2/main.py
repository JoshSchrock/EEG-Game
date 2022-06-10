import pygame
from game import Game
from viewer import Viewer
from eeg_interface import EEGInterface

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


def main():
    pygame.init()
    pygame.display.set_caption("Pursuit-Evasion Simulation")  # title on top of game window

    screen = pygame.display.set_mode((1200, 1000))  # DONE: Choose your own size
    clock = pygame.time.Clock()
    frame_rate = 120 # game and display rate

    eegInterface = EEGInterface()

    game = Game(eegInterface, frame_rate)  # Methods of game operation
    viewer = Viewer(screen, game)  # display the game

    while True:
        clock.tick(frame_rate)
        game.run_one_cycle()
        viewer.update()

if __name__ == "__main__":
    main()

