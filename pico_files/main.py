import math
import os
import time
from imu import MPU6050
from machine import Pin, I2C

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)
filename = "data_store.csv"
begin_time = time.ticks_us()

def measurement(show_readout=True):
    ax=round(imu.accel.x,2) # g's of acceleration
    ay=round(imu.accel.y,2) 
    az=round(imu.accel.z,2)
    gx=round(imu.gyro.x) # deg/s
    gy=round(imu.gyro.y)
    gz=round(imu.gyro.z)
    tem=round(imu.temperature,2)
    if show_readout:
        print(ax,"\t",ay,"\t",az,"\t",gx,"\t",gy,"\t",gz,"\t",tem,"        ",end="\r")
    return [ax,ay,az,gx,gy,gz,tem]

def write_data(data,filename):
    file_obj = open(filename,"a")
    file_obj.write(str(data)+",\n")
    file_obj.close()

def evaluate_measurement_performance(sample_size,write2file=False):
    i = 0
    m_time = 0.0
    while i < sample_size:
        start = time.ticks_us()
        data = measurement()
        if write2file:
            write_data(data,filename)
        end = time.ticks_us()
        m_time += time.ticks_diff(end,start)
        i += 1
    m_time /= i
    print("Average Measurement Time: ",m_time*10**(-3),"ms, N =",i)
    return m_time

dt = evaluate_measurement_performance(100,write2file=True)*10**(-6)
os.remove("data_store.csv")

step = 0
while True:
    step += 1
    m_vals = measurement(True)
    data = [step,m_vals,dt]
    write_data(data,filename)