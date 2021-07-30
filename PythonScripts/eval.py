import requests
import math
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from bisect import bisect_left
from scipy import stats
from mpl_toolkits import mplot3d
import haversine as hs
from statistics import mean

#data = pd.read_excel("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/May_2019/M13_GPS.xlsx", 2, usecols="A:F")
#arannw = pd.DataFrame(data)
#print("arannw: " + str(len(arannw)))
#
#data2 = pd.read_excel("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/May_2019/M13_GPS.xlsx", 1, usecols="A:F")
#rpi1 = pd.DataFrame(data2)
#rpi1 = rpi1.dropna()
#print("rpi1: " + str(len(rpi1)))

#arannwp = plt.plot(arannw.iloc[:,4],arannw.iloc[:,3])
#prpi1 = plt.plot(rpi1.iloc[:,4],rpi1.iloc[:,3])

arannwlong = latcp79
arannwlat = longcp79

rpi1long = latc55
rpi1lat = longc55

len1 = len(rpi1long)
len2 = len(arannwlong)
resultlist = []
index = int(len2/2)

for i in range(len(rpi1long)):

    left = hs.haversine((rpi1lat[i],rpi1long[i]),(arannwlat[index-1],arannwlong[index-1]))
#    print("left: " + str(left))
    middle = hs.haversine((rpi1lat[i],rpi1long[i]),(arannwlat[index],arannwlong[index]))
#    print("middle: " + str(middle))
    right = hs.haversine((rpi1lat[i],rpi1long[i]),(arannwlat[index+1],arannwlong[index+1]))
#    print("right: " + str(right))
    notdone = True
    
    while notdone:
        
        if index == 0 or index == len2:
            notdone = False
            result = index
        
        if middle<left and middle<right:
            notdone = False
            result = index
        
        elif left<middle:
            index = int(index-1)
        
        elif right<middle:
            index = int(index+1)
          
#        print("Index: " + str(index))
        left = hs.haversine((rpi1lat[i],rpi1long[i]),(arannwlat[index-1],arannwlong[index-1]))
#        print("left: " + str(left))
        middle = hs.haversine((rpi1lat[i],rpi1long[i]),(arannwlat[index],arannwlong[index]))
#        print("middle: " + str(middle))
        right = hs.haversine((rpi1lat[i],rpi1long[i]),(arannwlat[index+1],arannwlong[index+1]))
#        print("right: " + str(right))

    
#    print(result)
    resultlist.append((result))
#print(resultlist)
            
graddiffraw = []
graddiffclean = []
for i in range(len1):
    try:
#        diffraw = abs(gradrawrpi1[i]- gradrawarannw[resultlist[i]])
#        diffclean = abs(gradDEMcleanrpi1[i]- gradrawarannw[resultlist[i]])
        diffraw =abs((gradrawc55[i] - gradrawcp79[resultlist[i]])/(gradrawcp79[resultlist[i]]))*100
        diffclean = abs((gradDEMcleanc55[i] - gradrawcp79[resultlist[i]])/ (gradrawcp79[resultlist[i]]))*100
    except ZeroDivisionError:
        diff = 0

    graddiffraw.append(diffraw)
    graddiffclean.append(diffclean)
    
#print(graddiffclean)
meanraw = mean(graddiffraw)
meanclean = mean(graddiffclean)
print("c55")
print("mean raw error: " + str(meanraw))
print("mean clean error: " + str(meanclean))

points = [10,20,50,10,200,300,400,500,1000,2000,3000]
times = [1.108,2.480,7.000,9.430,20.740,30.130,37.640,47.820,93.480,192.720,304.500]

plt.plot(points,times)
plt.xlabel("Datapoints")
plt.ylabel("Time [Sec]")
plt.show()
#



        
        
        
        
        
        
        
        