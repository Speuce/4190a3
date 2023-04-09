"""
q_value_learning.py

"""

from cell import ExitCell
from color import Color
from grid_world import GridWorld
from action import Action
import random as rand

PRINT_AGENT = False

# returns the q value at a state x, y
# y=0 is the top row
def getQValue(grid_world, x, y):
    return grid_world.get_q_values(x, y)

# returns the value at a state x, y
# y=0 is the top row
def getValue(grid_world, x, y):
    q_values = getQValue(grid_world, x, y)
    max_value = None
    for value in q_values.values():
        if max_value is None or value > max_value:
            max_value = value
    return max_value

# updates the known value of a q state with a given reward
# y=0 is the top row
def update(grid_world, x, y, action, reward, alpha):
    q_values = getQValue(grid_world, x, y)
    q_values[action] = q_values[action] * (1 - alpha) + alpha * (reward)
    grid_world.update_known_value(x, y, getValue(grid_world, x, y))

# gets the list of the best choices at a state x, y
# it is a list so that we can randomly choose states of the same value
# y=0 is the top row
def get_best_choices(grid_world, x, y):
    q_values = getQValue(grid_world, x, y)
    max_value = None
    best_choices = []
    for action in q_values.keys():
        action_value = q_values[action]
        if max_value is None or q_values[action] >= max_value:
            if action_value == max_value:
                best_choices.append(action)
            else:
                best_choices = [action]
            max_value = q_values[action]
    return best_choices

# gets the policy at a given state x, y. Randomly chooses when states have the same value
# y=0 is the top row
def get_policy(grid_world, x, y):
    best_choices = get_best_choices(grid_world, x, y)
    return rand.choice(best_choices)

# Does Q Value Learning, accepts a GridWorld instance, a number of episodes, and an alpha value
def iterate(grid_world: GridWorld, eps: int, alpha: float):
    for i in range(eps):
        action = get_policy(grid_world, grid_world.agent_x, grid_world.agent_y)
        x, y = grid_world.get_position()
        reward = grid_world.take_action(action,
                                        has_noise=True,
                                        use_true_value=False)
        update(grid_world, x, y, action, reward, alpha)
        if grid_world.is_satisfied():
            x, y = grid_world.get_position()
            reward = grid_world.grid[y][x].value
            grid_world.update_known_value(x, y, reward)
            grid_world.reset(random=False)

# Q value printing function for a given cell x y
def _print_cell_value_with_arrow(grid_world, x, y, actions):
    val = grid_world.grid[y][x].known_value
    can_move = grid_world.grid[y][x].can_move
    absval = abs(val)
    if Action.LEFT in actions and can_move:
        print('<', end='')
    else:
        print(' ', end='')
    if (val == 0):
        print(' ', end='')
    elif val > 0:
        print(str(Color.GREEN) + " ", end='')
    else:
        print(Color.RED, end='')
    if absval >= 10:
        print("{:2.3f}".format(val), end='')
    elif absval >= 100:
        print("{:3.2f}".format(val), end='')
    elif absval >= 1000:
        print("{:4.1f}".format(val), end='')
    else:
        print("{:1.4f}".format(val), end='')
    print(Color.END, end='')
    if Action.RIGHT in actions and can_move:
        print('>', end='')
    else:
        print(' ', end='')


def printgrid(grid_world):
    '''
    Prints a grid with the values and policy of each cell
    '''
    for y in range(len(grid_world.grid)):
        _print_short_grid_line(grid_world)
        for x in range(len(grid_world.grid[y])):
            actions = get_best_choices(grid_world, x, y)
            if Action.UP in actions and grid_world.grid[y][x].can_move:
                print('|    ^    ', end='')
            else:
                print('|         ', end='')
        print('|')
        for x in range(len(grid_world.grid[y])):
            actions = get_best_choices(grid_world, x, y)
            print('|', end='')
            if PRINT_AGENT and x == grid_world.agent_x and y == grid_world.agent_y:
                print(Color.UNDERLINE, end='')
            if isinstance(grid_world.grid[y][x], ExitCell):
                _print_cell_value_with_arrow(grid_world, x, y, actions)
            elif not grid_world.grid[y][x].can_move:
                print('         ', end='')
            else:
                _print_cell_value_with_arrow(grid_world, x, y, actions)
        print('|')
        for x in range(len(grid_world.grid[y])):
            actions = get_best_choices(grid_world, x, y)
            if Action.DOWN in actions and grid_world.grid[y][x].can_move:
                print('|    v    ', end='')
            else:
                print('|         ', end='')
        print('|')
    _print_short_grid_line(grid_world)


def _print_value(val):
    '''
    Prints a value with a color
    '''
    absval = abs(val)
    if (val == 0):
        print(' ', end='')
    elif val > 0:
        print(str(Color.GREEN) + " ", end='')
    else:
        print(Color.RED, end='')
    print("{:1.2f}".format(val), end='')
    print(Color.END, end='')


def _print_grid_line(grid_world):
    '''
    Prints a border of a cell in a grid
    '''
    for x in range(len(grid_world.grid[0])):
        print('+-----------', end='')
    print('+')


def _print_short_grid_line(grid_world: GridWorld):
    '''
    Prints a (short) border of a cell in a grid
    '''
    for x in range(len(grid_world.grid[0])):
        print("+---------", end='')
    print('+')

def printgridqvals(grid_world):
    '''
    Prints out a the Q values for each cell
    '''
    for y in range(len(grid_world.grid)):
        _print_grid_line(grid_world)
        for x in range(len(grid_world.grid[y])):
            print('|   ', end='')
            _print_value(getQValue(grid_world, x, y)[Action.UP])
            print('   ', end='')
        print('|')
        for x in range(len(grid_world.grid[y])):
            if PRINT_AGENT and x == grid_world.agent_x and y == grid_world.agent_y:
                print(Color.UNDERLINE, end='')
            print('|', end='')
            _print_value(getQValue(grid_world, x, y)[Action.LEFT])
            print(' ', end='')
            _print_value(getQValue(grid_world, x, y)[Action.RIGHT])
        print('|')
        for x in range(len(grid_world.grid[y])):
            print('|   ', end='')
            _print_value(getQValue(grid_world, x, y)[Action.DOWN])
            print('   ', end='')
        print('|')
    _print_grid_line(grid_world)