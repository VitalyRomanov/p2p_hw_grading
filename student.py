import os

class Student:
    def __init__(self,name,path):
        self.name = name
        self.path = path+"/"+name
        self.solved_problems = dict()
        for p in self.get_problems_list(self.path):
            self.solved_problems[int(p)] = p
        self.grade = 0.
        self.checks_p = []
        self.checks_s = []
        self.assigned = []

    def can_assign(self,s,p,max_p):
        # if a given student was already assigned, pick another one
        # if not (s in self.checks_s):
        if self.can_assign_stud(s):
            # if number of needed problems exceeded, pick another one
            if self.checks_p.count(p)<max_p:
                return True
        return False

    def can_assign_stud(self,s):
        if s not in self.checks_s and s!=self.name:
            return True
        return False

    def can_assign_id(self,p_id):
        if p_id in self.assigned:
            return False
        return True

    def assign(self,s,p,p_id):
        self.checks_p.append(p)
        self.assign_stud(s)
        self.assigned.append(p_id)

    def assign_stud(self,s):
        self.checks_s.append(s)

    def get_problems_list(self,path):
        prob_list = os.listdir(path)
        plist = []
        for s in prob_list:
            try:
                prob = int(s)
                if not (prob<0 or prob>=10):
                    plist.append(s)
            except ValueError:
                continue
        return plist
