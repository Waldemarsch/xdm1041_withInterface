from flask import Flask, render_template, request, session
import json

import xdm
from xdm import *

app = Flask(__name__)
app.secret_key = "ya pidoras"


@app.route('/')
def main_page():
    return render_template("main_page.html")


@app.route('/port/', methods=['POST'])
def port_page():
    if request.method == "POST":
        port = request.form.get('port')
        try:
            ser = serial.Serial(port)
        except Exception as error:
            print(error)
            return render_template("main_page.html")
        ser.close()
        session['port'] = port
        return render_template("port_page.html")
    return render_template("main_page.html")


@app.route('/changeMode/', methods=['POST'])
def changeMode():
    if request.method == "POST":
        mode = request.json['mode']
        ser = serial.Serial(session.get('port'), 115200)
        xdm.xdm_changeMode(ser, mode)
        return "Success", 200


@app.route('/eval/', methods=['POST', 'GET'])
def make_eval():
    if request.method == "POST":
        var = request.json['var']
        time_v = float(request.json['time'])
        dur = float(request.json['dur'])
        ser = serial.Serial(session.get('port'), 115200)
        path_csv, c_time = xdm.make_eval_with_duration(ser, var, time_v, dur)
        path_graph = xdm.make_graph_from_csv(path_csv, c_time)
        return {'image': path_graph}
