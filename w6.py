from getconnect import Connection


aio = Connection.getconnect()

def getPumpState():
    data = aio.data('pump')
    print(data)
    if raiseErr(data) == None :
        return None
    return data[0]

def getLightState():
    data = aio.data('light')
    if raiseErr(data) == None :
        return None
    return data[0]

def raiseErr(data):
    if data == [] :
        print('Chưa có dữ liệu')
        exit()
    return 1

def getDeviceState():
    print('Now:\n\tPump: \t' + getPumpState().value + '\n\tLight: \t' + getLightState().value)
    pass

getDeviceState()

def getBrightness():
    data = aio.data('brightness')
    if raiseErr(data) == None :
        return None
    return data[0]


def getHumidity():
    data = aio.data('humidity')
    if raiseErr(data) == None :
        return None
    return data[0]


def getTemperature():
    data = aio.data('temperature')
    if raiseErr(data) == None :
        return None
    return data[0]


def getEnvirState():
    print('Now:\n\tBrightness: \t' + getBrightness().value + '\n\tHumidity: \t' + getHumidity().value + '\n\tTemperature: \t' + getTemperature().value)
    return None