import sys,os,re,time

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.loginer.AccountLoginer import AccountLoginer
from schema.loginer.baijia.BaiJiaLoginerSchemaFactory import BaiJiaLoginerSchemaFactory

class BaiJiaAccountLoginer(AccountLoginer):

  def create_schema(self):
    factory = BaiJiaLoginerSchemaFactory()
    self.schema = factory.create_account()

  
