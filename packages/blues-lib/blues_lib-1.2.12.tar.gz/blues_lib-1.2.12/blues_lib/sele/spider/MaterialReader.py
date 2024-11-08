import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.behavior.BehaviorChain import BehaviorChain
from sele.transformer.brief.BriefTransformerChain import BriefTransformerChain
from pool.BluesMaterialIO import BluesMaterialIO  
from util.BluesURL import BluesURL 
from util.BluesConsole import BluesConsole 

class MaterialReader():
  def __init__(self,browser,schema):
    self.browser = browser
    self.schema = schema
    self.__extract_schema_fields()

  def __extract_schema_fields(self):
    self.url = self.schema.url_atom.get_value()
    # need to set this size dynamic
    self.size = self.schema.size_atom.get_value()
    self.brief_atom = self.schema.brief_atom
    self.material_atom = self.schema.material_atom
    
  def read(self):
    briefs = self.get_briefs()
    if not briefs:
      BluesConsole.error('No available briefs')
      return None

    BluesConsole.success('%s available briefs' % str(len(briefs)))

    mateirals = []
    for brief in briefs:
      self.calc_material(mateirals,brief)

      # contrl the materail size
      if len(mateirals) >= self.size:
        break

    return mateirals

  def calc_material(self,mateirals,brief):
    try:
      material = self.get_material(brief)
      # weather the detail is legal
      if BluesMaterialIO.is_legal_detail(material):
        mateirals.append({**brief,**material})
    except Exception as e:
      # some detail page is wrong
      BluesConsole.info('Crawl the material (%s), get the next one, error %s' % (brief.get('material_title'),e))

  def get_briefs(self):
    self.browser.open(self.url)
    handler = BehaviorChain(self.browser,self.brief_atom)
    outcome = handler.handle()
    # briefs dict list
    if outcome.data:
      # use transform chain get the avail briefs
      return BriefTransformerChain().handle(outcome.data)
    else:
      return outcome.data

  def get_material(self,brief):
    url = BluesMaterialIO.get_material_url(brief)
    BluesConsole.success('Crawling material: %s' % url)
    self.browser.open(url)
    handler = BehaviorChain(self.browser,self.material_atom)
    outcome = handler.handle()
    return outcome.data

