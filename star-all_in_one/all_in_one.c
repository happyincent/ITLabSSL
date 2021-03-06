#include <SPI.h>
#include <Wire.h>
#include <BH1750.h>
#include <SoftwareSerial.h>

#define SoundSensorPin A10 // this pin read the analog voltage from the sound level meter
#define VREF 5.0           // voltage on AREF pin, default: operating voltage

SoftwareSerial PMS(10, 11); // arduino 的 RX, TX (PM2.5)
BH1750 lightMeter;          // BH1750 感光 → MEGA SCL -> SCL (A21 on Mega)
                            //                    SDA -> SDA (A20 on Mega)

// 紫外光
const int UVOUT = A8; //Output from the sensor
const int REF_3V3 = A9; //3.3V power on the Arduino board

// PIR 人體紅外感應
const int PIRout = 2;

// 路燈
const int led = 3;

/* ---------------------------------------- */

// update 延遲
const unsigned long update_delay = 1000;

// 紅外線控制
bool pir_status = false;
unsigned long PIR_sensed_millis = 0;

const int pir_timeout_default = 1000;    // 紅外線感測到預設亮約 1 (+2) 秒
int pir_timeout = pir_timeout_default;

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
bool led_status = false;

// Declare functions
void update_PMS();
void update_lux();
void update_uv();
void update_loud();
void update_PIR();
void load_cmd();
void send_data();
void change_pir_timeout();
void led_ctrl(bool led_opt, bool pir_opt);
void pir_ctrl(bool pir_opt);

/* ---------------------------------------- */

void setup() {
    pinMode(led, OUTPUT);
    pinMode(PIRout, INPUT);
    pinMode(UVOUT, INPUT);
    pinMode(REF_3V3, INPUT);
    
    Serial.begin(9600);
    inputString.reserve(200);
    
    PMS.begin(9600);
    Wire.begin();
    lightMeter.begin();
}

void loop() {
    load_cmd();
    
    if (pir_status || PIR_sensed_millis > 0) {
        update_PIR();
    }

    // 每 1 秒 update 一次 sensor data
    if (millis() % update_delay == 0) {
        led_status = digitalRead(led);
        update_PMS();
        update_lux();
        update_uv();
        update_loud();
    }
}

void update_PMS() {
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

        ++count;
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
    int if_sensed = digitalRead(PIRout);

    if (if_sensed) {
        PIR_sensed_millis = millis();
        led_ctrl(HIGH, pir_status);
    } else if (PIR_sensed_millis > 0 && millis() - PIR_sensed_millis > pir_timeout) {
        led_ctrl(LOW, pir_status);
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
        } else if (inputString == "led_on") {
            led_ctrl(HIGH, false);
        } else if (inputString == "led_off") {
            led_ctrl(LOW, false);
        } else if (inputString == "pir_on") {
            pir_ctrl(true);
        } else if (inputString == "pir_off") {
            pir_ctrl(false);
        } else if (inputString.startsWith("update_pir_millis=")) {
            change_pir_timeout();
        }
        
        inputString = "";
        stringComplete = false;
    }
}

void send_data() {
    String out ="{\"type\":\"data\", \"content\": {"
                "\"pmat25\": \"" + String(pmat25) + "\"," \
                "\"temperature\": \"" + String(temperature) + "\"," \
                "\"humidity\": \"" + String(humidity) + "\"," \
                "\"uv_intensity\": \"" + String(uv_intensity) + "\"," \
                "\"light_intensity\": \"" + String(light_intensity) + "\"," \
                "\"loudness\": \"" + String(loudness) + "\"," \
                "\"led_status\": \"" + String(led_status) + "\"," \
                "\"pir_status\": \"" + String(pir_status) + "\"," \
                "\"pir_timeout\": \"" + String(pir_timeout) + "\"}}";
    Serial.println(out);
}

void change_pir_timeout() {
    inputString.replace("update_pir_millis=", "");
    int timeout = inputString.toInt();
    pir_timeout = (timeout == 0) ? pir_timeout_default : timeout;
    Serial.println("{\"type\":\"update_pir_millis\", \"content\": {\"pir_timeout\": \"" + String(pir_timeout) + "\"}}");
}

// ---------- led function ----------
void led_ctrl(bool led_opt, bool pir_opt) {
    bool print_msg = led_status != led_opt || pir_status != pir_opt;
  
    if (led_status != led_opt) {
        digitalWrite(led, led_opt);
        led_status = led_opt;
    }
    
    if (pir_status != pir_opt) {
        PIR_sensed_millis = 0;
        pir_status = pir_opt;
    }

    if (print_msg) {
        String out ="{\"type\":\"led_ctrl\", \"content\": {"
                    "\"led_status\": \"" + String(led_status) + "\"," \
                    "\"pir_status\": \"" + String(pir_status) + "\"}}";
        Serial.println(out); 
    }
}

void pir_ctrl (bool opt) {
    // only enable/disable pir if led_off
    if (led_status == LOW && pir_status != opt) {
        PIR_sensed_millis = 0;
        pir_status = opt;

        String out ="{\"type\":\"pir_ctrl\", \"content\": {"
                    "\"pir_status\": \"" + String(pir_status) + "\"}}";
        Serial.println(out);
    }
}

// ---------- uv function ----------
int averageAnalogRead(int pinToRead) {
    byte numberOfReadings = 8;
    unsigned int runningValue = 0;

    for (int x = 0; x < numberOfReadings; ++x)
        runningValue += analogRead(pinToRead);
    
    runningValue /= numberOfReadings;

    return (runningValue);
}

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max) {
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}