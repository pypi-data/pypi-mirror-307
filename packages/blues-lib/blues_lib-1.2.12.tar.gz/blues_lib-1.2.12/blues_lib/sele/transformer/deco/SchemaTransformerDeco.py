import sys,os,re
from functools import wraps
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesConsole import BluesConsole

class SchemaTransformerDeco():
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

      # the handle's second paramter: materials
      handler_self = args[0]
      request = args[1]
      handler_kind = handler_self.kind
      handler_name = type(handler_self).__name__
      value = request.get('value')
      title = value.get('material_title') if value else 'None'
      
      # execute the wrappered func
      outcome = func(*args,**kwargs)
      
      handler_text = '%s [ %s ] - title : %s' % (handler_kind,handler_name,title)
      chain_text = '%s [ %s ]' % (handler_kind,handler_name)
      text = chain_text if handler_kind=='chain' else handler_text
      BluesConsole.info(text)
      
      # must return the wrappered func's value
      return outcome

    return wrapper

