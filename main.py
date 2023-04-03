from tents_game import *
from mypdf2images import *
from tents_solver import *
import matplotlib.pyplot as plt

tents_game = TentsGame(18, seed=26, show_before_remove_tents=False)
history = []
# for i in range(100):
    # tents_game = TentsGame(6, generate=False, trees_x=[1, 4, 0, 3, 4, 2, 1], trees_y=[0, 1, 2, 2, 2, 4, 5], tips_x=[2, 1, 1, 1, 1, 1], tips_y=[1, 2, 1, 1, 0, 2])
    # tents_game = TentsGame(8, generate=False, trees_x=[3, 1, 7, 4, 5, 7, 3, 7, 1, 6, 1, 4], trees_y=[0, 1, 1, 2, 3, 3, 5, 5, 6, 6, 7, 7], tips_x=[1, 1, 1, 2, 2, 1, 0, 4], tips_y=[2, 1, 3, 0, 2, 1, 2, 1])
    # tents_game = TentsGame(10, generate=False, trees_x=[2, 4, 9, 0, 6, 8, 2, 6, 8, 8, 2, 7, 3, 2, 7, 8, 2, 9, 1, 7], trees_y=[0,0,1,2,2,2,3,3,3,4,5,5,6,7,7,7,8,8,9,9], tips_x=[2,3,1,2,1,1,4,1,2,3], tips_y=[1,4,1,3,1,3,1,2,2,2])
    # tents_game = TentsGame(15, generate=False, trees_x=[0, 7, 10, 12, 6, 2, 3, 8, 10, 2, 7, 12, 1, 12, 0, 8, 10, 6, 7, 8, 11, 14, 2, 14, 12, 0, 7, 9, 4, 9, 0, 1, 3, 7, 11, 12, 14, 1, 7, 8, 13, 1, 5, 10, 11], trees_y=[0, 0, 0, 0, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 8, 9, 9, 9, 10, 10, 11, 11, 11, 11, 11, 11, 12, 13, 13, 13, 13, 14, 14, 14, 14], tips_x=[4, 3, 3, 2, 3, 2, 3, 2, 4, 2, 4, 3, 4, 2, 4], tips_y=[4, 2, 3, 3, 3, 2, 4, 2, 1, 5, 1, 5, 3, 3, 4])
tic = time.time()
# tents_game_solution = TentsGameSolver(tents_game)
toc = time.time()
history.append(toc-tic)
print(np.mean(np.array(history)))
tents_game.show()
# with open('data_game_inside.npy', 'wb') as f:
#     np.save(f, 0)
#     np.save(f, [])
# means = []
# stds = []
# ns = []
# n = 4
# with open('data_game.npy', 'wb') as f:
#     np.save(f, means)
#     np.save(f, stds)
#     np.save(f, ns)
# while True:
#     with open('data_game.npy', 'rb') as f:
#         means = np.load(f).tolist()
#         stds = np.load(f).tolist()
#         ns = np.load(f).tolist()
#     if len(ns) == 0:
#         n = 4
#     else:
#         n = ns[-1] + 1
#     ns.append(n)
#     with open('data_game_inside.npy', 'wb') as f:
#             np.save(f, 0)
#             np.save(f, [])
#     with open('data_game_inside.npy', 'rb') as f:
#         i = int(np.load(f))
#         history = np.load(f).tolist()
#     while i < 1000:
#         with open('data_game_inside.npy', 'rb') as f:
#             i = int(np.load(f))
#             history = np.load(f).tolist()
#         tents_game = TentsGame(n)
#         tic = time.time()
#         tents_game_solution = TentsGameSolver(tents_game)
#         toc = time.time()
#         history.append(toc-tic)
#         print(n, i)
#         with open('data_game_inside.npy', 'wb') as f:
#             np.save(f, i+1)
#             np.save(f, history)
        
#     means.append(np.mean(np.array(history)))
#     stds.append(np.std(np.array(history)))
#     with open('data_game.npy', 'wb') as f:
#         np.save(f, means)
#         np.save(f, stds)
#         np.save(f, ns)
    # n += 1

# means_to_fit = np.array(means)
# ns_to_fit = np.array(ns)

# means_to_fit = np.log(means_to_fit)

# A = np.array([ns_to_fit**2, ns_to_fit, np.ones(len(ns))]).transpose()
# coef = np.linalg.inv(A.transpose() @ A) @ A.transpose() @ means_to_fit.transpose()

# y_fit = coef[0] * ns_to_fit**2 + coef[1] * ns_to_fit + coef[2]
# print(np.e ** coef)

# plt.figure()
# plt.plot(ns, means_to_fit)
# plt.grid(True)
# plt.plot(ns, y_fit, 'r')
# plt.show()

# plt.figure()
# plt.plot(ns, stds)
# plt.grid(True)
# plt.show()
# tents_game.show()