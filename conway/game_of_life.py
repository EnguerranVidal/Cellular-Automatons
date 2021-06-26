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
        pattern_root = self.current_dir + "\\patterns"
        gifs_root = self.current_dir + "\\gifs"
        domains_root = self.current_dir + "\\domains"
        if not os.path.exists(pattern_root):  # creating the "patterns" directory if not present
            os.mkdir(pattern_root)
        if not os.path.exists(domains_root):  # creating the "domains" directory if not present
            os.mkdir(domains_root)
        if not os.path.exists(gifs_root):  # creating the "gifs" directory if not present
            os.mkdir(gifs_root)
        self.patterns_categories = [f for f in os.listdir(pattern_root) if os.path.isdir(os.path.join(pattern_root, f))]
        self.patterns = []
        for i in self.patterns_categories:
            category_path = os.path.join(pattern_root, i)
            category = [f for f in os.listdir(category_path) if os.path.isfile(os.path.join(category_path, f))]
            self.patterns.append(category)
        self.patterns.append([f for f in os.listdir(pattern_root) if not os.path.isdir(os.path.join(pattern_root, f))])

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

    def catalogue(self):
        n = len(self.patterns)
        for i in range(n-1):
            print(self.patterns_categories[i].upper()+" :")
            m = len(self.patterns[i])
            for j in range(m):
                print(self.patterns[i][j])
            print()
        if len(self.patterns[-1])>0:
            print("OTHER :")
            m = len(self.patterns[-1])
            for j in range(m):
                print(self.patterns[-1][j])

    def add_pattern(self, name="square", upper_corner=(0, 0)):
        # Get the pattern potential path
        n = len(self.patterns_categories)
        path = self.current_dir + "\\patterns\\" + name + ".txt"
        for i in range(n):
            if name + ".txt" in self.patterns[i]:
                path = self.current_dir + "\\patterns\\" + self.patterns_categories[i] + "\\" + name + ".txt"
        assert os.path.exists(path) == True, "ERROR : '" + name + ".txt' file does not exists, try a different name."
        # Loading the pattern
        pattern = np.loadtxt(path)
        extent = pattern.shape
        domain_extent = self.domain.shape
        if self.BC == "walls":
            assert upper_corner[0] + extent[0]<domain_extent[0],"ERROR : pattern overlapping with domain borders."
            assert upper_corner[1] + extent[1] < domain_extent[1], "ERROR : pattern overlapping with domain borders."
        self.domain[upper_corner[0]:upper_corner[0] + extent[0], upper_corner[1]:upper_corner[1] + extent[1]] = pattern
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

    def run_gif(self, steps=1000, gif_fps=15, gif_duration=10):
        assert self.domain is not None, "Error : Define domain before trying a new step."
        assert self.BC is not None, "Error : Define boundary conditions before trying a new step."
        assert gif_fps * gif_duration < steps,"Error : not enough steps to create a GIF with these characteristics"
        save_file = gif_name()
        gif_path = self.current_dir + "\\gifs\\" + save_file
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
        imageio.mimsave(gif_path, Images, fps=gif_fps)
