import sys,os,re
from .BriefExtender import BriefExtender  
from .BriefFilter import BriefFilter  
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.deco.BriefTransformerDeco import BriefTransformerDeco
from sele.transformer.Transformer import Transformer

class BriefTransformerChain(Transformer):
  '''
  Basic behavior chain, it's a handler too
  '''
  kind = 'chain'

  @BriefTransformerDeco()
  def resolve(self,briefs):
    '''
    Deal the atom by the event chain
    '''
    handler = self.__get_chain()
    format_briefs = handler.handle(briefs)
    return format_briefs if format_briefs else None

  def __get_chain(self):
    '''
    Converters must be executed sequentially
    '''
    # writer
    extender = BriefExtender()
    filter = BriefFilter()

    extender.set_next(filter)

    return extender
