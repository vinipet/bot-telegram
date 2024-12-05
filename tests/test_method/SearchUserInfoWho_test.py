import pytest
import bot
import classes
from unittest.mock import *

def test_user_as_dict_all_values_present():
   user = {
      "email": "user@example.com",
      "firstName": "John",
      "lastName": "Doe",
      "identification": "123456789"
   }
   result = bot.SearchUserInfoWhoIsNone(user)
   assert result == [] # nothing are missing

def test_user_as_dict_some_values_missing():
   user = {
      "email": "user@example.com",
      "firstName": "John"
   }
   result = bot.SearchUserInfoWhoIsNone(user)
   assert result == ["lastName", "identification"] # value missing

def test_user_as_dict_all_values_missing():
   user = {}
   result = bot.SearchUserInfoWhoIsNone(user)
   assert result == ['email', 'firstName', 'lastName', 'identification']  # value missing

def test_user_as_object_all_values_present():
   class User:
      email = "user@example.com"
      firstName = "John"
      lastName = "Doe"
      identification = "123456789"

   user = User()
   result = bot.SearchUserInfoWhoIsNone(user)
   assert result == []  # nothing are missing

def test_user_as_object_some_values_missing():
   class User:
      email = "user@example.com"
      lastName = "Doe"

   user = User()
   result = bot.SearchUserInfoWhoIsNone(user)
   assert result == ["firstName", "identification"]  # missing value

def test_user_as_object_all_values_missing():
   class User:
      email = None
      firstName = None
      lastName = None
      identification = None

   user = User()
   result = bot.SearchUserInfoWhoIsNone(user)
   assert result == ['email', 'firstName', 'lastName', 'identification']  # missing value

def test_user_with_empty_searching_info():
   user = {
      "email": "user@example.com",
      "firstName": "John"
   }
   result = bot.SearchUserInfoWhoIsNone(user, [])
   assert result == [] # nothing information to verify

def test_user_as_dict_no_matching_values():
   user = {}
   result = bot.SearchUserInfoWhoIsNone(user)
   assert result == ["email", "firstName", "lastName", "identification"]  # all are missing

def test_user_as_obj_with_not_atribute():
   class user():
      id = 123
   user = user()
   result = bot.SearchUserInfoWhoIsNone(user)
   assert result == ["email", "firstName", "lastName", "identification"]  # all are missing

def test_user_as_obj_search_random_value():
   class User:
      def __init__(self):
         self.email = None
         self.firstName = None
         self.lastName = None
         self.identification = None
   user = User()
   result = bot.SearchUserInfoWhoIsNone(user, ['cu', 'bct', 'penisGordo'])
   assert result == ['cu', 'bct', 'penisGordo']  # all are missing

def test_user_is_none():
   with  pytest.raises(TypeError):
      bot.SearchUserInfoWhoIsNone(None)
   
def test_user_is_string():
   with pytest.raises(TypeError):
      bot.SearchUserInfoWhoIsNone("invalid_string")

def test_user_is_list():
   with pytest.raises(TypeError):
      bot.SearchUserInfoWhoIsNone(["invalid", "list"])

def test_user_is_number():
   with pytest.raises(TypeError):
      bot.SearchUserInfoWhoIsNone(123)
