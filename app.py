from flask import Flask, render_template, request, jsonify, Response, json
from methods import LED0_update, LED1_update, MOTOR_update
from multiprocessing import Process
import serial
import vertigrow
import scheduler
from threading import Timer

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('login.html')

@app.route("/config")
def signUp():
    return render_template('child.html')

@app.route("/LED0", methods=['POST'])
def LED0():
    LED0_time = request.form['LED0'];
    LED0_update(LED0_time);
    return json.dumps({'status':'OK','LED0_time':LED0_time});

@app.route("/LED1", methods=['POST'])
def LED1():
    LED1_time = request.form['LED1'];
    LED1_update(LED1_time);
    return json.dumps({'status':'OK','LED1_time':LED1_time});

@app.route("/MOTOR0", methods=['POST'])
def MOTOR0():
    MOTOR0_steps = request.form['MOTOR0'];
    MOTOR_update(MOTOR0_steps);
    return json.dumps({'status':'OK','MOTOR0_steps':MOTOR0_steps});

@app.route("/WATER_ON", methods=['POST'])
def WATER_ON():
    fertilize = request.form['fert_box']
    vertiGrow.setWater(1, fertilize)
    return json.dumps({'status':'OK','Fertilize':fertilize});

@app.route("/WATER_OFF", methods=['POST'])
def WATER_OFF():
    vertiGrow.setWater(0,0)
    return json.dumps({'status':'OK'});

@app.route("/LIGHTS_ON", methods=['POST'])
def LIGHTS_ON():
    # Run Lights_turn_on program
    vertiGrow.setLight(1)
    return json.dumps({'status':'OK'});

@app.route("/LIGHTS_OFF", methods=['POST'])
def LIGHTS_OFF():
    # Run Lights_turn_off program
    vertiGrow.setLight(0)
    return json.dumps({'status':'OK'});

@app.route("/HOME_X", methods=['GET', 'POST'])
def HOME_X():
    if request.method == 'POST':
        # If this was a POST request, tell motors to go Home
        #MOTOR(0, 1)
        vertiGrow.setLocation("home")
        return json.dumps({'status':'far away'})
    elif request.method == 'GET':
        # If this was a GET request, get proper information
        # from a class or a file and send it on with json.dumps
        # so that the javascript can change the button appropriately.
        return json.dumps({'status':vertiGrow.isHome()})

@app.route("/SET_X", methods=['POST'])
def SET_X():
    tray = request.form['tray_select'];
    vertiGrow.setLocation(tray)
    return json.dumps({'tray':tray})

@app.route("/calibFlow", methods=['GET', 'POST'])
def calibFlow():
    if request.method == 'POST':
        # If this was a POST request, send data to vertiGrow.
        volume = request.form['calibrationVolume'];
        units = request.form['calibrationUnits'];
        time = request.form['time'];
        vertiGrow.setFlowRate(volume, units, time)
        return json.dumps({'time':time})
    elif request.method == 'GET':
        # If this was a GET request, get info from vertiGrow.
        return json.dumps({'flow':vertiGrow.getFlowRate()})

@app.route("/addEvent", methods=['GET', 'POST'])
def addEvent():
    if request.method == 'POST':
        # Hidden Quantities should be set to 0
        water_quant = 0
        end_date = 0
        repeat_freq = 0
        end_time = 0
        repeat_days = 0

        # Handle the event types
        eventType = request.form['add_event_select_type'];
        if (eventType == "water"):
            # water_quant = request.form['add_event_water_quantity'];
            print()
        elif (eventType =="lighting"):
            end_time = request.form['add_event_end_time'];

        start_date = request.form['add_event_start_date'];
        repeat = request.form['add_event_repeating']

        if (repeat == "True"):
            end_date = request.form['add_event_end_date'];
            repeat_freq = request.form['add_event_repeat_freq'];
            if (repeat_freq == "custom"):
                repeat_days = [request.form['sunday'], request.form['monday'],
                    request.form['tuesday'], request.form['wednesday'],
                    request.form['thursday'], request.form['friday'],
                    request.form['saturday']];
        time = request.form['add_event_time'];
        return json.dumps({'Status':scheduler.addEventWeb(eventType, water_quant, start_date, end_date,
            repeat, repeat_freq, time, end_time, repeat_days)})
    elif request.method == 'GET':
        # Get event info from scheduler
        #print(scheduler.getQueue())
        return json.dumps({'events':scheduler.getQueue()})

@app.route("/deleteEvent", methods=['POST'])
def deleteEvent():
    # Get unique event ID
    eventID = request.form['event'].split(',')[0];
    return json.dumps({'Status':scheduler.cancelEvent(eventID)})

if __name__ == "__main__":
    vertiGrow = vertigrow.vertiGrow("verti") # Initialize the vertiGrow system
    scheduler = scheduler.Scheduler("Grow", vertiGrow) # Initialize the scheduler
    app.run(host='0.0.0.0')
