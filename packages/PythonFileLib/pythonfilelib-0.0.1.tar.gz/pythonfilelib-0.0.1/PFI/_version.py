import __future__
import io
import sys

try:
        from .file import txt
except ImportError:
        from file import txt

__all__ = ['get_version',
           'from_txt_get_version']

try:
        from .exception import *
except ImportError:
        from exception import *

def get_versition():
        a = txt.txt("version.txt",txt.R)
        file_txt = a.readline()
        
        if file_txt == 'N' or "N":
                del a,file_txt
                return False
        
        elif file_txt == ''' version = '0.0.1' ''' or """version = '0.0.1'""":
                del a,file_txt
                return True
        
        else:
                raise VersionError()
                sys.exit()


def from_txt_get_version():
        try:
                from .file import file
        except ImportError:
                from file import file
        file = file.file('version.txt')
        file.change_extension('.py')
        try:
                import .version
        except ImportError:
                import version
        version = version.version
        if version == '0.0.1':
                file = file.file('version.py')
                file.change_extension('.txt')
                with io.open("version.txt",txt.W) as f:
                        f.write("N")
                return None
        else:
                file = file.file('version.py')
                file.change_extension('.txt')
                raise VersionTxtError()
                sys.exit()
