#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61);

// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #2 (M3 and M4)
Adafruit_StepperMotor *myMotor = AFMS.getStepper(513, 2);

int step_counter = 0;
char motor_steps = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(13, OUTPUT);  //green LED
  pinMode(12, OUTPUT);  //blue LED
  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz

  myMotor->setSpeed(10);  // 10 rpm
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()) {
    char ser = Serial.read();
    char green = ser % 2;
    char blue = (ser >> 1) % 2;
    char motor_stop = (ser >> 2) % 2;
    char motor_dir = (ser >> 3) % 2; //0 = backward, 1 = forward
    char motor_cmd = (ser >> 4) % 2;
    if (motor_cmd == 1) {
      motor_steps = (ser >> 5);
    }
    char step_amt = 0;
    switch (green) {
      case '0':
        digitalWrite(13, LOW);
        break;
      case '1':
        digitalWrite(13, HIGH);
        break;
    }
    switch (blue) {
      case '0':
        digitalWrite(12, LOW);
        break;
      case '1':
        digitalWrite(12, HIGH);
        break;
    }
    switch (motor_stop) {
      case '0': // motor running
        myMotor->setSpeed(10); // speed of motor is 10
        switch(motor_dir) {
          case '0': // motor turning backward
            if (motor_steps > 0) {
              myMotor->step(1, BACKWARD, SINGLE);
              motor_steps--;
            }
            break;
          case '1': // motor turning forward
            if (motor_steps > 0) {
              myMotor->step(1, FORWARD, SINGLE);
              motor_steps--;
            }
            break;
        }
        break;
      case '1': // motor stopped
        myMotor->setSpeed(0); // speed of motor is 0
        break;
    }
  }

}
