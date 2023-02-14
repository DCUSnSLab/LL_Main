# ftp_server_auth.py
import os
import netifaces as ni

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# FTP_HOST = '203.250.33.53'
FTP_HOST = os.environ['HOST_IP']
FTP_MACHINE = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
FTP_PORT = 9021

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FTP_DIRECTORY = os.path.join(BASE_DIR, 'cms_main_server/media/') # 공유폴더 지정.

def main():
    authorizer = DummyAuthorizer()

    # 서버 실행 시 DB에 접속하여 쉘터 테이블에 있는 쉘터 계정을 불러와야할 듯함=
    # 현재 구현된 코드에서 크게 벗어날 수 없으므로, 우선은 shelter database 계정 명시해서 진행하겠습니다.
    authorizer.add_user('shelter', '20121208', FTP_DIRECTORY, perm='elradfmwMT') #elr
    authorizer.add_anonymous(FTP_DIRECTORY)

    handler = FTPHandler
    handler.banner = "CMS FTP Media Server."

    handler.authorizer = authorizer
    handler.passive_ports = range(60000, 65535)

    address = (FTP_MACHINE, FTP_PORT)
    # address = (FTP_HOST, FTP_PORT)
    print("address")
    server = FTPServer(address, handler)

    print("max_cons")
    server.max_cons = 256
    server.max_cons_per_ip = 5

    print("serve_forever")
    server.serve_forever()

if __name__ == '__main__':
    main()
