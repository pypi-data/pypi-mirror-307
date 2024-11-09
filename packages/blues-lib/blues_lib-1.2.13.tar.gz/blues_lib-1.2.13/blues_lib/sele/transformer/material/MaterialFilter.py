import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.deco.MaterialTransformerDeco import MaterialTransformerDeco
from sele.transformer.Transformer import Transformer
from pool.BluesMaterialIO import BluesMaterialIO  

class MaterialFilter(Transformer):
  '''
  Remove the unavailable breifs
  '''
  kind = 'handler'

  @MaterialTransformerDeco()
  def resolve(self,materials):
    if not materials:
      return None
    
    return self.__filter(materials)

  def __filter(self,materials):
    avail_materials = [] 
    for material in materials:
      if BluesMaterialIO.is_legal_material(material):
        avail_materials.append(material)

    return avail_materials

