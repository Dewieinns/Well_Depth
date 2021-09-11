# Well Depth Monitor



Esp8622 Firmware to allow OTA updates
Tasmota
https://tasmota.github.io/docs/#/installation/
-- Frig that

Kotori Server for handling data/subscriptions/etc
https://getkotori.org/



WiFi Manager
https://randomnerdtutorials.com/wifimanager-with-esp8266-autoconnect-custom-parameter-and-manage-your-ssid-and-password/


OTA Web Updater
https://lastminuteengineers.com/esp32-ota-web-updater-arduino-ide/



Diagnostic page
- Voltage
- Sensor
- buttons for LEDs
- Resolving server properly (DNS name after connecting to WiFi)


Device Attributes:
Static 
- Hardware Version
- Serial Number		= ESP.getChipId()
- ThingsBoardToken

Semi-Static (Shared attributes - have to be added manually)
- Firmware
- Application State? (Enabled/Disabled - would disable LEDs maybe)
- UploadFrequency
- depth0_enabled
- depth0_LowWaterLevel_1
- depth0_LowWaterLevel_2
- depth0_LowWaterLevel_cutoff
- depth1_enabled
- depth1_LowWaterLevel_1
- depth1_LowWaterLevel_2
- depth1_LowWaterLevel_cutoff


Buffer idea:
- If we fail to send add to an array which gets digested


Hang on - we don't want/need Async I don't think... don't need the connection to persist if connecting every 5 minutes


Configuring Thingsboard proxy 
For use this conf, first enable mod_proxy, mod_proxy_http and mod_proxy_wstunnel
a2enmod proxy
a2enmod proxy_http
a2enmod proxy_wstunnel








Reset procedure

Jumper reset pin (onboard LED illuminates)
wait for flashing
remove jumper
boots into config mode




2020-03-14 - Set up device at Sitser's. It works for a while then disconnects and never reconnects. Played with logic to make it never put up an AP when there is something defined for the SSID. When device is reset manually it wipes the SSID and an AP is stood up.
2020-03-16 			- The great server crash of 2020
V2.0-2020.03.18-01 	- Thingsboard Server is now "welldepth.dewie.ca"
					- Only checks for new firmware if new version is not current version or "."
					- Only updates well UploadFrequency if >= 1 (occasionally this was not getting set properly and would upload like crazy)
V2.0-2020.03.21-01 	- Added WiFi.hostname("WellDepthSensor"); 
V2.0-2020.05.10 	- Changed directory bins are located in to /bins/WellDepth/
					- added a couple of Status Messages with regard to updating Firmware to hopefully provide some useful feedback.
V2.0-2020.06.01 	- Added Alarm state client attributes to use to track alarm states and trigger alarms within Thingsboard.
					- Extensive changes to how alarms are set/tracked
					- Reference new variable when flashing LEDs
V2.0-2020.06.01-02 	- Added ability to force more frequent updates when water is below thresholds
V2.0-2020.06.01-03 	- Changed how depth alarm state was stored for impacting upload frequency 
V2.0-2020.06.02 	- Wasn't properly setting the requested upload frequency