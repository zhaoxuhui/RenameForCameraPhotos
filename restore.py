# coding=utf-8
import os

if __name__ == '__main__':
    print "-" * 60
    print "Script for restore original names modified by 'rename.py'"
    print "-" * 60 + "\n"

    log_path = raw_input("Input log file path('log.txt' as default):\n")

    if log_path is "":
        log_path = ".\log.txt"

    directory = log_path[:-8]

    log_file = open(log_path)

    line = log_file.readline()
    while True:
        if line is not "":
            now_name = line.split(" ")[-1].strip("\n")
            ori_name = line.split(" ")[1]
            print now_name, " => ", ori_name
            os.rename(directory + os.path.sep + now_name, directory + os.path.sep + ori_name)
            line = log_file.readline()
        else:
            break

    log_file.close()
