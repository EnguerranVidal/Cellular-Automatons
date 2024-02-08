from typing import Optional
import numpy as np
from matplotlib import pyplot as plt


class GameOfLife:
    def __init__(self, domain: Optional[np.ndarray] = None, timeSteps: int = 10000, maxEndOscillations=5):
        self.domain = np.random.choice([0, 1], size=(200, 200)) if domain is None else domain
        self.initialDomain = self.domain.copy()
        self.timeSteps = timeSteps
        self.nbOscillations = 0
        self.maxEndOscillations = maxEndOscillations
        self.domainScreenShots = []

    def nextStep(self):
        extended = np.concatenate([self.domain[:, -1:], self.domain, self.domain[:, :1]], axis=1)
        extended = np.concatenate([extended[-1:, :], extended, extended[:1, :]], axis=0)
        neighbours = (extended[:-2, :-2] + extended[:-2, 1:-1] + extended[:-2, 2:] + extended[1:-1, 2:] +
                      extended[2:, 2:] + extended[2:, 1:-1] + extended[2:, :-2] + extended[1:-1, :-2])
        self.domain = np.where(((self.domain == 1) & ((neighbours == 2) | (neighbours == 3))) |
                               ((self.domain == 0) & (neighbours == 3)), 1, 0)

    def verifyOscillations(self):
        self.domainScreenShots.append(self.domain.copy())
        if len(self.domainScreenShots) > 2:
            if np.array_equal(self.domain, self.domainScreenShots[0]):
                self.nbOscillations += 1
            self.domainScreenShots.pop(0)
            if self.nbOscillations == self.maxEndOscillations:
                return True
        return False

    def runSimulation(self, steps: int = None):
        figure = plt.figure(figsize=(8, 8))
        ax = figure.add_subplot(111)
        plottingDomain = ax.imshow(np.flipud(self.domain))
        figure.show()
        steps = steps if steps is not None else self.timeSteps
        for i in range(steps):
            plt.pause(0.01)
            self.nextStep()
            plottingDomain.set_data(np.flipud(self.domain))
            plt.draw()
            if self.verifyOscillations():
                break


if __name__ == '__main__':
    game = GameOfLife()
    game.runSimulation()

