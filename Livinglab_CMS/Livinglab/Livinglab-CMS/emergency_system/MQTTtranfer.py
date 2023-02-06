import paho.mqtt.client as mqtt
import O2OInfo, time, json
from datetime import datetime

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("disconnect :", str(rc))

# def on_subscribe(client, userdata, mid, granted_qos):
#     print("subscribed: " + str(mid) + " " + str(granted_qos))

def on_publish(client, userdata, mid):
    print("In on_pub callback mid= ", mid)

def on_message(client, userdata, msg):
    print("message received ", str(msg.payload.decode("utf-8")))
    print("message topic=", msg.topic)
    print("message qos=", msg.qos)
    print("message retain flag=", msg.retain)

def EventTime():

    now = datetime.now()
    evtime = now.strftime("%Y%m%d%H%M%S")
    print("evtime",evtime)

    return evtime

def GetPublishData():

    sh_id = O2OInfo.shelterID
    datetime = EventTime()
    event = O2OInfo.event_list['비상벨']

    pub_data = {
        "sh_id": sh_id,
        "datetime": datetime,
        "event": event
    }

    return pub_data

def Transfer(Q2):

    client = mqtt.Client("DCU-EmergencyBell")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    client.on_message = on_message

    client.username_pw_set(O2OInfo.ID, O2OInfo.PW)
    client.connect(O2OInfo.O2OIP, O2OInfo.O2OPORT, 60)

    client.loop_start()
    while True:

        val = Q2.get()

        if val is not None:

            pub_data = GetPublishData()
            print("비상벨 ", val)
            print("pub_data", pub_data)
            pub_data_json = json.dumps(pub_data)
            client.publish('event/S001', pub_data_json)
