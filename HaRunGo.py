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

tots = []
for route in routes:
    times = re.findall(r'\\\"totalTime\\\"\:(\d+)', route)
    t = times[len(times) - 1]
    tots.append(int(t))
# print tots

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
        "Accept": "application/json",
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
        "Content-Type": "application/json;charset=UTF-8",
        "uid": str(uid),
        "Authorization": base64encode(username, pwd),
    }
    index = 0
    while index == 0:
        index = selectRoute()
    print ("Use " + str(index) + " data")

    thisdata, st, et = format(routes[index], tots[index])

    # print thisdata
    totDisA = re.findall(r'\\\"totalDis\\\"\:\\\"(\d+.\d+)\\\"', thisdata)

    totDis = float(totDisA[len(totDisA) - 1]) / 1000
    # print totDis, tots[index]

    speed = random.uniform(5, 7)
    # print speed

    speed_str =  "%.2f" % (speed)
    totDis_str = "%.2f" % (totDis)

    print speed_str
    print totDis_str

    postjson = {
        "allLocJson":thisdata,
        "fivePointJson":tps[index],
        "complete": "true",
        "totalTime": tots[index],
        "totalDis": totDis_str,
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
    Request = Session.post(url, headers = headers, data=json.dumps(postjson))
    print (Request.content)

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
    file = open('user.data', 'r')

    # line = file.readlines()
    line = []
    for l in open('user.data'):
        l = file.readline()
        if l != '\n':
            line.append(l.strip('\n'))
    # print line
    # for l in line:
    #     user, pwd = l.split(' ')
    #     print (base64encode(user, pwd))
    print line
    file.close()
    return line

def main():
    users = writeByData()

    index = selectRoute()
    # format(routes[index], 100)
    for u in users:
        username, password = u.split(' ')
        print username, password
        print "Start : %s" % time.ctime()
        logout(username, password)  

        uid = login(username, password)
        dataUpload(username, password, uid)
        logout(username, password)
        sleeptime = random.randint(20, 120)
        print "Sleep %d seconds" % sleeptime
        time.sleep(sleeptime)

if __name__== '__main__':
    main()
