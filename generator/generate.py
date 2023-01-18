import type
import instance
import sys
import os
import numpy as np
from jinja2 import Template
from operator import methodcaller

if len(sys.argv) < 5:
    raise AttributeError(
        'empty|gliders|coords size_x size_y generation_count output_output_cycle 0|1(include first gen)')

size_x = int(sys.argv[2])
size_y = int(sys.argv[3])
generation_count = int(sys.argv[4])
output_cycle = int(sys.argv[5])
include_start = 0
if (len(sys.argv) > 6): include_start = int(sys.argv[6])

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
        grid[int(coord[0]) - 1][int(coord[1]) - 1] = 1

    return grid

match sys.argv[1]:
    case 'empty':
        data = np.zeros((size_x, size_y))
    case 'gliders':
        X = int((size_x - (size_x % 5)) / 5)
        Y = int((size_y - (size_y % 5)) / 5)
        data = np.tile(glider, (X, Y))
    case _:
        if not os.path.isfile(sys.argv[1]):
            raise FileNotFoundError('Starting state file not present in the specified location')
        else:
            data = create_binary_graph(sys.argv[1], size_x, size_y)

outputFile = 'gol.xml'
appname = 'gol'
cellCount = len(data) * len(data[0])

messageNeighbours = type.MessageType(id='messageNeighbours', cdata='application/messageNeighbours.c')
messageSupervisor = type.MessageType(id='messageSupervisor', cdata='application/messageSupervisor.c')
cell = type.DeviceType(id='cell', properties='application/cell/properties.c', state='application/cell/state.c', onInit='application/cell/onInit.c', onDeviceIdle='application/cell/onDeviceIdle.c', readyToSend='application/cell/readyToSend.c', outputPins=[type.OutputPin('sender', 'messageNeighbours', 'application/cell/onSendNeighbours.c')], supervisorOutPin=type.SupervisorOutPin('messageSupervisor', 'application/cell/onSendSupervisor.c'), inputPins=[type.InputPin('receiver', 'messageNeighbours', 'application/cell/onReceive.c')])
pinger = type.DeviceType(id='pinger', properties='application/pinger/properties.c', state='application/pinger/state.c', onInit='application/pinger/onInit.c', onDeviceIdle='application/pinger/onDeviceIdle.c', readyToSend='application/pinger/readyToSend.c', outputPins=[], supervisorOutPin=type.SupervisorOutPin(messageTypeId='messageSupervisor', onSend='application/pinger/onSendSupervisor.c'), inputPins=[])
supervisor = type.SupervisorType(id='id', code='application/supervisor/code.c', state='application/supervisor/state.c', onInit='application/supervisor/onInit.c', onStop='application/supervisor/onStop.c', supervisorInPins=[type.SupervisorInPin('', 'messageSupervisor', 'application/supervisor/onReceive.c')])
graphType = type.GraphType(id='gol_type', messageTypes=[messageNeighbours, messageSupervisor], properties='application/properties.c', deviceTypes=[cell, pinger], supervisorType=supervisor)

graphInstance = instance.GraphInstance(id='gol_instance', graphTypeId='gol_type', P='{%d,%d,%d,%d}' % (cellCount, generation_count, output_cycle, include_start))

renderedGraphType = type.render(graphType=graphType)
renderedGraphInstance = instance.render(graphInstance=graphInstance, data=data)

with open(outputFile, 'w') as f:
    f.write(
        type.fullRender(appname=appname, graphType=renderedGraphType, graphInstance=renderedGraphInstance)
    )