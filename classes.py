class User:
   def __init__(userId, infos = None):
      self.id = userId,
      email = infos.email,
      firstName = infos.firstName,
      lastName = infos.lastName,
      identification = {
            "type": infos.documentType,
            "number": infos.DocumentNumeber
      },
      address = {
            "zip_code": infos.zipCode,
            "street_name": infos.streetName,
            "street_number": infos.StreetNumber,
            "neighborhood": infos.neighborhood,
            "city": infos.city,
            "federal_unit": infos.federal_unit
      }

class Usertemp:
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
