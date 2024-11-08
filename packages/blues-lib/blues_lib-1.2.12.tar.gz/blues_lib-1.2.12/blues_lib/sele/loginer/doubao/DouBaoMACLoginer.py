import sys,os,re,time
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.behavior.BehaviorChain import BehaviorChain
from sele.loginer.MACLoginer import MACLoginer
from schema.loginer.doubao.DouBaoLoginerSchemaFactory import DouBaoLoginerSchemaFactory
from util.BluesDateTime import BluesDateTime

class DouBaoMACLoginer(MACLoginer):

  def create_schema(self):
    factory = DouBaoLoginerSchemaFactory()
    self.schema = factory.create_mac()

  def code(self):
    '''
    @override : input one char one time
    '''
    for char in self.auth_code:
      self.code_atom.set_value(char)
      handler = BehaviorChain(self.browser,self.code_atom)
      handler.handle()
      time.sleep(1)
  
  def submit(self):
    '''
    @override : Doubao will submit automatically after the auth code filled
    '''
    pass
