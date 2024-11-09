from abc import ABC,abstractmethod
from .LoginerSchema import LoginerSchema

class MACLoginerSchema(LoginerSchema,ABC):

  def __init__(self):
    # define the subclass's fields, must define before super init
    # { ArrayAtom } : the behaviors that show the loginer form
    self.switch_atom = None
    # { ArrayAtom } : the behaviors that fill the form before sending the code
    self.fill_atom = None
    # { ArrayAtom } : the behaviors that send code
    self.send_atom = None
    # { InputAtom } : the behavior that input the code
    self.code_atom = None
    # { ArrayAtom } : the behaviors that submit
    self.submit_atom = None
    # { ValueAtom } : the max waiting time for the sms auth code
    self.captcha_valid_period_atom = None

    # invoke the parent's consrctor
    super().__init__()
  
  # the must-do template method
  def create_subtype_atoms(self):
    self.create_switch_atom()
    self.create_fill_atom()
    self.create_send_atom()
    self.create_code_atom()
    self.create_submit_atom()
    self.create_captcha_valid_period_atom()

  @abstractmethod
  def create_switch_atom(self):
    pass

  @abstractmethod
  def create_fill_atom(self):
    pass

  @abstractmethod
  def create_send_atom(self):
    pass

  @abstractmethod
  def create_code_atom(self):
    pass

  @abstractmethod
  def create_submit_atom(self):
    pass

  @abstractmethod
  def create_captcha_valid_period_atom(self):
    pass

