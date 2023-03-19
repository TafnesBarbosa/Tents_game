import numpy as np
from pdf2image import convert_from_path
from PIL import Image
import matplotlib.pyplot as plt

# Constants
PIXEL_X = 200 # Vertical
PIXEL_Y = 100 # Horizontal

def pdf2images(pdf):
    # Store Pdf with convert_from_path function
    images = convert_from_path(pdf)
    for image in images:
        image.save('page.png', 'PNG')

    image_original = np.asarray(Image.open('page.png'))
    i_init = []
    i_end = []
    changed_up = False
    changed_down = False
    row = image_original[PIXEL_X, PIXEL_Y-4:, 0]
    for i, pixel in enumerate(row):
        if i > 0 and pixel == 255 and row[i-1] == 0:
            changed_down = True
            changed_up = False
        elif i > 0 and pixel == 0 and row[i-1] == 255:
            changed_up = True
            changed_down = False
        if changed_up:
            i_init.append(i+PIXEL_Y-4)
            changed_up = False
        elif changed_down:
            i_end.append(i+PIXEL_Y-4)
            changed_down = False
    y_coordinates = []
    for i_i, i_e in zip(i_init[:-1], i_end[1:]):
        y_coordinates.append((i_i, i_e))

    i_init = []
    i_end = []
    changed_up = False
    changed_down = False
    column = image_original[PIXEL_X-4:, PIXEL_Y, 0]
    for j, pixel in enumerate(column):
        if j > 0 and pixel == 255 and column[j-1] == 0:
            changed_down = True
            changed_up = False
        elif j > 0 and pixel == 0 and column[j-1] == 255:
            changed_up = True
            changed_down = False
        if changed_up:
            i_init.append(j+PIXEL_X-4)
            changed_up = False
        elif changed_down:
            i_end.append(j+PIXEL_X-4)
            changed_down = False
    x_coordinates = []
    for i_i, i_e in zip(i_init[:-1], i_end[1:]):
        x_coordinates.append((i_i, i_e))

    images = []
    for i, (x, y) in enumerate(zip(x_coordinates, y_coordinates)):
        images.append(image_original[x[0]:x[1]+1, y[0]:y[1]+1, :])
        plt.imsave('game' + str(i) + '.png', images[-1])
    
    pass