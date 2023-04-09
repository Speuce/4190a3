"""
valueIteration.py
"""
from cell import ExitCell
from grid_world import GridWorld
from action import Action
from color import Color

PRINT_AGENT = False

# Does value iteration, accepts a GridWorld instance a number of steps k to do.
def iterate(grid_world: GridWorld, k: int):
    for i in range(k):
        grid_values = [[
            grid_world.grid[y][x].value for x in range(len(grid_world.grid[0]))
        ] for y in range(len(grid_world.grid))]
        for y in range(len(grid_world.grid)):
            for x in range(len(grid_world.grid[y])):
                best_reward = None
                if grid_world.is_cell(x, y):
                    for action in grid_world.agent_actions:
                        grid_world.set_position(x, y)
                        reward = grid_world.get_weighted_action_reward(action)
                        if best_reward is None or reward > best_reward:
                            best_reward = reward
                    grid_values[y][x] = best_reward
        for y in range(len(grid_world.grid)):
            for x in range(len(grid_world.grid[y])):
                grid_world.update_value(x, y, grid_values[y][x])


def _print_grid_line(grid_world: GridWorld):
    '''
    Prints a border of a cell in a grid
    '''
    for x in range(len(grid_world.grid[0])):
        print("+---------", end='')
    print('+')

def _print_cell_value_with_arrow(grid_world, x, y):
    '''
    Prints the cell value with a left or right arrow if the best action is left or right
    '''
    val = grid_world.grid[y][x].value
    absval = abs(val)
    can_move = grid_world.grid[y][x].can_move
    best_action = grid_world.computeActionFromValues((x, y))
    if best_action == Action.LEFT and can_move:
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
    if best_action == Action.RIGHT and can_move:
        print('>', end='')
    else:
        print(' ', end='')


def print_grid(grid_world: GridWorld):
    '''
    Prints the grid's values and best action for each cell
    '''
    for y in range(len(grid_world.grid)):
        _print_grid_line(grid_world)
        for x in range(len(grid_world.grid[y])):
            best_action = grid_world.computeActionFromValues((x, y))
            if PRINT_AGENT and x == grid_world.agent_x and y == grid_world.agent_y:
                print('|    A    ', end='')
            elif best_action == Action.UP and grid_world.grid[y][x].can_move:
                print('|    ^    ', end='')
            else:
                print('|         ', end='')
        print('|')
        for x in range(len(grid_world.grid[y])):
            print('|', end='')
            if isinstance(grid_world.grid[y][x], ExitCell):
                _print_cell_value_with_arrow(grid_world, x, y)
            elif not grid_world.grid[y][x].can_move:
                print('         ', end='')
            else:
                _print_cell_value_with_arrow(grid_world, x, y)
        print('|')
        for x in range(len(grid_world.grid[y])):
            best_action = grid_world.computeActionFromValues((x, y))
            if best_action == Action.DOWN and grid_world.grid[y][x].can_move:
                print('|    v    ', end='')
            else:
                print('|         ', end='')
        print('|')
    _print_grid_line(grid_world)
