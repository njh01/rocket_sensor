import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pdb
import re
import warnings
warnings.filterwarnings('ignore')
from kfilter import Filter
from dcm import direction_cosine_matrix as dcm 

filename = "data_store.csv"
filename = "data_store_1_maneuver.csv"
filename = "data_store_turn90.csv"
gravity = 9.81 # as measured

def vector_magnitude(a1,a2,a3):
    magnitude = np.sqrt(a1**2+a2**2+a3**2)
    return magnitude

def remove_gravity(ax,ay,az):
    grav_perc = 0.9041*gravity # constant verified from zero movement IMU tests
    mag = vector_magnitude(ax,ay,az)
    x_unit = ax/mag
    y_unit = ay/mag
    z_unit = az/mag
    mag -= grav_perc
    ax = x_unit * mag
    ay = y_unit * mag
    az = z_unit * mag
    return ax,ay,az

def low_pass_filter(p,q,r):
    mag = 1.732 # on average from zero movement IMU tests
    real_mag = vector_magnitude(p,q,r)
    p_unit = p/real_mag
    q_unit = q/real_mag
    r_unit = r/real_mag
    real_mag -= mag
    p = p_unit*real_mag
    q = q_unit*real_mag
    r = r_unit*real_mag
    return p,q,r


def orientation(p,q,r,dt):
    phi = p*dt
    theta = q*dt
    psi = r*dt
    return phi,theta,psi

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
        ax,ay,az=remove_gravity(ax,ay,az)
        p = df.iloc[i][4]
        q = df.iloc[i][5]
        r = df.iloc[i][6]
        p,q,r = low_pass_filter(p,q,r)
        ########################################################################
        # convert from IMU body to reference 
        phi,theta,psi = orientation(p,q,r,dt)
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
    time = f_out[1]
    x = []
    y = []
    z = []
    phi = []
    theta = []
    psi = []
    ax = []
    ay = []
    az = []
    p = []
    q = []
    r = []
    for i in range(len(f_out)):
        x.append(f_out[0][i][0])
        y.append(f_out[0][i][1])
        z.append(f_out[0][i][2])
        phi.append(f_out[0][i][6])
        theta.append(f_out[0][i][7])
        psi.append(f_out[0][i][8])
        ax.append(m_out[0][i][0])
        ay.append(m_out[0][i][1])
        az.append(m_out[0][i][2])
        p.append(m_out[0][i][3])
        q.append(m_out[0][i][4])
        r.append(m_out[0][i][5])
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.asarray(z)
    phi = np.asarray(phi)
    theta = np.asarray(theta)
    psi = np.asarray(psi)
    ax = np.asarray(ax)
    ay = np.asarray(ay)
    az = np.asarray(az)
    p = np.asarray(p)
    q = np.asarray(q)
    r = np.asarray(r)

    plt.figure("Filtered Output",figsize=(9,9))
    plt.subplot(2,1,1)
    plt.plot(time,x,label="x")
    plt.plot(time,y,label="y")
    plt.plot(time,z,label="z")
    plt.title("Position Estimate")
    plt.xlabel("Time, s")
    plt.ylabel("Position, m")
    plt.legend(loc="upper left")
    plt.subplot(2,1,2)
    plt.plot(time,phi,label="phi")
    plt.plot(time,theta,label="theta")
    plt.plot(time,psi,label="psi")
    plt.title("Heading Estimate")
    plt.xlabel("Time, s")
    plt.ylabel("Heading, deg")
    plt.legend(loc="upper left")
    plt.savefig("filter_man1.png")

    plt.figure("Measurements",figsize=(9,9))
    plt.subplot(2,1,1)
    plt.plot(time,ax,label="ax")
    plt.plot(time,ay,label="ay")
    plt.plot(time,az,label="az")
    plt.title("Acceleration input")
    plt.xlabel("Time, s")
    plt.ylabel("Acceleration, m/s/s")
    plt.legend(loc="upper left")
    plt.subplot(2,1,2)
    plt.plot(time,p,label="p")
    plt.plot(time,q,label="q")
    plt.plot(time,r,label="r")
    plt.title("Gyro input")
    plt.xlabel("Time, s")
    plt.ylabel("Angular Rates, deg/s")
    plt.legend(loc="upper left")
    plt.savefig("measurements_man1.png")
    plt.show()

if __name__ == "__main__":
    main()