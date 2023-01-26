import type, instance, definitions
import sys, argparse, os, errno
import numpy as np

# read user arguments 

parser = argparse.ArgumentParser(add_help=True, description='This script generates a proper XML to run The Game of Life on POETS.')

parser.add_argument('-o', '--output', nargs=1, metavar='', help='(filename) Output file name for the generated XML.', required=False, default=['gol.xml'])
parser.add_argument('-x', '--xstate', nargs=1, metavar='', help='(string|filename) Starting state preset: [gliders|empty] | Starting file state', required=False, default=['gliders'])
parser.add_argument('-s', '--size', nargs=2, metavar='', help='(int) Size of the grid: X, Y', required=True)
parser.add_argument('-g', '--generation', nargs=1, metavar='', help='(int) Number of total generations', required=False, default=[100])
parser.add_argument('-c', '--cycle', nargs=1, metavar='', help='(int) Iteration cycles to be sent to the supervisor', required=False, default=[1])
parser.add_argument('-i', '--include', nargs=1, metavar='', help='(int) set to 1 to send the first iteration to the supervisor', required=False, default=[0])

args = parser.parse_args()

if args.xstate[0] not in ['gliders', 'empty'] and not os.path.isfile(args.xstate[0]):
    raise FileNotFoundError(
    errno.ENOENT, os.strerror(errno.ENOENT), args.xstate[0])

size_x = int(args.size[0])
size_y = int(args.size[1])
generation_count = int(args.generation[0])
output_cycle = int(args.cycle[0])
include_start = int(args.include[0])

glider = np.array([[0,0,0,0,0],
[0,0,1,0,0],
[0,0,0,1,0],
[0,1,1,1,0],
[0,0,0,0,0]])

def create_binary_graph(filename, grid_size_x, grid_size_y):
    coords = []
    # Read the coordinates from the file
    with open(filename, 'r') as file:
        for line in file:
            coords.append(line.strip().split(','))

    # Create an empty grid with the specified size
    grid = [[0 for x in range(grid_size_y)] for y in range(grid_size_x)]

    # Set the coordinates to 1
    for coord in coords:
        grid[int(coord[0])][int(coord[1])] = 1

    return grid

match args.xstate[0]:
    case 'empty':
        data = np.zeros((size_x, size_y))
    case 'gliders':
        X = int((size_x - (size_x % 5)) / 5)
        Y = int((size_y - (size_y % 5)) / 5)
        data = np.tile(glider, (X, Y))
    case _:
        data = create_binary_graph(args.xstate[0], size_x, size_y)

cellCount = len(data) * len(data[0])

renderedGraphType = type.render(graphType=definitions.graphType)
renderedGraphInstance = instance.render(graphInstance=definitions.graphInstance([cellCount, generation_count, output_cycle, include_start]), data=data)

with open(definitions.outputFile, 'w') as f:
    f.write(
        type.fullRender(appname=definitions.appname, graphType=renderedGraphType, graphInstance=renderedGraphInstance)
    )
