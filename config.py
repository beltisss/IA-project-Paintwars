# Configuration file.

import arenas

# general -- first three parameters can be overwritten with command-line arguments (cf. "python tetracomposibot.py --help")

display_mode = 0
arena = 0
position = False 
max_iterations = 501 #401*500

# affichage

display_welcome_message = True
verbose_minimal_progress = True # display iterations
display_robot_stats = True
display_team_stats = True
display_tournament_results = True
display_time_stats = True

# initialization : create and place robots at initial positions (returns a list containing the robots)

import robot_wanderer
import robot_dumb
import robot_braitenberg_avoider
import robot_braitenberg_loveWall
import robot_braitenberg_hateWall
import robot_braitenberg_loveBot
import robot_braitenberg_hateBot
import robot_subsomption
import robot_randomsearch 
import randomsearch2
import genetic_algorithms

def initialize_robots(arena_size=-1, particle_box=-1): # particle_box: size of the robot enclosed in a square
    x_center = arena_size // 2 - particle_box / 2
    y_center = arena_size // 2 - particle_box / 2
    robots = []
    #robots.append(robot_braitenberg_avoider.Robot_player(4, y_center, 0, name="First Robot", team="Team Avoider"))
    #robots.append(robot_braitenberg_avoider.Robot_player(93, y_center, 180, name="Second robot", team="Team Avoider"))
    #robots.append(robot_braitenberg_avoider.Robot_player(x_center, y_center+20, 90, name="Third robot", team="Team Avoider"))
    #robots.append(robot_braitenberg_avoider.Robot_player(x_center, y_center-40, 270, name="Fourth robot", team="Team Avoider"))
    #robots.append(robot_braitenberg_loveWall.Robot_player(4, y_center, 0, name="First Robot", team="Team Avoider"))
    #robots.append(robot_braitenberg_loveWall.Robot_player(93, y_center, 180, name="Second robot", team="Team Avoider"))
    #robots.append(robot_braitenberg_loveWall.Robot_player(x_center, y_center+20, 90, name="Third robot", team="Team Avoider"))
    #robots.append(robot_braitenberg_loveWall.Robot_player(x_center, y_center-40, 270, name="Fourth robot", team="Team Avoider"))
    #robots.append(robot_braitenberg_hateWall.Robot_player(4, y_center, 0, name="First Robot", team="Team Avoider"))
    #robots.append(robot_braitenberg_hateWall.Robot_player(93, y_center, 180, name="Second robot", team="Team Avoider"))
    #robots.append(robot_braitenberg_hateWall.Robot_player(x_center, y_center+20, 90, name="Third robot", team="Team Avoider"))
    #robots.append(robot_braitenberg_hateWall.Robot_player(x_center, y_center-40, 270, name="Fourth robot", team="Team Avoider"))
    #robots.append(robot_braitenberg_loveBot.Robot_player(4, y_center, 0, name="First Robot", team="Team love_Bot"))
    #robots.append(robot_braitenberg_loveBot.Robot_player(93, y_center, 180, name="Second robot", team="Team love_Bot"))
    #robots.append(robot_braitenberg_loveBot.Robot_player(x_center, y_center+20, 90, name="Third robot", team="Team love_Bot"))
    #robots.append(robot_braitenberg_loveBot.Robot_player(x_center, y_center-40, 270, name="Fourth robot", team="Team love_Bot"))
    #robots.append(robot_braitenberg_loveBot.Robot_player(20, 80, 135, name="Sixth Robot", team="Team love_Bot"))
    #robots.append(robot_braitenberg_loveBot.Robot_player(80, 20, 315, name="Seventh Robot", team="Team love_Bot"))
    #robots.append(robot_braitenberg_loveBot.Robot_player(80, 80, 225, name="Eighth Robot", team="Team love_Bot"))
    #robots.append(robot_braitenberg_hateBot.Robot_player(4, y_center, 0, name="First Robot", team="Team hate_Bot"))
    #robots.append(robot_braitenberg_hateBot.Robot_player(93, y_center, 180, name="Second robot", team="Team hate_Bot"))
    #robots.append(robot_braitenberg_hateBot.Robot_player(x_center, y_center+20, 90, name="Third robot", team="Team hate_Bot"))
    #robots.append(robot_braitenberg_hateBot.Robot_player(x_center, y_center-40, 270, name="Fourth robot", team="Team hate_Bot"))python3 tetracomposibot.py



    #robots.append(robot_braitenberg_hateBot.Robot_player(25, 25, 45, name="Fifth Robot", team="Team hate_Bot"))
    #robots.append(robot_braitenberg_hateBot.Robot_player(25, 75, 135, name="Sixth Robot", team="Team hate_Bot"))
    #robots.append(robot_braitenberg_hateBot.Robot_player(75, 25, 315, name="Seventh Robot", team="Team hate_Bot"))
    #robots.append(robot_braitenberg_hateBot.Robot_player(75, 75, 225, name="Eighth Robot", team="Team hate_Bot"))

    #robots.append(robot_subsomption.Robot_player(4, y_center, 0, name="SubBot0", team="subsomption_Bot"))
    #robots.append(robot_braitenberg_hateBot.Robot_player(93, y_center, 180, name="Second robot", team="Team hate_Bot"))
    #robots.append(robot_braitenberg_hateBot.Robot_player(x_center, y_center+20, 90, name="Third robot", team="Team hate_Bot"))
    #robots.append(robot_braitenberg_hateBot.Robot_player(x_center, y_center-40, 270, name="Fourth robot", team="Team hate_Bot"))
    #robots.append(randomsearch2.Robot_player(50, y_center, 90, "Second robot", "robot_randomSearch",10,20))
    robots.append(robot_randomsearch.Robot_player(50, y_center, 90, "Third robot", "randomSearch2",10,20))
    #robots.append(genetic_algorithms.Robot_player(10, y_center, 90, "Third robot", "randomSearch",10,20))
    
    

    return robots
    
