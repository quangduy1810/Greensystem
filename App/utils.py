import json

class PlantType(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Land(object):
    def __init__(self, tempRange, humidRange, hazardTempRange, hazardHumidRange):
        self.temperatureRange = tempRange
        self.humidityRange = humidRange
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
        payload = {
            "id": str(self.deviceId),
            "name": "PUMP",
            "data": str(self.status),
            "unit": "",
            }

        return json.dumps(payload)

class LightAction(DeviceAction):
    def __init__(self, deviceId, value):
        self.deviceId = deviceId
        self.value = value
    
    def serialize(self):
        payload = {
            "id": str(self.deviceId),
            "name":"LIGHT",
            "data" : str(self.value),
            "unit" : ""
            }

        return json.dumps(payload)
