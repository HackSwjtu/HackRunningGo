<<<<<<< HEAD
# -*- coding:utf-8 -*-
import fileinput
import requests
import json
import base64
import random
import datetime
import re
import time
import hashlib
from Phone import *
import uuid
import codecs

#a time delta to pull back to the history,like a week,a month ago.
KKK_WEEK_MICROSECONDS = 604800000  # the microseconds in a week
KKK_DAY_MICROSECONDS = 86400000 # the microseconds in a day
KKK_TIME_DELTA_MILSEC = 0   #default set to zero,for no history hack
KKK_TIME_DELTA_BEGIN = 0
KKK_TIME_DELTA_END = 0

# Globle Var
file1 = open('route.data')
routes = file1.readlines()
file1.close()

file2 = codecs.open('tp.data', 'r', 'utf-8')
tps = file2.readlines()
file2.close()

#tots = []
#for route in routes:
#    times = re.findall(r'\\\"totalTime\\\"\:(\d+)', route)
#    t = times[len(times) - 1]
#    tots.append(int(t))
# print tots

tot_cnt = len(routes)

def base16encode(username):
    return str(base64.b16encode(username))

def base64encode(username, pwd):
    list = [username, pwd]
    sign = ':'
    strr = sign.join(list)
    return "Basic " + str(base64.b64encode(strr))



def selectRoute():
    return int(random.uniform(0, tot_cnt - 1))

def datetime_to_timestamp_in_milliseconds(d):
    return int(time.mktime(d.timetuple()) * 1000)


def login(username, pwd):
    url = 'http://gxapp.iydsj.com/api/v9/login'
    headers = {
        "Host": "gxapp.iydsj.com",
        "Accept": "application/json",
        "Authorization": base64encode(username, pwd),
        "osType": "0",
        "Content-Type": "application/json",
        "DeviceId": getDeviceId(),
        "CustomDeviceId": getCustomDeviceId(),
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.0; SM-N9002 Build/LRX21V)",
        "appVersion": "1.3.10",
        "timeStamp": str(int(time.time()*1000))
    }

    Session = requests.Session()
    data = {
        "device_model":getDeviceModel(),
        "imei":getImei(),
        "loginType":1,
        "mac_address":getMacAdress(),
        "os_version":"0"
    }
    Request = Session.post(url, headers = headers, data = json.dumps(data))
    reqData = Request.content
    print ('login response: ' + reqData)
    dicData = json.loads(reqData)
    return dicData['data']

def dataUpload(userInfo,KKKKK_TIMEDELTA_MICROSECOND=0):
    url = 'http://gxapp.iydsj.com/api/v10/runnings/add_record'
    timeStamp = str(int(time.time()*1000)- KKKKK_TIMEDELTA_MICROSECOND) 
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
        "deviceName": getDeviceModel(),
        "osType": "0",
        "osVersion": "1.3.10",
        "DeviceId": getDeviceId(),
        "CustomDeviceId": getCustomDeviceId(),
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.0; SM-N9002 Build/LRX21V)",
        "appVersion":"1.3.10",
        "uid":str(dic['uid']),
        "token":dic['token'],
        "tokenSign":digestDict(dic),
        "timeStamp":dic['timeStamp']
    }
    #index = 0
    #while index == 0:
    index = selectRoute()
    print ("Use " + str(index) + " data")
    alllocjson = json.loads(routes[index])
    fivepointjson = json.loads(tps[index])
    allloc = json.loads(alllocjson['allLocJson'])
    fivepoint = json.loads(fivepointjson['fivePointJson'])
    oldflag = allloc[0]['flag']
    totaltime = allloc[len(allloc)-1]['totalTime']
    newflag = int(time.time()*1000) - totaltime*1000 - KKKKK_TIMEDELTA_MICROSECOND
    delta = newflag-oldflag - KKKKK_TIMEDELTA_MICROSECOND
    timedelta = datetime.timedelta(days = int(delta/86400000), seconds = int(delta/1000)%86400, microseconds = delta%1000)
    speedid = int(random.uniform(0, 250))
    stepid = int(random.uniform(0, 250))
    currentdis = 0.0
    currenttime = newflag
    allstep = []
    allspeed = []
    for i in fivepoint:
        i['flag'] = newflag
        #i['pointName'] = 'gogogo'
    for i in allloc:
        i['flag'] = newflag
        oldtime = datetime.datetime.strptime(i['gainTime'],'%Y-%m-%d %H:%M:%S')- datetime.timedelta(microseconds=KKKKK_TIMEDELTA_MICROSECOND)
        newtime = oldtime + timedelta
        #print newtime
        endtime = datetime_to_timestamp_in_milliseconds(newtime) - KKKKK_TIMEDELTA_MICROSECOND
        distance = float(i['totalDis']) - currentdis
        currentdis = float(i['totalDis'])
        i['gainTime'] = newtime.strftime('%Y-%m-%d %H:%M:%S')
        step = {
            "avgDiff": random.uniform(12, 14),
            "beginTime": currenttime,
            "endTime": endtime,
            "flag": newflag,
            "id": stepid,
            "maxDiff": random.uniform(15, 20),
            "minDiff": random.uniform(8, 10),
            "stepsNum": int(distance/0.8)
        }
        allstep.append(step)
        speed = {
            "beginTime": currenttime,
            "distance": distance,
            "endTime": endtime,
            "flag": newflag,
            "id": speedid
        }
        allspeed.append(speed)
        currenttime = endtime
        speedid += 1
        stepid += 1

#    thisdata, st, et = format(routes[index], tots[index])

    # print thisdata
#    totDisA = re.findall(r'\\\"totalDis\\\"\:\\\"(\d+.\d+)\\\"', thisdata)

#    totDis = float(totDisA[len(totDisA) - 1]) / 1000
    # print totDis, tots[index]

#    speed = random.uniform(5, 7)
    # print speed

#    speed_str =  "%.2f" % (speed)
#    totDis_str = "%.2f" % (totDis)

#    print speed_str
#    print totDis_str

    alllocjson['allLocJson'] = json.dumps(allloc)
    fivepointjson['fivePointJson'] = json.dumps(fivepoint, ensure_ascii=False)
    postjson = {
        "allLocJson": json.dumps(alllocjson),
        "sportType": 1,
        "totalTime": totaltime,
        "totalDis": int(currentdis),
        "speed": int(1000/(currentdis/totaltime)/60*1000),
        "startTime": newflag,
        "stopTime": currenttime,
        "fivePointJson": json.dumps(fivepointjson, ensure_ascii=False),
        "complete": True,
        "selDistance": 1,
        "unCompleteReason": 0,
        "getPrize": False,
        "status": 0,
        "uid": userInfo['uid'],
        "avgStepFreq": int(currentdis/1.2/totaltime*60),
        "totalSteps": int(currentdis/1.2),
        "selectedUnid": userInfo['unid'],
        "uuid": str(uuid.uuid1())
    }
    signature = digestDict(postjson)
    postjson['signature'] = signature
    postjson['isUpload'] = False
    postjson['more'] = True
    postjson['roomId'] = 0
    postjson['speedPerTenSec'] = allspeed
    postjson['stepsPerTenSec'] = allstep
#    print json.dumps(postjson)
#    print signature
    Session = requests.Session()
    Request = Session.post(url, headers = headers, data=json.dumps(postjson))
    print ('upload response: ' + Request.content)


def logout(userInfo):
    url = 'http://gxapp.iydsj.com/api/v6/user/logout'
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
#    print headers
    Session = requests.Session()
    Request = Session.post(url, headers = headers)
    print ('logout response: ' + Request.content)

def digestDict(dic):
    keys = dic.keys()
    keys.sort()
    digeststr = u''
    for key in keys:
        if not isinstance(dic[key],bool):
            digeststr = digeststr+unicode(key)+u'='+unicode(dic[key])+u'&'
        else:
            if dic[key]:
                digeststr = digeststr+unicode(key)+u'='+u'true'+u'&'
            else:
                digeststr = digeststr+unicode(key)+u'='+u'false'+u'&'
    digeststr+=u'wh2016_swcampus'
    md5 = hashlib.md5()
    #digeststr = digeststr.encode('utf-8')
    length = len(digeststr)
    count = 0
    while count<length:
        if not ord(digeststr[count])<=0x7F:
            #md5.update(digeststr[count+2])
            codepoint = ord(digeststr[count])
            lowbyte = codepoint - ((codepoint >>8 ) << 8)
            md5.update(chr(lowbyte))
            count+=1
        else:
            md5.update(digeststr[count])
            count+=1
    return md5.hexdigest()
#            charArray.append

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

def modeSelection():
    global KKK_TIME_DELTA_MILSEC
    global KKK_TIME_DELTA_BEGIN
    global KKK_TIME_DELTA_END
    print "Select mode: \n\t1).Hack for todays\n\t2).Hack for history"
    mode = int(input("choose your mode:_____\b\b"))
    if mode == 1:
        #todays mode,delta time set to zero
        return 1
    elif mode == 2:
        #history mode,delta time set by user
        secondary_mode = int(input("Choose history hack mode:\n\t1).Hack for one single day\n\t2).Hack for a time zone\nyour selection:___\b\b"))
        if secondary_mode == 1:
            #hack for one day
            week_before = int(input("Input week(s) before today:____\b\b"))
            which_day = int(input("Input which day in that week you want to hack:_____\b\b"))
            if which_day > 7 or which_day < 0:
                print "INVALIDED DAYS INPUT!IT SHOULD BE BETWEEN 1 TO 7!EXIT!"
                exit()
            KKK_TIME_DELTA_MILSEC = KKK_WEEK_MICROSECONDS*week_before + KKK_DAY_MICROSECONDS*which_day
            return 2
        elif secondary_mode == 2:
            #hack for a time zone
            week_begin = int(input("Input the begining week you want to hack:_____\b\b"))
            day_begin = int(input("Input the day you want to hack in the begining week:_____\b\b"))
            week_end = int(input("Input the ending week you want to hack:_____\b\b"))
            day_end = int(input("Input the day you want to hack in the ending week:_____\b\b"))
            if (day_begin > 7 or day_begin < 0) or (day_end > 7 or day_end < 0):
                print "INVALIDED DAYS INPUT!IT SHOULD BE BETWEEN 1 TO 7!EXIT!"
                exit()
            KKK_TIME_DELTA_BEGIN = KKK_WEEK_MICROSECONDS*week_begin + KKK_DAY_MICROSECONDS*day_begin
            KKK_TIME_DELTA_END = KKK_WEEK_MICROSECONDS*week_end + KKK_DAY_MICROSECONDS*day_end
            return 3
        else:
            print "UNKNOW MODE!EXIT!"
            exit()
    else:
        print "UNKNOW MODE!EXIT!"
        exit()

def main():
    global KKK_TIME_DELTA_MILSEC
    global KKK_TIME_DELTA_BEGIN
    global KKK_TIME_DELTA_END
    users = writeByData()

#    index = selectRoute()
    # format(routes[index], 100)
    for u in users:
        username, password = u.split(' ')
        print username, password
        #mode selection
        mode = modeSelection()
        print "Start : %s" % time.ctime()
        userInfo = login(username, password)
        #hacking by mode
        if mode == 1:
            #hacking today
            print "mode 1"
            try:
                dataUpload(userInfo)
            finally:
                logout(userInfo)
        elif mode == 2:
            #hacking a single sleected day
            print "mode 2"
            try:
                dataUpload(userInfo,KKK_TIME_DELTA_MILSEC)
            finally:
                logout(userInfo)
        elif mode == 3:
            #hacking a day from specified begining to ending
            print "mode 3"
            i = 0
            print KKK_TIME_DELTA_BEGIN,KKK_TIME_DELTA_END
            while KKK_TIME_DELTA_BEGIN >= KKK_TIME_DELTA_END:
                i+=1
                print ">>>Performing the %d hacking on %s" % (i,(datetime.datetime.fromtimestamp(int(time.time())-KKK_TIME_DELTA_BEGIN/1000).strftime('%Y-%m-%d %H:%M:%S')))
                try:
                    dataUpload(userInfo,KKK_TIME_DELTA_BEGIN)
                except:
                    print "error."
                KKK_TIME_DELTA_BEGIN -= KKK_DAY_MICROSECONDS
                sleeptime = random.randint(20, 120)
                print "Sleep %d seconds" % sleeptime
                time.sleep(sleeptime)
            logout(userInfo)
        sleeptime = random.randint(20, 120)
        print "Sleep %d seconds" % sleeptime
        time.sleep(sleeptime)

if __name__== '__main__':
    main()
=======
import fileinput
import requests
import json
import base64
import random
import datetime
import re
import time
import hashlib
from Phone import *
import uuid
import codecs

# Globle Var
file1 = open('route.data')
routes = file1.readlines()
file1.close()

file2 = codecs.open('tp.data', 'r', 'utf-8')
tps = file2.readlines()
file2.close()

#tots = []
#for route in routes:
#    times = re.findall(r'\\\"totalTime\\\"\:(\d+)', route)
#    t = times[len(times) - 1]
#    tots.append(int(t))
# print tots

tot_cnt = len(routes)

def base16encode(username):
    return str(base64.b16encode(username))

def base64encode(username, pwd):
    list = [username, pwd]
    sign = ':'
    strr = sign.join(list)
    return "Basic " + str(base64.b64encode(strr))

#def virtualDevicedId(username):
#    fi = base16encode(username)
#    la = username[1:]
#    id = fi + la
#    res = "%s-%s-%s-%s-%s" % (id[0:8], id[8:12], id[12:16], id[16:20], id[20:])
#    return res

#def virtualCustomDeviceId(username):
#    return virtualDevicedId(username) + "_iOS_sportsWorld_campus"

def selectRoute():
    return int(random.uniform(0, tot_cnt - 1))

def datetime_to_timestamp_in_milliseconds(d):
    return int(time.mktime(d.timetuple()) * 1000)

#def format(data, totTime):
#    data = str(data)
#    res = re.findall(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', data)
#    startTime = res[0]
#    startDate = startTime[0:10]
#    dateToday = datetime.date.today()
#    newData = data.replace(startDate, str(dateToday))

#    startTimeDtObj = datetime.datetime.now() + datetime.timedelta(seconds = -int(totTime))
#    endTimeDtObj = startTimeDtObj + datetime.timedelta(seconds = int(totTime))

    # startTimeDtObj = datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
    # startTimeTiObj = time.strptime(startTime, "%Y-%m-%d %H:%M:%S")
    #st = datetime_to_timestamp_in_milliseconds(startTimeDtObj)
    #et = datetime_to_timestamp_in_milliseconds(endTimeDtObj)
    # newData = data.replace(str(dataDate), str(data_today))

    #res = re.findall(r'\d{13}', newData)
    #newData = newData.replace(res[0], str(st))

    # print("new data: " + newData)
    # print("totTime:  " + str(totTime))
    # print("start:    " + str(st))
    # print("end:      " + str(et))

    #return str(newData), int(st), int(et)


def login(username, pwd):
    url = 'http://gxapp.iydsj.com/api/v9/login'
    headers = {
        "Host": "gxapp.iydsj.com",
        "Accept": "application/json",
        "Authorization": base64encode(username, pwd),
        "osType": "0",
        "Content-Type": "application/json",
        "DeviceId": getDeviceId(),
        "CustomDeviceId": getCustomDeviceId(),
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.0; SM-N9002 Build/LRX21V)",
        "appVersion": "1.3.10",
        "timeStamp": str(int(time.time()*1000))
    }

    Session = requests.Session()
    data = {
        "device_model":getDeviceModel(),
        "imei":getImei(),
        "loginType":1,
        "mac_address":getMacAdress(),
        "os_version":"0"
    }
    Request = Session.post(url, headers = headers, data = json.dumps(data))
    reqData = Request.content
    print ('login response: ' + bytes(reqData).decode('utf-8'))
    dicData = json.loads(reqData)
    return dicData['data']

def dataUpload(userInfo):
    url = 'http://gxapp.iydsj.com/api/v10/runnings/add_record'
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
        "deviceName": getDeviceModel(),
        "osType": "0",
        "osVersion": "1.3.10",
        "DeviceId": getDeviceId(),
        "CustomDeviceId": getCustomDeviceId(),
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.0; SM-N9002 Build/LRX21V)",
        "appVersion":"1.3.10",
        "uid":str(dic['uid']),
        "token":dic['token'],
        "tokenSign":digestDict(dic),
        "timeStamp":dic['timeStamp']
    }
    #index = 0
    #while index == 0:
    index = selectRoute()
    print ("Use " + str(index) + " data")
    alllocjson = json.loads(routes[index])
    fivepointjson = json.loads(tps[index])
    allloc = json.loads(alllocjson['allLocJson'])
    fivepoint = json.loads(fivepointjson['fivePointJson'])
    oldflag = allloc[0]['flag']
    totaltime = allloc[len(allloc)-1]['totalTime']
    newflag = int(time.time()*1000) - totaltime*1000
    delta = newflag-oldflag
    timedelta = datetime.timedelta(days = int(delta/86400000), seconds = int(delta/1000)%86400, microseconds = delta%1000)
    speedid = int(random.uniform(0, 250))
    stepid = int(random.uniform(0, 250))
    currentdis = 0.0
    currenttime = newflag
    allstep = []
    allspeed = []
    for i in fivepoint:
        i['flag'] = newflag
        #i['pointName'] = 'gogogo'
    for i in allloc:
        i['flag'] = newflag
        oldtime = datetime.datetime.strptime(i['gainTime'],'%Y-%m-%d %H:%M:%S')
        newtime = oldtime + timedelta
        #print newtime
        endtime = datetime_to_timestamp_in_milliseconds(newtime)
        distance = float(i['totalDis']) - currentdis
        currentdis = float(i['totalDis'])
        i['gainTime'] = newtime.strftime('%Y-%m-%d %H:%M:%S')
        step = {
            "avgDiff": random.uniform(12, 14),
            "beginTime": currenttime,
            "endTime": endtime,
            "flag": newflag,
            "id": stepid,
            "maxDiff": random.uniform(15, 20),
            "minDiff": random.uniform(8, 10),
            "stepsNum": int(distance/0.8)
        }
        allstep.append(step)
        speed = {
            "beginTime": currenttime,
            "distance": distance,
            "endTime": endtime,
            "flag": newflag,
            "id": speedid
        }
        allspeed.append(speed)
        currenttime = endtime
        speedid += 1
        stepid += 1

#    thisdata, st, et = format(routes[index], tots[index])

    # print thisdata
#    totDisA = re.findall(r'\\\"totalDis\\\"\:\\\"(\d+.\d+)\\\"', thisdata)

#    totDis = float(totDisA[len(totDisA) - 1]) / 1000
    # print totDis, tots[index]

#    speed = random.uniform(5, 7)
    # print speed

#    speed_str =  "%.2f" % (speed)
#    totDis_str = "%.2f" % (totDis)

#    print speed_str
#    print totDis_str

    alllocjson['allLocJson'] = json.dumps(allloc)
    fivepointjson['fivePointJson'] = json.dumps(fivepoint, ensure_ascii=False)
    postjson = {
        "allLocJson": json.dumps(alllocjson),
        "sportType": 1,
        "totalTime": totaltime,
        "totalDis": int(currentdis),
        "speed": int(1000/(currentdis/totaltime)/60*1000),
        "startTime": newflag,
        "stopTime": currenttime,
        "fivePointJson": json.dumps(fivepointjson, ensure_ascii=False),
        "complete": True,
        "selDistance": 1,
        "unCompleteReason": 0,
        "getPrize": False,
        "status": 0,
        "uid": userInfo['uid'],
        "avgStepFreq": int(currentdis/1.2/totaltime*60),
        "totalSteps": int(currentdis/1.2),
        "selectedUnid": userInfo['unid'],
        "uuid": str(uuid.uuid1())
    }
    signature = digestDict(postjson)
    postjson['signature'] = signature
    postjson['isUpload'] = False
    postjson['more'] = True
    postjson['roomId'] = 0
    postjson['speedPerTenSec'] = allspeed
    postjson['stepsPerTenSec'] = allstep
#    print json.dumps(postjson)
#    print signature
    Session = requests.Session()
    Request = Session.post(url, headers = headers, data=json.dumps(postjson))
    print ('upload response: ' + bytes(Request.content).decode('utf-8'))


def logout(userInfo):
    url = 'http://gxapp.iydsj.com/api/v6/user/logout'
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
#    print headers
    Session = requests.Session()
    Request = Session.post(url, headers = headers)
    print ('logout response: ' + bytes(Request.content).decode('utf-8'))

def digestDict(dic):
    keys = dic.keys()
    keys.sort()
    digeststr = u''
    for key in keys:
        if not isinstance(dic[key],bool):
            digeststr = digeststr+unicode(key)+u'='+unicode(dic[key])+u'&'
        else:
            if dic[key]:
                digeststr = digeststr+unicode(key)+u'='+u'true'+u'&'
            else:
                digeststr = digeststr+unicode(key)+u'='+u'false'+u'&'
    digeststr+=u'wh2016_swcampus'
    md5 = hashlib.md5()
    #digeststr = digeststr.encode('utf-8')
    length = len(digeststr)
    count = 0
    while count<length:
        if not ord(digeststr[count])<=0x7F:
            #md5.update(digeststr[count+2])
            codepoint = ord(digeststr[count])
            lowbyte = codepoint - ((codepoint >>8 ) << 8)
            md5.update(chr(lowbyte))
            count+=1
        else:
            md5.update(digeststr[count])
            count+=1
    return md5.hexdigest()
#            charArray.append

def writeByData():
    file = open('user.data', 'r')

    # line = file.readlines()
    line = []
    for l in open('user.data'):
        l = file.readline()
        if l != '\n' and l != '\r' and l!='\r\n':
            line.append(l.strip('\n').strip('\r'))
    # print line
    # for l in line:
    #     user, pwd = l.split(' ')
    #     print (base64encode(user, pwd))
    print line
    file.close()
    return line

def main():
    users = writeByData()

#    index = selectRoute()
    # format(routes[index], 100)
    for u in users:
        username, password = u.split(' ')
        print username, password
        print "Start : %s" % time.ctime()
        userInfo = login(username, password)
        try:
            dataUpload(userInfo)
        finally:
            logout(userInfo)
        sleeptime = random.randint(20, 120)
        print "Sleep %d seconds" % sleeptime
        time.sleep(sleeptime)

if __name__== '__main__':
    main()
>>>>>>> 23373ebd04eb188a4f464777ceb320c7df4348c1
