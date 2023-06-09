from constants import *
from utils import *
from math import inf
import time
counter = 0

class TentsGameSolver(object):
    def __init__(self, tents_game):
        self.tents_game = tents_game
        self.field = tents_game.field
        self.size = tents_game.size
        self.tips_x_copy = tents_game.tips_x_copy
        self.tips_y_copy = tents_game.tips_y_copy
        self.tips_x = tents_game.tips_x
        self.tips_y = tents_game.tips_y
        self.trees = tents_game.trees
        self.trees_possibilities = HeapMin([]) # heap to use in solving
        self.possible_tents = HeapMax([])
        self.verified_tips_equal_0 = False
        self.verified_possible_tents_equal_1 = False
        self.verified_tips_equal_possible_tents = False
        self.is_wrong = False
        self.state_queue = [] # To store the previous state of solving: field, tips_copy
        self.tents_put = []

        # tic = time.time()
        self.do_func(self.start, self.verifies_tips_equal_0)
        self.do_func(self.verifies_possible_tents_equal_1, self.verifies_tips_equal_0)
        while self.verified_possible_tents_equal_1:
            self.do_func(self.verifies_possible_tents_equal_1, self.verifies_tips_equal_0)
        
        self.do_func(self.verifies_tips_equal_possible_tents, self.verifies_tips_equal_0)
        while self.verified_tips_equal_possible_tents or self.verified_possible_tents_equal_1 or self.verified_tips_equal_0:
            self.do_func(self.verifies_tips_equal_possible_tents, self.verifies_tips_equal_0)
            if len(self.tents_put) == 0:
                self.do_func(self.verifies_possible_tents_equal_1, self.verifies_tips_equal_0)
                while self.verified_possible_tents_equal_1:
                    self.do_func(self.verifies_possible_tents_equal_1, self.verifies_tips_equal_0)
        # toc = time.time()
        # print(toc-tic)
        # print('Finished initial state')
        self.check_is_wrong()
        self.heuristic()

    def do_func(self, func1, func2):
        func1()
        func2()

    def is_valid_coordinate(self, i, j):
        if i >= 0 and i < self.size and j >= 0 and j < self.size:
            return True
        return False 

    def update_minimum_heap(self, i, j):
        for ii, jj in FOUR_CONNECTED:
            coord_i = i + ii
            coord_j = j + jj
            if self.is_valid_coordinate(coord_i, coord_j) and self.field[coord_i, coord_j] == TREE:
                index = self.trees_possibilities.find((coord_i, coord_j))
                if index != None:
                    self.trees_possibilities.modify(index, (self.trees_possibilities[index][0]-1, self.trees_possibilities[index][1]))

    def update_maximum_heap(self, i, j):
        index = self.possible_tents.find((i, j))
        self.possible_tents.modify(index, (inf, self.possible_tents.heap[index][1]))
        self.possible_tents.extract_max()
        for ii, jj in EIGHT_CONNECTED:
            coord_i = i + ii
            coord_j = j + jj
            if self.is_valid_coordinate(coord_i, coord_j) and self.field[coord_i, coord_j] == POSSIBLE_TENT:
                index = self.possible_tents.find((coord_i, coord_j))
                self.possible_tents.modify(index, (self.possible_tents.heap[index][0]-1, self.possible_tents.heap[index][1]))

    def put_tent(self, tree, know_what_tree=True, tent=(None, None)):
        # if tent == (6, 16):
        #     print('é')
        #     pass
        if know_what_tree:
            for i, j in FOUR_CONNECTED:
                coord_i = tree[0] + i
                coord_j = tree[1] + j
                if self.is_valid_coordinate(coord_i, coord_j):
                    if self.field[coord_i, coord_j] == POSSIBLE_TENT:
                        self.field[coord_i, coord_j] = TENT
                        self.update_8_connected((coord_i, coord_j))
                        self.tips_x_copy[coord_j] -= 1
                        self.tips_y_copy[coord_i] -= 1
        else:
            if self.field[tent[0], tent[1]] == EMPTY:
                self.is_wrong = True
            else:
                self.field[tent[0], tent[1]] = TENT
                self.update_8_connected(tent)
                self.tips_x_copy[tent[1]] -= 1
                self.tips_y_copy[tent[0]] -= 1

    def update_8_connected(self, tent):
        self.update_maximum_heap(tent[0], tent[1])
        self.update_minimum_heap(tent[0], tent[1])
        for i, j in EIGHT_CONNECTED:
            coord_i = tent[0] + i
            coord_j = tent[1] + j
            if self.is_valid_coordinate(coord_i, coord_j):
                if self.field[coord_i, coord_j] == POSSIBLE_TENT:
                    self.field[coord_i, coord_j] = EMPTY
                    self.update_minimum_heap(coord_i, coord_j)
                    self.update_maximum_heap(coord_i, coord_j)

    def remove_trees(self, finished=False):
        if not finished and not self.is_wrong:
            entrou = True
            while entrou:
                entrou = False
                aux = []
                for tent in self.tents_put:
                    num_trees = 0
                    for i, j in FOUR_CONNECTED:
                        coord_i, coord_j = tent[0] + i, tent[1] + j
                        if self.is_valid_coordinate(coord_i, coord_j):
                            if self.field[coord_i, coord_j] == TREE:
                                index = self.trees_possibilities.find((coord_i, coord_j))
                                if index != None:
                                    num_trees += 1
                                    coord_i_aux, coord_j_aux = coord_i, coord_j
                    if num_trees == 1:
                        entrou = True
                        for i, j in FOUR_CONNECTED:
                            coord_i, coord_j = coord_i_aux + i, coord_j_aux + j
                            if self.is_valid_coordinate(coord_i, coord_j):
                                if self.field[coord_i, coord_j] == POSSIBLE_TENT:
                                    tem_arvore = False
                                    for ii, jj in FOUR_CONNECTED:
                                        coord_ii, coord_jj = coord_i + ii, coord_j + jj
                                        if self.is_valid_coordinate(coord_ii, coord_jj):
                                            if self.field[coord_ii, coord_jj] == TREE and (coord_ii, coord_jj) != (coord_i_aux, coord_j_aux):
                                                tem_arvore = True
                                    if not tem_arvore:
                                        self.field[coord_i, coord_j] = EMPTY
                                        self.update_maximum_heap(coord_i, coord_j)
                                        self.update_minimum_heap(coord_i, coord_j)
                        aux.append((tent, coord_i_aux, coord_j_aux))
                if len(aux) > 0:
                    for tent, coord_i, coord_j in aux:
                        indextree = self.trees_possibilities.find((coord_i, coord_j))
                        if indextree != None:
                            self.trees_possibilities.modify(indextree, (-inf, (coord_i, coord_j)))
                            self.trees_possibilities.extract_min()
                            try:
                                self.tents_put.pop(self.tents_put.index(tent))
                            except ValueError:
                                self.is_wrong = True
            
            self.check_has_cycle()

    def check_has_cycle(self):
        possible_tents = []
        for tent in self.tents_put:
            num_trees = 0
            for i, j in FOUR_CONNECTED:
                coord_i, coord_j = tent[0] + i, tent[1] + j
                if self.is_valid_coordinate(coord_i, coord_j):
                    if self.field[coord_i, coord_j] == TREE:
                        index = self.trees_possibilities.find((coord_i, coord_j))
                        if index != None:
                            vale = True
                            for ii, jj in FOUR_CONNECTED:
                                coord_ii, coord_jj = coord_i + ii, coord_j + jj
                                if self.is_valid_coordinate(coord_ii, coord_jj):
                                    if self.field[coord_ii, coord_jj] == POSSIBLE_TENT:
                                        vale = False
                                        break
                            if vale:
                                num_trees += 1
            if num_trees >= 2:
                possible_tents.append(tent)
        trees = []
        trees_quantities = []
        for tent in possible_tents:
            for i, j in FOUR_CONNECTED:
                coord_i, coord_j = tent[0] + i, tent[1] + j
                if self.is_valid_coordinate(coord_i, coord_j):
                    if self.field[coord_i, coord_j] == TREE:
                        if (coord_i, coord_j) not in trees:
                            trees.append((coord_i, coord_j))
                            trees_quantities.append(1)
                        else:
                            trees_quantities[trees.index((coord_i, coord_j))] += 1
            # self.tents_put.pop(self.tents_put.index(tent))
        aux = trees_quantities.count(2) + trees_quantities.count(3) + trees_quantities.count(4)
        if aux == len(possible_tents):
            if aux == len(self.tents_put):
                for tree, quantity in zip(trees, trees_quantities):
                    if quantity == 2:
                        index = self.trees_possibilities.find(tree)
                        self.trees_possibilities.modify(index, (-inf, tree))
                        self.trees_possibilities.extract_min()
                        for i, j in FOUR_CONNECTED:
                            coord_i, coord_j = tree[0] + i, tree[1] + j
                            if self.is_valid_coordinate(coord_i, coord_j):
                                if self.field[coord_i, coord_j] == TENT:
                                    if (coord_i, coord_j) in self.tents_put:
                                        self.tents_put.pop(self.tents_put.index((coord_i, coord_j)))

    def save_state(self, possible_tent, was_tent):
        self.state_queue.append((
            self.field.copy(),
            self.tips_x_copy.copy(),
            self.tips_y_copy.copy(),
            HeapMax(self.possible_tents.heap.copy()),
            HeapMin(self.trees_possibilities.copy()),
            self.tents_put.copy(),
            self.verified_tips_equal_0,
            self.verified_possible_tents_equal_1,
            self.verified_tips_equal_possible_tents,
            self.is_wrong,
            possible_tent,
            was_tent
        ))

    def return_last_state(self):
        (
            self.tents_game.field,
            self.tents_game.tips_x_copy,
            self.tents_game.tips_y_copy,
            self.possible_tents,
            self.trees_possibilities,
            self.tents_put,
            self.verified_tips_equal_0,
            self.verified_possible_tents_equal_1,
            self.verified_tips_equal_possible_tents,
            self.is_wrong,
            possible_tent,
            was_tent
        ) = self.state_queue.pop()
        self.field = self.tents_game.field
        self.tips_x_copy = self.tents_game.tips_x_copy
        self.tips_y_copy = self.tents_game.tips_y_copy
        return possible_tent, was_tent

    def check_is_wrong(self, finished=False):
        if not self.is_wrong:
            # Check if a tree has no tent
            for tree in self.trees:
                self.is_wrong = True
                for i, j in FOUR_CONNECTED:
                    coord_i = tree[0] + i
                    coord_j = tree[1] + j
                    if self.is_valid_coordinate(coord_i, coord_j):
                        if self.field[coord_i, coord_j] == TENT or self.field[coord_i, coord_j] == POSSIBLE_TENT:
                            self.is_wrong = False
                            break
                if self.is_wrong:
                    break
            # Check if number of tents is greater than tips
            for j, tip_x in enumerate(self.tips_x):
                if tip_x < len(np.where(self.field[:, j] == TENT)[0]):
                    self.is_wrong = True
                    break
            for i, tip_y in enumerate(self.tips_y):
                if tip_y < len(np.where(self.field[i, :] == TENT)[0]):
                    self.is_wrong = True
                    break
            if len(self.possible_tents.heap) == 0:
                # Check if number of tents is less than tips when is over
                for j, tip_x in enumerate(self.tips_x):
                    if tip_x > len(np.where(self.field[:, j] == TENT)[0]):
                        self.is_wrong = True
                        break
                for i, tip_y in enumerate(self.tips_y):
                    if tip_y > len(np.where(self.field[i, :] == TENT)[0]):
                        self.is_wrong = True
                        break
                if len(self.trees_possibilities) != 0:
                    self.is_wrong = True
            else:
                pass
        
    # States of the solver    
    def start(self):
        possible_tents = []
        for tree in self.trees:
            num_possible_tents = 0
            for i, j in FOUR_CONNECTED:
                coord_i = tree[0] + i
                coord_j = tree[1] + j
                if self.is_valid_coordinate(coord_i, coord_j):
                    if self.field[coord_i, coord_j] == EMPTY or self.field[coord_i, coord_j] == POSSIBLE_TENT:
                        if self.field[coord_i, coord_j] != POSSIBLE_TENT:
                            possible_tents.append((coord_i, coord_j))
                        self.field[coord_i, coord_j] = POSSIBLE_TENT
                        num_possible_tents += 1
            self.trees_possibilities.insert((num_possible_tents, tree))
        for possible_tent in possible_tents:
            num_possible_tents = 0
            for i, j in EIGHT_CONNECTED:
                coord_i = possible_tent[0] + i
                coord_j = possible_tent[1] + j
                if self.is_valid_coordinate(coord_i, coord_j):
                    if self.field[coord_i, coord_j] == POSSIBLE_TENT:
                        num_possible_tents += 1
            self.possible_tents.insert((num_possible_tents, possible_tent))

    def verifies_tips_equal_0(self):
        self.verified_tips_equal_0 = False
        if not self.is_wrong:
            for j in np.where(self.tips_x_copy == 0)[0]:
                self.verified_tips_equal_0 = True
                self.tips_x_copy[j] = TIPS_ZEROED
                for i in np.where(self.field[:, j] == POSSIBLE_TENT)[0]:
                    self.field[i, j] = EMPTY
                    self.update_minimum_heap(i, j)
                    self.update_maximum_heap(i, j)
            for i in np.where(self.tips_y_copy == 0)[0]:
                self.verified_tips_equal_0 = True
                self.tips_y_copy[i] = TIPS_ZEROED
                for j in np.where(self.field[i, :] == POSSIBLE_TENT)[0]:
                    self.field[i, j] = EMPTY
                    self.update_minimum_heap(i, j)
                    self.update_maximum_heap(i, j)

    def verifies_possible_tents_equal_1(self):
        self.verified_possible_tents_equal_1 = False
        if not self.is_wrong:
            while len(self.trees_possibilities) > 0 and self.trees_possibilities[0][0] == 1:
                self.verified_possible_tents_equal_1 = True
                tree = self.trees_possibilities[0][1]
                self.trees_possibilities.extract_min()
                self.put_tent(tree)

    def verifies_tips_equal_possible_tents(self):
        self.verified_tips_equal_possible_tents = False
        if not self.is_wrong:
            for i in range(self.size):
                aux = np.where(self.field[i, :] == POSSIBLE_TENT)[0]
                if self.tips_y_copy[i] == len(aux):
                    self.verified_tips_equal_possible_tents = True
                    for j in aux:
                        self.put_tent((None, None), know_what_tree=False, tent=(i, j))
                        self.tents_put.append((i, j))
            for j in range(self.size):
                aux = np.where(self.field[:, j] == POSSIBLE_TENT)[0]
                if self.tips_x_copy[j] == len(aux):
                    self.verified_tips_equal_possible_tents = True
                    for i in aux:
                        self.put_tent((None, None), know_what_tree=False, tent=(i, j))
                        self.tents_put.append((i, j))
            self.remove_trees()

    def heuristic(self):
        # global counter
        while len(self.possible_tents.heap) > 0 or self.is_wrong:
            # counter += 1
            # print(counter)
            # if counter == 88:
            #     print('e')
            if not self.is_wrong:
                # print(self.tents_game)
                if self.possible_tents.heap[0][0] >= NUM_POSSIBLE_TENTS_TO_PUT_EMPTY:
                    possible_tent = self.possible_tents.heap[0][1]
                    self.save_state(possible_tent, was_tent=False)
                    self.field[possible_tent[0], possible_tent[1]] = EMPTY
                    self.update_maximum_heap(possible_tent[0], possible_tent[1])
                    self.update_minimum_heap(possible_tent[0], possible_tent[1])
                else:
                    possible_tent = self.possible_tents.heap[0][1]
                    self.save_state(possible_tent, was_tent=True)
                    self.put_tent((None, None), know_what_tree=False, tent=possible_tent)
                    self.tents_put.append(possible_tent)
                    self.remove_trees()
                
                self.verifies_tips_equal_0()
                if len(self.tents_put) == 0:
                    self.do_func(self.verifies_possible_tents_equal_1, self.verifies_tips_equal_0)
                    while self.verified_possible_tents_equal_1:
                        self.do_func(self.verifies_possible_tents_equal_1, self.verifies_tips_equal_0)
                        self.check_is_wrong()
                        if self.is_wrong:
                            break
                
                self.do_func(self.verifies_tips_equal_possible_tents, self.verifies_tips_equal_0)
                self.check_is_wrong()
                while self.verified_tips_equal_possible_tents or self.verified_possible_tents_equal_1 or self.verified_tips_equal_0:
                    self.do_func(self.verifies_tips_equal_possible_tents, self.verifies_tips_equal_0)
                    self.check_is_wrong()
                    if len(self.tents_put) == 0:
                        self.do_func(self.verifies_possible_tents_equal_1, self.verifies_tips_equal_0)
                        self.check_is_wrong()
                        while self.verified_possible_tents_equal_1:
                            self.do_func(self.verifies_possible_tents_equal_1, self.verifies_tips_equal_0)
                            self.check_is_wrong()
                            if self.is_wrong:
                                break
                    if self.is_wrong:
                        break
                # self.verifies_tips_equal_0()
                # self.verifies_tips_equal_possible_tents()
                # self.check_is_wrong()
                # while self.verified_tips_equal_0 or self.verified_tips_equal_possible_tents:
                #     self.verifies_tips_equal_0()
                #     self.verifies_tips_equal_possible_tents()
                #     self.check_is_wrong()
                #     if self.is_wrong:
                #         break
            else:
                possible_tent, was_tent = self.return_last_state()
                if was_tent:
                    self.field[possible_tent[0], possible_tent[1]] = EMPTY
                    self.update_maximum_heap(possible_tent[0], possible_tent[1])
                    self.update_minimum_heap(possible_tent[0], possible_tent[1])
                else:
                    self.put_tent((None, None), know_what_tree=False, tent=possible_tent)
                    self.tents_put.append(possible_tent)
                    self.remove_trees()

                self.verifies_tips_equal_0()
                if len(self.tents_put) == 0:
                    self.do_func(self.verifies_possible_tents_equal_1, self.verifies_tips_equal_0)
                    while self.verified_possible_tents_equal_1:
                        self.do_func(self.verifies_possible_tents_equal_1, self.verifies_tips_equal_0)
                        self.check_is_wrong()
                        if self.is_wrong:
                            break

                self.do_func(self.verifies_tips_equal_possible_tents, self.verifies_tips_equal_0)
                self.check_is_wrong()
                while self.verified_tips_equal_possible_tents or self.verified_possible_tents_equal_1 or self.verified_tips_equal_0:
                    self.do_func(self.verifies_tips_equal_possible_tents, self.verifies_tips_equal_0)
                    self.check_is_wrong()
                    if len(self.tents_put) == 0:
                        self.do_func(self.verifies_possible_tents_equal_1, self.verifies_tips_equal_0)
                        self.check_is_wrong()
                        while self.verified_possible_tents_equal_1:
                            self.do_func(self.verifies_possible_tents_equal_1, self.verifies_tips_equal_0)
                            self.check_is_wrong()
                            if self.is_wrong:
                                break
                    if self.is_wrong:
                        break
                # self.verifies_tips_equal_0()
                # self.verifies_tips_equal_possible_tents()
                # self.check_is_wrong()
                # while self.verified_tips_equal_0 or self.verified_tips_equal_possible_tents:
                #     self.verifies_tips_equal_0()
                #     self.verifies_tips_equal_possible_tents()
                #     self.check_is_wrong()
                #     if self.is_wrong:
                #         break
        else:
            pass
            # print('Finished heuristic')
            self.remove_trees(True)
            if len(self.trees_possibilities) > 0:
                print(self.tents_game)
                print(self.tents_game.field_copy)