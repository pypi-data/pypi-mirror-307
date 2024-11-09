import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.deco.BriefTransformerDeco import BriefTransformerDeco
from sele.transformer.Transformer import Transformer
from entity.STDOut import STDOut
from pool.BluesMaterialLogIO import BluesMaterialLogIO
from util.BluesURL import BluesURL 

class MaterialQuota(Transformer):
  '''
  Extend the required fields by existed fields
  '''
  kind = 'handler'
  daily_qty_limit = {
    'events':12,
    'news':8,
  }

  @BriefTransformerDeco()
  def resolve(self,material,platform,channel):
    if not material:
      return STDOut(404,'input material is None')
    else:
      return self.__limit(material,platform,channel) 

  def __limit(self,material,platform,channel):
    today_pubed_qty = BluesMaterialLogIO.get_today_pubed_qty(platform,channel)
    limit = self.daily_qty_limit['channel']
    if today_pubed_qty > limit:
      return STDOut(500,'Today limit (%s) is used up' % limit)
    else:
      return STDOut(200,'Today %sth' % today_pubed_qty+1)

