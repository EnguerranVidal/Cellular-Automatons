from typing import Optional
import numpy as np
from matplotlib import pyplot as plt
import scipy


def gaussFunction(x, mu, sigma):
    return np.exp(- 0.5 * ((x - mu) / sigma) ** 2)


class LeniaSimulation:
    def __init__(self, domain: Optional[np.ndarray] = None, timeSteps: int = 10000, maxEndOscillations=5):
        self.growthFunction = None
        self.filter = None
        self.filterFft = None
        self.domain = np.random.choice([0, 1], size=(200, 200)) if domain is None else domain
        self.initialDomain = self.domain.copy()
        self.timeSteps = timeSteps

    def setGaussianFilter(self, radius=13, mu=0.5, sigma=0.15):
        N, M = self.domain.shape
        y, x = np.ogrid[-N // 2:N // 2, -M // 2:M // 2]
        distance = np.sqrt((1 + x) ** 2 + (1 + y) ** 2) / radius
        kLenia = gaussFunction(distance, mu, sigma)
        kLenia[distance > 1] = 0
        self.filterFft = np.fft.fft2(np.fft.fftshift(kLenia / np.sum(kLenia)))
        kLenia = kLenia[N // 2 - radius:N // 2 + radius, M // 2 - radius:M // 2 + radius]
        self.filter = kLenia / np.sum(kLenia)

    def setMultiRingFilter(self, radius=18, mu=0.5, sigma=0.15, ringStrengths=None):
        if ringStrengths is None:
            ringStrengths = [1]
        nRings = len(ringStrengths)
        N, M = self.domain.shape
        y, x = np.ogrid[-N // 2:N // 2, -M // 2:M // 2]
        print(y, x)
        distance = np.sqrt(x ** 2 + y ** 2) / radius * nRings
        KMulti = np.zeros_like(distance)
        for i in range(nRings):
            mask = (distance.astype(int) == i)
            KMulti += mask * ringStrengths[i] * gaussFunction(distance % 1, mu, sigma)
        self.filterFft = np.fft.fft2(np.fft.fftshift(KMulti / np.sum(KMulti)))
        KMulti = KMulti[N // 2 - radius:N // 2 + radius, M // 2 - radius:M // 2 + radius]
        self.filter = KMulti / np.sum(KMulti)

    def setGaussianGrowth(self, mu=0.15, sigma=0.015):
        self.growthFunction = lambda u: -1 + 2 * gaussFunction(u, mu, sigma)

    def setHydroGrowth(self):
        self.setGaussianGrowth(mu=0.26, sigma=0.036)

    def nextStep(self, dt=0.1, method='fft'):
        if method == 'fft':
            U = np.real(np.fft.ifft2(self.filterFft * np.fft.fft2(self.domain)))
        else:
            U = scipy.signal.convolve2d(self.domain, self.filter, mode='same', boundary='wrap')
        self.domain = np.clip(self.domain + dt * self.growthFunction(U), 0, 1)

    def nextStepConvolution(self, dt=0.1):
        U = np.real(np.fft.ifft2(self.filterFft * np.fft.fft2(self.domain)))
        self.domain = np.clip(self.domain + dt * self.growthFunction(U), 0, 1)

    def runSimulation(self, steps: int = None, method='fft'):
        figure = plt.figure(figsize=(8, 8))
        ax = figure.add_subplot(111)
        plottingDomain = ax.imshow(np.flipud(self.domain))
        figure.show()
        steps = steps if steps is not None else self.timeSteps
        for i in range(steps):
            plt.pause(0.01)
            self.nextStep(method=method)
            plottingDomain.set_data(np.flipud(self.domain))
            plt.draw()


def testOrbium():
    orbium = np.array([[0, 0, 0, 0, 0, 0, 0.1, 0.14, 0.1, 0, 0, 0.03, 0.03, 0, 0, 0.3, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0.08, 0.24, 0.3, 0.3, 0.18, 0.14, 0.15, 0.16, 0.15, 0.09, 0.2, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0.15, 0.34, 0.44, 0.46, 0.38, 0.18, 0.14, 0.11, 0.13, 0.19, 0.18, 0.45, 0, 0, 0],
                       [0, 0, 0, 0, 0.06, 0.13, 0.39, 0.5, 0.5, 0.37, 0.06, 0, 0, 0, 0.02, 0.16, 0.68, 0, 0, 0],
                       [0, 0, 0, 0.11, 0.17, 0.17, 0.33, 0.4, 0.38, 0.28, 0.14, 0, 0, 0, 0, 0, 0.18, 0.42, 0, 0],
                       [0, 0, 0.09, 0.18, 0.13, 0.06, 0.08, 0.26, 0.32, 0.32, 0.27, 0, 0, 0, 0, 0, 0, 0.82, 0, 0],
                       [0.27, 0, 0.16, 0.12, 0, 0, 0, 0.25, 0.38, 0.44, 0.45, 0.34, 0, 0, 0, 0, 0, 0.22, 0.17, 0],
                       [0, 0.07, 0.2, 0.02, 0, 0, 0, 0.31, 0.48, 0.57, 0.6, 0.57, 0, 0, 0, 0, 0, 0, 0.49, 0],
                       [0, 0.59, 0.19, 0, 0, 0, 0, 0.2, 0.57, 0.69, 0.76, 0.76, 0.49, 0, 0, 0, 0, 0, 0.36, 0],
                       [0, 0.58, 0.19, 0, 0, 0, 0, 0, 0.67, 0.83, 0.9, 0.92, 0.87, 0.12, 0, 0, 0, 0, 0.22, 0.07],
                       [0, 0, 0.46, 0, 0, 0, 0, 0, 0.7, 0.93, 1, 1, 1, 0.61, 0, 0, 0, 0, 0.18, 0.11],
                       [0, 0, 0.82, 0, 0, 0, 0, 0, 0.47, 1, 1, 0.98, 1, 0.96, 0.27, 0, 0, 0, 0.19, 0.1],
                       [0, 0, 0.46, 0, 0, 0, 0, 0, 0.25, 1, 1, 0.84, 0.92, 0.97, 0.54, 0.14, 0.04, 0.1, 0.21, 0.05],
                       [0, 0, 0, 0.4, 0, 0, 0, 0, 0.09, 0.8, 1, 0.82, 0.8, 0.85, 0.63, 0.31, 0.18, 0.19, 0.2, 0.01],
                       [0, 0, 0, 0.36, 0.1, 0, 0, 0, 0.05, 0.54, 0.86, 0.79, 0.74, 0.72, 0.6, 0.39, 0.28, 0.24, 0.13,
                        0],
                       [0, 0, 0, 0.01, 0.3, 0.07, 0, 0, 0.08, 0.36, 0.64, 0.7, 0.64, 0.6, 0.51, 0.39, 0.29, 0.19, 0.04,
                        0],
                       [0, 0, 0, 0, 0.1, 0.24, 0.14, 0.1, 0.15, 0.29, 0.45, 0.53, 0.52, 0.46, 0.4, 0.31, 0.21, 0.08, 0,
                        0],
                       [0, 0, 0, 0, 0, 0.08, 0.21, 0.21, 0.22, 0.29, 0.36, 0.39, 0.37, 0.33, 0.26, 0.18, 0.09, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0.03, 0.13, 0.19, 0.22, 0.24, 0.24, 0.23, 0.18, 0.13, 0.05, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0.02, 0.06, 0.08, 0.09, 0.07, 0.05, 0.01, 0, 0, 0, 0, 0]])
    N = 128
    M = int(np.ceil((16 * N) / 9))
    X = np.zeros((N, M))
    pos_x = M // 6
    pos_y = N // 6
    X[pos_x:(pos_x + orbium.shape[1]), pos_y:(pos_y + orbium.shape[0])] = orbium.T
    game = LeniaSimulation(domain=X)
    game.setGaussianFilter()
    game.setGaussianGrowth()
    game.runSimulation(method='convolution')


def testGenerativeSpot():
    N = 256
    M = int(np.ceil((16 * N) / 9))
    r = 36
    y, x = np.ogrid[-N // 2:N // 2, -M // 2:M // 2]
    X = np.exp(-0.5 * (x * x + y * y) / (r * r))
    game = LeniaSimulation(domain=X)
    game.setGaussianFilter()
    game.setGaussianGrowth()
    game.runSimulation()


def testMultiRings():
    game = LeniaSimulation()
    game.setMultiRingFilter(ringStrengths=[0.5, 1, 0.667])


if __name__ == '__main__':
    testOrbium()