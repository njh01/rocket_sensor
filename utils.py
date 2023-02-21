import matplotlib.pyplot as plt
import numpy as np
import re

gravity = 9.81

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

def temp_conversion(celcius):
    fahr = celcius*(9/5) + 32
    return fahr

def plotter(f_out,m_out,df,disp=True,save=True):
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
    temps = []
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
        temps.append(float(re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", df.iloc[i][7])[0]))
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
    temps = np.asarray(temps)

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
    if save:
        plt.savefig("filter.png")

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
    if save:
        plt.savefig("measurements.png")

    fs = np.round(temp_conversion(temps),3)
    temps = np.round(temps,3)
    avg_temp = np.round(np.mean(temps),1)
    avg_tempf = temp_conversion(avg_temp)
    figs,ax1=plt.subplots(figsize=(6,6))
    ax2 = ax1.twinx()
    ax1.plot(time,temps,label="celcius,avg="+str(avg_temp),color="firebrick")
    ax2.plot(time,fs,label="fahrenheit,avg="+str(avg_tempf),color="royalblue")
    ax1.set_title("Temperature")
    ax1.set_xlabel("Time, s")
    ax1.set_ylabel("Temperature, C")
    ax2.set_ylabel("Temperature, F")
    ax1.legend(loc = "upper left")
    ax2.legend(loc = "lower right")
    if save:
        plt.savefig("temps.png")
    if disp:
        plt.show()