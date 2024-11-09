import sys,os,re
from abc import ABC,abstractmethod
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.reader.ifeng.IFengSchemaFactory import IFengSchemaFactory
from schema.reader.thepaper.ThePaperSchemaFactory import ThePaperSchemaFactory
from sele.spider.AnyMaterialSpider import AnyMaterialSpider    

class NAPS(ABC):
  '''
  1. Crawl a materail
  2. Login the publish page
  3. Publish
  4. Set published log
  '''
  def __init__(self):
    self.crawl_count = 1
  
  def multi_execute(self):
    self.spide()
    self.multi_publish()

  def execute(self):
    self.spide()
    self.publish()

  def multi_publish(self):
    pass
  
  @abstractmethod
  def publish(self):
    pass

  def spide(self):
    '''
    Crawl a material
    Return:
      {bool}
    '''
    factory = ThePaperSchemaFactory()
    thepaper_intl_schema = factory.create_news('intl')

    factory = IFengSchemaFactory()
    tech_schema = factory.create_tech_news()
    tech_outpost_schema = factory.create_tech_outpost()
    host_schema = factory.create_hot_news()

    schemas = [thepaper_intl_schema,tech_schema,tech_outpost_schema,host_schema]
    spider = AnyMaterialSpider(schemas)
    return spider.spide(self.crawl_count)
 


