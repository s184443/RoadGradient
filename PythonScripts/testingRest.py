#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 14:01:40 2021

@author: madsmoller
"""
import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time

def graph(data,yName):
    plt.plot(data)
    plt.ylabel(yName)
    plt.show()
    
def FindLong(data):
    longitude = []
    for i in data:
        longitude.append(float(i[0]))
    return longitude

def FindLat(data):
    latitude = []
    for i in data:
        latitude.append(float(i[1]))
    return latitude

def FindAlt(data):
    altitude = []
    for i in data:
        altitude.append(float(i[2]))
    return altitude

def RestCall(token, request):
    request = "https://api.dataforsyningen.dk/RestGeokeys_v2?elevationmodel=dtm&method=geopmulti&geop={0}&georef=EPSG:4326&token={1}".format(request,token)
#    print(request)
    response = requests.get(request)
    datastore = json.dumps(response.json())
    json_string = json.loads(datastore)
#    print(json_string)
    geopmulti = json_string["geopmulti"]
    
    eledata = []
    for i in geopmulti:
        eledata.append(i["geop"])
        
    orderedData = []
    for i in eledata:
        x = i.split(",")
        orderedData.append(x)
    return orderedData

def Request(dataframe,start,end):
    latdata = dataframe.iloc[start:end,1].values.tolist()
    longdata = dataframe.iloc[start:end,2].values.tolist()
    revpairs = []
    for i in range(len(latdata)):
        revpairs.append([longdata[i],latdata[i]])
    
    for i in range(len(revpairs)):
        revpairs[i] = ','.join(str(e) for e in revpairs[i]) 
    return revpairs
    

token = "e9aec1f926aa2482b16acad49cb11e83"
path = '/Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/task_4955_gps_raw.txt'
request = "12.54261016845703125,55.722789764404296875"
requestThorsbakke = '12.042551240309155,55.95146839187394%3B12.042433018657173,55.95153458352012%3B12.041558178432517,55.95242154066077%3B12.0410616474942,55.952871630542326%3B12.040470539234294,55.953467329692764%3B12.039690276331223,55.95424834358085%3B12.038437126735781,55.95545292740055%3B12.036900245260032,55.95697514995309%3B12.03571802871629,55.958113468611195%3B12.034464879205295,55.959331167744644%3B12.03321172967931,55.96060176952655%3B12.031627559536988,55.962137024319034%3B12.030327121350219,55.964029539112985%3B12.029381348122014,55.96600136166522%3B12.029286770797011,55.9673511419815%3B12.029854234726516,55.96903168497185%3B12.028199131598788,55.96949481396548%3B12.0250780799865,55.97024904065848%3B12.023446621189168,55.97102971596032%3B12.02214618301738,55.97046075077163'


data = pd.read_csv(path,'\t')
dataframe = pd.DataFrame(data)
latdata = dataframe.iloc[250:300,1].values.tolist()
longdata = dataframe.iloc[250:300,2].values.tolist()
revpairs = []
for i in range(len(latdata)):
    revpairs.append([longdata[i],latdata[i]])

for i in range(len(revpairs)):
    revpairs[i] = ','.join(str(e) for e in revpairs[i])  


#revpairs = Request(dataframe, 250,300)
#request = '%3B'.join(revpairs)

#print(len(dataframe.iloc[:,1]))
findata = []
for i in range(50,len(dataframe.iloc[:,1])+50,50):
    if (i>len(dataframe.iloc[:,1])):
        i = len(dataframe.iloc[:,1])

    revpairs = Request(dataframe, i-50,i)
    request = '%3B'.join(revpairs)

    data = RestCall(token, request)
    findata.append(data)
    print(data)

list1 = []
for i in findata:
    list1 += i
    


    
#revpairs = Request(dataframe, 0,50)
#request = '%3B'.join(revpairs)
#data = RestCall(token, request)
#print(data)
#    
#revpairs = Request(dataframe, 50,100)
#request = '%3B'.join(revpairs)
#data = RestCall(token, request)
#print(data)
#    
#revpairs = Request(dataframe, 100,150)
#request = '%3B'.join(revpairs)
#data = RestCall(token, request)
#print(data)

altitude = FindAlt(list1)
plt.plot(dataframe.iloc[2675:3330,0].values.tolist(),altitude[2675:3330])
plt.title("Elevation From Danmarks Højdemodel")
plt.show()

plt.plot(rawgpsdist[2675:3330],altitude[2675:3330])
plt.title("Elevation From Danmarks Højdemodel")
plt.show()


    
#data = RestCall(token, request)
#longitude = FindLong(data)
##print(longitude)
#latitude = FindLat(data)
##print(latitude)
#altitude = FindAlt(data)
##print(altitude)
#graph(altitude, "Elevation")















