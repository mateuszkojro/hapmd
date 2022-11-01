#include <Arduino.h>
#include "A4988.h"

float step_angle = 360.f / 200.f; // default change in angle, when rotated by one step
float current_angle = 0;
A4988 stepper_motor(6, 8);
String response;
String message;
String command;
String message_copy;

String handle_set(const String &message)
{
  auto new_angle = message.toFloat();
  int no_steps_to_move = round((new_angle - current_angle) / step_angle);
  if (no_steps_to_move < 0)
  {
    stepper_motor.SetDirection(A4988::Direction::CCW);
    no_steps_to_move *= -1;
  }
  else
  {
    stepper_motor.SetDirection(A4988::Direction::CW);
  }
  stepper_motor.Step(no_steps_to_move);
  current_angle = current_angle + (no_steps_to_move * step_angle);
  return String(current_angle);
}
void setup()
{
  Serial.begin(115200);
  Serial.print("arduino_ok\n");
}
void loop()
{
  message = Serial.readStringUntil('\n');
  while (message.length() == 0)
  {
    message = Serial.readStringUntil('\n');
    message.trim(); // deletes all leading and trailing whitespaces
    message.replace("\n", "");
  }

  message_copy = message;

  command = message.substring(0, 3);

  if (command == "get")
  {
    response = String(current_angle) + "";
  }
  else if (command == "set")
  {
    response = handle_set(message.substring(3));
  }
  else if (command == "con")
  {
    response = "arduino_ok";
  }
  else if (command == "ovr")
  {
    current_angle = message.toFloat();
    response = String(current_angle);
  }
  else
  {
    response = String("failed to intepret the input>" + message_copy + "<");
  }
  Serial.print(response + "\n");
}