import re
from os import path
from urllib.parse import urlparse
from tld import get_fld

class BluesURL():

  @classmethod
  def get_domain(cls,url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

  @classmethod
  def get_main_domain(cls,url):
    return get_fld(url)
  
  @classmethod
  def get_file_name(cls,url,with_extension=True):
    parsed_url = urlparse(url)
    file_name = path.basename(parsed_url.path)
    if with_extension:
      return file_name
    else:
      return path.splitext(file_name)[0]

  @classmethod
  def get_extend_name(cls,file_name):
    return path.splitext(file_name)[1]

  @classmethod
  def get_file_path(cls,dir_path,file_name):
    return path.join(dir_path,file_name)

  @classmethod
  def get_file_dir(cls,file_path):
    '''
    Get the file path witout file name
    '''
    return path.dirname(file_path)

  @classmethod
  def rename_extend_name(cls,file_path,extend_name):
    if not extend_name:
      return file_path

    file_dir = cls.get_file_dir(file_path)
    pure_file_name = cls.get_file_name(file_path,False)
    new_file_name = '%s.%s' % (pure_file_name,extend_name)
    return path.join(file_dir,new_file_name)
    
