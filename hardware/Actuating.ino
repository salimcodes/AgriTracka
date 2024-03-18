#include "DHT.h"  // Including the DHT sensor library
#include <LiquidCrystal.h>  // Including the LiquidCrystal library for LCD display

#define DHTPIN 7  // Define the pin for connecting the DHT sensor
#define DHTTYPE DHT11  // Define the type of DHT sensor being used

#define VIN 5  // Define the voltage input pin

int rs = 8;  // Define LCD pin for RS (Register Select)
int en = 9;  // Define LCD pin for Enable
int d4 = 10; // Define LCD pin for data pin 4
int d5 = 11; // Define LCD pin for data pin 5
int d6 = 12; // Define LCD pin for data pin 6
int d7 = 13; // Define LCD pin for data pin 7

LiquidCrystal lcd(rs, en, d4, d5, d6, d7);  // Initialize the LCD object

DHT dht(7, DHT11);  // Initialize the DHT sensor object with pin and type

int photoPin = A0;  // Define the analog pin for the photoresistor
int width = 15;  // Define the width for the character buffer

float lux;  // Variable to store light intensity

void setup() {
  Serial.begin(9600);  // Initialize serial communication at 9600 baud
  dht.begin();  // Initialize the DHT sensor
  lcd.begin(16,2);  // Initialize the LCD with 16 columns and 2 rows
}

void loop() {
  float humidity = dht.readHumidity();  // Read humidity from DHT sensor
  float temperature = dht.readTemperature();  // Read temperature from DHT sensor
  float lightIntensity = getLightIntensity();  // Read light intensity from photoresistor

  char buffer1[width + 1];  // Create character buffer for humidity
  char buffer2[width + 1];  // Create character buffer for temperature
  char buffer3[width + 1];  // Create character buffer for light intensity

  dtostrf(humidity, width, 2, buffer1);  // Convert humidity to string and store in buffer1
  dtostrf(temperature, width, 2, buffer2);  // Convert temperature to string and store in buffer2
  dtostrf(lightIntensity, width, 2, buffer3);  // Convert light intensity to string and store in buffer3

  Serial.print("Humidity: ");  // Print label for humidity
  Serial.print(buffer1);  // Print humidity value
  Serial.print("%\tTemperature: ");  // Print label for temperature
  Serial.print(buffer2);  // Print temperature value
  Serial.print("°C\tLight Intensity: ");  // Print label for light intensity
  Serial.print(buffer3);  // Print light intensity value
  Serial.println(" lux");  // Print units for light intensity
  displayLCD("Humidity", buffer1);  // Display humidity on LCD
  delay(2000);  // Delay for 2 seconds
  displayLCD("Temperature", buffer2);  // Display temperature on LCD
  delay(2000);  // Delay for 2 seconds
  displayLCD("Light Intensity", buffer3);  // Display light intensity on LCD
  delay(2000);  // Delay for 2 seconds
}

float getLightIntensity() {
  int lightReading = analogRead(photoPin);  // Read analog value from photoresistor
  float voltageOut = float(lightReading) * (VIN / float(1023));  // Convert analog value to voltage
  float RLDR = (4.3 * (VIN - voltageOut)) / voltageOut;  // Calculate resistance of LDR
  float lightIntensity = 500 / (RLDR / 1000);  // Calculate light intensity in lux
  return lightIntensity;  // Return light intensity value
}

void displayLCD(const char* title, const char* data) {
  lcd.clear();  // Clear LCD display
  lcd.setCursor(0,0);  // Set cursor to first column of first row
  lcd.print(title);  // Print title on LCD
  lcd.setCursor(0,1);  // Set cursor to first column of second row
  lcd.print(data);  // Print data on LCD
}
