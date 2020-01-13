# Well Depth Sensor V2.0

The Second iteration of my Well Water depth sensor which reads the water level from a ~20 ft dug well as well as from a ~200 ft drilled well. Built using a custom PCB it also has provisions for two additional Analog IOs and an external header which allows for digital devices.

--- 
## Software

Software is broken in to 3 components:

#### /Arduino 
Contains the program uploaded to the NodeMCU. When a web request comes in the hardware polls the water sensors for their depth, then returns a formatted JSON response.

Built on:
https://forum.arduino.cc/index.php?topic=223286.0



#### /Server Side
Contains a script that's run via a cronjob on a Linux server hourly which simply polls the NodeMCU for its JSON data and logs the raw data (0-1024) to a Database.

#### *Webserver*
The data is intrepreted and graphed via my personal webserver in various places via various methods for various reasons. 




---
## Hardware 
 
I have attemped to design a solution that allows me to monitor two wells on my property (possibly more) while including provisions on the board to do more. I also tried to make the unit so I can have multiples of this board printed and use it for the most basic function of monitoring one well (See Notes below). 
 
 
#### Notes:  
- Intentionally used A0 on ESP8266 D1 Mini instead of ADS1115 so board could be assembled as single depth monitor. 
-- This requries a voltage divider so we can read the 0-5VDC signal from the sensor with the 0-3.3V range of NodeMCU. 

### Circuit/PCB
https://easyeda.com/dewie/well-depth

#### Voltage Divider
Sensors are fed 12VDC but circuitry can't read that. A Voltage divider is necessary to drop the voltage down so we don't fry the electronics. 
** MORE ON THIS LATER**
- R1 & R2 = Divider for voltage Sensing  (R1 10k & R2 3.3k)

|Input Voltage	| Divided Voltage|
|--------	| -------	|
| 15v 		| 3.72		|
| 12v 		| 2.97v  	|
|10v 		| 2.48		|

- R3 & R4 = Divider for Sensor 0  **NOTE** Max 3.3VDC on ESP8266, not 5VDC like ADS1115
- R5 & R6 = Divider for Sensor 1
- ** NO DIVIDER FOR AUX 0
- R7 & R8 = Divider for Aux 1
- R9  - Power LED    - Will depend on the LED used. 
- R10 - Sensor 0 LED - Will depend on the LED used. 	(470ohm?)
- R11 - Sensor 1 LED - Will depend on the LED used. 	(470ohm?)

---
### Sensor Wiring 
|Color 		| Purpose	|
|-------	| -------	|			
|Red 		|Power		|
|Black		|Common		|
|White		|Output	 	|

https://www.aliexpress.com/item/4-20mA-Submersible-Liquid-Level-Sensor-Water-Level-Transmitter-Tank-Level-Transducer-DC24V-For-Detecting-0/32956105218.html?spm=a2g0s.9042311.0.0.7cfc4c4dooYNBU


|Shallow Well 															| Deep Well	|
|-------																| -------	|	
|- Sensor Range		    	= 0 - 1024									| - Sensor Range		    	= 0 - 1024	|
|- Sensor out of water entirely 	= ~7								| - Sensor out of water entirely 	= 				|
|- Run out of water at 	     	= 65.0									| - Run out of water at 	     	= 65.0					|
|- 2 ft of water above 100% reading (limitation of the sensor purchased)| 					|




---
### ESP8266 D1 Mini
The heart and brains of the board. Connects directly to one Depth Sensor and to another via an ADS1115 (see below). 
https://www.aliexpress.com/item/D1-mini-Mini-NodeMcu-4M-bytes-Lua-WIFI-Internet-of-Things-development-board-based-ESP8266-by/32651747570.html?spm=a2g0s.9042311.0.0.74074c4dUEWRCt

#### Getting Started (Driver)
https://www.wemos.cc/en/latest/tutorials/d1/get_started_with_arduino_d1.html
** May need to reboot after installing driver

#### Program via Arduino
https://www.instructables.com/id/Quick-Start-to-Nodemcu-ESP8266-on-Arduino-IDE/

** *CHANGE 'Reset Method' to "nodemcu"* in Arduino IDE

|Pin on board		|Pin in Arduino IDE		|Use			|
|-------------------|-----------------------|---------------|
|D0				|GPIO 16 				|Aux Header	&LED-DEPTH1 	|
|D1 				|GPIO 5  				|ADS1115 SCL	|
|D2 				|GPIO 4  				|ADS1115 SDA	|
|D3 				|GPIO 0	 				|LED-DEPTH0		|
|~~D4~~ 			|GPIO 2					|~~LED-DEPTH1~~	|
|D5 				|GPIO 14				|Aux Header		|
|D6 				|GPIO 12				|Aux Header		|
|D7 				|GPIO 13 				|Aux Header		|
|D8 				|GPIO 15				|Aux Header		|
|A0				|A0						|DEPTH0 		|


### ADS1115
ADS1115 ADC ultra-compact 16-precision ADC module development board I31
https://www.aliexpress.com/item/32765300165.html
Provides the ESP8266 with additional Analog IOs

#### Address
0x48 (1001000)
http://henrysbench.capnfatz.com/henrys-bench/arduino-voltage-measurements/arduino-ads1115-module-getting-started-tutorial/

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
- ~~Find an integrated powersupply option to replace cell phone charger~~
- ~~Voltage divider/voltage monitoring of the battery which runs the electronics at the Well Head~~
- ~~Provisions for a second well depth monitor (Deep well)~~ ADS1115
#### Future Planning
- ~~Make additional Analog IOs accessible~~
- ~~Make an expansion header to make additional ESP8266 Digital IOs accessible~~ 

#### Next Version
- Don't make anything use internal LED (D4)
- Ground for Aux1 ended up too close to power pins for Depth0 & 1 LEDs and shorted them to ground
- Jumper resistors for Depth0 & 1 LEDs as they're not really necessary in this application 
- Capacitor for 12v Input (After divider) ? (Possibly not necessary)

#### Helpful Links
###### Measuring the battery voltage 
https://raspberrypi.stackexchange.com/questions/55177/vehicle-12v-detection-or-measurement
