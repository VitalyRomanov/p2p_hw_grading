# import zipfile
import os
import shutil
import subprocess
import pyminizip
import random
import sys

# cas = "A3"
# mode = "pre_test"
cas = sys.argv[1]
mode = sys.argv[2]

cdir = os.getcwd()
files_path = cdir+"/"+cas+"/"+mode+"/00_feedback/"

files = os.listdir(files_path)


# log = open(files_path+"00_log.txt","r").read()

arc_path = files_path+"/00_arc/"
if not (os.path.isdir(arc_path)):
    os.mkdir(arc_path)

passw = open(files_path+"00_passw.csv","w")

for fl in files:
    if fl[-3:]=="txt":#os.path.isdir(files_path+fl+"/"):
        if fl[0:2] == "00":
            continue
        # start_line = "\n"+"==== "+fl +" start ===="+"\n"
        # end_line = "\n"+"==== "+fl +" end ===="+"\n"
        # start_pos = log.find(start_line)
        # end_pos = log.find(end_line)

        # feedback = open(feedback_path+fl+".txt","w")
        # feedback.write(log[start_pos:end_pos])
        # feedback.close()

        password = repr(int(random.uniform(1000000, 9999999)))
        passw.write(fl[:-4]+","+password+"\n")
        pyminizip.compress(files_path+fl, arc_path+fl[:-4]+".zip", password, 1)
        # os.remove(feedback_path+fl+".txt")

passw.close()
