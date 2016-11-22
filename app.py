from flask import Flask, render_template, request
import json
from test import test_method
app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('child.html')

@app.route("/signUp")
def signUp():
    return render_template('signUp.html')

@app.route("/signUpUser", methods=['POST'])
def signUpUser():
    user = request.form['username'];
    password = request.form['password'];
    return json.dumps({'status':'OK','user':user,'pass':password});

@app.route("/test", methods=['POST'])
def test():
    test_method()
    return render_template('signUp.html')

if __name__ == "__main__":
    app.run()
