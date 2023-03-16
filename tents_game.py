import numpy as np

# Constants
TENT = 2
TREE = 1
EMPTY = 0
OUTSIDE = -1

class TentsGame(object):
    """
    Creates a tents game, where size is the size of rectangular field.

    trees_x and trees_y are the coordinates of the trees, starting at zero of the top left.

    tips_x and tips_y are the number of tents in each column and row respectively
    """

    def __init__(self, size, trees_x, trees_y, tips_x, tips_y):
        self.size = size
        self.field = np.ones((size, size), dtype = int) * EMPTY
        for x, y in zip(trees_x, trees_y):
            self.field[y, x] = TREE

        self.tips_x = tips_x
        self.tips_y = tips_y

    def __repr__(self):
        field_repr = '   '
        for i in range(len(self.tips_x)):
            field_repr += ' ' + str(self.tips_x[i])
        field_repr += '\n   '
        for i in range(len(self.tips_x)):
            field_repr += '--'
        field_repr += '\n'

        for i in range(self.size):
            field_repr += str(self.tips_y[i]) + ' |'
            for j in range(self.size):
                if self.field[i, j] == TREE:
                    field_repr += ' ' + '\U00002663'
                elif self.field[i, j] == EMPTY:
                    field_repr += ' ' + '\U000025A1'
                elif self.field[i, j] == TENT:
                    field_repr += ' ' + '\U000025B2'
            field_repr += '\n'
        return field_repr

a = TentsGame(6, [1, 4, 3, 4, 0, 0, 1], [0, 0, 2, 2, 3, 4, 5], [2, 1, 1, 1, 1, 1], [2, 1, 0, 2, 0, 2])
print(a)