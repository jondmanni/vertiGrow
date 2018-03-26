#include <AccelStepper.h>
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include <string.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// // which pin to use for reading the sensor? can use any pin!
// #define FLOWSENSORPIN 3
//
// // count how many pulses!
// volatile uint16_t pulses = 0;
// // track the state of the pulse pin
// volatile uint8_t lastflowpinstate;
// // you can try to keep time of how long it is between pulses
// volatile uint32_t lastflowratetimer = 0;
// // and use that to calculate a flow rate
// volatile float flowrate;
// // Interrupt is called once a millisecond, looks for any pulses from the sensor!
// SIGNAL(TIMER0_COMPA_vect) {
//   uint8_t x = digitalRead(FLOWSENSORPIN);
//
//   if (x == lastflowpinstate) {
//     lastflowratetimer++;
//     return; // nothing changed!
//   }
//
//   if (x == HIGH) {
//     //low to high transition!
//     pulses++;
//   }
//   lastflowpinstate = x;
//   flowrate = 1000.0;
//   flowrate /= lastflowratetimer;  // in hertz
//   lastflowratetimer = 0;
// }

// void useInterrupt(boolean v) {
//   if (v) {
//     // Timer0 is already used for millis() - we'll just interrupt somewhere
//     // in the middle and call the "Compare A" function above
//     OCR0A = 0xAF;
//     TIMSK0 |= _BV(OCIE0A);
//   } else {
//     // do not call the interrupt function COMPA anymore
//     TIMSK0 &= ~_BV(OCIE0A);
//   }
// }


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
  Serial.println("Stepper test!");
  Serial.println("Motor#:Direction:Steps");

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
  pinMode(9, OUTPUT);
  digitalWrite(9, HIGH);


  // flow sensor
  //pinMode(FLOWSENSORPIN, INPUT);
  //digitalWrite(FLOWSENSORPIN, HIGH);
  //lastflowpinstate = digitalRead(FLOWSENSORPIN);
  //useInterrupt(true);

}

void loop() {
  int *commands;
  // Get a command from serial and activate motors if necessary
  commands = getCommand();

  // this code works
  if ((checkSwitch1() == 1) && (homed==0)) { // we are home
    stepper1.move(0);
    stepper2.move(0);
    stepper1.move(10);
    stepper2.move(10);
    homed = 1;
    digitalWrite(9, HIGH);
  } else if (checkSwitch2() == 1) { // we are away
    stepper1.move(-30000);
    stepper2.move(-30000);
  }
  //
  // if (checkSwitch1() == 1) { // we are home
  //   Serial.println("HOME!");
  //   stepper1.move(0);
  // } else if (checkSwitch2() == 1) {
  //   Serial.println("AWAY!");
  //   stepper1.move(-10000);
  // }

  // if ((checkSwitch1() == 0) && (checkSwitch2() == 0)) {
  //   //stepper1.runSpeedToPosition();
  //   Serial.println('ye');
  // } else if (checkSwitch1() != 0) { // we are home
  //   Serial.println("HOME!");
  //   stepper1.move(-10000);
  // } else if (checkSwitch2() != 0) { // we are away
  //   Serial.println("AWAY!");
  //   stepper1.move(10000);
  // }
  stepper1.run();
  stepper2.run();

  // Use this one
  //Serial.print("Freq: "); Serial.println(flowrate);

  //Serial.print("Pulses: "); Serial.println(pulses, DEC);

  // if a plastic sensor use the following calculation
  // Sensor Frequency (Hz) = 7.5 * Q (Liters/min)
  // Liters = Q * time elapsed (seconds) / 60 (seconds/minute)
  // Liters = (Frequency (Pulses/second) / 7.5) * time elapsed (seconds) / 60
  // Liters = Pulses / (7.5 * 60)

  // Use this one
  //float liters = pulses;
  //liters /= 7.5;
  //liters /= 60.0;

  //Serial.print(liters); Serial.println(" Liters");
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



// return command as pointer to
int* getCommand() {

  static int cmds[6]; // declare array

  int j = 0;
  String content = "";
  char character;
  char input[16];

  while(Serial.available()) {
      character = Serial.read();
      content.concat(character);
      delay(10);
  }

  if (content != "") {
    content.toCharArray(input, 16);
    Serial.println("Input");
    Serial.println(input);
    // Read each command pair
    char* command = strtok(input, "&");
    while (command != 0) {
      //http://arduino.stackexchange.com/questions/1013/how-do-i-split-an-incoming-string
      // Split the command into two values
      char* separator = strchr(command, ':'); // this char has all incl. 1st ':'
      if (separator != 0)
      {
          *separator = 0; // separates rest from command
          int motor = atoi(command);
          //Split that command into two
          ++separator;
          char* separator2 = strchr(separator, ':'); // this is all from next ':' on
          int dir = atoi(separator);
          int steps = 0;
          if (separator2 != 0)
          {
            *separator2 = 0;
            ++separator2;
            steps = atoi(separator2);
          }

          // Do something with the values
          cmds[j+0] = motor;
          cmds[j+1] = dir;
          cmds[j+2] = steps;
          //Serial.println(motor);
          //Serial.println(dir);
          //Serial.println(steps);
      }
      // Find the next command in input string
      command = strtok(0, "&");
      Serial.println("Done");
      j = j + 3; // increment j by 3 to account for 3 values
    }
    activateMotors(cmds); // activate motors only when command sent
  }
  //return cmds; // return the proper values to outside function
}

void activateMotors(int *commands_array) {
  Serial.println(commands_array[0]);
  Serial.println(commands_array[1]);
  Serial.println(commands_array[2]);
  Serial.println(commands_array[3]);
  Serial.println(commands_array[4]);
  Serial.println(commands_array[5]);
  Serial.println(commands_array[6]);
  // Serial.println("Motors Activated");
  // Controls Motor1
  // Serial.println(checkSwitch1());
  //if ((checkSwitch1() == 0) && (checkSwitch2()==0)) { // not at limits
    //Serial.println(commands_array[2]);
    //Serial.println(commands_array[1]);


    // if (commands_array[2] > 0) {
    //
    //
    //   if (commands_array[1] == 0) { // move forward
    //     stepper1.move(commands_array[2]);
    //   } else {                      // move backward
    //     stepper1.move(-commands_array[2]);
    //   }
    //   commands_array[2] = 0;


      //Serial.print("Motor 1 Steps Remaining: ");
      //Serial.println(commands_array[2]);

      // Check if Motor1 is done moving and send command if so
      //if (commands_array[2] == 1) {
      //  Serial.println("Motor 1 is done moving - - - - - - -");
      //}
      //commands_array[2]--; // decrement steps remaining

    // This is the home case: 0:0:0
  if ((commands_array[2]==0) && (commands_array[1]==0)) {
    home(); // send the stepper home
    Serial.println("HOME ME BABYABABAYAY");
  } else if ((commands_array[2]==1) && (commands_array[1]==1)) {
    stepper1.move(30000); // send the stepper away
    stepper2.move(30000);
    Serial.println("AND WE'RE OFF!");
    digitalWrite(9, LOW);
  } else {
    commands_array[2] = 0;
  }

    // Controls Motor2
    // if (commands_array[5] > 0) {
    //   if (commands_array[4] == 0) { // move forward
    //     myMotor2->step(1, FORWARD, SINGLE);
    //   } else {                      // move backward
    //     myMotor2->step(1, BACKWARD, SINGLE);
    //   }
    //   Serial.print("Motor 2 Steps Remaining: ");
    //   Serial.println(commands_array[5]);
    //
    //   // Check if Motor2 is done moving and send command if so
    //   if (commands_array[5] == 1) {
    //     Serial.println("Motor 2 is done moving - - - - - - -");
    //   }
    //   commands_array[5]--; // decrement steps remaining
    // }
  // } else {
  //   Serial.println("STOOOPPPPP PLLLLLEASSSE");
  //   stepper1.move(0);
  // }
  //else {
  //  commands_array[2] = 0;
  //  commands_array[5] = 0;
  //}
  homed = 0;
}
