import sys,os,re,time
from abc import ABC,abstractmethod
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from sele.browser.BluesLoginChrome import BluesLoginChrome    
from sele.behavior.FormBehavior import FormBehavior       
from util.BluesConsole import BluesConsole
from util.BluesDateTime import BluesDateTime

class Publisher(ABC):

  def __init__(self,schema=None,loginer=None):
    # { Loginer } the site's loginer
    self.loginer = loginer
    # { BluesLoginChrome } login auto
    self.browser = None
    # publish status: 'available','published','pubsuccess','pubfailure','illegal'
    self.set_schema(schema)

  def set_schema(self,schema):
    '''
    Set the schema after the publisher intance created
    '''
    if schema:
      # { ReleaserSchema } 
      self.schema = schema
    # { Dict } material, in multi vistor, don't need pass schema in init
      self.material = schema.material
      self.url = schema.url_atom.get_value()
    else:
      self.schema = None
      self.material = None
      self.url = ''
  
  @abstractmethod
  def accept(self,visitor):
    '''
    Double dispatch with visitor
    '''
    pass

  def accept_test(self,visitor,callback):
    visitor.visit_test(self,callback)

  def publish(self,is_pre=False):
    '''
    @description : the final method
    '''
    if not self.material:
      BluesConsole.error('No available materials')
      return False
    self.login()
    self.release(is_pre)
    self.quit()

  def pre_publish(self):
    self.publish(True)

  def release(self,is_pre=False):
    '''
    Fill the form and submit
    Parameters:
      is_pre {bool} : is pre-publish, if Ture: just preview don't submit
    '''
    try:
      self.open()
      self.fill_richtext() # only news need
      self.fill()
      self.verify_before_submit()
      self.preview()
      if not is_pre:
        self.submit()
        self.verify_after_submit()
    except Exception as e:
      self.catch(e)
    finally:
      if not is_pre:
        self.clean()
        self.record()
      else:
        BluesDateTime.count_down({'duration':30,'title':'preview...'})

  
  def login(self):
    self.browser = BluesLoginChrome(self.url,self.loginer)

  def open(self):
    self.browser.open(self.url)
    BluesConsole.success('Opened form page: %s' % self.browser.interactor.document.get_title())

  def quit(self):
    if self.browser:
      self.browser.quit()

  def fill(self):
    '''
    @description : override by the concrete publisher
    '''

    fill_atom = self.schema.fill_atom
    popup_atom = self.schema.popup_atom
    handler = FormBehavior(self.browser,fill_atom,popup_atom)
    handler.handle()
    BluesConsole.info('Form filled')

  def fill_richtext(self):
    richtext_atom = self.schema.richtext_atom
    popup_atom = self.schema.popup_atom
    if not richtext_atom:
      return
    
    handler = FormBehavior(self.browser,richtext_atom,popup_atom)
    handler.handle()
    BluesConsole.info('Fill the richtext')

  def verify_before_submit(self):
    '''
    Verify is all required fields filled
    Use the fill_atom to verify
    '''
    BluesConsole.info('Form filled successfully')

  def preview(self):
    '''
    @description : preview before submit
    '''
    preview_atom = self.schema.preview_atom
    popup_atom = self.schema.popup_atom
    if preview_atom:
      handler = FormBehavior(self.browser,preview_atom,popup_atom)
      handler.handle()
      BluesConsole.info('Preview successfully')

  def submit(self):
    '''
    @description : submit
    '''
    submit_atom = self.schema.submit_atom
    popup_atom = self.schema.popup_atom
    if submit_atom:
      handler = FormBehavior(self.browser,submit_atom,popup_atom)
      handler.handle()
      BluesConsole.info('Submited successfully')

  def verify_after_submit(self):
    '''
    Verify whether the publication is successful.
    If the publication is successful and the page jumps, then the publishing button element will not exist.
    '''
    # Use the form page's submit element to make sure weather published succesfully

    if self.browser.waiter.ec.url_changes(self.url,10):
      self.material['material_status'] = 'pubsuccess'
      BluesConsole.success('Published successfully.')
    else:
      self.material['material_status'] = 'pubfailure'
      BluesConsole.error('Published failure')

  def catch(self,e):
    self.material['material_status'] = 'pubfailure'
    BluesConsole.error(e,'Publish failure')
    
  def clean(self):
    '''
    Update the meterial's status
    '''
    pass

  def record(self):
    pass
    


