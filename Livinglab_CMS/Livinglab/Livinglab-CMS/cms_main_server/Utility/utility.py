import qrcode
import os
from pathlib import Path
from.network import GetcurrentIP
import os, cv2
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

def createDirectory(directory):

    try:
        if not os.path.exists(directory):
            os.makedirs(directory)

            return directory
    except OSError:
        print('Error: Creating directory. ' + directory)

def CutFilePath(path, string):

    split_path = path.split(string)
    cut_path = split_path[1] + "thumbnail.jpg"
    # print(cut_path)

    return cut_path

def MakeQRcode(id):

    serverIP = GetcurrentIP()
    port_number = str(8000)

    contentQR = "http://" + os.environ['HOST_IP'] + ":" + port_number + "/Userservice/UploadContent/" + str(id)
    communityQR = "http://" + os.environ['HOST_IP'] + ":" + port_number + "/Userservice/AddCommunityComment/" + str(id)

    #contentQR = "http://" + serverIP + ":" + port_number + "/Userservice/UploadContent/" + str(id)
    #communityQR = "http://" + serverIP + ":" + port_number + "/Userservice/AddCommunityComment/" + str(id)

    # http://203.250.33.53:8000/Content/2 http://203.250.33.53:8000/Community/2
    # print("QR address ", contentQR, communityQR)

    contentQR_img = qrcode.make(contentQR)
    communityQR_img = qrcode.make(communityQR)

    contSavePath = MEDIA_ROOT+"/ShelterQR/Content/"+"Shelter_"+str(id)+"/"
    comSavePath = MEDIA_ROOT + "/ShelterQR/Community/" + "Shelter_" + str(id) + "/"

    # print(contSavePath, comSavePath)

    createDirectory(contSavePath)
    createDirectory(comSavePath)

    contentQR_img.save(contSavePath + "contentQR.jpg")
    communityQR_img.save(comSavePath + "communityQR.jpg")

    return contSavePath + "contentQR.jpg", comSavePath + "communityQR.jpg"

def FileTypeCheck(file):
    name, ext = os.path.splitext(file)

    if ext == ".mp4" or ext == ".avi":
        type = "Video"
        return name, type

    elif ext == ".jpg" or ext == ".png" or ext == ".jpeg":
        type = "Image"
        return name, type

def GetFileInfo(file, type):

    if type == "Image":

        imgInfo = Image.open(file)
        name = imgInfo.filename
        format = imgInfo.format
        size = imgInfo.size
        mode = imgInfo.mode
        width = imgInfo.width
        height = imgInfo.height
        HVType = None

        if int(width) > int(height):
            HVType = "landscape"

        elif int(width) < int(height):
            HVType = "portrait"

        elif int(width) == int(height):
            HVType = "square"

        imgDict = {'name': name, 'format': format,
                   'size': size, 'mode': mode,
                   'width': width, 'height': height,
                   'HVType': HVType}

        return imgDict

    else:
        vodInfo = cv2.VideoCapture(file)
        width = vodInfo.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = vodInfo.get(cv2.CAP_PROP_FRAME_HEIGHT)
        HVType = None

        if int(width) > int(height):
            HVType = "landscape"

        elif int(width) < int(height):
            HVType = "portrait"

        elif int(width) == int(height):
            HVType = "square"

        vodDict = {'width': width, 'height': height, 'HVType': HVType}

        return vodDict

def GetThumbnail(path, save_dir):
    vodCap = cv2.VideoCapture(path)

    cnt = 0
    while(vodCap.isOpened()):

        if cnt == 0:
            ret, frame = vodCap.read()
            cv2.imwrite(save_dir+"thumbnail.jpg", frame)

            cnt +=1
        else:
            break
    vodCap.release()
