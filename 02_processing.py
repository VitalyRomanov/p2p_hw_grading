import os
import shutil
import subprocess

# Current assignment
cas = "A2"
mode = "test"

cdir = os.getcwd()
files_path = cdir+"/"+cas+"/"+mode+"/"
verPath = cdir+"/"+cas+"/verification/"
problems = ["01","02","03","04","05"]
files = os.listdir(files_path)


report = open("report.csv","w")

for fl in files:
    cpath = files_path+fl+"/"
    if os.path.isdir(cpath):
        print("\n"+"==== "+fl +" start ===="+"\n")
        for p in problems:
            ver_p = verPath+p+"/"
            use_p = cpath+p+"/"
            if os.path.isdir(use_p):
                print("\n\n\n"+"==== Problem " + p + " start ====\n\n\n")
                shutil.copyfile(ver_p+"verification.py", use_p+"verification.py")
                shutil.copyfile(ver_p+"verification.cpp", use_p+"verification.cpp")
                os.chdir(use_p)
                result = subprocess.run(['python3',use_p+'verification.py'], stdout=subprocess.PIPE)
                output = result.stdout.decode('utf-8')
                grade = output.split('\n')[-2]
                os.chdir(cdir)
                report.write(fl+","+p+","+grade+"\n")
                print("Score "+grade)
                print("\n\n\n"+"==== Problem " + p + " end ====\n\n\n")

        print("\n"+"==== "+fl +" end ===="+"\n")

report.close()
