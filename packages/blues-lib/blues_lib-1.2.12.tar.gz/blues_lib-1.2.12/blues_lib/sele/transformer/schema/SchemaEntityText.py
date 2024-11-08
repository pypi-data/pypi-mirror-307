import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.deco.SchemaTransformerDeco import SchemaTransformerDeco
from sele.transformer.Transformer import Transformer
from atom.Atom import Atom

class SchemaEntityText(Transformer):
  '''
  Replace the schema's placeholder by data
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

    if not request.get('value'):
      return request
    
    if not request.get('limit'):
      return request
    
    self.__limit_content(request)
    self.__limit_title(request)
    return request

  def __limit_content(self,request):
    '''
    Replace the placeholder value in the atom
    Parameter:
      entity {dict} : the key is the placeholder, the value is the real value
    '''
    # Only support to replace the atom's vlue
    title_max_length = request.get('limit').get('title_max_length')
    content_max_length = request.get('limit').get('content_max_length')
    material_body_text = request.get('value').get('material_body_text')
    material_title = request.get('value').get('material_title')
    if content_max_length and material_body_text:

      # add title to the content in the events channel
      if material_title and not title_max_length:
        material_body_text.insert(0,'[%s] ' % material_title)

      limit_material_body_text = []
      length = 0
      for para in material_body_text:
        if length<content_max_length:
          limit_material_body_text.append(para)
          length += len(para)

      request['value']['material_body_text'] = limit_material_body_text

  def __limit_title(self,request):
    '''
    Replace the placeholder value in the atom
    Parameter:
      entity {dict} : the key is the placeholder, the value is the real value
    '''
    # Only support to replace the atom's vlue
    title_max_length = request.get('limit').get('title_max_length')
    material_title = request.get('value').get('material_title')

    if title_max_length and material_title:
      if len(material_title)>title_max_length:
        end_index = title_max_length-3
        limit_material_title = material_title[:end_index]+'...'
        request['value']['material_title'] = limit_material_title




