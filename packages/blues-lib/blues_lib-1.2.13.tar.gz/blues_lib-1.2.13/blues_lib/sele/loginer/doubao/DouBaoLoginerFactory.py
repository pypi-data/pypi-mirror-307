import sys,os,re
from .DouBaoMACLoginer import DouBaoMACLoginer   
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.loginer.LoginerFactory import LoginerFactory

class DouBaoLoginerFactory(LoginerFactory):
  def create_mac(self,once=False):
    return DouBaoMACLoginer(once)

