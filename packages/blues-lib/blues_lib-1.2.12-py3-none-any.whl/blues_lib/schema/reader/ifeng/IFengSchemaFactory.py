import sys,re,os
from .IFengTechNewsSchema import IFengTechNewsSchema
from .IFengHotNewsSchema import IFengHotNewsSchema
from .IFengTechOutpostSchema import IFengTechOutpostSchema
from .IFengGallerySchema import IFengGallerySchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.reader.ReaderSchemaFactory import ReaderSchemaFactory

class IFengSchemaFactory(ReaderSchemaFactory):

  def create_tech_news(self):
    return IFengTechNewsSchema()

  def create_hot_news(self):
    return IFengHotNewsSchema()

  def create_tech_outpost(self):
    return IFengTechOutpostSchema()

  def create_gallery(self):
    return IFengGallerySchema()
