import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.deco.SchemaTransformerDeco import SchemaTransformerDeco
from sele.transformer.Transformer import Transformer
from atom.Atom import Atom

class SchemaSelectorReplacer(Transformer):
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
    
    self.__fill_value(request)
    return request

  def __fill_value(self,request):
    '''
    Replace the placeholder value in the atom
    Parameter:
      entity {dict} : the key is the placeholder, the value is the real value
    '''
    # Only support to replace the atom's vlue
    atom = request.get('atom')
    value = request.get('value')

    if type(atom) == list:
      for atom_item in atom:
        self.__set_atom_selector(atom_item,value)
    else:
      self.__set_atom_selector(atom,value)

    if type(atom) == dict:
      for atom_item in atom.values():
        self.__set_atom_selector(atom_item,value)
    else:
      self.__set_atom_selector(atom,value)

  def __set_atom_selector(self,atom_node,entity):
    if not atom_node:
      return
    
    # only deal with atom node
    if not isinstance(atom_node,Atom):
      return

    # find the child nodes
    atom_value = atom_node.get_value()

    if isinstance(atom_value,list):
      for sub_atom_value in atom_value:
        if isinstance(sub_atom_value,Atom):
          self.__replace_selector(sub_atom_value,entity)
          self.__set_atom_selector(sub_atom_value,entity)
      
    elif isinstance(atom_value,dict):
      for key,sub_atom_value in atom_value.items():
        if isinstance(sub_atom_value,Atom):
          self.__replace_selector(sub_atom_value,entity)
          self.__set_atom_selector(sub_atom_value,entity)

    else:
      # replace the current node's selector
      self.__replace_selector(atom_node,entity)

  def __replace_selector(self,atom_node,entity):
    if not hasattr(atom_node,'get_selector_template') or not entity:
      return 
    
    selector_template = atom_node.get_selector_template()
    if not selector_template:
      return 

    # pattern matched
    if not re.search(r'\$\{.+\}',selector_template):
      return

    for key in entity:
      pattern = r'\$\{'+key+r'\}'

      if not re.search(pattern,selector_template):
        continue

      value = str(entity.get(key))
      selector = re.sub(pattern,value,selector_template)
      atom_node.set_selector(selector)
      break

