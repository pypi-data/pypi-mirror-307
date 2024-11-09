import sys,os,re,json
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.ai.AIQASchema import AIQASchema

class DouBaoQASchema(AIQASchema):

  def create_url_atom(self):
    self.url_atom = self.atom_factory.createURL('QA page url','https://www.doubao.com/chat/')

  def create_question_atom(self):
    atoms = [
      # value placeholder 2: material_body_text
      self.atom_factory.createClickable('swich','div[data-testid="create_conversation_button"]'),
      self.atom_factory.createInput('input','textarea.semi-input-textarea','${question}'),
    ]

    self.question_atom = self.atom_factory.createArray('question',atoms)

  def create_submit_atom(self):
    atoms = [
      # value placeholder 2: material_body_text
      self.atom_factory.createClickable('submit','#flow-end-msg-send'),
    ]

    self.submit_atom = self.atom_factory.createArray('submit',atoms)

  def create_answer_atom(self):
    '''
    Fetch the title and content as a text block
    The line will be split by \n\n
    This seletor suport left and right receive message
    '''
    para_field_atoms = [
      # main selector
      self.atom_factory.createText('title','div[class^=right-side] .flow-markdown-body h1'),
      self.atom_factory.createText('content','div[class^=right-side] .flow-markdown-body'),
      # spare selector
      self.atom_factory.createText('title_2','div[data-testid="receive_message"] .message-content h1'),
      self.atom_factory.createText('content_2','div[data-testid="receive_message"] .message-content'),
    ]
    self.answer_atom = self.atom_factory.createArray('title and content',para_field_atoms) 

  def __get_standard_answer_atom(self):
    '''
    The standard receive message atom
    '''
    para_unit_selector = 'div[data-testid="receive_message"] .message-content'
    para_field_atoms = [
      # use the para selector
      self.atom_factory.createText('text',''),
    ]
    para_array_atom = self.atom_factory.createArray('para fields',para_field_atoms) 
    self.answer_atom = self.atom_factory.createPara('answer',para_unit_selector,para_array_atom) 

