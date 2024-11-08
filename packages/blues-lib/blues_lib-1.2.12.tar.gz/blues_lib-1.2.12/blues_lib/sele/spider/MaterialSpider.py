import sys,re,os,json
from .MaterialReader  import MaterialReader  
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.browser.BluesStandardChrome import BluesStandardChrome
from sele.transformer.material.MaterialTransformerChain import MaterialTransformerChain
from pool.BluesMaterialIO import BluesMaterialIO
from util.BluesConsole import BluesConsole 

class MaterialSpider():

  def __init__(self,schema):
    self.schema = schema 
    # the original authors, they should be replaced by the system author
    self.browser = BluesStandardChrome()
    self.system_author = '深蓝'

  def read(self):
    reader = MaterialReader(self.browser,self.schema)
    rows = reader.read()
    return rows

  def spide(self):
    rows = self.read()
    stat = True
    if not rows:
      BluesConsole.error('No available briefs')
      stat = False
    else:
      BluesConsole.success('Crawled %s briefs' % str(len(rows)))
      format_materials = MaterialTransformerChain().handle(rows)
      result = BluesMaterialIO.insert(format_materials)
      if result['code'] == 200:
        BluesConsole.success('Inserted %s materials successfully' % result['count'])
      else:
        BluesConsole.error('Failed to insert, %s' % result.get('message'))
        stat = False

    self.browser.quit()
    return stat

