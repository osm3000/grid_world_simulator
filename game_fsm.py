import game_state
class GameLogicBase:
    def __init__(self):
        self.game_fsm = {}
        self.game_over = False
        self.game_score = 0
        self.env_changes = {}

    def update_fsm(self, robot_status):
        raise (NotImplemented)

    def reset_variables(self):
        raise (NotImplemented)

class Collect_Ball_Simple(GameLogicBase):
    """
    The target here is to collect one ball only, and put it in the basket.
    """
    def __init__(self):
        super(Collect_Ball_Simple, self).__init__()
        self.game_fsm['ball_collected'] = False
        self.game_fsm['ball_scored']    = False
        self.env_changes = {'delete':None}

    def update_fsm(self, robot_status: game_state.RobotStatus):
        self.reset_variables()
        if not self.game_over:
            if self.game_fsm['ball_collected'] == False:
                if robot_status.subgoals[-1] == '1':
                    self.game_fsm['ball_collected'] = True
                    self.env_changes['delete'] = robot_status.robot_position[-1]
                    print ("BALLLLLLLLLLLLLLLLLL COLLECTED")

            elif self.game_fsm['ball_scored'] == False:
                if robot_status.subgoals[-1] == '2':
                    self.game_fsm['ball_collected'] = True
                    self.env_changes['delete'] = robot_status.robot_position[-1]
                    self.game_over = True
                    self.game_score = 10
                    print ("GOAAAAAAAAAAAAAAAAAAAAAAAAAL!!!!!!!!!!!!!!!!!!!!!!!!!!")

        return self.game_over, self.game_score, self.env_changes

    def reset_variables(self):
        self.env_changes['delete'] = None

class three_steps_game(GameLogicBase):
    """
    The target here is to collect one ball only, and put it in the basket.
    """
    def __init__(self):
        super(three_steps_game, self).__init__()
        self.game_fsm['step_1']     = False
        self.game_fsm['step_2']     = False
        self.game_fsm['step_3']     = False
        self.env_changes = {'delete':None}

    def update_fsm(self, robot_status: game_state.RobotStatus):
        self.reset_variables()
        if not self.game_over:
            if self.game_fsm['step_1'] == False:
                if robot_status.subgoals[-1] == '1':
                    self.game_fsm['step_1'] = True
                    self.env_changes['delete'] = robot_status.robot_position[-1]
                    # print ("Step 1 is done")

            elif (self.game_fsm['step_2'] == False) and (self.game_fsm['step_1'] == True):
                if robot_status.subgoals[-1] == '2':
                    self.game_fsm['step_2'] = True
                    self.env_changes['delete'] = robot_status.robot_position[-1]
                    # print ("Step 2 is done")

            elif (self.game_fsm['step_3'] == False) and (self.game_fsm['step_2'] == True):
                if robot_status.subgoals[-1] == '3':
                    self.game_fsm['step_3'] = True
                    self.env_changes['delete'] = robot_status.robot_position[-1]
                    # print ("Step 3 is done")
                    self.game_over = True
                    self.game_score = 10
                    print ("GOAAAAAAAAAAAAAAAAAAAAAAAAAL!!!!!!!!!!!!!!!!!!!!!!!!!!")

        return self.game_over, self.game_score, self.env_changes

    def reset_variables(self):
        self.env_changes['delete'] = None
