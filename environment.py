import numpy as np
import map_parser
import agents
import game_state
from typing import Iterator, NamedTuple
import time
import game_fsm

class environment:
    def __init__(self, visible=True, map_class=map_parser.map_parser(), delete_subgoals=True):
        self.visible = visible
        self.delete_subgoals = delete_subgoals
        self.robot_position = [None, None]
        # self.game_logic = game_fsm.Collect_Ball_Simple()
        self.game_logic = game_fsm.three_steps_game()
        self.time_counter = 0
        self.map_class = map_class
        self.nb_action = 4
        self.game_state = game_state.RobotStatus()
        self.robot_agent = agents.AgentRandom(nb_actions=4)
        self.game_over = False
        self.game_score = 0
        # Load the map
        self.map_class.read_map()
        self.game_state.unique_elements = self.map_class.unique_elements

    def set_agent(self, agent_object):
        self.robot_agent = agent_object

    def add_robot(self, robot_object):
        self.robots.append(robot_object)

    def initialize_robot_fixed(self, robot_position=[1, 1]):
        self.robot_position = robot_position

    def draw(self):
        """
        This will draw the map, then draw the robot on that map
        """
        # Save the current value of the relevant robot position on the map
        current_value = self.map_class.map_matrix[self.robot_position[0], self.robot_position[1]]
        # Replace this value to be R (for Robot)
        self.map_class.map_matrix[self.robot_position[0], self.robot_position[1]] = 'R'
        # Now, draw the map:
        drawing = ''
        for row in self.map_class.map_matrix:
            drawing += "".join(row) + "\n"
        print (drawing)
        # Now, return the map to its original state....and we are done
        self.map_class.map_matrix[self.robot_position[0], self.robot_position[1]] = current_value

    def update(self):
        new_action = self.robot_agent.get_next_move()
        row, col = self.robot_position
        new_action_name = None
        if new_action == 0: # Go up
            row -= 1
            new_action_name = 'up'
        elif new_action == 1: # Go down
            row += 1
            new_action_name = 'down'

        elif new_action == 2: # Go right
            col += 1
            new_action_name = 'right'

        elif new_action == 3: # Go left
            col -= 1
            new_action_name = 'left'

        else:
            raise("Illegal action")

        # Check if the move is legal, in order to update
        # print ("Action: {}, Current Pos: {}".format(new_action_name, self.robot_position))
        # print ("New pos Row: {}, Col: {}".format(row, col))

        try:
            if self.map_class.map_matrix[row, col] != '#':
                self.robot_position = [row, col]
        except:
            pass

        # Get the sensor readings
        sensor_reading = self.extract_sensors()
        # Draw the map
        if self.visible:
            print (sensor_reading)
            self.draw()
            time.sleep(.300)

        # Extract the current goal (if the robot position is on a goal)
        subgoal = self.check_subgoal()
        # if subgoal != -1:
        #     print ("Subgoal: ", subgoal)

        # Fill the robot status
        self.game_state.robot_position.append(self.robot_position)
        self.game_state.robot_sensors_readings.append(sensor_reading)
        self.game_state.subgoals.append(subgoal)

        # Update the game logic, and get its feedback
        self.game_over, self.game_score, env_changes = self.game_logic.update_fsm(self.game_state)
        if self.delete_subgoals:
            if env_changes['delete'] != None:
                self.del_elements(env_changes['delete'])
        self.game_state.game_score.append(self.game_score)

        # Update the time
        self.time_counter += 1

        # Check if the game is to be stopped or not
        # if self.game_over:
        #     print (self.game_score)


    def check_subgoal(self):
        subgoal = -1
        current_map_value = self.map_class.map_matrix[self.robot_position[0],self.robot_position[1]]
        if (current_map_value != '#') and (current_map_value != ' '):
            subgoal = current_map_value
        return subgoal

    def extract_sensors(self, flattened=True):
        """
        This will return the 8 pixels surrounding the robot
        """
        relevant_pixels = self.map_class.map_matrix[self.robot_position[0]-1:self.robot_position[0]+2,
        self.robot_position[1]-1:self.robot_position[1]+2]
        if flattened:
            relevant_pixels = relevant_pixels.flatten()
            # Remove the middle point (which is the robot location)
            # relevant_pixels = np.delete(relevant_pixels, 4)
        return relevant_pixels

    def del_elements(self, index_to_delete):
        self.map_class.map_matrix[index_to_delete[0], index_to_delete[1]] = ' '

    def save_env_results(self, file_name='./'):
        with open(file_name, 'w') as fileHandle:
            print (self.game_state.log_status(), file=fileHandle)

# nb_simulations = 1000
# max_simulation_time = 300
# success_rate = 0
# for i in range(nb_simulations):
#     my_env = environment(visible=False)
#     my_env.initialize_robot_fixed()
#     while True:
#         my_env.update()
#         # if (my_env.time_counter == max_simulation_time) or (my_env.game_over):
#         if (my_env.time_counter == max_simulation_time): # If all the sequences have the same length, this will be
#             break
#
#     if my_env.game_over:
#         my_env.save_env_results("./logs/"+str(i)+"_s")
#         success_rate += 1
#     else:
#         my_env.save_env_results("./logs/"+str(i)+"_f")
#
#     # print ("Done: ", my_env.time_counter)
#     print (i)
# print ("Success rate: ", (success_rate/nb_simulations))

# Target: Generate a 100 success
nb_simulations = 100
max_simulation_time = 300
success_rate = 0
counter = 0
generate_success = False
while True:
    my_env = environment(visible=False, delete_subgoals=False)
    my_env.initialize_robot_fixed()
    while True:
        my_env.update()
        # if (my_env.time_counter == max_simulation_time) or (my_env.game_over):
        if (my_env.time_counter == max_simulation_time): # If all the sequences have the same length, this will be
            break

    if generate_success:
        if my_env.game_over:
            my_env.save_env_results("./logs/"+str(nb_simulations)+"_s")
            nb_simulations -= 1
    else:
        if not my_env.game_over:
            my_env.save_env_results("./logs/"+str(nb_simulations)+"_f")
            nb_simulations -= 1
    # print ("Done: ", my_env.time_counter)
    print (counter, "--", nb_simulations)
    counter += 1
    if nb_simulations == 0:
        break
