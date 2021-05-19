from re import T
from mysql.connector.catch23 import STRING_TYPES
from pkg_resources import Environment
from getconnect import Connection
from devicestate import *
import time


aio = Connection.getconnectMQTTClient()

def checkValue(value):
    if type(value).__name__ != 'int':
        return error(0)
    return 1

def sendBrightness(value):
    if checkValue(value) != 1:
        return checkValue(value)
    aio.publish('brightness',value)


def sendHumidity(value):
    if checkValue(value) != 1:
        return checkValue(value)
    aio.publish('humidity',value)


def sendTemperature(value):
    if checkValue(value) != 1:
        return checkValue(value)
    aio.publish('temperature',value)


def sendPump(value):
    aio.publish('pump',value)

def sendLight(value):
    aio.publish('light', value)

def send():
    return 1

def error(num):
    if num == 0:
        error = 'Wrong type input'
    elif num == 1:
        error = 'Timeout, check your connection'
    return error

def sendOnceTempHumid(temp,humid):
    sendTemperature(temp)
    sendHumidity(humid)

    data = {
    "id":"7",
    "name":['TEMP' , 'HUMID'],
    "data":[str(temp), str(humid)],
    "unit":['*C','%']
    }
    
    return data

def sendOnceBright(bright):
    if bright > 2 or bright < 0:
        error(0)
    
    sendBrightness(bright)
    data = {
        "id":"1",
        "name":"LED",
        "data":str(bright),
        "unit":""
    }
    return data


def sendInfomation(*param):
    timeout = 30
    if len(param) == 1:
        pre = getBrightness().created_at
        while(timeout > 0):
            sendOnceBright(param[0])
            if getBrightness().created_at == pre:
                print(getBrightness().created_at)
                sendOnceBright(param[0])
            else: 
                break
            timeout = timeout - 1
            if timeout == 0:
                return  error(1)
            time.sleep(30)
    else:
        pre1 = getTemperature().created_at
        pre2 = getHumidity().created_at
        while(timeout > 0):
            sendOnceTempHumid(param[0],param[1])
            if getTemperature().created_at == pre1 or getHumidity().created_at == pre2:
                sendOnceTempHumid(param[0],param[1])
            else: 
                break
            timeout = timeout - 1
            if timeout == 0:
                return error(1)
            time.sleep(30)
    return 'Send success'        
                

def message(aio, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))


def sendAction(action,feed):
    timeout = 30
    if type(action).__name__ != 'str' or type(feed).__name__ != 'str':
        return error(0)
    if feed == 'pump':
        pre = getPumpState().created_at
        sendPump(action)
        while(pre == getPumpState().created_at or timeout < 0):
            timeout = timeout - 1
            # time.sleep(30)
    else:
        pre = getLightState().created_at
        sendLight(action)
        while(pre == getLightState().created_at or timeout < 0):
            timeout = timeout - 1
            # time.sleep(30)
    if timeout < 0:
        return 'Timeout, check your connection'
    return 'Send success'

print(sendAction('ON','light'))

