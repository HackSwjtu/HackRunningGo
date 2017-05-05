import json
import hashlib
import time
config = open('./app.conf')
conf = json.load(config)
config.close()
def getImei():
    return conf['imei']
def getDeviceModel():
    return conf['device_model']
def getMacAdress():
    return conf['mac_address']
def getMD5Key():
    return conf['md5_key']
def getCustomDeviceId():
    if len(conf['customDeviceId'])==0:
        conf['customDeviceId'] = hashlib.md5(str(int(time.time()*1000))+conf['md5_key']).hexdigest().upper() 
        with open('./app.conf','w') as f:
            f.write(json.dumps(conf))
    return conf['customDeviceId']
def getDeviceId():
    if len(conf['deviceId'])==0:
        conf['deviceId'] = hashlib.md5(conf['imei']+conf['device_model']+conf['mac_address']).hexdigest()
        with open('./app.conf','w') as f:
            f.write(json.dumps(conf))
    return conf['deviceId']
def getStartLatLng():
    return conf['startLatLng']
