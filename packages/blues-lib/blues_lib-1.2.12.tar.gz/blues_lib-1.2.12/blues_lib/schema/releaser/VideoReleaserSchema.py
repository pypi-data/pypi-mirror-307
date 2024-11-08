import sys,os,re
from abc import ABC,abstractmethod
from .ReleaserSchema import ReleaserSchema
sys.path.append(re.sub('test.*','blues_lib',os.path.realpath(__file__)))
from sele.transformer.schema.SchemaValueReplacer import SchemaValueReplacer     
from util.BluesFiler import BluesFiler
from util.BluesCSV import BluesCSV
from util.BluesURL import BluesURL
from util.BluesConsole import BluesConsole

class VideoReleaserSchema(ReleaserSchema,ABC):

  CHANNEL = 'video'

  def __init__(self,material_index=0):
    self.limit = {
      'title_max_length':28,
      'video_max_size':'1GB'
    }
    # {list<Mateail>}
    self.materials = None
    self.material_index = material_index
    super().__init__()

  def __get_video_list(self):
    video_dir = 'D:\short-video'
    return BluesFiler.readfiles(video_dir)

  def __get_materials(self):
    video_csv = 'D:\short-video\list.csv'
    activities_rows = None
    try:
      activities_rows = BluesCSV.read_rows(video_csv)
    except Exception as e:
      BluesConsole.error('Read csv error : %s' % e)
      return None

    rows = []

    if not activities_rows:
      return None

    for row in activities_rows:
      if not row['activities'] or not row['video']:
        continue

      activitity_list = row['activities'].split('-')
      for activity in activitity_list:
        if not activity:
          continue
        rows.append({
          'material_title':activity,
          'material_video':row['video'],
        })
    return (rows if rows else None)

  def __get_materials_v1(self):
    files = self.__get_video_list()
    if not files:
      return None

    materials = []
    for file_path in files:
      file_name = BluesURL.get_file_name(file_path,False)
      materials.append({
        'material_title':file_name,
        'material_video':file_path,
      })

    BluesConsole.info('video list: %s' % materials)
    return materials

  def fill_fields(self):
    '''
    Cover the parent's method
    '''
    if not self.fill_atom:
      return

    materials = self.__get_materials()
    if not materials:
      return
    
    # keep all material list
    self.materials = materials
    index = self.material_index if self.material_index < len(self.materials) else -1
    material = materials[index]
    self.material = material

    # replace the placeholder
    self.set_video_fill_atom(material)

  def set_video_fill_atom(self,material):
    activity_switch = None
    if self.activity_atom:
      activity_switch = self.activity_atom.get_value()['switch']

    SchemaValueReplacer().handle({
      'atom':[self.fill_atom,activity_switch],
      'value':material, # set first as the default value
    })

    
