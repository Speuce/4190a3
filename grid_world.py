"""
grid_world.py
This is the GridWorld class, it contains all of the states and provides functions to help with Q-learning and value iteartion.
"""

import random as rand
from cell import ExitCell, EmptyCell, BoulderCell
from action import Action


class GridWorld:
    # Grid is a [y][x] array of cells. 
    # Start_x is starting s value 
    # start_y is starting y value (indexed as 0 being top row), 
    # noise is a float, probability of wind 
    # transition cost, float cost for living
    # discount is a float
    def __init__(self, grid, start_x, start_y, noise, transition_cost,
                 discount):
        self.grid = grid
        self.start_x = start_x
        self.start_y = start_y
        self.agent_x = start_x
        self.agent_y = start_y # y = 0 is the top row
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
        self.agent_actions = [
            Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT
        ]

    # Picks a random empty cell, this was for experimenting with random start positions
    def choose_random_empty_cell(self):
        selection = None
        while selection is None:
            x = rand.randint(0, len(self.grid[0]) - 1)
            y = rand.randint(0, len(self.grid) - 1)
            if isinstance(self.grid[y][x], EmptyCell):
                selection = (x, y)
        return selection

    # returns whether or not the agent is currently in an end state
    def is_satisfied(self):
        return isinstance(self.grid[self.agent_y][self.agent_x], ExitCell)

    # resets the position of the agent, pass random=True for a random init
    def reset(self, random=False):
        if random:
            self.set_position(*self.choose_random_empty_cell())
        else:
            self.set_position(self.start_x, self.start_y)

    # sets the agents position to x y (y=0 is top row)
    def set_position(self, x, y):
        self.agent_x = x
        self.agent_y = y

    # returns potiion of the agent
    def get_position(self):
        return (self.agent_x, self.agent_y)

    # determines if an agent can actually move in a certain direction if it tries to. 
    # Prevents agent from leaving grid or going into boulders
    def can_move(self, action: Action):
        if action == Action.UP:
            return self.agent_y > 0 and not isinstance(
                self.grid[self.agent_y - 1][self.agent_x], BoulderCell)
        elif action == Action.DOWN:
            return self.agent_y < len(self.grid) - 1 and not isinstance(
                self.grid[self.agent_y + 1][self.agent_x], BoulderCell)
        elif action == Action.LEFT:
            return self.agent_x > 0 and not isinstance(
                self.grid[self.agent_y][self.agent_x - 1], BoulderCell)
        elif action == Action.RIGHT:
            return self.agent_x < len(self.grid[0]) - 1 and not isinstance(
                self.grid[self.agent_y][self.agent_x + 1], BoulderCell)

    # perturbs and returns and action according to random noise
    def peturb_action(self, action):
        action = rand.choice(self.action_noises[action])
        return action

    # Gets the value of taking an action at a state wrt noise
    def get_weighted_action_reward(self, desired_action):
        cur_x = self.agent_x
        cur_y = self.agent_y
        reward = 0
        for action in self.action_noises[desired_action]:
            reward += self.take_action(action) * self.noise / 2
            self.set_position(cur_x, cur_y)
        reward += self.take_action(desired_action) * (1 - self.noise)
        self.set_position(cur_x, cur_y)
        return reward

    # takes an action, moves the agent, returns a reward
    # has_noise: should there be random perturbations (yes for q learning)
    # use_true_values: should it use true values or known values of states (False for q learning)
    def take_action(self,
                    action: Action,
                    has_noise=False,
                    use_true_value=True):
        if has_noise and rand.uniform(0, 1) <= self.noise:
            action = self.peturb_action(action)
        if not self.can_move(action):
            action = Action.NOPE
        self.agent_x += self.action_to_index[action.value][0]
        self.agent_y += self.action_to_index[action.value][1]
        reward = self.transition_cost
        if use_true_value:
            reward += self.grid[self.agent_y][
                self.agent_x].value * self.discount
        else:
            reward += self.grid[self.agent_y][self.agent_x].known_value * self.discount
        return reward

    # Updates the true value of a state
    def update_value(self, x, y, value):
        self.grid[y][x].update_value(value)

    # Updates the known value of a state
    def update_known_value(self, x, y, value):
        self.grid[y][x].update_known_value(value)

    # Requested function (this was added after we were done the assignment)
    # Given a state, finds the best action to take given true state values.
    # State is a tuple (x, y), where y=0 is the top row
    def computeActionFromValues(self, state: tuple):
        saved_pos = self.get_position()
        best_action = None
        best_score = None
        pos_x = state[0]
        pos_y = state[1]
        for action in [Action.UP, Action.DOWN, Action.RIGHT, Action.LEFT]:
            self.set_position(pos_x, pos_y)
            if self.can_move(action):
                cur_score = self.take_action(action, False, True)
                if best_action is None or cur_score > best_score:
                    best_action = action
                    best_score = cur_score
        self.set_position(saved_pos[0], saved_pos[1])
        return best_action

    # Requested function (written after we were done)
    # Computes the Q value of taking an action a at state s
    # State is a tuple (x, y), where y=0 is the top row
    # action is an Action
    def computeQValueFromValues(self, state: tuple, action: Action):
        saved_pos = self.get_position()
        pos_x = state[0]
        pos_y = state[1]
        self.set_position(pos_x, pos_y)
        reward = self.get_weighted_action_reward(action)
        self.set_position(saved_pos[0], saved_pos[1])
        return reward

    # returns whether or not a cell is Empty (can be walked on, not an exist cell)
    # y=0 is the top row
    def is_cell(self, x, y):
        return isinstance(self.grid[y][x], EmptyCell)

    # gets the q values for a state, y=0 is the top row
    def get_q_values(self, x, y):
        return self.grid[y][x].q_values
