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

unsigned long serialdata;
int inbyte;
int servoPose;
int servoPoses[80] = {};
int attachedServos[80] = {};
int servoPin;
int pinNumber;
int sensorVal;
int analogRate;
int digitalState;

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  getSerial();
  switch(serialdata)
  {
  case 1:
    {
      //analog digital write
      getSerial();
      switch (serialdata)
      {
      case 1:
        {
          //analog write
          getSerial();
          pinNumber = serialdata;
          getSerial();
          analogRate = serialdata;
          pinMode(pinNumber, OUTPUT);
          analogWrite(pinNumber, analogRate);
          pinNumber = 0;
          break;
        }
      case 2:
        {
          //digital write
          getSerial();
          pinNumber = serialdata;
          getSerial();
          digitalState = serialdata;
          pinMode(pinNumber, OUTPUT);
          if (digitalState == 1)
          {
            digitalWrite(pinNumber, LOW);
          }
          if (digitalState == 2)
          {
            digitalWrite(pinNumber, HIGH);
          }
          pinNumber = 0;
          break;

        }
     }
     break;
    }
    case 2:
    {
      getSerial();
      switch (serialdata)
      {
      case 1:
        {
          //analog read
          getSerial();
          pinNumber = serialdata;
          pinMode(pinNumber, INPUT);
          sensorVal = analogRead(pinNumber);
          Serial.println(sensorVal);
          sensorVal = 0;
          pinNumber = 0;
          break;
        }
      case 2:
        {
          //digital read
          getSerial();
          pinNumber = serialdata;
          pinMode(pinNumber, INPUT);
          sensorVal = digitalRead(pinNumber);
          Serial.println(sensorVal);
          sensorVal = 0;
          pinNumber = 0;
          break;
        }
      }
      break;
    }
    case 3:
    {
      getSerial();
      switch (serialdata)
      {
        case 1:
        {
           //servo read
           getSerial();
           servoPin = serialdata;
           Serial.println(servoPoses[servoPin]);
           break;
        }
        case 2:
        {
           //servo write
           getSerial();
           servoPin = serialdata;
           getSerial();
           servoPose = serialdata;
           if (servoPin == 1) {
             // forward
             myMotor->step(servoPose, FORWARD, SINGLE);
           }
           else if (servoPin == 0) {
             // backwards
             myMotor->step(servoPose, BACKWARD, SINGLE);
           }
           break;
        }
        case 3:
        {
          //detach
          getSerial();
          servoPin = serialdata;
          if (attachedServos[servoPin] == 1)
          {
            attachedServos[servoPin] = 0;
          }
        }
      }
    break;
    }
  }
}

long getSerial()
{
  serialdata = 0;
  while (inbyte != '/')
  {
    inbyte = Serial.read();
    if (inbyte > 0 && inbyte != '/')
    {

      serialdata = serialdata * 10 + inbyte - '0';
    }
  }
  inbyte = 0;
  return serialdata;
}
