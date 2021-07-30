import requests
import matplotlib.pyplot as plt
import json
from requests.structures import CaseInsensitiveDict
import pandas as pd

#data = pd.read_excel("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/May_2019/M13_GPS.xlsx", 2, usecols="A:F")
#arannw = pd.DataFrame(data)
#print("arannw: " + str(len(arannw)))

#data1 = pd.read_excel("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/May_2019/M13_GPS.xlsx", 3, usecols="A:F")
#p79nw= pd.DataFrame(data1)
#print("p79nw: " + str(len(p79nw)))
#
data2 = pd.read_excel("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/May_2019/M13_GPS.xlsx", 1, usecols="A:F")
rpi1 = pd.DataFrame(data2)
rpi1 = rpi1.dropna()
print("rpi1: " + str(len(rpi1)))
#
#data3 = pd.read_excel("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/May_2019/M13_GPS.xlsx", 1, usecols="H:M")
#rpi2 = pd.DataFrame(data3)
#rpi2 = rpi2.dropna()
#print("rpi2: " + str(len(rpi2)))
#
#data4 = pd.read_excel("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/May_2019/M13_GPS.xlsx", 1, usecols="O:T")
#rpi3 = pd.DataFrame(data4)
#rpi3 = rpi3.dropna()
#print("rpi3: " + str(len(rpi3)))
#
#data5 = pd.read_excel("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/May_2019/M13_GPS.xlsx", 1, usecols="V:AA")
#rpi4 = pd.DataFrame(data5)
#rpi4 = rpi4.dropna()
#print("rpi4: " + str(len(rpi4)))
#
#data6 = pd.read_excel("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/May_2019/M13_GPS.xlsx", 1, usecols="AC:AH")
#rpi5 = pd.DataFrame(data6)
#rpi5 = rpi5.dropna()
#print("rpi5: " + str(len(rpi5)))
#
#data7 = pd.read_excel("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/May_2019/M13_GPS.xlsx", 1, usecols="AJ:AO")
#rpi6 = pd.DataFrame(data7)
#rpi6 = rpi6.dropna()
#print("rpi6: " + str(len(rpi6)))
#
#
#data8 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5587_gps_raw.txt",'\t')
#d5587gps = pd.DataFrame(data8)
#print("d5587: " + str(len(d5587gps)))
#
#data8 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5587_speed.txt",'\t')
#d5587spd = pd.DataFrame(data8)
#print("d5587: " + str(len(d5587spd)))
#
#data8 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5587_acc_rpi.txt",'\t')
#d5587acc = pd.DataFrame(data8)
#print("d5587: " + str(len(d5587acc)))
#
#
#data9 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5589_gps_raw.txt",'\t')
#d5589gps = pd.DataFrame(data9)
#print("d5589: " + str(len(d5589gps)))
#
#data9 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5589_speed.txt",'\t')
#d5589spd = pd.DataFrame(data9)
#print("d5589: " + str(len(d5589spd)))
#
#data9 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5589_acc_rpi.txt",'\t')
#d5589acc = pd.DataFrame(data9)
#print("d5589: " + str(len(d5589acc)))
#
#
#data10 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5592_gps_raw.txt",'\t')
#d5592gps = pd.DataFrame(data10)
#print("d5592: " + str(len(d5592gps)))
#
#data10 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5592_speed.txt",'\t')
#d5592spd = pd.DataFrame(data10)
#print("d5592: " + str(len(d5592spd)))
#
#data10 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5592_acc_rpi.txt",'\t')
#d5592acc = pd.DataFrame(data10)
#print("d5592: " + str(len(d5592acc)))
#
#
#data11 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5597_gps_raw.txt",'\t')
#d5597gps = pd.DataFrame(data11)
#print("d5597: " + str(len(d5597gps)))
#
#data11 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5597_speed.txt",'\t')
#d5597spd = pd.DataFrame(data11)
#print("d5597: " + str(len(d5597spd)))
#
#data11 = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/M13_DTU_LOOP_GPS_DATA/November_2020/task_5597_acc_rpi.txt",'\t')
#d5597acc = pd.DataFrame(data11)
#print("d5597: " + str(len(d5597acc)))

def pairs(dataframe,longindex,latindex):
    long = dataframe.iloc[:,longindex].values.tolist()
    lat = dataframe.iloc[:,latindex].values.tolist()
    pairs = []
    for i in range(len(long)):
        pairs.append([long[i],lat[i]])
    return pairs

def jsonrequest(pairs):
    request = {"data":{"gps":pairs}}
    jsonrequest = json.dumps(request)
    return jsonrequest
    
url = "http://127.0.0.1:5000/gradient"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"

data = jsonrequest(pairs(rpi1,3,4))
#print(data)

resp = requests.post(url, headers=headers, data=data)
print(resp.json())
