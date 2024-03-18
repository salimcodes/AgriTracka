// Including necessary libraries
#include "DHT.h"                // Library for DHT temperature and humidity sensor
#include <LiquidCrystal.h>      // Library for controlling liquid crystal displays (LCDs)

// Defining pin numbers for DHT sensor
#define DHTPIN 7                // Pin connected to the DHT sensor
#define DHTTYPE DHT11           // Type of DHT sensor (DHT11 in this case)


// Setting up pin numbers for LCD
#define vin 5                   // Voltage input pin for the sensor

int rs = 8;                     // Register select pin for the LCD
int en = 9;                     // Enable pin for the LCD
int d4 = 10;                    // Data pin 4 for the LCD
int d5 = 11;                    // Data pin 5 for the LCD
int d6 = 12;                    // Data pin 6 for the LCD
int d7 = 13;                    // Data pin 7 for the LCD

// Initializing LiquidCrystal object with the pin numbers
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);

// Initializing DHT sensor object
DHT dht(7, DHT11);

// Defining pin number for photoresistor and width for buffer
int photopin = A0;              // Pin connected to the photoresistor
int width = 15;                 // Width for buffer

float lux;                      // Variable to store light intensity

// Setup function runs once when the microcontroller starts
void setup() {

  Serial.begin(9600);          // Start serial communication at 9600 bits per second
  dht.begin();                  // Initialize DHT sensor
  lcd.begin(16,2);              // Initialize LCD with 16 columns and 2 rows

}

// Loop function runs repeatedly as long as the microcontroller is powered
void loop() {

  float h = dht.readHumidity();      // Read humidity from DHT sensor

  // Initialize character arrays (buffers) to store sensor readings as strings
  char buffer1[width + 1];           
  char buffer2[width + 1];
  char buffer3[width + 1];

  float t = dht.readTemperature();   // Read temperature from DHT sensor

  // Read light intensity from photoresistor and convert raw value to physical value
  float light = analogRead(photopin);  
  lux = sensorRawToPhys(light);

  // Convert sensor readings to strings and store them in buffers
  dtostrf(h, width, 2, buffer1);   
  dtostrf(t, width, 2, buffer2);
  dtostrf(lux, width, 2, buffer3);

  // Print sensor readings to serial monitor
  Serial.print(buffer1);
  Serial.print(buffer2);
  Serial.print(buffer3);
  Serial.println(); 

  delay(2000);  // Delay for 2 seconds before taking next readings
}

// Function to convert raw sensor value to physical value (lux)
float sensorRawToPhys(int raw)
{
  // Calculate output voltage from the sensor
  float Vout = float(raw) * (vin / float(1023));
  // Calculate resistance of LDR (Light Dependent Resistor)
  float RLDR = (4.3 * (vin - Vout))/Vout;
  // Convert resistance to lux value using a simple approximation
  float phys = 500/(RLDR/1000);
  return phys;  // Return the lux value
}
