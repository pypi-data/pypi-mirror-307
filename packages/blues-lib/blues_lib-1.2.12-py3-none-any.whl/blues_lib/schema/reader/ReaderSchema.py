import sys,os,re
from abc import ABC,abstractmethod
sys.path.append(re.sub('test.*','blues_lib',os.path.realpath(__file__)))
from atom.AtomFactory import AtomFactory     

class ReaderSchema(ABC):
  def __init__(self):

    # Decalare fields
    self.atom_factory = AtomFactory()

    # { URLAtom } the list page url
    self.url_atom = None
    # { ValueAtom } the material size would crawl
    self.size_atom = None
    # { ValueAtom } the max image size in a material
    self.image_size_atom = None
    # { BriefAtom } the brief atom
    self.brief_atom = None
    # { ArticleAtom } the article atom
    self.material_atom = None
    # { ValueAtom  of list} the author list
    self.author_atom = None

    # create the fields
    self.create()
  
  # final templte method
  def create(self):
    self.create_url_atom()
    self.create_size_atom()
    self.create_image_size_atom()
    self.create_brief_atom()
    self.create_material_atom()
    self.create_author_atom()

  # === steps method === 
  @abstractmethod
  def create_url_atom(self):
    pass

  def create_size_atom(self):
    self.size_atom = self.atom_factory.createData('Material size',1)

  def create_image_size_atom(self):
    self.image_size_atom = self.atom_factory.createData('Max image size in a material',9)

  @abstractmethod
  def create_brief_atom(self):
    pass

  @abstractmethod
  def create_material_atom(self):
    pass
  
  @abstractmethod
  def create_author_atom(self):
    pass


