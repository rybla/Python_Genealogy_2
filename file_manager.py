import os, sys

class FileManager:
    def __init__(self,dir_path,file_name):
        self.dir_path = dir_path
        self.file_name = file_name

        try:
            os.stat(dir_path)
        except:
            os.makedirs(dir_path)

        self.file = open(self.dir_path + "/" + file_name, "w+")

    def write(self,txt):
        self.file.write(txt + "\n")

    def close(self):
        self.file.close()