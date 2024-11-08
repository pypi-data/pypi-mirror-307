import sys,os,re
from functools import wraps
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesConsole import BluesConsole

class BriefTransformerDeco():
  '''
  Only used to the Acter class's resovle method
  '''

  def __init__(self):
    '''
    Create the decorator
    Has no parameters
    '''
    pass

  def __call__(self,func):
    @wraps(func) 
    def wrapper(*args,**kwargs):

      # the handle's second paramter: briefs
      handler_self = args[0]
      briefs = args[1]
      handler_kind = handler_self.kind
      handler_name = type(handler_self).__name__
      input_size = 0 if not briefs else len(briefs)
      
      # execute the wrappered func
      outcome = func(*args,**kwargs)
      
      output_size = 0 if not outcome else len(outcome)
      BluesConsole.info('%s [ %s ] ; briefs input: %s output: %s' % (handler_kind,handler_name,str(input_size),str(output_size)))
      
      # must return the wrappered func's value
      return outcome

    return wrapper

