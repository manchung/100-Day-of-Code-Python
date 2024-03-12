from PIL import Image as im
import os
from os.path import join, dirname
import random
# import numpy as np

xx = im.open(join(os.path.dirname(__file__), 'zebra.jpg'))
yy = im.new('L', [3*xx.size[0], 3*xx.size[1]], 0)
zz = im.new('L', [3*xx.size[0], 3*xx.size[1]], 0)

xpix = xx.load()
ypix = yy.load()
zpix = zz.load()

for i in range(xx.size[0]):
    for j in range(xx.size[1]):
        ypix[3*i, 3*j] = xpix[i, j]

# for j in range(zz.size[1]):
#     for i in range(zz.size[0]):
#         conv = [(i-2, 1/3), (i-1, 2/3), (i, 1), (i+1, 2/3), (i+2, 1/3)]
#         for pos, ratio in conv:
#             if pos >= 0 and pos < yy.size[0]:
#                 zpix[i,j] += int(ratio * ypix[pos, j])

# for i in range(zz.size[0]):
#     for j in range(zz.size[1]):
#         conv = [(j-2, 1/3), (j-1, 2/3), (j, 1), (j+1, 2/3), (j+2, 1/3)]
#         for pos, ratio in conv:
#             if pos >= 0 and pos < yy.size[1]:
#                 zpix[i,j] += int(ratio * ypix[i, pos])


for i in range(zz.size[0]):
    for j in range(zz.size[1]):
        filters = []
        for m in [-2, -1, 0, 1, 2]:
            fm = 1 - abs(m)/3
            for n in [-2, -1, 0, 1, 2]:
                fn = 1 - abs(n)/3
                filters.append((i+m, j+n, fm*fn))
        for p, q, factor in filters:
            if p in range(yy.size[0]) and q in range(yy.size[1]):
                zpix[i,j] += int(factor * ypix[p,q])

zz.save(join(os.path.dirname(__file__), 'zebraConv.jpg'))


