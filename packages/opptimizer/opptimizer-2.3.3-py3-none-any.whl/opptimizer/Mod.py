from .PModulePy import *

class Mod(PModulePy):
    ''' Class for instances of modules used for pipeline execution'''
    def __init__(self, func_exec=None, name=None, func_init=None, func_onprocess=None):
        '''
        Initialize the Module instance
        Args:
            func_exec: method called while module is executed in pipeline
            name: name of module
            func_init: method called right before module is executed
            func_onprocess: method called instead of `func_exec` for each input file. Only called when `dataloop=1` is set in context or params.
        '''
        if name is None:
            name = str(self.__str__)

        PModulePy.__init__(self,name, func_exec, func_init, func_onprocess)
        
        return