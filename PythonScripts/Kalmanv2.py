#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 09:27:30 2021

@author: madsmoller
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from bisect import bisect_left

data = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/task_4955_gps_raw.txt",'\t')
dataframegps = pd.DataFrame(data)
data = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/task_4957_gps_raw.txt",'\t')
dataframegps57 = pd.DataFrame(data)
data = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/task_4959_gps_raw.txt",'\t')
dataframegps59 = pd.DataFrame(data)
data = pd.read_csv("//Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/P79_W_imp_mat.csv", ';', encoding='latin-1')
dataframep79 = pd.DataFrame(data)
data = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/task_4955_speed.txt",'\t')
dataframespeed = pd.DataFrame(data)

# Supress scientific notation when printing NumPy arrays
np.set_printoptions(precision=15,suppress=True)

state_estimate_k_minus_1 = np.array([12.5,55.5,0.0])
k = 1
dk = 1.7276368054350362*10**(-3)

# A matrix
# 3x3 matrix -> number of states x number of states matrix
# Expresses how the state of the system [x,y,yaw] changes 
A_k_minus_1 = np.array([[1.0,  0,  (1/111.139)* np.cos(state_estimate_k_minus_1[2])*dk, 0],
                        [  0,1.0,(1/111.139)* np.sin(state_estimate_k_minus_1[2])*dk, 0],
                        [  0,  0, 1.0, 0],
                        [  0,  0,  0,  1.0]])
 
# Noise applied to the forward kinematics (calculation
# of the estimated state at time k from the state
# transition model of the mobile robot). This is a vector
# with the number of elements equal to the number of states
process_noise_v_k_minus_1 = np.array([0.0001,0.0001,0.0003,0.001])
     
# State model noise covariance matrix Q_k
# When Q is large, the Kalman Filter tracks large changes in 
# the sensor measurements more closely than for smaller Q.
# Q is a square matrix that has the same number of rows as states.
Q_k = np.array([[0.0011443667504844985,  -0.00022552009908184255, -0.0942788195121566, -0.0011889478207327477],
                [-0.00022552009908184255, 0.00014620020148430957,  0.0519015250456933,  9.864899931927105e-05],
                [-0.0942788195121566,     0.0519015250456933,      314.63974502669043, -0.47463414770347145],
                [-0.0011889478207327477,  9.864899931927105e-05,  -0.47463414770347145, 0.44474869685705415]])
                 
# Measurement matrix H_k
H_k = np.array([[1.0,  0,   0, 0],
                [  0,1.0,   0, 0],
                [  0,  0, 1.0, 0],
                [  0,  0,   0, 1]])
                         
# Sensor measurement noise covariance matrix R_k
# Has the same number of rows and columns as sensor measurements.
# If we are sure about the measurements, R will be near zero.
R_k = np.array([[(1/111139),   0,    0, 0],
                [  0, (1/111139),    0, 0],
                [  0, 0, 0.0001, 0 ],
                [  0, 0, 0, 10*(1/111139)]])  
                 
# Sensor noise. This is a vector with the
# number of elements equal to the number of sensor measurements.
sensor_noise_w_k = np.array([0.00005,0.00005,5,0.0005])

estimates = []

def angle(x1,x2,y1,y2, prev):
    try:
        result = math.atan((y2-y1)/(x2-x1))
    except ZeroDivisionError:
        result = prev
    return result

def take_closest_x(myList,pos, x):
    if pos == 0:
        return myList[:x*2]
    if pos == len(myList):
        return myList[-x*2:]
    if pos-x < 0:
        left = pos-x
        return myList[:pos+x-left]
    if pos+x >len(myList):
        right = pos+x-len(myList)
        return myList[pos-x-right]
    else:
        return myList[pos-x:pos+x]
  
    
def take_closest_index(myList, myNumber):
    pos = bisect_left(myList, myNumber)
    return pos
  
    


#def getB(theta, deltak):
#    B = np.array([[(1/111139)*1/2 * np.cos(theta)*(deltak**2), 0],
#                  [(1/111139)*1/2 * np.sin(theta)*(deltak**2), 0],
#                  [deltak,                          0],
#                  [0,                          deltak]])
#    return B
 
#Determines B matrix. 
def getB(theta, deltak):
    B = np.array([[0, 0],
                  [0, 0],
                  [0, 0],
                  [0, 0]])
    return B
 
#Inputs:  Observed measurement vector
#         Initial state estimate
#         Initial control vector
#         Initial state covariance matrix
#         Time interval in seconds    
#Outputs: x_k, State estimate at time k
#         p_k, state covariance matrix at time k    
def ekf(z_k_observation_vector, state_estimate_k_minus_1, 
        control_vector_k_minus_1, P_k_minus_1, dk):
    
    state_estimate_k = A_k_minus_1 @ (
            state_estimate_k_minus_1) + (
            getB(state_estimate_k_minus_1[2],dk)) @ (
            control_vector_k_minus_1) + (
            process_noise_v_k_minus_1)
             
#    print(f'State Estimate Before EKF={state_estimate_k}')
             
    # Predict the state covariance estimate based on the previous
    # covariance and some noise
    P_k = A_k_minus_1 @ P_k_minus_1 @ A_k_minus_1.T + (Q_k)

    # Calculate the difference between the actual sensor measurements
    # at time k minus what the measurement model predicted 
    # the sensor measurements would be for the current timestep k.
    measurement_residual_y_k = z_k_observation_vector - (
            (H_k @ state_estimate_k) + (
            sensor_noise_w_k))
 
#    print(f'Observation={z_k_observation_vector}')
             
    # Calculate the measurement residual covariance
    S_k = H_k @ P_k @ H_k.T + R_k
         
    # Calculate the near-optimal Kalman gain
    # We use pseudoinverse since some of the matrices might be
    # non-square or singular.
    K_k = P_k @ H_k.T @ np.linalg.pinv(S_k)
         
    # Calculate an updated state estimate for time k
    state_estimate_k = state_estimate_k + (K_k @ measurement_residual_y_k)
     
    # Update the state covariance estimate for time k
    P_k = P_k - (K_k @ H_k @ P_k)
     
    # Print the best (near-optimal) estimate of the current state of the robot
#    print(f'State Estimate After EKF={state_estimate_k}')
    estimates.append(state_estimate_k.tolist())
 
    # Return the updated state and covariance estimates
    return state_estimate_k, P_k
     
def main():
 
    k = 1
    dk = 1.7276368054350362
    
    long = dataframegps.iloc[:,1].values.tolist()
    #print(long)
    lat = dataframegps.iloc[:,2].values.tolist()
    #print(lat)

    result =[]
    ang = 0
    for i in range(len(long)):
        if (i==0):
            ang = 0
        else:
            ang = angle(lat[i-1],lat[i],long[i-1],long[i],ang)
            
        pos = take_closest_index(dataframespeed.iloc[:,0],dataframegps.iloc[i,0])
        speedlist = take_closest_x(dataframespeed.iloc[:,1],pos, 25).values.tolist()
        speed = sum(speedlist)/len(speedlist) 
        imm = [lat[i],long[i],speed,ang]
        result.append(imm)
    
 
    z_k = result 
#np.array([[12.54293142,55.69827573,0.0000000000], # k=1
#                    [12.54293044,55.69827648,-37.42705136], # k=2


    
    # The estimated state vector at time k-1 in the global reference frame.
    # [x_k_minus_1, y_k_minus_1, yaw_k_minus_1]
    # [meters, meters, radians]
    state_estimate_k_minus_1 = np.array([z_k[0][0],z_k[0][1],z_k[0][2],z_k[0][3]])
    control_vector_k_minus_1 = np.array([0.0,0.0])
    P_k_minus_1 = np.array([[0.000001,  0,   0,  0     ],
                            [  0,0.000001,   0,  0     ],
                            [  0,  0, 0.001000,  0     ],
                            [  0,  0, 0,         0.0010]])
                             
    # Start at k=1 and go through each of the 5 sensor observations, 
    # one at a time.
    for k, obs_vector_z_k in enumerate(z_k,start=1):
     
        # Print the current timestep
#        print(f'Timestep k={k}')  
         
        # Run the Extended Kalman Filter and store the 
        # near-optimal state and covariance estimates
        optimal_state_estimate_k, covariance_estimate_k = ekf(
            obs_vector_z_k, # Most recent sensor measurement
            state_estimate_k_minus_1, # Our most recent estimate of the state
            control_vector_k_minus_1, # Our most recent control input
            P_k_minus_1, # Our most recent state covariance matrix
            dk) # Time interval
         
        # Get ready for the next timestep by updating the variable values
        state_estimate_k_minus_1 = optimal_state_estimate_k
        P_k_minus_1 = covariance_estimate_k
         
#         Print a blank line
#        print()
    #print(estimates)
 
# Program starts running here with the main method  
main()

long = []
lat = []

for i in estimates:
    long.append(i[0])
    lat.append(i[1])
print(long)
print(lat)
print(dataframegps.iloc[1,1:].values.tolist())
print(dataframegps57.iloc[1,1:].values.tolist())
print(dataframegps59.iloc[1,1:].values.tolist())
print(str(lat[2500])+','+str(long[2500]))
print(len(dataframep79.iloc[:,2].values.tolist()))

plt.figure(figsize=(10,6))
#plt.plot(dataframep79.iloc[:,37].values.tolist(),dataframep79.iloc[:,3].values.tolist())
#plt.title("Elevation From P79")
#plt.show
    
plt.plot(long[2675:3330],lat[2675:3330])
plt.show
    
plt.plot(dataframegps.iloc[2675:3330,2].values.tolist(),dataframegps.iloc[2675:3330,1].values.tolist())
plt.show
    
#plt.plot(dataframegps57.iloc[:,2].values.tolist(),dataframegps57.iloc[:,1].values.tolist())
#plt.show
    
#plt.plot(dataframegps59.iloc[1000:3000,2].values.tolist(),dataframegps59.iloc[1000:3000,1].values.tolist())
#plt.show
dt = dataframep79.iloc[:,2].values.tolist()  
dt55 = dataframegps.iloc[2675:3330,2].values.tolist()
print(len(dt)) 
print(len(dt55))

meanlist = []
for i in range(138,len(dt),138):
    mean = sum(dt[i-138:i])/138
    meanlist.append(mean)
print(len(meanlist))