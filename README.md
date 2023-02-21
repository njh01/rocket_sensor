# A Repositiory for code to post-process IMU data

## kfilter.py
A class implementing a standard extended kalman filter

## filter_app.py
An app to run a kalman filter implementation and plot the output

## dcm.py
A rotation matrix class for translating body coordinates of an IMU into the reference frame

## CSV Files

Uploaded .csv files contain real imu data. 

`data_store.csv` contains stationary IMU data for calibration

`data_store_1_maneuver.csv` contains IMU data for a sensor that was lifted up about 25 cm for a few second then returned to the table

`data_store_turn90.csv` contains IMU data for a sensor that was lifted up about 25 cm, turned 90 degrees, then returned to the table

`.png` files contain plots of raw and filtered output