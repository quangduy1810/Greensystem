from ActionProcessing import *
from CustomEnvironmentUpdate import *
from utils import *


if __name__ == "__main__":
    env = Environment(humidity=85,temperature=35,brightness=212)
    land = Land(    
        tempRange=(20,30),humidRange=(70,80),
        hazardHumidRange=(40,90),hazardTempRange=(15,45))

    processAction(land,env)
