import requests
import matplotlib.pyplot as plt
import json
from requests.structures import CaseInsensitiveDict
import pandas as pd

def Request(dataframe,start,end):
    latdata = dataframe.iloc[start:end,1].values.tolist()
    longdata = dataframe.iloc[start:end,2].values.tolist()
    revpairs = []
    for i in range(len(latdata)):
        revpairs.append([longdata[i],latdata[i]])
    
    for i in range(len(revpairs)):
        revpairs[i] = ','.join(str(e) for e in revpairs[i]) 
    return revpairs

def Jsonreq(gps):
    requestlist = []
    for i in gps:
        requestlist.append('{"location":['+str(i)+']}')
    requeststring = ','.join(requestlist)
    return requeststring

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

def Requestfromjson(data, start, end):
    latdata = FindLat(data[start:end])
    longdata = FindLong(data[start:end])
    revpairs = []
    for i in range(len(latdata)):
        revpairs.append([longdata[i],latdata[i]])
    
    for i in range(len(revpairs)):
        revpairs[i] = ','.join(str(e) for e in revpairs[i]) 
    return revpairs


data = pd.read_csv("/Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/task_4955_gps_raw.txt",'\t')
dataframegps = pd.DataFrame(data)

data = pd.read_csv("//Users/madsmoller/Desktop/BachelorThesis/PlatoonData-GradientProject/P79_W_imp_mat.csv", ';', encoding='latin-1')
dataframep79 = pd.DataFrame(data)

gps = Request(dataframegps, 2675, 3330)
request = Jsonreq(gps)

token = "e9aec1f926aa2482b16acad49cb11e83"
url = "https://api.geoapify.com/v1/mapmatching?apiKey=d0ba724be19c4a6cabd1c731e4e6ef06"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"

data = '{"mode":"drive","waypoints":['+ request + ']}'
#print(data)

#resp = requests.post(url, headers=headers, data=data)

respjson = resp.json()
geo = respjson['features']
gep = geo[0]
geometry = gep['geometry']
coordinate = geometry['coordinates']
coordinatelist = coordinate[0]

#long = FindLong(coordinatelist)
#lat = FindLat(coordinatelist)
#plt.plot(long,lat)

findata = []

revpairs = Requestfromjson(coordinatelist,0,50)
request = '%3B'.join(revpairs)
print(request)

restdata = RestCall(token, request)

restalt = FindAlt(restdata)
print(restalt)
restlong = FindLong(restdata)
print(restlong)
restlat = FindLat(restdata)
print(restlat)
plt.plot(alt)
#findata.append(data)
#print(data)


