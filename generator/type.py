from jinja2 import Template

#====================================================================
#=============================GRAPH TYPE=============================
#====================================================================

def file_to_cdata(file):
    with open('../' + file, 'r') as f:
        lines = list(f.readlines())
        code = ''

        state = 0

        for i in reversed(lines):
            if '//@@//' in i:
                state = state + 1
            elif state == 1:
                code = i + code
            if state == 2:
                break

        return '\n'.join(code.split('\n')[:-1])

class OutputPin:
    def __init__(self, name, messageTypeId, onSend):
        self.name = name
        self.messageTypeId = messageTypeId
        self.OnSend = file_to_cdata(onSend) #file path

class SupervisorOutPin:
    def __init__(self, messageTypeId, onSend):
        self.messageTypeId = messageTypeId
        self.OnSend = file_to_cdata(onSend) #file path

class InputPin:
    def __init__(self, name, messageTypeId, onReceive):
        self.name = name
        self.messageTypeId = messageTypeId
        self.OnReceive = file_to_cdata(onReceive) #file path

class SupervisorInPin:
    def __init__(self, id, messageTypeId, onReceive):
        self.id = id
        self.messageTypeId = messageTypeId
        self.OnReceive = file_to_cdata(onReceive)

class MessageType:
    def __init__(self, id, cdata):
        self.id = id
        self.CDATA = file_to_cdata(cdata) #file path

class DeviceType:
    def __init__(self, id, sharedCode, properties, state, onInit, onDeviceIdle, readyToSend, outputPins, supervisorOutPin, inputPins):
        self.id = id
        self.Properties = file_to_cdata(properties) #file path
        self.SharedCode = file_to_cdata(sharedCode) #file path
        self.State = file_to_cdata(state) #file path
        self.OnInit = file_to_cdata(onInit) #file path
        self.OnDeviceIdle = file_to_cdata(onDeviceIdle) #file path
        self.ReadyToSend = file_to_cdata(readyToSend) #file path
        self.OutputPins = outputPins #Array of OutputPin
        self.SupervisorOutPin = supervisorOutPin 
        self.InputPins = inputPins #Array of InputPin

class SupervisorType:
    def __init__(self, id, code, state, onInit, onStop, supervisorInPins):
        self.id = id
        self.Code = file_to_cdata(code) #file path
        self.State = file_to_cdata(state) #file path
        self.OnInit = file_to_cdata(onInit) #file path
        self.OnStop = file_to_cdata(onStop) #file path
        self.SupervisorInPins = supervisorInPins #Array of SupervisorInPin

class GraphType:
  def __init__(self, id, sharedCode, messageTypes, properties, deviceTypes, supervisorType):
    self.id = id
    self.SharedCode = file_to_cdata(sharedCode) #file path
    self.MessageTypes = messageTypes #Array of MessageType
    self.Properties = file_to_cdata(properties) #file path
    self.DeviceTypes = deviceTypes #Array of MessageType
    self.SupervisorType = supervisorType

template = Template('''
    <GraphType id="{{ graphType.id }}">
        <Properties>
            <![CDATA[ 
            {{ graphType.Properties }}
            ]]>
        </Properties>
        <SharedCode>
            <![CDATA[
            {{ graphType.SharedCode}}
            ]]>
        </SharedCode>
        <MessageTypes>{% for messageType in graphType.MessageTypes %}
            <MessageType id="{{ messageType.id }}">
                <Message>
                    <![CDATA[ 
                        {{ messageType.CDATA }}
                    ]]>
                </Message>
            </MessageType>{% endfor %}
        </MessageTypes>
        <DeviceTypes>{% for device in graphType.DeviceTypes %}
            <DeviceType id="{{ device.id }}">
                <Properties>
                    <![CDATA[
                        {{ device.Properties }}
                    ]]>
                </Properties>
                <SharedCode>
                    <![CDATA[
                    {{ device.SharedCode}}
                    ]]>
                </SharedCode>
                <State>
                    <![CDATA[ 
                        {{ device.State }}
                    ]]>
                </State>
                <OnInit>
                    <![CDATA[ 
                        {{ device.OnInit }}
                    ]]>
                </OnInit>
                <OnDeviceIdle>
                    <![CDATA[
                        {{ device.OnDeviceIdle }}
                    ]]>
                </OnDeviceIdle>
                <ReadyToSend>
                    <![CDATA[
                        {{ device.ReadyToSend }}
                    ]]>
                </ReadyToSend>{% for outputPin in device.OutputPins %}
                <OutputPin name="{{ outputPin.name }}" messageTypeId="{{ outputPin.messageTypeId }}">
                    <OnSend>
                        <![CDATA[
                            {{ outputPin.OnSend }}
                        ]]>
                    </OnSend>
                </OutputPin>{% endfor %}
                <SupervisorOutPin messageTypeId="{{ device.SupervisorOutPin.messageTypeId }}">
                    <OnSend>
                        <![CDATA[ 
                            {{ device.SupervisorOutPin.OnSend }}
                        ]]>
                    </OnSend>
                </SupervisorOutPin>{% for inputPin in device.InputPins %}
                <InputPin name="{{ inputPin.name }}" messageTypeId="{{ inputPin.messageTypeId }}">
                    <OnReceive>
                        <![CDATA[
                            {{ inputPin.OnReceive }}
                        ]]>
                    </OnReceive>
                </InputPin>{% endfor %}
            </DeviceType>{% endfor %}
            <SupervisorType id="{{ graphType.SupervisorType.id }}">
                <Code>
                    <![CDATA[ 
                        {{ graphType.SupervisorType.Code }}
                    ]]>
                </Code>
                <State>
                    <![CDATA[
                        {{ graphType.SupervisorType.State }}
                    ]]>
                </State>
                <OnInit>
                    <![CDATA[
                        {{ graphType.SupervisorType.OnInit }}
                    ]]>
                </OnInit>
                <OnStop>
                    <![CDATA[
                        {{ graphType.SupervisorType.OnStop }}
                    ]]>
                </OnStop>{% for supervisorInPin in graphType.SupervisorType.SupervisorInPins %}
                <SupervisorInPin id="{{ supervisorInPin.id }}" messageTypeId="{{ supervisorInPin.messageTypeId }}">
                    <OnReceive>
                        <![CDATA[
                            {{ supervisorInPin.OnReceive }}
                        ]]>
                    </OnReceive>
                </SupervisorInPin>{% endfor %}
            </SupervisorType>
        </DeviceTypes>
    </GraphType>
''')

def render(graphType):
    return template.render(graphType=graphType)

def fullRender(appname, graphType, graphInstance):
    template = Template('''
<?xml version="1.0" encoding="UTF-8"?>

<Graphs xmlns="" appname="{{ appname }}">
    {{ graphType }}
    {{ graphInstance }}
</Graphs>
    ''')

    return template.render(appname=appname, graphType=graphType, graphInstance=graphInstance)