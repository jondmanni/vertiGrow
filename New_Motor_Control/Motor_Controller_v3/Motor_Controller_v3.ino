#include <AccelStepper.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <string.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield();
// Or, create it with a different I2C address (say for stacking)
// Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x61);

// Connect a stepper motor with 200 steps per revolution (1.8 degree)
// to motor port #2 (M3 and M4)
Adafruit_StepperMotor *myMotor1 = AFMS.getStepper(200, 1);
Adafruit_StepperMotor *myMotor2 = AFMS.getStepper(200, 2);

void forwardstep1() {
  myMotor1->onestep(FORWARD, DOUBLE);
}
void backwardstep1() {
  myMotor1->onestep(BACKWARD, DOUBLE);
}
void forwardstep2() {
  myMotor2->onestep(FORWARD, DOUBLE);
}
void backwardstep2() {
  myMotor2->onestep(BACKWARD, DOUBLE);
}

// Use functions to step
AccelStepper stepper1(forwardstep1, backwardstep1);
AccelStepper stepper2(forwardstep2, backwardstep2);

// Create a home switch variable
int prox1 = 0;
int prox2 = 0;
int homed = 0;

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps

  AFMS.begin();  // create with the default frequency 1.6KHz
  TWBR = ((F_CPU /400000l) - 16) / 2; // Change the i2c clock to 400KHz
  //AFMS.begin(1000);  // OR with a different frequency, say 1KHz

  stepper1.setMaxSpeed(200.0);
  stepper1.setAcceleration(100.0);
  stepper1.setSpeed(200);

  stepper2.setMaxSpeed(200.0);
  stepper2.setAcceleration(100.0);
  stepper2.setSpeed(200);

  // Set Digital Pin 2, 13 to INPUT for prox switch
  pinMode(2, INPUT);
  pinMode(13, INPUT);

  // Set Digital Pin 11 to INPUT for watering switch
  pinMode(3, INPUT);
  attachInterrupt(digitalPinToInterrupt(3), beginWater, RISING);

  // Set Digital Pin 4 to INPUT for fertilize switch
  pinMode(4, INPUT);

  // Set Boom Solenoid
  pinMode(8, OUTPUT);
  // Set Main Solenoid
  pinMode(9, OUTPUT);
  // Set Fert Solenoid
  pinMode(10, OUTPUT);

}

void loop() {
  if ((checkSwitch1() == 1) && (homed==0)) { // we are home
    stepper1.move(0);
    stepper2.move(0);
    stepper1.move(10);
    stepper2.move(10);
    myMotor1->release();
    myMotor2->release();
    homed = 1;
  } else if (checkSwitch2() == 1) { // we are away
    home();
    // Turn off all solenoids
    digitalWrite(8, LOW);
    digitalWrite(9, LOW);
    digitalWrite(10, LOW);
  }
  stepper1.run();
  stepper2.run();
}

void home() {
  stepper1.move(-30000);
  stepper2.move(-30000);
}

// control switch variable to know when prox has been hit
// Returns whether or not the prox switch has been hit.
// This is the home prox switch.
int checkSwitch1() {
  if (digitalRead(13) == LOW) {
    return 0;
  } else {
    prox1 = 1;
  }
  return prox1;
}

// control switch variable to know when prox has been hit
// Returns whether or not the prox switch has been hit.
int checkSwitch2() {
  if (digitalRead(2) == LOW) {
    return 0;
  } else {
    prox2 = 1;
  }
  return prox2;
}

void beginWater() {
  if (digitalRead(4) == HIGH) {
    // Fertilize On
    // Turn on Fertilizer and Boom
    Serial.println("Fertilizing...");
    digitalWrite(9, LOW); // Turn off main
    digitalWrite(10, HIGH); // Turn on fertilizer
    digitalWrite(8, HIGH);  // Turn on boom
  } else {
    // Fertilize off
    Serial.println("Watering...");
    digitalWrite(10, LOW); // Turn off fertilizer
    digitalWrite(9, HIGH); // Turn on main
    digitalWrite(8, HIGH); // Turn on boom
  }
  stepper1.move(30000); // send the stepper away
  stepper2.move(30000);
  homed = 0;
}

// // return command as pointer to
// int* getCommand() {
//
//   static int cmds[6]; // declare array
//
//   int j = 0;
//   String content = "";
//   char character;
//   char input[16];
//
//   while(Serial.available()) {
//       character = Serial.read();
//       content.concat(character);
//       delay(10);
//   }
//
//   if (content != "") {
//     content.toCharArray(input, 16);
//     Serial.println("Input");
//     Serial.println(input);
//     // Read each command pair
//     char* command = strtok(input, "&");
//     while (command != 0) {
//       //http://arduino.stackexchange.com/questions/1013/how-do-i-split-an-incoming-string
//       // Split the command into two values
//       char* separator = strchr(command, ':'); // this char has all incl. 1st ':'
//       if (separator != 0)
//       {
//           *separator = 0; // separates rest from command
//           int motor = atoi(command);
//           //Split that command into two
//           ++separator;
//           char* separator2 = strchr(separator, ':'); // this is all from next ':' on
//           int dir = atoi(separator);
//           int steps = 0;
//           if (separator2 != 0)
//           {
//             *separator2 = 0;
//             ++separator2;
//             steps = atoi(separator2);
//           }
//
//           // Do something with the values
//           cmds[j+0] = motor;
//           cmds[j+1] = dir;
//           cmds[j+2] = steps;
//           //Serial.println(motor);
//           //Serial.println(dir);
//           //Serial.println(steps);
//       }
//       // Find the next command in input string
//       command = strtok(0, "&");
//       Serial.println("Done");
//       j = j + 3; // increment j by 3 to account for 3 values
//     }
//     activateMotors(cmds); // activate motors only when command sent
//   }
//   //return cmds; // return the proper values to outside function
// }
//
// void activateMotors(int *commands_array) {
//   Serial.println(commands_array[0]);
//   Serial.println(commands_array[1]);
//   Serial.println(commands_array[2]);
//   Serial.println(commands_array[3]);
//   Serial.println(commands_array[4]);
//   Serial.println(commands_array[5]);
//   Serial.println(commands_array[6]);
//   // Serial.println("Motors Activated");
//   // Controls Motor1
//   // Serial.println(checkSwitch1());
//   //if ((checkSwitch1() == 0) && (checkSwitch2()==0)) { // not at limits
//     //Serial.println(commands_array[2]);
//     //Serial.println(commands_array[1]);
//
//
//     // if (commands_array[2] > 0) {
//     //
//     //
//     //   if (commands_array[1] == 0) { // move forward
//     //     stepper1.move(commands_array[2]);
//     //   } else {                      // move backward
//     //     stepper1.move(-commands_array[2]);
//     //   }
//     //   commands_array[2] = 0;
//
//
//       //Serial.print("Motor 1 Steps Remaining: ");
//       //Serial.println(commands_array[2]);
//
//       // Check if Motor1 is done moving and send command if so
//       //if (commands_array[2] == 1) {
//       //  Serial.println("Motor 1 is done moving - - - - - - -");
//       //}
//       //commands_array[2]--; // decrement steps remaining
//
//     // This is the home case: 0:0:0
//   if ((commands_array[2]==0) && (commands_array[1]==0)) {
//     home(); // send the stepper home
//     Serial.println("HOME ME BABYABABAYAY");
//   } else if ((commands_array[2]==1) && (commands_array[1]==1)) {
//     stepper1.move(30000); // send the stepper away
//     stepper2.move(30000);
//     Serial.println("AND WE'RE OFF!");
//   } else {
//     commands_array[2] = 0;
//   }
//   homed = 0;
// }
