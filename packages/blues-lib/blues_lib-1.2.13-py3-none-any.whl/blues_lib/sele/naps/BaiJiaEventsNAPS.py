import sys,os,re

from .NAPS import NAPS
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from pool.MaterialLogIO import MaterialLogIO
from schema.releaser.baijia.BaiJiaSchemaFactory import BaiJiaSchemaFactory
from sele.loginer.baijia.BaiJiaLoginerFactory import BaiJiaLoginerFactory   
from sele.publisher.StandardPublisher import StandardPublisher
from sele.publisher.visitor.MultiVisitor import MultiVisitor
from util.BluesConsole import BluesConsole

class BaiJiaEventsNAPS(NAPS):
  '''
  1. Crawl a materail
  2. Login the publish page
  3. Publish
  4. Set published log
  '''
  DAILY_LIMIT = {
    'events':10,
    'news':5,
  }

  def __init__(self):
    super().__init__()

    self.method_count = {
      'create_news':0,
      'create_events':0,
    }

    self.set_count()
  
  def set_count(self):
    avail_limit = self.get_avail_limit()
    crawl_count = 0
    # only get one in one channel
    if avail_limit['events']>0:
      crawl_count+=1
      self.method_count['create_events'] =1
    if avail_limit['news']>0:
      crawl_count+=1
      self.method_count['create_news'] =1
    
    if crawl_count==0:
      raise Exception('Daily limit reached!')

    self.crawl_count = crawl_count
    BluesConsole.info('Will crawl %s materails: %s' % (self.crawl_count,self.method_count))

  def get_avail_limit(self):
    events = MaterialLogIO.get_today_pubed_count('baijia','events')['count']
    news = MaterialLogIO.get_today_pubed_count('baijia','news')['count']
    return {
      'events':self.DAILY_LIMIT['events']-events,
      'news':self.DAILY_LIMIT['news']-news,
    }

  def multi_publish(self):
    loginer_factory = BaiJiaLoginerFactory()
    loginer = loginer_factory.create_account()

    factory = BaiJiaSchemaFactory()
    schema = factory.create_events()
    visitor = MultiVisitor(factory,self.method_count)
    # this schema just for loginer
    publisher = StandardPublisher(schema,loginer)
    publisher.accept(visitor)

  def publish(self):
    loginer_factory = BaiJiaLoginerFactory()
    loginer = loginer_factory.create_account()

    factory = BaiJiaSchemaFactory()
    schema = factory.create_events()

    publisher = StandardPublisher(schema,loginer)
    publisher.publish()


