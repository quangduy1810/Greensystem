DROP TABLE IF EXISTS plant_planted_in_land;
DROP TABLE IF EXISTS device_acted_in_land;
DROP TABLE IF EXISTS device_used_in_land;
DROP TABLE IF EXISTS plant_history;
DROP TABLE IF EXISTS environment_log;
DROP TABLE IF EXISTS land;
DROP TABLE IF EXISTS device;
DROP TABLE IF EXISTS person;
DROP TABLE IF EXISTS plant;


# Người dùng 
CREATE TABLE PERSON (
	Id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Password VARCHAR(512) NOT NULL,
    Name VARCHAR(100) NOT NULL,
	Address VARCHAR(512) NOT NULL,
    Phone VARCHAR(20) NOT NULL
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
    PlantName VARCHAR(50) NOT NULL,
    lowerTemperature FLOAT NOT NULL,
    upperTemperature FLOAT NOT NULL,
    lowerHumidity FLOAT NOT NULL,
    upperHumidity FLOAT NOT NULL,
    
    lowerHazardousTemperature FLOAT NOT NULL,  
    upperHazardousTemperature FLOAT NOT NULL,  
	lowerHazardousHumidity FLOAT NOT NULL, 
    upperHazardousHumidity FLOAT NOT NULL 
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
	Id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	DeviceId INT NOT NULL,
    LandId INT NOT NULL,
    RealTime DATETIME NOT NULL,
	State VARCHAR(20) NOT NULL,
    
    FOREIGN KEY (DeviceId) REFERENCES Device(Id),
    FOREIGN KEY (LandId) REFERENCES Land(Id)
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

# Lịch sử trồng cây, hiện thực của mối quan
# hệ was planted trong erd diagram
CREATE TABLE PLANT_HISTORY(
	LandId INT NOT NULL,
    PlantId INT NOT NULL,
    StartTime DATETIME NOT NULL,
    EndTime DATETIME NOT NULL,
    Comment VARCHAR(256) NOT NULL,
    FOREIGN KEY (LandId) REFERENCES Land(Id)
		ON DELETE CASCADE,
    FOREIGN KEY (PlantId) REFERENCES Plant(Id)
		ON DELETE CASCADE,
    PRIMARY KEY (LandId, PlantId)
);


# môi trường của cây tại một thời điểm
# trong quá khứ. Hiện thực của file log
# khi nhận được dữ liệu từ sensor 
CREATE TABLE ENVIRONMENT_LOG (
	# Use auto-increment for primary key is always a good choice =))
	Id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
    LandId INT NOT NULL,
    measureValue INT NOT NULL,
    measureType VARCHAR(50) NOT NULL,
    CurrentTime DATETIME NOT NULL,
    FOREIGN KEY(LandId) REFERENCES Land(Id)
);

INSERT IGNORE INTO Person(Username, Password, Address, Name, Phone) VALUES 
	('person1', '12345', "", "person1", "0123"),
    ('person2', '12345', "", "person2", "0123"),
    ('person3', '12345', "", "person3", "0123"),
    ('person4', '12345', "", "person4", "0123"),
    ('person5', '12345', "", "person5", "0123")
;

INSERT IGNORE INTO Device(deviceType, UserId) VALUES 
	('Light', 1), -- 1 
    ('Pump', 1),-- 2
    ('Pump', 1),-- 3
    ('Light', 2),-- 4
    ('Light', 2),-- 5
	('Pump', 1),-- 6
    ('Light', 2),-- 7
    ('Pump', 2),-- 8
    ('Pump', 2),-- 9
    ('Pump', 3), -- 10
    ('Pump', 1) -- 11
;



INSERT IGNORE INTO PLANT (plantName,lowerTemperature,upperTemperature,lowerHumidity,upperHumidity,
	lowerHazardousTemperature, upperHazardousTemperature, lowerHazardousHumidity, upperHazardousHumidity) VALUES
	("Rice",20, 40, 50, 80, 10, 50, 20, 100),
    ("Corn",21, 40, 50, 80, 10, 50, 20, 100),
    ("Strawberry",22, 40, 50, 80, 10, 50, 20, 100),
    ("Raspberry",23, 40, 50, 80, 10, 50, 20, 100),
    ("Melon",24, 40, 50, 80, 10, 50, 20, 100),
    ("Pumpkin",25, 40, 50, 80, 10, 50, 20, 100),
    ("Cauliflower",26, 40, 50, 80, 10, 50, 20, 100)
;

INSERT IGNORE INTO LAND(UserId, LandName, PlantId,lowerTemperature,upperTemperature,lowerHumidity,upperHumidity,
	lowerHazardousTemperature, upperHazardousTemperature, lowerHazardousHumidity, upperHazardousHumidity) VALUES
	(1, "land1", 1, 20, 40, 50, 80, 10, 50, 20, 100),
	(2, "land2", 1, 20, 40, 50, 80, 10, 50, 20, 100),
    (3, "land3", 2, 25, 40, 50, 75, 10, 50, 20, 90),
	(4, "land4", 2, 25, 40, 50, 75, 10, 50, 20, 90),
    (1, "land5", 1, 20, 40, 50, 80, 10, 50, 20, 100)
;
INSERT IGNORE INTO device_used_in_land(DeviceId, LandId) VALUES
	(1, 1),
	(2, 1),
	(3, 1),
	(4, 2),
	(5, 2),
    (11,1),
    (6,5),
    (1, 5)
;

SELECT * FROM DEVICE_ACTED_IN_LAND;

SELECT LandName FROM LAND WHERE UserId = 1;

SELECT device.deviceType, device.Id ,device.UserId, device_used_in_land.LandId FROM device INNER JOIN device_used_in_land ON device.ID = device_used_in_land.DeviceId WHERE UserId =1 and device_used_in_land.LandId<>5 ;
SELECT * 
FROM person 
	right join device 
    On device.userid = person.id
    left join device_used_in_land
    on device_used_in_land.deviceid = Device.id
	and device_used_in_land.LandId=5
    where person.Id =1
    and device_used_in_land.DeviceId is Null
     ;

SELECT * FROM ENVIRONMENT_LOG ORDER BY CurrentTIme DESC;

SELECT * FROM (device INNER JOIN device_used_in_land ON device.ID = device_used_in_land.DeviceId) inner join person On device.userid = person.id where UserId=1 ;
SELECT * FROM device INNER JOIN device_used_in_land ON device.ID = device_used_in_land.DeviceId where device_used_in_land.LandId=5;