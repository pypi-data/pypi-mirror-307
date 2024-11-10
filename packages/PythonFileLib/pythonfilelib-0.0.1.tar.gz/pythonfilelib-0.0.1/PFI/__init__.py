#from .file import file,TxtPathError

import pandas as pd
import numpy as np

del pd,np

import ._version as v

if v.get_version():
        v.from_txt_get_version()

del v

__all__ = ['file',
           'exceptions',
           ]
