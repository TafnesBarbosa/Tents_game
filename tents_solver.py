from constants import *
from utils import *

# agent is the tents_game
# FSM is the tents_game_solver

class TentsGameSolver(object):
    def __init__(self, tents_game, state):
        self.tents_game = tents_game
        self.state = state
    
    def change_state(self, new_state, finished=False):
        self.state = new_state
        self.state.finished = finished

    def update(self):
        self.state.execute(self.tents_game)
        self.state.check_transition(self.tents_game, self)

class State(object):
    def __init__(self, state_name):
        """
        Creates a state.

        :param state_name: the name of the state.
        :type state_name: str
        """
        self.state_name = state_name
        self.finished = False

    def check_transition(self, agent, fsm):
        """
        Checks conditions and execute a state transition if needed.

        :param agent: the agent where this state is being executed on.
        :param fsm: finite state machine associated to this state.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")

    def execute(self, agent):
        """
        Executes the state logic.

        :param agent: the agent where this state is being executed on.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")
    
    def check_row_column_equal_0(self, agent):
        for x, y in zip(agent.tips_x, agent.tips_y):
            if x == 0 or y == 0:
                return True
        return False

    def check_row_column_equal_n_posibilities(self, agent):
        for j, x in enumerate(agent.tips_x_copy):
            number_posibilities = 0
            for i in range(agent.size):
                if agent.field[i, j] == POSSIBLE_TENT:
                    number_posibilities += 1
            if number_posibilities == x:
                return True
            
        for i, y in enumerate(agent.tips_y_copy):
            number_posibilities = 0
            for j in range(agent.size):
                if agent.field[i, j] == POSSIBLE_TENT:
                    number_posibilities += 1
            if number_posibilities == y:
                return True
        return False

    def check_n_posibilities_of_tree(self, agent):
        return agent.pq[0][0]
                    
    
class I1State(State):
    def __init__(self):
        super().__init__('I1')

    def check_transition(self, agent, state_machine):
        # Todo: add logic to check and execute state transition
        if self.finished:
            if self.check_row_column_equal_0(agent):
                state_machine.change_state(S1State())
            else:
                state_machine.change_state(S1State(), finished=True)
            if not self.check_row_column_equal_0(agent) and not self.check_row_column_equal_n_posibilities(agent) and self.check_n_posibilities_of_tree(agent) > 1:
                state_machine.change_state(S3State())
            elif self.check_n_posibilities_of_tree(agent) == 0:
                state_machine.change_state(S4State())
        
    def execute(self, agent):
        # Todo: add execution logic
        if not self.finished:
            for tree in agent.trees:
                number_trees = 0
                for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    if tree[0] + x >= 0 and tree[0] + x < agent.size and tree[1] + y >= 0 and tree[1] + y < agent.size:
                        if agent.field[tree[0] + x, tree[1] + y] != TREE:
                            agent.field[tree[0] + x, tree[1] + y] = POSSIBLE_TENT
                            number_trees += 1
                agent.pq.insert((number_trees, tree))
            self.finished = True


class S1State(State):
    def __init__(self):
        super().__init__('S1')

    def check_transition(self, agent, state_machine):
        # Todo: add logic to check and execute state transition
        if self.finished:
            if self.check_row_column_equal_n_posibilities(agent):
                state_machine.change_state(S2State())
            else:
                state_machine.change_state(S2State(), finished=True)
        
    def execute(self, agent):
        # Todo: add execution logic
        if not self.finished:
            for k, x in enumerate(agent.tips_x_copy):
                if x == 0:
                    for i in range(agent.size):
                        if agent.field[i, k] == POSSIBLE_TENT:
                            agent.field[i, k] = EMPTY
                            for ii, jj in [(-1,0),(1,0),(0,-1),(0,1)]:
                                if ii + i >= 0 and ii + i < agent.size and jj + k >= 0 and jj + k < agent.size:
                                    if agent.field[ii+i, jj+k] == TREE:
                                        index = agent.pq.find((ii+i, jj+k))
                                        agent.pq.modify(index, (agent.pq[index][0]-1, (ii+i, jj+k)))
                    agent.tips_x_copy[k] = TIPS_ZEROED
                            
                                             
            for k, y in enumerate(agent.tips_y_copy):
                if y == 0:
                    for j in range(agent.size):
                        if agent.field[k, j] == POSSIBLE_TENT:
                            agent.field[k, j] = EMPTY
                            for ii, jj in [(-1,0),(1,0),(0,-1),(0,1)]:
                                if ii + k >= 0 and ii + k < agent.size and jj + j >= 0 and jj + j < agent.size:
                                    if agent.field[ii+k, jj+k] == TREE:
                                        index = agent.pq.find((ii+k, jj+k))
                                        agent.pq.modify(index, (agent.pq[index][0]-1, (ii+k, jj+j)))
                    agent.tips_y_copy[k] = TIPS_ZEROED
            self.finished = True

class S2State(State):
    def __init__(self):
        super().__init__('S2')

    def check_transition(self, agent, state_machine):
        # Todo: add logic to check and execute state transition
        if self.finished:
            if self.check_n_posibilities_of_tree(agent) == 1:
                state_machine.change_state(S2State())
            elif self.check_n_posibilities_of_tree(agent) > 1:
                state_machine.change_state(I1State(), finished=True)
            else:
                state_machine.change_state(S4State())
        
    def execute(self, agent):
        # Todo: add execution logic
        pass
        

class S3State(State):
    def __init__(self):
        super().__init__('S3')

    def check_transition(self, agent, state_machine):
        # Todo: add logic to check and execute state transition
        if self.finished:
            state_machine.change_state(I1State(), finished=True)
        
    def execute(self, agent):
        # Todo: add execution logic
        pass

class S4State(State):
    def __init__(self):
        super().__init__('S4')

    def check_transition(self, agent, state_machine):
        # Todo: add logic to check and execute state transition
        if self.finished:
            state_machine.change_state(S3State())
        
    def execute(self, agent):
        # Todo: add execution logic
        pass