import serial
import time
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


matplotlib.use('agg')


def xdm_changeMode(ser, mode):
    mode = "CONF:" + mode + '\n'
    ser.write(mode.encode('ASCII'))

def make_eval_with_duration(ser, var, time_v, dur):
    mode = "CONF:" + var + '\n'
    ser.write(mode.encode('ASCII'))

    time.sleep(1)

    time_l = []
    var_l = []

    for i in np.arange(0, dur, time_v):
        time_l.append(i)
        ser.write(b'MEAS?\n')
        msg = float(ser.readline().decode('ASCII'))
        var_l.append(msg)
        print(i, msg)
        time.sleep(time_v)
    df = pd.DataFrame({'time': time_l, f'{var}': var_l})
    current_time = time.strftime('%H.%M.%S', time.localtime())
    path_csv = f'./csv/{current_time}_{var}.csv'
    df.to_csv(path_csv)
    return path_csv, current_time


def make_graph_from_csv(path_csv, c_time):
    df = pd.read_csv(path_csv)

    x = df.iloc[:, 1]
    y = df.iloc[:, 2]

    plt.plot(x, y)

    plt.xlabel("Time, seconds")
    plt.ylabel(list(df.columns)[2])
    path_graph = '/static/' + f'{c_time}_' + list(df.columns)[2] + '.png'
    plt.savefig('.' + path_graph)
    plt.close()
    return path_graph
