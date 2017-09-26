import zipfile
import os
import shutil
import subprocess

# Current assignment
cas = "A4"
mode = "test"

cdir = os.getcwd()
files_path = cdir+"/"+cas+"/"+mode+"/"

files = os.listdir(files_path)



for fl in files:
    if fl[-3:]=="zip":
        name = fl[:fl.find('_')]
        zip_ref = zipfile.ZipFile(files_path+fl, 'r')
        os.mkdir(files_path+name)
        zip_ref.extractall(files_path+name)
        zip_ref.close()
        print fl
