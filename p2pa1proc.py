import pandas
from name_normalizer import NNorm
from peer_verify import grade_a1,grade_a2,get_average_ans,grade_resp_a1,grade_resp_a2
import pickle
from scipy.sparse import coo_matrix,csr_matrix
from scipy.sparse.linalg import eigs
import os
import numpy as np
import shutil
from anumstring import get_passw
from p7zipfile import p7zipfile

resp1 = pandas.read_csv("./A6/p2pa1ans.csv")
resp2 = pandas.read_csv("./A6/p2pa2ans.csv")
class_list = pandas.read_csv("class1.csv")
proper_list = pandas.read_csv("./A6/00_st_out_proper.csv")
improper_list = pandas.read_csv("./A6/00_st_out_improper.csv")

def get_s_info(class_list):
    return list(class_list['Name']),list(class_list['Email'])

def find_user_by_id(search_in,p_id):
    name = None
    for table in search_in:
        rec = table.loc[table['id'] == p_id]
        if rec.empty:
            continue
        name = rec['Name'].values[0]
    if name == None:
        raise Exception("Could not match problem %s"%p_id)
    return name

def add_to_p_dict(r,p_id):
    if p_id in [68445209,71253374,78613059,15964045,94551258,90249756,95147336,83234103,19920331,35987240,25183552,84932606,27588275,88445137,79267658]:
        return
    if p_id in p_dict:
        p_dict[p_id].append(r)
    else:
        p_dict[p_id] = [r]

def process_responces(resp,question_fields):
    responces = []
    for row in resp.iterrows():



        grader = nnorm.get_name_by_email(row[1][field['email']])
        gradee = find_user_by_id([proper_list,improper_list],row[1][field['id']])

        if grader not in people:
            people.append(grader)
        if gradee not in people:
            people.append(gradee)

        grader_id = people.index(grader)
        gradee_id = people.index(gradee)

        responce = {
            'grader':grader_id,
            'gradee':gradee_id,
            'p_id':row[1][field['id']]
        }

        for question in question_fields:
            responce[question] = row[1][question]
        responces.append(responce)
        add_to_p_dict(responce,row[1][field['id']])
    return responces


def grade(a,type):
    data = []; row = []; col = []
    resp_matr = np.zeros(shape=(len(people),len(people)),dtype=np.float32)
    for r in a:
        with open("./A6/feedback/%s.txt"%people_inv[r['gradee']],"a") as fdb:
            if type == "a1":
                grade,feedback = grade_a1(r)
            elif type == "a2":
                grade,feedback = grade_a2(r)
            resp_matr[r['gradee'],r['grader']] = grade
            fdb.write(feedback+"\n")
    return resp_matr

def grade_responces(resps):
    if os.path.isdir("./A6/feedback_r"):
        shutil.rmtree("./A6/feedback_r")
    os.mkdir("./A6/feedback_r")
    data = []; row = []; col = []
    resp_matr = np.zeros(shape=(len(people),len(people)),dtype=np.float32)
    for i_a,a in enumerate(resps):
        for r in a:
            p_id = r['p_id']
            if p_id in [68445209,71253374,78613059,15964045,94551258,90249756,95147336,83234103,19920331,35987240,25183552,84932606,27588275,88445137,79267658]:
                continue
            with open("./A6/feedback_r/%s.txt"%people_inv[r['grader']],"a") as fdb:
                if i_a == 0:
                    grade,feedback = grade_resp_a1(r,av_ans)
                elif i_a == 1:
                    grade,feedback = grade_resp_a2(r,av_ans)
                resp_matr[r['grader'],r['gradee']] = grade
                fdb.write(feedback+"\n")
    return resp_matr


name, email = get_s_info(class_list)

nnorm = NNorm(name, email)

field = {'email':'Email Address',\
        'id':'The ID number of the work'}

question_fields_a1 = list(resp1.columns[resp1.columns.get_loc("Does the program compile?"):])
question_fields_a2 = list(resp2.columns[resp2.columns.get_loc("Does the program compile?"):])


people = []; problems = [];p_dict = dict()

a1 = process_responces(resp1,question_fields_a1)
a2 = process_responces(resp2,question_fields_a2)


people = dict(zip(people,range(len(people))))
people_inv = dict(zip(range(len(people)),people))

av_ans = get_average_ans(p_dict)
evaluation_matrix = np.zeros(shape=(len(people),len(people)),dtype=np.float32)
eval_matr = grade_responces([a1, a2])
# print(eval_matr)

def grade_count(values):
    count = np.count_nonzero(values)
    avr = values.sum()/count
    return avr,count

def grade_reviewer(matr,p_id):
    rc = np.nonzero(matr[:,p_id])
    mm = np.zeros(matr.shape)
    row = rc[0]
    grade = 0.
    for r in row:
        avg,_ = grade_count(matr[r,:])
        grade += (avg-abs(matr[r,p_id]-avg))/avg*100
        mm[r,p_id] = (avg-abs(matr[r,p_id]-avg))/avg*100
    return grade/len(row),mm


if os.path.isdir("./A6/feedback"):
    shutil.rmtree("./A6/feedback")
os.mkdir("./A6/feedback")

a1_mat = grade(a1,"a1")
np.savetxt("a1_mat.csv",a1_mat,delimiter=',',fmt='%2.2f',)
a2_mat = grade(a2,"a2")
np.savetxt("a2_mat.csv",a2_mat,delimiter=',',fmt='%2.2f',)
with open("./A6/grades.csv","w") as gr:
    gr.write("Name,Email,A1,A1 graded by,A2,A2 graded by,Average,Review Dev,Rev\n")
    for p in people_inv:
        name = people_inv[p]
        _,email = nnorm.get_info(name)
        A1,A1_gr = grade_count(a1_mat[p,:])
        A2,A2_gr = grade_count(a2_mat[p,:])
        GR = (A1+A2)/2
        R1,mm1 = grade_reviewer(a1_mat,p)
        R2,mm2 = grade_reviewer(a2_mat,p)
        R = (R1+R2)/2
        mm = mm1.transpose()+mm2.transpose()
        hh = np.sum(mm*eval_matr)/np.count_nonzero(mm)
        # print(np.sum(mm*eval_matr)/np.count_nonzero(mm))
        gr.write("%s,%s,%f,%d,%f,%d,%f,%f,%f\n"%(name,email,A1,A1_gr,A2,A2_gr,GR,R,hh))
        c_passw = get_passw()
        p7zipfile.compress_folder("./A6/feedback/%s.txt"%name,"%s.7z"%name,c_passw)
