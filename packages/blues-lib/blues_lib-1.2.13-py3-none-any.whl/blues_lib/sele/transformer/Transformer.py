import sys,os,re
from abc import ABC,abstractmethod
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))

class Transformer(ABC):

  def __init__(self):
    '''
    The abstract class of handlers 
    '''
    self._next_handler = None
  
  def set_next(self,handler):
    '''
    Set the next handler
    Parameter:
      handler {Acter} : the next handler
    Returns 
      {Acter} : return the passin Acter
    '''
    self._next_handler = handler
    return handler
  

  def handle(self,data):
    '''
    Write the field by a handler in the chain
    Prev handler's output is next handler's input
    '''
    result = self.resolve(data)
    if self._next_handler:
      return self._next_handler.handle(result)
    else:
      return result

  @abstractmethod
  def resolve(self,data):
    '''
    This method will be implemented by subclasses
    '''
    pass


