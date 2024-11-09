import sys,os,re,time
from abc import ABC,abstractmethod
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.browser.BluesLoginChrome import BluesLoginChrome    
from sele.behavior.FormBehavior import FormBehavior       
from sele.behavior.BehaviorChain import BehaviorChain       
from util.BluesDateTime import BluesDateTime
from util.BluesConsole import BluesConsole

class AIQA(ABC):
  
  def __init__(self,schema,loginer=None,login_element=None):
    # { AIQASchema }
    self.schema = schema
    # { Loginer } set loginer for relogin
    self.loginer = loginer
    # { str } the login page's selector
    self.login_element = login_element
    # {BluesLoginChrome}
    self.browser = None
    # { int } wait the AI answer
    self.waiting_timeout = 15

  def execute(self):
    '''
    Fianl tempalte method
    Input question and return answer
    Returns {json} : json string
    '''
    try:
      self.open()
      self.question()
      self.submit()
      self.wait()
      return self.answer()
    except Exception as e:
      BluesConsole.error(e)
      return None
    finally:
      self.browser.quit()

  def open(self):
    url = self.schema.url_atom.get_value()
    self.browser = BluesLoginChrome(url,self.loginer,self.login_element)
    self.browser.open(url)
    BluesConsole.success('Opened form page: %s' % self.browser.interactor.document.get_title())
  
  def question(self):
    BluesDateTime.count_down({'duration':5,'title':'Wait the AI ready...'})
    # contains fill atom and send atom
    popup_atom = self.schema.popup_atom
    question_atom = self.schema.question_atom
    handler = FormBehavior(self.browser,question_atom,popup_atom)
    handler.handle()

  def submit(self):
    popup_atom = self.schema.popup_atom
    submit_atom = self.schema.submit_atom
    handler = FormBehavior(self.browser,submit_atom,popup_atom)
    handler.handle()

  def wait(self):
    BluesDateTime.count_down({'duration':self.waiting_timeout,'title':'Wait the AI answer...'})

  def answer(self):
    answer_atom = self.schema.answer_atom
    handler = BehaviorChain(self.browser,answer_atom)
    outcome = handler.handle()
    BluesConsole.info('AI outcome: %s , %s' % (outcome.code,outcome.data))
    # briefs dict list
    if not outcome.data:
      return None
    else:
      #  {dict} : {'title':'text','content':'xxx\n\nxxx\n\nxxx'}
      return self.extract(outcome.data)
  
  @abstractmethod
  def extract(self,ai_entity):
    '''
    Template method: extract title and para list from the text square
    Parameters:
      ai_entity {dict} : such as {'title':'text','content':'xxx\n\nxxx\n\nxxx'}
    '''
    pass
