import sys,os,re
from .BluesCookie import BluesCookie    
from .BluesStandardChrome import BluesStandardChrome   

sys.path.append(re.sub('blues_lib.*','blues_lib',os.path.realpath(__file__)))
from util.BluesConsole import BluesConsole   
from util.BluesPowerShell import BluesPowerShell    
from util.BluesType import BluesType    
from util.BluesFiler import BluesFiler    
from sele.loginer.Loginer import Loginer    

class BluesLoginChrome(BluesStandardChrome,BluesCookie):
  '''
  This class is used exclusively to open pages that can only be accessed after login
  There are three ways to complete automatic login:
    1. Login by a cookie string
    2. Login by a cookie file path
    3. Login by the BluesLoginer class
  '''
  
  # Maximum relogin times
  max_relogin_time = 1

  def __init__(self,url,loginer_or_cookie=None,login_element=None):
    '''
    Parameter:
      url {str} : the url will be opened
      loginer_or_cookie {Loginer|str} : 
        - when as str: it is the cookie string or local cookie file, don't support relogin
        - when as Loginer : it supports to relogin
      login_element {str} : the login page's element css selector
        some site will don't redirect, need this CS to ensure is login succesfully
    '''
    super().__init__()
    
    # current relogin times
    self.url = url
    self.loginer_or_cookie = loginer_or_cookie
    self.login_element = login_element
    self.loginer = None
    self.cookie_value = None
    self.cookie_file = None
    self.relogin_time = 0
    
    # extract the loginer_or_cookie
    self.__extract_fields()

    # open the page
    self.__open()

  def __extract_fields(self):
    if isinstance(self.loginer_or_cookie,Loginer):
      self.loginer = self.loginer_or_cookie
    elif isinstance(self.loginer_or_cookie,str):
      if BluesFiler.exists(self.loginer_or_cookie):
        self.cookie_file = self.loginer_or_cookie
      else:
        self.cookie_value = self.loginer_or_cookie

  def __open(self):
    
    # must open first, or can't add cookie
    self.open(self.url)

    if self.__has_input_cookie():
      self.__log_in_by_input_cookie()
    else:
      # if login file, will relogin by the loginer
      self.__log_in_by_default_cookie()
    
  def __has_input_cookie(self):
    return self.cookie_value or self.cookie_file

  def __log_in_by_input_cookie(self):
    '''
    log in by the input cookie
    '''
    input_cookie = None
    text = ''
    if self.cookie_value:
      input_cookie = self.cookie_value
      text = 'input cookie : %s' % input_cookie
    elif self.cookie_file:
      input_cookie = self.read_cookies(self.cookie_file)
      text = 'input file : %s' % self.cookie_file

    if input_cookie:
      self.__login_with_cookie(input_cookie,text)

  def __log_in_by_default_cookie(self):
    '''
    log in by the local default cookie file
    '''
    default_cookie = self.read_cookies()
    if not default_cookie:
      BluesConsole.info('[Step2] No defualt cookie : logged out, go to relogin')
      self.__relogin()
    else:
      if not self.__login_with_cookie(default_cookie,'Login by default cookie '):
        self.__relogin()

  def __login_with_cookie(self,cookie,text):
    # add cookie to the browser
    self.interactor.cookie.set(cookie) 
    # reopen the home page
    self.open(self.url)
    # Check if login successfully
    if self.__is_logged_in():
      BluesConsole.success('[Step2] %s : logged successfully' % text)
      return True
    else:
      BluesConsole.info('[Step2] %s : logged failure' % text)
      return False

  def __is_logged_in(self):
    '''
    Weather logged in 
    @return:
      {bool} : If you are not logged in, you are redirected to the login page
    '''
    if self.login_element:
      return not self.waiter.querier.query(self.login_element,timeout=5)
    else:
      return not self.waiter.ec.url_changes(self.url,5)
  
  def __relogin(self):
    if not self.loginer:
      BluesConsole.error('There is no loginer set up, so you cannot log in again.')
      return

    if self.relogin_time>=self.max_relogin_time:
      BluesConsole.error('Login failed, the maximum number of relogins has been reached.')
      return

    self.relogin_time+=1
    
    # Relogin and save the new cookies to the local file
    BluesConsole.info('Relogin using the %s' % type(self.loginer).__name__)
    self.loginer.login()
    
    # Refresh the page to get the new token in the document before reopen
    self.interactor.navi.refresh() 

    # Reopen the page using the new cookies
    self.__log_in_by_default_cookie()

