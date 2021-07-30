#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 23:19:37 2021

@author: madsmoller
"""

import requests
import math
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from bisect import bisect_left
import statistics as st
import haversine as hs



data = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/task_4955_acc_rpi.txt",'\t')
dataframeacc = pd.DataFrame(data)

data = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/task_4955_alt_raw.txt",'\t')
dataframealt = pd.DataFrame(data)

data = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/task_4955_gps_raw.txt",'\t')
dataframegps = pd.DataFrame(data)

data = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/task_4955_odo.txt",'\t')
dataframeodo = pd.DataFrame(data)

data = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/task_4955_speed.txt",'\t')
dataframespeed = pd.DataFrame(data)

data = pd.read_csv("//Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/P79_W_imp_mat.csv", ';', encoding='latin-1')
dataframep79 = pd.DataFrame(data)

def angle(x1,x2,y1,y2, prev):
    try:
        result = math.atan((y2-y1)/(x2-x1))
    except ZeroDivisionError:
        result = prev
    return result
    

def take_closest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       return after
    else:
       return before
   
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

def distance(long,lat):
    distance = []
    currentdist = 0
    for i in range(len(long)):
        if i ==0:
             distance.append(currentdist)
        else:
            currentdist = currentdist + hs.haversine((long[i-1],lat[i-1]),(long[i],lat[i]))
            distance.append(currentdist) 
    return distance
    
long = dataframegps.iloc[:,1].values.tolist()
#print(long)
lat = dataframegps.iloc[:,2].values.tolist()
#print(lat)

result =[]
angleslist = []
speedlist1 = []
ang = 0
for i in range(len(long)):
    if (i==0):
        ang = 0
    else:
        ang = angle(lat[i-1],lat[i],long[i-1],long[i],ang)
    angleslist.append(ang)
    pos = take_closest_index(dataframespeed.iloc[:,0],dataframegps.iloc[i,0])
    speedlist = take_closest_x(dataframespeed.iloc[:,1],pos, 5).values.tolist()
    speed = sum(speedlist)/len(speedlist)  
    speedlist1.append(speed)
    imm = [lat[i],long[i]]
    result.append(imm)
    
#print(result[:10]),ang, speed


#result = take_closest_index(dataframespeed.iloc[:,0],dataframegps.iloc[4000,0])
#resultlist = take_closest_x(dataframespeed.iloc[:,1],result, 25).values.tolist()
#mean = sum(resultlist)/len(resultlist)
#print(mean)

#plt.scatter(dataframegps.iloc[:,1], dataframegps.iloc[:,0])
#plt.show()
#plt.scatter(dataframespeed.iloc[:,1],dataframespeed.iloc[:,0])
#plt.show
#print(dataframespeed.iloc[:,1].values.tolist())
    x = speedlist1
    y = angleslist
    
    mean_x = sum(x)/len(x)
    mean_y = sum(y)/len(y)
    
    cov = sum((a - mean_x) * (b - mean_y) for (a,b) in zip(x,y)) / len(x)
print(cov)

plt.plot(dataframealt.iloc[2675:3330,0].values.tolist(),dataframealt.iloc[2675:3330,1].values.tolist())
plt.title("Elevation From Raw GPS Data")
plt.show()

p79dist1 = distance(dataframep79.iloc[:,1].values.tolist(),dataframep79.iloc[:,2].values.tolist())
p79dist = [x+22.466900707280757 for x in p79dist1]
rawgpsdist = distance(long,lat)
geoapifydist1 = distance(restlat,restlong)
geoapifydist = [x+22.466900707280757 for x in geoapifydist1]


plt.figure(figsize=(10,6))
gpsaltplot = plt.plot(rawgpsdist[2675:3330],dataframealt.iloc[2675:3330,1])
demaltplot = plt.plot(rawgpsdist[2675:3330],altitude[2675:3330])
p79altplot = plt.plot(p79dist, dataframep79.iloc[:,3].values.tolist())
geoapifyplot = plt.plot(geoapifydist,restalt)
plt.legend(['GPS', 'DEM', 'P79', 'Geoapify'])
plt.title("Elevation Comparison")
plt.show()

gpsaltplot = plt.plot(rawgpsdist[2675:3330])
#demaltplot = plt.plot(rawgpsdist[2675:3330])
p79altplot = plt.plot(p79dist)
geoapifyplot = plt.plot(geoapifydist)
plt.show()










    