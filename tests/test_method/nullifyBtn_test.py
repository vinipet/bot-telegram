import pytest
import bot
import classes
from unittest.mock import *

def test_nullify_btn():
   btns = [
      [
            bot.types.InlineKeyboardButton("Button 1", callback_data="data1"),
            bot.types.InlineKeyboardButton("Button 2", callback_data="data2"),
      ],
      [
            bot.types.InlineKeyboardButton("Button 3", callback_data="data3"),
      ]
   ]
   result = bot.nullifyBtn(btns)
   assert isinstance(result, bot.types.InlineKeyboardMarkup)
   rows = result.keyboard  
   assert len(rows) == len(btns) 

   for row_result, row_expected in zip(rows, btns):
      assert len(row_result) == len(row_expected) 
      for btn_result, btn_expected in zip(row_result, row_expected):
            assert btn_result.text == btn_expected.text
            assert btn_result.callback_data == "None"


def test_nullify_btn_without_btn():
   btns = []
   result = bot.nullifyBtn(btns)
   assert isinstance(result, bot.types.InlineKeyboardMarkup)
   rows = result.keyboard  
   assert len(rows) == len(btns) 

   for row_result, row_expected in zip(rows, btns):
      assert len(row_result) == len(row_expected) 
      for btn_result, btn_expected in zip(row_result, row_expected):
            assert btn_result.text == btn_expected.text
            assert btn_result.callback_data == "None"


def test_nullify_btn_with_NoneText_btn():
   btns = [
      [
            bot.types.InlineKeyboardButton(None, callback_data=None),
            bot.types.InlineKeyboardButton(None, callback_data=None),
      ]
   ]
   result = bot.nullifyBtn(btns)
   assert isinstance(result, bot.types.InlineKeyboardMarkup)
   rows = result.keyboard  
   assert len(rows) == len(btns) 

   for row_result, row_expected in zip(rows, btns):
      assert len(row_result) == len(row_expected) 
      for btn_result, btn_expected in zip(row_result, row_expected):
            assert btn_result.text == btn_expected.text
            assert btn_result.callback_data == "None"