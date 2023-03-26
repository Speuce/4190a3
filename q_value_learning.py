import os
from cell import ExitCell
from color import Color
from grid_world import GridWorld
from action import Action
import random as rand
import reader

def getQValue(grid_world, x, y):
    grid_world.get_q_values(x, y)

def getValue(grid_world, x, y):
    q_values = getQValue(grid_world, x, y)
    max_value = None
    for value in q_values.values():
        if max_value is None or value > max_value:
            max_value = value
    return max_value

def update(grid_world, x, y, action, reward, alpha):
    q_values = getQValue(grid_world, x, y)
    q_values[action] = q_values[action] * (1-alpha) + alpha*(reward) 
    grid_world.update_known_value(x, y, getValue(grid_world, x, y))

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

def get_policy(grid_world, x, y):
    best_choices = get_best_choices(grid_world, x, y)
    return rand.choice(best_choices)

def iterate(grid_world: GridWorld, eps: int, alpha: float):
    eps = 10
    for i in range(eps):
        print("Iteration: " + str(i))
        action = get_policy(grid_world, grid_world.agent_x, grid_world.agent_y)
        reward = grid_world.take_action(action, has_noise=True, use_true_value=False)
        update(grid_world, grid_world.agent_x, grid_world.agent_y, action, reward, alpha)
        printgrid(grid_world)
        if grid_world.is_satisfied():
            x, y = grid_world.get_position()
            reward = grid_world.grid[y][x].value
            grid_world.update_known_value(x, y, reward)
            grid_world.reset()

def _print_cell_value_with_arrow(grid_world, x, y, actions):
    val = grid_world.grid[y][x].value
    absval = abs(val)
    if Action.LEFT in actions:
        print('<', end='')
    else:
        print(' ', end='')
    if(val == 0):
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
    if Action.RIGHT in actions:
        print('>', end='')
    else:
        print(' ', end='')

def printgrid(grid_world):
    for y in range(len(grid_world.grid)):
        actions = get_best_choices(grid_world, x, y)
        grid_world._print_grid_line()
        for x in range(len(grid_world.grid[y])):
            if Action.UP in actions:
                print('|    ^    ', end='')
            else:
                print('|         ', end='')
        print('|')
        for x in range(len(grid_world.grid[y])):
            print('|', end='')
            if x == grid_world.agent_x and y == grid_world.agent_y:
                print(Color.UNDERLINE)
            if isinstance(grid_world.grid[y][x], ExitCell):
                _print_cell_value_with_arrow(grid_world, x, y, actions)
            elif not grid_world.grid[y][x].can_move:
                print('         ', end='')
            else:
                _print_cell_value_with_arrow(grid_world, x, y, actions)
        print('|')
        for x in range(len(grid_world.grid[y])):
            if Action.DOWN in actions:
                print('|    v    ', end='')
            else:
                print('|         ', end='')
    grid_world._print_grid_line()

                    



if __name__ == '__main__':
    os.system('color')
    (grid, _, eps, a) = reader.read_grid("grid.txt")
    iterate(grid, eps, a)


