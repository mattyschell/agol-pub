import organization
import os
import shutil

# we may manage several types of content
# simple first case: a local gdb published to an item on the nycmaps organization 

class pubitem(object):

    def __init__(self
                ,org
                ,id):

        self.org = org
        self.id = id

    def describe(self):

        for var, value in self.__dict__.items(): 
            print(f'{var}: {value}')

    def replace(self,
                localcontent):
        
        existingitem = self.org.gis.content.get(self.id)

        existingitem.update(data=localcontent)       

        
class localgdb(object):

    def __init__(self
                ,filegdb):

        if os.path.isdir(filegdb):
            self.gdb  = filegdb
            self.gdbname = os.path.basename(self.gdb)
        else:
            raise ValueError("{0} is not a valid path to a file geodatabase".format(filegdb))
                
    def zip(self
           ,zippath):
        
        # plan to always zip to a new path
        # the source cscl environment is shared
        
        # zippath C:\temp\dir2
        # C:\temp\dir1\mydata.gdb
        # C:\temp\dir2\mydata.gdb.zip

        self.zipped = os.path.join(zippath
                                  ,"{0}.zip".format(self.gdbname))
        
        shutil.make_archive(self.gdb
                           ,'zip'
                           ,self.gdb)

        os.rename("{0}.zip".format(self.gdb)
                 ,self.zipped)
        
    def clean(self):
        
        os.remove(self.zipped)

        
