import numpy as np
import math
import random
import os
from pdf2image import convert_from_path
from PIL import Image
import matplotlib.pyplot as plt
import time
from constants import *
from utils import *

class TentsGame(object):
    """
    Creates a tents game, where size is the size of rectangular field.

    trees_x and trees_y are the coordinates of the trees, starting at zero of the top left.

    tips_x and tips_y are the number of tents in each column and row respectively
    """

    # def __init__(self, size, trees_x, trees_y, tips_x, tips_y):
    #     self.size = size
    #     self.field = np.ones((size, size), dtype = int) * EMPTY
    #     for x, y in zip(trees_x, trees_y):
    #         self.field[y, x] = TREE

    #     self.tips_x = tips_x
    #     self.tips_y = tips_y

    def __init__(self, size=6, seed=None, show_before_remove_tents = False):
        # tic0 = time.time()
        if seed != None:
            random.seed(seed)
        # toc0 = time.time()

        self.size = size
        self.number_of_trees = int(math.floor(size * size / 5))
        self.field = np.ones((size, size)) * EMPTY
        # tic1 = time.time()
        done = False
        while not done:
            try:
                self._construct_put_tents()
                done = True
            except:
                done = False
        # toc1 = time.time()
        # tic2 = time.time()
        (self.tips_x, self.tips_y) = self._get_tents_positions()
        self.tips_x_copy, self.tips_y_copy = self.tips_x.copy(), self.tips_y.copy()
        # toc2 = time.time()
        # tic3 = time.time()
        done = False
        while not done:
            try:
                self._construct_put_trees()
                done = True
            except:
                done = False
        # toc3 = time.time()
        # tic4 = time.time()
        if not show_before_remove_tents:
            self._construct_remove_tents()
        # toc4 = time.time()

        # print(toc0-tic0)
        # print(toc1-tic1)
        # print(toc2-tic2)
        # print(toc3-tic3)
        # print(toc4-tic4)

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
                elif self.field[i, j] == POSSIBLE_TENT:
                    field_repr += ' ' + '\U000025A0'
            field_repr += '\n'
        return field_repr
    
    def _construct_put_tents(self):
        positions = []
        for i in range(self.size):
            for j in range(self.size):
                positions.append((i, j))

        tents = []
        for k in range(self.number_of_trees):
            tents.append(random.sample(positions, 1)[0])
            positions.remove(tents[-1])
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if tents[-1][0] + i >= 0 and tents[-1][0] + i < self.size:
                        if tents[-1][1] + j >= 0 and tents[-1][1] + j < self.size:
                            if i != 0 or j != 0:
                                try:
                                    positions.remove((tents[-1][0]+i, tents[-1][1]+j))
                                except:
                                    pass

        for tent in tents:
            self.field[tent[0], tent[1]] = TENT
        self.tents = tents

    def _get_tents_positions(self):
        tips_y = np.sum(self.field, axis=1) / TENT
        tips_x = np.sum(self.field, axis=0) / TENT

        return tips_x.astype(int).tolist(), tips_y.astype(int).tolist()

    def _construct_put_trees(self):
        possible_positions_to = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self.trees = []
        for tent in self.tents:
            position_to = random.sample(possible_positions_to, 4)
            for i in range(4):
                if tent[0]+position_to[i][0] >= 0 and tent[0]+position_to[i][0] < self.size and tent[1]+position_to[i][1] >= 0 and tent[1]+position_to[i][1] < self.size:
                    if self.field[tent[0]+position_to[i][0], tent[1]+position_to[i][1]] != TREE:
                        self.field[tent[0]+position_to[i][0], tent[1]+position_to[i][1]] = TREE
                        self.trees.append((tent[0]+position_to[i][0], tent[1]+position_to[i][1]))
                        break
                    else:
                        continue
    
    def _construct_remove_tents(self):
        for tent in self.tents:
            self.field[tent[0], tent[1]] = EMPTY
        self.tents = []

    def is_valid_coordinate(self, x, y):
        if x >= 0 and y >= 0 and x < self.size and y < self.size:
            return True
        else:
            return False

    def show(self):
        fileTEX = open('pic.tex', 'w', encoding='UTF-8')
        fileTEX.write('\\documentclass{article}\n')
        fileTEX.write('\\usepackage{fontspec}\n')
        fileTEX.write('\\newfontfamily{\\NotoEmoji}{NotoColorEmoji.ttf}[Renderer=Harfbuzz]\n')
        # fileTEX.write('\\newfontfamily{\\SymbolaEmoji}{Symbola}\n')
        fileTEX.write('\\usepackage{tikz}\n')
        fileTEX.write('\\usetikzlibrary{positioning,calc,3d,}\n')
        fileTEX.write('\\usepackage{pgfplots}\n')
        fileTEX.write('\\begin{document}\n')
        fileTEX.write('\t\\resizebox{\\textwidth}{!}{\n')
        fileTEX.write('\t\t\\begin{tikzpicture}\n')
        # for i in range(self.size+1):
        #     fileTEX.write(f'\t\t\t\\draw[thick] (0,{i})--++({self.size},0);\n')
        #     fileTEX.write(f'\t\t\t\\draw[thick] ({i},0)--++(0,{self.size});\n')
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i, j] == EMPTY:
                    fileTEX.write(f'\t\t\t\\node[draw=black,thick,fill=brown!50, anchor=north west, minimum size = 1cm] (a{i}{j}) at ({j},{self.size-i})'+' {};\n')
                elif self.field[i, j] == TREE:
                    fileTEX.write(f"\t\t\t\\node[draw=black,thick,fill=green!50, anchor=north west, minimum size = 1cm] (a{i}{j}) at ({j},{self.size-i})"+' {\\NotoEmoji\\symbol{"1F333}};\n')
                elif self.field[i, j] == TENT:
                    fileTEX.write(f'\t\t\t\\node[draw=black,thick,fill=green!50, anchor=north west, minimum size = 1cm] (a{i}{j}) at ({j},{self.size-i})'+' {\\NotoEmoji\\symbol{"26FA}};\n')
                elif self.field[i, j] == POSSIBLE_TENT:
                    fileTEX.write(f'\t\t\t\\node[draw=black,thick,fill=black!50, anchor=north west, minimum size = 1cm] (a{i}{j}) at ({j},{self.size-i})'+' {};\n')
        for i, x in enumerate(self.tips_x):
            fileTEX.write(f'\t\t\t\\node (x{i}) at ({i+0.5},{self.size+0.5})'+' {\\textbf{'+f'{x}'+'}};\n')
        for j, y in enumerate(self.tips_y):
            fileTEX.write(f'\t\t\t\\node (y{j}) at ({-0.5},{self.size-j-0.5})'+' {\\textbf{'+f'{y}'+'}};\n')
        
        fileTEX.write('\t\t\\end{tikzpicture}\n')
        fileTEX.write('\t}\n')
        fileTEX.write('\\end{document}')

        fileTEX.close()

        os.system('lualatex.exe -synctex=1 -interaction=nonstopmode "pic".tex > NUL 2>&1')

        images = convert_from_path('pic.pdf')
        for image in images:
            image.save('pic.png', 'PNG')

        image_original = np.asarray(Image.open('pic.png'))
        plt.imshow(image_original[300:1300, 350:1450, :])
        plt.grid(False)
        plt.axis('off')
        plt.show()
        os.system('del pic.*')