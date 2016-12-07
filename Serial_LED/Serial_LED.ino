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
int motor_steps = 0;
int motor_stop = 0;
int motor_dir = 0;

unsigned long serialdata;
int inbyte;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(11, OUTPUT);  //green LED
  pinMode(9, OUTPUT);  //blue LED
  pinMode(8, OUTPUT);   // debug LED
  AFMS.begin();  // create with the default frequency 1.6KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz

  myMotor->setSpeed(10);  // 10 rpm
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    char ser = Serial.read();
    //this step just sends info back over the serial
    char str[2];
    str[0] = ser;
    str[1] = '\0';
    Serial.print(str);
    //end section
    int green = ser % 2;
    int blue = (ser >> 1) % 2;
    //motor on variable
    int on = (ser >> 2) % 2;
    int motor_cmd = (ser >> 4) % 2;
    // if (motor_cmd != 0) {
    //   motor_steps = (ser >> 5);
    //   motor_stop = (ser >> 2) % 2;
    //   motor_dir = (ser >> 3) % 2; //0 = backward, 1 = forward
    // }

    // begin switching lights
    switch (blue) {
      case 0:
        digitalWrite(8, LOW);
        break;
      case 1:
        digitalWrite(8, HIGH);
        break;
    }
    switch (green) {
      case 0:
        digitalWrite(11, LOW);
        break;
      case 1:
        digitalWrite(11, HIGH);
        break;
    }
    // begin MOTOR section
    if (on == 1) {
      myMotor->step(50, FORWARD, SINGLE);
    }
  }

}
