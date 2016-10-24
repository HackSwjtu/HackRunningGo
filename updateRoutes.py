# coding=utf-8
import requests
import json
import re
import math

class Point:
    lat = 0
    lng = 0

    def __init__(self, x, y):
        self.lat = x
        self.lng = y

    def __str__(self):
        return "x: " + str(self.lat) + ", y: " + str(self.lng)

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



headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "DeviceId": "913476526138277",
        "source": "000049",
        "appVersion": "1.2.1",
        "osType": "0",
        "CustomDeviceId": "1F5576C69162C0D40D54B2F804CBF370",
        "uid": "80604",
        "Authorization": "Basic MTgzMzU0MTA4MTc6MTIzNDU2",
        "User-Agent": "Dalvik/1.6.0 (Linux; U; Android 4.4.4; R9 Build/KTU84P)",
        "Host": "gxapp.iydsj.com",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }

testPoints = [
        Point(103.985729,30.771025),
        Point(103.987364,30.768690),
        Point(103.988141,30.772452),
        Point(103.989982,30.768566),
        Point(103.990072,30.765339),
        Point(103.990113,30.775152),
        Point(103.991393,30.769404),
        Point(103.991707,30.763314),
        Point(103.992839,30.767362),
        Point(103.993903,30.772670),
        Point(103.995718,30.773321),
        Point(103.996032,30.766797),
        Point(103.996949,30.770715),
        Point(103.998134,30.768291),
        Point(103.998840,30.766111),
        Point(104.000061,30.774981),
    ]

def getOriginalJson(roomId):
    url = 'http://gxapp.iydsj.com/api/v3/get/'+ str(roomId) + '/history/finished/record '
    Session = requests.Session()
    Request = Session.get(url, headers=headers)
    return Request.content

def isSelectedPoint(lat, lng):
    # print lat, lng
    xx = Point(float(lat), float(lng))
    for tp in testPoints:
        dis = tp.dis(xx)


    return 0


def getRoomIdJson():
    url = 'http://gxapp.iydsj.com/api/v3/get/aboutrunning/list/80604/901/3'
    Session = requests.Session()
    Request = Session.get(url, headers=headers)
    reqDate = Request.content
    print reqDate
    s = json.loads(Request.content)
    output = open('route.data', 'w')
    cnt = 0
    for item in s["data"]:
        OriginalJson = getOriginalJson(item["roomId"])
        NewJson = OriginalJson.replace("\\\"", "\"")
        NewJson2 = NewJson.replace("\\\\", "\\")
        # output.writelines(NewJson2)
        # print (str(cnt * 2) + "% :" + ("#" * cnt))
        # print NewJson2
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
                isSelectedPoint(float(point_json['lat']), float(point_json['lng']))

            if (cnt >= 5):
                break


    output.close()

def main():
    getRoomIdJson()

if __name__== '__main__':
    main()