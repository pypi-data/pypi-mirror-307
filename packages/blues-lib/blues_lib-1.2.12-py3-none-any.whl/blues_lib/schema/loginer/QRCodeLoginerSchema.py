from abc import ABC,abstractmethod
from .LoginerSchema import LoginerSchema

class QRCodeLoginerSchema(LoginerSchema,ABC):

  def __init__(self):
    # define the subclass's fields, must define before super init
    # { ArrayAtom } : the behaviors that show the loginer form
    self.switch_atom = None
    # { InputAtom } : the behavior that input the code
    self.code_atom = None

    # invoke the parent's consrctor
    super().__init__()
  
  # the must-do template method
  def create_subtype_atoms(self):
    self.create_switch_atom()
    self.create_code_atom()

  @abstractmethod
  def create_switch_atom(self):
    pass

  @abstractmethod
  def create_code_atom(self):
    pass

