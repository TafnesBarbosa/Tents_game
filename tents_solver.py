from constants import *
from utils import *

class TentsGameSolver(object):
    def __init__(self, tents_game, state):
        self.tents_game = tents_game
        self.state = state
        self.trees_possibilities = Heap([]) # heap to use in solving
        self.entrou_equal0 = False
        self.entrou_equal1tent = False
        self.entrou_equaltiptent = False
        self.acabou_pela_regra = False
    
    def change_state(self, new_state):
        self.state = new_state

    def update(self):
        self.state.execute(self.tents_game, self.trees_possibilities, self)

class State(object):
    def __init__(self, state_name):
        """
        Creates a state.

        :param state_name: the name of the state.
        :type state_name: str
        """
        self.state_name = state_name

    def execute(self, tents_game, trees_possibilities, solver):
        """
        Executes the state logic.

        :param tents_game: the tents_game where this state is being executed on.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")
    
    def check_row_column_equal_0(self, tents_game):
        for x, y in zip(tents_game.tips_x, tents_game.tips_y):
            if x == 0 or y == 0:
                return True
        return False

    def check_row_column_equal_n_posibilities(self, tents_game):
        for j, x in enumerate(tents_game.tips_x_copy):
            number_posibilities = 0
            for i in range(tents_game.size):
                if tents_game.field[i, j] == POSSIBLE_TENT:
                    number_posibilities += 1
            if number_posibilities == x:
                return True
            
        for i, y in enumerate(tents_game.tips_y_copy):
            number_posibilities = 0
            for j in range(tents_game.size):
                if tents_game.field[i, j] == POSSIBLE_TENT:
                    number_posibilities += 1
            if number_posibilities == y:
                return True
        return False

    def check_n_posibilities_of_tree(self, tents_game):
        return tents_game.pq[0][0]

    def update_minimum_heap(self, tents_game, trees_possibilities, i, j):
        for ii, jj in FOUR_CONNECTED:
            if tents_game.is_valid_coordinate(i+ii, j+jj) and tents_game.field[i+ii, j+jj] == TREE:
                index = trees_possibilities.find((i+ii, j+jj))
                trees_possibilities.modify(index, (trees_possibilities[index][0]-1, trees_possibilities[index][1]))
    
    def put_tent(self, tree, tents_game, trees_possibilities, know_what_tree = True):
        if know_what_tree:
            for i, j in FOUR_CONNECTED:
                if tents_game.is_valid_coordinate(tree[0]+i, tree[1]+j):
                    if tents_game.field[tree[0]+i, tree[1]+j] == POSSIBLE_TENT:
                        tents_game.field[tree[0]+i, tree[1]+j] = TENT
                        self.update_8_connected((tree[0]+i, tree[1]+j), tents_game, trees_possibilities)
                        tents_game.tips_x_copy[tree[1]+j] -= 1
                        tents_game.tips_y_copy[tree[0]+i] -= 1
        else:
            if tree[0] != -1:
                for j in range(tents_game.size):
                    if tents_game.field[tree[0], j] == POSSIBLE_TENT:
                        tents_game.field[tree[0], j] = TENT
                        self.update_8_connected((tree[0], j), tents_game, trees_possibilities)
                        tents_game.tips_y_copy[tree[0]] -= 1
                        tents_game.tips_x_copy[j] -= 1
            elif tree[1] != -1:
                for i in range(tents_game.size):
                    if tents_game.field[i, tree[1]] == POSSIBLE_TENT:
                        tents_game.field[i, tree[1]] = TENT
                        self.update_8_connected((i, tree[1]), tents_game, trees_possibilities)
                        tents_game.tips_x_copy[tree[1]] -= 1
                        tents_game.tips_y_copy[i] -= 1
    
    def update_8_connected(self, tent, tents_game, trees_possibilities):
        for i in range(-1,2):
            for j in range(-1,2):
                if tents_game.is_valid_coordinate(tent[0]+i, tent[1]+j) and tents_game.field[tent[0]+i, tent[1]+j] == POSSIBLE_TENT:
                    tents_game.field[tent[0]+i, tent[1]+j] = EMPTY
                    self.update_minimum_heap(tents_game, trees_possibilities, tent[0]+i, tent[1]+j)

class StartState(State):
    """
    State that creates minimum heap, set number of possibilities in the field.
    """
    def __init__(self):
        super().__init__('Start')
        
    def execute(self, tents_game, trees_possibilities, solver):
        # Todo: add execution logic
        for tree in tents_game.trees:
            number_trees = 0
            for i, j in FOUR_CONNECTED:
                if tents_game.is_valid_coordinate(tree[0]+i, tree[1]+j):
                    if tents_game.field[tree[0]+i, tree[1]+j] == EMPTY or tents_game.field[tree[0]+i, tree[1]+j] == POSSIBLE_TENT:
                        tents_game.field[tree[0]+i, tree[1]+j] = POSSIBLE_TENT
                        number_trees += 1
            trees_possibilities.insert((number_trees, tree))
        solver.change_state(Equal0State())

class Equal0State(State):
    def __init__(self):
        super().__init__('RowColumnEqual0')

    def execute(self, tents_game, trees_possibilities, solver):
        solver.entrou_equal0 = False
        for j, tip_x in enumerate(tents_game.tips_x_copy):
            if tip_x == 0:
                solver.entrou_equal0 = True
                tents_game.tips_x_copy[j] = TIPS_ZEROED
                for i in range(tents_game.size):
                    if tents_game.field[i, j] == POSSIBLE_TENT:
                        tents_game.field[i, j] = EMPTY
                        self.update_minimum_heap(tents_game, trees_possibilities, i, j)

        for i, tip_y in enumerate(tents_game.tips_y_copy):
            if tip_y == 0:
                solver.entrou_equal0 = True
                tents_game.tips_y_copy[i] = TIPS_ZEROED
                for j in range(tents_game.size):
                    if tents_game.field[i, j] == POSSIBLE_TENT:
                        tents_game.field[i, j] = EMPTY
                        self.update_minimum_heap(tents_game, trees_possibilities, i, j)
        solver.change_state(Equal1TentState())

class Equal1TentState(State):
    def __init__(self):
        super().__init__('NumberTentsEqual1')

    def execute(self, tents_game, trees_possibilities, solver):
        solver.entrou_equal1tent = False
        while trees_possibilities[0][0] == 1:
            solver.entrou_equal1tent = True
            tree = trees_possibilities[0][1]
            trees_possibilities.extract_min()
            self.put_tent(tree, tents_game, trees_possibilities)
            solver.change_state(Equal0State())
        if not solver.entrou_equal1tent:
            solver.change_state(EqualTipTentsState())

class EqualTipTentsState(State):
    def __init__(self):
        super().__init__('NumberTentsEqualTip')

    def execute(self, tents_game, trees_possibilities, solver):
        solver.entrou_equaltiptent = False
        for i in range(tents_game.size):
            number_possible_tents = 0
            for j in range(tents_game.size):
                if tents_game.field[i, j] == POSSIBLE_TENT:
                    number_possible_tents += 1
            if tents_game.tips_y_copy[i] == number_possible_tents:
                solver.entrou_equaltiptent = True
                self.put_tent((i, -1), tents_game, trees_possibilities, know_what_tree=False)
        
        for j in range(tents_game.size):
            number_possible_tents = 0
            for i in range(tents_game.size):
                if tents_game.field[i, j] == POSSIBLE_TENT:
                    number_possible_tents += 1
            if tents_game.tips_x_copy[j] == number_possible_tents:
                solver.entrou_equaltiptent = True
                self.put_tent((-1, j), tents_game, trees_possibilities, know_what_tree=False)
        solver.change_state(Equal0State())
        if not solver.entrou_equal0 and not solver.entrou_equal1tent and not solver.entrou_equaltiptent:
            solver.acabou_pela_regra = True