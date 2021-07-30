from flask import Flask, request
from flask_restful import Resource, Api
import json
import requests
import math
import numpy as np
from bisect import bisect_left
from scipy import stats
import haversine as hs
app = Flask(__name__)
api = Api(app)
token = 'e9aec1f926aa2482b16acad49cb11e83'
def Finddata(data, index):
    extracted = []
    for i in data:
        extracted.append(float(i[index]))
    return extracted

def Request(lat, long):
    revpairs = []
    for i in range(len(lat)):
        revpairs.append([long[i],lat[i]])
    
    for i in range(len(revpairs)):
        revpairs[i] = ','.join(str(e) for e in revpairs[i]) 
    return revpairs

def RestCall(token, request):
    request = "https://api.dataforsyningen.dk/RestGeokeys_v2?elevationmodel=dtm&method=geopmulti&geop={0}&georef=EPSG:4326&token={1}".format(request,token)
    print(request)
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

def FullRequest(revpairs):
    findata = []
    for i in range(50,len(revpairs)+50,50):
        if (i>len(revpairs)):
            request = '%3B'.join(revpairs[i-50:len(revpairs)])
    
        request = '%3B'.join(revpairs[i-50:i])
    
        data = RestCall(token, request)
        findata.append(data)
        print(data)
    list1 = []
    for i in findata:
        list1 += i
    return list1

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

def FindGradient(alt, dist):
    gradient = []
    for i in range(len(alt)):
        if i == 0:
            gradient.append(0)
        else:
            try:
                gradient.append((alt[i]-alt[i-1])/((dist[i]-dist[i-1])*1000)*100)
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
                gradient.append((alt[i]-alt[i-1])/((dist[i]-dist[i-1])*1000)*100)
            except ZeroDivisionError:
                gradient.append(0)
    z = np.abs(stats.zscore(gradient))
#    print(z)
    outlierIndex = np.where(z>threshold)
    print(outlierIndex)
    for i in outlierIndex[0]:
        gradient[i] = gradient[i-1]
    return gradient

def requestHandeling(request):
    datastore = json.dumps(request)
    json_string = json.loads(datastore)
#    data = json_string["data"]
    gps = json_string["gps"]
#    print(gps)
    
    lat = Finddata(gps, 0)
    long = Finddata(gps,1)
    revpairs = Request(lat,long)
    fulldata = FullRequest(revpairs)
    DEMalt = Finddata(fulldata, 2)
    dist = Distance(long,lat)
    grad = FindGradient(DEMalt, dist)
    gradclean = Gradientclean(DEMalt, dist)

    answer = []
    for i in range(len(lat)):
        answer.append([lat[i],long[i],DEMalt[i],gradclean[i]])
    
    response = {"gps":answer}
    jsonresponse = json.dumps(response)
    return response

class Gradient(Resource):
    # methods go here
    def get(self):
        return "Hello", 200
    pass
    
    def post(self):
        return requestHandeling(request.get_json()), 200
    pass

api.add_resource(Gradient, '/gradient')  # '/users' is our entry point for Users

if __name__ == '__main__':
    app.run()
    