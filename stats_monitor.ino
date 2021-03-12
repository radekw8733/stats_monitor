#include <AsyncUDP.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include "wifi_secrets.h"
LiquidCrystal_I2C lcd(0x27,16,2);
StaticJsonDocument<1024> doc;
WiFiClient wifi;
AsyncUDP udp;
bool lcdTimerResetted = false;
int lcdTimer = 0;
bool lcdTimerActive = false;
int lcdCurrentCharacter = 0;
bool lcdFirstRowScroll = false;
bool lcdSecondRowScroll = false;
void setup() {
    Serial.begin(115200);
    Serial.setDebugOutput(true);
    WiFi.mode(WIFI_STA);
    WiFi.config(IPAddress(192,168,8,122),IPAddress(192,168,8,1),IPAddress(255,255,255,0));
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    delay(1000);
    udp.listen(2137);
    udp.onPacket(udpMessageReceived);
    lcd.begin();
    ledcSetup(0,5000,8);
    ledcSetup(1,5000,8);
    ledcSetup(2,5000,8);
    ledcAttachPin(19,0);
    ledcAttachPin(18,1);
    ledcAttachPin(5,2);
    ledcWrite(0,255);
    ledcWrite(1,255);
    ledcWrite(2,255);
    lcd.print("ESPDeck ready");
}

void loop () {
    if (lcdTimerResetted == true && lcdTimer > millis() + 1000) {
        lcdTimerActive = true;
    }
    if (lcdTimerActive == true && lcdTimer > millis() + 300) {
        lcdTimer = millis();
        lcdCurrentCharacter++;
        lcd.clear();
        lcd.setCursor(0,0);
        if (lcdFirstRowScroll) {
            lcd.print(doc["firstRow"].as<String>().substring(lcdCurrentCharacter));
        }
        else {
            lcd.print(doc["firstRow"].as<String>());
        }
        lcd.setCursor(0,1);
        if (lcdSecondRowScroll) {
            lcd.print(doc["secondRow"].as<String>().substring(lcdCurrentCharacter));
        }
        lcd.print(doc["secondRow"].as<String>());
    }
}

void udpMessageReceived(AsyncUDPPacket packet) {
    lcdTimerResetted = true;
    lcdTimerActive = false;
    lcdTimer = millis();
    lcdCurrentCharacter = 0;
    Serial.println("Deserializing");
    deserializeJson(doc,packet.data());
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print(doc["firstRow"].as<String>());
    lcd.setCursor(0,1);
    lcd.print(doc["secondRow"].as<String>());
    if (doc["firstRow"].as<String>().length() > 16) {
        lcdFirstRowScroll = true;
    }
    Serial.println("String length " + String(doc["firstRow"].as<String>().length()));
    if (doc["secondRow"].as<String>().length() > 16) {
        lcdSecondRowScroll = true;
    }
    Serial.println("String length2 " + String(doc["secondRow"].as<String>().length()));
    if (doc["type"].as<String>() == "osu") {
        rgb(75, 200, 20);
    }
    if (doc["type"].as<String>() == "spotify") {
        rgb(255, 0, 255);
    }
}

void rgb(int r, int g, int b) {
    ledcWrite(0,r);
    ledcWrite(1,g);
    ledcWrite(2,b);
}