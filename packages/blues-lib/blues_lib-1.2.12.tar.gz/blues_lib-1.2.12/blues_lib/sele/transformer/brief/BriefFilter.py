import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.deco.BriefTransformerDeco import BriefTransformerDeco
from sele.transformer.Transformer import Transformer
from pool.BluesMaterialIO import BluesMaterialIO  

class BriefFilter(Transformer):
  '''
  Remove the unavailable breifs
  '''
  kind = 'handler'

  @BriefTransformerDeco()
  def resolve(self,briefs):
    if not briefs:
      return None
    
    return self.__filter(briefs)

  def __filter(self,briefs):
    avail_briefs = [] 
    for brief in briefs:
      if BluesMaterialIO.is_legal_brief(brief) and not BluesMaterialIO.exist(brief):
        avail_briefs.append(brief)

    return avail_briefs

