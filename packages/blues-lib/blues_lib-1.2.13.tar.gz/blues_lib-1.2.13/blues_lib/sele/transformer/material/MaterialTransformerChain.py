import sys,os,re
from .MaterialThumbnail import MaterialThumbnail  
from .MaterialParaImage import MaterialParaImage  
from .MaterialParaText import MaterialParaText  
from .MaterialExtender import MaterialExtender  
from .MaterialAIRewriter import MaterialAIRewriter  
from .MaterialFilter import MaterialFilter  

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.deco.MaterialTransformerDeco import MaterialTransformerDeco
from sele.transformer.Transformer import Transformer

class MaterialTransformerChain(Transformer):
  '''
  Basic behavior chain, it's a handler too
  '''
  kind = 'chain'

  @MaterialTransformerDeco()
  def resolve(self,materials):
    '''
    Deal the atom by the event chain
    '''
    handler = self.__get_chain()
    format_materials = handler.handle(materials)
    return format_materials if format_materials else None

  def __get_chain(self):
    '''
    Converters must be executed sequentially
    '''
    # writer
    thumbnail = MaterialThumbnail()
    para_image = MaterialParaImage()
    para_text = MaterialParaText()
    extender = MaterialExtender()
    rewriter = MaterialAIRewriter()
    filter = MaterialFilter()

    thumbnail.set_next(para_image) \
      .set_next(para_text) \
      .set_next(extender) \
      .set_next(rewriter) \
      .set_next(filter)

    return thumbnail
