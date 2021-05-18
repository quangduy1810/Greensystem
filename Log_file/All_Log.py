import pandas as pd

temperature = pd.read_csv("Log_file/Device/temperature_log.csv")
humidity = pd.read_csv("Log_file/Device/humidity_log.csv")
brightness = pd.read_csv("Log_file/Device/brightness_log.csv")
light = pd.read_csv("Log_file/Device/light_log.csv")
pump = pd.read_csv("Log_file/Device/pump_log.csv")

temperature = temperature.drop(['Unnamed: 0'],axis=1)
humidity = humidity.drop(['Unnamed: 0'],axis=1)
brightness = brightness.drop(['Unnamed: 0'],axis=1)
light = light.drop(['Unnamed: 0'],axis=1)
pump = pump.drop(['Unnamed: 0'],axis=1)


all_log = pd.concat([temperature,humidity,brightness,light,pump],axis=0)
all_log['Date time'] = pd.to_datetime(all_log['Date time']).dt.tz_localize(None)
all_log.sort_values(by='Date time',ascending=False,inplace=True)
all_log.reset_index(drop=True,inplace=True)

all_log.to_csv("Log_file/all_log.csv")