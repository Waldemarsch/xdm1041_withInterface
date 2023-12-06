import os

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
    time.sleep(1)


def xdm_changeVarMode(ser, mode, varMode):
    if mode == "VOLT" or mode == "CURR" :
        varMode = "CONF:" + mode + ':' + varMode + '\n'
    elif mode == "RES":
        varMode = "CONF:" + mode + ' ' + varMode + '\n'
    else:
        varMode = mode + ':' + varMode + '\n'
    print(varMode)
    ser.write(varMode.encode('ASCII'))
    time.sleep(1)


def make_single_eval(ser):
    ser.write(b'MEAS?\n')
    msg = float(ser.readline().decode('ASCII'))
    return msg


def change_mode_and_wait(ser, var):
    xdm_changeMode(ser, var)

    time.sleep(1)


def initialize_csv(path, df):
    df.to_csv(path)


def make_eval_with_graph(ser, var, time_v, path, mode, low_int, high_int, dur):

    print("Begin evaluation with time ", time_v)

    if time_v == 0.:
        # xdm_changeVarMode(ser, mode, var)
        curr_time = time.strftime('%d.%m.%Y___%H_%M_%S', time.localtime())
        path = f'./static/{curr_time}'
        if not os.path.exists('./static'):
            os.mkdir('static')
        os.mkdir(path)

    msg = make_single_eval(ser)
    print(time_v, msg)

    evaluation = {"time": [time_v], f'{var}': [msg]}

    if not os.path.exists(f'./{path}/{var}.csv'):
        df = pd.DataFrame(evaluation)

    else:
        df = pd.read_csv(f'./{path}/{var}.csv', usecols=['time', f'{var}'])
        df.loc[len(df.index)] = [time_v, msg]

    path_csv = f'./{path}/{var}.csv'
    df.to_csv(path_csv)
    path_graph = make_graph_from_csv(path, mode, var, low_int, high_int, dur)

    return path, path_graph


def make_graph_from_csv(path, mode, var, low_int, high_int, dur):
    df = pd.read_csv(f'{path}/{var}.csv')

    x = df.iloc[:, 1]
    y = df.iloc[:, 2]

    plt.figure(figsize=(16, 6))

    plt.plot(x, y)

    plt.xlim([0, float(dur)])
    plt.ylim([float(low_int), float(high_int)])

    plt.xlabel("Time, seconds")
    m_var = list(df.columns)[2]
    if m_var == "VOLT":
        plt.ylabel('Voltage, V')
    elif m_var == "CURR":
        plt.ylabel('Current, A')
    elif m_var == "TEMP":
        print(mode)
        plt.ylabel('Temperature, ' + mode[-1])
    elif m_var == "FREQ":
        plt.ylabel('Frequency, Hz')
    elif m_var == "RES":
        plt.ylabel('Resistance, Ω')
    path_graph = f'{path}/{var}.png'
    plt.savefig(path_graph)
    plt.close()
    return path_graph

