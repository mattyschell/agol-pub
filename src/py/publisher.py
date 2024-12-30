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

        # we dont check for existence
        # so we can use clean() as a pre-step
        self.gdb  = filegdb
        self.gdbname = os.path.basename(self.gdb)
        self.gdbpath = os.path.dirname(self.gdb)

        # depending on failure point any of these can exist 
        # and muck up a re-run
        self.tempcopy = None 
        self.renamed  = None
        self.zipped   = None
        self.unzipped = None
        
    def zip(self
           ,zippath):
        
        # we mostly always renamezip (slower, next def)
        # zip then move here
        
        # zippath is the target dir
        #     C:\dir2
        # start: C:\dir1\mydata.gdb
        # end:   C:\dir2\mydata.gdb.zip        

        zippedsrc = shutil.make_archive(self.gdb
                                       ,'zip'
                                       ,self.gdbpath
                                       ,self.gdbname)

        self.zipped = shutil.move(zippedsrc
                                 ,zippath)

    def renamezip(self
                 ,zippath
                 ,name):

        # zippath is the target dir
        #     C:\dir2
        # name is the new name 
        #     pubdata.gdb
        # start: C:\dir1\mydata.gdb
        # end:   C:\dir2\pubdata.gdb.zip  
        # 1 copy 2 rename 3 zip

        self.tempcopy = os.path.join(zippath,"{0}".format(self.gdbname))
        self.renamed  = os.path.join(zippath,"{0}".format(name))

        # pre-clean
        self.clean()

        # C:\dir1\mydata.gdb to
        # C:\dir2\mydata.gdb
        shutil.copytree(self.gdb
                       ,os.path.join(zippath,"{0}".format(self.gdbname)))

        # C:\dir2\mydata.gdb to
        # C:\dir2\pubdata.gdb
        os.rename(os.path.join(zippath,"{0}".format(self.gdbname))
                 ,self.renamed)
        
        # C:\temp\dir2\pubdata.gdb
        # C:\temp\dir2\pubdata.gdb.zip
        self.zipped = shutil.make_archive(self.renamed
                                         ,'zip'
                                         ,zippath
                                         ,name)
        
    def unzip(self
             ,unzippath):
        
        shutil.unpack_archive(self.zipped
                             ,unzippath)   

        self.unzipped = self.zipped.replace('.zip','')     

    def remove_readonly(self
                       ,func
                       ,path
                       ,_):
        
        os.chmod(path, stat.S_IWRITE)
        func(path)

    def clean(self):

        if (self.tempcopy and os.path.exists(self.tempcopy)):
            # PermissionError: [WinError 5] 
            #     Access is denied: 'D:\\temp\\renamesample.gdb'
            # some files in the gdb are readonly (but not the dir itself)
            # onexc callback is copied verbatim from the shutil docs
            shutil.rmtree(self.tempcopy, onerror=self.remove_readonly)
        
        if (self.renamed and os.path.exists(self.renamed)):
            # PermissionError: [WinError 5] 
            #     Access is denied: 'D:\\temp\\renamesample.gdb'
            # some files in the gdb are readonly (but not the dir itself)
            # onexc callback is copied verbatim from the shutil docs
            shutil.rmtree(self.renamed, onerror=self.remove_readonly)

        if (self.zipped and os.path.isfile(self.zipped)):
            # let it throw caller should know
            os.remove(self.zipped)    
            # From cscl but not from tests
            # PermissionError: [WinError 32] The process cannot access the file 
            # because it is being used by another process
            # reminder that this just fails silently
            # shutil.rmtree(self.zipped, ignore_errors=True)

        if (self.unzipped and os.path.isdir(self.unzipped)):
            shutil.rmtree(self.unzipped, onerror=self.remove_readonly)


         

            

        
