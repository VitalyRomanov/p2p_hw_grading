import numpy as np
import pandas as pd


def grade_a1(r):

    questions = {
        'q1':'Does the program compile?',
        'f1':'Copy and paste the compile errors',
        'q2':'Made with a template?',
        'q3':'Can work with generic data structures through iterators?',
        'q4':'Does the function accept functional objects or a pointer to a function?',
        'q5':'How many requirements on the parameters are given?',
        'q6':'How many of them are sound?',
        'q7':'How many additional requirements you would add?',
        'f2':'Provide a feedback in a free form'
    }

    grade = 0.;grade_max = 5
    feedback = "======= FEEDBACK ASSIGNMENT 1 =======\n\n"
    for q in questions:
        feedback += questions[q].upper() + " : \n"
        if type(r[questions[q]])==type(''):
            feedback += r[questions[q]] + "\n"
        else:
            feedback += repr(r[questions[q]]) + "\n"

    if r[questions['q1']] == "Yes":
        grade += 1.

    if r[questions['q2']] == "Yes":
        grade += 1.

    allowed_iterators = set(["Integer", "Boolean", "Char", "Float", "List STL", "Vector STL"])

    if pd.isnull(r[questions['q3']]):
        iterators = []
    else:
        iterators = r[questions['q3']].split(";")
    it_count = 0
    for it in iterators:
        it_count += (it in allowed_iterators)
    grade += it_count/len(allowed_iterators)

    if r[questions['q4']] == "functional objects":
        grade += 1.
    elif r[questions['q4']] == "pointer to a function":
        grade += 0.

    try:
        req_giv = int(r[questions['q5']])
        req_sou = int(r[questions['q6']])
        req_add = int(r[questions['q7']])
    except ValueError:
        print("Human intervention needed")
        print('How many requirements on the parameters are given? ',r['How many requirements on the parameters are given?'])
        print('How many of them are sound? ',r['How many of them are sound?'])
        print('How many additional requirements you would add? ',r['How many additional requirements you would add?'])
        req_giv = int(input("Given "))
        req_sou = int(input("Sound "))
        req_add = int(input("Would add "))

    if (req_sou+req_add)==0 and req_giv > 0:
        grade += 1.
    elif (req_sou+req_add)==0 and req_giv ==0:
        grade += 0.
    else:
        grade += req_sou/(req_giv+req_add)



    grade = grade/grade_max*100
    return grade,feedback

def grade_a2(r):

    questions = {
        'q1':'Does the program compile?',
        'f1':'Copy and paste the compile errors',
        'q2':'Implemented as a template?',
        'q3':'Is the iterator for the class Node implemented?',
        'q4':'Which operators are overloaded for this iterator?',
        'f2':'Provide a feedback in a free form'
    }
    grade = 0.;grade_max = 4.
    feedback = "======= FEEDBACK ASSIGNMENT 2 =======\n\n"
    for q in questions:
        feedback += questions[q].upper() + " : \n"
        if type(r[questions[q]])==type(''):
            feedback += r[questions[q]] + "\n"
        else:
            feedback += repr(r[questions[q]]) + "\n"

    if r[questions['q1']] == "Yes":
        grade += 1.

    if r[questions['q2']] == 'No':
        grade += 1.

    if r[questions['q3']] == "Yes":
        grade += 1.

    it_ops = set(['*','++','!='])

    if pd.isnull(r[questions['q4']]):
        iterators = []
    else:
        iterators = r[questions['q4']].split(";")

    it_count = 0.
    for it in it_ops:
        it_count +=  1 if it in iterators else 0
    grade += it_count/3.

    grade = grade/grade_max*100
    return grade,feedback

def get_average_ans(p_dict):

    qa1 = {
        'q1':'Does the program compile?',
        'f1':'Copy and paste the compile errors',
        'q2':'Made with a template?',
        'q3':'Can work with generic data structures through iterators?',
        'q4':'Does the function accept functional objects or a pointer to a function?',
        'q5':'How many requirements on the parameters are given?',
        'q6':'How many of them are sound?',
        'q7':'How many additional requirements you would add?',
        'f2':'Provide a feedback in a free form'
    }

    qa2 = {
        'q1':'Does the program compile?',
        'f1':'Copy and paste the compile errors',
        'q2':'Implemented as a template?',
        'q3':'Is the iterator for the class Node implemented?',
        'q4':'Which operators are overloaded for this iterator?',
        'f2':'Provide a feedback in a free form'
    }

    def get_a_type(p):
        if len(p)!=0:
            if 'Made with a template?' in p[0].keys():
                # print(p[0])
                at = 1
            if 'Implemented as a template?' in p[0].keys():
                at = 2
        else:
            at = 3
        return at


    for p in p_dict:
        at = get_a_type(p_dict[p])
        if at != 3:
            master_ans = dict().fromkeys(p_dict[p][0].keys())
            if at == 1:
                ans = []
                for r in p_dict[p]:
                    ans.append(r[qa1['q1']])
                master_ans[qa1['q1']] = 'Yes' if ans.count('Yes')>=2 else 'No'

                ans = []
                for r in p_dict[p]:
                    ans.append(r[qa1['q2']])
                master_ans[qa1['q2']] = 'Yes' if ans.count('Yes')>=2 else 'No'

                ans = []
                for r in p_dict[p]:
                    ans.append(r[qa1['q4']])
                master_ans[qa1['q4']] = 'Yes' if ans.count('functional objects')>=2 else 'No'
            elif at == 2:
                ans = []
                for r in p_dict[p]:
                    ans.append(r[qa2['q1']])
                master_ans[qa2['q1']] = 'Yes' if ans.count('Yes')>=2 else 'No'

                ans = []
                for r in p_dict[p]:
                    ans.append(r[qa2['q2']])
                master_ans[qa2['q2']] = 'Yes' if ans.count('Yes')>=2 else 'No'

                ans = []
                for r in p_dict[p]:
                    ans.append(r[qa2['q3']])
                master_ans[qa2['q3']] = 'Yes' if ans.count('Yes')>=2 else 'No'
        p_dict[p] = master_ans
    return p_dict

def grade_resp_a1(r,av_ans):
    qa1 = {
        'q1':'Does the program compile?',
        'f1':'Copy and paste the compile errors',
        'q2':'Made with a template?',
        'q3':'Can work with generic data structures through iterators?',
        'q4':'Does the function accept functional objects or a pointer to a function?',
        'q5':'How many requirements on the parameters are given?',
        'q6':'How many of them are sound?',
        'q7':'How many additional requirements you would add?',
        'f2':'Provide a feedback in a free form'
    }
    grade = 0.;feedback = ""
    if r['p_id'] not in av_ans: return grade,feedback
    av = av_ans[r['p_id']]
    grade = 1.
    if av[qa1['q1']]!=r[qa1['q1']]:
        grade -= .1
    if av[qa1['q2']]!=r[qa1['q2']]:
        grade -= .1
    if av[qa1['q4']]!=r[qa1['q4']]:
        grade -= .1
    return grade,feedback

def grade_resp_a2(r,av_ans):
    qa2 = {
        'q1':'Does the program compile?',
        'f1':'Copy and paste the compile errors',
        'q2':'Implemented as a template?',
        'q3':'Is the iterator for the class Node implemented?',
        'q4':'Which operators are overloaded for this iterator?',
        'f2':'Provide a feedback in a free form'
    }
    grade = 0.
    feedback = ""

    if r['p_id'] not in av_ans: return grade,feedback
    grade = 1.
    av = av_ans[r['p_id']]
    if av[qa2['q1']]!=r[qa2['q1']]:
        grade -= .1
    if av[qa2['q2']]!=r[qa2['q2']]:
        grade -= .1
    if av[qa2['q3']]!=r[qa2['q3']]:
        grade -= .1
    return grade,feedback
