"""
Reader.py

Reads the queries from the file and runs the appropriate algorithms on the given gridworld
"""

import os
import sys
import random
from typing import Dict, List, Tuple
from grid_world import GridWorld
from cell import EmptyCell, ExitCell, BoulderCell, GridItem
import valueiteration
import q_value_learning


def read_queries(file: str) -> List[Tuple[int, str, str]]:
    '''
    Reads the queries from the file
    '''
    queries = []
    with open(file, "r") as file:
        for line in file:
            if line.startswith("#"):
                continue
            h, v, step, method, query = line.strip().split(",")
            queries.append((int(step), method, query))
    return queries


def parse_terminal_boulder_line(line):
    '''
    Helper function for parsing the terminal and boulder states
    '''
    data = line.strip("{}\n")
    items = data.split("},")
    result = {}
    for item in items:
        key, values = item.split("={")
        values = values.strip("}").split(",")
        int_values = list(map(int, values[:2]))
        if len(values) == 3:
            int_values.append(float(values[2]))
        result[int(key)] = tuple(int_values)
    return result


def read_values_from_file(file_path):
    '''
    Reads the config values from the grid file
    '''
    config = {}
    with open(file_path, "r") as file:
        for line in file:
            if "=" in line:
                key, value = line.split("=", 1)
                if key in ["Terminal", "Boulder"]:
                    config[key] = parse_terminal_boulder_line(value)
                elif key == "RobotStartState":
                    config[key] = tuple(
                        map(int,
                            value.strip("{}\n").split(",")))
                else:
                    try:
                        config[key] = int(value.strip())
                    except ValueError:
                        try:
                            config[key] = float(value.strip())
                        except ValueError:
                            pass
    return config


def build_grid(
        horizontal: int, vertical: int, terminal: Dict[int, Tuple[int, int,
                                                                  int]],
        boulder: Dict[int, Tuple[int, int, int]]) -> List[List[GridItem]]:
    '''
    Builds the grid from the config values
    '''
    grid = []
    for y in range(vertical):
        row = []
        for x in range(horizontal):
            row.append(EmptyCell(x, y))
        grid.append(row)

    for key, value in terminal.items():
        x, y, value = value
        grid[vertical - y - 1][x] = ExitCell(x, vertical - y - 1, value)

    for key, value in boulder.items():
        x, y = value
        grid[vertical - y - 1][x] = BoulderCell(x, vertical - y - 1)
    return grid


def read_grid(file: str) -> Tuple[GridWorld, int, int, int]:
    '''
    Reads the grid from the file
    '''
    config = read_values_from_file(file)
    grid = build_grid(config["Horizontal"], config["Vertical"],
                      config["Terminal"], config["Boulder"])
    start_x, start_y = config["RobotStartState"]
    noise = config["Noise"]
    transition_cost = config["TransitionCost"]
    discount = config["Discount"]
    depth = config["K"]
    episodes = config["Episodes"]
    alpha = config["alpha"]
    return (GridWorld(grid, start_x, (config["Vertical"] - 1 - start_y), noise,
                      transition_cost, discount), depth, episodes, alpha)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python reader.py <grid> <queries>")
        exit(1)
    os.system('color')
    seed = random.randint(0, 1000)
    grid_file_name = sys.argv[1]
    queries_file_name = sys.argv[2]
    queries = read_queries(queries_file_name)
    for (step, method, query) in queries:
        (grid, k, eps, a) = read_grid(grid_file_name)
        random.seed(seed)
        print("Step: " + str(step) + " Method: " + method)
        if method == "MDP":
            valueiteration.iterate(grid, step)
            valueiteration.print_grid(grid)
        elif method == "RL":
            q_value_learning.iterate(grid, step, a)
            if query == "bestPolicy":
                q_value_learning.printgrid(grid)
            else:
                q_value_learning.printgridqvals(grid)
        else:
            print("Unknown method: " + method)
