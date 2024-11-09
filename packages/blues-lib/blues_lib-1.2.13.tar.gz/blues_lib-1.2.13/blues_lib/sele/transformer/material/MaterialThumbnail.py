import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.deco.MaterialTransformerDeco import MaterialTransformerDeco
from sele.transformer.Transformer import Transformer
from pool.BluesMaterialIO import BluesMaterialIO
from util.BluesURL import BluesURL 

class MaterialThumbnail(Transformer):
  '''
  Extend the required fields by existed fields
  '''
  kind = 'handler'

  @MaterialTransformerDeco()
  def resolve(self,materials):
    if not materials:
      return None
    
    for material in materials:
      self.__download(material)

    return materials

  def __download(self,material):
    # convert online image to local image
    material['material_thumbnail'] = BluesMaterialIO.get_download_thumbnail(material)
