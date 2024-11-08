import sys,os,re,json
from .DouBaoQA import DouBaoQA
from .MoshuQA import MoshuQA
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from pool.BluesMaterialIO import BluesMaterialIO     
from util.BluesConsole import BluesConsole

class AIRewriter():
  '''
  This class writer the input news
  '''
  
  def __init__(self,ai_name='doubao'):
    '''
    Paramters:
      ai {str} : The ai name 
    '''
    # { AIQA }
    self.ai_name = ai_name

  def get_ai_qa(self,question):
    if self.ai_name=='doubao':
      return DouBaoQA(question)
    elif self.ai_name=='moshu':
      return MoshuQA(question)

  def rewrite(self,article,length=800):
    if not article:
      BluesConsole.error('No article for question')
      return

    question = self.get_question(article,length)
    ai_qa = self.get_ai_qa(question)
    fields = ai_qa.execute()
    BluesConsole.info('Rewrited fields: %s' % fields)
    return fields

  def rewrite_by_texts(self,texts,length=800):
    '''
    Parameters:
       texts {json or list} : 
    '''
    article = self.get_article_by_texts(texts)
    return self.rewrite(article,length)

  def rewrite_by_id(self,id='',length=800):
    article = self.get_article_by_id(id)
    return self.rewrite(article,length)

  def get_question(self,article,length=800):
    q = '重写下面这则新闻，要求%s字以内，分段明确，移除文中的广告、订阅信息和作者，提供一个震撼的标题： %s' % (length,article)
    return q

  def get_article_by_texts(self,texts):
    '''
    Get the rewrite question from the text list
    Parameter:
      texts {json or list} the article's para list
    '''
    paras = texts
    if type(texts) == str:
      paras = json.loads(texts)
    article = ''
    for para in paras:
      article+=para
    return article

  def get_article_by_id(self,id=''):
    '''
    Get a full content from body para list
    '''
    material_body_text = self.get_material(id)
    if not material_body_text:
      return None
    else:
      return self.get_article_by_texts(material_body_text)

  def get_material(self,id=''):
    if id:
      conditions = [
        {'field':'material_id','comparator':'=','value':id}, # ifeng.com_8dZIWYbSBUs 
      ]
      response = BluesMaterialIO.get('*',conditions)
    else:
      response = BluesMaterialIO.random()

    if response['data']:
      texts = response['data'][0]['material_body_text']
      if texts:
        return texts
      else:
        BluesConsole.error('Bad row data,no texts: %s' % response)
        return None

    else:
      BluesConsole.error('No material : %s' % response)
      return None

    


