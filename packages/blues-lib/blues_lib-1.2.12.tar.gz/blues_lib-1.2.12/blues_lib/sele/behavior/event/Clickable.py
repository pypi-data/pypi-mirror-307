import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.behavior.Behavior import Behavior
from sele.behavior.deco.BehaviorDeco import BehaviorDeco
from entity.STDOut import STDOut

class Clickable(Behavior):

  @BehaviorDeco()
  def resolve(self):
    '''
    Deal the atom
    Returns:
      {False} : the handler can't deal with the Atom
      {STDOut} : the result of handling
    '''
    if self.kind!='clickable':
      return False 
    
    self.browser.action.mouse.click(self.selector,self.parent_selector,self.timeout)
    return STDOut()
