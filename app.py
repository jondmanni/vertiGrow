from flask import Flask, render_template, request
import json
from test import test_method, LED0_update
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('child.html')

@app.route("/signUp")
def signUp():
    return render_template('signUp.html')

@app.route("/LED0", methods=['POST'])
def LED0():
    LED0_time = request.form['LED0_time'];
    return LED0_update(LED0_time);

@app.route("/signUpUser", methods=['POST'])
def signUpUser():
    user = request.form['username'];
    password = request.form['password'];
    return json.dumps({'status':'OK','user':user,'pass':password});

@app.route("/test")
def test():
    return test_method();

if __name__ == "__main__":
    app.run(host='0.0.0.0')
