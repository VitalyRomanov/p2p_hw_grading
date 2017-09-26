import os
import shutil
from subprocess import Popen, PIPE

def compile_and_run(path_fname):
    score = 0
    # comp = Popen(['g++',path_fname,'-o',path_fname[:-4]], stdout=PIPE, stderr=PIPE)
    comp = Popen(['/usr/local/Cellar/gcc/7.2.0/bin/g++-7','-std=c++14',path_fname,'-o',path_fname[:-4]], stdout=PIPE, stderr=PIPE)
    comp_err_out, comp_err = comp.communicate()
    if os.path.isfile(path_fname[:-4]):
        execu = Popen([path_fname[:-4]], stdout=PIPE, stderr=PIPE)
        execu_out, execu_err = execu.communicate()
        for line in execu_out.decode('utf-8').split('\n')[:-1]:
            words = line.split(" ")
            if len(words)>1:
                if words[-2] == 'score:':
                    score = int(line.split()[-1].split("/")[0])
    else:
        execu_err = "".encode('utf-8')
        execu_out = "".encode('utf-8')
    return score,execu_out,execu_err,comp_err


def get_problems_list(path):
    prob_list = os.listdir(path)
    plist = []
    for s in prob_list:
        try:
            prob = int(s)
            if not (prob<0 or prob>=10):
                # prob_list.remove(s)
                plist.append(s)
        except ValueError:
            continue
            # prob_list.remove(s)
    # print(plist)
    return plist

def get_verification_files(ver_path):
    ver_path_dir = os.listdir(ver_path)
    ver_files = []
    for fl in ver_path_dir:
        if fl[0:6]=="verif_":
            ver_files.append(fl)
    return ver_files

def get_student_list(path):
    fls = os.listdir(path)
    students = []
    for fl in fls:
        if fl[0:2] == "00": continue
        if os.path.isdir(path+"/"+fl):
            students.append(fl)
    return students

class MPPAssign:
    def __init__(self,asgm,mode):
        cdir = os.getcwd()
        if not os.path.isdir(cdir+"/"+asgm):
            raise Exception("No assignment "+asgm)
        self.assign = int(asgm[1])
        self.path = cdir+"/"+asgm
        if not os.path.isdir(self.path+"/"+mode):
            raise Exception("No files for the mode: "+mode)
        self.mode = mode
        self.testing_dir = self.path+"/"+mode
        if not os.path.isdir(self.path+"/verification"):
            raise Exception("No verification files found")
        self.ver_path = self.path+"/verification"
        self.problems = dict()
        self.max_score = 0
        for p in get_problems_list(self.ver_path):
            self.problems[int(p)] = Problem(p,self.ver_path)
            self.max_score += self.problems[int(p)].max_score
        self.students = [Student(stud,self.testing_dir) for stud in get_student_list(self.testing_dir)]

    def grade_students(self):
        for i,s in enumerate(self.students):
            print(i+1,"/",len(self.students)," ",s.name)
            self.grade_student(s)
            s.create_report(self.path+"/"+self.mode+"/"+"00_feedback")

    def grade_student(self,s):
        for p in s.solved_problems:
            self.copy_tests(s,self.problems[p])
            self.compile_test(s,self.problems[p])
            self.delete_tests(s,self.problems[p])
        s.grade = s.grade#*100./self.max_score

    def copy_tests(self,s,prbl):
        for test in prbl.tests:
            shutil.copyfile(prbl.path+test,s.path+"/"+s.solved_problems[prbl.id]+"/"+test)
    def delete_tests(self,s,prbl):
        for test in prbl.tests:
            os.remove(s.path+"/"+s.solved_problems[prbl.id]+"/"+test)

    def compile_test(self,stud,prbl):
        stud.comp_err_out[int(prbl.folder)] = dict()
        stud.exec_err_out[int(prbl.folder)] = dict()
        stud.exec_out[int(prbl.folder)] = dict()
        stud.score[int(prbl.folder)] = dict()
        score = 0.
        for i,test in enumerate(prbl.tests):
            target_path = stud.path+"/"+stud.solved_problems[prbl.id]+"/"+test
            s,out,e_out,c_out = compile_and_run(target_path)
            if os.path.isfile(target_path[:-4]):
                os.remove(target_path[:-4])
            # print(repr(s)+" "+repr(e_out)+" "+repr(c_out))
            score += s
            stud.comp_err_out[int(prbl.folder)][i+1] = c_out
            stud.exec_err_out[int(prbl.folder)][i+1] = e_out
            stud.exec_out[int(prbl.folder)][i+1] = out
            stud.score[int(prbl.folder)][i+1] = s
        stud.grade += prbl.get_score(score)
        # print(prbl.folder,stud.grade)

    def create_grade_report(self):
        with open(self.path+"/"+self.mode+"/"+"00_report.csv","w") as report:
            for student in self.students:
                report.write(student.name+","+repr(student.grade)+"\n")






class Problem:
    def __init__(self,problem,path):
        self.path = path+"/"+problem+"/"
        self.folder = problem
        self.id = int(problem)
        self.tests = dict.fromkeys(get_verification_files(self.path))
        for test in self.tests:
            self.tests[test] = self.get_test_description(test)
        self.max_score = self.read_max_score()

    def read_max_score(self):
        with open(self.path+"description.txt") as desc:
            return float(desc.readline().split(" ")[1])

    def get_score(self,n_solved):
        return self.max_score*n_solved/len(self.tests)


    def get_test_description(self,test):
        with open(self.path+test) as tfile:
            return tfile.readline()[2:-1]


class Student:
    def __init__(self,name,path):
        self.name = name
        self.path = path+"/"+name
        # self.solved_problems = [int(p) for p in get_problems_list(self.path)]
        self.solved_problems = dict()
        for p in get_problems_list(self.path):
            self.solved_problems[int(p)] = p
        self.grade = 0.
        self.issues = ""
        self.comp_err_out = dict.fromkeys(self.solved_problems.keys())
        self.exec_err_out = dict.fromkeys(self.solved_problems.keys())
        self.exec_out = dict.fromkeys(self.solved_problems.keys())
        self.score = dict.fromkeys(self.solved_problems.keys())

    def create_report(self,path):
        if not os.path.isdir(path):
            os.mkdir(path)
        with open(path+"/"+self.name+".txt","w") as srep:
            for problem in self.comp_err_out:
                srep.write("=====================================================")
                srep.write("=====================================================\n")

                for test in self.comp_err_out[problem]:
                    srep.write("= PROBLEM "+repr(problem)+" TEST "+repr(test)+" =\n")
                    # srep.write("\n====== Test "+repr(test)+" start ======\n\n")
                    srep.write("COMPILER OUTPUT:\n")
                    srep.write(self.comp_err_out[problem][test].decode('utf-8'))
                    srep.write("\n\nAPPLICATION OUTPUT:\n")
                    srep.write(self.exec_out[problem][test].decode('utf-8'))
                    srep.write("\n")
                    srep.write(self.exec_err_out[problem][test].decode('utf-8'))
                    # srep.write("====== Test "+repr(test)+" end ======\n\n")
                    if self.score[problem][test]:
                        srep.write("\n"+"TEST PASSED"+"\n\n")
                    else:
                        srep.write("\n"+"TEST FAILED"+"\n\n")
                # srep.write("====== Problem "+repr(problem)+" end ======\n\n")
