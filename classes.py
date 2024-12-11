class User:
    def __init__(self, userId, infos):
      self.id = userId,
      self.steps = infos
      self.email = None
      self.firstName = None
      self.lastName = None
      self.identification = None
      # {"type": None,"number": None}
      self.address = {
            "zip_code": None,
            "street_name": None,
            "street_number": None,
            "neighborhood": None,
            "city": None,
            "federal_unit": None
      }
class Usertest:
    def __init__(self, userId = 1, infos = [], email = "tiamaria@gmail.com", firstName = "vini", lastName = "pet",identification = 12345678909):
      self.id = userId,
      self.steps = infos
      self.email = email
      self.firstName = firstName
      self.lastName = lastName
      self.identification = identification
     