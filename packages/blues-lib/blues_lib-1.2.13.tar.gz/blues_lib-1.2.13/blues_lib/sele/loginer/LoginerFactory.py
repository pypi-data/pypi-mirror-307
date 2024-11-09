from abc import ABC,abstractmethod

class LoginerFactory(ABC):
  def create_account(self):
    pass

  def create_mac(self):
    pass

  def create_qrcode(self):
    pass
