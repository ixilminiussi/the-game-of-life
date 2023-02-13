from operator import methodcaller
import numpy as np
from PIL import Image
import uuid
import sys, argparse, errno, os
import matplotlib.cm as cm
    
outputFull = False
outputVideo = False
outputGeneration = False

cmap = cm.get_cmap('viridis')

# read user arguments 

parser = argparse.ArgumentParser(add_help=True, description='This script interprets output files from the POETS implementation of The Game of Life.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-i', '--input', metavar='', help='(filename) input file used to make generations', required=False, default='gol_output')
parser.add_argument('-v', '--video', metavar='', help='(filename) output file name for a video render of all generations', required=False)
parser.add_argument('-f', '--full', metavar='', help='(dir) output dir name for a full image render of all generations', required=False, default='frames')
parser.add_argument('-g', '--generation', metavar='', help='(number) specific generation to be rendered as .png', required=False)
parser.add_argument('-s', '--speed', metavar='', help='(number) framerate of generated video', required=False, default=10)
parser.add_argument('-r', '--render', metavar='', help='(string) render type: [binary|performance]', required=False, default='binary')

for arg in sys.argv:
    if (arg in ['-v', '--video']):
        outputVideo = True
    elif (arg in ['-f', '--full']):
        outputFull = True
    elif (arg in ['-g', '--generation']):
        outputGeneration = True

if (not outputFull and not outputGeneration and not outputVideo):
    outputFull = True

args = parser.parse_args()

if not os.path.isfile(args.input):
    raise FileNotFoundError(
    errno.ENOENT, os.strerror(errno.ENOENT), args.input)

# code

g = []
G = {}

with open(args.input,'r') as f:
    lines = map(methodcaller('strip', '\n'), f.readlines())
    data = list(map(methodcaller('split', ','), lines))
    
    for i in range(len(data)): data[i] = list(map(int, data[i]))
        
    data.sort(key = lambda i: i[1])
    
    for i in data:
        if i[2] not in g: 
            g.append(i[2])
            G[i[2]] = []
            
        G[i[2]].append(i)

X = max(data, key=lambda x: x[0])[0] +1
Y = max(data, key=lambda x: x[1])[1] +1

range = max([max(i, key=lambda x: x[4])[4] - min(i, key=lambda x: x[4])[4] for i in G.values()])

def map_float_to_rgb(x):
    return list(cmap(x)[:3])

def generate_grid(generation):
    grid = np.zeros((Y, X, 3))

    minimum = min(G[generation], key = lambda x: x[4])[4]
    
    data = G[generation]
    
    match args.render:
        case 'performance':
            grid = np.zeros((Y, X, 3))
            for e in data:
                grid[e[1]][e[0]] = map_float_to_rgb((e[4] - minimum) / range)
        case _:
            grid = np.zeros((Y, X))
            for e in data:
                grid[e[1]][e[0]] = e[3]
    
    return (grid*255).astype('uint8')
    
locations = []

def generate_all(output):
    os.system("mkdir -p {0}".format(output))
    for i in g:
        imageObject = Image.fromarray(generate_grid(int(i)))
        locations.append(str(output) + '/' + str(i) + '.png')
        imageObject.save(str(output) + '/' + str(i) + '.png')
    return locations

if (outputFull):
    generate_all(args.full)

if (outputVideo):
    if (outputFull):
        os.system("ffmpeg  -hide_banner -loglevel error -framerate {0} -i '{1}/%00d.png' -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p {2}".format(args.speed, args.full, args.video))
    else:
        output = uuid.uuid1()
        locations = generate_all(output)
        os.system("ffmpeg  -hide_banner -loglevel error -framerate {0} -i '{1}/%00d.png' -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p {2}".format(args.speed, output, args.video))
        for image in locations:
            os.system("rm {0}".format(image))
        os.system('rmdir {0}'.format(output))

if (outputGeneration):
    grid = generate_grid(int(args.generation))
    imageObject = Image.fromarray(grid)
    imageObject.save('{0}.png'.format(args.generation))