# coding=utf-8
import requests
import json
import re
import math
import time
import datetime
import random
import hashlib
import codecs
from Phone import *
from HaRunGo import *

class Point:
    lat = 0
    lng = 0

    def __init__(self, x, y):
        self.lat = x
        self.lng = y

    def __str__(self):
        return "x: " + str(self.lat) + ", y: " + str(self.lng)

    # def __eq__(self, other):
    #     return (self.lat == other.lat & self.lng == other.lng)

    def radian(self, data):
        return data * math.pi / 180.0

    def dis(self, point):
        a = self.radian(self.lat) - self.radian(point.lat)
        b = self.radian(self.lng) - self.radian(point.lng)
        r1 = self.radian(self.lat)
        r2 = self.radian(point.lat)
        s = 2 * math.asin(math.sqrt(math.pow(math.sin(a / 2), 2) + math.cos(r1) * math.cos(r2) * math.pow(math.sin(b / 2), 2)))
        s = s * 6378.137
        return s * 1000

outdata = codecs.open('tp.data', 'w', 'utf-8')

testPoints = {}

def datetime_to_timestamp_in_milliseconds(d):
    return int(time.mktime(d.timetuple()) * 1000)

def getOriginalJson(roomId,headers):
    data = {
        "roomId":roomId
    }
    url = 'http://gxapp.iydsj.com/api/v8/get/room/history/finished/record'
    Session = requests.Session()
    Request = Session.post(url, headers=headers, data=json.dumps(data))
#    print Request.content
    return Request.content

MAX_DISTANCE = 50

def isSelectedPoint(lat, lng):
    #print testPoints
    thisPoint = Point(float(lat), float(lng))
    for tp in testPoints:
        dis = testPoints[tp].dis(thisPoint)
        if dis <= MAX_DISTANCE:
            return 1, tp
    return 0, 0

def getTestPoints(userInfo):
    timeStamp = str(int(time.time()*1000))
    dic = {
        'uid':userInfo['uid'],
        'token':userInfo['token'],
        'timeStamp':timeStamp
    }
    headers = {
        "Host": "gxapp.iydsj.com",
        "Accept": "application/json",
        "osType": "0",
        "Content-Type": "application/json",
        "DeviceId": getDeviceId(),
        "CustomDeviceId": getCustomDeviceId(),
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.0; SM-N9002 Build/LRX21V)",
        "appVersion":"1.3.10",
        "uid":str(dic['uid']),
        "token":dic['token'],
        "tokenSign":digestDict(dic),
        "timeStamp":dic['timeStamp']
    }
    md5key = getMD5Key()
    latlng = getStartLatLng()
    url = 'http://gxapp.iydsj.com/api/v8/get/1/distance/1'
    sign = hashlib.md5(url+md5key).hexdigest().upper()
    post = {
        "latitude":latlng['lat'],
        "longitude":latlng['lng'],
        "selectedUnid":userInfo['unid'],
        "sign":sign
    }
    data = json.dumps(post)
    Session = requests.Session()
    for i in xrange(5):
        Request = Session.post(url, headers=headers, data=data)
        points = json.loads(Request.content)['data']['pointsResModels']
        for p in points:
            if not testPoints.has_key(p['pointName']):
                testPoints[p['pointName']] = Point(p['lat'],p['lon'])

def createFivePoints(points):
#    tpData = "{\"fivePointJson\":\"["
    tpData = set()

    for point in points:
#        assert isinstance(point, Point)
#        need = "{\\\"flag\\\":%s,\\\"lon\\\":\\\"%s\\\",\\\"lat\\\":\\\"%s\\\",\\\"isFixed\\\":0,\\\"isPass\\\":true,\\\"isfinal\\\":false,\\\"id\\\":%s}" % (str(flag), str(point.lng), str(point.lat), str(id))
#        print type(point)
        selected, pointName = isSelectedPoint(point['lat'], point['lng'])
        if selected == 1:
            tpData.add(pointName)
        #tpData += need
        # print need
        #id += 1
            #cnt += 1
            #if cnt >= 5:
            #or cnt == len(points) - 1:
                #break
#    print tpData
    if len(tpData)<3:
        return False
    fivePoints = []
    flag = datetime_to_timestamp_in_milliseconds(datetime.datetime.now())
    id = int(random.uniform(0, 250))
    cnt = len(fivePoints)
    for i in tpData:
        fp = {
            "flag": flag,
            "hasReward": False,
            "id": id,
            "isFixed": 0,
            "isPass": True,
            "lat": str(testPoints[i].lat),
            "lon": str(testPoints[i].lng),
            "pointName": i
        }
        fivePoints.append(fp)
        cnt += 1
        id += 1
        if cnt >= 5:
            break
    #print len(fivePoints)
    fixed = random.randint(0,len(fivePoints)-1)
    fivePoints[fixed]['isFixed'] = 1
    cnt = len(fivePoints)
    #print cnt
    while cnt<5:
        for p in testPoints:
            if p in tpData:
                continue
            fp = {
                "flag": flag,
                "hasReward": False,
                "id": id,
                "isFixed": 0,
                "isPass": False,
                "lat": str(testPoints[p].lat),
                "lon": str(testPoints[p].lng),
                "pointName": p
            }
            fivePoints.append(fp)
            cnt += 1
            id += 1
            if cnt >= 5:
                break
        #tpData += ','

    # print tpData
    #tpData += "]\",\"useZip\":false}\n"

    #print len(points)
    #print len(fivePoints)
    fivepointjson = {
        "fivePointJson": json.dumps(fivePoints ,ensure_ascii=False),
        "useZip": False
    }
    outdata.write(json.dumps(fivepointjson ,ensure_ascii=False)+'\n')
    return True


#    print tpData


def getRoomIdJson(userInfo):
    timeStamp = str(int(time.time()*1000))
    dic = {
        'uid':userInfo['uid'],
        'token':userInfo['token'],
        'timeStamp':timeStamp
    }
    headers = {
        "Host": "gxapp.iydsj.com",
        "Accept": "application/json",
        "osType": "0",
        "Content-Type": "application/json",
        "DeviceId": getDeviceId(),
        "CustomDeviceId": getCustomDeviceId(),
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.0; SM-N9002 Build/LRX21V)",
        "appVersion":"1.3.10",
        "uid":str(dic['uid']),
        "token":dic['token'],
        "tokenSign":digestDict(dic),
        "timeStamp":dic['timeStamp']
    }
    url = 'http://gxapp.iydsj.com/api/v8/get/aboutrunning/list/'+str(dic['uid'])+'/'+str(userInfo['unid'])+'/'+'3'
#    getTestPoints(headers)
    Session = requests.Session()
    Request = Session.get(url, headers=headers)
    reqDate = Request.content
#    print reqDate
    s = json.loads(Request.content)
#    print s['data']
    output = open('route.data', 'w')
#    cnt = 0
    for item in s["data"]:
        OriginalJson = getOriginalJson(item["roomId"],headers)
#        print OriginalJson
        data = json.loads(OriginalJson)['data']
        for l in data['roomersModelList']:
            if l['finished']:
                d = json.loads(l['points'])
                d = json.loads(d['allLocJson'])
                if isinstance(d,list) and d[0].has_key('createtime'):
                    print 'got one record for iphone,ignore it'
                    continue
                if createFivePoints(d):
                    print 'got one record'
                    alllocjson = {
                        "allLocJson": json.dumps(d),
                        "useZip": False
                    }
                    output.write(json.dumps(alllocjson) + '\n')
                else:
                    print 'got one record but doesn\'t match testPoint,ignore it'
#            print json.loads(l['points'])
#        NewJson = OriginalJson.replace("\\\"", "\"")
#        NewJson2 = NewJson.replace("\\\\", "\\")
        # output.writelines(NewJson2)
        # print (str(cnt * 2) + "% :" + ("#" * cnt))
        # print NewJson2

#        willSelectedPoint = set()

#        run_data_str = re.findall(r'{\"allLocJson\":\"\[\{\\"av.+\"useZip\":false}', str(NewJson2))
#        if (len(run_data_str) > 0):
            # print cnt + 1
#            cnt = cnt + 1
#            print ("Updating " + str(cnt) + " running groups data. ")
#            output.write(run_data_str[0] + '\n')

#            run_points_str = re.findall(r'\\\"lat\\\"\:\\\"\d+.\d+\\\",\\\"lng\\"\:\\\"\d+.\d+\\\"', run_data_str[0])
            # print run_points_str
#            for run_point_str in run_points_str:
                # print run_point_str
#                point_json_str = "{" + run_point_str + "}"
#                point_json_str = point_json_str.replace('\\\"', '\"')
                # print point_json_str
#                point_json = json.loads(point_json_str)
#                print point_json

#                thisPoint = Point(float(point_json['lat']), float(point_json['lng']))

#                isPass, addPoint = isSelectedPoint(float(point_json['lat']), float(point_json['lng']))

#                if isPass  == 1:
#                    willSelectedPoint.add(addPoint)
#
            # for p in willSelectedPoint:
            #     print p
#            createFivePointsStr(willSelectedPoint)
#
#            if (cnt >= 50):
#                break
    output.close()
    outdata.close()


def main():
    users = writeByData()
    length = len(users)
    username, password = users[random.randint(0,length-1)].split(' ')
    userInfo = login(username, password)
    try:
        getTestPoints(userInfo)
        getRoomIdJson(userInfo)
    finally:
        logout(userInfo)

if __name__== '__main__':
    main()
