# Configuration file.

import arenas

# general -- first three parameters can be overwritten with command-line arguments (cf. "python tetracomposibot.py --help")

display_mode = 1
arena = 1
position = False 

# affichage

display_welcome_message = False
verbose_minimal_progress = False # display iterations
display_robot_stats = False
display_team_stats = False
display_tournament_results = False
display_time_stats = True

# optimization

evaluations = 1000
it_per_evaluation = 400
max_iterations = evaluations * it_per_evaluation + 1

# initialization : create and place robots at initial positions (returns a list containing the robots)

import robot_optimize
import robot_randomsearch
import randomsearch2
import genetic_algorithms

def initialize_robots(arena_size=-1, particle_box=-1): # particle_box: size of the robot enclosed in a square
    x_center = arena_size // 2 - particle_box / 2
    y_center = arena_size // 2 - particle_box / 2
    robots = []
    #robots.append(robot_randomsearch.Robot_player(x_center, y_center+20, 90, "First robot", "randomSearch",10,20))
    #robots.append(randomsearch2.Robot_player(x_center, y_center+20, 90, "First robot", "randomSearch",10,20))
    robots.append(genetic_algorithms.Robot_player(x_center, y_center+20, 90, "First robot", "randomSearch",10,20))
    
    return robots
