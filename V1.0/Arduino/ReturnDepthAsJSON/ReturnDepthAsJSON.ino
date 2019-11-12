#include <ESP8266WiFi.h>
#include <ArduinoJson.h>
 
const char* ssid = "255 Stevens Rd";
const char* password = "dewie123";

int ledPin = 13; // GPIO13
WiFiServer server(80);


 
void setup() {
  Serial.begin(115200);
  delay(10);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  WiFi.hostname("Well_Depth_v2");
 
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
 
  // Start the server
  server.begin();
  Serial.println("Server started");
 
  // Print the IP address
  Serial.print("Use this URL to connect: ");
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");
 
}
 
void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }

  // Turn on the LED (used to flash to indicate we sent data)
  digitalWrite(ledPin, HIGH);
 
  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available()){
    delay(1);
  }
 
    // Prepare the response
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: application/json");
  client.println(""); //  do not forget this one
   
  client.print("{\"IDkey\":\"WellA\",\"sensors\":{\"1\":{\"type\":\"water_depth\",\"value\":");
  client.print(analogRead(A0));
  client.println("}}}\r\n\r\n");
  digitalWrite(ledPin, LOW);
 
  delay(1);
  Serial.println("Client disonnected");
  Serial.println("");

  digitalWrite(ledPin, LOW);
 
}
 
