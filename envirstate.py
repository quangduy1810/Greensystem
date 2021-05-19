from pkg_resources import Environment
from getconnect import Connection
import time


aio = Connection.getconnectClient()


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


def raiseErr(data):
    if data == [] :
        print('Chưa có dữ liệu')
        return None
    return 1

def getTempHumid(data):
    data = {
        "id":"7",
        "name":['TEMP' , 'HUMID'],
        "data":[getTemperature().value, getHumidity.value()],
        "unit":['*C','%']
    }
    return data

def getBright(data):
    data = {
        "id":"1",
        "name":"LED",
        "data":getBrightness().value,
        "unit":""
    }
    return data

