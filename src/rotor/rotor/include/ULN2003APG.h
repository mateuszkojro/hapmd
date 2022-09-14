///  stepper driver controller for ULN2003APG

#include <Arduino.h>

#pragma once
enum Direction
{
    POSITIVE,
    NEGATIVE

};
enum RotationMode
{
    HALF_STEP,
    FULL_STEP,
    NONE
};

class ULN2003APG
{

    uint32_t no_steps_per_full_rotation = 64; // default motor model : 28kYj-48
    float gear_ratio = 0.015625;              // default motor model : 28kYj-48 ratio = 1:64

    float step_angle; // final angle after applying all gear_ratios

    // // driver pins
    // //     Code    | MCU IO | Micro-controller Pin
    uint8_t A; //  |  IN1  | PORTA.0
    uint8_t B; //  |  IN2  | PORTA.1
    uint8_t C; //  |  IN3  | PORTA.2
    uint8_t D; //  |  IN4  | PORTA.3

    float current_angle = 0;

    /**
     * @brief (private) set pin states; energize coils in drive to move shaft to next position
     *
     * @param a 0 or 1, for LOW / HIGH pin state
     * @param b 0 or 1, for LOW / HIGH pin state
     * @param c 0 or 1, for LOW / HIGH pin state
     * @param d 0 or 1, for LOW / HIGH pin state
     */
    void write(uint8_t a, uint8_t b, uint8_t c, uint8_t d)
    {

        digitalWrite(A, a);
        digitalWrite(B, b);
        digitalWrite(C, c);
        digitalWrite(D, d);
    }

public:
    RotationMode rotation_mode = RotationMode::FULL_STEP;

    ULN2003APG(const uint8_t A, const uint8_t B, const uint8_t C, const uint8_t D)
        : A(A), B(B), C(C), D(D)
    {
        step_angle = 5.625 * gear_ratio;
        no_steps_per_full_rotation = 360 / step_angle;
        // setup();
        // write(LOW, LOW, LOW, LOW);
        release();
    }

    uint32_t GetNoStepsPerFullRotation() { return no_steps_per_full_rotation; }
    void SetNoStepsPerFullRotation(uint32_t no_steps_per_full_rotation) { this->no_steps_per_full_rotation = no_steps_per_full_rotation; }
    uint32_t GetGearRatio() { return gear_ratio; }
    void SetGearRatio(uint32_t gear_ratio) { this->gear_ratio = gear_ratio; }

    /**
     * @brief rotate one motor step, movement is divided in 8 steps
     *
     * @param direction movement direction
     * @param microsecond_delay movement speed, the lower the delay the faster step
     */
    void full_cycle_step(Direction direction, uint32_t microsecond_delay = 1000)
    {
        if (direction == Direction::NEGATIVE)
        {
            write(1, 0, 0, 0);
            delayMicroseconds(microsecond_delay);
            write(1, 1, 0, 0);
            delayMicroseconds(microsecond_delay);
            write(0, 1, 0, 0);
            delayMicroseconds(microsecond_delay);
            write(0, 1, 1, 0);
            delayMicroseconds(microsecond_delay);
            write(0, 0, 1, 0);
            delayMicroseconds(microsecond_delay);
            write(0, 0, 1, 1);
            delayMicroseconds(microsecond_delay);
            write(0, 0, 0, 1);
            delayMicroseconds(microsecond_delay);
            write(1, 0, 0, 1);
            delayMicroseconds(microsecond_delay);
        }
        else
        {
            write(1, 0, 0, 1);
            delayMicroseconds(microsecond_delay);
            write(0, 0, 0, 1);
            delayMicroseconds(microsecond_delay);
            write(0, 0, 1, 1);
            delayMicroseconds(microsecond_delay);
            write(0, 0, 1, 0);
            delayMicroseconds(microsecond_delay);
            write(0, 1, 1, 0);
            delayMicroseconds(microsecond_delay);
            write(0, 1, 0, 0);
            delayMicroseconds(microsecond_delay);
            write(1, 1, 0, 0);
            delayMicroseconds(microsecond_delay);
            write(1, 0, 0, 0);
            delayMicroseconds(microsecond_delay);
        }
    }
    /**
     * @brief rotate one motor step, movement is divided in 4 steps
     *
     * @param direction movement direction
     * @param microsecond_delay movement speed, the lower the delay the faster step
     */
    void half_cycle_step(Direction direction, uint32_t microsecond_delay = 5000)
    {

        if (direction == NEGATIVE)
        {
            current_angle -= step_angle;
            write(1, 1, 0, 0);
            delayMicroseconds(microsecond_delay);
            write(0, 1, 1, 0);
            delayMicroseconds(microsecond_delay);
            write(0, 0, 1, 1);
            delayMicroseconds(microsecond_delay);
            write(1, 0, 0, 1);
            delayMicroseconds(microsecond_delay);
        }
        else
        {
            current_angle += step_angle;
            write(1, 0, 0, 1);
            delayMicroseconds(microsecond_delay);
            write(0, 0, 1, 1);
            delayMicroseconds(microsecond_delay);
            write(0, 1, 1, 0);
            delayMicroseconds(microsecond_delay);
            write(1, 1, 0, 0);
            delayMicroseconds(microsecond_delay);
        }
    }

    void rotate_to_angle(float angle)
    {
        if (angle < 0)
            angle = 0;

        while (angle >= 360.0)
            angle -= 360.0;

        Direction rotation_direction;

        if (abs(current_angle - angle) < 180)
            rotation_direction = POSITIVE;
        else
            rotation_direction = NEGATIVE;

        while (abs(current_angle - angle) > step_angle)
        {
            if (rotation_mode == HALF_STEP)
                half_cycle_step(rotation_direction, 2000);
            else if (rotation_mode == FULL_STEP)
                full_cycle_step(rotation_direction, 2000);
        }
    }

    float dist(float a, float b)
    {
        return abs(abs(a) - abs(b));
    }

    void rotate_by_angle(float angle)
    {

        while (angle >= 360.0)
            angle -= 360.0;

        while (angle <= -360.0)
            angle += 360.0;

        auto new_angle = current_angle + angle;

        Direction rotation_direction;
        if (angle < 0)
            rotation_direction = NEGATIVE;
        else
            rotation_direction = POSITIVE;

        while (dist(current_angle, new_angle) > step_angle)
        {
            if (rotation_mode == HALF_STEP)
                half_cycle_step(rotation_direction, 2000);
            else if (rotation_mode == FULL_STEP)
                full_cycle_step(rotation_direction, 2000);
        }
    }
    void release()
    {
        write(0, 0, 0, 0);
    }
};