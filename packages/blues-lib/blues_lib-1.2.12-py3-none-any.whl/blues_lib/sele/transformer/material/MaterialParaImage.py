import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.deco.MaterialTransformerDeco import MaterialTransformerDeco
from sele.transformer.Transformer import Transformer
from pool.BluesMaterialIO import BluesMaterialIO
from util.BluesURL import BluesURL 

class MaterialParaImage(Transformer):
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
    paras = material.get('material_body')
    material_thumbnail = material.get('material_thumbnail')
    image_count = 0
    for para in paras:
      # download and deal image
      if para['type'] == 'image':
        image_count += 1
        para['value'] = BluesMaterialIO.get_download_image(material,para['value'])
    
    # make sure have at least one image
    if not image_count:
      paras.append({'type':'image','value':material_thumbnail})

