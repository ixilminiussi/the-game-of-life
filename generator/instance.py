from jinja2 import Template

def graphToXML(data):
    Y = len(data)
    X = len(data[0])

    deviceInstances = '<DevI id="%d" type="pinger" P="" />\n' % (X*Y+1)
    #deviceInstances = ''
    edgeInstances = ''

    def right(id):
        if (id + 1) % X == 0:
            return id - X + 1
        return id + 1

    def left(id):
        if id % X == 0:
            return id + X - 1
        return id - 1

    def top(id):
        if id < X:
            return id + X * (Y - 1)
        return id - X

    def bottom(id):
        if id >= X * (Y - 1):
            return id % X
        return id + X

    def top_right(id):
        return top(right(id))

    def top_left(id):
        return top(left(id))

    def bottom_right(id):
        return bottom(right(id))

    def bottom_left(id):
        return bottom(left(id))

    id = 0

    for y in range(Y):
        for x in range(X):
            deviceInstances += '<DevI id="%d" type="cell" P="{%d,%d,%d}" />' % (
                id, int(data[y][x]), x, y)

            edgeInstances += '<EdgeI path="%d:receiver-%d:sender" />' % (
                id, top_left(id))
            edgeInstances += '<EdgeI path="%d:receiver-%d:sender" />' % (
                id, top(id))
            edgeInstances += '<EdgeI path="%d:receiver-%d:sender" />' % (
                id, top_right(id))
            edgeInstances += '<EdgeI path="%d:receiver-%d:sender" />' % (
                id, right(id))
            edgeInstances += '<EdgeI path="%d:receiver-%d:sender" />' % (
                id, bottom_right(id))
            edgeInstances += '<EdgeI path="%d:receiver-%d:sender" />' % (
                id, bottom(id))
            edgeInstances += '<EdgeI path="%d:receiver-%d:sender" />' % (
                id, bottom_left(id))
            edgeInstances += '<EdgeI path="%d:receiver-%d:sender" />' % (
                id, left(id))

            id += 1

    return deviceInstances, edgeInstances


template = Template('''
<GraphInstance id="{{ graphInstance.id }}" graphTypeId="{{ graphInstance.graphTypeId }}" P="{{ graphInstance.P }}">
    <DeviceInstances>
        {{ deviceInstances }}
    </DeviceInstances>
    <EdgeInstances>
        {{ edgeInstances }}
    </EdgeInstances>
</GraphInstance>
''')


class GraphInstance:
    def __init__(self, id, graphTypeId, P):
        self.id = id
        self.graphTypeId = graphTypeId
        self.P = P


def render(graphInstance, data):
    deviceInstances, edgeInstances = graphToXML(data)
    return template.render(graphInstance=graphInstance, deviceInstances=deviceInstances, edgeInstances=edgeInstances)
