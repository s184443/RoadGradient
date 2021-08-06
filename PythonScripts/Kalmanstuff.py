import numpy as np
import matplotlib.pyplot as plt
from filterpy.kalman import KalmanFilter
import pandas as pd
from bisect import bisect_left
import math
#import book_plots as bp

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
data = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/task_4955_acc_rpi.txt",'\t')
dataframeacc = pd.DataFrame(data)



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

dk = 1.7276368054350362

f = KalmanFilter(dim_x=6, dim_z=6)

f.x = np.array([12.5,55.5,0.0,0.0,0.0,0.0])

f.u = np.array([0.3])

f.F = np.array([[1.0,  0, (1/111139)* np.cos(f.x[2])*dk,    0, (1/11139)*(1/2)*dk**2,                     0], 
                [  0,1.0, (1/111139)* np.sin(f.x[2])*dk,    0,                     0, (1/11139)*(1/2)*dk**2],
                [  0,  0,                           1.0,    0,                     dk,                   dk],
                [  0,  0,                             0,  1.0,                     0,                     0],
                [  0,  0,                             0,    0,                   1.0,                     0],
                [  0,  0,                             0,    0,                     0,                   1.0]])

f.H = np.array([[1.0,   0,   0,   0,   0,   0],
                [  0, 1.0,   0,   0,   0,   0],
                [  0,   0, 1.0,   0,   0,   0],
                [  0,   0,   0, 1.0,   0,   0],
                [  0,   0,   0,   0, 1.0,   0],
                [  0,   0,   0,   0,   0, 1.0]])

f.P = np.array([[0.0011443667504844985,  -0.00022552009908184255, -0.0942788195121566,  -0.0011889478207327477, -1.6399627988501922e-05,  2.782398352852163e-05],
                [-0.00022552009908184255, 0.00014620020148430957,  0.0519015250456933,   9.864899931927105e-05, -6.684826211867397e-06,  -1.7103219795560057e-05],
                [-0.0942788195121566,     0.0519015250456933,      314.63974502669043,  -0.47463414770347145,   -0.061662589621975225,   -0.09336115170031786],
                [-0.0011889478207327477,  9.864899931927105e-05,  -0.47463414770347145,  0.44474869685705415,   -0.0004606751093717806,   0.0003287050465213762],
                [-1.6399627988501922e-05,-6.684826211867397e-06,  -0.061662589621975225,-0.0004606751093717806,  0.0033635944742029405,  -0.0003958623075952534],
                [2.782398352852163e-05,  -1.7103219795560057e-05, -0.09336115170031786,  0.0003287050465213762, -0.0003958623075952534,   0.0018536842507653932]])

f.R = np.array([[0.8*(1/111139),         0,       0,            0,       0,      0],
                [        0,  0.2*(1/111139),      0,            0,       0,      0],
                [        0,          0,  0.0001,            0,       0,      0],
                [        0,          0,       0, 5*(1/111139),      0,      0],
                [        0,          0,       0,            0,  0.00421,      0],
                [        0,          0,       0,            0,       0, 0.00423]])

f.Q= np.array([[0.0001,        0,        0,      0,    0,    0],
               [  0,      0.0001,        0,      0,    0,    0],
               [  0,             0, 0.0001,      0,    0,    0],
               [  0,             0,        0, 0.0001,    0,    0],
               [  0,             0,        0,      0, 0.0001,    0],
               [  0,             0,        0,      0,    0, 0.0001]])

#f.B = np.array([[0],
#                [0],
#                [0],
#                [dk],
#                [0],
#                [0]])

lat = dataframegps.iloc[:,1].values.tolist()
long = dataframegps.iloc[:,2].values.tolist()
finalspeedlist = []
finalanglist =[]
finalaccxlist = []
finalaccylist = []

result =[]
ang = 0
for i in range(len(long)):
    if (i==0):
        ang = 0
    else:
        ang = angle(lat[i-1],lat[i],long[i-1],long[i],ang)
    finalanglist.append(ang)   
    pos = take_closest_index(dataframespeed.iloc[:,0],dataframegps.iloc[i,0])
    speedlist = take_closest_x(dataframespeed.iloc[:,1],pos, 25).values.tolist()
    speed = sum(speedlist)/len(speedlist) 
    finalspeedlist.append(speed)
    posacc = take_closest_index(dataframeacc.iloc[:,0],dataframegps.iloc[i,0])
    accxlist = take_closest_x(dataframeacc.iloc[:,1],posacc, 25).values.tolist()
    accx = sum(accxlist)/len(accxlist) 
    finalaccxlist.append(accx)
    accylist = take_closest_x(dataframeacc.iloc[:,2],posacc, 25).values.tolist()
    accy = sum(accylist)/len(accylist)
    finalaccylist.append(accy)
    imm = [long[i],lat[i],speed*3.6,ang,accx,accy]
    result.append(imm)

mu, cov, _, _ = f.batch_filter(result)
M, P, C, _ = f.rts_smoother(mu, cov)


plt.figure(figsize=(10,6))
p79 = plt.plot(dataframep79.iloc[:,2].values.tolist(),dataframep79.iloc[:,1].values.tolist(),'k')
raw = plt.plot(dataframegps.iloc[2675:3330,2].values.tolist(),dataframegps.iloc[2675:3330,1].values.tolist(),'g')
#p79nwp = plt.plot(p79nw.iloc[900:1245,4],p79nw.iloc[900:1245,3])
#p5587 = plt.plot(d5587gps.iloc[1179:1310,2],d5587gps.iloc[1179:1310,1])
kalman = plt.plot(mu[2675:3330,0],mu[2675:3330,1], 'm')
smooth = plt.plot(M[2675:3330,0], M[2675:3330,1], 'c--')
#geoapify = plt.plot(long,lat)
#plt.legend(['P79','raw','Kalman Filter','RTS Smoother','Geoapify'])
plt.title("Route Comparison")
#plt.xlim([12.54226, 12.5588])
#plt.ylim([55.698, 55.7077])
#plt.xlim([12.54528, 12.5517])
#plt.ylim([55.698, 55.702])
#plt.xlim([12.5508, 12.5534])
#plt.ylim([55.7033, 55.7073])
plt.ylabel('Latitude')
plt.xlabel('Longitude')
plt.legend(['p79','c55','kalman','rts'])
plt.show()




