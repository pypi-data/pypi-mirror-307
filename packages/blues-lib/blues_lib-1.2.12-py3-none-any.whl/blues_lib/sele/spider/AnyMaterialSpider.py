import sys,os,re
from .MaterialSpider import MaterialSpider    
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesConsole import BluesConsole

class AnyMaterialSpider(MaterialSpider):
  '''
  Invoke any a spider, then stop
  '''

  def __init__(self,schemas):
    '''
    Parameters:
      schemas {list<Schema>} : multi reader schema
    '''
    self.schemas = schemas

  def spide(self,count=1):
    '''
    Spide multi matrails in multi schema pages
    Paramters:
      count {int} : the crawled count
    returns 
      {int}  : the crawled count
    '''
    crawl_count = 0
    for schema in self.schemas:
      # use one schema crawl until have no avail materail
      while crawl_count<count and MaterialSpider(schema).spide():
        crawl_count+=1
        BluesConsole.info('Crawl the %s / %s material' % (crawl_count,count))

      if crawl_count>=count:
        break

    return crawl_count
