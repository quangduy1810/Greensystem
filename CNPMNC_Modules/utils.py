import json

class PlantType(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Device(object):
    def __init__(self, id, type):
        self.id = id
        self.type = type

# Is this the same as UserFarm in the Implementation View Diagram??
class Land(object):
    def __init__(self, tempRange, humidRange, hazardTempRange, hazardHumidRange):
        # self.plantType = plantType
        # self.deviceList = deviceList
        # self.startTime = startTime
        # self.endTime = endTime
        # self.lightOnTime = lightOnTime
        self.temperatureRange = tempRange
        self.humidityRange = humidRange
        # Nhiet do khac nghiet, Do am khac nghiet
        self.hazardousTemperatureRange = hazardTempRange
        self.hazardousHumidityRange = hazardHumidRange

        
class Environment(object):
    def __init__(self, humidity, temperature, brightness):
        self.humidity = humidity
        self.temperature = temperature
        self.brightness = brightness
        # self.lightOnTime = lightOnTime

class DeviceAction(object):
    pass

class PumpAction(DeviceAction):
    def __init__(self, deviceId, status):
        self.deviceId = deviceId
        self.status = status

    def serialize(self):
        payload = {"device_id": str(self.deviceId),"values": [str(self.status)]}

        return json.dumps(payload)

class LightAction(DeviceAction):
    def __init__(self, deviceId, value):
        self.deviceId = deviceId
        self.value = value
    
    def serialize(self):
        payload = {"device_id": str(self.deviceId), "values" : [str(self.status)]}

        return json.dumps(payload)


