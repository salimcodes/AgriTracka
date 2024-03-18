#include "DHT.h"  // Including the DHT sensor library
#include <LiquidCrystal.h>  // Including the LiquidCrystal library for LCD display

#define DHTPIN 7  // Defining the pin for connecting the DHT sensor
#define DHTTYPE DHT11  // Defining the type of DHT sensor being used

#define VIN 5  // Defining the voltage input pin

int rs = 8;  // Defining LCD pin for RS (Register Select)
int en = 9;  // Defining LCD pin for Enable
int d4 = 10; // Defining LCD pin for data pin 4
int d5 = 11; // Defining LCD pin for data pin 5
int d6 = 12; // Defining LCD pin for data pin 6
int d7 = 13; // Defining LCD pin for data pin 7

LiquidCrystal lcd(rs, en, d4, d5, d6, d7);  // Initializing the LCD object

DHT dht(7, DHT11);  // Initializing the DHT sensor object with pin and type

int photoPin = A0;  // Defining the analog pin for the photoresistor
int width = 15;  // Defining the width for the character buffer

float lux;  // Variable to store light intensity

void setup() {
  Serial.begin(9600);  // Initializing serial communication at 9600 baud
  dht.begin();  // Initializing the DHT sensor
  lcd.begin(16,2);  // Initializing the LCD with 16 columns and 2 rows
}

void loop() {
  float humidity = dht.readHumidity();  // Reading humidity from DHT sensor
  float temperature = dht.readTemperature();  // Reading temperature from DHT sensor
  float lightIntensity = getLightIntensity();  // Reading light intensity from photoresistor

  char buffer1[width + 1];  // Creating character buffer for humidity
  char buffer2[width + 1];  // Creating character buffer for temperature
  char buffer3[width + 1];  // Creating character buffer for light intensity

  dtostrf(humidity, width, 2, buffer1);  // Converting humidity to string and store in buffer1
  dtostrf(temperature, width, 2, buffer2);  // Converting temperature to string and store in buffer2
  dtostrf(lightIntensity, width, 2, buffer3);  // Converting light intensity to string and store in buffer3

  Serial.print("Humidity: ");  // Printing label for humidity
  Serial.print(buffer1);  // Printing humidity value
  Serial.print("%\tTemperature: ");  // Printing label for temperature
  Serial.print(buffer2);  // Printing temperature value
  Serial.print("°C\tLight Intensity: ");  // Printing label for light intensity
  Serial.print(buffer3);  // Printing light intensity value
  Serial.println(" lux");  // Printing units for light intensity
  displayLCD("Humidity", buffer1);  // Displaying humidity on LCD
  delay(2000);  // Delaying for 2 seconds
  displayLCD("Temperature", buffer2);  // Displaying temperature on LCD
  delay(2000);  // Delaying for 2 seconds
  displayLCD("Light Intensity", buffer3);  // Displaying light intensity on LCD
  delay(2000);  // Delaying for 2 seconds
}

float getLightIntensity() {
  int lightReading = analogRead(photoPin);  // Reading analog value from photoresistor
  float voltageOut = float(lightReading) * (VIN / float(1023));  // Converting analog value to voltage
  float RLDR = (4.3 * (VIN - voltageOut)) / voltageOut;  // Calculating resistance of LDR
  float lightIntensity = 500 / (RLDR / 1000);  // Calculating light intensity in lux
  return lightIntensity;  // Returning light intensity value
}

void displayLCD(const char* title, const char* data) {
  lcd.clear();  // Clearing LCD display
  lcd.setCursor(0,0);  // Setting cursor to first column of first row
  lcd.print(title);  // Printing title on LCD
  lcd.setCursor(0,1);  // Setting cursor to first column of second row
  lcd.print(data);  // Printing data on LCD
}
