#include <Arduino.h>

class A4988
{
public:
// if pin is disabled
#define DISABLED_PIN UINT8_MAX

  enum Direction
  {
    CW = HIGH,
    CCW = LOW
  };

  A4988(const uint8_t step_pin, const uint8_t dir_pin) : step_pin(step_pin),
                                                         dir_pin(dir_pin)
  {
    /*
    In simple configuration, driver is always enabled, never sleeps, does not require any step division
    thus only two pins that need to be addressed are step and dir pin.
    The rest of addressable pins will be disabled
    */
    pinMode(step_pin, OUTPUT);
    pinMode(dir_pin, OUTPUT);
    digitalWrite(dir_pin, Direction::CW);
  }

  /**
   * @brief checks weather pin is disabled or not
   *
   * @param pin to check
   * @return true if in is disabled
   * @return false if is enabled
   */
  bool IsDisabled(const uint8_t pin)
  {
    return (pin == DISABLED_PIN);
  }

  /**
   * @brief move motor's shaft
   *
   * @param no_steps no steps to move, default: 1
   */
  void Step(int no_steps = 1)
  {
    for (int i = 0; i < no_steps; i++)
    {
      digitalWrite(step_pin, LOW);
      digitalWrite(step_pin, HIGH);
      digitalWrite(step_pin, LOW);
      delay(10);
    }
  }

  /**
   * @brief Set the rotation direction
   *
   * @param direction new rotation direction
   */
  void SetDirection(const Direction direction)
  {
    digitalWrite(dir_pin, direction);
  }

protected:
  // Stepper Motor Driver
  // main driver control pins
  uint8_t step_pin;
  uint8_t dir_pin;

  // general utility
  uint8_t enable_pin = DISABLED_PIN;
  uint8_t sleep_pin = DISABLED_PIN;
  uint8_t reset_pin = DISABLED_PIN;

  // step division pins
  uint8_t ms1_pin = DISABLED_PIN;
  uint8_t ms2_pin = DISABLED_PIN;
  uint8_t ms3_pin = DISABLED_PIN;
};

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
  int no_steps_to_move = (new_angle - current_angle) / step_angle;
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
  else
  {
    response = String("failed to intepret the input>" + message_copy + "<");
  }
  Serial.print(response + "\n");
}