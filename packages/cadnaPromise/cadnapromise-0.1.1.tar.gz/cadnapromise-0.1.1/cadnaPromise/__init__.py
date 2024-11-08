from .promise import Promise 
import os

__version__ = '0.1.1'

curr_loc = os.path.dirname(os.path.realpath(__file__))

set_cadna_env = False

if not os.path.isfile(curr_loc+'/cadna/a.out'):
    if 'CADNA_PATH' in os.environ:
         set_cadna_env = False
    else:
        import logging
        logging.basicConfig()
        log = logging.getLogger(__file__)

        log.warning("Have not found CADNA path, please ensure CADNA is installed in this machine.")
        
else:
    set_cadna_env = True
    
if set_cadna_env:
    os.environ["CADNA_PATH"] = curr_loc+'/cadna/'

cachePath = "/cache"
if os.path.exists(curr_loc + cachePath):
    with open(curr_loc+cachePath+"/CXX.txt", "r") as file:
        __compiler__ = file.read()

    if __compiler__ != 'g++' and __compiler__ is not None:
            alias = {'--alias':__compiler__}
else:
    __compiler__ = 'g++'
