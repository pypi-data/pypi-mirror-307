from abc import ABC,abstractmethod
from .LoginerSchema import LoginerSchema

class AccountLoginerSchema(LoginerSchema,ABC):

  def __init__(self):
    # define the subclass's fields, must define before super init
    # { ArrayAtom } : the behaviors that show the loginer form
    self.switch_atom = None
    # { ArrayAtom } : the behaviors that fill the form
    self.fill_atom = None
    # { ArrayAtom } : the behaviors that submit
    self.submit_atom = None

    # invoke the parent's consrctor
    super().__init__()
  
  # the must-do template method
  def create_subtype_atoms(self):
    self.create_switch_atom()
    self.create_fill_atom()
    self.create_submit_atom()
  
  # define the mini steps 
  @abstractmethod
  def create_switch_atom(self):
    pass

  @abstractmethod
  def create_fill_atom(self):
    pass

  @abstractmethod
  def create_submit_atom(self):
    pass

