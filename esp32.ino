#include <WiFi.h>
#include <HTTPClient.h>

// Replace with your network credentials
const char* ssid = "Ritik";
const char* password = "8291189618";

// Flask API endpoints
const char* sensorDataUrl = "https://flask-hello-world-nine-sage.vercel.app/sensor-data"; // Replace with your Flask server URL for sensor data
const char* ledControlUrl = "https://flask-hello-world-nine-sage.vercel.app/led"; // Flask server URL for LED control

// LED pin on the ESP32 (use onboard LED or specify a connected pin)
const int ledPin = 2;  // GPIO2 is often the onboard LED on ESP32

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  WiFi.begin(ssid, password);

  // Wait for WiFi connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void sendSensorData() {
  if (WiFi.status() == WL_CONNECTED) {
    // Generate random temperature and humidity values
    int temperature = random(15, 30); // Random temperature between 15 and 30
    int humidity = random(30, 80);    // Random humidity between 30 and 80

    // Create a JSON object to send
    String jsonData = String("{\"temperature\":") + temperature + ",\"humidity\":" + humidity + "}";

    HTTPClient http;
    http.begin(sensorDataUrl);
    http.addHeader("Content-Type", "application/json"); // Specify the content type

    int httpResponseCode = http.POST(jsonData); // Send the JSON data

    if (httpResponseCode > 0) {
      String response = http.getString(); // Get response
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }
    http.end(); // Free resources
  } else {
    Serial.println("WiFi not connected. Cannot send data.");
  }
}

void checkLEDStatus() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(ledControlUrl);

    int httpResponseCode = http.GET();

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("LED Status Response: " + response);

      if (response.indexOf("\"led_state\":\"on\"") >= 0) {
        digitalWrite(ledPin, HIGH); 
      } else if (response.indexOf("\"led_state\":\"off\"") >= 0) {
        digitalWrite(ledPin, LOW);
      }
    } else {
      Serial.print("Error on sending GET: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }
}

void loop() {
  sendSensorData();      // Send sensor data to the server
  checkLEDStatus();      // Check the LED status from the server
  delay(1000);           // Delay for next cycle (adjust as necessary)
}
