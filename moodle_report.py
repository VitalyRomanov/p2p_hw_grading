import pandas
import editdistance
import os
import sys
import pyminizip
import random

class MoodleRep:
    def __init__(self,assign,mode):
        cdir = os.getcwd()
        class_desc = cdir+"/"+"class1.csv"
        self.test_desc = cdir+"/"+"A"+assign[1]+"/"+mode+"/"
        self.records = pandas.read_csv(class_desc)
        self.grades = pandas.read_csv(self.test_desc+"00_report.csv",header = None)
        self.assignment_name = "Assignment: Assignment "+assign[1]+" (Real)"

    def getPersonsGrade(self,name):
        return float(self.grades.loc[self.grades[0] == name][1])
    def getName(self,row):
        return row['First name']+" "+row['Last Name']

    def packFeedback(self,name):
        feedback_path = self.test_desc+"00_feedback/"
        arc_path = self.test_desc+"00_arc/"
        if not (os.path.isdir(arc_path)):
            os.mkdir(arc_path)
        password = repr(int(random.uniform(1000000, 9999999)))
        # passw.write(fl[:-4]+","+password+"\n")
        pyminizip.compress(feedback_path+name+".txt", arc_path+name+".zip", password, 1)
        return password

    def assign(self):
        people = []
        for key in self.grades[0]:
            people.append(key)
        # print(people)
        for p in people:
            min_dist = 900
            min_dist_index = -1
            for index, row in self.records.iterrows():
                dist = editdistance.eval(p,self.getName(row))
                if min_dist>dist:
                    min_dist = dist
                    min_dist_index = index

            self.records.loc[min_dist_index,self.assignment_name] = self.getPersonsGrade(p)
            passw = self.packFeedback(p)
            self.records.loc[min_dist_index,'Comments'] = "Password for feedback: %s"%passw
        self.records.to_csv(self.test_desc+"00_frep.csv",index = False)









cas = sys.argv[1]
mode = sys.argv[2]



rep = MoodleRep(cas,mode)
rep.assign()
