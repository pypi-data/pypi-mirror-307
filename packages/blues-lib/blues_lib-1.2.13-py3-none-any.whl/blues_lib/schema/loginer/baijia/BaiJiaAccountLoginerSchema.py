import sys,os,re
sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from schema.loginer.AccountLoginerSchema import AccountLoginerSchema

class BaiJiaAccountLoginerSchema(AccountLoginerSchema):
  
  # === create the base fields ===
  def create_log_in_atom(self):
    self.log_in_atom = self.atom_factory.createURL('Log in url','https://baijiahao.baidu.com/builder/theme/bjh/login')

  def create_proxy_atom(self):
    config = {
      'scopes': ['.*baijiahao.baidu.com.*'],
    }
    self.proxy_atom = self.atom_factory.createData('proxy config',config)

  def create_cookie_filter_atom(self):
    config = {
      'url_pattern':'/builder/rc/home',
      'value_pattern':None
    }
    self.cookie_filter_atom = self.atom_factory.createData('cookie filter config',config)
  
  # === create the account subtype fields ===
  def create_switch_atom(self):
    atom = [
      self.atom_factory.createClickable('switch to account mode','div[class^=btnlogin]'),
    ]
    self.switch_atom = self.atom_factory.createArray('switch atom',atom)

  def create_fill_atom(self):
    atom = [
      self.atom_factory.createInput('name','#pass-login-main input[name=userName]','17607614755'),
      self.atom_factory.createInput('password','#pass-login-main input[name=password]','Langcai10.'),
      self.atom_factory.createChoice('agree protocal','#pass-login-main input[name=isAgree]',True),
      self.atom_factory.createChoice('remember me','#pass-login-main input[name=memberPass]',True),
    ]
    self.fill_atom = self.atom_factory.createArray('fill atom',atom)

  def create_submit_atom(self):
    atom = [
      self.atom_factory.createClickable('submit','#pass-login-main input[type=submit]'),
    ]
    self.submit_atom = self.atom_factory.createArray('submit atom',atom)

