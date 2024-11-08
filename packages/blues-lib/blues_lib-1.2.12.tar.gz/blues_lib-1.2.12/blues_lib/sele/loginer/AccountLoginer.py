import sys,os,re
from abc import ABC,abstractmethod
from .Loginer import Loginer
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.behavior.BehaviorChain import BehaviorChain

class AccountLoginer(Loginer,ABC):

  def create_subtype_fields(self):
    # { ArrayAtom } the switch atom list
    self.switch_atom = self.schema.switch_atom    
    # { ArrayAtom } the fill atom list
    self.fill_atom = self.schema.fill_atom    
    # { ArrayAtom } the submit atom list
    self.submit_atom = self.schema.submit_atom    
    
  def perform(self):
    '''
    Implement the template method
    '''
    self.switch() 
    self.fill() 
    self.submit() 
  
  def switch(self):
    handler = BehaviorChain(self.browser,self.switch_atom)
    handler.handle()

  def fill(self):
    handler = BehaviorChain(self.browser,self.fill_atom)
    handler.handle()

  def submit(self):
    handler = BehaviorChain(self.browser,self.submit_atom)
    handler.handle()
