def checkValue(value):
    if type(value).__name__ != 'int':
        print('không phải kiểu số')
        return 0
    return 1

def sendBrightness(value):
    print('1')
    if checkValue(value) == 0:
        exit()
    aio.publish('brightness',value)


def sendHumidity(value):
    
    if type(value).__name__ != 'int':
        print('không phải kiểu số')
        exit()
    aio.publish('humidity',value)


def sendTemperature(value):

    if type(value).__name__ != 'int':
        print('không phải kiểu số')
        exit()
    aio.publish('temperature',value)

    
    
def message(aio, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
