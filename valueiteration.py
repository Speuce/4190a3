import os
from grid_world import GridWorld
from action import Action
import reader

def iterate(grid_world: GridWorld, k: int):
    for i in range(k):
        print("Iteration: " + str(i))
        grid_world.print()
        for y in range(len(grid_world.grid)):
            for x in range(len(grid_world.grid[y])):
                best_reward = None
                if grid_world.is_cell(x, y):
                    for action in grid_world.agent_actions:
                        grid_world.set_position(x, y)
                        reward = grid_world.get_weighted_action_reward(action)
                        if best_reward is None or reward > best_reward:
                            best_reward = reward
                    grid_world.update_value(x, y, best_reward)


if __name__ == '__main__':
    os.system('color')
    (grid, k, _, _) = reader.read_grid("grid.txt")
    iterate(grid, 10)


