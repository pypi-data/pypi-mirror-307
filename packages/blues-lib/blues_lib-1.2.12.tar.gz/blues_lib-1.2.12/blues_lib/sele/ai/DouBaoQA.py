import sys,os,re,json
from .AIQA import AIQA
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.ai.doubao.DouBaoSchemaFactory import DouBaoSchemaFactory
from sele.loginer.doubao.DouBaoLoginerFactory import DouBaoLoginerFactory   

class DouBaoQA(AIQA):
  
  def __init__(self,question=''):
    # { AIQASchema }
    schema = DouBaoSchemaFactory().create_qa(question)
    # { Loginer } set loginer for relogin
    loginer = DouBaoLoginerFactory().create_mac()

    super().__init__(schema,loginer,'button[data-testid="to_login_button"')

    # { int } wait the AI answer
    self.waiting_timeout = 20

  def extract(self,ai_entity):
    '''
    Template method: extract title and para list from the text square
    Parameters:
      ai_entity {dict} : such as {'title':'text','content':'xxx\n\nxxx\n\nxxx'}
    Returns:
      {dict} : {'title':'xxx','paras':'json of text list'}
    '''
    title = ai_entity['title'] if ai_entity['title'] else ai_entity.get('title_2')
    content = ai_entity['content'] if ai_entity['content'] else ai_entity.get('content_2')
    title = self.__get_title(title)
    return self.__get_field_dict(title,content)

  def __get_field_dict(self,title,content):
    '''
    Returns {json} : json of str list
    '''
    # remov all " for convert to json
    paras = content.replace('"',"'").split('\n\n')
    # remove the title
    title_para = paras.pop(0)
    if not paras:
      return None

    field_dict = {
      'paras':json.dumps(paras,ensure_ascii=False),
      'title':title
    }
    if field_dict['title']:
      return field_dict 

    field_dict['title'] = self.__get_title(title_para)
    if field_dict['title']:
      return field_dict 
    else:
      return None

  def __get_title(self,title):
    if not title:
      return ''

    # pattern 1 : 标题：《xxx》
    matcheds_01 = re.findall(r'《(.+)》',title)
    # pattern 2: 标题: xxx
    matcheds_02 = re.findall(r'标题\s*[:：]?\s*(.+)',title)
    # If have no title, don't use the ai result
    if matcheds_01:
      return matcheds_01[0]
    if matcheds_02:
      return matcheds_02[0]

    return title
