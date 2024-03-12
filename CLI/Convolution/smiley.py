from PIL import Image as im
import os
from os.path import join, dirname
import random
# import numpy as np

def calc_conv(p1, mask, starting_idx, size, dev):
    val = 0
    s_col, s_row = starting_idx
    for col in range(size[0]):
        for row in range(size[1]):
            # print(f'i: {i}  j:{j}  si: {si}  sj: {sj}')
            # print(p1[i+si, j+sj])
            # print(mask[i,j])
            val += (p1[col+s_col, row+s_row] + random.gauss(0, dev)) * mask[row][col]
    return val


B,W = (-1, 1)
MASK = [
    [W, W, W, W, W, W, W],
    [W, B, B, B, B, B, W],
    [W, B, W, B, W, B, W],
    [W, B, B, W, B, B, W],
    [W, B, B, B, B, B, W],
    [W, B, W, W, W, B, W],
    [W, B, B, B, B, B, W],
    [W, W, W, W, W, W, W],
]
# mask size in (width, height)
MASK_SIZE = (7, 8) 

xx = im.open(join(os.path.dirname(__file__), 'findsmiley.jpg'))
xpix = xx.load()

for i in range(xx.size[0]):
    for j in range(xx.size[1]):
        if xpix[i, j] < 170:
            xpix[i, j] = -1
        else:
            xpix[i, j] = 1

for dev in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]:
    max_conv = -1000
    max_indices = None
    # print(xpix[0:5][0:5])
    for j in range(xx.size[0] - MASK_SIZE[0]):
        for i in range(xx.size[1] - MASK_SIZE[1]):
            conv = calc_conv(xpix, MASK, (i, j), MASK_SIZE, dev)
            if conv > max_conv:
                max_conv = conv
                max_indices = (i, j)

    print(f'dev: {dev} max_conv: {max_conv} col: {max_indices[0]} row: {max_indices[1]}')
