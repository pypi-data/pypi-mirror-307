import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.deco.SchemaTransformerDeco import SchemaTransformerDeco
from sele.transformer.Transformer import Transformer
from atom.Atom import Atom
from util.BluesFiler import BluesFiler
from util.BluesImager import BluesImager
from util.BluesConsole import BluesConsole

class SchemaEntityImage(Transformer):
  '''
  Replace the schema's placeholder by data
  '''
  kind = 'handler'
  default_image = 'c:/blues_lib/material/thumbnail.jpg'

  @SchemaTransformerDeco()
  def resolve(self,request):
    '''
    Parameter:
      request {dict} : the schema and value dict, such as:
        {'atom':Atom, 'value':dict}
    '''
    if not request or not request.get('atom'):
      return request

    if not request.get('value'):
      return request
    
    if not request.get('limit'):
      return request
    
    self.__replace_thumbnail(request)
    self.__replace_images(request)
    self.__limit_image(request)
    return request

  def __limit_image(self,request):
    '''
    Replace the placeholder value in the atom
    Parameter:
      entity {dict} : the key is the placeholder, the value is the real value
    '''
    # Only support to replace the atom's vlue
    image_max_length = request.get('limit').get('image_max_length')
    material_body_image = request.get('value').get('material_body_image')
    if image_max_length and material_body_image:
      request['value']['material_body_image'] = material_body_image[:image_max_length]

  def __replace_thumbnail(self,request):
    material_thumbnail = request.get('value').get('material_thumbnail')
    if not BluesFiler.exists(material_thumbnail):
      request['value']['material_thumbnail'] = self.default_image
      BluesConsole.info('Thumbnail (%s) do not exists, use the default image (%s)' % (material_thumbnail,self.default_image))
      
  def __replace_images(self,request):
    material_body_image = request.get('value').get('material_body_image')
    exists_images = []
    for image in material_body_image: 
      if not BluesFiler.exists(image):
        continue
      ratio = BluesImager.get_wh_ratio(image)
      # remove the AD banner image, width/height > 4
      if ratio>4:
        continue
      exists_images.append(image)

    if not exists_images:
      exists_images.append(self.default_image)
      BluesConsole.info('All images (%s) do not exists, use the default image (%s)' % (material_body_image,self.default_image))

    request['value']['material_body_image'] = exists_images
      







