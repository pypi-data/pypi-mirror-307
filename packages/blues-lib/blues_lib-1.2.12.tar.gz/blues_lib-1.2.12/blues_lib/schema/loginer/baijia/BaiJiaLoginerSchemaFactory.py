import sys,os,re
from .BaiJiaAccountLoginerSchema import BaiJiaAccountLoginerSchema
from .BaiJiaMACLoginerSchema import BaiJiaMACLoginerSchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.LoginerSchemaFactory import LoginerSchemaFactory

class BaiJiaLoginerSchemaFactory(LoginerSchemaFactory):

  def create_account(self):
    return BaiJiaAccountLoginerSchema()

  def create_mac(self):
    return BaiJiaMACLoginerSchema()
