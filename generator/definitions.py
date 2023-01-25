import instance
import type

outputFile = 'gol.xml'
appname = 'gol'

cell = type.DeviceType(
    id='cell',
    properties='application/cell/properties.c',
    sharedCode='application/cell/sharedCode.c',
    state='application/cell/state.c',
    onInit='application/cell/onInit.c',
    onDeviceIdle='application/cell/onDeviceIdle.c',
    readyToSend='application/cell/readyToSend.c',
    outputPins=[type.OutputPin(
        name='sender',
        messageTypeId='messageNeighbours',
        onSend='application/cell/onSendNeighbours.c')],
    supervisorOutPin=type.SupervisorOutPin(
        messageTypeId='messageSupervisor',
        onSend='application/cell/onSendSupervisor.c'),
    inputPins=[type.InputPin(
        name='receiver',
        messageTypeId='messageNeighbours',
        onReceive='application/cell/onReceive.c')])

pinger = type.DeviceType(
    id='pinger', 
    properties='application/pinger/properties.c', 
    sharedCode='application/pinger/sharedCode.c',
    state='application/pinger/state.c', 
    onInit='application/pinger/onInit.c', 
    onDeviceIdle='application/pinger/onDeviceIdle.c', 
    readyToSend='application/pinger/readyToSend.c', 
    outputPins=[], 
    supervisorOutPin=type.SupervisorOutPin(
        messageTypeId='messageSupervisor', 
        onSend='application/pinger/onSendSupervisor.c'), 
    inputPins=[])

supervisor = type.SupervisorType(
    id='id',
    code='application/supervisor/code.c',
    state='application/supervisor/state.c',
    onInit='application/supervisor/onInit.c',
    onStop='application/supervisor/onStop.c',
    supervisorInPins=[type.SupervisorInPin(
        id='',
        messageTypeId='messageSupervisor',
        onReceive='application/supervisor/onReceive.c')])

graphType = type.GraphType(
    id='gol_type',
    sharedCode='application/sharedCode.c',
    messageTypes=[
        type.MessageType(
            id='messageNeighbours',
            cdata='application/messageNeighbours.c'),
        type.MessageType(
            id='messageSupervisor',
            cdata='application/messageSupervisor.c')],
    properties='application/properties.c',
    deviceTypes=[cell, pinger],
    supervisorType=supervisor)


def graphInstance(P):
    param = ','.join(str(p) for p in P)
    return instance.GraphInstance(id='gol_instance', graphTypeId='gol_type', P='{%s}' % param)
