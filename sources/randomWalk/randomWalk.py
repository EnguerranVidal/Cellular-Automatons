import time

import matplotlib.pyplot as plt
import random
import imageio
import numpy as np


def generateGifName():
    t0 = time.time()
    struct = time.localtime(t0)
    timeString = str(struct.tm_year) + '-'
    nbMonths = str(struct.tm_mon)  # MONTHS
    if len(nbMonths) == 1:
        nbMonths = '0' + nbMonths
    timeString = timeString + nbMonths + '-'
    nbDays = str(struct.tm_mday)  # DAYS
    if len(nbMonths) == 1:
        nbDays = '0' + nbDays
    timeString = timeString + nbDays + '-'
    nbHours = str(struct.tm_hour)  # HOURS
    if len(nbHours) == 1:
        nbHours = '0' + nbHours
    timeString = timeString + nbHours + '-'
    nMinutes = str(struct.tm_min)  # MINUTES
    if len(nMinutes) == 1:
        nMinutes = '0' + nMinutes
    timeString = timeString + nMinutes + '-'
    nbSeconds = str(struct.tm_sec)  # SECONDS
    if len(nbSeconds) == 1:
        nbSeconds = '0' + nbSeconds
    timeString = timeString + nbSeconds + '.gif'
    return timeString


def selectionList(originalList, nbSelections):
    m = len(originalList)
    skip = int(m / nbSelections)
    new_l = []
    for i in range(m):
        if i % skip == 0:
            new_l.append(originalList[i])
    return new_l


def randomWalk(initialPosition=(0, 0), steps=1000):
    saveName = generateGifName()
    X, Y = [initialPosition[0]], [initialPosition[0]]
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
    gifFps = 25
    gifDuration = 15
    nbImages = gifFps * gifDuration
    Images = selectionList(Images, nbImages)
    imageio.mimsave(saveName, Images, fps=gifFps)
