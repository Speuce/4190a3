from grid_world import GridWorld
from action import Action
import random as rand

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
    grid_world.update_value(x, y, getValue(grid_world, x, y))

def get_policy(grid_world, x, y):
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
    return rand.choice(best_choices)

def iterate():
    grid_world, eps = reader.read_grid()
    for i in range(k):
        for y in len(grid_world.grid):
            for x in len(grid_world.grid[y]):
                best_reward = None
                if grid_world.is_cell(x, y):
                    for action in grid_world.agent_actions:
                        grid_world.set_agent(x, y)
                        reward = grid_world.take_action(x, y, action)
                        if best_reward is None or reward > best_reward:
                            best_reward = reward
                    grid_world.update_value(x, y, best_reward)




if __name__ == '__main__':
    iterate()


