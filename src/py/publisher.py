import organization
import os
import stat
import shutil
import time

# we may manage several types of content
# simple first case: a local gdb published to an item on the nycmaps organization 

class pubitem(object):

    def __init__(self
                ,org
                ,id):

        self.org  = org
        self.id   = id
        self.existingitem = self.org.gis.content.get(self.id)

    def describe(self):

        for var, value in self.__dict__.items(): 
            print(f'{var}: {value}')

    def replace(self,
                localcontent):
        
        # returns true or false
        return(self.existingitem.update(data=localcontent))  

    def download(self
                ,localpath): 

        #should return path\item.zip
        self.zipped = self.existingitem.download(localpath)

        if not self.zipped.endswith('.zip'):
            raise ValueError('didnt download a zip file, got {0}'.format(self.zipped))

    def clean(self):

         if self.zipped:
            # let it throw caller should know
            os.remove(self.zipped)          

        
class localgdb(object):

    def __init__(self
                ,filegdb):

        if os.path.isdir(filegdb):
            self.gdb  = filegdb
            self.gdbname = os.path.basename(self.gdb)
            self.gdbpath = os.path.dirname(self.gdb)
        else:
            raise ValueError("{0} is not a valid path to a file geodatabase".format(filegdb))

        self.renamed = None
        self.zipped  = None
        
    def zip(self
           ,zippath):
        
        # plan to always zip to a new path
        # the source cscl environment is shared
        # zip then move for performance
        
        # zippath C:\temp\dir2
        # C:\temp\dir1\mydata.gdb
        # C:\temp\dir2\mydata.gdb.zip

        self.zipped = os.path.join(zippath
                                  ,"{0}.zip".format(self.gdbname))
        
        shutil.make_archive(self.gdb
                           ,'zip'
                           ,self.gdb)

        shutil.move("{0}.zip".format(self.gdb)
                   ,self.zipped)

    def renamezip(self
                 ,zippath
                 ,name):

        # 1 copy 2 rename 3 zip
        self.renamed = os.path.join(zippath,"{0}".format(name))
        self.zipped = os.path.join(zippath
                                  ,"{0}.zip".format(name))

        # C:\temp\dir1\mydata.gdb to
        # C:\temp\dir2\mydata.gdb
        shutil.copytree(self.gdb
                       ,os.path.join(zippath,"{0}".format(self.gdbname)))

        # C:\temp\dir2\mydata.gdb to
        # C:\temp\dir2\pubdata.gdb
        os.rename(os.path.join(zippath,"{0}".format(self.gdbname))
                 ,self.renamed)
        
        # C:\temp\dir2\pubdata.gdb
        # C:\temp\dir2\pubdata.gdb.zip
        shutil.make_archive(self.renamed
                           ,'zip'
                           ,self.renamed)

    def remove_readonly(self
                       ,func
                       ,path
                       ,_):
        
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def clean(self):
        
        if (self.renamed and os.path.exists(self.renamed)):
            # PermissionError: [WinError 5] 
            #     Access is denied: 'D:\\temp\\renamesample.gdb'
            # some files in the gdb are readonly (but not the dir itself)
            # onexc callback is copied verbatim from the shutil docs
            shutil.rmtree(self.renamed, onerror=self.remove_readonly)

        if self.zipped:
            # let it throw caller should know
            os.remove(self.zipped)    
            # From cscl but not from tests
            # PermissionError: [WinError 32] The process cannot access the file 
            # because it is being used by another process
            # reminder that this just fails silently
            # shutil.rmtree(self.zipped, ignore_errors=True)


         

            

        
