# coding=utf-8
import requests
import json
import re
import math
import time
import datetime
import random
import HaRunGo

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

def getHeaders(userName,userPasswd):
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "DeviceId": "913476526138277",
        "source": "000049",
        "appVersion": "1.2.1",
        "osType": "0",
        "CustomDeviceId": "1F5576C69162C0D40D54B2F804CBF370",
        "uid": "80604",
        "Authorization": HaRunGo.base64encode(userName,userPasswd),
        "User-Agent": "Dalvik/1.6.0 (Linux; U; Android 4.4.4; R9 Build/KTU84P)",
        "Host": "gxapp.iydsj.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
        }
    return headers

outdata = open('tp.data', 'w')

testPoints = [
        Point(30.771025, 103.985729),
        Point(30.768690, 103.987364),
        Point(30.772452, 103.988141),
        Point(30.768566, 103.989982),
        Point(30.765339, 103.990072),
        Point(30.775152, 103.990113),
        Point(30.769404, 103.991393),
        Point(30.763314, 103.991707),
        Point(30.767362, 103.992839),
        Point(30.772670, 103.993903),
        Point(30.773321, 103.995718),
        Point(30.766797, 103.996032),
        Point(30.770715, 103.996949),
        Point(30.768291, 103.998134),
        Point(30.766111, 103.998840),
        Point(30.774981, 104.000061),
    ]

def datetime_to_timestamp_in_milliseconds(d):
    return int(time.mktime(d.timetuple()) * 1000)

def getOriginalJson(roomId,headers):
    url = 'http://gxapp.iydsj.com/api/v3/get/'+ str(roomId) + '/history/finished/record '
    Session = requests.Session()
    Request = Session.get(url, headers=headers)
    return Request.content

MAX_DISTANCE = 20

def isSelectedPoint(lat, lng):
    thisPoint = Point(float(lat), float(lng))
    for tp in testPoints:
        dis = tp.dis(thisPoint)
        if dis <= MAX_DISTANCE:
            return 1, tp
    return 0, 0


def createFivePointsStr(points):
    tpData = "{\"fivePointJson\":\"["
    flag = datetime_to_timestamp_in_milliseconds(datetime.datetime.now())
    id = int(random.uniform(0, 250))
    cnt = 0

    for point in points:
        assert isinstance(point, Point)
        need = "{\\\"flag\\\":%s,\\\"lon\\\":\\\"%s\\\",\\\"lat\\\":\\\"%s\\\",\\\"isFixed\\\":0,\\\"isPass\\\":true,\\\"isfinal\\\":false,\\\"id\\\":%s}" % (str(flag), str(point.lng), str(point.lat), str(id))
        tpData += need
        # print need
        id += 1
        cnt += 1
        if cnt >= 4 or cnt == len(points) - 1:
            break
        tpData += ','

    # print tpData
    tpData += "]\",\"useZip\":false}\n"

    outdata.writelines(tpData)


    print tpData


def getRoomIdJson(headers):
    url = 'http://gxapp.iydsj.com/api/v3/get/aboutrunning/list/0/901/3'
    Session = requests.Session()
    Request = Session.get(url, headers=headers)
    reqDate = Request.content
    print reqDate
    s = json.loads(Request.content)
    output = open('route.data', 'w')
    cnt = 0
    for item in s["data"]:
        OriginalJson = getOriginalJson(item["roomId"],headers)
        NewJson = OriginalJson.replace("\\\"", "\"")
        NewJson2 = NewJson.replace("\\\\", "\\")
        # output.writelines(NewJson2)
        # print (str(cnt * 2) + "% :" + ("#" * cnt))
        # print NewJson2

        willSelectedPoint = set()

        run_data_str = re.findall(r'{\"allLocJson\":\"\[\{\\"av.+\"useZip\":false}', str(NewJson2))
        if (len(run_data_str) > 0):
            # print cnt + 1
            cnt = cnt + 1
            print ("Updating " + str(cnt) + " running groups data. ")
            output.write(run_data_str[0] + '\n')

            run_points_str = re.findall(r'\\\"lat\\\"\:\\\"\d+.\d+\\\",\\\"lng\\"\:\\\"\d+.\d+\\\"', run_data_str[0])
            # print run_points_str
            for run_point_str in run_points_str:
                # print run_point_str
                point_json_str = "{" + run_point_str + "}"
                point_json_str = point_json_str.replace('\\\"', '\"')
                # print point_json_str
                point_json = json.loads(point_json_str)
                # print point_json

                thisPoint = Point(float(point_json['lat']), float(point_json['lng']))

                isPass, addPoint = isSelectedPoint(float(point_json['lat']), float(point_json['lng']))

                if isPass  == 1:
                    willSelectedPoint.add(addPoint)

            # for p in willSelectedPoint:
            #     print p
            createFivePointsStr(willSelectedPoint)

            if (cnt >= 50):
                break
    output.close()
    outdata.close()


def main():
    users = HaRunGo.writeByData()
    length = len(users)
    username, password = users[random.randint(0,length-1)].split(' ')
    headers = getHeaders(username, password)
    getRoomIdJson(headers)

if __name__== '__main__':
    main()
