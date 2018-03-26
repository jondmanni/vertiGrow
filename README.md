# vertiGrow
The software side of a robotic vertical gardening system built as part of my senior design project in 2017.
The system was built using a Flask web server hosted on a Raspberry Pi interfacing with an Arduino used as a motor controller. System subroutines interfaced with Flask and received commands via clients connected through LAN.


## Getting Started
(Note: Code required for Raspberry Pi and Arduino has been commented out in 'vertigrow.py' for the sake of testing on other devices. To run using actual hardware, uncomment lines 7, 44-63 in 'vertigrow.py'.)
To run, use Python 3 to run 'app.py' in the project directory as follows:
```
python3 app.py
```
A web server will be hosted at 0.0.0.0:5000. Visit the webpage to view the user interface and system controls.

### Scheduling Events
1. To log into the web server, use the username "user" and password "pass"
2. After you've logged in, events can be added using the panel on the right side of the webpage.
3. To delete a scheduled event, hover over the event in the schedule queue and click the "X" that appears.

### "Testing" and "Calibrating" the System
1. Click on the "Test" or "Calibrate" tabs to view testing and calibration functionality.
2. Use the available options and view system response in the terminal used to run 'app.py.' Though nothing is implemented in hardware (errors may appear as a result), expected response will be shown in the terminal.

### Authors
The software was developed in 2016 and 2017 by Jonathan Manni.

### Special Thanks
Thanks to the following for their libraries:
* jQuery: http://jquery.org
* Flask: http://flask.pocoo.org
* jQuery Timepicker: http://timepicker.co
* Countless code snippets on StackOverflow
