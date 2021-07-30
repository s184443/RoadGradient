import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

data = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/task_4955_gps_raw.txt",'\t')
dataframegps = pd.DataFrame(data)
data = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/task_4957_gps_raw.txt",'\t')
dataframegps57 = pd.DataFrame(data)
data = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/task_4959_gps_raw.txt",'\t')
dataframegps59 = pd.DataFrame(data)
data = pd.read_csv("//Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/P79_W_imp_mat.csv", ';', encoding='latin-1')
dataframep79 = pd.DataFrame(data)
# Supress scientific notation when printing NumPy arrays
np.set_printoptions(precision=9,suppress=True)
 
# A matrix
# 3x3 matrix -> number of states x number of states matrix
# Expresses how the state of the system [x,y,yaw] changes 
A_k_minus_1 = np.array([[1.0,  0,   0],
                        [  0,1.0,   0],
                        [  0,  0, 1.0]])
 
# Noise applied to the forward kinematics (calculation
# of the estimated state at time k from the state
# transition model of the mobile robot). This is a vector
# with the number of elements equal to the number of states
process_noise_v_k_minus_1 = np.array([0.0001,0.0001,0.003])
     
# State model noise covariance matrix Q_k
# When Q is large, the Kalman Filter tracks large changes in 
# the sensor measurements more closely than for smaller Q.
# Q is a square matrix that has the same number of rows as states.
Q_k = np.array([[0.00001,   0,   0],
                [  0, 0.000001,   0],
                [  0,   0, 0.00100]])
                 
# Measurement matrix H_k
H_k = np.array([[1.0,  0,   0],
                [  0,1.0,   0],
                [  0,  0, 1.0]])
                         
# Sensor measurement noise covariance matrix R_k
# Has the same number of rows and columns as sensor measurements.
# If we are sure about the measurements, R will be near zero.
R_k = np.array([[0.00000000001,   0,    0],
                [  0, 0.00000000001,    0],
                [  0,    0, 0.01]])  
                 
# Sensor noise. This is a vector with the
# number of elements equal to the number of sensor measurements.
sensor_noise_w_k = np.array([0.00006,0.00006,0.00005])

estimates = []

def angle(x1,x2,y1,y2, prev):
    try:
        result = math.atan((y2-y1)/(x2-x1))
    except ZeroDivisionError:
        result = prev
    return result
    
 
#Determines B matrix. 
def getB(theta, deltak):
    B = np.array([[np.cos(theta)*deltak, 0],
                  [np.sin(theta)*deltak, 0],
                  [0, deltak]])
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
             
    #print(f'State Estimate Before EKF={state_estimate_k}')
             
    # Predict the state covariance estimate based on the previous
    # covariance and some noise
    P_k = A_k_minus_1 @ P_k_minus_1 @ A_k_minus_1.T + (
            Q_k)

    # Calculate the difference between the actual sensor measurements
    # at time k minus what the measurement model predicted 
    # the sensor measurements would be for the current timestep k.
    measurement_residual_y_k = z_k_observation_vector - (
            (H_k @ state_estimate_k) + (
            sensor_noise_w_k))
 
    #print(f'Observation={z_k_observation_vector}')
             
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
    #print(f'State Estimate After EKF={state_estimate_k}')
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
            
        imm = [lat[i],long[i],ang]
        result.append(imm)
    
 
    z_k = result 
#np.array([[12.54293142,55.69827573,0.0000000000], # k=1
#                    [12.54293044,55.69827648,-37.42705136], # k=2
#                    [12.54292946,55.69827722,-37.05652818], # k=3
#                    [12.54292847,55.69827797,-37.14668669], # k=4
#                    [12.54292749,55.69827871,-37.05652818], # k=5
#                    [12.54292651,55.69827946,-37.42705136], # k=6
#                    [12.54292553,55.69828020,-37.05652818], # k=7
#                    [12.54292454,55.69828095,-37.14668669], # k=8
#                    [12.54292356,55.69828169,-37.05652818], # k=9
#                    [12.54292258,55.69828244,-37.42705136], # k=10
#                    [12.54292160,55.69828318,-37.05652818], # k=11
#                    [12.54292062,55.69828393,-37.42705136], # k=12
#                    [12.54291963,55.69828467,-36.77718611], # k=13
#                    [12.54291865,55.69828542,-37.42705136], # k=14
#                    [12.54291767,55.69828616,-37.05652818], # k=15
#                    [12.54291669,55.69828691,-37.42705136], # k=16
#                    [12.54291571,55.69828765,-37.05652818], # k=17
#                    [12.54291473,55.69828840,-37.42705136], # k=18
#                    [12.54291375,55.69828914,-37.05652818], # k=19
#                    [12.54291276,55.69828989,-37.14668669], # k=20
#                    [12.54291178,55.69829063,-37.05652818], # k=21 
#                    [12.54291080,55.69829138,-37.42705136], # k=22
#                    [12.54290982,55.69829212,-37.05652818], # k=23
#                    [12.54290884,55.69829287,-37.42705136]])# k=24

    
    # The estimated state vector at time k-1 in the global reference frame.
    # [x_k_minus_1, y_k_minus_1, yaw_k_minus_1]
    # [meters, meters, radians]
    state_estimate_k_minus_1 = np.array([12.5,55.5,0.0])
    control_vector_k_minus_1 = np.array([8.5,0.0])
    P_k_minus_1 = np.array([[0.000001,  0,   0],
                            [  0,0.000001,   0],
                            [  0,  0, 0.001000]])
                             
    # Start at k=1 and go through each of the 5 sensor observations, 
    # one at a time.
    for k, obs_vector_z_k in enumerate(z_k,start=1):
     
        # Print the current timestep
        #print(f'Timestep k={k}')  
         
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
         
        # Print a blank line
        #print()
    #print(estimates)
 
# Program starts running here with the main method  
main()
long = []
lat = []

for i in estimates:
    long.append(i[0])
    lat.append(i[1])
#print(long)
#print(lat)
#print(dataframegps.iloc[1,1:].values.tolist())
#print(dataframegps57.iloc[1,1:].values.tolist())
#print(dataframegps59.iloc[1,1:].values.tolist())
#print(str(lat[2500])+','+str(long[2500]))
#print(len(dataframep79.iloc[:,2].values.tolist()))


plt.plot(dataframep79.iloc[:,2].values.tolist(),dataframep79.iloc[:,1].values.tolist())
plt.show
    
plt.plot(long[2675:3330],lat[2675:3330])
plt.show
    
#plt.plot(dataframegps.iloc[2675:3330,2].values.tolist(),dataframegps.iloc[2675:3330,1].values.tolist())
#plt.show
    
#plt.plot(dataframegps57.iloc[:,2].values.tolist(),dataframegps57.iloc[:,1].values.tolist())
#plt.show
    
#plt.plot(dataframegps59.iloc[1000:3000,2].values.tolist(),dataframegps59.iloc[1000:3000,1].values.tolist())
#plt.show
#dt = dataframep79.iloc[:,2].values.tolist()  
#dt55 = dataframegps.iloc[2675:3330,2].values.tolist()
#print(len(dt)) 
#print(len(dt55))
#
#meanlist = []
#for i in range(138,len(dt),138):
#    mean = sum(dt[i-138:i])/138
#    meanlist.append(mean)
#print(len(meanlist))



























