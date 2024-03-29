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
| 15v 		| 3.72v		|
| 12v 		| 2.97v  	|
| 10v 		| 2.48v		|

- R3 & R4 = Divider for Sensor 0  (R1 (R4) 2.2k & R2 (R3) 3.3k)   
**NOTE** Max 3.3VDC on ESP8266, not 5VDC like ADS1115
**NOTE** 2k & 1k Resistors would be better suited, didn't have any 2k

|Input Voltage	| Divided Voltage|
|--------	| -------	|
| 5v 		| 3v		|
| 2.5v 		| 1.5v  	|
| 1v 		| 0.6v		|

- R5 & R6 = Divider for Sensor 1
- ** NO DIVIDER FOR AUX 0
- R7 & R8 = Divider for Aux 1
- R9  - Power LED    - Will depend on the LED used. 
- R10 - Sensor 0 LED - Will depend on the LED used. 	(470ohm?)
- R11 - Sensor 1 LED - Will depend on the LED used. 	(470ohm?)

---
### Sensor Wiring 
Shallow Well
|Color 		| Purpose	|
|-------	| -------	|			
|Red 		|Power		|
|Black		|Common		|
|White		|Output	 	|

Deep Well
|Color 		| Purpose	|
|-------	| -------	|			
|Red 		|Power		|
|blue		|Common		|
|yellow		|Output	 	|

https://www.aliexpress.com/item/4-20mA-Submersible-Liquid-Level-Sensor-Water-Level-Transmitter-Tank-Level-Transducer-DC24V-For-Detecting-0/32956105218.html?spm=a2g0s.9042311.0.0.7cfc4c4dooYNBU

Prototype Board:
|Shallow Well 															|
|-------																|
|- Sensor Range		    	= 0 - 1024									|
|- Sensor out of water entirely 	= ~7								|
|- Run out of water at 	     	= 65.0									|
|- 2 ft of water above 100% reading (limitation of the sensor purchased)| 	

Well Depth Sensor V2.0
|Shallow Well 															| Deep Well	|
|-------																| -------	|	
|- Sensor Range		    	= 0 - 23482									| - Sensor Range		    	= 0 - 1024	|
|- Sensor out of water entirely 	= 								| - Sensor out of water entirely 	= 				|
|- Run out of water at 	     	= 	(Estimated/Calculated) 1490 		| - Run out of water at 	     	= 65.0					|
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

##### Arduino GPIOs
|Pin on board		|Pin in Arduino IDE		|Use			|
|-------------------|-----------------------|---------------|
|D0					|GPIO 16 				|Aux Header	&LED-DEPTH1 	|
|D1 				|GPIO 5  				|ADS1115 SCL	|
|D2 				|GPIO 4  				|ADS1115 SDA	|
|D3 				|GPIO 0	 				|LED-DEPTH0		|
|~~D4~~ 			|GPIO 2					|~~LED-DEPTH1~~	|
|D5 				|GPIO 14				|Aux Header	- Setup Pin	|
|D6 				|GPIO 12				|Aux Header		|
|D7 				|GPIO 13 				|Aux Header		|
|D8 				|GPIO 15				|Aux Header		|
|A0					|A0						|~~DEPTH0~~ 		|

* DEPTH0 - It was determiend after testing that... why not just use the 0-5V inputs of the ADS1115 for reading the depth sensors? 
* D5 - Subject to change which one we use but used for a magnetic switch to put the device in Setup Mode

### ADS1115
ADS1115 ADC ultra-compact 16-precision ADC module development board I31
https://www.aliexpress.com/item/32765300165.html
Provides the ESP8266 with additional Analog IOs

+5vdc = 23482

|Pin on board		|Use					|
|-------------------|-----------------------|
|A0					| Board Input Voltage 	|
|A1 				| ~~DEPTH1~~ DEPTH0		|
|A2					| ~~AUX0~~ DEPTH1		|
|A3 				| AUX1					|


#### Address
0x48 (1001000)
http://henrysbench.capnfatz.com/henrys-bench/arduino-voltage-measurements/arduino-ads1115-module-getting-started-tutorial/



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
##### 2019-07-18
- Hooked up solar panel. Sheep had been on well and knocked leads off a few times. Generally working pretty well these past few months other than when the battery gets low the sensor suddenly reads slow. Solar panel will hopefully take care of this. 
##### 2019-07-07 
- Still Seems to be working as intended - was down during a hurricane & we had a power outage... should maybe try to figure out some way to make a buffer if V2.0 submits live data
##### 2020-01-25
- Ran out of water. Adjusted setpoints for warning messages. 

##### New PC - apparently lost some logging that I didn't submit...

##### 2020-01-22
- Realized Shallow well wasn't reading properly (readings were going up/down with Voltage) - Re-wired and got some better looking data. 
- Attempted to hook up Drilled well bypassing extension cable. Knocked power wires loose. Hooked them up backwards and fried everything... (burnt traces off board even)
##### 2020-01-23
- Assembled new depth sensor ignoring A0 on ESP8266 entirely. Made new extension cable and hooked to both wells. Logging at 1m intervals.
- Noticed I'm getting negative values returned when water depth sensor is removed entirely from water (Depth0 - shallow well) 			

##### 2020-06-01
- Ran out of water entirely. Lowest recording was 1203. Immediately went back up to 1724 (may have been from me moving sensor around looking down well)
-- Suggest cut-off at 1700
-- Suggest 1st stage warning of 6000
-- Suggest 2nd stage warning of 3000
-- Had 2000L of water delivered, range went from ~1972 to 19273. (difference of 17,301)

##### 2020-06-11
- Out of water again. Played with Thingboard ruleengine as alerts weren't getting sent out
-- Had 2000Gallons of water delivered, range went from ~2001 to 18246. (difference of 16,245)

##### 2020-08-19
- Getting low on water, put in ~2400L of water. This equated to approximately 3 raw units per L of water on the gauge. 
-- 12203 - 4887 = 3.0483

##### 2021-09-11
- Migrated server to dewie-projects.ca, a cloud hosted server. This is due to receiving Starlink and no longer having an externally facing IP/issues encounterd with MQTT running over a cloudflare tunnel (not possible)



---
## ToDo
- ~~Look at setting a DNS Name for the ESP8266~~
- ~~Find an integrated powersupply option to replace cell phone charger~~
- ~~Voltage divider/voltage monitoring of the battery which runs the electronics at the Well Head~~
- ~~Provisions for a second well depth monitor (Deep well)~~ ADS1115
- Add buffer to logic which clears the alarm to prevent fluxuations from causing a hundred email messages
- Get emails being sent out for low level warnings
#### Future Planning
- ~~Make additional Analog IOs accessible~~
- ~~Make an expansion header to make additional ESP8266 Digital IOs accessible~~ 

## Assembly Notes:
- Don't need resistors for Depth1, just run a jumper in place of R5 (Nothing for R6) to get signal to ESP8266
- Cut traces for -ve of Depth LEDs as they're shorted to an Aux pin and short it to ground when an LED is hooked up. (you have to bypass the resistor and hook ground up via a jumper wire on bottom of board)
- Cut trace for power to Depth 1 LED and jumper to D0 on ESP8266 (was connected to onboard)


#### Next Version
- Don't make anything use internal LED (D4)
- Ground for Aux1 ended up too close to power pins for Depth0 & 1 LEDs and shorted them to ground
- Jumper resistors for Depth0 & 1 LEDs as they're not really necessary in this application 
- Capacitor for 12v Input (After divider) ? (Possibly not necessary)
- DEPTH1 doesn't need a voltage divider, ADS1115 already reads 0-5VDC
- Make both DEPTH0 and DEPTH1 run off ADS1115 (Get rid of voltage divider, jumper, etc)
- Position Text for Screw Terminals where I can actually read it... 
- text for jumpers... 
- Spacing for pins of power supply not quite right
- Not quite enough room for ADS1115 (Depends on which one used)
- Keep traces away from 5v power regulator pins (one currently runs between 5+ pins on board)
- Capicitors for sensors (?) 
- Reverse Polarity protection?
- Join negatives on power regulator so everything is common (12V Status LED was feeding through something else
- Boards are just a hair too big in x axis still. Shave off from left side. Left Screw hole and bottom holes ok. Top holes could go up a hair, far right hole over nearly half width of hole. 
- provisions for magnetic switch on D5 to ground to enter setup mode (D5 - Pin 14?)
- Don't need a voltage divider for measuring battery voltage - just more resistors: https://www.instructables.com/DIY-Monitor-Your-Car-Battery-Code-Setup/


14100432


#### Helpful Links
###### Measuring the battery voltage 
https://raspberrypi.stackexchange.com/questions/55177/vehicle-12v-detection-or-measurement

## Google Cloud integration

#### / Samples of note:
Uploading to Google Cloud:
https://github.com/GoogleCloudPlatform/google-cloud-iot-arduino
- Requires:
https://github.com/esp8266/arduino-esp8266fs-plugin

Combined with the following to send useful data:
http://nilhcem.com/iot/cloud-iot-core-with-the-esp32-and-arduino


#### Libraries possibly used:
https://github.com/dreed47/WifiMQTTManager
* Note Dependencies (and versions of said dependencies)
