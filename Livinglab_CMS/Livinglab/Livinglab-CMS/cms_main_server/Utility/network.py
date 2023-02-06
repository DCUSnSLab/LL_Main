
import socket

def GetcurrentIP():
    val = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    val.connect(("8.8.8.8", 80))
    print("현재 IP 주소 : ", val.getsockname()[0])

    return val.getsockname()[0]


