"""
cell.py
Cells that make up gridworld
"""

from abc import ABC
from action import Action


class GridItem(ABC):
    '''
    Reprents any cell in the problem grid, abstract class
    '''

    # Accepts position, whether or not this is a cell you can move on, and a value for the cell
    # y=0 is the top row
    def __init__(self, x, y, can_move=True, value=0):
        self.x = x
        self.y = y
        self.can_move = can_move
        self.value = value
        self.known_value = 0
        self.q_values = {
            Action.UP: 0,
            Action.DOWN: 0,
            Action.LEFT: 0,
            Action.RIGHT: 0
        }

    # updates the value of a state to a passed value (does not use alpha, just accepts the new value)
    def update_value(self, value):
        if value is None:
            raise ValueError("Value cannot be None")
        self.value = value

    # Updates the known value, similar to update_value but for q learning
    def update_known_value(self, value):
        if value is None:
            raise ValueError("Value cannot be None")
        self.known_value = value


class BoulderCell(GridItem):
    '''
    Represents a boulder cell
    '''

    def __init__(self, x, y):
        super().__init__(x, y, False)

    # These get no values!
    def update_value(self, value):
        pass


class EmptyCell(GridItem):
    '''
    Represents an default cell
    '''

    def __init__(self, x, y):
        super().__init__(x, y, True)


class ExitCell(GridItem):
    '''
    Represents an exit cell
    '''

    def __init__(self, x, y, value=0):
        super().__init__(x, y, False, value)

    # These get no values!
    def update_value(self, value):
        pass
