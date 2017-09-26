# import os
# import shutil
# import subprocess
import sys
from MPPAssignment import MPPAssign

# def compile_and_run(path):
#     try:
#         subprocess.check_output(['g++','-Wall','verification.cpp','-o','ver'])
#         result = subprocess.run(['./ver'], stdout=subprocess.PIPE)
#         for line in result.stdout.decode('utf-8').split('\n')[:-1]:
#             if line.split(" ")[-2] == 'score:':
#                 return line.split()[-1]
#
#     except subprocess.CalledProcessError as e:
#         return "-1/Failed to compile"
#     return "-1/Runtime failure"
#     # Need to remove "ver" after it was tested
#
# def copy_verification_files(ver_path,use_path):
#     ver_path_dir = os.listdir(ver_path)
#     ver_files = []
#     for fl in ver_path_dir:
#         if fl[0:6]=="verif_":
#             ver_files.append(fl)
#     for fl in ver_files:
#         shutil.copyfile(ver_path+fl, use_path+fl)
#     return ver_files
#
# def remove_files(use_p,ver_files):
#     for fl in ver_files:
#         os.remove(use_p+fl)
#
# def get_problems_list(assignm_path):
#     prob_list = os.listdir(assignm_path)
#     for s in prob_list:
#         try:
#             prob = int(s)
#             if prob<0 or prob>=10:
#                 prob_list.remove(s)
#         except ValueError:
#             prob_list.remove(s)
#     return prob_list
#
# def standardize(problem):
#     prob = int(problem)
#     p = "0"+repr(prob)
#     return p

# Current assignment
# cas = "A3"
# mode = "pre_test"
cas = sys.argv[1]
mode = sys.argv[2]

MPP = MPPAssign(cas,mode)

# for p in MPP.problems:
#     print(MPP.problems[p].max_score)

# st = MPP.students[0]
# MPP.grade_student(st)
# print(st.grade)
# st.create_report(MPP.path+"/"+"00_feedback")



MPP.grade_students()
MPP.create_grade_report()

# for p in assing.problems:
#     pk = assing.problems[p]
#     print(repr(pk.folder)+" "+pk.path+" "+repr(pk.tests))
# # print(assing.students)
# for stud in assing.students:
#     print(stud.name)
#     print(stud.path+" "+repr(os.path.isdir(stud.path)))
#     print(stud.solved_problems)
#     print(stud.grade)
#     print(stud.issues)
#     print(stud.feedback)
#     print("")

# print(assing.students[0].name)
#


# for k1 in assing.students[0].comp_out:
#     for k2 in assing.students[0].comp_out[k1]:
#         print("Problem ",k1," Test 1 ",assing.students[0].comp_out[k1][k2]," ",k2," ",assing.students[0].exec_out[k1][k2])

# assing.students[0].create_report(assing.path+"/"+"00_feedback")


# cdir = os.getcwd()
# files_path = cdir+"/"+cas+"/"+mode+"/"
# verPath = cdir+"/"+cas+"/verification/"
# # problems = ["01","02","03","04","05"]
# files = os.listdir(files_path)





# report = open("report.csv","w")
#
#
#
# for fl in files:
#     if fl[0:2] == "00": continue
#     cpath = files_path+fl+"/"
#     if os.path.isdir(cpath):
#         print("\n"+"==== "+fl +" start ===="+"\n")
#         for p in get_problems_list(cpath):
#             ver_p = verPath+standardize(p)+"/"       # path with verification files
#             use_p = cpath+p+"/"         # path with submitted files
#             if os.path.isdir(use_p):
#                 print("\n\n"+"==== Problem " + p + " start ====\n\n")
#                 ver_files = copy_verification_files(ver_p,use_p)
#                 remove_files(use_p,ver_files)
#                 # shutil.copyfile(ver_p+"verification.cpp", use_p+"verification.cpp")
#                 # os.chdir(use_p)
#                 # grade = compile_and_run(use_p)
#                 # os.chdir(cdir)
#                 # report.write(fl+","+p+","+grade+"\n")
#                 # print("Score " + grade)
#                 # print("\n\n"+"==== Problem " + p + " end ====\n\n")
#
#         print("\n"+"==== "+fl +" end ===="+"\n")
#
# report.close()
