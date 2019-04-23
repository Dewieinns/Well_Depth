# Well Depth Sensor V1.0

The First iteration of my Well Water depth sensor which reads the water level from a ~20 ft dug well only. 

#### /Arduino 
Contains the program uploaded to the NodeMCU

#### /Server Side
Contains a script that's run via a cronjob on a Linux server at varying rates (stick to an hour most of the time) which simply polls the NodeMCU for data and logs it to a Database.

---
## Sensor
|Color 		| Purpose	|
|-------	| -------	|			
|Red 		|Power		|
|Black		|Common		|
|White		|Output	 	|

https://www.aliexpress.com/item/4-20mA-Submersible-Liquid-Level-Sensor-Water-Level-Transmitter-Tank-Level-Transducer-DC24V-For-Detecting-0/32956105218.html?spm=a2g0s.9042311.0.0.7cfc4c4dooYNBU

- Sensor Range		    	= 0 - 1024
- Sensor out of water entirely 	= ~7
- Run out of water at 	     	= 65.0
- 2 ft of water above 100% reading (limitation of the sensor purchased)

Data stored raw in DB
Percentage calculated in PHP script that polls database. 

---
## ESP8266 NodeMcu

SeeKool 2 pcs ESP8266 NodeMcu LUA WiFi Module CP2102 ESP-12E Development Board Open Source Serial Wireless Module Works Great with Arduino IDE/Micropython

#### Program via Arduino
https://www.instructables.com/id/Quick-Start-to-Nodemcu-ESP8266-on-Arduino-IDE/

** *CHANGE 'Reset Method' to "nodemcu"* in Arduino IDE

|Pin on board		|Pin in Arduino IDE		|Use		|
|-----------------------|-------------------------------|---------------|
|D7 			|Pin 13 			|LED		|
|D5			|Pin 14				|Sensor Input	|

---
## Log
##### 2019-03-23
- Up and running after determing seller provided wrong wiring information initially. 
- Seems to work fine off 12 (10.90) VDC
##### 2019-04-12 
- Ran the water level down as far as I could get it with Nic's pump then ran the water hydrants on the house managed to get a low reading of 75.0 without actually running out, but could see foot valve. Much lower may as well be considered 0
##### 2019-04-13 
- Had accidentally left the heatpump on after yesterday which ran it completely out of water. Lowest observed reading was 65.0 @ 2019-04-12 23:45:01
##### 2019-04-22 
- Has rained a lot, well finally read 100% full (as high as sensor could read) which appeared to be at the bottom of the 2nd well crock from the top. This is to say there is a couple of ft of water above 100%. 


---
## ToDo
- Look at setting a DNS Name for the NodeMCU
- Voltage divider/voltage monitoring of the battery which runs the electronics at the Well Head
- Provisions for a second well depth monitor (Deep well)