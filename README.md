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
1. To log into the web server, use the username "user" and password "pass"
