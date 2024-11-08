import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.deco.MaterialTransformerDeco import MaterialTransformerDeco
from sele.transformer.Transformer import Transformer
from sele.ai.AIRewriter import AIRewriter
from pool.BluesMaterialIO import BluesMaterialIO
from util.BluesURL import BluesURL 

class MaterialAIRewriter(Transformer):
  '''
  Extend the required fields by existed fields
  '''
  kind = 'handler'

  @MaterialTransformerDeco()
  def resolve(self,materials):
    if not materials:
      return None
    
    for material in materials:
      self.__rewrite(material)

    return materials

  def __rewrite(self,material):
    rewriter = AIRewriter('doubao')
    result = rewriter.rewrite_by_texts(material['material_body_text'],800)
    if result:
      # save the original value to the ori field
      material['material_ori_title'] = material['material_title']
      material['material_ori_body_text'] = material['material_body_text']
      # use ai firstly
      material['material_title'] = result['title']
      material['material_body_text'] = result['paras']

