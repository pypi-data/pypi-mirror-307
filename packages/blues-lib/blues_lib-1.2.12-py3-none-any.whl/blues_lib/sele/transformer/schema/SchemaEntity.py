import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.deco.SchemaTransformerDeco import SchemaTransformerDeco
from sele.transformer.Transformer import Transformer
from pool.BluesMaterialIO import BluesMaterialIO

class SchemaEntity(Transformer):
  '''
  Replace the schema's palceholder by data
  '''
  kind = 'handler'

  @SchemaTransformerDeco()
  def resolve(self,request):
    '''
    Parameter:
      request {dict} : the schema and value dict, such as:
        {'atom':Atom, 'value':dict}
    '''
    if not request or not request.get('atom'):
      return request
    
    # If pass a value ,don't get again
    if request.get('value'):
      return request
    
    request['value'] = self.__get_latest_material()
    return request

  def __get_latest_material(self):
    response = BluesMaterialIO.latest()
    data = response.get('data')
    if not data:
      return None

    material = data[0]
    title = material.get('material_title')
    texts = json.loads(material.get('material_body_text'))
    # append the title as the first line
    images = json.loads(material.get('material_body_image'))
    body = json.loads(material.get('material_body'))
    
    # convert the json to object
    material['material_body_text']=texts
    material['material_body_image']=images
    material['material_body']=body
    return material

