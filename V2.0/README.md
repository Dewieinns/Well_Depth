# Well Depth Sensor V2.0

The Second iteration of my Well Water depth sensor which reads the water level from a ~20 ft dug well as well as from a ~200 ft drilled well. Built using a custom PCB it also has provisions for two additional Analog IOs and an external header which allows for digital devices.

--- 
## Software

Software is broken in to 3 components:

#### /Arduino 
Contains the program uploaded to the NodeMCU. When a web request comes in the hardware polls the water sensors for their depth, then returns a formatted JSON response.

#### /Server Side
Contains a script that's run via a cronjob on a Linux server hourly which simply polls the NodeMCU for its JSON data and logs the raw data (0-1024) to a Database.

#### *Webserver*
The data is intrepreted and graphed via my personal webserver in various places via various methods for various reasons. 




---
## Hardware 
 Have yet to build this.
 
I have attemped to design a solution that allows me to monitor two wells on my property (possibly more) while including provisions on the board to do more. I also tried to make the unit so I can have multiples of this board printed and use it for the most basic function of monitoring one well (See Notes below). 
 
 
#### Notes:  
- Intentionally used A0 on ESP8266 D1 Mini instead of ADS1115 so board could be assembled as single depth monitor. 
-- This requried voltage divider to be used to use 0-5VDC signal with 0-3.3V range of NodeMCU. 

### Circuit/PCB
https://easyeda.com/dewie/well-depth

---
### Sensor Wiring 
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



---
### ESP8266 D1 Mini
The heart and brains of the board. Connects directly to one Depth Sensor and to another via an ADS1115 (see below). 
https://www.aliexpress.com/item/D1-mini-Mini-NodeMcu-4M-bytes-Lua-WIFI-Internet-of-Things-development-board-based-ESP8266-by/32651747570.html?spm=a2g0s.9042311.0.0.74074c4dUEWRCt

#### Program via Arduino
https://www.instructables.com/id/Quick-Start-to-Nodemcu-ESP8266-on-Arduino-IDE/

** *CHANGE 'Reset Method' to "nodemcu"* in Arduino IDE

|Pin on board		|Pin in Arduino IDE		|Use			|
|-------------------|-----------------------|---------------|
|D0					|Pin  					|Aux Header		|
|D1 				|Pin  					|ADS1115 SCL	|
|D2 				|Pin  					|ADS1115 SDA	|
|D3 				|Pin  					|LED-DEPTH0		|
|D4 				|Pin  					|LED-DEPTH1		|
|D5 				|Pin  					|Aux Header		|
|D5 				|Pin  					|Aux Header		|
|D7 				|Pin 13 				|Aux Header		|
|D8 				|Pin 					|Aux Header		|
|D5					|Pin 14					|Sensor Input	|

### ADS1115
Provides the ESP8266 with additional Analog IOs

|Pin on board		|Use						|
|-------------------|---------------			|
|A0					| Battery Voltage Monitor	|
|A1 				| DEPTH1					|
|A2 				| AUX0 						|
|A3 				| AUX1						|


---
## Log



---
## ToDo
- Look at setting a DNS Name for the ESP8266 
- ~~Voltage divider/voltage monitoring of the battery which runs the electronics at the Well Head~~
- ~~Provisions for a second well depth monitor (Deep well)~~
#### Future Planning
- ~~Make additional Analog IOs accessible~~
- ~~Make an expansion header to make additional ESP8266 Digital IOs accessible ~~




#### Helpful Links
###### Measuring the battery voltage 
https://raspberrypi.stackexchange.com/questions/55177/vehicle-12v-detection-or-measurement
