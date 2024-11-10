import sys
import os
from warnings import *

try:
        from .file import file as fl
except ImportError:
        from file import file as fl

class WayError(fl.WayError):
        '''
        This will run if you use wrong 'way' keys.
        
        def __init__(self,error_code):
                super().__init__(f"{error_code} is not excepted.")
                self.error_code = error_code
        '''
        pass

class VersionError(SystemError):
        '''
        it will return if version.txt has some error.
        '''
        def __init__(self):
                super().__init__(f"version.txt has some errors.")

class VersionTxtError(SystemError):
        '''
        it will return if version.txt was changed.
        '''
        def __init__(self):
                super().__init__(f"version.txt was changed unexceptedly.")

class FileError(Exception):
        '''
        the father class of all the file errors.
        '''
        def __init__(self,filename,event):
                #super().__init__(f"{filename} was {event}.")
                self.filename = filename
                self.event = event

class PathError(FileError,OSError):
        '''
        it would return if path has some error.
        '''
        def __init__(self,path,event):
                super().__init__(f"{path} was {event}.")
                self.path = path
                self.event = event

class PathNotFoundError(PathError):
        '''
        it would return if path has some error.
        '''
        def __init__(self,path):
                super().__init__(f"{path} not found.")
                self.path = path
                self.event = "not_found"

class PathIsFoundError(PathError):
        '''
        it would return if path has some error.
        '''
        def __init__(self,path):
                super().__init__(f"{filename} is found.")
                self.path = path
                self.event = "is_found"

class TextError(Exception):
        '''
        the father class of all the text errors.
        '''
        def __init__(self,texttype,event):
                #super().__init__(f"{filename} was {event}.")
                self.texttype = texttype
                self.event = event

class TextTypeError(TextError,TypeError):
        '''
        it would return if type has some errors.
        '''
        def __init__(self,texttype,event):
                super().__init__(f"{texttype} is not right.")
                self.texttype = texttype
                self.event = "not_right"

class TextChangeError(TextError,TypeError):
        '''
        it would return if type has some errors.
        '''
        def __init__(self,texttype1,texttype2,event):
                super().__init__(f"{texttype1} couldn't change into {texttype2}.")
                self.texttype = texttype
                self.event = "could_not_change"

class CSVError(Exception):
        pass

class PPTError(Exception):
        pass

class DocError(Exception):
        pass

class PdfError(Exception):
        pass

del sys,os,warnings,fl
