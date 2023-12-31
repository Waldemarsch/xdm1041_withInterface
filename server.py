import sys

import flask
from flask import Flask, render_template, request, session
import webview
import threading
import xdm
from xdm import *

app = Flask(__name__, static_folder='../static', template_folder='./templates')
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
        ser.close()
        return "Success", 200


@app.route('/make_single_eval/', methods=['POST'])
def make_single_eval():
    if request.method == "POST":
        ser = serial.Serial(session.get('port'), 115200)
        msg = xdm.make_single_eval(ser)
        ser.close()
        return {"msg": msg}


@app.route('/changeVarMode/', methods=['POST'])
def changeVarMode():
    if request.method == "POST":
        mode = request.json['mode']
        varMode = request.json['varMode']
        ser = serial.Serial(session.get('port'), 115200)
        xdm.xdm_changeVarMode(ser, mode, varMode)
        ser.close()
        return "Success", 200


@app.route('/eval/', methods=['POST', 'GET'])
def make_eval():
    if request.method == "POST":
        var = request.json['var']
        time_v = float(request.json['time'])
        mode = request.json['mode']
        path = request.json['path']
        low_int = request.json['low_int']
        high_int = request.json['high_int']
        dur = request.json['dur']
        ser = serial.Serial(session.get('port'), 115200)
        path, path_graph = xdm.make_eval_with_graph(ser, var, time_v, path, mode, low_int, high_int, dur)
        ser.close()
        filename = f'{path_graph[9:]}'
        print(flask.url_for('static', filename=filename))
        return {'image': flask.url_for('static', filename=filename), 'path': path}


def start_server():
    host = 'localhost'
    port = 5000
    app.run(host=host, port=port)


if __name__ == '__main__':
    t = threading.Thread(target=start_server)
    t.setDaemon(True)
    t.start()
    webview.create_window('Xdm', app)
    webview.start()
    sys.exit()
