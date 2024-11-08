import sys,os,re
from .DouBaoMACLoginerSchema import DouBaoMACLoginerSchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.LoginerSchemaFactory import LoginerSchemaFactory

class DouBaoLoginerSchemaFactory(LoginerSchemaFactory):

  def create_account(self):
    pass

  def create_mac(self):
    return DouBaoMACLoginerSchema()
