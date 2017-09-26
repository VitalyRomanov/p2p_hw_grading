from numpy import random

def get_passw():
    c_list = list(map(chr, range(97, 123)))+['0','1','2','3','4','5','6','7','8','9']
    return "".join(random.choice(c_list,7))
