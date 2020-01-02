import sys
import os

PRGPATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(PRGPATH)
sys.path.append(os.path.join(PRGPATH, 'lib'))
sys.path.append(os.path.join(PRGPATH, 'plugins'))
sys.path.append(os.path.join(PRGPATH, 'controllers'))

import  serial

print(serial)