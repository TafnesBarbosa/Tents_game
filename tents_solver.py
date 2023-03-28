from constants import *
from utils import *
from math import inf
counter = 0

class TentsGameSolver(object):
    def __init__(self, tents_game, state):
        self.tents_game = tents_game
        self.state = state
        self.trees_possibilities = Heap([]) # heap to use in solving
        self.entrou_equal0 = False
        self.entrou_equal1tent = False
        self.entrou_equaltiptent = False
        self.acabou_pela_regra = False
        self.queue = [] # To store the previous state of solving: field, tips_copy
    
    def change_state(self, new_state):
        self.previous_state = self.state
        self.state = new_state

    def update(self):
        self.state.execute(self)

class State(object):
    def __init__(self, state_name):
        """
        Creates a state.

        :param state_name: the name of the state.
        :type state_name: str
        """
        self.state_name = state_name

    def __repr__(self):
        return self.state_name

    def execute(self, solver):
        """
        Executes the state logic.

        :param tents_game: the tents_game where this state is being executed on.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")

    def update_minimum_heap(self, tents_game, trees_possibilities, i, j):
        for ii, jj in FOUR_CONNECTED:
            if tents_game.is_valid_coordinate(i+ii, j+jj) and tents_game.field[i+ii, j+jj] == TREE:
                index = trees_possibilities.find((i+ii, j+jj))
                if index != None:
                    trees_possibilities.modify(index, (trees_possibilities[index][0]-1, trees_possibilities[index][1]))
    
    def put_tent(self, tree, tents_game, trees_possibilities, know_what_tree = True, have_one_possibility = True, tent = (None, None)):
        if know_what_tree:
            if have_one_possibility:
                for i, j in FOUR_CONNECTED:
                    if tents_game.is_valid_coordinate(tree[0]+i, tree[1]+j):
                        if tents_game.field[tree[0]+i, tree[1]+j] == POSSIBLE_TENT:
                            tents_game.field[tree[0]+i, tree[1]+j] = TENT
                            self.update_8_connected((tree[0]+i, tree[1]+j), tents_game, trees_possibilities)
                            tents_game.tips_x_copy[tree[1]+j] -= 1
                            tents_game.tips_y_copy[tree[0]+i] -= 1
            else:
                tents_game.field[tent[0], tent[1]] = TENT
                self.update_8_connected((tent[0], tent[1]), tents_game, trees_possibilities)
                tents_game.tips_x_copy[tent[1]] -= 1
                tents_game.tips_y_copy[tent[0]] -= 1

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

    def save_state_of_solving(self, solver, before=True, possible_tent=(None, None)):
        if before:
            solver.queue.append((
                solver.tents_game.field.copy(),
                solver.tents_game.tips_x_copy.copy(),
                solver.tents_game.tips_y_copy.copy(),
                Heap(solver.trees_possibilities.copy()),
                solver.entrou_equal0,
                solver.entrou_equal1tent,
                solver.entrou_equaltiptent,
                solver.acabou_pela_regra
            ))
        else:
            state = solver.queue.pop()
            solver.queue.append((
                state[0],
                state[1],
                state[2],
                state[3],
                state[4],
                state[5],
                state[6],
                state[7],
                possible_tent
            ))

    def return_to_last_state(self, solver):
        if len(solver.queue[-1]) == 9:
            (
                solver.tents_game.field,
                solver.tents_game.tips_x_copy,
                solver.tents_game.tips_y_copy,
                solver.trees_possibilities,
                solver.entrou_equal0,
                solver.entrou_equal1tent,
                solver.entrou_equaltiptent,
                solver.acabou_pela_regra,
                possible_tent
            ) = solver.queue.pop()
            return possible_tent
        else:
            (
                solver.tents_game.field,
                solver.tents_game.tips_x_copy,
                solver.tents_game.tips_y_copy,
                solver.trees_possibilities,
                solver.entrou_equal0,
                solver.entrou_equal1tent,
                solver.entrou_equaltiptent,
                solver.acabou_pela_regra
            ) = solver.queue.pop()
            return None

    def check_if_is_over(self, solver):
        solver.acabou_pela_regra = True
        for tip_x, tip_y in zip(solver.tents_game.tips_x_copy, solver.tents_game.tips_x_copy):
            if tip_x != TIPS_ZEROED or tip_y != TIPS_ZEROED:
                solver.acabou_pela_regra = False
        if len(solver.trees_possibilities) == 0:
            solver.acabou_pela_regra = True
        if self.check_if_is_wrong(solver, solver.acabou_pela_regra):
            solver.acabou_pela_regra = False
            solver.change_state(ReturnPreviousState())
            
    def check_if_is_wrong(self, solver, is_over):
        if not is_over: # If number of tents is greater of tips
            for j, tip_x in enumerate(solver.tents_game.tips_x):
                number_tents = 0
                for i in range(solver.tents_game.size):
                    if solver.tents_game.field[i, j] == TENT:
                        number_tents += 1
                if tip_x < number_tents:
                    return True
            
            for i, tip_y in enumerate(solver.tents_game.tips_y):
                number_tents = 0
                for j in range(solver.tents_game.size):
                    if solver.tents_game.field[i, j] == TENT:
                        number_tents += 1
                if tip_y < number_tents:
                    return True
        else: # if number of tips is different of number of tents
            for j, tip_x in enumerate(solver.tents_game.tips_x):
                number_tents = 0
                for i in range(solver.tents_game.size):
                    if solver.tents_game.field[i, j] == TENT:
                        number_tents += 1
                if tip_x != number_tents:
                    return True
            
            for i, tip_y in enumerate(solver.tents_game.tips_y):
                number_tents = 0
                for j in range(solver.tents_game.size):
                    if solver.tents_game.field[i, j] == TENT:
                        number_tents += 1
                if tip_y != number_tents:
                    return True
        return False

class StartState(State):
    """
    State that creates minimum heap, set number of possibilities in the field.
    """
    def __init__(self):
        super().__init__('Start')
        
    def execute(self, solver):
        # Todo: add execution logic
        for tree in solver.tents_game.trees:
            number_possible_tents = 0
            for i, j in FOUR_CONNECTED:
                if solver.tents_game.is_valid_coordinate(tree[0]+i, tree[1]+j):
                    if solver.tents_game.field[tree[0]+i, tree[1]+j] == EMPTY or solver.tents_game.field[tree[0]+i, tree[1]+j] == POSSIBLE_TENT:
                        solver.tents_game.field[tree[0]+i, tree[1]+j] = POSSIBLE_TENT
                        number_possible_tents += 1
            solver.trees_possibilities.insert((number_possible_tents, tree))
        solver.change_state(Equal0State())
        self.check_if_is_over(solver)

class Equal0State(State):
    def __init__(self):
        super().__init__('RowColumnEqual0')

    def execute(self, solver):
        solver.entrou_equal0 = False
        for j, tip_x in enumerate(solver.tents_game.tips_x_copy):
            if tip_x == 0:
                solver.entrou_equal0 = True
                solver.tents_game.tips_x_copy[j] = TIPS_ZEROED
                for i in range(solver.tents_game.size):
                    if solver.tents_game.field[i, j] == POSSIBLE_TENT:
                        solver.tents_game.field[i, j] = EMPTY
                        self.update_minimum_heap(solver.tents_game, solver.trees_possibilities, i, j)

        for i, tip_y in enumerate(solver.tents_game.tips_y_copy):
            if tip_y == 0:
                solver.entrou_equal0 = True
                solver.tents_game.tips_y_copy[i] = TIPS_ZEROED
                for j in range(solver.tents_game.size):
                    if solver.tents_game.field[i, j] == POSSIBLE_TENT:
                        solver.tents_game.field[i, j] = EMPTY
                        self.update_minimum_heap(solver.tents_game, solver.trees_possibilities, i, j)
        solver.change_state(Equal1TentState())
        self.check_if_is_over(solver)

class Equal1TentState(State):
    def __init__(self):
        super().__init__('NumberTentsEqual1')

    def execute(self, solver):
        solver.entrou_equal1tent = False
        while len(solver.trees_possibilities) > 0 and solver.trees_possibilities[0][0] == 1:
            solver.entrou_equal1tent = True
            tree = solver.trees_possibilities[0][1]
            solver.trees_possibilities.extract_min()
            self.put_tent(tree, solver.tents_game, solver.trees_possibilities)
            solver.change_state(Equal0State())
        if not solver.entrou_equal1tent:
            if solver.trees_possibilities[0][0] == 0:
                tree = solver.trees_possibilities[0][1]
                entrou = False
                for i, j in FOUR_CONNECTED:
                    if solver.tents_game.is_valid_coordinate(tree[0]+i, tree[1]+j):
                        if solver.tents_game.field[tree[0]+i, tree[1]+j] == TENT:
                            solver.trees_possibilities.extract_min()
                            entrou = True
                            break
                if not entrou: # if number of possibilities is zero and there is no tent
                    solver.change_state(ReturnPreviousState())

                
            solver.change_state(EqualTipTentsState())
        self.check_if_is_over(solver)

class EqualTipTentsState(State):
    def __init__(self):
        super().__init__('NumberTentsEqualTip')

    def execute(self, solver):
        solver.entrou_equaltiptent = False
        for i in range(solver.tents_game.size):
            number_possible_tents = 0
            for j in range(solver.tents_game.size):
                if solver.tents_game.field[i, j] == POSSIBLE_TENT:
                    number_possible_tents += 1
            if solver.tents_game.tips_y_copy[i] == number_possible_tents:
                solver.entrou_equaltiptent = True
                self.put_tent((i, -1), solver.tents_game, solver.trees_possibilities, know_what_tree=False)
        
        for j in range(solver.tents_game.size):
            number_possible_tents = 0
            for i in range(solver.tents_game.size):
                if solver.tents_game.field[i, j] == POSSIBLE_TENT:
                    number_possible_tents += 1
            if solver.tents_game.tips_x_copy[j] == number_possible_tents:
                solver.entrou_equaltiptent = True
                self.put_tent((-1, j), solver.tents_game, solver.trees_possibilities, know_what_tree=False)
        solver.change_state(Equal0State())
        if not solver.entrou_equal0 and not solver.entrou_equal1tent and not solver.entrou_equaltiptent:
            self.check_if_is_over(solver)
            if not solver.acabou_pela_regra:
                solver.change_state(HeuristicState())

class HeuristicState(State):
    def __init__(self):
        super().__init__('HeuristicaState')

    def execute(self, solver):
        before = True
        self.save_state_of_solving(solver, before)
        tree = solver.trees_possibilities[0][1]
        while len(solver.trees_possibilities) > 0 and solver.trees_possibilities[0][0] <= 0:
            solver.trees_possibilities.extract_min()
            if len(solver.trees_possibilities) > 0:
                tree = solver.trees_possibilities[0][1]
            else:
                self.check_if_is_over(solver)
                # solver.change_state(ReturnPreviousState())
        else:
            if len(solver.trees_possibilities) > 0:
                solver.trees_possibilities.extract_min()
                mini = inf
                minii = None
                minij = None
                for i, j in FOUR_CONNECTED:
                    if solver.tents_game.is_valid_coordinate(tree[0]+i,tree[1]+j):
                        if solver.tents_game.field[tree[0]+i,tree[1]+j] == POSSIBLE_TENT:
                            if solver.tents_game.tips_x_copy[j] + solver.tents_game.tips_y_copy[i] < mini:
                                minii = i
                                minij = j
                                mini = solver.tents_game.tips_x_copy[j] + solver.tents_game.tips_y_copy[i]
                if minii != None:
                    self.put_tent(tree, solver.tents_game, solver.trees_possibilities, know_what_tree=True, have_one_possibility=False, tent=(tree[0]+minii,tree[1]+minij))
                    self.save_state_of_solving(solver, False, possible_tent=(tree[0]+minii,tree[1]+minij))
                else:
                    print('i, j = None')
                
        solver.change_state(Equal0State())
        self.check_if_is_over(solver)

class ReturnPreviousState(State):
    def __init__(self):
        super().__init__('ReturnPreviousState')

    def execute(self, solver):
        possible_tent = self.return_to_last_state(solver)
        if possible_tent != None:
            solver.tents_game.field[possible_tent[0], possible_tent[1]] = EMPTY
            self.update_minimum_heap(solver.tents_game, solver.trees_possibilities, possible_tent[0], possible_tent[1])
            solver.change_state(HeuristicState())
            global counter 
            counter += 1
            if counter % 100 == 0:
                print(counter)
        else:
            solver.change_state(ReturnPreviousState())
