import pandas
import editdistance
import os
import pyminizip
import random

class MoodleRep:
    def __init__(self,assign,mode):
        cdir = os.getcwd()
        class_desc = cdir+"/"+"class1.csv"
        self.records = pandas.read_csv(class_desc)

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
        pyminizip.compress(feedback_path+name+".txt", arc_path+name+".zip", password, 1)
        return password

    def assign(self,source,column):
        if column not in self.records:
            self.records[column] = ""
        people = list(source.keys())
        for p in people:
            min_dist = 900
            min_dist_match = ""
            min_dist_index = -1
            for index, row in self.records.iterrows():
                dist = editdistance.eval(p,self.getName(row))
                if min_dist>dist:
                    min_dist = dist
                    min_dist_match = p
                    min_dist_index = index
            if min_dist_index == -1:
                raise Exception("Could not match %s"%p)
            self.records.loc[min_dist_index,column] = source[min_dist_match]


    def get_records():
        return self.records

    def store(self,path):
        self.records.to_csv(path+"/"+"00_frep.csv",index = False)
