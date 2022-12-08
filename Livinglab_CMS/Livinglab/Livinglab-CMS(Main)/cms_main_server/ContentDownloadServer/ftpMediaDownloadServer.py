# ftp_server_auth.py
import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

FTP_HOST = '203.250.33.53'
FTP_PORT = 9021

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FTP_DIRECTORY = os.path.join(BASE_DIR, 'cms_main_server/media/') # 공유폴더 지정.

def main():
    authorizer = DummyAuthorizer()

    # 서버 실행 시 DB에 접속하여 쉘터 테이블에 있는 쉘터 계정을 불러와야할 듯함=
    authorizer.add_user('shelter01', 'shelterPW', FTP_DIRECTORY, perm='elradfmwMT') #elr
    authorizer.add_anonymous(FTP_DIRECTORY)

    handler = FTPHandler
    handler.banner = "CMS FTP Media Server."

    handler.authorizer = authorizer
    handler.passive_ports = range(60000, 65535)

    address = (FTP_HOST, FTP_PORT)
    server = FTPServer(address, handler)

    server.max_cons = 256
    server.max_cons_per_ip = 5

    server.serve_forever()

if __name__ == '__main__':
    main()
