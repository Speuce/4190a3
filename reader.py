import os
from typing import Dict, List, Tuple
from grid_world import GridWorld
from cell import EmptyCell, ExitCell, BoulderCell, GridItem

file_name = "grid.txt" # change this to the name of your file

def parse_terminal_boulder_line(line):
    data = line.strip("{}\n")
    items = data.split("},")
    result = {}
    for item in items:
        print(item)
        key, values = item.split("={")
        values = values.strip("}").split(",")
        int_values = list(map(int, values[:2]))
        if len(values) == 3:
            int_values.append(float(values[2]))
        result[int(key)] = tuple(int_values)
    return result

def read_values_from_file(file_path):
    config = {}
    with open(file_path, "r") as file:
        for line in file:
            if "=" in line:
                print(line)
                key, value = line.split("=", 1)
                if key in ["Terminal", "Boulder"]:
                    config[key] = parse_terminal_boulder_line(value)
                elif key == "RobotStartState":
                    config[key] = tuple(map(int, value.strip("{}\n").split(",")))
                else:
                    try:
                        config[key] = int(value.strip())
                    except ValueError:
                        try:
                            config[key] = float(value.strip())
                        except ValueError:
                            pass
    return config

def build_grid(horizontal: int, vertical: int,
               terminal: Dict[int, Tuple[int, int, int]],
               boulder: Dict[int, Tuple[int, int, int]]) -> List[List[GridItem]]:
    grid = []
    for y in range(vertical):
        row = []
        for x in range(horizontal):
            row.append(EmptyCell(x, y))
        grid.append(row)

    for key, value in terminal.items():
        x, y, value = value
        grid[y][x] = ExitCell(x, y, value)

    for key, value in boulder.items():
        x, y = value
        grid[y][x] = BoulderCell(x, y)
    return grid



def read_grid(file: str) -> Tuple[GridWorld, int, int, int]:
    config = read_values_from_file(file_name)
    grid = build_grid(config["Horizontal"], config["Vertical"], config["Terminal"], config["Boulder"])
    start_x, start_y = config["RobotStartState"]
    noise = config["Noise"]
    transition_cost = config["TransitionCost"]
    discount = config["Discount"]
    depth = config["K"]
    episodes = config["Episodes"]
    alpha = config["alpha"]
    return (GridWorld(grid, start_x, start_y, noise, transition_cost, discount), depth, episodes, alpha)


if __name__ == "__main__":
    os.system('color')
    grid_world = read_grid(file_name)
    grid_world.print()