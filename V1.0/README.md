# Well_Depth

The First iteration of my Well Water depth sensor which reads the water level from a ~20 ft dug well only. 

### Arduino 
Contains the program uploaded to the NodeMCU

### Server Side
Contains a script that's run via a cronjob on a Linux server at varying rates (stick to an hour most of the time) which simply polls the NodeMCU for data and logs it to a Database.

## Sensor			
- Red 		Power	
- Black		Common	
- White		Output	 	

https://www.aliexpress.com/item/4-20mA-Submersible-Liquid-Level-Sensor-Water-Level-Transmitter-Tank-Level-Transducer-DC24V-For-Detecting-0/32956105218.html?spm=a2g0s.9042311.0.0.7cfc4c4dooYNBU

- Sensor Range		    	= 0 - 1024
- Sensor out of water entirely 	= ~7
- Run out of water at 	     	= 

Data stored raw in DB
Percentage calculated in PHP script that polls database. 

## ESP8266 NodeMcu

SeeKool 2 pcs ESP8266 NodeMcu LUA WiFi Module CP2102 ESP-12E Development Board Open Source Serial Wireless Module Works Great with Arduino IDE/Micropython
	https://www.instructables.com/id/Quick-Start-to-Nodemcu-ESP8266-on-Arduino-IDE/

** *CHANGE 'Reset Method' to "nodemcu"* in Arduino IDE



|Pin on board		|Pin in Arduino IDE		|Use		|
|-----------------------|-------------------------------|---------------|
|D7 			|Pin 13 			|LED		|
|D5			|Pin 14				|Sensor Input	|


2019-03-23 	- Up and running after determing seller provided wrong wiring information initially. 
		- Seems to work fine off 12 (10.90) VDC