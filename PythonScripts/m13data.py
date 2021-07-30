
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

def RestCall(token, request):
    request = "https://api.dataforsyningen.dk/RestGeokeys_v2?elevationmodel=dtm&method=geopmulti&geop={0}&georef=EPSG:4326&token={1}".format(request,token)
    print(request)
    response = requests.get(request)
    datastore = json.dumps(response.json())
    json_string = json.loads(datastore)
    print(json_string)
    geopmulti = json_string["geopmulti"]
    
    eledata = []
    for i in geopmulti:
        eledata.append(i["geop"])
        
    orderedData = []
    for i in eledata:
        x = i.split(",")
        orderedData.append(x)
    return orderedData

def Request(lat, long):
    revpairs = []
    for i in range(len(lat)):
        revpairs.append([long[i],lat[i]])
    
    for i in range(len(revpairs)):
        revpairs[i] = ','.join(str(e) for e in revpairs[i]) 
    return revpairs

def FullRequest(revpairs):
    findata = []
    for i in range(50,len(revpairs)+50,50):
        if (i>len(revpairs)):
            x = len(revpairs)
            request = '%3B'.join(revpairs[i-50:len(revpairs)])
    
        request = '%3B'.join(revpairs[i-50:i])
    
        data = RestCall(token, request)
        findata.append(data)
        print(data)
    list1 = []
    for i in findata:
        list1 += i
    return list1

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

def Distance(long,lat):
    distance = []
    currentdist = 0
    for i in range(len(long)):
        if i ==0:
             distance.append(currentdist)
        else:
            currentdist = currentdist + hs.haversine((long[i-1],lat[i-1]),(long[i],lat[i]))
            distance.append(currentdist) 
    return distance

def Gradient(alt, dist):
    gradient = []
    for i in range(len(alt)):
        if i == 0:
            gradient.append(0)
        else:
            try:
                gradient.append(((alt[i]-alt[i-1])/((dist[i]-dist[i-1])*1000))*100)
            except ZeroDivisionError:
                gradient.append(0)

    return gradient

def Gradientclean(alt, dist):
    gradient = []
    threshold = 2
    for i in range(len(alt)):
        if i == 0:
            gradient.append(0)
        else:
            try:
                gradient.append(((alt[i]-alt[i-1])/((dist[i]-dist[i-1])*1000))*100)
            except ZeroDivisionError:
                gradient.append(0)
    z = np.abs(stats.zscore(gradient))
#    print(z)
    outlierIndex = np.where(z>threshold)
    print(outlierIndex)
    for i in outlierIndex[0]:
        gradient[i] = gradient[i-1]
    return gradient

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
        return myList[pos-x-right:]
    else:
        return myList[pos-x:pos+x]
  

def take_closest_index(myList, myNumber):
    pos = bisect_left(myList, myNumber)
    return pos

def angle(x1,x2,y1,y2, prev):
    try:
        result = math.atan((y2-y1)/(x2-x1))
    except ZeroDivisionError:
        result = prev
    return result

token = "e9aec1f926aa2482b16acad49cb11e83"

data = pd.read_excel("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/May_2019/M13_GPS.xlsx", 2, usecols="A:F")
arannw = pd.DataFrame(data)
print("arannw: " + str(len(arannw)))

data1 = pd.read_excel("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/May_2019/M13_GPS.xlsx", 3, usecols="A:F")
p79nw= pd.DataFrame(data1)
print("p79nw: " + str(len(p79nw)))

data2 = pd.read_excel("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/May_2019/M13_GPS.xlsx", 1, usecols="A:F")
rpi1 = pd.DataFrame(data2)
rpi1 = rpi1.dropna()
print("rpi1: " + str(len(rpi1)))

data3 = pd.read_excel("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/May_2019/M13_GPS.xlsx", 1, usecols="H:M")
rpi2 = pd.DataFrame(data3)
rpi2 = rpi2.dropna()
print("rpi2: " + str(len(rpi2)))

data4 = pd.read_excel("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/May_2019/M13_GPS.xlsx", 1, usecols="O:T")
rpi3 = pd.DataFrame(data4)
rpi3 = rpi3.dropna()
print("rpi3: " + str(len(rpi3)))

data5 = pd.read_excel("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/May_2019/M13_GPS.xlsx", 1, usecols="V:AA")
rpi4 = pd.DataFrame(data5)
rpi4 = rpi4.dropna()
print("rpi4: " + str(len(rpi4)))

data6 = pd.read_excel("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/May_2019/M13_GPS.xlsx", 1, usecols="AC:AH")
rpi5 = pd.DataFrame(data6)
rpi5 = rpi5.dropna()
print("rpi5: " + str(len(rpi5)))

data7 = pd.read_excel("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/May_2019/M13_GPS.xlsx", 1, usecols="AJ:AO")
rpi6 = pd.DataFrame(data7)
rpi6 = rpi6.dropna()
print("rpi6: " + str(len(rpi6)))


data8 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5587_gps_raw.txt",'\t')
d5587gps = pd.DataFrame(data8)
print("d5587: " + str(len(d5587gps)))

data8 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5587_speed.txt",'\t')
d5587spd = pd.DataFrame(data8)
print("d5587: " + str(len(d5587spd)))

data8 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5587_acc_rpi.txt",'\t')
d5587acc = pd.DataFrame(data8)
print("d5587: " + str(len(d5587acc)))


data9 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5589_gps_raw.txt",'\t')
d5589gps = pd.DataFrame(data9)
print("d5589: " + str(len(d5589gps)))

data9 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5589_speed.txt",'\t')
d5589spd = pd.DataFrame(data9)
print("d5589: " + str(len(d5589spd)))

data9 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5589_acc_rpi.txt",'\t')
d5589acc = pd.DataFrame(data9)
print("d5589: " + str(len(d5589acc)))


data10 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5592_gps_raw.txt",'\t')
d5592gps = pd.DataFrame(data10)
print("d5592: " + str(len(d5592gps)))

data10 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5592_speed.txt",'\t')
d5592spd = pd.DataFrame(data10)
print("d5592: " + str(len(d5592spd)))

data10 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5592_acc_rpi.txt",'\t')
d5592acc = pd.DataFrame(data10)
print("d5592: " + str(len(d5592acc)))


data11 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5597_gps_raw.txt",'\t')
d5597gps = pd.DataFrame(data11)
print("d5597: " + str(len(d5597gps)))

data11 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5597_speed.txt",'\t')
d5597spd = pd.DataFrame(data11)
print("d5597: " + str(len(d5597spd)))

data11 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5597_acc_rpi.txt",'\t')
d5597acc = pd.DataFrame(data11)
print("d5597: " + str(len(d5597acc)))

data12 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/task_4955_gps_raw.txt",'\t')
city55 = pd.DataFrame(data12)
print("city55: " + str(len(city55)))

data13 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/task_4955_alt_raw.txt",'\t')
city55alt = pd.DataFrame(data13)
print("city55alt: " + str(len(city55alt)))

data14 = pd.read_csv("//Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/P79_W_imp_mat.csv", ';', encoding='latin-1')
cityp79 = pd.DataFrame(data14)
print("cityp79: " + str(len(cityp79)))


print("p79nw: " + str(len(p79nw)))
print("arannw: " + str(len(arannw)))
print("rpi1: " + str(len(rpi1)))
print("rpi2: " + str(len(rpi2)))
print("rpi3: " + str(len(rpi3)))
print("rpi4: " + str(len(rpi4)))
print("rpi5: " + str(len(rpi5)))
print("rpi6: " + str(len(rpi6)))
#print("d5587: " + str(len(d5587gps)))
#print("d5587: " + str(len(d5587spd)))
#print("d5589: " + str(len(d5589gps)))
#print("d5589: " + str(len(d5589spd)))
#print("d5592: " + str(len(d5592gps)))
#print("d5592: " + str(len(d5592spd)))
#print("d5597: " + str(len(d5597gps)))
#print("d5597: " + str(len(d5597spd)))
print("city55: " + str(len(city55)))
print("cityp79: " + str(len(cityp79)))

#Plots for the whole route:
plt.figure(figsize=(10,6))
#p79nwp = plt.plot(p79nw.iloc[:,4],p79nw.iloc[:,3])
arannwp = plt.plot(arannw.iloc[:,4],arannw.iloc[:,3])
#prpi1 = plt.plot(rpi1.iloc[:,4],rpi1.iloc[:,3])
#prpi2 = plt.plot(rpi2.iloc[:,4],rpi2.iloc[:,3])
#prpi3 = plt.plot(rpi3.iloc[:,4],rpi3.iloc[:,3])
prpi4 = plt.plot(rpi4.iloc[:,4],rpi4.iloc[:,3])
#prpi5 = plt.plot(rpi5.iloc[:,4],rpi5.iloc[:,3])
#prpi6 = plt.plot(rpi6.iloc[:,4],rpi6.iloc[:,3])
#p5587 = plt.plot(d5587gps.iloc[:,2],d5587gps.iloc[:,1])
#p5589 = plt.plot(d5589gps.iloc[:,2],d5589gps.iloc[:,1])
#p5592 = plt.plot(d5592gps.iloc[:,2],d5592gps.iloc[:,1])
#p5597 = plt.plot(d5597gps.iloc[:,2],d5597gps.iloc[:,1])
#plt.legend(['P79NW','aranNW','rpi1','rpi2','rpi3','rpi4','rpi5','rpi6','p5587','p5589','p5592','p5597'])
plt.show()

#Plots for a spicific part of the route:
plt.figure(figsize=(10,6))
#p79nwp = plt.plot(p79nw.iloc[900:1245,4],p79nw.iloc[900:1245,3])
arannwp = plt.plot(arannw.iloc[900:1250,4],arannw.iloc[900:1250,3])
prpi1 = plt.plot(rpi1.iloc[128:166,4],rpi1.iloc[128:166,3])
prpi2 = plt.plot(rpi2.iloc[111:166,4],rpi2.iloc[111:166,3])
prpi3 = plt.plot(rpi3.iloc[104:,4],rpi3.iloc[104:,3])
prpi4 = plt.plot(rpi4.iloc[111:166,4],rpi4.iloc[111:166,3])
prpi5 = plt.plot(rpi5.iloc[111:,4],rpi5.iloc[111:,3])
prpi6 = plt.plot(rpi6.iloc[114:,4],rpi6.iloc[114:,3])
#p5587 = plt.plot(d5587gps.iloc[1179:1310,2],d5587gps.iloc[1179:1310,1])
#p5589 = plt.plot(d5589gps.iloc[1179:1310,2],d5589gps.iloc[1179:1310,1])
#p5592 = plt.plot(d5592gps.iloc[1391:1510,2],d5592gps.iloc[1391:1510,1])
#p5597 = plt.plot(d5597gps.iloc[152:280,2],d5597gps.iloc[152:280,1])
plt.legend(['aranNW','rpi1','rpi2','rpi3','rpi4','rpi5','rpi6'])
plt.show()

#Plots for speed:
plt.figure(figsize=(10,6))
#p79nwp = plt.plot(p79nw.iloc[:,4],p79nw.iloc[:,3])
#arannwp = plt.plot(arannw.iloc[:,4],arannw.iloc[:,3])
#prpi1 = plt.plot(rpi1.iloc[:,4],rpi1.iloc[:,3])
#prpi2 = plt.plot(rpi2.iloc[:,4],rpi2.iloc[:,3])
#prpi3 = plt.plot(rpi3.iloc[:,4],rpi3.iloc[:,3])
#prpi4 = plt.plot(rpi4.iloc[:,4],rpi4.iloc[:,3])
#prpi5 = plt.plot(rpi5.iloc[:,4],rpi5.iloc[:,3])
#prpi6 = plt.plot(rpi6.iloc[:,4],rpi6.iloc[:,3])
#p5587 = plt.plot(d5587spd.iloc[:,0],d5587spd.iloc[:,1])
#p5589 = plt.plot(d5589spd.iloc[:,0],d5589spd.iloc[:,1])
#p5592 = plt.plot(d5592spd.iloc[:,0],d5592spd.iloc[:,1])
#p5597 = plt.plot(d5597spd.iloc[:,0],d5597spd.iloc[:,1])
#plt.legend(['P79NW','aranNW','rpi1','rpi2','rpi3','rpi4','rpi5','rpi6','p5587','p5589','p5592','p5597'])
plt.show()

revpairsp79 = Request(p79nw.iloc[:,3],p79nw.iloc[:,4])
fulldatap79 = FullRequest(revpairsp79)

DMEaltp79 = FindAlt(fulldatap79)
    
revpairsarannw = Request(arannw.iloc[:,3],arannw.iloc[:,4])
fulldataarannw = FullRequest(revpairsarannw)

DEMaltarannw = FindAlt(fulldataarannw)

revpairsrpi1 = Request(rpi1.iloc[:,3],rpi1.iloc[:,4])
fulldatarpi1 = FullRequest(revpairsrpi1)

DEMaltrpi1 = FindAlt(fulldatarpi1)

revpairsrpi2 = Request(rpi2.iloc[:,3],rpi2.iloc[:,4])
fulldatarpi2 = FullRequest(revpairsrpi2)

DEMaltrpi2= FindAlt(fulldatarpi2)

revpairsrpi3 = Request(rpi3.iloc[:,3],rpi3.iloc[:,4])
fulldatarpi3 = FullRequest(revpairsrpi3)

revpairsrpi4 = Request(rpi4.iloc[:,3],rpi4.iloc[:,4])
fulldatarpi4 = FullRequest(revpairsrpi4)

revpairsrpi5 = Request(rpi5.iloc[:,3],rpi5.iloc[:,4])
fulldatarpi5 = FullRequest(revpairsrpi5)

revpairsrpi6 = Request(rpi6.iloc[:,3],rpi6.iloc[:,4])
fulldatarpi6 = FullRequest(revpairsrpi6)

revpairsd5587 = Request(d5587gps.iloc[:,1],d5587gps.iloc[:,2])
fulldatad5587 = FullRequest(revpairsd5587)

revpairsd5589 = Request(d5589gps.iloc[:,1],d5589gps.iloc[:,2])
fulldatad5589 = FullRequest(revpairsd5589)
#
revpairsd5592 = Request(d5592gps.iloc[:,1],d5592gps.iloc[:,2])
fulldatad5592 = FullRequest(revpairsd5592)
#
revpairsd5597 = Request(d5597gps.iloc[:,1],d5597gps.iloc[:,2])
fulldatad5597 = FullRequest(revpairsd5597)

revpairsc55 = Request(city55.iloc[2675:3330,1].values.tolist(),city55.iloc[2675:3330,2].values.tolist())
fulldatac55 = FullRequest(revpairsc55)

revpairscp79 = Request(cityp79.iloc[:,1],cityp79.iloc[:,2])
fulldatacp79 = FullRequest(revpairscp79)



latp79 = FindLong(fulldatap79)
longp79 = FindLat(fulldatap79)
altp79 = p79nw.iloc[:,5].values.tolist()
DEMaltp79 = FindAlt(fulldatap79)
distp79 = Distance(longp79,latp79)
gradrawp79 = Gradient(altp79,distp79)
gradDEMp79 = Gradient(DEMaltp79,distp79)
gradDEMcleanp79 = Gradientclean(DEMaltp79,distp79)

latarannw = FindLong(fulldataarannw)
longarannw = FindLat(fulldataarannw)
altarannw = arannw.iloc[:,5].values.tolist()
DEMaltarannw = FindAlt(fulldataarannw)
distarannw = Distance(longarannw,latarannw)
gradrawarannw = Gradient(altarannw,distarannw)
gradDEMarannw = Gradient(DEMaltarannw,distarannw)
gradDEMcleanarannw = Gradientclean(DEMaltarannw,distarannw)


latrpi1 = FindLong(fulldatarpi1)
longrpi1 = FindLat(fulldatarpi1)
altrpi1 = rpi1.iloc[:,2]
DEMaltrpi1 = FindAlt(fulldatarpi1)
distrpi1 = Distance(latrpi1,longrpi1)
gradrawrpi1 = Gradient(altrpi1,distrpi1)
gradDEMrpi1 = Gradient(DEMaltrpi1,distrpi1)
gradDEMcleanrpi1 = Gradientclean(DEMaltrpi1,distrpi1)

latrpi2 = FindLong(fulldatarpi2)
longrpi2 = FindLat(fulldatarpi2)
altrpi2 = rpi2.iloc[:,2]
DEMaltrpi2 = FindAlt(fulldatarpi2)
distrpi2 = Distance(latrpi2,longrpi2)
gradrawrpi2 = Gradient(altrpi2,distrpi2)
gradDEMrpi2 = Gradient(DEMaltrpi2,distrpi2)
gradDEMcleanrpi2 = Gradientclean(DEMaltrpi2,distrpi2)

latrpi3 = FindLong(fulldatarpi3)
longrpi3 = FindLat(fulldatarpi3)
altrpi3 = rpi3.iloc[:,2]
DEMaltrpi3 = FindAlt(fulldatarpi3)
distrpi3 = Distance(latrpi3,longrpi3)
gradrawrpi3 = Gradient(altrpi3,distrpi3)
gradDEMrpi3 = Gradient(DEMaltrpi3,distrpi3)
gradDEMcleanrpi3 = Gradientclean(DEMaltrpi3,distrpi3)

latrpi4 = FindLong(fulldatarpi4)
longrpi4 = FindLat(fulldatarpi4)
altrpi4 = rpi4.iloc[:,2]
DEMaltrpi4 = FindAlt(fulldatarpi4)
distrpi4 = Distance(latrpi4,longrpi4)
gradrawrpi4 = Gradient(altrpi4,distrpi4)
gradDEMrpi4 = Gradient(DEMaltrpi4,distrpi4)
gradDEMcleanrpi4 = Gradientclean(DEMaltrpi4,distrpi4)

latrpi5 = FindLong(fulldatarpi5)
longrpi5 = FindLat(fulldatarpi5)
altrpi5 = rpi5.iloc[:,2]
DEMaltrpi5 = FindAlt(fulldatarpi5)
distrpi5 = Distance(latrpi5,longrpi5)
gradrawrpi5 = Gradient(altrpi5,distrpi5)
gradDEMrpi5 = Gradient(DEMaltrpi5,distrpi5)
gradDEMcleanrpi5 = Gradientclean(DEMaltrpi5,distrpi5)


latrpi6 = FindLong(fulldatarpi6)
longrpi6 = FindLat(fulldatarpi6)
altrpi6 = rpi6.iloc[:,2]
DEMaltrpi6 = FindAlt(fulldatarpi6)
distrpi6 = Distance(latrpi6,longrpi6)
gradrawrpi6 = Gradient(altrpi6,distrpi6)
gradDEMrpi6 = Gradient(DEMaltrpi6,distrpi6)
gradDEMcleanrpi6 = Gradientclean(DEMaltrpi6,distrpi6)

latd5587 = FindLong(fulldatad5587)
longd5587 = FindLat(fulldatad5587)
DEMaltd5587 = FindAlt(fulldatad5587[875:1260])
distd5587 = Distance(latd5587[875:1260],longd5587[875:1260])
spdd5587 = d5587spd.iloc[:,1].values.tolist()
gradDEMd5587 = Gradient(DEMaltd5587,distd5587)
gradDEMcleand5587 = Gradientclean(DEMaltd5587,distd5587)
    
#resultd5587 =[]
#ang = 0
#for i in range(len(longd5587)):
#    if (i==0):
#        ang = 0
#    else:
#        ang = angle(latd5587[i-1],latd5587[i],longd5587[i-1],longd5587[i],ang)  
#    pos = take_closest_index(d5587spd.iloc[:,0],d5587gps.iloc[i,0])
#    speedlist = take_closest_x(d5587spd.iloc[:,1],pos, 25).values.tolist()
#    speed = sum(speedlist)/len(speedlist) 
#    posacc = take_closest_index(d5587acc.iloc[:,0],d5587gps.iloc[i,0])
#    accxlist = take_closest_x(d5587acc.iloc[:,1],posacc, 25).values.tolist()
#    accx = sum(accxlist)/len(accxlist) 
#    accylist = take_closest_x(d5587acc.iloc[:,2],posacc, 25).values.tolist()
#    accy = sum(accylist)/len(accylist)
#    imm = [latd5587[i],longd5587[i],speed/3.6,ang,accx,accy]
#    resultd5587.append(imm)

    

latd5589 = FindLong(fulldatad5589)
longd5589 = FindLat(fulldatad5589)
DEMaltd5589 = FindAlt(fulldatad5589[337:])
distd5589 = Distance(latd5589[337:],longd5589[337:])
spdd5589 = d5589spd.iloc[:,1].values.tolist()
gradDEMd5589 = Gradient(DEMaltd5589,distd5589)
gradDEMcleand5589 = Gradientclean(DEMaltd5589,distd5589)

#resultd5589 =[]
#ang = 0
#for i in range(len(longd5589)):
#    if (i==0):
#        ang = 0
#    else:
#        ang = angle(latd5589[i-1],latd5589[i],longd5589[i-1],longd5589[i],ang)  
#    pos = take_closest_index(d5589spd.iloc[:,0],d5589gps.iloc[i,0])
#    speedlist = take_closest_x(d5589spd.iloc[:,1],pos, 25).values.tolist()
#    speed = sum(speedlist)/len(speedlist) 
#    posacc = take_closest_index(d5589acc.iloc[:,0],d5589gps.iloc[i,0])
#    accxlist = take_closest_x(d5589acc.iloc[:,1],posacc, 25).values.tolist()
#    accx = sum(accxlist)/len(accxlist) 
#    accylist = take_closest_x(d5589acc.iloc[:,2],posacc, 25).values.tolist()
#    accy = sum(accylist)/len(accylist)
#    imm = [latd5589[i],longd5589[i],speed/3.6,ang,accx,accy]
#    resultd5589.append(imm)
    

latd5592 = FindLong(fulldatad5592)
longd5592 = FindLat(fulldatad5592)
DEMaltd5592 = FindAlt(fulldatad5592[246:740])
distd5592 = Distance(latd5592[246:740],longd5592[246:740])
spdd5592 = d5592spd.iloc[:,1].values.tolist()
gradDEMd5592 = Gradient(DEMaltd5592,distd5592)
gradDEMcleand5592 = Gradientclean(DEMaltd5592,distd5592)
#
#resultd5592 =[]
#ang = 0
#for i in range(len(longd5592)):
#    if (i==0):
#        ang = 0
#    else:
#        ang = angle(latd5592[i-1],latd5592[i],longd5592[i-1],longd5592[i],ang)  
#    pos = take_closest_index(d5592spd.iloc[:,0],d5592gps.iloc[i,0])
#    speedlist = take_closest_x(d5592spd.iloc[:,1],pos, 25).values.tolist()
#    speed = sum(speedlist)/len(speedlist) 
#    posacc = take_closest_index(d5592acc.iloc[:,0],d5592gps.iloc[i,0])
#    accxlist = take_closest_x(d5592acc.iloc[:,1],posacc, 25).values.tolist()
#    accx = sum(accxlist)/len(accxlist) 
#    accylist = take_closest_x(d5592acc.iloc[:,2],posacc, 25).values.tolist()
#    accy = sum(accylist)/len(accylist)
#    imm = [latd5592[i],longd5592[i],speed/3.6,ang,accx,accy]
#    resultd5592.append(imm)
#    

latd5597 = FindLong(fulldatad5597)
longd5597 = FindLat(fulldatad5597)
DEMaltd5597 = FindAlt(fulldatad5597[132:549])
distd5597 = Distance(latd5597[132:549],longd5597[132:549])
spdd5597 = d5597spd.iloc[:,1].values.tolist()
gradDEMd5597 = Gradient(DEMaltd5597,distd5597)
gradDEMcleand5597 = Gradientclean(DEMaltd5597,distd5597)

#resultd5597 =[]
#ang = 0
#for i in range(len(longd5597)):
#    if (i==0):
#        ang = 0
#    else:
#        ang = angle(latd5597[i-1],latd5597[i],longd5597[i-1],longd5597[i],ang)  
#    pos = take_closest_index(d5597spd.iloc[:,0],d5597gps.iloc[i,0])
#    speedlist = take_closest_x(d5597spd.iloc[:,1],pos, 25).values.tolist()
#    speed = sum(speedlist)/len(speedlist) 
#    posacc = take_closest_index(d5597acc.iloc[:,0],d5597gps.iloc[i,0])
#    accxlist = take_closest_x(d5597acc.iloc[:,1],posacc, 25).values.tolist()
#    accx = sum(accxlist)/len(accxlist) 
#    accylist = take_closest_x(d5597acc.iloc[:,2],posacc, 25).values.tolist()
#    accy = sum(accylist)/len(accylist)
#    imm = [latd5597[i],longd5597[i],speed/3.6,ang,accx,accy]
#    resultd5597.append(imm)

latc55 = FindLong(fulldatac55)
longc55 = FindLat(fulldatac55)
altc55 = city55alt.iloc[2675:3330,1].values.tolist()
DEMaltc55 = FindAlt(fulldatac55)
distc55 = Distance(latc55,longc55)
gradrawc55 = Gradient(altc55,distc55)
gradDEMc55 = Gradient(DEMaltc55,distc55)
gradDEMcleanc55 = Gradientclean(DEMaltc55,distc55)

latcp79 = FindLong(fulldatacp79)
longcp79 = FindLat(fulldatacp79)
altcp79 = cityp79.iloc[:,3].values.tolist()
DEMaltcp79 = FindAlt(fulldatacp79)
distcp79 = Distance(longcp79,latcp79)
gradrawcp79 = Gradient(altcp79,distcp79)
gradrawcp79 = Gradientclean(altcp79,distcp79)
gradDEMcp79 = Gradient(DEMaltcp79,distcp79)
gradDEMcleancp79 = Gradientclean(DEMaltcp79,distcp79)


#plt.plot(distcp79,altcp79)
#plt.plot(distc55,altc55)
plt.plot(distcp79,DEMaltcp79)
plt.plot(distc55,DEMaltc55)
#plt.legend(['rawdata','DEMdata'])
#plt.title('Elevation Comparison')
plt.show()


#plt.plot(distarannw,altarannw)
plt.plot(distarannw,DEMaltarannw)
#plt.legend(['raw','DEM'])
#plt.ylabel('ELevation [M]')
#plt.xlabel('Distance Traveled [KM]')
##plt.title('Elevation Comparison')
#plt.show()
#
#plt.plot(distarannw[1080:1160],DEMaltarannw[1080:1160])
#plt.ylabel('ELevation [M]')
#plt.xlabel('Distance Traveled [KM]')
#plt.show()



#plt.plot(distrpi1,altrpi1)
plt.plot(distrpi1,DEMaltrpi1)

#plt.plot(distrpi2,altrpi2)
#plt.plot(distrpi2,DEMaltrpi2)

#plt.plot(distrpi3,altrpi3)
#plt.plot(distrpi3,DEMaltrpi3)

#plt.plot(distrpi4,altrpi4)
#plt.plot(distrpi4,DEMaltrpi4)

#plt.plot(distrpi5,altrpi5)
#plt.plot(distrpi5,DEMaltrpi5)

#plt.plot(distrpi6,altrpi6)
#plt.plot(distrpi6,DEMaltrpi6)

#plt.plot(distd5587,DEMaltd5587)

#plt.plot(distd5589,DEMaltd5589)

#plt.plot(distd5592,DEMaltd5592)

#plt.plot(distd5597,DEMaltd5597)

#Gradient Plots:
plt.plot(distcp79,gradrawcp79)
#plt.plot(distcp79,gradDEMcp79)
plt.plot(distcp79,gradDEMcleancp79)
plt.plot(distcp79,DEMaltcp79)

plt.plot(distc55,gradrawc55)
plt.plot(distc55,gradDEMc55)
plt.plot(distc55,gradDEMcleanc55)
plt.plot(distc55,DEMaltc55)

#plt.plot(distarannw,gradrawarannw)
#plt.plot(distarannw,gradDEMarannw)
plt.plot(distarannw,gradDEMcleanarannw)

#fig = plt.figure(figsize=(10,6))
#ax = plt.axes(projection='3d')
#ax.plot3D(longarannw,latarannw,gradDEMcleanarannw)
#ax.plot3D(longrpi1,latrpi1,gradDEMcleanrpi1)
#plt.show()

#plt.plot(distrpi1,gradrawrpi1)
#plt.plot(distrpi1,gradDEMrpi1)
plt.plot(distrpi1,gradDEMcleanrpi1)
plt.ylabel('Road Gradient [%]')
plt.xlabel('Distance Traveled [KM]')
plt.legend(['aran','rpi1'])
plt.show()

plt.figure(figsize=(10,6))
plt.plot(distrpi2,gradrawrpi2)
plt.plot(distrpi2,gradDEMrpi2)
plt.plot(distrpi2,gradDEMcleanrpi2, 'm', linewidth = 3)
plt.legend(['raw','DEM','cleaned DEM'])
plt.ylabel('Road Gradient [%]')
plt.xlabel('Distance Traveled [KM]')
plt.show()
#
#plt.plot(distrpi3,gradrawrpi3)
#plt.plot(distrpi3,gradDEMrpi3)
#plt.plot(distrpi3,gradDEMcleanrpi3)
#
#
#plt.plot(distrpi4,gradrawrpi4)
#plt.plot(distrpi4,gradDEMrpi4)
#plt.plot(distrpi4,gradDEMcleanrpi4)
#
#
#plt.plot(distrpi5,gradrawrpi5)
#plt.plot(distrpi5,gradDEMrpi5)
#plt.plot(distrpi5,gradDEMcleanrpi5)
#
#
#plt.plot(distrpi6,gradrawrpi6)
#plt.plot(distrpi6,gradDEMrpi6)
#plt.plot(distrpi6,gradDEMcleanrpi6)

#plt.plot(distd5587,gradDEMd5587)
#plt.plot(distd5587,gradDEMcleand5587)

#plt.plot(distd5589,gradDEMd5589)
#plt.plot(distd5589,gradDEMcleand5589)

#plt.plot(distd5592,gradDEMd5592)
#plt.plot(distd5592,gradDEMcleand5592)

#plt.plot(distd5597,gradDEMd5597)
#plt.plot(distd5597,gradDEMcleand5597)


fig = plt.figure(figsize=(10,6))

ax = fig.add_subplot(111, projection='3d')
#ax.plot(latc55,longc55,gradrawc55)
#ax.plot(latcp79,longcp79,gradrawcp79)
#ax.plot(latc55,longc55,gradDEMcleanc55, 'm', linewidth = 2)
#ax.plot(latrpi1,longrpi1,gradrawrpi1)
ax.plot(latarannw,longarannw,gradDEMcleanarannw)
ax.plot(latrpi1,longrpi1,gradDEMcleanrpi1, 'm', linewidth = 3)
ax.plot(latrpi3,longrpi3,gradDEMcleanrpi3, linewidth = 2)
ax.set_xlabel("Latitude")

#ax.set_ylabel("Longitude")
#ax.set_zlim([-200,200])

ax.set_zlabel("Road Gradient [%]")

#ax.view_init(elev=-90, azim=0)
ax.view_init(elev=0, azim=90)
#ax.legend(["aran", "rpi1", "rpi3"], loc= "best")
plt.show()

fig = plt.figure(figsize=(10,6))

ax = fig.add_subplot(111, projection='3d')
ax.plot(latc55,longc55,gradrawc55)
ax.plot(latcp79,longcp79,gradDEMcleancp79)
ax.plot(latc55,longc55,gradDEMcleanc55, 'm', linewidth = 1)
#ax.plot(latrpi1,longrpi1,gradrawrpi1)
#ax.plot(latarannw,longarannw,gradDEMcleanarannw)
#ax.plot(latrpi1,longrpi1,gradDEMcleanrpi1, 'm', linewidth = 3)
ax.set_xlabel("Latitude")

ax.set_ylabel("Longitude")
ax.set_zlim([-10,10])

#ax.set_zlabel("Road Gradient [%]")

#ax.view_init(elev=-90, azim=0)
ax.view_init(elev=0, azim=-0)
#ax.legend(["raw", "aran", "DEM"], loc= "best")
plt.show()

fig = plt.figure(figsize=(10,6))

ax = fig.add_subplot(111, projection='3d')
ax.plot(latc55,longc55,gradrawc55)
ax.plot(latcp79,longcp79,gradDEMcleancp79)
ax.plot(latc55,longc55,gradDEMcleanc55, 'm', linewidth = 3)
#ax.plot(latrpi2,longrpi2,gradrawrpi2)
#ax.plot(latarannw,longarannw,gradDEMcleanarannw)
#ax.plot(latrpi2,longrpi2,gradDEMcleanrpi2, 'm', linewidth = 3)
ax.set_xlabel("Latitude")

ax.set_ylabel("Longitude")
ax.set_zlim([-10,10])

#ax.set_zlabel("Road Gradient [%]")

#ax.view_init(elev=-90, azim=0)
ax.view_init(elev=0, azim=-90)
#ax.legend(["raw", "aran", "DEM"], loc= "best")
plt.show()

fig = plt.figure(figsize=(10,6))

ax = fig.add_subplot(111, projection='3d')
#ax.plot(latc55,longc55,gradrawc55)
#ax.plot(latcp79,longcp79,gradDEMcleancp79)
ax.plot(latc55,longc55,gradDEMcleanc55, 'm', linewidth = 3)
ax.set_xlabel("Latitude")

ax.set_ylabel("Longitude")

#ax.set_zlabel("Road Gradient [%]")

#ax.view_init(elev=-90, azim=0)
ax.view_init(elev=30, azim=-60)
#ax.legend(["raw", "aran", "DEM"], loc= "best")
plt.show()


    
    
    
    
    
