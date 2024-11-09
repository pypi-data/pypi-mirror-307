from abc import ABC,abstractmethod
from .ReleaserSchema import ReleaserSchema

class EventsReleaserSchema(ReleaserSchema,ABC):

  CHANNEL = 'events'

  def __init__(self):
    self.limit = {
      'content_max_length':1000,
      'image_max_length':9
    }
    super().__init__()
