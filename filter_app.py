import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pdb
import re
import warnings
warnings.filterwarnings('ignore')
import utils
from kfilter import Filter
from dcm import direction_cosine_matrix as dcm 

filename = "data_store.csv"
filename = "data_store_1_maneuver.csv"
filename = "data_store_turn90.csv"
filename = "data_store_outdoor_temps.csv"
gravity = 9.81 # as measured

def main():
    df = pd.read_csv(filename,header=None)
    dt = float(re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", df.iloc[0][8])[0])
    kf = Filter(debug=False)
    for i in range(len(df)):
        ax = float(re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", df.iloc[i][1])[0])
        ax *= gravity
        ay = df.iloc[i][2]
        ay *= gravity
        az = df.iloc[i][3]
        az *= gravity
        ax,ay,az=utils.remove_gravity(ax,ay,az)
        p = df.iloc[i][4]
        q = df.iloc[i][5]
        r = df.iloc[i][6]
        p,q,r = utils.low_pass_filter(p,q,r)
        ########################################################################
        # convert from IMU body to reference 
        phi,theta,psi = utils.orientation(p,q,r,dt)
        angles = [psi,theta,phi]
        sequence = [3,2,1]
        mat = dcm()
        accel = np.dot(mat.DCM(angles,sequence),np.asarray([[ax],[ay],[az]]))
        ########################################################################

        ax = accel[0]
        ay = accel[1]
        az = accel[2]
        measurement = np.asarray([[ax],[ay],[az],[p],[q],[r]])
        kf.filter(measurement,dt)

    measurement_data = kf.measurement_save
    filtered_data = kf.Xsave
    m_out = pd.DataFrame(measurement_data)
    f_out = pd.DataFrame(filtered_data)
    utils.plotter(f_out,m_out,df)

if __name__ == "__main__":
    main()