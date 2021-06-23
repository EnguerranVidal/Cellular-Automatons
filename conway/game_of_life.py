import matplotlib.pyplot as plt
import imageio
import numpy as np
import os

from functions import *


class GameOfLife:
    def __init__(self, domain=None, steps=None, bc=None):
        self.initial_domain = domain
        self.conditions = ["walls"]
        self.BC = bc
        self.domain = domain
        self.steps = steps
        self.domain_type = None
        # Loading Patterns
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.patterns = []

    def random_domain(self, K=5000, extent=(100, 100)):
        arr = np.zeros(extent)
        arr.resize((extent[0] * extent[1],))
        arr[:K] = 1
        np.random.shuffle(arr)
        arr.resize(extent)
        self.domain = arr
        self.initial_domain = arr

    def save_domain(self, name="domain"):
        path = self.current_dir + "\\domains\\" + name + ".txt"
        assert os.path.exists(path) == False, "ERROR : '" + name + ".txt' file already exists, try a different name."
        np.savetxt(path, self.initial_domain)

    def load_domain(self, name="domain"):
        path = self.current_dir + "\\domains\\" + name + ".txt"
        assert os.path.exists(path) == True, "ERROR : '" + name + ".txt' file does not exists, try a different name."
        self.initial_domain = np.loadtxt(path)
        self.domain = self.initial_domain

    def set_custom_slate(self, extent=(100, 100)):
        self.domain = np.zeros(extent)
        self.initial_domain = self.domain

    def add_pattern(self, name="square", upper_corner=(0, 0)):
        path = self.current_dir + "\\patterns\\" + name + ".txt"
        assert os.path.exists(path) == True, "ERROR : '" + name + ".txt' file does not exists, try a different name."
        pattern = np.loadtxt(path)
        extent = pattern.shape
        domain_extent = self.domain.shape
        self.domain[upper_corner[0]:upper_corner[0] + extent[0],upper_corner[1]:upper_corner[1] + extent[1]]=pattern
        self.initial_domain = self.domain

    def boundaries(self, bc="walls"):
        assert bc in self.conditions, "Error : Mentioned boundary conditions '" + bc + "' not recognised."
        self.BC = bc

    def reinitiliaze(self):
        self.domain = self.initial_domain

    def next_step(self):
        assert self.domain is not None, "Error : Define domain before trying a new step."
        assert self.BC is not None, "Error : Define boundary conditions before trying a new step."
        universe = self.domain
        new_universe = np.zeros_like(universe)
        extent = self.domain.shape
        if self.BC == "walls":
            for i in range(1, extent[0] - 1):
                for j in range(1, extent[1] - 1):
                    alive_neighbours = universe[i, (j - 1)] + universe[i, (j + 1)] + universe[(i - 1), j] + universe[
                        (i + 1), j] + universe[(i - 1), (j - 1)] + universe[(i - 1), (j + 1)] + universe[
                                           (i + 1), (j - 1)] + universe[(i + 1), (j + 1)]
                    if universe[i, j] == 1:
                        if alive_neighbours == 2 or alive_neighbours == 3:
                            new_universe[i, j] = 1
                    if universe[i, j] == 0 and alive_neighbours == 3:
                        new_universe[i, j] = 1
            self.domain = new_universe

    def run_plot(self, steps=1000):
        assert self.domain is not None, "Error : Define domain before trying a new step."
        assert self.BC is not None, "Error : Define boundary conditions before trying a new step."
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111)
        extent = self.domain.shape
        plt.xlim(0, extent[0])
        plt.ylim(0, extent[1])
        universe = ax.imshow(np.flipud(self.domain), cmap='Greys')
        fig.show()
        plt.pause(1)
        for n in range(steps):
            plt.pause(0.05)
            self.next_step()
            universe.set_data(np.flipud(self.domain))
            plt.draw()

    def run_gif(self, steps=1000, gif_fps=10, gif_duration=30):
        assert self.domain is not None, "Error : Define domain before trying a new step."
        assert self.BC is not None, "Error : Define boundary conditions before trying a new step."
        save_file = gif_name()
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(111)
        extent = self.domain.shape
        plt.xlim(0, extent[0])
        plt.ylim(0, extent[1])
        universe = ax.imshow(np.flipud(np.flipud(self.domain)), cmap='Greys')
        Images = []
        fig.show()
        plt.pause(1)
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        Images.append(image)
        for n in range(steps):
            plt.pause(0.05)
            self.next_step()
            universe.set_data(np.flipud(np.flipud(self.domain)))
            plt.draw()
            fig.canvas.draw()
            image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
            image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            Images.append(image)
        # Creating GIF
        n_images = gif_fps * gif_duration
        Images = select_list(Images, n_images)
        imageio.mimsave(save_file, Images, fps=gif_fps)
