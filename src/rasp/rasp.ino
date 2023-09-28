#include <WiFi.h>
#include <Mouse.h>

const char* ssid = "WIFI_NAME";
const char* password = "WIFI_PASSWORD";

int port = 50123;
int x = 0;
int y = 0;
int maxValue = 127;
int minValue = -127;
String cmd = "";

WiFiServer server(port);
WiFiClient client;

void setup() {

  delay(5000);

  Mouse.begin();
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
  }

  server.begin();
}

void loop() {
  if (!client || !client.connected()) {
    client = server.available();
  } 

  while (client.connected()) {
    if (!client.connected()) return;

    String cmd = client.readStringUntil('\r');

    if (cmd.length() > 0) {
      if (cmd[0] == 'M') {
        int commaIndex = cmd.indexOf(',');
        if (commaIndex != -1) {
          x = cmd.substring(1, commaIndex).toInt();
          y = cmd.substring(commaIndex + 1).toInt();

          if (x > maxValue) x = maxValue;
          if (x < minValue) x = minValue;
          if (y > maxValue) y = maxValue;
          if (y < minValue) y = minValue;

          Mouse.move(x, y);
        }
      } else if (cmd[0] == 'C') {
        int randomDelay = random(40, 80);
        Mouse.press(MOUSE_LEFT);
        delay(randomDelay);
        Mouse.release(MOUSE_LEFT);
      } else if (cmd[0] == 'B') {
        if (cmd[1] == '1') {
          Mouse.press(MOUSE_LEFT);
        } else if (cmd[1] == '0') {
          Mouse.release(MOUSE_LEFT);
        }
      }
      cmd = "";

      client.print("ACK\r");
      client.flush();
    }
    delay(1);
  }

  delay(5000);
}