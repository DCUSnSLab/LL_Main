import ftplib
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# CMS 공유 디렉토리
FTP_DIRECTORY = os.path.join(BASE_DIR, 'cms_main_server/media/')

def MediaDownload(fileDir): # 이거 코드 중복 수정. 조건문 왜 안되지!!!!이거 이미지, 동영상, 커뮤니티 댓글, 이미지 다 될수있도록 수정

    # 하드코딩 요소로 추후 수정요망
    serverIP = "203.250.33.53"
    serverPort = 9021

    clientID = "shelter01"
    clientPW = "shelterPW"

    ftp = ftplib.FTP()
    ftp.connect(serverIP, serverPort)
    ftp.login(clientID, clientPW)

    print("동기화 파일 경로", fileDir)

    dir, file = os.path.split(fileDir)

    print("dir, file", dir, file)

    ftp.cwd('/'+ dir)

    # ftp.retrbinary(cmd, file): 파일을 바이너리로 다운로드 한다.
    # [cmd] 'RETR filename' 로 RETR은 정적이며 filename은 ftp에 있는 파일명이다.
    # [file] 다운로드할 파일
    SHELTER_DIR = os.path.join(BASE_DIR, 'local_shelter_server/media/')
    DOWNLOAD_DIR = os.path.join(SHELTER_DIR, dir)

    os.makedirs(DOWNLOAD_DIR)
    fd = open(DOWNLOAD_DIR + '/' + file, 'wb')
    ftp.retrbinary('RETR %s' % file, fd.write)
    fd.close()

    print("Check Downloaded")


