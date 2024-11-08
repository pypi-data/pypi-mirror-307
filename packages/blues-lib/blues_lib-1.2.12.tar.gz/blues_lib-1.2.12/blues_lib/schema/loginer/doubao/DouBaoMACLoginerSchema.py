import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.MACLoginerSchema import MACLoginerSchema

class DouBaoMACLoginerSchema(MACLoginerSchema):

  # === create base fields ===
  def create_log_in_atom(self):
    # Base atom
    self.log_in_atom = self.atom_factory.createURL('Page URL','https://www.doubao.com/chat/')

  def create_log_in_element_atom(self):
    self.log_in_element_atom = self.atom_factory.createElement('login page ele','button[data-testid="to_login_button"')

  def create_proxy_atom(self):
    # Base atom
    config = {
      'scopes': ['.*doubao.com.*'],
    }
    self.proxy_atom = self.atom_factory.createData('proxy config',config)

  def create_cookie_filter_atom(self):
    # Base atom
    config = {
      'url_pattern':'/profile/self',
      'value_pattern':None
    }
    self.cookie_filter_atom = self.atom_factory.createData('cookie filter config',config)
  
  # === create mac subclass fields ===
  def create_switch_atom(self):
    # Typed atom
    atom = [
      # load the main content in 60 seconds
      self.atom_factory.createClickable('Popup the login dialog','button[data-testid="to_login_button"',timeout=60),
    ]
    self.switch_atom = self.atom_factory.createArray('switch atom',atom)

  def create_fill_atom(self):
    '''
    Typed atom
    Fill the phone number for send sms
    '''
    atom = [
      # wait the form dialog popup in 10 seconds
      self.atom_factory.createInput('Phone number','input[data-testid="login_phone_number_input"]','17607614755',timeout=10),
      self.atom_factory.createChoice('Agree privacy','.semi-checkbox-inner-display',True),
    ]
    self.fill_atom = self.atom_factory.createArray('Fill phone number',atom)

  def create_send_atom(self):
    '''
    Typed atom
    Send the sms
    '''
    atom = [
      self.atom_factory.createClickable('Next step','div[data-testid="login_next_button"]'),
    ]
    self.send_atom = self.atom_factory.createArray('Send the sms',atom)

  def create_code_atom(self):
    '''
    Typed atom
    Fill in the auth code
    Only one character can be entered in the input field at a time
    It will receive a dynamic value
    '''
    self.code_atom = self.atom_factory.createInput('Char input','.code-input .semi-input','')

  def create_submit_atom(self):
    '''
    Typed atom
    Submit to login, this site will submit automatically after the auth code are filled
    '''
    pass

  def create_captcha_valid_period_atom(self):
    self.captcha_valid_period_atom = self.atom_factory.createData('Captcha valid period',5*60)
