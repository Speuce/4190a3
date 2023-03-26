import random as rand
from cell import ExitCell, EmptyCell, BoulderCell
from action import Action
from color import Color

class GridWorld:
    def __init__(self, grid, start_x, start_y, noise, transition_cost, discount):
        self.grid = grid
        self.start_x = start_x
        self.start_y = start_y
        self.agent_x = start_x
        self.agent_y = start_y
        self.noise = noise
        self.transition_cost = transition_cost
        self.discount = discount
        self.action_to_index = {
            Action.UP.value: (0, -1),
            Action.DOWN.value: (0, 1),
            Action.LEFT.value: (-1, 0),
            Action.RIGHT.value: (1, 0),
            Action.NOPE.value: (0, 0)
        }
        self.action_noises = {
            Action.UP: [Action.LEFT, Action.RIGHT], 
            Action.DOWN: [Action.LEFT, Action.RIGHT], 
            Action.LEFT: [Action.UP, Action.DOWN], 
            Action.RIGHT: [Action.UP, Action.DOWN]
        }
        self.agent_actions = [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]

    def choose_random_empty_cell(self):
        selection = None
        while selection is None:
            x = rand.randint(0, len(self.grid[0]) - 1)
            y = rand.randint(0, len(self.grid) - 1)
            if isinstance(self.grid[y][x], EmptyCell):
                selection = (x, y)
        return selection

    def is_satisfied(self):
        return isinstance(self.grid[self.agent_y][self.agent_x], ExitCell)

    def reset(self, random=False):
        if random:
            self.set_position(*self.choose_random_empty_cell())
        else:
            self.set_position(self.start_x, self.start_y)

    # sets the agents position
    def set_position(self, x, y):
        self.agent_x = x
        self.agent_y = y
    
    def get_position(self):
        return (self.agent_x, self.agent_y)
    
    # determines if an action is possible
    def can_move(self, action:Action):
        if action == Action.UP:
            return self.agent_y > 0 and not isinstance(self.grid[self.agent_y - 1][self.agent_x], BoulderCell)
        elif action == Action.DOWN:
            return self.agent_y < len(self.grid) - 1 and not isinstance(self.grid[self.agent_y + 1][self.agent_x], BoulderCell)
        elif action == Action.LEFT:
            return self.agent_x > 0 and not isinstance(self.grid[self.agent_y][self.agent_x - 1], BoulderCell)
        elif action == Action.RIGHT:
            return self.agent_x < len(self.grid[0]) - 1 and not isinstance(self.grid[self.agent_y][self.agent_x + 1], BoulderCell)

    # perturbs and returns and action according to noise
    def peturb_action(self, action):
        action = rand.choice(self.action_noises[action])
        return action

    def get_weighted_action_reward(self, desired_action):
        cur_x = self.agent_x 
        cur_y = self.agent_y
        reward = 0
        for action in self.action_noises[desired_action]:
            # print("Trying noisy action: " + str(action))
            reward += self.take_action(action)*self.noise/2
            self.set_position(cur_x, cur_y)
        # print("Trying desired action: " + str(desired_action))
        reward += self.take_action(desired_action)*(1-self.noise)
        self.set_position(cur_x, cur_y)
        return reward

    # takes an action, moves the agent, returns a reward
    def take_action(self, action:Action, has_noise=False, use_true_value=True):
        if has_noise and rand.uniform(0, 1) <= self.noise:
            action = self.peturb_action(action)
        if not self.can_move(action):
            print("Can't make move")
            action = Action.NOPE
        # print(action)
        # print(self.agent_x, self.agent_y)
        self.agent_x += self.action_to_index[action.value][0]
        self.agent_y += self.action_to_index[action.value][1]
        # print("Agent moved to: (" + str(self.agent_x) + ", " + str(self.agent_y) + ")")
        reward = self.transition_cost 
        # TODO check this is right later, is exist reward part of reward for transition or part of value of state?
        if use_true_value:
            reward += self.grid[self.agent_y][self.agent_x].value * self.discount
        else:
            reward += self.grid[self.agent_y][self.agent_x].known_value * self.discount
        return reward 

    def update_value(self, x, y, value):
        self.grid[y][x].update_value(value)
    
    def update_known_value(self, x, y, value):
        self.grid[y][x].update_known_value(value)

    def _print_grid_line(self):
        for x in range(len(self.grid[0])):
            print('+---------', end='')
        print('+')

    def _print_cell_value(self, x, y):
        val = self.grid[y][x].value
        absval = abs(val)
        if(val == 0):
            print(' ', end='')
        elif val > 0:
            print(str(Color.GREEN) + " ", end='')
        else:
            print(Color.RED, end='')
        if absval >= 10:
            print(" {:2.3f} ".format(val), end='')
        elif absval >= 100:
            print(" {:3.2f} ".format(val), end='')
        elif absval >= 1000:
            print(" {:4.1f} ".format(val), end='')
        else:
            print(" {:1.4f} ".format(val), end='')
        print(Color.END, end='')

    def is_cell(self, x, y):
        return isinstance(self.grid[y][x], EmptyCell) 
    
    def get_q_values(self, x, y):
        return self.grid[y][x].q_values

    def print(self):
        for y in range(len(self.grid)):
            self._print_grid_line()
            for x in range(len(self.grid[y])):
                if x == self.agent_x and y == self.agent_y:
                    print('|    A    ', end='')
                else:
                    print('|         ', end='')
            print('|')
            for x in range(len(self.grid[y])):
                print('|', end='')
                if isinstance(self.grid[y][x], ExitCell):
                    self._print_cell_value(x, y)
                elif not self.grid[y][x].can_move:
                    print('         ', end='')
                else:
                    self._print_cell_value(x, y)
            print('|')
            for x in range(len(self.grid[y])):
                print('|         ', end='')
            print('|')
        self._print_grid_line()
