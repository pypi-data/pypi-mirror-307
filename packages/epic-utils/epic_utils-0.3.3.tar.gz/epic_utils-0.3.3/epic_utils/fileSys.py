import os
import json

class File:
    def __init__(self, path : str, create : bool = False):
        if (File.isAbsPath(path)):
            self.path = path
        else:
            self.path = File.toAbsPath(path)
        self.directory = File.directoryName(self.path)
        temp = File.baseName(self.path).split(".")
        self.name = temp[0]
        self.extension = temp[1]  
            
    @staticmethod
    def baseName(path : str):
        return os.path.basename(path)
    @staticmethod
    def directoryName(path : str):
        return os.path.dirname(path) 
    @staticmethod
    def toAbsPath(path : str):
        return os.path.abspath(path)
    @staticmethod
    def isAbsPath(path : str):
        return os.path.isabs(path)
    def exists(self):
        return os.path.exists(self.path)
    
    def read(self):
        with open(self.path, "r") as file:
            return file.read()
    def readJSON(self):
        with open(self.path, "r") as file:
            return json.load(file)
    
    def write(self, data : str):
        with open(self.path, "w") as file:
            file.write(data)
        return True
    def writeJSON(self, data : dict|list|str):
        if not isinstance(data, str):
            data = json.dumps(data)
        return self.write(data)