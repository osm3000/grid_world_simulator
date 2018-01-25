import numpy as np
class RobotStatus:
    def __init__(self, log_robot_pos=True, log_robot_sensors=True, properties={}):
        self.log_robot_pos = log_robot_pos
        self.log_robot_sensors = log_robot_sensors
        self.robot_position = []
        self.robot_sensors_readings = []
        self.subgoals = []
        self.action_taken = []
        self.game_score = []
        self.unique_elements = None

        self.properties = properties
        if len(self.properties.keys()) == 0:
            self.properties['position']  = True
            self.properties['sensors']   = True
            self.properties['subgoals']   = True


    def __str__(self):
        final_string = ''
        final_string += "Robot position: " + str(self.robot_position[-1]) + "\n"
        final_string += "Sensors: " + str(self.robot_sensors_readings[-1]) + "\n"
        final_string += "Subgoals: " + str(self.subgoals[-1]) + "\n"
        return final_string

    def get_robot_status(self):
        robot_status_vector = []
        if self.properties['position']:
            robot_status_vector += self.robot_position[-1]
        if self.properties['sensors']:
            robot_status_vector += self.robot_sensors_readings[-1]
        if self.properties['subgoals']:
            robot_status_vector += self.subgoals[-1]

        return robot_status_vector

    def log_status(self):
        final_text = ''
        final_text += "unique_elements:" + ",".join(self.unique_elements) + '\n'
        for i in range(len(self.game_score)):
            final_text += \
            str(",".join(map(str, self.robot_sensors_readings[i]))) + ":" + \
            str(",".join(map(str, self.robot_position[i]))) + ":" + \
            str(self.subgoals[i]) + ":" + \
            str(self.game_score[i]) + "\n"
        return final_text
