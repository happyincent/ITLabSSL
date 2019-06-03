#include "DHT.h"
#include <SPI.h>
#include <Wire.h>
#include <BH1750.h>
#include <SoftwareSerial.h>

#define DHTPIN 12          // what pin we're connected to DATA
#define DHTTYPE DHT22      // DHT 22 (AM2302)
#define ledDHT 13
#define SoundSensorPin A10 // this pin read the analog voltage from the sound level meter
#define VREF 5.0           // voltage on AREF pin, default: operating voltage
#define roadlight 4

SoftwareSerial PMS(10, 11); // arduino 的 RX, TX (PM2.5)
BH1750 lightMeter;          // BH1750 感光 → MEGA SCL -> SCL (A21 on Mega)
                            //                    SDA -> SDA (A20 on Mega)

// DHT22
DHT dht(DHTPIN, DHTTYPE);

// PIR 人體紅外感應
const int led = 3; // 路燈
const int PIRout = 2;

// 紫外光
int UVOUT = A8; //Output from the sensor
int REF_3V3 = A9; //3.3V power on the Arduino board

// Serial String
String inputString = "";
bool stringComplete = false;

// Init variables
long pmat25 = 0;
float temperature = 0;
float humidity = 0;
float uv_intensity = 0;
float light_intensity = 0;
float loudness = 0;
bool light_status = false;

// Declare functions
void update_pm25();
void update_lux();
void update_uv();
void update_loud();
void update_PIR();
void load_cmd();
void send_data();
void light_ctl();

void setup() {
    pinMode(ledDHT, OUTPUT);
    pinMode(roadlight, OUTPUT);
    pinMode(led, OUTPUT);
    pinMode(PIRout, INPUT);
    Serial.begin(9600);
    PMS.begin(9600);
    dht.begin();
    Wire.begin();
    lightMeter.begin();
    pinMode(UVOUT, INPUT);
    pinMode(REF_3V3, INPUT);
    inputString.reserve(200);
}

void loop() {
    update_pm25();
    update_lux();
    update_uv();
    update_loud();
    update_PIR();
    load_cmd();
    delay(1000);
}

void update_pm25() {
    int count = 0;
    unsigned char c;
    unsigned char high;
    
    while (PMS.available()) {
        c = PMS.read();

        if ((count == 0 && c != 0x42) || (count == 1 && c != 0x4d)) {
            break;
        }

        if (count > 27) {
            break;
        } else if ( count == 10 || count == 12 || count == 14 || \
                    count == 24 || count == 26 || count == 16 || \
                    count == 18 || count == 20 || count == 22) {
            high = c;
        } else if (count == 13) {
            pmat25 = 256 * high + c;
        } else if (count == 25) {
            temperature = (256 * high + c) / 10.0;
        } else if (count == 27) {
            humidity = (256 * high + c) / 10.0;
        }

        count++;
    }
    
    while (PMS.available()) {
        PMS.read();
    }
}

void update_lux() {
    light_intensity = lightMeter.readLightLevel();
}

void update_uv() {
    int uvLevel = averageAnalogRead(UVOUT);
    int refLevel = averageAnalogRead(REF_3V3);
    
    //Use the 3.3V power pin as a reference to get a very accurate output value from sensor
    float outputVoltage = 3.3 / refLevel * uvLevel;
    
    uv_intensity = mapfloat(outputVoltage, 0.99, 2.9, 0.0, 15.0);
}

void update_loud() {
    float voltageValue = analogRead(SoundSensorPin) / 1024.0 * VREF;
    
    //convert voltage to decibel value
    loudness = voltageValue * 50.0;
}

void update_PIR() {
    int val = digitalRead(PIRout); //讀取 PIR 輸出
    if (val == HIGH) {
        //PIR 有偵測到時 : LED 閃一下
        for (int i = 0; i < 3; i++) {
            digitalWrite(led, HIGH);
            delay(50);
            digitalWrite(led, LOW);
            delay(50);
        }
    } else {
        //PIR 沒有偵測到 : LED 暗
        digitalWrite(led, LOW);
    }
}

// ---------- serial function ----------
void serialEvent() {  
  while (Serial.available()) {
    char inChar = (char)Serial.read();

    if (inChar == '\r' || inChar == '\n') {
      if (inputString == "") {
        continue;
      }
      stringComplete = true;
      continue;
    }
    
    inputString += inChar;
  }
}

void load_cmd() {
    if (stringComplete) {
        if (inputString == "data") {
            send_data();
        } else if (inputString == "light") {
            Serial.println("light: status=" + String(light_status));
        } else if (inputString == "light_on") {
            light_ctl(true);
        } else if (inputString == "light_off") {
            light_ctl(false);
        }
        
        inputString = "";
        stringComplete = false;
    }
}

void send_data() {
    String out ="data: " \
                "pmat25=" + String(pmat25) + " " \
                "temperature=" + String(temperature) + " " \
                "humidity=" + String(humidity) + " " \
                "uv_intensity=" + String(uv_intensity) + " " \
                "light_intensity=" + String(light_intensity) + " " \
                "loudness=" + String(loudness) + " " \
                "light_status=" + String(light_status);
    Serial.println(out);
}

// ---------- light function ----------
void light_ctl(bool opt) {
    light_status = opt;
    Serial.println("light_ctl: opt=" + String(opt));
    // digitalWrite(led, opt);
}

// ---------- uv function ----------
int averageAnalogRead(int pinToRead) {
    byte numberOfReadings = 8;
    unsigned int runningValue = 0;

    for (int x = 0; x < numberOfReadings; x++)
        runningValue += analogRead(pinToRead);
    
    runningValue /= numberOfReadings;

    return (runningValue);
}

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max) {
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}
