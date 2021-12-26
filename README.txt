# Message Maze generator - Capstone Project for the course Introduction to AI

## Installation
All the modules are included in a package called 'messagemaze' which can be installed using pip.
It is recommended to first create a virtual environment by running the following command in 
the directory of the project:

Linux/MacOs/Windows:
    $ python3 -m venv venv

Then activate the virtual environment by running the following command:

Linux/MacOs:
    $ source venv/bin/activate

Windows:
    $ .\venv\Scripts\activate.bat

Then install the modules using the following command:
    $ pip install -e .

It will automatically install all dependent libraries required (there is one in this project 
which is the 'pygame'). The dot . indicates that the command is run from the directory of the project.

After the module was successfully installed, you can try open the ipython notebook 'runner.ipynb' which
introduces basic usage of the package (make sure to open it in the environment you previously installed 
the package in).

## List of Modules
- cell.py: contains the class Cell with methods to add walls and remove walls
- maze.py: contains the class Maze with methods to generate a maze and to display it
- message_path.py: contains the class MessagePath with methods to generate a message path
- random_path.py: contains the function RandomPattern to generate a random path connecting two points in
a rectangular grid
- draw_pattern.py: contains the function DrawPattern which allows users to draw a pattern - the desired 
solution path of a maze on a rectangular grid
- combine.py: contains 2 functions to combine a list of Maze objects to create another Maze object,
horizontally and vertically
- maze_viz.py: contains the class Visualizer contains methods to save the maze as
a picture and to display the maze in a window
- algorithms.py: contains 3 algorithms to generate the maze given a rectangular grid - a blank Maze object
or a Maze object with only solution path generated from MessagePath
- visualize_algorithms.py: contains 3 algorithms as above but were modified for visualization purpose

