import sys,os,re,json
from .DouBaoQASchema import DouBaoQASchema

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.ai.AISchemaFactory import AISchemaFactory

class DouBaoSchemaFactory(AISchemaFactory):

  def create_qa(self,question):
    return DouBaoQASchema(question)

