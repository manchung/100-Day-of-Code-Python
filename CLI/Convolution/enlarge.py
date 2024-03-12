from PIL import Image as im
import os
from os.path import join, dirname

xx = im.open(join(os.path.dirname(__file__), 'zebra.jpg'))
yy = im.new('L', [3*xx.size[0], 3*xx.size[1]], 0)

xpix = xx.load()
ypix = yy.load()

for j in range(yy.size[1]):
    for i in range(yy.size[0]):
        ypix[i,j] = xpix[int(i/3), int(j/3)]

yy.save(join(os.path.dirname(__file__), 'zebraZOH.jpg'))

