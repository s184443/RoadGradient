from flask import Flask, request
from flask_restful import Resource, Api
import json
import requests
import numpy as np
from scipy import stats
import haversine as hs
app = Flask(__name__)
api = Api(app)

#Replace this with own token from Kortforsyningen at: https://kortforsyningen.dk
token = 'e9aec1f926aa2482b16acad49cb11e83'

#Makes a list from a specific Index in aa list of lists.
def Finddata(data, index):
    extracted = []
    for i in data:
        extracted.append(float(i[index]))
    return extracted

#Creates a list of coordinate pairs.
def Request(lat, long):
    revpairs = []
    for i in range(len(lat)):
        revpairs.append([long[i],lat[i]])
    
    for i in range(len(revpairs)):
        revpairs[i] = ','.join(str(e) for e in revpairs[i]) 
    return revpairs

#Calls Kortforsyningen for 50 datapoints and unpacks them.
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

#Runs a loop calling 50 points at a time until all requested points have been found.
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

#Find the total distance traveled on a route. 
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

#Calculates the route gradient using the elevation and the total distance traveled.
#Hereafter it cleans the data.
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

    outlierIndex = np.where(z>threshold)
    print(outlierIndex)
    for i in outlierIndex[0]:
        gradient[i] = gradient[i-1]
    return gradient

#Handels REST requests.
def requestHandeling(request):
    datastore = json.dumps(request)
    json_string = json.loads(datastore)

    gps = json_string["gps"]

    
    lat = Finddata(gps, 0)
    long = Finddata(gps,1)
    revpairs = Request(lat,long)
    fulldata = FullRequest(revpairs)
    DEMalt = Finddata(fulldata, 2)
    dist = Distance(long,lat)
    gradclean = Gradientclean(DEMalt, dist)

    answer = []
    for i in range(len(lat)):
        answer.append([lat[i],long[i],DEMalt[i],gradclean[i]])
    
    response = {"gps":answer}

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
    