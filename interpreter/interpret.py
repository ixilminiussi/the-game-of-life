from operator import methodcaller
import numpy as np
from PIL import Image
import sys
import os

g = []
G = {}

inputLocation = sys.argv[1]
outputLocation = sys.argv[2]
generation = sys.argv[3]
framerate = 10
if (len(sys.argv) > 4): framerate = int(sys.argv[4])

with open(inputLocation,'r') as f:
    lines = map(methodcaller('strip', '\n'), f.readlines())
    data = list(map(methodcaller('split', ','), lines))
    
    for i in range(len(data)): data[i] = list(map(int, data[i]))
        
    data.sort(key = lambda i: i[1])
    
    for i in data:
        if i[2] not in g: 
            g.append(i[2])
            G[i[2]] = []
            
        G[i[2]].append(i)

g.sort(reverse=True)
data = sorted(G[g[0]], key = lambda x: (-x[1], -x[0]))
X = data[0][0] +1
Y = data[0][1] +1 
g.sort()

def generate_grid(generation):
    data = sorted(G[generation], key = lambda x: (-x[1], -x[0]))
    grid = np.zeros((Y, X))
    
    for e in data:
        grid[e[1]][e[0]] = e[3]
    
    return grid.astype('uint8')*255
    
if (generation == '-v'):
    for i in g:
        imageObject = Image.fromarray(generate_grid(int(i)))
        imageObject.save(outputLocation + '/' + str(i) + '.png')
    os.system("ffmpeg  -hide_banner -loglevel error -framerate {0} -i '{1}' -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p video.mp4".format(framerate, outputLocation + '/%00d.png'))
else:
    imageObject = Image.fromarray(generate_grid(int(generation)))
    imageObject.save(outputLocation)