from tents_game import *
from mypdf2images import *
from tents_solver import *

# a = TentsGame(6, [1, 4, 3, 4, 0, 0, 1], [0, 0, 2, 2, 3, 4, 5], [2, 1, 1, 1, 1, 1], [2, 1, 0, 2, 0, 2])
tents_game = TentsGame(6, show_before_remove_tents=False)
# tents_game.show()
tents_game_solution = TentsGameSolver(tents_game, StartState())
while not tents_game_solution.acabou_pela_regra:
    tents_game_solution.update()
# print(a)
tents_game.show()
# pdf2images('6x6tents.pdf')