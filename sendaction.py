from App.Constants import *
from App.utils import *
from App.ActionProcessing import *


aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

def connected(aio):
    print('Connected to {0}'.format('humidity'))
    aio.subscribe('temperature')
def disconnected(aio):
    print("Disconnected")
    sys.exit(1)
def subscribe(aio, userdata, mid, granted_qos):
    # This method is called when the aio subscribes to a new feed.
    print('Subscribed to {0} with QoS {1}'.format('humidity', granted_qos[0]))
def message(aio, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))

def getconnectMQTTClient():
    aio = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    
    aio.on_connect = connected
    aio.on_disconnect= disconnected
    aio.on_message = message
    aio.on_subscribe = subscribe

    aio.connect()       
    aio.loop_background()

    return aio 

 
def getPumpState():
    data = aio.data(PUMP_RELAY_FEED_ID)
    return data[0]

def getLightState():
    data = aio.data(LIGHT_RELAY_FEED_ID)
    return data[0]

def waterAction(status):
    client = getconnectMQTTClient()
    if status > 1:
        return 'Wrong action'
    if status == 0:
        pumpAction = PumpAction(PUMP_DEVICE_ID, OFF, "")
    else:
        pumpAction = PumpAction(PUMP_DEVICE_ID, ON, "")

    timeout = 31
    pre = getPumpState().created_at
    client.publish(PUMP_RELAY_FEED_ID, pumpAction.serialize())
    while(timeout > 0):
        if pre != getPumpState().created_at:
            break
        timeout = timeout - 1  
        if timeout <= 0:
            return 'Timeout, check your connection'
        time.sleep(30)
        aio.publish(PUMP_RELAY_FEED_ID, pumpAction.serialize()) 
    pumpTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # insertActionToDatabase(pumpAction, pumpTime)
    return 'Send success'

def lightAction(status):
    client = getconnectMQTTClient()
    if status > 1:
        return 'Wrong action'
        
    lightAction = LightAction(LIGHT_RELAY_FEED_ID, status, "")

    timeout = 31
    pre = getLightState().created_at
    
    client.publish(LIGHT_RELAY_FEED_ID, lightAction.serialize())
    while(timeout > 0):
        if pre != getLightState().created_at:
            break
        timeout = timeout - 1  
        if timeout <= 0:
            return 'Timeout, check your connection'
        time.sleep(30)
        client.publish(LIGHT_RELAY_FEED_ID, lightAction.serialize())
    pumpTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # insertActionToDatabase(lightAction, pumpTime)
    return 'Send success'

def buttonLight():
    lightAction(1)
    time.sleep(120)
    lightAction(0)
    return 'Light off'
    
def buttonPump():
    waterAction(1)
    time.sleep(120)
    waterAction(0)
    return 'Pump off'
