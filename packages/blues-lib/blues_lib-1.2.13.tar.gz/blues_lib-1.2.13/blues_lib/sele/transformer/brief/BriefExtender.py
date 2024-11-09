import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.deco.BriefTransformerDeco import BriefTransformerDeco
from sele.transformer.Transformer import Transformer
from util.BluesURL import BluesURL 

class BriefExtender(Transformer):
  '''
  Extend the required fields by existed fields
  '''
  kind = 'handler'

  @BriefTransformerDeco()
  def resolve(self,briefs):
    if not briefs:
      return None
    
    for brief in briefs:
      self.__extend(brief)

    return briefs

  def __extend(self,brief):
    url = brief['material_url']
    material_site = BluesURL.get_main_domain(url)
    material_id = material_site+'_'+BluesURL.get_file_name(url)
    brief['material_id'] = material_id
    brief['material_site'] = material_site

