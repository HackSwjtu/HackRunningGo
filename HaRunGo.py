import fileinput
import requests
import json
import base64
import random
import datetime
import re
import time

# Globle Var
file1 = open('route.data')
routes = file1.readlines()
file1.close()

file2 = open('tp.data')
tps = file2.readlines()
file2.close()

file3 = open('totTime.data')
tots = file3.readlines()
file3.close()

tot_cnt = len(routes)

def base16encode(username):
    return str(base64.b16encode(username))

def base64encode(username, pwd):
    list = [username, pwd]
    sign = ':'
    strr = sign.join(list)
    return "Basic " + str(base64.b64encode(strr))

def virtualDevicedId(username):
    fi = base16encode(username)
    la = username[1:]
    id = fi + la
    res = "%s-%s-%s-%s-%s" % (id[0:8], id[8:12], id[12:16], id[16:20], id[20:])
    return res

def virtualCustomDeviceId(username):
    return virtualDevicedId(username) + "_iOS_sportsWorld_campus"

def selectRoute():
    return int(random.uniform(0, tot_cnt - 1))

def datetime_to_timestamp_in_milliseconds(d):
    return int(time.mktime(d.timetuple()) * 1000)

def format(data, totTime):
    data = str(data)
    res = re.findall(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', data)
    startTime = res[0]
    startDate = startTime[0:10]
    dateToday = datetime.date.today()
    newData = data.replace(startDate, str(dateToday))

    startTimeDtObj = datetime.datetime.now() + datetime.timedelta(seconds = -int(totTime))
    endTimeDtObj = startTimeDtObj + datetime.timedelta(seconds = int(totTime))

    # startTimeDtObj = datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
    # startTimeTiObj = time.strptime(startTime, "%Y-%m-%d %H:%M:%S")
    st = datetime_to_timestamp_in_milliseconds(startTimeDtObj)
    et = datetime_to_timestamp_in_milliseconds(endTimeDtObj)
    # newData = data.replace(str(dataDate), str(data_today))

    res = re.findall(r'\d{13}', newData)
    newData = newData.replace(res[0], str(st))

    # print("new data: " + newData)
    # print("totTime:  " + str(totTime))
    # print("start:    " + str(st))
    # print("end:      " + str(et))

    return str(newData), int(st), int(et)


def login(username, pwd):
    url = 'http://gxapp.iydsj.com/api/v3/login'
    headers = {
        "Host": "gxapp.iydsj.com",
        "Accept": "*/*",
        "Authorization": base64encode(username, pwd),
        "Proxy-Connection": "keep-alive",
        "osType": "appVersion",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-Hans-CN;q=1",
        "Content-Type": "application/x-www-form-urlencoded",
        "DeviceId": virtualDevicedId(username),
        "CustomDeviceId": virtualCustomDeviceId(username),
        "User-Agent": "SWCampus/1.2.0 (iPhone; iOS 9.3.4; Scale/3.00)",
        "appVersion":"1.2.0"
    }

    Session = requests.Session()
    Request = Session.post(url, headers = headers)
    reqData = Request.content
    print (reqData)
    dicData = json.loads(reqData)
    uid = dicData['data']['uid']
    return uid

def dataUpload(username, pwd, uid):
    url = 'http://gxapp.iydsj.com/api/v2/users/' + str(uid) + '/running_records/add'
    headers = {
        "appVersion": "1.2.1",
        "CustomDeviceId": virtualCustomDeviceId(username),
        "DeviceId": virtualDevicedId(username),
        "osType": "0",
        "source": "000049",
        "uid": str(uid),
        "Authorization": base64encode(username, pwd),
    }
    index = selectRoute()
    print ("Use " + str(index) + " data")

    thisdata, st, et = format(routes[index], tots[index])

    # print thisdata
    totDisA = re.findall(r'\\\"totalDis\\\"\:\\\"(\d+.\d+)\\\"', thisdata)

    totDis = totDisA[len(totDisA) - 1]
    # print totDis, tots[index]

    speed = (float(tots[index]) / 60) / (float(totDis) / 1000)
    # print speed

    speed_str =  "%.2f" % (speed)

    json = {
        "allLocJson":thisdata,
        "fivePointJson":tps[index],
        "complete": "true",
        "totalTime": tots[index],
        "totalDis": totDis,
        "stopTime": et,
        "speed": speed_str,
        "startTime": st,
        "sportType": 1,
        "selDistance": 1,
        "abnormal": 0,
        "isUpload": "false",
        "unCompleteReason": 0
    }
    Session = requests.Session()
    Request = Session.post(url, headers = headers, json = json)
    # print (Request.content)

def logout(username, pwd):
    url = 'http://gxapp.iydsj.com/api/v2/user/logout'
    headers = {
        "Host": "gxapp.iydsj.com",
        "Accept": "*/*",
        "Authorization": base64encode(username, pwd),
        "Proxy-Connection": "keep-alive",
        "osType": "appVersion",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-Hans-CN;q=1",
        "Content-Type": "application/x-www-form-urlencoded",
        "DeviceId": virtualDevicedId(username),
        "CustomDeviceId": virtualCustomDeviceId(username),
        "User-Agent": "SWCampus/1.2.0 (iPhone; iOS 9.3.4; Scale/3.00)",
        "appVersion":"1.2.0"
    }

    Session = requests.Session()
    Request = Session.post(url, headers = headers)
    print Request.content

def writeByData():
    file = open('user.data')

    line = file.readlines()
    # for l in line:
    #     user, pwd = l.split(' ')
    #     print (base64encode(user, pwd))
    file.close()
    return line

def main():
    users = writeByData()

    index = selectRoute()
    # format(routes[index], 100)
    for u in users:
        username, password = u.split(' ')
        print username, password
        uid = login(username, password)
        dataUpload(username, password, uid)
        logout(username, password)


if __name__== '__main__':
    main()