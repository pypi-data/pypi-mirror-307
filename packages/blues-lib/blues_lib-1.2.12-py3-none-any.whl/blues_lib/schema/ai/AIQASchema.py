import sys,os,re
from abc import ABC,abstractmethod
from .AISchema import AISchema
sys.path.append(re.sub('test.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.schema.SchemaValueReplacer import SchemaValueReplacer     

class AIQASchema(AISchema,ABC):

  def __init__(self,question='who are you'):
    super().__init__()
    
    # { str } question : pass by invoker
    self.question = question

    # { ArrayAtom }
    self.question_atom = None

    # { ArrayAtom }
    self.submit_atom = None

    # { ArrayAtom }
    self.popup_atom = None

    # { ArrayAtom }
    self.answer_atom = None

    # crete the atom fileds
    self.create_fields()

    # fillin the replaceholder
    self.fill_fields()

  def create_fields(self):
    self.create_url_atom()
    self.create_question_atom()
    self.create_submit_atom()
    self.create_answer_atom()
  
  def fill_fields(self):
    request = SchemaValueReplacer().handle({
      'atom':self.question_atom,
      # value must be a dict, dict's key it's the placeholder value
      'value':{
        'question':self.question,
      }, 
    })

  @abstractmethod
  def create_question_atom(self):
    '''
    The form for input question 
    '''
    pass

  @abstractmethod
  def create_submit_atom(self):
    '''
    Sbumit the question
    '''
    pass

  def create_popout_atom(self):
    pass

  @abstractmethod
  def create_answer_atom(self):
    '''
    The atom for read the answer
    '''
    pass
