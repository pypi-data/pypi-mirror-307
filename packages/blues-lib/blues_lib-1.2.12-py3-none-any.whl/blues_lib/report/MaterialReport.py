import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from pool.BluesMaterialIO import BluesMaterialIO
from pool.MaterialLogIO import MaterialLogIO
from util.BluesDateTime import BluesDateTime
from util.BluesURL import BluesURL
from util.BluesConsole import BluesConsole

class MaterialReport():

  def __init__(self,browser,material,platform='',channel=''):
    self.browser = browser
    self.material = material
    self.platform = platform
    self.channel = channel

  def execute(self):
    shot_path = self.screenshot()
    entity = {
      'pub_m_id':self.material['material_id'],
      'pub_m_title':self.material['material_title'],
      'pub_date':BluesDateTime.get_now(),
      'pub_status':self.material['material_status'],
      'pub_platform':self.platform,
      'pub_channel':self.channel,
      'pub_screenshot':shot_path
    }
    response = MaterialLogIO.insert(entity)
    if response.get('code') == 200 and response.get('count') == 1:
      BluesConsole.success('Inserted log successfully')
    else:
      BluesConsole.error('Inserted log failure, error: %s' % response.get('message'))
  
  def screenshot(self):
    '''
    Record the submission log
    If submit failure, make a screenshot
    '''
    dirs = [self.material['material_site']]
    file_name = '%s_%s.png' % (self.material['material_status'],self.material['material_id'])
    shot_dir = BluesMaterialIO.get_screenshot_dir(dirs)
    file_path = BluesURL.get_file_path(shot_dir,file_name)
    return self.browser.interactor.window.screenshot(file_path)

