import os
from pathlib import Path

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
    print(cut_path)

    return cut_path