#include <SPI.h>    
#include <Wire.h>
#include "DHT.h"
#include <BH1750.h>
    
#include <SoftwareSerial.h>
#define DHTPIN 12     // what pin we're connected to DATA
#define DHTTYPE DHT22   // DHT 22  (AM2302)
#define ledDHT 13
#define SoundSensorPin A10 //this pin read the analog voltage from the sound level meter
#define VREF 5.0 //voltage on AREF pin,default:operating voltage
#define roadlight 4

SoftwareSerial PMS(10, 11); // arduino 的RX, TX    (PM2.5)
BH1750 lightMeter;  //BH1750感光→MEGA SCL -> SCL (A21 on Mega)
                    //                SDA -> SDA (A20 on Mega)
    
//PM2.5    
long pmat10 = 0;    
long pmat25 = 0;    
long pmat100 = 0;    
float temperature = 0;    
float humandity = 0;    

//DHT22
int maxHum = 60;
int maxTemp = 30;
DHT dht(DHTPIN, DHTTYPE);

//PIR人體紅外感應
const int led=3;  //路燈
const int PIRout=2;

//紫外光
int UVOUT = A8; //Output from the sensor
int REF_3V3 = A9; //3.3V power on the Arduino board

void setup() {    
  pinMode(ledDHT, OUTPUT);
  pinMode(roadlight, OUTPUT);
  pinMode(led,OUTPUT);  
  pinMode(PIRout,INPUT);
  Serial.begin(9600);    
  PMS.begin(9600);
  dht.begin();
  Wire.begin();
  lightMeter.begin();
  pinMode(UVOUT, INPUT);
  pinMode(REF_3V3, INPUT);
}    
    
    
    
void loop() {    
  String s = "";
  while (Serial.available()) {
      char c = Serial.read();
      if(c!='\n'){
          s += c;
      }
      delay(5);    // 沒有延遲的話 UART 串口速度會跟不上Arduino的速度，會導致資料不完整
  }
  
  if(s=="data\r"){
  //PM2.5
  Serial.print("【PM2.5】"); 
  retrievepm25();  

  //PIR
  int val=digitalRead(PIRout);  //讀取 PIR 輸出
  if (val==HIGH) {   //PIR 有偵測到時 : LED 閃一下
    for(int i=0; i<3; i++){
      digitalWrite(led,HIGH);
      delay(50);
      digitalWrite(led,LOW);
      delay(50);
    }}
  else {  //PIR 沒有偵測到 : LED 暗
    digitalWrite(led,LOW);
    }
//大約5秒後才會再進行偵測
//順時針+敏感；逆時針-敏感
//      ↓
//       +    +
//   ---------------
//    |           |
//     \         /
//       --------



/*
  //DHT22
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
    return;}
  if(h > maxHum || t > maxTemp) {
      digitalWrite(ledDHT, HIGH);
  } else {
     digitalWrite(ledDHT, LOW); 
  }
  Serial.println("---------溫溼度------------"); 
  Serial.print("濕度："); 
  Serial.print(h);
  Serial.print(" %\t");
  Serial.print("溫度："); 
  Serial.print(t);
  Serial.println(" *C ");
  Serial.println();
*/


//BH1750 感光
  float lux = lightMeter.readLightLevel();
  Serial.print("【亮度】：");
  Serial.print(lux);
  Serial.println(" lux");

//紫外光
  int uvLevel = averageAnalogRead(UVOUT);
  int refLevel = averageAnalogRead(REF_3V3);
  
  //Use the 3.3V power pin as a reference to get a very accurate output value from sensor
  float outputVoltage = 3.3 / refLevel * uvLevel;
  
  float uvIntensity = mapfloat(outputVoltage, 0.99, 2.9, 0.0, 15.0);
  Serial.print("【紫外光】:");
  /*
  Serial.print("MP8511 output: ");
  Serial.print(uvLevel);

  Serial.print(" MP8511 voltage: ");
  Serial.print(outputVoltage);
  */
  Serial.print("UV Intensity (mW/cm^2): ");
  Serial.println(uvIntensity);

//sound
    Serial.print("【環境音量】");
    float voltageValue,dbValue;
    voltageValue = analogRead(SoundSensorPin) / 1024.0 * VREF;
    dbValue = voltageValue * 50.0; //convert voltage to decibel value
    Serial.print(dbValue,1);
    Serial.println(" dBA");

  
  Serial.println();
  
  delay(1000);   
  
      
    }
}   




//PM2.5 function   
void retrievepm25(){    
  int count = 0;    
  unsigned char c;    
  unsigned char high;    
  while (PMS.available()) {     
    c = PMS.read();    
    if((count==0 && c!=0x42) || (count==1 && c!=0x4d)){    
      Serial.println("check failed");    
      break;    
    }    
    if(count > 27){     
      Serial.println("complete");    
      break;    
    }    
     else if(count == 10 || count == 12 || count == 14 || count == 24 || count == 26    
     || count == 16 || count == 18 || count == 20 || count == 22    
     ) {    
      high = c;    
    }    
    else if(count == 11){    
      pmat10 = 256*high + c;    
      Serial.print("PM1.0=");   
      Serial.print(pmat10);   
      Serial.print(" ug/m3   ");   
    }    
    else if(count == 13){    
      pmat25 = 256*high + c;    
      Serial.print("PM2.5=");   
      Serial.print(pmat25);   
      Serial.print(" ug/m3   ");     
    }  /*  
    else if(count == 15){    
      pmat100 = 256*high + c;    
      Serial.print("PM10=");   
      Serial.print(pmat100);   
      Serial.println(" ug/m3");  
    }    
     else if(count == 17){    
      int u03 = 256*high + c;    
      Serial.print("PM10=");   
      Serial.print(pmat100);   
      Serial.println(" ug/m3");    
    }    
     else if(count == 19){    
      int u05 = 256*high + c;    
      Serial.print("PM10=");   
      Serial.print(pmat100);   
      Serial.println(" ug/m3");   
    }    
     else if(count == 21){    
      int u10 = 256*high + c;    
      Serial.print("PM10=");   
      Serial.print(pmat100);   
      Serial.println(" ug/m3");     
    }    
     else if(count == 23){    
      int u25 = 256*high + c;    
      Serial.print("PM10=");   
      Serial.print(pmat100);   
      Serial.println(" ug/m3");    
    }    */
     else if(count == 25){            
      temperature = (256*high + c)/10.0;     
      Serial.print("Temp=");   
      Serial.print(temperature);   
      Serial.print("(C)   ");   
  
    }    
    else if(count == 27){                
      humandity = (256*high + c)/10.0;    
      Serial.print("Humidity=");   
      Serial.print(humandity);   
      Serial.println("(%)   ");    
    }       
    count++;    
  }    
  while(PMS.available()) PMS.read();    
  //Serial.println();    
}      

//紫外光function
int averageAnalogRead(int pinToRead)
{
  byte numberOfReadings = 8;
  unsigned int runningValue = 0; 

  for(int x = 0 ; x < numberOfReadings ; x++)
    runningValue += analogRead(pinToRead);
  runningValue /= numberOfReadings;

  return(runningValue);  
}

//紫外光function
float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}