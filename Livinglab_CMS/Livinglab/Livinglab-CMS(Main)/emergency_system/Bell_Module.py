import sys, glob, serial    # 시리얼 포트 자동 찾기
import platform             # 운영체제 정보 확인
import pymysql              # MySQL 연결
import Alert as at          # 비상경보
import time, threading, json, argparse
import requests, re         # 연결 PC의 IP 주소 파악
# from multiprocessing import Queue
from queue import Queue
import MQTTtranfer as MQ
from collections import OrderedDict
import O2OInfo

def main():

    # parser = argparse.ArgumentParser(description='Argument 객체')
    # parser.add_argument('-ip', type=str, help='central server ip for data trafer') # 호출데이터 전송할 서버 IP
    # parser.add_argument('-port', type=int, help='central server port for data trafer')
    # args = parser.parse_args()  # 입력 Argument들을 args에 할당, argument 값 저장

    # ip = args.ip
    # port = args.port
    # print("ip : ", ip, "type : ", type(ip), "port : ", port, "type : ", type(port))

    # DB = SettingDB(ip, port)
    # deviceLoc = FindDevLoc(DB)
    # print("현재 시설명 : ", deviceLoc)

    que1 = Queue()
    que2 = Queue()
    ArduSerial = None
    try:
        ard_reciver = SerialFinder()            # 현재 연결된 모듈의 시리얼 포트 찾기
        OSINFO = CheckOS(ard_reciver)           # 연결 모듈의 OS 확인
        print(' The serial version            : ' + serial.__version__)
        print(' The current OS information    : ' + OSINFO[0])
        print(' The current OS name           : ' + OSINFO[1])
        print(' The current OS release number : ' + OSINFO[2])
        print(" The current Port information  : " + OSINFO[3])

        # 아두이노 시리얼 통신 설정
        osValue = OSINFO[1]
        serialValue = OSINFO[3]
        PORT = str(serialValue)
        BaudRate = 9600
        ArduSerial = serial.Serial(PORT, BaudRate)

    except Exception as e:
        print("현재 비상벨모듈이 연결되어 있지 않습니다.", e)

    serialTranferThread = threading.Thread(target=SerialTranfer, args=(ArduSerial, que1, que2))
    AlertThread = threading.Thread(target=at.Alert, args=(que1, ))
    MQTTransfer = threading.Thread(target=MQ.Transfer, args=(que2,))

    serialTranferThread.start()
    AlertThread.start()
    MQTTransfer.start()
    serialTranferThread.join()
    AlertThread.join()
    MQTTransfer.join()


def SettingDB(ip, port):

    DB = pymysql.connect(  # 데이터베이스 설정
        host=ip,
        port=port,
        user="root",
        passwd='0110',
        db="livinglabdb",
        charset='utf8')

    return DB

def FindDevLoc(DB):

    req = requests.get("http://ipconfig.kr")
    ip = re.search(r'IP Address : (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', req.text)[1]
    # print("외부 IP : ", ip, type(ip))

    try:
        with DB.cursor() as cursor:  #  MySQL 데이터베이스 객체 생성 control structure of database

            query_name = 'SELECT name FROM managesystem_facility WHERE IP_address=%s'
            cursor.execute(query_name, (ip))
            rows = cursor.fetchall()
            # print(rows[0][0])
            DB.commit()
            return rows[0][0]
    finally:
        pass

def CheckOS(ard_reciver):
    osinfo = platform.platform()        # 현재 OS 정보
    osType = platform.system()          # 현재 OS 이름
    osRelVersion = platform.release()   # 현재 OS release 넘버

    serialVal = []
    if osType == "Windows":
        serialVal = ard_reciver[0]
    elif osType == "Linux":
        serialVal = ard_reciver[0]

    return osinfo, osType, osRelVersion, serialVal

def SerialFinder(): # 현재 연결된 비상벨모듈의 시링얼 포트번호를 가져옴

    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)

        except (OSError, serial.SerialException):
            pass
    return result

def Insert2DB(crnt_loc, crnt_time, DB):

    try:
        with DB.cursor() as cursor:  #  MySQL 데이터베이스 객체 생성 control structure of database

            query_name = 'SELECT id FROM managesystem_facility WHERE name=%s'
            cursor.execute(query_name, (crnt_loc))
            rows = cursor.fetchall()
            print(rows[0][0])
            DB.commit()

            query_call = """
                INSERT INTO managesystem_emergencybell (name, callDate, facilityFK) VALUES(%s, %s, %s)
            """
            val = (crnt_loc, crnt_time, rows[0][0])
            cursor.execute(query_call, val)

            DB.commit()

    finally:
        pass

def SerialTranfer(ArduSerial, que1 ,que2, deviceLoc=None, DB=None): # 비상벨 모듈의 호출 신호 수신

    while(True):
        event = ArduSerial.readline()         # 이벤트 여부

        if event is not None:
            evt = str(event)
            evt = evt.split('\'')[1]
            evt = evt.split('\\')[0]
            que1.put(evt)
            que2.put(1)

            # Insert2DB(deviceLoc, current_time, DB)
            # SendMessage2Facil(evt, deviceLoc, current_time)
        # else:
        #     pass

if __name__ == '__main__':
    main()

