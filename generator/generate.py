import instance
import argparse, os, errno
import numpy as np
import xml.etree.ElementTree as ET
from jinja2 import Template

# read user arguments 

parser = argparse.ArgumentParser(add_help=True, description='This script generates a proper XML to run The Game of Life on POETS.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-a', '--application', metavar='', help='(filename) graphtype being used', required=False, default='../application.xml')
parser.add_argument('-o', '--output', metavar='', help='(filename) output file name for the generated XML', required=False, default='gol.xml')
parser.add_argument('-x', '--xstate', metavar='', help='(string|filename) starting state preset: [gliders|empty] | Starting file state', required=False, default='gliders')
parser.add_argument('-s', '--size', nargs=2, metavar='', help='(int) size of the grid: X, Y', required=True)
parser.add_argument('-g', '--generation', metavar='', help='(int) number of total generations', required=False, default=100)
parser.add_argument('-c', '--cycle', metavar='', help='(int) cycles of iterations to be sent to the supervisor', required=False, default=1)
parser.add_argument('-i', '--include', help='send the first iteration to the supervisor', required=False, action='store_true')

args = parser.parse_args()

if args.xstate not in ['gliders', 'empty'] and not os.path.isfile(args.xstate):
    raise FileNotFoundError(
    errno.ENOENT, os.strerror(errno.ENOENT), args.xstate)

size_x = int(args.size[0])
size_y = int(args.size[1])
generation_count = int(args.generation)
output_cycle = int(args.cycle)
include_start = int(args.include)
output_file = args.output

glider = np.array([[0,0,0,0,0],
[0,0,1,0,0],
[0,0,0,1,0],
[0,1,1,1,0],
[0,0,0,0,0]])

graphType = ''

with open(args.application, 'r') as file:
    graphType = file.read()


appname = 'gol'

graphTypeId = ET.fromstring(graphType).attrib.get('id')

ET.register_namespace('', 'https://poets-project.org/schemas/virtual-graph-schema-v4')

def graphInstance(P):
    param = ','.join(str(p) for p in P)
    return instance.GraphInstance(id='gol_instance', graphTypeId=graphTypeId, P='{%s}' % param)

def fullRender(appname, graphType, graphInstance):
    template = Template('''<?xml version="1.0" encoding="UTF-8"?>
<Graphs xmlns="https://poets-project.org/schemas/virtual-graph-schema-v4" appname="{{ appname }}">
    {{ graphType }}
    {{ graphInstance }}
</Graphs>
    ''')
    return template.render(appname=appname, graphType=graphType, graphInstance=graphInstance)

def createBinaryGraph(filename, grid_size_x, grid_size_y):
    coords = []
    # Read the coordinates from the file
    with open(filename, 'r') as file:
        for line in file:
            coords.append(line.strip().split(','))

    # Create an empty grid with the specified size
    grid = [[0 for x in range(grid_size_x)] for y in range(grid_size_y)]

    # Set the coordinates to 1
    for coord in coords:
        grid[int(coord[1])][int(coord[0])] = 1

    return grid

match args.xstate:
    case 'empty':
        data = np.zeros((size_x, size_y))
    case 'gliders':
        X = int((size_x - (size_x % 5)) / 5)
        Y = int((size_y - (size_y % 5)) / 5)
        data = np.tile(glider, (X, Y))
    case _:
        data = createBinaryGraph(args.xstate, size_x, size_y)

cellCount = len(data) * len(data[0])

renderedGraphInstance = instance.render(graphInstance=graphInstance([cellCount, generation_count, output_cycle, include_start]), data=data)

with open(output_file, 'w') as f:
    f.write(fullRender(appname=appname, graphType=graphType, graphInstance=renderedGraphInstance))