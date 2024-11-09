from .PExecutor import *

class Executor(PExecutor):
    """
    This is a main class for executing pipeline.
    """
    def __init__(self, context = None, params = None, modules = None, cfg = None):
        """
        Initialize the Executor instance.

        Args:
            context (str): The context in which the pipeline execution occurs. This could include any relevant contextual information
                needed by the executor.
            params : Parameters defined for specific instance of pipeline execution.
            modules :  Modules used during the pipeline execution process. These can be represented by names or Mod classes
           
        """
        PExecutor.__init__(self, context, params, modules, cfg)
        
        return
    