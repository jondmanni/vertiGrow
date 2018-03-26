import serial
import time
import datetime
from datetime import datetime as dt

# When using Raspberry Pi
#import RPi.GPIO as GPIO


class vertiGrow(object):

    def flow1_callback(self, channel):
        print("Flow1 Triggered")

    def flow2_callback(self, channel):
        print("Flow2 Triggered")

    def __init__(self, name):
        # Return a vertiGrow object whose name is *name*
        # Creates all variables regarding basic system config
        self.name = name

        # Water Attributes
        self.flow_rate = 0
        self.watering = 0

        # Light Attributes
        self.light_status = 0

        # Robot Attributes
        self.home = 0
        self.location = 0

        # Tray Location Attributes
        self.tray1 = 0
        self.tray2 = 0
        self.tray3 = 0
        self.tray4 = 0
        self.tray5 = 0
        self.tray6 = 0

        # Setup Raspberry Pi
        #setup GPIO using Board numbering
        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(14, GPIO.OUT) # Fertilize Solenoid
        #GPIO.setup(15, GPIO.OUT) # Main Water Solenoid
        #GPIO.setup(18, GPIO.OUT) # Top Boom Solenoid

        #GPIO.setup(17, GPIO.OUT) # Lighting control

        #GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Flow Meter1
        #GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Flow Meter2

        #GPIO.add_event_detect(23, GPIO.FALLING, callback=self.flow1_callback, bouncetime=10)
        #GPIO.add_event_detect(24, GPIO.FALLING, callback=self.flow2_callback, bouncetime=10)

        # Initialize communication with Arduino
        #self.arduino = serial.Serial('/dev/cu.usbmodem1411', 9600, timeout=.1)
        #self.arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=.1)
        time.sleep(2)
        #self.arduino.write("1".encode('ascii'))
        #print(self.arduino.readline())
        #print(self.arduino.readline())

        print("look ma, no hands!")
        # Call getValues in here to make sure we get the proper vals

    def getValues(self):
        # Loads class values from config.txt
        print("worked")

# Water Functions

    def getFlowRate(self):
        # Returns the configured water flow rate for the system in L/s
        return self.flow_rate;

    def setFlowRate(self, volume, units, time):
        # Calculates and sets the flow rate of the system based on the
        # system flow calibration found in the UI
        # Flow rate is set in Liters / second (L/s)
        volume = float(volume) # Convert from string to float
        if (units == "Gal"):
            # Convert Gallons to Liters
            temp_vol = volume * 3.78541
        elif (units == "C"):
            # Convert Cups to Liters
            temp_vol = volume * 0.24
        elif (units == "Oz"):
            # Convert Ounces to Liters
            temp_vol = volume * 0.0295735
        else:
            # Leave in Liters
            temp_vol = volume
        self.flow_rate = temp_vol/(float(time)/1000);

    def setWater(self, status, fertilize):
        # Sets the current status of the water to on or off,
        # where *fertilize* controls if the system should use
        # fertilizer (1 = yes; 0 = no)
        print("Status:", status)
        try:
            if (status == 1): # If the user says to turn water on
                print("Turning water on...")
                if (self.getWater() == 0) : # Check that water is currently off
                    if (fertilize == "True"): # Check for fertilizer
                        print("Fertilizing...")
                        #Turn on water with fertilizer
                        GPIO.output(14, GPIO.HIGH)
                        #Turn on Boom
                        GPIO.output(18, GPIO.HIGH)
                    else: # Fertilizer is off
                        print("Not fertilizing...")
                        # Turn off fertilizer and boom
                        GPIO.output(14, GPIO.LOW)
                        GPIO.output(18, GPIO.LOW)

                        # Turn on water w/o fertilizer
                        GPIO.output(15, GPIO.HIGH)
                        # Turn on Boom
                        GPIO.output(18, GPIO.HIGH)
                    self.watering = 1
            elif (status == 0):           # If the user says to turn water off
                print("Turning water off...")
                if (self.getWater() == 1): # Check that water is currently on
                    # Turn the fertilizer off
                    GPIO.output(14, GPIO.LOW)
                    # Turn the water off
                    GPIO.output(15, GPIO.LOW)
                    # Turn the boom off
                    GPIO.output(18, GPIO.LOW)

                    self.watering = 0
            print("Success!")
            return 0
        except:
            print("Failure!")
            return 1


    def getWater(self):
        # Returns the current status of the watering system,
        # where 0 means off and 1 means on
        return self.watering

# Lighting Functions

    def getLight(self):
        # Returns the current status of the lights:
        # 0: Lights are off
        # 1: Lights are on
        return self.light_status

    def setLight(self, setting):
        # Sets the status of the lights
        # - Setting:
        # 0: Set lights to off
        # 1: Set lights to on

        # Error check setting by making sure it is 0 or 1
        #Do Lights stuff
        if (setting == 1):
            print("Turning lights on...")
            GPIO.output(17, GPIO.HIGH)
        elif (setting == 0):
            print("Turning lights off...")
            GPIO.output(17, GPIO.LOW)
        self.light_status = setting

# Robot Functions

    def isHome(self):
        # Returns if robot is home
        # with open('there.txt', 'r+') as file:
        #     line = file.readline().strip()
        #     print(line)
        #     if line == '1':
        #         return 'home';
        #     else:
        #         return 'away';
        return self.home

    def setLocation(self, location):
        # Sets the location of the robot using *location*
        if (location == "home"):
            self.arduino.write(("0:0:0").encode('ascii'))
            #self.arduino.write(("1:1:"+str(500)+"&").encode('ascii'))
            self.home = 1
            print("info sent to arduino")
        else:
            #print(("1:0:"+str(int(location)*50)+"&").encode('ascii'))
            self.arduino.write(("1:1:1").encode('ascii'))
            #self.arduino.write(("1:0:"+str(int(location)*50)+"&").encode('ascii'))
            print("info sent to arduino")
        print()

    def getLocation(self):
        # Returns location of the robot
        return self.location

# Tray Functions

    def setTray(self, tray, location):
        # Sets the location of a tray based on current setup
        # and user configuration
        print()

# Interface Functions
# Note: These run commands from the scheduler and are implemented
#       using commands above

    def water(self, quantity, webEventList, event, scheduler):
        # *quantity* is a string containing "light", "moderate", or "heavy"
        # *trays* is a list containing the trays that need to watered
        # *webEventList* is the list from which the event should be removed when complete

        print("Just doing a lil bit of watering...")

        self.arduino.write(("1:1:1").encode('ascii'))
        #if (quantity == "light"):
        self.setWater(1, False) # Turn water on
        time.sleep(1.05)
        time.sleep(6.5)
        self.setWater(0, False)
        time.sleep(3)
        self.setWater(1, False)
        time.sleep(6.5)
        self.setWater(0, False)
        time.sleep(3.225)
        self.setWater(1, False)
        time.sleep(6.5)
        self.setWater(0, False)
        time.sleep(3)
        self.setWater(1, False)
        time.sleep(6.5)
        self.setWater(0, False)
        time.sleep(3)
        self.setWater(1, False)
        time.sleep(6.5)
        #elif (quantity == "moderate"):
        #    time.sleep(10)
        #elif (quantity == "heavy"):
        #    time.sleep(45)
        self.setWater(0, False) # Turn water back off

        # Remove the event from the list
        webEventList.remove(event)

        if (event[5] == 'True'): # If repeating
            print("should be setting things up")
            # Do things to set up next watering cycle
            if (event[3] < event[4]):
                date = event[3]
                if (event[6] == "daily"):
                    date += datetime.timedelta(days=1)
                    scheduler.addEventWeb(event[1], event[2], date, event[4], event[5], event[6], event[7], event[8], [])
                elif (event[6] == "every_other"):
                    date += datetime.timedelta(days=2)
                    scheduler.addEventWeb(event[1], event[2], date, event[4], event[5], event[6], event[7], event[8], [])
                elif (event[6] == "weekly"):
                    date += datetime.timedelta(weeks=1)
                    scheduler.addEventWeb(event[1], event[2], date, event[4], event[5], event[6], event[7], event[8], [])

        return 0

    def fertilize(self, webEventList, event):
        # *quantity* is a string containing "light", "moderate", or "heavy"
        # *trays* is a list containing the trays that need to watered
        # *webEventList* is the list from which the event should be removed when complete

        print("Just doing a lil bit of fertilizing...")
        self.setWater(1, True) # Turn water on
        time.sleep(5)
        self.setWater(0, False) # Turn water back off

        # Remove the event from the list
        webEventList.remove(event)
        return 0

    def lighting(self, webEventList, event, scheduler):
        # *webEventList* is the list from which the event should be removed when complete
        # Turns the light on, and then reschedules an event to turn the light off
        print(event[1])
        if (event[1] == "LightingOn"):
            print("Turning the lights on")

            # Turn the lights on
            self.setLight(1)

            # Remove the event from the list
            webEventList.remove(event)

            hour = int(event[8][0:2])
            # Add 12 if in PM
            if (event[8][6] == "P"):
                if (int(event[8][0:2]) != 12):
                    hour = int(event[8][0:2]) + 12
                else:
                    hour = 12

            date = dt.combine(event[3].date(), datetime.time(hour, int(event[8][3:5])))
            print(date)
            scheduler.addEventWeb("lighting_off", event[2], date, event[4], event[5], event[6], event[8], event[8], [])


        elif (event[1] == "LightingOff"):
            print("Turning the lights off")
            self.setLight(0)

            # Remove the event from the list
            webEventList.remove(event)

            if (event[5] == 'True'): # If repeating and LightingOff
                print("should be setting things up")
                # Do things to set up next watering cycle
                if (event[3] < event[4]):
                    date = event[3]
                    if (event[6] == "daily"):
                        date += datetime.timedelta(days=1)
                        scheduler.addEventWeb("lighting", event[2], date, event[4], event[5], event[6], event[7], event[8], [])
                    elif (event[6] == "every_other"):
                        date += datetime.timedelta(days=2)
                        scheduler.addEventWeb("lighting", event[2], date, event[4], event[5], event[6], event[7], event[8], [])
                    elif (event[6] == "weekly"):
                        date += datetime.timedelta(weeks=1)
                        scheduler.addEventWeb("lighting", event[2], date, event[4], event[5], event[6], event[7], event[8], [])

        return 0
