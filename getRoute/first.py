# coding=utf-8
import fileinput
import requests
import json
import base64
import random
import datetime
import re
import time

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


def login(username, pwd):
    url = 'http://gxapp.iydsj.com/api/v3/login'
    headers = {
        "Host": "gxapp.iydsj.com",
        "Accept": "application/json",
        "Authorization": base64encode(username, pwd),
        "Proxy-Connection": "keep-alive",
        "osType": "0",
        "Accept-Encoding": "gzip",
        "Accept-Language": "zh-Hans-CN;q=1",
        "Content-Type": "Keep-Alive",
        "DeviceId": "1F5576C69162C0D40D54B2F804CBF370",
        "CustomDeviceId": "357413306433247",
        "User-Agent": "Dalvik/1.6.0 (Linux; U; Android 4.4.4; R7c Build/KTU84P)",
        "appVersion": "1.2.1",
        "source": "000049"
    }
    return 105
    #Session = requests.Session()
    #Request = Session.post(url, headers = headers)
    #reqData = Request.content
    #print (reqData)
    #dicData = json.loads(reqData)
    #uid = dicData['data']['uid']
    #return uid

def logout(username, pwd):
    url = 'http://gxapp.iydsj.com/api/v2/user/logout'
    headers = {
        "Host": "gxapp.iydsj.com",
        "Accept": "application/json",
        "Authorization": base64encode(username, pwd),
        "Proxy-Connection": "keep-alive",
        "osType": "0",
        "Accept-Encoding": "gzip",
        "Accept-Language": "zh-Hans-CN;q=1",
        "Content-Type": "Keep-Alive",
        "DeviceId": "1F5576C69162C0D40D54B2F804CBF370",
        "CustomDeviceId": "357413306433247",
        "User-Agent": "Dalvik/1.6.0 (Linux; U; Android 4.4.4; R7c Build/KTU84P)",
        "appVersion":"1.2.1",
        "source":"000049"
    }

    Session = requests.Session()
    Request = Session.post(url, headers = headers)
    print Request.content

def writeByData():
    file = open('user.data')

    line = file.readlines()

    file.close()
    return line

def getOriginalJson(roomId,uid,username,pwd):
    url = 'http://gxapp.iydsj.com/api/v3/get/'+ str(roomId) + '/history/finished/record '
    headers = {
        "Host": "gxapp.iydsj.com",
        "Accept": "application/json",
        "Authorization": base64encode(username, pwd),
        "Proxy-Connection": "keep-alive",
        "osType": "0",
        "Accept-Encoding": "gzip",
        "Accept-Language": "zh-Hans-CN;q=1",
        "Content-Type": "Keep-Alive",
        "DeviceId": "1F5576C69162C0D40D54B2F804CBF370",
        "CustomDeviceId": "357413306433247",
        "User-Agent": "Dalvik/1.6.0 (Linux; U; Android 4.4.4; R7c Build/KTU84P)",
        "appVersion": "1.2.1",
        "source": "000049"
    }
    Session = requests.Session()
    Request = Session.get(url, headers=headers)
    return Request.content

def getRoomIdJson(uid,username,pwd):
    url = 'http://gxapp.iydsj.com/api/v3/get/aboutrunning/list/' + str(uid) + '/901/3'
    headers = {
        "Host": "gxapp.iydsj.com",
        "Accept": "application/json",
        "Authorization": base64encode(username, pwd),
        "Proxy-Connection": "keep-alive",
        "osType": "0",
        "Accept-Encoding": "gzip",
        "Accept-Language": "zh-Hans-CN;q=1",
        "Content-Type": "Keep-Alive",
        "DeviceId": "1F5576C69162C0D40D54B2F804CBF370",
        "CustomDeviceId": "357413306433247",
        "User-Agent": "Dalvik/1.6.0 (Linux; U; Android 4.4.4; R7c Build/KTU84P)",
        "appVersion": "1.2.1",
        "source": "000049"
    }
    Session = requests.Session()
    Request = Session.get(url, headers=headers)
    reqDate = Request.content
    print reqDate
    s = json.loads(Request.content)
    output = open('all.data', 'w')
    cnt = 0
    for item in s["data"]:
        #print item["roomId"]
        cnt = cnt + 1
        OriginalJson = getOriginalJson(item["roomId"],uid,username,pwd)
        NewJson = OriginalJson.replace("\\\"", "\"")
        NewJson2 = NewJson.replace("\\\\", "\\")
        output.writelines(NewJson2)
        print cnt
        output.writelines(' 0 ')

    output.close()

def main():
    users = writeByData()

    for u in users:
        username, password = u.split(' ')
        uid = login(username, password)
        getRoomIdJson(uid,username ,password)
        logout(username, password)

if __name__== '__main__':
    main()