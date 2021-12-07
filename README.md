# **RANDOM MOTION / CONWAY'S GAME OF LIFE** 

  [![HitCount](http://hits.dwyl.com/EnguerranVidal/Conway-Game-of-Life.svg?style=flat)](http://hits.dwyl.com/EnguerranVidal/Conway-Game-of-Life)

<p align="center">
  <img src="https://github.com/EnguerranVidal/Random-Motion/blob/main/docs/showcase_gifs/gameoflife.gif" width="600" height="600">
</p>


This Python project's goal is to simulate different kinds of random motion and emerging patterns from simple rules.
It contains a Conway's Game of Life and a Random Walk algorithm all able to create animations in GIF formats through the use of the Imageio and Matplotlib library.


## Random Walk :

Imagine a drunk person making steps in 4 random directions : "forward", "backward", "left" and "right" and you keep track of all the position they has been in, making for a marvelous pattern emerging from randomness. That is basically the concept for this part of the project which revolves around a single Python function capable of chossing random steps, keeping track of the tracer's trajectory ( the drunk person ) and create a GIF animation out of it, resulting in something such as what you can see below :

<p align="center">
  <img src="https://github.com/EnguerranVidal/Random-Motion/blob/main/docs/showcase_gifs/randomwalk.gif" width="600" height="600">
</p>


## Conway's Game of Life :

This part of the project focuses more on a famous cellular automaton rules which create interesting emerging patterns. The Conway's Game of life is made of a grid which pixels are defined by their state as "dead" or "alive" and follow 4 famous rules :

- Any live cell with fewer than two live neighbours dies, as if by underpopulation.
- Any live cell with two or three live neighbours lives on to the next generation.
- Any live cell with more than three live neighbours dies, as if by overpopulation.
- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

We implemented these conditions/rules in the **[GameOfLife.nextstep](https://github.com/EnguerranVidal/Random-Motion/blob/main/conway/game_of_life.py)** method.
The code contains a major object called **[GameOfLife](https://github.com/EnguerranVidal/Random-Motion/blob/main/conway/game_of_life.py)** that instigates and runs the simulations but also can withstand the implementation of different boundary conditions and pattern changes. It can also save and load domains if need be, reinitialize himself if you want to see a specific result again, add famous Game of Life pattern/blocks for further study and creativity such as this "glider gun" used in the creation of computers inside the game of life !

- Glider Gun Pattern

<p align="center">
  <img src="https://github.com/EnguerranVidal/Random-Motion/blob/main/docs/showcase_gifs/glider_gun.gif" width="300" height="300">
</p>

- Max Pattern

<p align="center">
  <img src="https://github.com/EnguerranVidal/Random-Motion/blob/main/docs/showcase_gifs/max.gif" width="300" height="300">
</p>


# FUTURE ADDITIONS ?

- The created GIFs are as of now uncompressed and can therefore become quite heavy, we will try to implement a compressing function later on to ease this problem.

- We will allow the user to show the steps passing through a display in the animation.

- We will add a receiding trail for the random walk animation instead of the current bright white one.

- We will try and add more boundary conditions for the game of life algorithm, at least implement toroidal boundary conditions.

- We will hopefully add a system where an image file could be converted as a txt file and added in the pattern catalogue.

