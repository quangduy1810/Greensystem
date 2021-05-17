DROP TABLE IF EXISTS plant_planted_in_land;
DROP TABLE IF EXISTS device_acted_in_land;
DROP TABLE IF EXISTS device_used_in_land;
DROP TABLE IF EXISTS land;
DROP TABLE IF EXISTS device;
DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS plant;

# Người dùng 
CREATE TABLE PERSON (
	Id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(512) NOT NULL,
	Address VARCHAR(512) NOT NULL
);

# Thiết bị và mối quan hệ thiết bị của người dùng nào
CREATE TABLE DEVICE (
	Id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    deviceType VARCHAR(50) NOT NULL,
    UserId INT NOT NULL,
    FOREIGN KEY (UserId) REFERENCES Person(Id)
    ON DELETE CASCADE
);

# Loại cây 
CREATE TABLE PLANT (
	Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    PlantName VARCHAR(50) NOT NULL
);

# Bảng này lưu trữ thông tin về 
# vùng đất và những thông số 
# môi trường liên quan đến 
# vùng đất đó
CREATE TABLE LAND (
	Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    UserId INT NOT NULL,
	LandName VARCHAR(50) NOT NULL,
	PlantId INT NOT NULL,

    #LightonTime INTEGER NOT NULL, # In seconds
	lowerTemperature FLOAT NOT NULL,
    upperTemperature FLOAT NOT NULL,
    lowerHumidity FLOAT NOT NULL,
    upperHumidity FLOAT NOT NULL,
    
    lowerHazardousTemperature FLOAT NOT NULL,  
    upperHazardousTemperature FLOAT NOT NULL,  
	lowerHazardousHumidity FLOAT NOT NULL, 
    upperHazardousHumidity FLOAT NOT NULL, 
    
    FOREIGN KEY (PlantId) REFERENCES Plant(Id)
);


# Bảng này dùng để lưu trữ 
# về những thiết bị ĐANG được sử dụng
# trong những vùng đất
CREATE TABLE DEVICE_USED_IN_LAND (
	DeviceId INT NOT NULL,
    LandId INT NOT NULL,
    
    FOREIGN KEY (DeviceId) REFERENCES Device(Id)
		ON DELETE CASCADE,
    FOREIGN KEY (LandId) REFERENCES Land(Id)
		ON DELETE CASCADE,    
    PRIMARY KEY (DeviceId, LandId)
);

# Bảng này dùng để lưu trữ file log về
# các hoạt động tưới tiêu đã được xảy
# ra cho đến hiện tại.
CREATE TABLE DEVICE_ACTED_IN_LAND (
	DeviceId INT NOT NULL,
    LandId INT NOT NULL,
    RealTime DATETIME NOT NULL,
    
    measurementUnit VARCHAR(20) NOT NULL,
    measurementValue FLOAT NOT NULL,
    
    FOREIGN KEY (DeviceId) REFERENCES Device(Id)
		ON DELETE CASCADE,
    FOREIGN KEY (LandId) REFERENCES Land(Id)
		ON DELETE CASCADE
    ,    
    PRIMARY KEY (DeviceId, LandId)
);

# Bảng này dùng để lưu trữ file log về 
# những loại cây đã được trồng
# trong những vùng đất
CREATE TABLE PLANT_PLANTED_IN_LAND (
	PlantId INT NOT NULL,
    LandId INT NOT NULL,
	StartTime DATETIME NOT NULL,
    EndTime DATETIME NOT NULL,
	
	FOREIGN KEY (PlantId) REFERENCES Plant(Id)
		ON DELETE CASCADE,
	FOREIGN KEY (LandID) REFERENCES Land(Id) 
		ON DELETE CASCADE,
    PRIMARY KEY (PlantId, LandId)
);


INSERT IGNORE INTO Person(Username, Password, Address) VALUES 
	('person1', '12345', ""),
    ('person2', '12345', ""),
    ('person3', '12345', ""),
    ('person4', '12345', ""),
    ('person5', '12345', "")
;

INSERT IGNORE INTO Device(deviceType, UserId) VALUES 
	('LightSensor', 1),
    ('TemperatureSensor', 1),
    ('Pump', 1),
    ('HumiditySensor', 1),
    ('Pump', 1),
	('LightSensor', 2),
    ('TemperatureSensor', 2),
    ('Pump', 2),
    ('HumiditySensor', 2),
    ('Pump', 3)
;

INSERT IGNORE INTO device_used_in_land(DeviceId, LandId) VALUES
	(1, 1),
	(2, 1),
	(3, 1),
	(4, 2),
	(5, 2)
;

-- INSERT IGNORE INTO device_acted_in_land(DeviceId, LandId, RealTime) VALUES

-- ;

INSERT IGNORE INTO PLANT (plantName) VALUES
	("Rice"),
    ("Corn"),
    ("Strawberry"),
    ("Raspberry"),
    ("Melon"),
    ("Pumpkin"),
    ("Cauliflower")
;

INSERT IGNORE INTO LAND(UserId, LandName, PlantId,lowerTemperature,upperTemperature,lowerHumidity,upperHumidity,
	lowerHazardousTemperature, upperHazardousTemperature, lowerHazardousHumidity, upperHazardousHumidity) VALUES
	(1, "land1", 1, 20, 40, 50, 80, 10, 50, 20, 100),
	(2, "land2", 1, 20, 40, 50, 80, 10, 50, 20, 100),
    (3, "land3", 2, 25, 40, 50, 75, 10, 50, 20, 90),
	(4, "land4", 2, 25, 40, 50, 75, 10, 50, 20, 90)
;

SELECT * FROM Land;