import matplotlib.pyplot as plt
import random
import imageio
import numpy as np


from functions import*


def random_walk(initial_position=(0, 0), steps=1000):
    save_file = gif_name()
    X, Y = [initial_position[0]], [initial_position[0]]
    fig = plt.figure(figsize=(8, 8))
    fig.patch.set_facecolor('xkcd:black')  # Changing figure to black
    ax = fig.add_subplot(111)
    ax.set_facecolor('xkcd:black')  # Changing background to black
    plt.xlim(-15, 15)
    plt.ylim(-15, 15)
    line = ax.plot(X, Y, c="white")
    Images = []
    fig.show()
    plt.pause(1)
    fig.canvas.draw()
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    Images.append(image)
    for i in range(steps):
        plt.pause(0.00001)
        # Random step choice
        ways = ["up", "down", "left", "right"]
        direction = random.choice(ways)
        if direction == "up":
            X.append(X[-1])
            Y.append(Y[-1] + 0.1)
        if direction == "down":
            X.append(X[-1])
            Y.append(Y[-1] - 0.1)
        if direction == "left":
            X.append(X[-1] - 0.1)
            Y.append(Y[-1])
        if direction == "right":
            X.append(X[-1] + 0.1)
            Y.append(Y[-1])
        # Updating plot
        line[0].set_data(X, Y)
        plt.draw()
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        Images.append(image)
    # Creating GIF
    gif_fps = 25
    gif_duration = 15
    n_images = gif_fps * gif_duration
    Images = select_list(Images, n_images)
    imageio.mimsave(save_file, Images, fps=gif_fps)