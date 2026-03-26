/**
 * ESP32 Sensor Data Sender
 * Sensors: AD8232 (ECG), MLX90614 (Temperature), MAX30102 (Heart Rate & SpO2)
 */

#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// ==================== WiFi Configuration ====================
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Flask server URL (update with your computer's IP)
const char* serverUrl = "http://192.168.1.100:5000/api/sensor-data";

// ==================== Sensor Libraries ====================
// MAX30102 - Heart Rate & SpO2
#include <MAX30105.h>
#include <spo2_algorithm.h>  // Include for SpO2 calculation

// MLX90614 - Temperature
#include <Adafruit_MLX90614.h>

// ==================== Pin Definitions ====================
#define ECG_PIN 34      // AD8232 OUTPUT to GPIO34 (ADC pin)
#define LO_PLUS_PIN 35  // AD8232 LO+ to GPIO35
#define LO_MINUS_PIN 32 // AD8232 LO- to GPIO32

// ==================== Initialize Sensors ====================
MAX30105 particleSensor;
Adafruit_MLX90614 mlx = Adafruit_MLX90614();

// ==================== Variables ====================
// Heart Rate & SpO2
const int RATE_SIZE = 4;  // Increase this for more averaging
int rates[RATE_SIZE];
int rateSpot = 0;
long lastBeat = 0;
int beatAvg = 0;
int heartRate = 0;
int spo2 = 0;

// ECG
int ecgValue = 0;
bool leadOffDetected = false;

// Temperature
float temperature = 0;

// Timing
unsigned long lastSendTime = 0;
const unsigned long sendInterval = 5000; // Send every 5 seconds

// ==================== Setup ====================
void setup() {
  Serial.begin(115200);
  Serial.println("\n\n=== Vital Signs Monitor ===");
  
  // Connect to WiFi
  connectToWiFi();
  
  // Initialize I2C (SDA=21, SCL=20 for ESP32-S3)
  Wire.begin(21, 20);
  
  // Initialize MAX30102
  initMAX30102();
  
  // Initialize MLX90614
  initMLX90614();
  
  // Configure ECG pins
  initECG();
  
  Serial.println("\n✓ All sensors initialized!");
  Serial.println("Waiting for data...\n");
}

// ==================== WiFi Connection ====================
void connectToWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✓ WiFi connected!");
    Serial.print("  IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n✗ WiFi connection failed!");
  }
}

// ==================== MAX30102 Initialization ====================
void initMAX30102() {
  Serial.print("Initializing MAX30102...");
  
  if (!particleSensor.begin(Wire, I2C_SPEED_FAST)) {
    Serial.println(" FAILED!");
    Serial.println("  - Check wiring: VIN→3.3V, GND→GND, SDA→21, SCL→20");
    while (1);
  }
  
  Serial.println(" OK");
  
  // Configure MAX30102
  byte ledBrightness = 0x1F;  // 0x1F = 6.4mA, 0x7F = 25.4mA, 0xFF = 50mA
  byte sampleAverage = 4;      // 1, 2, 4, 8, 16, 32
  byte ledMode = 2;            // 1 = Red only, 2 = Red + IR
  int sampleRate = 400;        // 50, 100, 200, 400, 800, 1000, 1600, 3200
  int pulseWidth = 411;        // 69, 118, 215, 411
  int adcRange = 4096;         // 2048, 4096, 8192, 16384
  
  particleSensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange);
  
  Serial.println("  ✓ MAX30102 configured");
}

// ==================== MLX90614 Initialization ====================
void initMLX90614() {
  Serial.print("Initializing MLX90614...");
  
  if (!mlx.begin()) {
    Serial.println(" FAILED!");
    Serial.println("  - Check wiring: VIN→3.3V, GND→GND, SDA→21, SCL→20");
  } else {
    Serial.println(" OK");
    Serial.println("  ✓ MLX90614 configured");
  }
}

// ==================== ECG Initialization ====================
void initECG() {
  pinMode(ECG_PIN, INPUT);
  pinMode(LO_PLUS_PIN, INPUT);
  pinMode(LO_MINUS_PIN, INPUT);
  
  Serial.println("✓ ECG (AD8232) configured");
  Serial.println("  - Connect electrodes: RA (Right Arm), LA (Left Arm), RL (Right Leg)");
}

// ==================== Read ECG Signal ====================
int readECG() {
  // Check lead-off detection
  bool loPlus = digitalRead(LO_PLUS_PIN);
  bool loMinus = digitalRead(LO_MINUS_PIN);
  
  if (loPlus || loMinus) {
    if (!leadOffDetected) {
      leadOffDetected = true;
      Serial.println("⚠️ ECG: Lead-off detected! Check electrode connections.");
    }
    return -1;  // Lead-off
  }
  
  leadOffDetected = false;
  return analogRead(ECG_PIN);
}

// ==================== Read Heart Rate from MAX30102 ====================
int readHeartRate() {
  long irValue = particleSensor.getIR();
  
  if (irValue < 50000) {
    // No finger detected
    return 0;
  }
  
  // Simple peak detection
  static long lastIR = 0;
  static unsigned long lastPeakTime = 0;
  
  if (irValue > 50000 && lastIR < 50000) {
    // Detected a beat
    unsigned long now = millis();
    if (lastPeakTime != 0) {
      int interval = now - lastPeakTime;
      if (interval > 300 && interval < 1500) {  // Valid heart rate range
        int hr = 60000 / interval;
        
        // Moving average
        rates[rateSpot++] = hr;
        if (rateSpot >= RATE_SIZE) rateSpot = 0;
        
        beatAvg = 0;
        for (int i = 0; i < RATE_SIZE; i++) {
          beatAvg += rates[i];
        }
        beatAvg /= RATE_SIZE;
        heartRate = beatAvg;
      }
    }
    lastPeakTime = now;
  }
  
  lastIR = irValue;
  return heartRate;
}

// ==================== Read SpO2 from MAX30102 ====================
int readSpO2() {
  // Simplified SpO2 calculation
  // For accurate SpO2, use the spo2_algorithm.h library
  
  long redValue = particleSensor.getRed();
  long irValue = particleSensor.getIR();
  
  if (irValue < 50000) {
    return 0;
  }
  
  // Simple ratio calculation
  float ratio = (float)redValue / (float)irValue;
  
  // Convert to SpO2 (approximate formula)
  // SpO2 = 110 - 25 * ratio
  int calculatedSpO2 = 110 - (int)(25 * ratio);
  
  // Constrain to valid range
  if (calculatedSpO2 < 70) calculatedSpO2 = 70;
  if (calculatedSpO2 > 100) calculatedSpO2 = 100;
  
  spo2 = calculatedSpO2;
  return spo2;
}

// ==================== Read Temperature ====================
float readTemperature() {
  return mlx.readObjectTempC();
}

// ==================== Send Data to Server ====================
void sendData() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("⚠️ WiFi not connected, attempting reconnect...");
    connectToWiFi();
    return;
  }
  
  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  
  // Create JSON payload
  StaticJsonDocument<512> doc;
  doc["heart_rate"] = heartRate;
  doc["spo2"] = spo2;
  doc["temperature"] = temperature;
  doc["ecg_sample"] = ecgValue;
  doc["lead_off"] = leadOffDetected;
  
  // Add timestamp
  doc["timestamp"] = millis();
  
  String payload;
  serializeJson(doc, payload);
  
  int httpResponseCode = http.POST(payload);
  
  if (httpResponseCode > 0) {
    Serial.print("✓ Data sent | ");
    Serial.print("HR: ");
    Serial.print(heartRate);
    Serial.print(" | SpO2: ");
    Serial.print(spo2);
    Serial.print("% | Temp: ");
    Serial.print(temperature, 1);
    Serial.print("°C | ECG: ");
    Serial.print(ecgValue);
    if (leadOffDetected) Serial.print(" | ⚠️ Lead-off");
    Serial.println();
  } else {
    Serial.print("✗ Error sending data: ");
    Serial.println(httpResponseCode);
  }
  
  http.end();
}

// ==================== Main Loop ====================
void loop() {
  unsigned long now = millis();
  
  // Read sensors
  heartRate = readHeartRate();
  spo2 = readSpO2();
  temperature = readTemperature();
  ecgValue = readECG();
  
  // Print debug info every second
  static unsigned long lastDebugPrint = 0;
  if (now - lastDebugPrint >= 1000) {
    lastDebugPrint = now;
    Serial.print("  HR: ");
    Serial.print(heartRate > 0 ? heartRate : 0);
    Serial.print(" BPM | SpO2: ");
    Serial.print(spo2 > 0 ? spo2 : 0);
    Serial.print("% | Temp: ");
    Serial.print(temperature, 1);
    Serial.print("°C | ECG: ");
    Serial.print(ecgValue);
    if (leadOffDetected) Serial.print(" | LEAD-OFF");
    Serial.println();
  }
  
  // Send data at intervals
  if (now - lastSendTime >= sendInterval) {
    lastSendTime = now;
    if (heartRate > 0 && spo2 > 0 && temperature > 0 && !leadOffDetected) {
      sendData();
    } else {
      Serial.println("⚠️ Invalid readings, waiting for stable data...");
    }
  }
  
  delay(50);  // Small delay for stability
}