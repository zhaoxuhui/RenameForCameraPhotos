# coding=utf-8
from PIL import Image
from PIL.ExifTags import TAGS
import os


def findAllFiles(root_dir, filter):
    """
    遍历搜索文件

    :param root_dir:搜索目录
    :param filter: 搜索文件类型
    :return: 路径、文件名、路径+文件名
    """
    print("Finding files ends with \'" + filter + "\' ...")
    separator = os.path.sep
    paths = []
    names = []
    files = []
    # 遍历
    for parent, dirname, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(filter):
                paths.append(parent + separator)
                names.append(filename)
    for i in range(paths.__len__()):
        files.append(paths[i] + names[i])
    print (names.__len__().__str__() + " files have been found.")
    paths.sort()
    names.sort()
    files.sort()
    return paths, names, files


def get_exif_data(fname):
    """
    获取EXIF信息

    :param fname: 影像文件路径
    :return: 字典类型的EXIF信息
    """
    ret = {}
    try:
        img = Image.open(fname)
        if hasattr(img, '_getexif'):
            exifinfo = img._getexif()
            if exifinfo != None:
                for tag, value in exifinfo.items():
                    decoded = TAGS.get(tag, tag)
                    ret[decoded] = value
    except IOError:
        print 'IOERROR ' + fname
    return ret


def decodeTime(time_info):
    ymd = time_info.split(" ")[0]
    hms = time_info.split(" ")[1]
    year = ymd.split(":")[0]
    month = ymd.split(":")[1]
    day = ymd.split(":")[2]
    hour = hms.split(":")[0]
    minute = hms.split(":")[1]
    second = hms.split(":")[2]
    return year, month, day, hour, minute, second


def getTimeInfo(filename):
    """
    获取EXIF中的时间信息

    :param filename: 影像路径
    :return: 字符串类型的时间信息
    """

    exif = get_exif_data(filename)
    if exif.has_key('DateTime'):
        time_info = exif.get('DateTime')
        return time_info
    else:
        return "No Time."


def composeFileName(directory, sep_time):
    base = directory + os.path.sep + \
           "IMG_" + sep_time[0] + sep_time[1] + sep_time[2] + "_" + \
           sep_time[3] + sep_time[4] + sep_time[5]
    file_name = base + ".jpg"
    counter = 0
    while True:
        if os.path.exists(file_name):
            counter += 1
            file_name = base + "_" + counter.__str__().zfill(2) + ".jpg"
        else:
            break
    return file_name


if __name__ == '__main__':
    print "-" * 60
    print "Rename script for camera photos."
    print "-" * 60 + "\n"

    directory = raw_input("Input directory of images('.' as default):\n")

    file_type = raw_input("Input image type('.JPG' as default):\n")

    if directory is "":
        directory = "."

    if file_type is "":
        file_type = ".JPG"

    paths, names, files = findAllFiles(directory, file_type)

    save_file = open(paths[0] + os.path.sep + "log.txt", 'w+')

    for i in range(names.__len__()):
        time = getTimeInfo(files[i])
        res = decodeTime(time)
        new_name = composeFileName(paths[0], res)
        out_line = (i + 1).__str__().zfill(4) + "/" + names.__len__().__str__().zfill(4) + " " + \
                   names[i] + " => " + new_name.split("\\")[-1]
        save_file.write(out_line + "\n")
        print out_line
        os.rename(files[i], new_name)

    save_file.close()
    print "Name change log saved in", paths[0] + os.path.sep + "log.txt"
