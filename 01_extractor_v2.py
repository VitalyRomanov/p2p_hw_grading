import zipfile
import rarfile
import os
import shutil
import subprocess
import sys
import editdistance


edit_dist_thr = 7


def unpack_zip(path,filename,name):
    print(path+"/"+filename)
    zip_ref = zipfile.ZipFile(path+"/"+filename, 'r')
    zip_ref.extractall(path+"/"+name)
    zip_ref.close()

def unpack_rar(path,filename,name):
    rar_ref = rarfile.RarFile(path+"/"+filename, 'r')
    rar_ref.extractall(path+"/"+name)
    rar_ref.close()

def unpack_7z(path,filename,name):
    raise NotImplemented

def unpack(path,filename,name):
    if filename[-3:].lower()=="zip":
        unpack_zip(path,filename,name)
        return True
    elif filename[-3:].lower()=="rar":
        unpack_rar(path,filename,name)
        return True
    elif filename[-2:].lower()=="7z":
        unpack_7z(path,filename,name)
        return True
    return False

def listdirs(path):
    content = os.listdir(path)
    dirs = []
    for c in content:
        if os.path.isdir(path+"/"+c):
            dirs.append(c)
    return dirs




class Extractor:
    def __init__(self,asgm,mode):
        cdir = os.getcwd()
        if not os.path.isdir(cdir+"/"+asgm):
            raise Exception("No assignment "+asgm)
        self.assign = int(asgm[1])
        self.path = cdir+"/"+asgm
        if not os.path.isdir(self.path+"/"+mode):
            raise Exception("No files for the mode: "+mode)
        self.mode = mode
        self.testing_dir = self.path+"/"+mode

        self.names = []

        self.unpack()
        self.normalize_folder_structure()

    def unpack(self):
        files = os.listdir(self.testing_dir)
        for fl in files:
            # if unpack(self.testing_dir,fl,name):
            #     self.names.append(name)
            if fl[-3:].lower()=="zip" or fl[-3:].lower()=="rar":
                name = fl[:fl.find('_')]
                if fl[-3:].lower()=="zip":
                    unpack_zip(self.testing_dir,fl,name)
                if fl[-3:].lower()=="rar":
                    unpack_rar(self.testing_dir,fl,name)
                self.names.append(name)


    def normalize_folder_structure(self):

        for name in self.names:
            s_path = self.testing_dir + "/" + name
            dirs = listdirs(s_path)
            for d in dirs:
                split_name = name.split(" ")
                if len(split_name)>1:
                    ed = min(editdistance.eval(d,split_name[0]+" "+split_name[1]),
                            editdistance.eval(d,split_name[1]+" "+split_name[0]))
                else:
                    ed = editdistance.eval(d,name)

                if ed < edit_dist_thr:
                    files_to_move = os.listdir(s_path + "/" + d)

                    for sd in files_to_move:
                        shutil.move(s_path + "/" + d + "/" + sd,s_path + "/" +sd)



def main():
    cas = sys.argv[1]
    mode = sys.argv[2]

    ext = Extractor(cas,mode)



if __name__ == "__main__":
    main()
