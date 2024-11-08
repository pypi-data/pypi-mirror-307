from abc import ABC
import sys,os,re

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from atom.Atom import Atom     

class CompositeAtom(Atom,ABC):

  _category = 'composite'

  def __init__(self,kind,title,value=None):
    '''
    A atoms' collections ,don't case the item atom's kind
    Parameter:
      title (str) : the atom's title
      selector (str) : the atoms' parent selector
      value (list|tuple|dict) : the atoms' collection
    Returns:
      BluesAtom : a atom instance
    '''
    super().__init__(self._category,kind,title)
    self._value = value
  
  # getter
  def get_value(self):
    return self._value
  
  # setter
  def set_value(self,value):
    self._value = value




