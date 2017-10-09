from subprocess import Popen, PIPE
import os


class p7zipfile:
    def compress_folder(path,out_name,passw = None):
        cwd = os.getcwd()
        if os.path.isdir(path):
            os.chdir(path)
            if passw==None:
                comp = Popen(['7z','a',"../"+out_name], stdout=PIPE, stderr=PIPE)
            else:
                comp = Popen(['7z','-p%s'%passw,'a',"../"+out_name], stdout=PIPE, stderr=PIPE)
            os.chdir(cwd)
        elif os.path.isfile(path):
            os.chdir(os.path.dirname(path))
            if passw==None:
                comp = Popen(['7z','a',out_name], stdout=PIPE, stderr=PIPE)
            else:
                comp = Popen(['7z','-p%s'%passw,'a',out_name], stdout=PIPE, stderr=PIPE)
            os.chdir(cwd)
