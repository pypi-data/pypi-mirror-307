import sys,os,re
from abc import ABC,abstractmethod

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from atom.AtomFactory import AtomFactory     

class LoginerSchema(ABC):
  def __init__(self):
    # define fields
    self.atom_factory = AtomFactory()

    # { ValueAtom } : the value atom of loginer page's url
    self.log_in_atom = None
    # { ElementAtom } : the loginer page's element selector
    self.log_in_element_atom = None
    # { ValueAtom } : the verify login status and save http cookies
    self.verify_wait_period_atom = None
    # { ValueAtom } : the value atom of proxy config
    self.proxy_atom = None
    # { ValueAtom } : the value atom of cookie filter config
    self.cookie_filter_atom = None

    # invoke the template method
    self.create()

  def create(self):
    '''
    The final template method define the skeleton of an algorithm
    '''
    # base steps
    self.create_log_in_atom()
    self.create_log_in_element_atom()
    self.create_proxy_atom()
    self.create_cookie_filter_atom()
    self.create_verify_wait_period_atom()

    # sub abstract steps
    self.create_subtype_atoms()
  
  # === Create the base required fields
  @abstractmethod
  def create_log_in_atom(self):
    pass

  def create_log_in_element_atom(self):
    # set a empty selector as the default
    self.log_in_element_atom = self.atom_factory.createElement('default empty login page element','')

  def create_verify_wait_period_atom(self):
    # At least, to wait the http response to save cookies
    self.verify_wait_period_atom = self.atom_factory.createValue('verify wait atom',10)

  @abstractmethod
  def create_proxy_atom(self):
    pass

  @abstractmethod
  def create_cookie_filter_atom(self):
    pass
  
  # === This operation have to be implemented in sub abstract class
  @abstractmethod
  def create_subtype_atoms(self):
    '''
    Second algorithm : create the subclass's atoms
    '''
    pass
