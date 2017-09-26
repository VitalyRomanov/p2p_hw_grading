# import zipfile
import os
import shutil
import subprocess
from collections import Counter
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

cdir = os.getcwd()
files_path = cdir+"/[F17] 214 Modern Programming Paradigms-Assignment 2-7066/"
verPath = cdir+"/ver/A2/"
problems = ["01","02","03","04","05"]
files = os.listdir(files_path)

def normalize(c):
    t = 0
    for key in c:
        t+=c[key]
    for key in c:
        c[key]/=t
    return c

code = ""

for fl in files:
    cpath = files_path+fl+"/"
    if os.path.isdir(cpath):
        for p in problems:
            ver_p = verPath+p+"/"
            use_p = cpath+p+"/"
            if os.path.isdir(use_p):
                stack = use_p+"Stack.hpp"
                array = use_p+"Array.hpp"
                if os.path.isfile(stack):
                    temp = open(stack,"r").read()
                    end_comm = temp.find("*/")
                    code += temp[end_comm:]
                if os.path.isfile(array):
                    temp = open(array,"r").read()
                    end_comm = temp.find("*/")
                    code += temp[end_comm:]


vocab = list(Counter(code).keys())

print("Vocab size: " + repr(vocab))

people = []
vectors = []


for fl in files:
    cpath = files_path+fl+"/"
    if os.path.isdir(cpath):
        code = ""
        vector = []
        for p in problems:
            ver_p = verPath+p+"/"
            use_p = cpath+p+"/"
            if os.path.isdir(use_p):
                stack = use_p+"Stack.hpp"
                array = use_p+"Array.hpp"
                if os.path.isfile(stack):
                    code += open(stack,"r").read()
                if os.path.isfile(array):
                    code += open(array,"r").read()
        local_c = normalize(Counter(code))

        for e in vocab:
            vector.append(local_c[e])
        people.append(fl)
        vectors.append(vector)

# print((np.array(vectors)).shape())

wv = np.array(vectors)

tsne = TSNE(n_components=2, random_state=0)
np.set_printoptions(suppress=True)
Y = tsne.fit_transform(wv)

plt.scatter(Y[:, 0], Y[:, 1],s=5)
for label, x, y in zip(people, Y[:, 0], Y[:, 1]):
    plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
plt.show()

my_pos = people.index("Vitaly Romanov")
my_vec = wv[my_pos,:]

for ind,name in enumerate(people):
    dist = np.linalg.norm(wv[ind,:] - my_vec)
    print(people[ind]," ",dist)
