from tents_game import *
from mypdf2images import *
from tents_solver import *

tents_game = TentsGame(16, seed=15, show_before_remove_tents=False)
# tents_game = TentsGame(6, generate=False, trees_x=[3, 3, 5, 0, 2, 5, 1], trees_y=[0, 1, 1, 2, 3, 4, 5], tips_x=[2, 1, 1, 1, 1, 1], tips_y=[1, 1, 2, 1, 1, 1])
# tents_game = TentsGame(8, generate=False, trees_x=[0, 3, 4, 7, 0, 3, 6, 0, 3, 4, 3, 7], trees_y=[1, 1, 1, 2, 3, 3, 4, 5, 5, 5, 7, 7], tips_x=[2, 1, 2, 1, 2, 1, 1, 2], tips_y=[2, 2, 0, 3, 0, 1, 3, 1])
# tents_game.show()
tic = time.time()
tents_game_solution = TentsGameSolver(tents_game, StartState())
while not tents_game_solution.acabou_pela_regra:
    print(tents_game)
    # print(tents_game_solution.state)
    tents_game_solution.update()
    time.sleep(0.5)
toc = time.time()
print(toc-tic)
tents_game.show()
# pdf2images('6x6tents.pdf')