# coding=utf-8
import requests
import json

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

def getOriginalJson(roomId):
    url = 'http://gxapp.iydsj.com/api/v3/get/'+ str(roomId) + '/history/finished/record '
    Session = requests.Session()
    Request = Session.get(url, headers=headers)
    return Request.content

def getRoomIdJson():
    url = 'http://gxapp.iydsj.com/api/v3/get/aboutrunning/list/80604/901/3'
    Session = requests.Session()
    Request = Session.get(url, headers=headers)
    reqDate = Request.content
    print reqDate
    s = json.loads(Request.content)
    output = open('all.data', 'w')
    cnt = 0
    for item in s["data"]:
        cnt = cnt + 1
        OriginalJson = getOriginalJson(item["roomId"])
        NewJson = OriginalJson.replace("\\\"", "\"")
        NewJson2 = NewJson.replace("\\\\", "\\")
        output.writelines(NewJson2)
        print cnt
        output.writelines(' 0 ')

    output.close()

def main():
    getRoomIdJson()

if __name__== '__main__':
    main()