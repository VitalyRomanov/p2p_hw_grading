from subprocess import Popen, PIPE
# import random
import os


class p7zipfile:
    def compress_folder(path,out_name,passw = None):
        cwd = os.getcwd()
        os.chdir(path)
        if passw==None:
            comp = Popen(['7z','a',"../"+out_name], stdout=PIPE, stderr=PIPE)
        else:
            comp = Popen(['7z','-p%s'%passw,'a',"../"+out_name], stdout=PIPE, stderr=PIPE)
        comp_err_out, comp_err = comp.communicate()
        # print(comp_err_out.decode('utf-8'))
        # print(comp_err.decode('utf-8'))
        os.chdir(cwd)


# c_path = os.getcwd()+"/src"

# p7zipfile.compress_folder(c_path,"src.7z",passw = "1q2w3e")

# chars = list(map(chr, range(97, 123)))+['0','1','2','3','4','5','6','7','8','9']
#
# from numpy import random
# print("".join(random.choice(chars,7)))
# print(chars)
# rsmpl = random.sample(chars,7)
# print(''.join(rsmpl))
