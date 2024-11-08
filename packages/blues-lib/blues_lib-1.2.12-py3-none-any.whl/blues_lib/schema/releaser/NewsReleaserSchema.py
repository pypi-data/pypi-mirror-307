from abc import ABC,abstractmethod
from .ReleaserSchema import ReleaserSchema

class NewsReleaserSchema(ReleaserSchema,ABC):

  CHANNEL = 'news'

  def __init__(self):
    self.limit = {
      'title_max_length':28,
      'content_max_length':3000,
      'image_max_length':9
    }
    
    super().__init__()

