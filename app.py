from flask import Flask, render_template, request
import json
from test import test_method, LED0_update, LED1_update, MOTOR_update
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('child.html')

@app.route("/signUp")
def signUp():
    return render_template('signUp.html')

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

@app.route("/test")
def test():
    return test_method();

if __name__ == "__main__":
    app.run(host='0.0.0.0')
