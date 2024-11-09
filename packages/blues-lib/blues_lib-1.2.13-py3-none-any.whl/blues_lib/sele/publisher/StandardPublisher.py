import sys,os,re,time
from .Publisher import Publisher
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from pool.BluesMaterialIO import BluesMaterialIO
from report.MaterialReport import MaterialReport
from util.BluesConsole import BluesConsole

class StandardPublisher(Publisher):
  
  def test(self):
    self.open()

  def accept(self,visitor):
    '''
    Double dispatch with visitor
    Parameters:
      visitor { Visitor }
    '''
    visitor.visit_standard(self)

  def clean(self):
    '''
    Update the meterial's status
    '''
    material_id = self.material.get('material_id')
    entity = {'material_status':self.material['material_status']}      
    conditions = [
      {'field':'material_id','comparator':'=','value':material_id}
    ]
    response = BluesMaterialIO.update(entity,conditions)
    if response.get('code') == 200 and response.get('count') == 1:
      BluesConsole.success('Updated the material status to [%s] successfully' % self.material['material_status'])
    else:
      BluesConsole.error('Updated the material status to [%s] failure, error: %s' % (self.material['material_status'],response.get('message')))

  def record(self):
    platform = self.schema.PLATFORM
    channel = self.schema.CHANNEL
    report = MaterialReport(self.browser,self.material,platform,channel)
    report.execute()
    


