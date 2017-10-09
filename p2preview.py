from collections import Counter
from random import uniform
from numpy import random
import pandas as df
from p7zipfile import p7zipfile
from moodle_report_v2 import MoodleRep
import datetime
import shutil
import copy
import time
import sys
import os

from student import Student
from anumstring import get_passw


max_p = 3


def mkdir_if_not_exist(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def get_student_list(path):
    fls = os.listdir(path)
    students = []
    for fl in fls:
        if fl[0:2] == "00": continue
        if os.path.isdir(path+"/"+fl):
            students.append(fl)
    return students

class p2pRev:
    def __init__(self,c_path,asgm,mode,arrby):
        # check that all paths exist
        self.check_directories(c_path,asgm,mode)
        # nop : number of problems solved
        # max_problems : maximum number of problems solved by a student. x3 will
        # be the number that a student should review
        # arr : stores the type of arrangement {by_problemms, by_Students}
        self.nop = 0
        self.max_problems = 0
        self.arr = arrby
        # Analyze students and their submitted problem
        self.students = [Student(stud,self.testing_dir) for stud in get_student_list(self.testing_dir)]
        self.check_empty_students()
        self.update_student_index()


        for s in self.students:
            self.nop += len(s.solved_problems) # calculate num of solved problems
            if self.max_problems < len(s.solved_problems): self.max_problems = len(s.solved_problems) # get max solved problems

        print("MP: ",self.max_problems)


        self.s_passw = {} # Stores passwords for students

        self.problem_ids = set([0]) # create a dummy problem id

        self.records = self.prepare_prob_db()
        # problem_skip_list stores problems that were solved by less than
        # max_p of sudents
        self.problem_skip_list = []
        self.update_problem_index()

        st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M')
        self.target_dir = self.path + "/" + self.mode + "_" + st
        mkdir_if_not_exist(self.target_dir)

    def check_directories(self,c_path,asgm,mode):
        if not os.path.isdir(c_path+"/"+asgm):
            raise Exception("No assignment "+asgm)
        self.assign = int(asgm[1])
        self.path = c_path+"/"+asgm
        if not os.path.isdir(self.path+"/"+mode):
            raise Exception("No files for the mode: "+mode)
        self.mode = mode
        self.testing_dir = self.path+"/"+mode


    def update_student_index(self):
        self.s_ind = {}
        for s in self.students:
            # id's for students are one symbol longer
            s_id = int(uniform(10000000, 99999999))
            self.s_ind[s.name] = {'id':s_id,'info':s,'iby':[]}

    def create_stud_index(self,students):
        s_ind = {}
        for s in students:
            # id's for students are one symbol longer
            s_id = int(uniform(10000000, 99999999))
            s_ind[s.name] = {'id':s_id,'info':s,'iby':[]}
        return s_ind

    def update_problem_index(self):
        self.p_ind = {}
        for p in self.records.ix[:,"Problem"].unique():
            self.p_ind[p] = self.records.loc[self.records['Problem']==p,:]
            if self.p_ind[p].shape[0]<max_p:
                self.problem_skip_list.append(p)

    def check_empty_students(self):
        for stud in self.students:
            if len(stud.solved_problems) == 0:
                print("Check : %s"%stud.name)



    def prepare_prob_db(self):
        records = []
        for student in self.students:
            for p_key in student.solved_problems:
                # create a unique id for all solved problems bu all students
                p_id = 0
                while p_id in self.problem_ids:
                    p_id = int(uniform(1000000, 9999999))
                record = {"id":p_id,
                            "Name":student.name,
                            "Problem":student.solved_problems[p_key],
                            "inspected_by":[]}
                records.append(record)
        # convert list of dicts to dataframe
        records_df = df.DataFrame(records,columns=["id","Name","Problem","inspected_by"])
        return records_df


    def arrange(self):
        for attempt in range(1000):
            # errors keeps the problems that were not assigned enouth times
            errors = []
            # create local copies of objects
            c_records = copy.deepcopy(self.records)
            c_students = copy.deepcopy(self.students)
            # iterate over all problems
            if self.arr == 'p':
                self.assign_problems(c_records,c_students,errors)
            elif self.arr == 's':
                self.s_ind = self.assign_students(c_records,c_students,errors)
            else:
                raise NotImplemented

            print("Iteration %d errors : %d"%(attempt+1,len(errors)))
            if len(errors) == 0: break

        # Store final results
        print("%d errors occurred"%len(errors))
        self.records = c_records
        self.students = c_students
        # self.update_student_index()
        # Dump all error messages into a file
        self.dump_errors(errors)


    def assign_students(self,c_records,c_students,errors):
        s_ind = self.create_stud_index(c_students)
        for assignee in s_ind:
            list_of_stud = list(s_ind.keys())
            for j in range(max_p):
                assigned = False
                while not assigned and len(list_of_stud)!=0:
                    s_id = random.choice(list_of_stud)
                    list_of_stud.remove(s_id)
                    c_stud = s_ind[s_id]['info']
                    if c_stud.can_assign_stud(assignee):
                        if len(c_stud.checks_s) < 3:
                            c_stud.assign_stud(assignee)
                            s_ind[assignee]['iby'].append(c_stud.name)
                            assigned = True
                if len(list_of_stud)==0:
                    errors.append("Failed to assign %s\n"%(assignee))
        return s_ind


    def assign_problems(self,c_records,c_students,errors):
        for i in range(c_records.shape[0]):
            # Prepare the list of students to assign problems to them. If none of
            # them satisfied the criteria, we failed to assign the problem
            list_of_stud = list(range(len(c_students)))
            p_id,s_to_assign,p_to_assign = c_records.loc[i,["id","Name","Problem"]]
            c_records.set_value(i,"inspected_by",[])
            if p_to_assign in self.problem_skip_list: continue
            # Assign a problem to max_p people
            for j in range(max_p):
                assigned = False
                # iterate until assigned or failed to assign
                while not assigned and len(list_of_stud)!=0:
                    s_id = random.choice(list_of_stud)
                    list_of_stud.remove(s_id)
                    c_stud = c_students[s_id]
                    if c_stud.can_assign(s_to_assign,p_to_assign,max_p):
                        c_stud.assign(s_to_assign,p_to_assign,p_id)
                        # the fact of assignment is reflected in records
                        c_records.loc[i,"inspected_by"].append(c_stud.name)
                        assigned = True
                # In the case of failure we create an error
                if len(list_of_stud)==0:
                    errors.append("Failed to assign %d %s %s\n"%(p_id,s_to_assign,p_to_assign))
                    assigned  = True
        return c_records,c_students





    def complete_assignment(self):
        problems = False
        must_have = self.max_problems*max_p
        # print("Each must have %d problems"%must_have)
        for s in self.students:
            if len(s.checks_p)!=must_have:
                problems = True
                # print(s.name," %d/%d"%(len(s.checks_p),must_have))
                for p in self.p_ind:
                    assigned = s.checks_p.count(p)
                    if assigned < max_p:
                        # print("\t%s : %d"%(p,max_p-assigned))
                        for ii in range(max_p-assigned):
                            p_id,s_name,i_by = self.get_random_problem(p)
                            while not s.can_assign_id(p_id):
                                p_id,s_name,i_by = self.get_random_problem(p)
                            s.assign(s_name,p,p_id)
                            i_by.append(s.name)
                            # print("\t\tAssigned %s %s %d"%(s_name,p,p_id))
            elif len(s.assigned)!=len(set(s.assigned)):
                print(s.name)
                print("\t",s.checks_p)
                raise Exception("Problems are not unique!")
        return problems

    def verify_assignment(self):
        for index, row in self.records.iterrows():
            if len(row['inspected_by']) < max_p:
                raise Exception("Problem is underassigned!")


    def store_records(self):
        if self.arr == 'p':
            self.records.to_csv(self.target_dir+"/"+"00_st_out.csv",index=False)
        elif self.arr == 's':
            with open(self.target_dir+"/"+"00_st_out.csv","w") as outf:
                for s,val in self.s_ind.items():
                    outf.write("%d,%s,%s\n"%(val['id'],s,repr(val['iby'])))



    def get_random_problem(self,p):
        p_id = self.p_ind[p].sample(1)[['id',"Name",'inspected_by']].values[0]
        return p_id


    def dump_errors(self,err):
        with open(self.target_dir+"/"+"00_errors.txt","w") as a_err:
            for e in err:
                a_err.write(e)

    def collect_problems(self):
        colfile = open(self.target_dir+"/"+"00_p_arrangement.txt","w")
        for s in self.students:
            user_dir = self.target_dir + "/" + s.name
            mkdir_if_not_exist(user_dir)
            colfile.write(s.name+"\n")
            if self.arr == 'p':
                paths = self.prepare_paths_prob(s,user_dir)
            elif self.arr == 's':
                paths = self.prepare_paths_stud(s,user_dir)

            for path in paths:
                src_path = path[0];p_dir = path[1]
                shutil.copytree(src_path,p_dir)
                colfile.write("\t%s\n"%src_path)
                # if self.arr == 'p':
                #     colfile.write("\t%d %s %s\n"%(s.assigned[i],s.checks_s[i],s.checks_p[i]))
                # elif self.arr == 's':
                #     colfile.write("\t%s\n"%src_path)

            # for i in range(len(s.assigned)):
            #     p_dir = user_dir + "/" + repr(s.assigned[i])
            #     src_path = self.s_ind[s.checks_s[i]]['info'].path + "/" + s.checks_p[i]
                # shutil.copytree(src_path,p_dir)
            #     colfile.write("\t%d %s %s\n"%(s.assigned[i],s.checks_s[i],s.checks_p[i]))
            c_passw = get_passw()
            self.s_passw[s.name] = c_passw
            p7zipfile.compress_folder(user_dir,"%s.7z"%s.name,c_passw)

    def prepare_paths_prob(self,s,user_dir):
        paths = []
        for i in range(len(s.assigned)):
            p_dir = user_dir + "/#" + repr(s.assigned[i])
            src_path = self.s_ind[s.checks_s[i]]['info'].path + "/" + s.checks_p[i]
            paths.append((src_path,p_dir))
        return paths

    def prepare_paths_stud(self,s,user_dir):
        paths = []
        for a_s in s.checks_s:
            p_dir = user_dir + "/#" + repr(self.s_ind[a_s]['id'])
            src_path = self.s_ind[a_s]['info'].path
            paths.append((src_path,p_dir))
        return paths

    def run_checks(self):
        if self.arr == 'p':
            self.complete_assignment()
            if self.complete_assignment()!=False:
                raise Exception("Cannot assign problems")
            else:
                print("Assignment \t\tcomplete!")
            self.verify_assignment()
        print("Verification \t\tcomplete!")


def process_arguments(args):
    if len(args) < 3:
        raise Exception("Not enough arguments")

    cas = sys.argv[1]
    mode = sys.argv[2]
    arrange_by = "p"

    if len(args) > 3:
        arrange_by = sys.argv[3]

    return cas,mode,arrange_by

def main():

    cas,mode,arrby = process_arguments(sys.argv)

    print("Arranging by : %s"%arrby)

    report = MoodleRep(cas,mode)


    # initialize the process
    rev = p2pRev(os.getcwd(),cas,mode,arrby)
    print("Nos: %d"%len(rev.students))
    print("Nop: %d"%rev.nop)
    print("Problems per stud: %f"%(rev.nop/len(rev.students)))
    print("Max problems : ", rev.max_problems)

    rev.arrange()
    # rev.assign_problems()
    print("Pre-assignment \t\tcomplete!")
    # rev.store_records()

    rev.run_checks()


    rev.store_records()

    rev.collect_problems()
    report.assign(rev.s_passw,'Password')
    report.store(rev.target_dir)





if __name__ == "__main__":
    main()
