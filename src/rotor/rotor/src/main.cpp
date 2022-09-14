#include <Servo.h>
#include <Arduino.h>
#include <String.h>
#include "ULN2003APG.h"

ULN2003APG rotor_handle = ULN2003APG(PIN2, PIN3, PIN4, PIN5);
void setup()
{
  rotor_handle.rotation_mode = FULL_STEP;
  Serial.begin(115200);
  // put your setup code here, to run once:
  Serial.write("ok\n");
}

void loop()
{

  if (Serial.available())
  {
    String response;

    response = Serial.readStringUntil('\n');
    response.trim();

    if (response == "test_connection")
      Serial.print("ok\n");
    else
    {

      float angle = response.toFloat();
      rotor_handle.rotate_by_angle(angle);
      rotor_handle.release();
      Serial.print(String(String(angle) + "\n").c_str());
    }
  }

  // rotor_handle.rotate_by_angle(5);
  // rotor_handle.release();
  // delayMicroseconds(500);

  // rotor_handle.rotate_by_angle(-5);
  // rotor_handle.release();
  // delayMicroseconds(500);
}