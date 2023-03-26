from abc import ABC, abstractmethod
from action import Action

class GridItem(ABC):
    '''
    Reprents any cell in the problem grid
    '''
    def __init__(self, x, y, can_move=True, value=0):
        self.x = x 
        self.y = y
        self.can_move=can_move
        self.value = value
        self.q_values = {Action.UP: 0, Action.DOWN: 0, Action.LEFT: 0, Action.RIGHT: 0}

    # @abstractmethod
    def update_value(self, value):
        if value is None:
            raise ValueError("Value cannot be None")
        self.value = value


class BoulderCell(GridItem):
    '''
    Represents a boulder cell
    '''
    def __init__(self, x, y):
        super().__init__(x, y, False)

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
        super().__init__(x, y, True, value)
    
    def update_value(self, value):
        pass




